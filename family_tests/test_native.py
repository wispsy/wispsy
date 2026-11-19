"""Actual POSIX application input and restoration, distinct from fake terminals."""
import json
import os
import select
import subprocess
import sys
import time
import unittest


@unittest.skipUnless(os.name == 'posix', 'native interactive profile requires POSIX')
class NativeApplicationTests(unittest.TestCase):
    def test_hypnosis_quit_restores_a_real_pseudo_terminal(self):
        import fcntl
        import pty
        import struct
        import termios
        master, slave = pty.openpty()
        fcntl.ioctl(slave, termios.TIOCSWINSZ, struct.pack('HHHH', 24, 80, 0, 0))
        before = termios.tcgetattr(slave)
        process = None
        output = bytearray()
        try:
            process = subprocess.Popen([sys.executable, '-I', '-m', 'hypnosis', 'terminal', '--text', 'hello'],
                stdin=slave, stdout=subprocess.PIPE, stderr=slave, env={**os.environ, 'TERM': 'xterm-256color'})
            deadline = time.monotonic() + 5
            while b'\x1b[?1049h' not in output and time.monotonic() < deadline:
                ready, _, _ = select.select([master], [], [], 0.05)
                if ready:
                    output.extend(os.read(master, 4096))
                if process.poll() is not None:
                    break
            self.assertIn(b'\x1b[?1049h', output)
            os.write(master, b'q')
            result, _ = process.communicate(timeout=5)
            self.assertIn(process.returncode, (0, 1))
            self.assertIn(json.loads(result)['status'], ('completed', 'canceled'))
            restored = termios.tcgetattr(slave)
            if sys.platform == 'darwin':
                # Darwin's PENDIN is transient kernel state, as in Carets's
                # existing real-terminal restoration qualification.
                restored[3] &= ~termios.PENDIN
                before[3] &= ~termios.PENDIN
            self.assertEqual(restored, before)
        finally:
            if process is not None and process.poll() is None:
                process.kill()
                process.communicate()
            if process is not None and process.stdout is not None:
                process.stdout.close()
            os.close(master)
            os.close(slave)
