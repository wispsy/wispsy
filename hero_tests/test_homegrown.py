from dataclasses import replace
import json
from pathlib import Path
import subprocess
import sys
from tempfile import TemporaryDirectory
import unittest

from engl import normalize_entry,parse_sentence
from hypnosis.data import Source,DataLimits,prepare_corpus,load_corpus,SourceApprovalError
from hypnosis.records import RunLedger,TrainingReceipt
from hypnosis.training import JobConfig,run_job
from thoughtform.recipes import HERO
from thoughtform.artifacts import load_artifact


class HomegrownIntegrationTests(unittest.TestCase):
    def test_engl_is_an_independent_language_component(self):
        value=normalize_entry({'word':'bright','lang_code':'en','pos':'adj',
            'forms':[{'form':'brighter','tags':['comparative']}],
            'senses':[{'glosses':['Giving light.']}]},source='fixture')
        self.assertEqual(value.lemma,'bright');self.assertEqual(value.upos,'ADJ')
        sentence=parse_sentence(('# sent_id = fixture\n# text = Birds fly.\n'
            '1\tBirds\tbird\tNOUN\t_\tNumber=Plur\t2\tnsubj\t_\t_\n'
            '2\tfly\tfly\tVERB\t_\t_\t0\troot\t_\t_\n'
            '3\t.\t.\tPUNCT\t_\t_\t2\tpunct\t_\t_\n').splitlines(),source='fixture')
        self.assertEqual(len(sentence.tokens),3)

    def test_approved_training_resume_specialization_and_fresh_process_receipts(self):
        with TemporaryDirectory() as directory:
            root=Path(directory);corpus=root/'corpus'
            with self.assertRaises(SourceApprovalError): Source('python3-vault','candidate')
            prepare_corpus([Source('internal-v1','recipe')],corpus,
                limits=DataLimits(documents_per_source=80,max_documents=80))
            receipt,documents=load_corpus(corpus)
            self.assertTrue(all(receipt['splits'][split]>0 for split in ('train','validation','test')))
            groups={}
            for value in documents: groups.setdefault(value['group'],set()).add(value['split'])
            self.assertTrue(all(len(split)==1 for split in groups.values()))
            recipe=replace(HERO,width=8,layers=1,heads=2,kv_heads=1,hidden=12,lora_rank=2)
            config=JobConfig('installed-hero',max_steps=2,block_size=4,max_seconds=30,evaluation_sequences=1)
            result=run_job(corpus,root/'hero',config,recipe=recipe)
            self.assertEqual(result['training']['step'],2)
            self.assertEqual(run_job(corpus,root/'hero',config,recipe=recipe),result)
            parent=load_artifact(root/'hero/artifact.json');original=(root/'hero/model.tft').read_bytes()
            child=replace(recipe,model_id='hero-coding',role='coding',parent_model_id='hero')
            specialized=run_job(corpus,root/'coding',replace(config,run_id='installed-coding',model_id='hero-coding'),
                recipe=child,parent_artifact=root/'hero/artifact.json')
            self.assertEqual(specialized['parent_sha256'],parent.receipt['checkpoint']['sha256'])
            self.assertEqual((root/'hero/model.tft').read_bytes(),original)
            code='''import sys
from hypnosis.records import RunLedger, TrainingReceipt
with RunLedger(sys.argv[1]) as ledger:
    values=ledger.recall(TrainingReceipt,'installed-coding')
    assert len(values)==1 and values[0].value.steps==2
'''
            subprocess.run([sys.executable,'-I','-c',code,str(root/'coding/receipts.sqlite')],check=True)
            self.assertEqual(result['evaluation']['heldout']['test']['status'],'measured')
            self.assertEqual(specialized['training']['selection']['documents_unknown'],0)
