"""Qualify exact installed family sources, native input and generated commands."""
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
from tempfile import TemporaryDirectory

ROOT = Path(__file__).resolve().parents[1]

RECEIPT = '''
from importlib import metadata
import json
from pathlib import Path
import sys
sources = json.loads(Path(sys.argv[1]).read_text())['sources']
installed = {}
for name, expected in sources.items():
    distribution = metadata.distribution(name)
    direct = json.loads(distribution.read_text('direct_url.json') or '{}')
    commit = direct.get('vcs_info', {}).get('commit_id')
    if commit != expected:
        raise RuntimeError(f'{name} source does not match the selected profile')
    installed[name] = {'version': distribution.version, 'commit': commit}
print(json.dumps(installed, sort_keys=True))
'''


def main():
    if sys.version_info < (3, 14):
        raise RuntimeError('The family profile requires Python 3.14+')
    directory = Path(sys.argv[1]).resolve()
    artifacts = sorted([*directory.glob('*.whl'), *directory.glob('*.tar.gz')])
    if len(artifacts) != 2:
        raise ValueError('Select exactly one wheel and one source distribution')
    receipts = []
    for artifact in artifacts:
        with TemporaryDirectory() as temporary:
            outside = Path(temporary)
            environment = outside / 'env'
            subprocess.run(['uv', 'venv', str(environment), '--python', sys.executable], check=True)
            python = environment / ('Scripts/python.exe' if sys.platform == 'win32' else 'bin/python')
            subprocess.run(['uv', 'pip', 'install', '--python', str(python), str(artifact) + '[family]'], check=True, cwd=outside)
            subprocess.run([str(python), '-I', '-m', 'unittest', 'discover', '-s', str(ROOT / 'family_tests'), '-v'], check=True, cwd=outside)
            manifest = ROOT / 'docs/cohesion-block-b/sources-v1.json'
            result = subprocess.run([str(python), '-I', '-c', RECEIPT, str(manifest)], check=True, cwd=outside,
                                    capture_output=True, text=True)
            installed = json.loads(result.stdout)
            project = outside / 'progress-desk'
            subprocess.run([str(python), '-I', '-m', 'compose_application.projects', str(project),
                '--name', 'progress-desk', '--profile', 'terminal'], check=True, cwd=outside)
            subprocess.run(['uv', 'pip', 'install', '--python', str(python), '--no-deps', str(project)], check=True, cwd=outside)
            process_environment = dict(os.environ)
            process_environment.pop('PYTHONPATH', None)
            command = environment / ('Scripts/progress-desk.exe' if sys.platform == 'win32' else 'bin/progress-desk')
            for invocation in ([str(python), '-I', '-m', 'progress_desk', 'check'], [str(command), 'check']):
                result = subprocess.run(invocation, cwd=outside, env=process_environment, check=True,
                                        capture_output=True, text=True, timeout=10)
                if json.loads(result.stdout)['status'] != 'completed' or result.stderr:
                    raise RuntimeError('Generated terminal command did not complete cleanly')
            subprocess.run(['uv', 'pip', 'check', '--python', str(python)], check=True, cwd=outside)
            receipts.append({'artifact': artifact.name, 'sha256': hashlib.sha256(artifact.read_bytes()).hexdigest(),
                'python': sys.version.split()[0], 'platform': sys.platform, 'installed': installed,
                'native_terminal': 'POSIX pseudo-terminal' if os.name == 'posix' else 'not qualified'})
            print(json.dumps(receipts[-1], sort_keys=True), flush=True)
    Path('family-qualification.json').write_text(json.dumps({'schema': 1, 'artifacts': receipts}, indent=2) + '\n')


if __name__ == '__main__':
    main()
