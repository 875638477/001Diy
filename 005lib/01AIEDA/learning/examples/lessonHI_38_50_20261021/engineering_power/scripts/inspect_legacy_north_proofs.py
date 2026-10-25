from pathlib import Path
import json
H=Path(r'D:/001DIY/005lib/01AIEDA/learning/examples/lessonHI_38_50_20261021');O=H/'engineering_power'
for v in ['2L','4L']:
 p=H/('batches/clearance_remaining_2L_b016_SH2_common_fixed.json' if v=='2L' else 'batches/clearance_remaining_4L_b016_tail_cleanup.json');q=json.loads(p.read_text());print(v,[(k,type(x).__name__,len(x) if isinstance(x,(list,dict)) else '') for k,x in q.items()]);out=[]
 def walk(x,path):
  if isinstance(x,dict):
   if any(a in x for a in ['toAlias','fromAlias','alias','aliasName','aliasId','targetAlias']) and any(s in json.dumps(x) for s in ['PC13','PC14','PC15']):out.append(dict(path=path,value=x))
   for k,a in x.items():
    if isinstance(a,(dict,list)):walk(a,path+'.'+k)
  elif isinstance(x,list):
   for i,a in enumerate(x):walk(a,path+'['+str(i)+']')
 walk(q,'root');(O/f'readouts/North_legacy_proofs_{v}.json').write_text(json.dumps(out,indent=2));print('ALIASES',json.dumps(out)[:10000])
 print('SAMPLE',q['aliases'][:3],q['proofs'][:3]);print('NORTH_ALIASES',[(i,a) for i,a in enumerate(q['aliases']) if any(z in json.dumps(a) for z in ['PC13','PC14','PC15'])])

 print('RELEVANTPROOFS',[(i,a) for i,a in enumerate(q['proofs']) if a.get('from') in ['U1.2','U1.3','U1.4'] or a.get('to') in [z['id'] for z in q['aliases'] if any(t in str(z) for t in ['PC13','PC14','PC15'])]])
