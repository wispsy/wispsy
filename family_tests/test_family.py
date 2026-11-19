"""Installed cross-library behavior; no optional skips in this selected profile."""
import asyncio
from contextlib import aclosing
import io
import unittest

from carets import Program
from carets.testing import SnapshotRenderer
from hypnosis import Harness
from hypnosis.execution import model_text
from hypnosis.terminal import HarnessTerminal, visible
from paracosm import Habitat, Resident, Snapshot, World
from thoughtform import Action, Being, GenerationConfig, ModelDefinition
from thoughtform.thoughtformula import ThoughtformulaModel
from thoughtformula import BPETokenizer, ModernMicroGPT


class FamilyTests(unittest.IsolatedAsyncioTestCase):
    async def test_real_model_has_equivalent_headless_and_terminal_output(self):
        tokenizer = BPETokenizer()
        tokenizer.train('hello world', max_merges=0)
        model = ModernMicroGPT(len(tokenizer.vocab), n_embd=8, n_heads=2, n_kv_heads=1,
            n_layers=1, n_experts=1, moe_top_k=1, expert_hidden=8, lora_rank=2)
        definition = ModelDefinition('tiny', 'thoughtformula', 'synthetic-untrained',
            GenerationConfig(max_new_tokens=3, temperature=0))
        adapter = ThoughtformulaModel(definition, model, tokenizer)
        events = [event async for event in Harness().stream(lambda: model_text(adapter, 'hello'), run_id='headless')]
        self.assertEqual(events[-1].kind, 'completed')
        expected = ''.join(event.text for event in events)
        terminal = HarnessTerminal(lambda: model_text(adapter, 'hello'), exit_on_completion=True)
        renderer = SnapshotRenderer()
        program = terminal.program = Program(terminal, renderer=renderer, output_stream=io.StringIO(), stream_buffer=2)
        await asyncio.wait_for(program.run([], stop_on_eof=False, commands=[terminal.start()]), 5)
        self.assertEqual(terminal.status, 'completed')
        self.assertEqual(terminal.output, visible(expected))
        self.assertIn('completed', renderer.latest)
        alice, bob = Being('alice', 'Alice', model=definition), Being('bob', 'Bob', model=definition)
        world = World(Snapshot('family', (Habitat('woods', 'The Woods'),),
            (Resident(alice, 'woods'), Resident(bob, 'woods'))))
        result = world.step({})
        self.assertEqual(result.snapshot.tick, 1)
        self.assertEqual([action.actor_id for action in result.actions], ['alice', 'bob'])

    async def test_habitat_proposals_remain_subject_to_world_authority(self):
        world = World(Snapshot('family', (Habitat('woods', 'Woods', mind=Being('forest', 'Forest')),
                                          Habitat('village', 'Village')),
            (Resident(Being('alice', 'Alice'), 'woods'),)))
        class Mind:
            def decide(self, observation):
                return Action(observation.actor_id, 'condition', 'village', 'rain')
        before = world.snapshot
        with self.assertRaises(ValueError):
            world.step({'forest': Mind()})
        self.assertIs(world.snapshot, before)
