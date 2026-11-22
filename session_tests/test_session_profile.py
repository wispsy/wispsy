from dataclasses import replace
import json
from pathlib import Path
import subprocess
import sys
from tempfile import TemporaryDirectory
import unittest

from hypnosis.data import Source,DataLimits,prepare_corpus
from hypnosis.data.sources import bind_source
from hypnosis.training import JobConfig,run_job
from hypnosis.checkpoints import CheckpointCollection,index_run
from thoughtform.recipes import recipe_for


class SessionProfileTests(unittest.TestCase):
    def test_approved_markdown_balanced_sampling_continuation_and_collection(self):
        with TemporaryDirectory() as directory:
            root=Path(directory);vault=root/'python3_vault';(vault/'tutorials').mkdir(parents=True)
            for n in range(12):
                (vault/f'tutorials/lesson-{n}.md').write_bytes(
                    f'# Lesson {n}\n\nA function returns a value. α = {n}\n\n```python\ndef solve(x):\n    return x + {n}\n```\n'.encode())
            source=Source('python-vault-tutorials',str(vault));source=replace(source,fingerprint=bind_source(source)['fingerprint'])
            corpus=root/'corpus'
            prepare_corpus([Source('internal-v1','recipe'),source],corpus,
                limits=DataLimits(documents_per_source=40,max_documents=100))
            recipe=replace(recipe_for('hero','balanced-v2'),width=8,layers=1,heads=2,kv_heads=1,hidden=12,lora_rank=2)
            config=JobConfig('profile-first',profile='balanced-v2',max_steps=2,block_size=4,
                max_sequences=30,evaluation_sequences=1,checkpoint_interval=1)
            first=run_job(corpus,root/'first',config,recipe=recipe)
            selection=first['training']['selection']
            self.assertEqual(set(selection['sources']),{'internal-v1','python-vault-tutorials'})
            self.assertEqual(selection['documents_unknown'],0)
            self.assertEqual(len(first['training']['consumed_sources']['windows']),2)
            saved=(root/'first/model.tft').read_bytes()
            continued=run_job(corpus,root/'continued',replace(config,run_id='profile-continued'),
                recipe=recipe,continue_artifact=root/'first/artifact.json')
            self.assertEqual((continued['training']['step'],continued['training']['steps_this_job']),(4,2))
            self.assertEqual(saved,(root/'first/model.tft').read_bytes())
            database=root/'collection.sqlite'
            index_run(root/'first',database,root);index_run(root/'continued',database,root)
            self.assertEqual(index_run(root/'continued',database,root)['added'],0)
            result=subprocess.run([sys.executable,'-I','-m','hypnosis','checkpoints',str(database),str(root),
                '--model-id','hero','--profile','balanced-v2'],capture_output=True,text=True,check=True)
            records=json.loads(result.stdout)['checkpoints']
            self.assertEqual(len(records),6)
            self.assertTrue(all(record['corpus_sha256']==first['corpus_sha256'] for record in records))
