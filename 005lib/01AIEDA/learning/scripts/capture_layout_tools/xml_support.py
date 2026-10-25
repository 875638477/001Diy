"""Read-only inventory of official Capture XML; no CAD or design writes.
Geometric transforms and displayed strings needing native confirmation are labelled.
"""
import argparse,collections,hashlib,json,pathlib,xml.etree.ElementTree as E
import sys
sys.path.insert(0,str(pathlib.Path(__file__).resolve().parent))

def d(e,path='Defn'):
 x=e.find(path) if e is not None else None
 return dict(x.attrib) if x is not None else {}
def val(e,path,key='val',default=''):
 return d(e,path).get(key,default)
def num(v):
 try:return int(v)
 except (ValueError,TypeError):
  try:return float(v)
  except (ValueError,TypeError):return v
def props(e,tag):return {x.get('name',''):x.get('val','') for p in e.findall(tag) for x in p.findall('Defn')}
def canon(e,context='',mode='full'):
 """Sort children, preserving every semantic attr incl pin position; omit IDs/path metadata.
 full candidate ignores only object's self name/cellname, never user values/pins/footprints.
 visual candidate deliberately excludes value/property defaults; NOT a merge approval.
 """
 if mode=='visual' and (e.tag.endswith('UserProp') or e.tag in ('PartValue','Reference','ContentsLibName','ContentsViewName','ContentsViewType','SymbolDisplayProp')):return None
 a=dict(e.attrib)
 for k in ['dbId','refInstId','sourceLibName','libName']:a.pop(k,None)
 if e.tag=='Defn' and context in ['Package','LibPart','OffPageSymbol','GlobalSymbol','PortSymbol']:
  a.pop('CellName',None);a.pop('name',None)
 children=[canon(x,e.tag,mode) for x in e]
 return [e.tag,sorted(a.items()),sorted([x for x in children if x is not None],key=lambda z:json.dumps(z,ensure_ascii=True)),(e.text or '').strip()]
def signature(e,mode='full'):return hashlib.sha256(json.dumps(canon(e,mode=mode),ensure_ascii=True,separators=(',',':')).encode()).hexdigest()
def save_json(p,obj):p.write_text(json.dumps(obj,ensure_ascii=False,indent=2),encoding='utf-8')
def save_lines(p,rows):
 with p.open('w',encoding='utf-8',newline='\n') as f:
  for row in rows:f.write(json.dumps(row,ensure_ascii=False,separators=(',',':'))+'\n')
def font(e,path):return {k:(v if k=='name' else num(v)) for k,v in d(e,path).items()}
def transform(x,y,owner):
 # Candidate only. Exact owner transform must be compared to native absolute hotspot.
 m=int(owner.get('mirror','0'));r=int(owner.get('rotation','0'))
 if m in (1,3):x=-x
 if m in (2,3):y=-y
 for _ in range(r%4):x,y=-y,x
 return [x+int(owner.get('locX','0')),y+int(owner.get('locY','0'))]

