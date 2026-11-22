"""Installed application profile; optional components may not silently skip."""
import asyncio
from contextlib import aclosing
from dataclasses import replace
import io
import json
import os
from pathlib import Path
import subprocess
import sys
from tempfile import TemporaryDirectory
import unittest

from carets import KeyMsg
from carets.testing import TestProgram
from hypnosis.application import run_application_demo
from hypnosis.process import ProcessRun
from hypnosis.workbench import Workbench, ProgressMsg
from hypnosis.tools import digest
from wispsy.application import StatusDesk


class ApplicationFamilyTests(unittest.IsolatedAsyncioTestCase):
    async def test_independent_shell_consumers_and_actual_service_outcomes(self):
        report = await run_application_demo()
        self.assertEqual(report.status, 'completed', report.receipt())
        self.assertEqual([a['passed'] for a in report.verification['attempts']], [False, True])
        workbench = Workbench(run_application_demo)
        workbench._worker_result['report'] = report
        workbench.update(ProgressMsg({'kind': 'outcome', 'status': report.status}))
        for model in (workbench, StatusDesk()):
            async with TestProgram(model) as app:
                await app.resize(19, 6)
                app.assert_fits(19, 6)
                await app.resize(100, 24)
                app.assert_fits(100, 24)
            self.assertEqual(app.terminal.restore_count, 1)
        self.assertEqual(report.trials.recommendation, 'candidate')
        decision = report.trials.promote('candidate', expected_report_sha256=digest(report.trials.receipt()))
        self.assertEqual(decision.config_id, 'candidate')

    async def test_actual_process_stream_and_unchanged_single_document_command(self):
        run = ProcessRun([sys.executable, '-I', '-m', 'hypnosis', 'stream', '--text', 'hello 界'])
        async with aclosing(run.stream()) as events:
            values = [event async for event in events]
        self.assertTrue(run.outcome.transport_ok, run.outcome.receipt())
        self.assertEqual(run.outcome.status, 'completed')
        self.assertEqual(''.join(v['text'] for v in values), 'hello 界')
        result = await asyncio.to_thread(subprocess.run,
            [sys.executable, '-I', '-m', 'hypnosis', 'demo', '--text', 'hello'], capture_output=True, text=True, timeout=5)
        self.assertEqual((result.returncode, result.stderr), (0, ''))
        self.assertEqual(json.loads(result.stdout)['text'], 'hello')

    async def test_native_artifact_probe_preserves_zero_step_checkpoint(self):
        from thoughtformula import BPETokenizer, TrainingConfig, TrainingState, save_training_checkpoint
        from thoughtform.recipes import HERO, initialize
        from thoughtform.artifacts import artifact_metadata, publish_artifact
        with TemporaryDirectory() as temporary:
            root = Path(temporary)
            tokenizer = BPETokenizer()
            tokenizer.train(''.join(chr(i) for i in range(32, 127))+'\n', max_merges=0)
            recipe = replace(HERO, width=8, layers=1, heads=2, kv_heads=1, experts=1, hidden=8, lora_rank=2)
            checkpoint = root/'model.tft'
            save_training_checkpoint(checkpoint, initialize(recipe, tokenizer), tokenizer,
                TrainingConfig(block_size=4), TrainingState(), metadata=artifact_metadata(recipe, 'a'*64))
            artifact = root/'artifact.json'
            publish_artifact(artifact, checkpoint, recipe, corpus_sha256='a'*64)
            original = checkpoint.read_bytes()
            report = await run_application_demo(artifact=str(artifact), prompt='1')
            self.assertTrue(report.verification['attempts'])
            self.assertEqual(report.verification['attempts'][0]['verification_code'], 'syntax_only')
            self.assertEqual(original, checkpoint.read_bytes())


@unittest.skipUnless(os.name == 'posix', 'Native console evidence is POSIX only')
class NativeApplicationTests(unittest.TestCase):
    def test_actual_application_cli_quits_and_restores_terminal(self):
        import pty
        import select
        import termios
        master, slave = pty.openpty()
        original = termios.tcgetattr(slave)
        child = subprocess.Popen([sys.executable, '-I', '-m', 'hypnosis', 'app'], stdin=slave, stderr=slave, stdout=subprocess.PIPE)
        try:
            self.assertTrue(select.select([master], [], [], 8)[0], 'No application frame')
            os.read(master, 8192)
            os.write(master, b'q')
            output, _ = child.communicate(timeout=8)
            result = json.loads(output)
            self.assertIn(result['status'], ('completed', 'canceled'))
            self.assertIn(child.returncode, (0, 1))
            restored = termios.tcgetattr(slave)
            if sys.platform == 'darwin':
                restored[3] &= ~termios.PENDIN
                original[3] &= ~termios.PENDIN
            self.assertEqual(restored, original)
        finally:
            if child.poll() is None:
                child.kill()
                child.communicate()
            os.close(master)
            os.close(slave)
