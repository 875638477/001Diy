from pathlib import Path
import sys,json,dataclasses,collections,hashlib,re
J=Path(r'D:\001DIY\005lib\01AIEDA\learning\examples\lessonJK_51_59_20261022');sys.path.insert(0,str(J/'tooling/packages'))
from gerbonara import GerberFile
from gerbonara.utils import MM
def canon(a):
 if dataclasses.is_dataclass(a):return canon(dataclasses.asdict(a))
 if isinstance(a,dict):return {str(k):canon(v)for k,v in a.items()}
 if isinstance(a,(tuple,list)):return [canon(x)for x in a]
 if isinstance(a,float):return round(a,8)
 if isinstance(a,(int,str,bool))or a is None:return a
 return str(a)
def key(g):return collections.Counter(json.dumps(canon(p),sort_keys=True)for o in g.objects for p in o.to_primitives(unit=MM))
source=J/'exports/newstack_4L_TRAINING_NOT_FOR_FAB';old=J/'exports/J55_corrected_4L_TRAINING_NOT_FOR_FAB';checks=[];changed=[];same=[]
for p in sorted(source.glob('*.art')):
 q=old/p.name;g=GerberFile.open(p);h=GerberFile.open(q);equal=key(g)==key(h)
 layout=re.search(r'^G04 Layout Name:\s+(.+?)\*$',p.read_text(encoding='ascii'),re.M)
 checks.append({'name':p.stem+' actual header references newstack source board','pass':layout is not None and layout[1]=='JK_4L_L2_GND_L3_V3V3_STACK_TRAINING_NOT_RELEASED.brd'})
 if equal:same.append(p.stem)
 else:changed.append({'film':p.stem,'oldObjectCount':len(h.objects),'newObjectCount':len(g.objects)})
 if p.stem not in ['L2','L3']:checks.append({'name':p.stem+' unchanged outside requested inner plane modification','pass':equal})
checks.append({'name':'Exactly L2 and L3 CAM geometries changed','pass':[x['film']for x in changed]==['L2','L3']})
p=J/'native/4L/JK_4L_L2_GND_L3_V3V3_STACK_TRAINING_NOT_RELEASED.brd';sha=hashlib.sha256(p.read_bytes()).hexdigest().upper();checks.append({'name':'Native output board exact known SHA','pass':sha=='471176A9B25BA8DEF9F117AEFB1E9220CBCBEBBAC5191BCBC6E228F52831F3F9'})
d={'sourceBoard':str(p),'sourceSHA256':sha,'checks':checks,'passed':sum(x['pass']for x in checks),'failures':[x for x in checks if not x['pass']],'changedFilms':changed,'unchangedFilms':same,'electricalNetIdentity':'Read from fresh native database in separate independent audit; ordinary Gerber cannot prove GND/V3V3','release':False}
(J/'review/independent_CAM_NEWSTACK/geometry_delta.json').write_text(json.dumps(d,ensure_ascii=False,indent=2),encoding='utf8')
print(json.dumps({'passed':d['passed'],'total':len(checks),'failures':d['failures'],'changed':changed}))
