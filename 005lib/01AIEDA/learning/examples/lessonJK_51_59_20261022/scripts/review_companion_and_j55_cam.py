import pathlib,sys,json,re,hashlib,dataclasses,collections,base64
J=pathlib.Path(r'D:\001DIY\005lib\01AIEDA\learning\examples\lessonJK_51_59_20261022')
sys.path[:0]=[str(J/'tooling/packages'),str(J.parents[2]/'learning/tools/pymupdf_1_28_2')]
from gerbonara import GerberFile
from gerbonara.utils import MM
import pymupdf
OUT=J/'review/companion_and_J55_CAM';OUT.mkdir(exist_ok=True)
def dump(p,d):p.write_text(json.dumps(d,ensure_ascii=False,indent=2),encoding='utf8')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def canon(a):
 if dataclasses.is_dataclass(a):return canon(dataclasses.asdict(a))
 if isinstance(a,dict):return {str(k):canon(v) for k,v in a.items()}
 if isinstance(a,(tuple,list)):return [canon(x) for x in a]
 if isinstance(a,float):return round(a,8)
 if isinstance(a,(int,str,bool)) or a is None:return a
 return str(a)
def primitive_counter(g):
 return collections.Counter(json.dumps(canon(p),sort_keys=True) for o in g.objects for p in o.to_primitives(unit=MM))
reports={}
for v in ['2L','4L']:
 out=OUT/v;out.mkdir(exist_ok=True)
 a=J/f'exports/native_{v}_TRAINING_NOT_FOR_FAB'
 b=J/f'exports/J55_corrected_{v}_TRAINING_NOT_FOR_FAB'
 diffs=[];unchanged=[];checks=[]
 for p in sorted(a.glob('*.art')):
  q=b/p.name;g=GerberFile.open(p);h=GerberFile.open(q)
  equal=primitive_counter(g)==primitive_counter(h)
  if equal:unchanged.append(p.stem)
  else:diffs.append({'film':p.stem,'oldObjects':len(g.objects),'newObjects':len(h.objects)})
  if p.stem!='PDFTOP':checks.append({'name':'J55 preserved non-target Film geometry '+p.stem,'pass':equal})
 checks.append({'name':'Only assembly REFDES Film PDFTOP geometry changed','pass':[d['film'] for d in diffs]==['PDFTOP']})
 source=J/f'exports/supplement_{v}_THREE_TEXTS_TRAINING'
 expected={'REFDES_SILK_TOP':'REF DES/SILKSCREEN_TOP','REFDES_ASSEMBLY_TOP':'REF DES/ASSEMBLY_TOP','VALUE_ASSEMBLY_TOP':'COMPONENT VALUE/ASSEMBLY_TOP'}
 checks.append({'name':'Exactly three companion Film files','pass':set(p.stem for p in source.glob('*.art'))==set(expected)})
 panels=[];stats=[]
 for stem,layer in expected.items():
  p=source/(stem+'.art');raw=p.read_text(encoding='ascii');g=GerberFile.open(p)
  actual=re.findall(r'^G04 Layer:\s+(.+?)\*$',raw,re.M)
  checks.extend([{'name':stem+' only requested native class/subclass','pass':actual==[layer]},{'name':stem+' nonempty MM3.6 geometry','pass':bool(g.objects) and g.import_settings.unit==MM and g.import_settings.number_format==(3,6)}])
  svg=str(g.to_svg(margin=1));(out/(stem+'.svg')).write_text(svg,encoding='utf8')
  doc=pymupdf.open('svg',svg.encode());pix=doc[0].get_pixmap(matrix=pymupdf.Matrix(2,2),alpha=False);pix.save(str(out/(stem+'.png')))
  panels.append((stem,len(g.objects),base64.b64encode(pix.tobytes('png')).decode()))
  stats.append({'file':str(p),'sha256':sha(p),'headerLayers':actual,'objects':len(g.objects),'bounds':g.bounding_box(unit=MM)})
 chunks=[]
 for i,(name,count,data) in enumerate(panels):
  x=i*100
  chunks.append(f'<rect x="{x}" y="10" width="100" height="90" fill="white" stroke="#ddd"/><text x="{x+2}" y="16" font-size="3">{name}</text><text x="{x+2}" y="21" font-size="2.5">{count} vector objects; native 80 text instances</text><image x="{x+1}" y="24" width="98" height="74" href="data:image/png;base64,{data}"/>')
 svg='<svg xmlns="http://www.w3.org/2000/svg" width="300mm" height="101mm" viewBox="0 0 300 101"><rect width="300" height="101" fill="white"/><text x="2" y="6" font-size="4">JK56 '+v+' actual companion text CAM - TRAINING NOT FOR FAB</text>'+''.join(chunks)+'</svg>'
 (out/'THREE_TEXT_FILMS.svg').write_text(svg,encoding='utf8');doc=pymupdf.open('svg',svg.encode());doc[0].get_pixmap(matrix=pymupdf.Matrix(1.5,1.5)).save(str(out/'THREE_TEXT_FILMS.png'))
 reports[v]={'checks':checks,'passed':sum(c['pass']for c in checks),'failures':[c for c in checks if not c['pass']],'unchangedOriginalFilms':unchanged,'changedOriginalFilms':diffs,'companionFilms':stats,'nativeTextInstanceCountPerRequestedLayer':80,'textCountSource':'J55 fresh native instance audit, not OCR or Gerber stroke count','visualReviewed':False,'release':False}
 dump(out/'report.json',reports[v])
 print(v,json.dumps({'checks':len(checks),'passed':reports[v]['passed'],'failures':reports[v]['failures'],'changed':diffs}))
dump(OUT/'summary.json',reports)
