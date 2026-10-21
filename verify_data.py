#!/usr/bin/env python3
"""Verify the published non-ranking Pantanal comparative dataset (standard library only)."""
from pathlib import Path
import csv,json,collections
root=Path(__file__).parent
obj=json.loads((root/'RESULTS.json').read_text(encoding='utf-8'))
faq=json.loads((root/'FAQ_DATA.json').read_text(encoding='utf-8'))
meta=json.loads((root/'metadata.json').read_text(encoding='utf-8'))
def read(name):
 with open(root/name,encoding='utf-8-sig',newline='') as fh:return list(csv.DictReader(fh))
participants=obj['participants']; matrix=read('OBSERVATION_MATRIX.csv'); claims=read('FACT_CLAIM_MAP.csv'); sources=read('SOURCE_REGISTER.csv')
assert len(participants)==len(matrix)==15
assert len(claims)==105 and len(sources)==22
assert obj['researchId']==faq['researchId']==meta['researchId']
assert obj['version']==meta['version']=='1.0.0'
assert [p['candidateId'] for p in participants]==[r['candidate_id'] for r in matrix]
assert obj['scoring']['applies'] is False
assert obj['scoring']['ranks'] is None and obj['scoring']['scores'] is None and obj['scoring']['weights'] is None
assert meta['scoring']['applies'] is False
sids={s['source_id'] for s in sources}
statuses=set(obj['evidenceStatusVocabulary'])
assert len(statuses)==5
cnt=collections.Counter()
for p in participants:
 assert len(p['attributes'])==7 and p['officialSourceId'] in sids
 for f,v in p['attributes'].items():
  assert v['status'] in statuses
  cnt[(p['candidateId'],f)]+=1
assert len(cnt)==105
assert len(faq['items'])>=8
for c in claims:
 assert (c['candidate_id'],c['attribute']) in cnt
 assert c['evidence_status'] in statuses
 for sid in c['source_ids'].split(';'):
  assert sid.strip() in sids
print('PASS: 15 organizers / 7 fields / 105 claims / 22 source records / no rank or scores')
