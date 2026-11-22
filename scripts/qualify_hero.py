"""Install the independent homegrown profile and verify its exact source pins."""
import hashlib
import json
from pathlib import Path
import subprocess
import sys
from tempfile import TemporaryDirectory

from qualify_family import RECEIPT

ROOT=Path(__file__).resolve().parents[1]


def qualify(directory, *, manifest_name="hero-sources-v1.json", test_folder="hero_tests",
            receipt_name="hero-qualification.json", schema="hero-homegrown-sources/1", hypnosis_extras="training",
            claim="installed composition and tiny learning fixtures only"):
    if sys.version_info<(3,14): raise RuntimeError('Hero qualification requires Python 3.14+')
    directory=Path(directory).resolve()
    artifacts=sorted([*directory.glob('*.whl'),*directory.glob('*.tar.gz')])
    if len(artifacts)!=2: raise ValueError('Select one wheel and one source distribution')
    manifest=ROOT/'docs/cohesion-block-b'/manifest_name
    selected=json.loads(manifest.read_text())
    if selected['schema']!=schema: raise ValueError('Unsupported homegrown profile')
    receipts=[]
    for artifact in artifacts:
        with TemporaryDirectory() as temporary:
            outside=Path(temporary);environment=outside/'env'
            subprocess.run(['uv','venv',str(environment),'--python',sys.executable],check=True)
            python=environment/('Scripts/python.exe' if sys.platform=='win32' else 'bin/python')
            requirement='hypnosis['+hypnosis_extras+'] @ git+https://github.com/wispsy/hypnosis.git@'+selected['sources']['hypnosis']
            subprocess.run(['uv','pip','install','--python',str(python),str(artifact),requirement],check=True,cwd=outside)
            subprocess.run([str(python),'-I','-m','unittest','discover','-s',str(ROOT/test_folder),'-v'],check=True,cwd=outside)
            verified=subprocess.run([str(python),'-I','-c',RECEIPT,str(manifest)],check=True,cwd=outside,capture_output=True,text=True)
            subprocess.run(['uv','pip','check','--python',str(python)],check=True,cwd=outside)
            receipt={'artifact':artifact.name,'sha256':hashlib.sha256(artifact.read_bytes()).hexdigest(),
                'python':sys.version.split()[0],'platform':sys.platform,'installed':json.loads(verified.stdout),
                'profile':selected['schema'],'claim':claim}
            receipts.append(receipt);print(json.dumps(receipt,sort_keys=True),flush=True)
    Path(receipt_name).write_text(json.dumps({'schema':1,'artifacts':receipts},indent=2)+'\n')


if __name__=='__main__': qualify(sys.argv[1])
