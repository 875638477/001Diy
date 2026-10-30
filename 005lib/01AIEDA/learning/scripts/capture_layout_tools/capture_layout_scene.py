"""Offline Capture XML full scene, ink collision candidates and display-only plan.
Never loads Capture, opens a DSN or writes a design. Anchor assumptions are explicit.
"""
import argparse,collections,csv,hashlib,html,json,math,pathlib,subprocess,sys,xml.etree.ElementTree as E
sys.path.insert(0,str(pathlib.Path(__file__).resolve().parent))
from _dependencies import configure
configure()
from shapely.geometry import Polygon,LineString,Point,box
from shapely.ops import unary_union
from shapely.strtree import STRtree
from shapely import from_wkb
from shapely.affinity import affine_transform,translate,rotate
from font_metrics_gdi import measure
from xml_support import d,val,font,transform as legacy_transform,save_json,save_lines
from native_affine import read_frames,bind_part,apply_frame

def transform(x,y,owner):
 return apply_frame(x,y,owner,legacy_transform)

def table(p):
 if p and p.exists():return list(csv.DictReader(p.open(encoding='utf-8-sig',newline=''),delimiter='\t'))
 return []
def n(x,default=0):
 try:return float(x)
 except (ValueError,TypeError):return default
def text_path(m):
 # GDI TextOut path uses nested contours. XOR implements alternate fill and preserves counters.
 g=Polygon()
 for ring in m['contours']:
  if len(ring)<4:continue
  p=Polygon(ring)
  if not p.is_valid:p=p.buffer(0)
  if not p.is_empty:g=g.symmetric_difference(p)
 return g
class Scene:
 def __init__(self,a):
  self.a=a;self.root=E.parse(a.xml).getroot();self.text=[];self.geom=[];self.unresolved=[];self.metrics={};self.fontissues=[]
  self.pins={(r['page'],r['pin_id']):r for r in table(a.native/'pins.tsv')}
  self.page_bounds={r['page']:[0,0,n(r['width_doc']),n(r['height_doc'])] for r in table(a.native/'page_grid.tsv')}
  self.netsymbols={(r['page'],r['id']):r for r in table(a.native/'net_symbols.tsv')}
  self.styles={(r['page'],r['part_id']):r for r in table(a.text_native/'part_pin_style.tsv')} if a.text_native else {}
  self.dps={(r['page'],r['dp_id']):r for r in table(a.text_native/'displayprops.tsv')} if a.text_native else {}
  frame_path=getattr(a,'part_frames',None)
  if frame_path is None and (a.native/'part_frames.tsv').exists():frame_path=a.native/'part_frames.tsv'
  self.part_frames=read_frames(frame_path)
  self.lib={val(lp,'Defn','CellName')+val(lp.find('NormalView'),'Defn','suffix'):(p,lp,lp.find('NormalView')) for p in self.root.findall('./Cache/Package') for lp in p.findall('LibPart')}
  self.lib_by_source={}
  for package in self.root.findall('./Cache/Package'):
   for part in package.findall('LibPart'):
    view=part.find('NormalView')
    if view is None:continue
    key=(val(package,'Defn','name'),val(package,'Defn','sourceLibName').replace('/','\\').casefold(),val(part,'Defn','CellName')+val(view,'Defn','suffix'))
    self.lib_by_source.setdefault(key,[]).append((package,part,view))
  self.sym={(x.tag,d(x).get('name')):x for x in self.root.find('Cache') if x.tag in ('OffPageSymbol','GlobalSymbol','PortSymbol')}
  self.sym_by_source={}
  for symbol in self.root.find('Cache'):
   if symbol.tag not in ('OffPageSymbol','GlobalSymbol','PortSymbol'):continue
   key=(symbol.tag,d(symbol).get('name',''),d(symbol).get('sourceLibName','').replace('/','\\').casefold())
   self.sym_by_source.setdefault(key,[]).append(symbol)
  self.defaultfonts={val(x,'Defn','index'):font(x,'Defn') for x in self.root.findall('./DefaultValues/DefaultFont')}
  if a.font_cache and a.font_cache.exists():
   for line in a.font_cache.read_text(encoding='utf8').splitlines():
    c=json.loads(line);self.metrics[tuple(c['key'])]=(c['metric'],from_wkb(bytes.fromhex(c['ink_wkb_hex'])))
 def part_owner(self,page,inst):
  return bind_part(d(inst),page,self.part_frames)
 def cachepart(self,inst):
  owner=d(inst)
  key=(owner.get('pkgName',''),owner.get('libName','').replace('/','\\').casefold(),val(inst,'GraphicName/Defn','name'))
  matches=self.lib_by_source.get(key,[])
  if len(matches)!=1:raise ValueError('Missing or ambiguous exact cache source identity: '+str(key))
  return matches[0]
 def cache_symbol(self,kind,inst):
  owner=d(inst)
  key=(kind,owner.get('symbolName',''),owner.get('libName','').replace('/','\\').casefold())
  matches=self.sym_by_source.get(key,[])
  if len(matches)!=1:raise ValueError('Missing or ambiguous net-symbol source identity: '+str(key))
  return matches[0]
 def metric(self,txt,ft):
  k=(txt,json.dumps(ft,sort_keys=True))
  if k not in self.metrics:
   m=measure(txt,ft);self.metrics[k]=(m,text_path(m))
   if m['font_family_substituted'] or m['missing_primary_font_glyphs']:self.fontissues.append({'text':txt,'font':ft,'resolved':m['font_resolved'],'missing':m['missing_primary_font_glyphs']})
  return self.metrics[k]
 def addtext(self,page,kind,iid,txt,ft,anchor,justify=1,rotation=0,owner='',ref='',prop='',confidence='ANCHOR_MODEL_REQUIRES_NATIVE_RENDER',extra=None,vertical='top'):
  if not txt:return
  try:m,local=self.metric(txt,ft)
  except Exception as e:self.unresolved.append({'page':page,'kind':kind,'id':iid,'text':txt,'reason':str(e)});return
  offset= -m['advance_width'] if justify==3 else -m['advance_width']/2 if justify==2 else 0
  # Official DP LEFT/TOP, Alias LEFT/BOTTOM and pin preview anchors; full native LOGFONT.
  baseline={'top':m['metrics']['tmAscent'],'bottom':-m['metrics']['tmDescent'],'middle':(m['metrics']['tmAscent']-m['metrics']['tmDescent'])/2,'baseline':0}[vertical]
  g=translate(local,xoff=offset,yoff=baseline)
  if rotation:g=rotate(g,90*rotation,origin=(0,0))
  g=translate(g,xoff=anchor[0],yoff=anchor[1])
  r={'page':page,'kind':kind,'id':str(iid),'owner_id':str(owner),'ref':ref,'property':prop,'text':txt,'font':ft,'anchor':anchor,'justification':justify,'rotation':rotation,'confidence':confidence,'vertical_anchor_model':vertical,'bbox':list(g.bounds),'ink_area':g.area,'geometry':g,'metric_key':(txt,json.dumps(ft,sort_keys=True))}
  if extra:r.update(extra)
  self.text.append(r)
 def line(self,page,kind,iid,pts,owner='',ref='',width=.35,status='XML_EXACT_MODEL_STROKE_WIDTH'):
  if len(pts)<2 or all(p==pts[0] for p in pts):return
  self.geom.append({'page':page,'kind':kind,'id':str(iid),'owner_id':str(owner),'ref':ref,'points':pts,'geometry':LineString(pts).buffer(width/2,cap_style='round',join_style='round'),'confidence':status,'width_model':width})
 def graphic(self,page,kind,iid,g,owner,ref='',ownerid=''):
  q=d(g);tag=g.tag;pts=[]
  if tag=='Line':pts=[[n(q['x1']),n(q['y1'])],[n(q['x2']),n(q['y2'])]]
  elif tag in ('Rect','Box'):
   x1,y1,x2,y2=[n(q[k]) for k in ['x1','y1','x2','y2']];pts=[[x1,y1],[x2,y1],[x2,y2],[x1,y2],[x1,y1]]
  elif tag in ('Ellipse','Arc'):
   x1,y1,x2,y2=[n(q[k]) for k in ['x1','y1','x2','y2']];cx=(x1+x2)/2;cy=(y1+y2)/2;rx=abs(x2-x1)/2;ry=abs(y2-y1)/2
   if not rx or not ry:return
   if tag=='Ellipse':start=0;sweep=2*math.pi
   else:
    start=math.atan2((n(q['startY'])-cy)/ry,(n(q['startX'])-cx)/rx);end=math.atan2((n(q['endY'])-cy)/ry,(n(q['endX'])-cx)/rx);sweep=(end-start)%(2*math.pi)
   count=max(8,math.ceil(sweep*max(rx,ry)/.3));pts=[[cx+rx*math.cos(start+sweep*k/count),cy+ry*math.sin(start+sweep*k/count)] for k in range(count+1)]
  elif tag in ('Polygon','Polyline'):
   for point in g.findall('Point'):z=d(point);pts.append([n(z.get('x')),n(z.get('y'))])
  else:return
  if not pts:self.unresolved.append({'page':page,'id':iid,'kind':kind,'reason':'unparsed '+tag});return
  pts=[transform(*p,owner) for p in pts]
  self.line(page,kind,iid,pts,ownerid,ref,status='ARC_SWEEP_MODEL_REQUIRES_NATIVE_RENDER' if tag=='Arc' else 'XML_EXACT_MODEL_STROKE_WIDTH')
 def build(self):
  for pg in self.root.findall('./Schematic/Page'):
   page=val(pg,'Defn','name')
   if self.a.page_filter and page!=self.a.page_filter:continue
   for graphic in pg.findall('GraphicPolylineInst'):
    pts=[[n(d(point).get('x')),n(d(point).get('y'))] for point in graphic.findall('PolylinePoint')]
    self.line(page,'page_graphic',d(graphic).get('dbId'),pts,status='XML_EXACT_ABSOLUTE_POLYLINE_MODEL_WIDTH')
   for net in pg.findall('NetScalar'):
    for wire in net.findall('WireScalar'):
     q=d(wire);wid=q['dbId'];points=[[n(q['startX']),n(q['startY'])],[n(q['endX']),n(q['endY'])]];self.line(page,'wire',wid,points)
     for al in wire.findall('Alias'):
      z=d(al);self.addtext(page,'alias',z['dbId'],z.get('name',''),font(al,'AliasFont/Defn'),[n(z['locX']),n(z['locY'])],1,int(z.get('rotation',0)),wid,confidence='OFFICIAL_PREVIEW_LEFT_BOTTOM_NOT_GUI_VERIFIED',vertical='bottom')
   for inst in pg:
    if inst.tag not in ('PartInst','OffPageConnector','Global','GraphicCommentTextInst'):continue
    q=d(inst);iid=q['dbId'];xy=[n(q.get('locX')),n(q.get('locY'))];ref=val(inst,'Reference/Defn','name')+q.get('deviceDesignator','');up={d(p).get('name'):d(p).get('val','') for p in inst.findall('PartInstUserProp')}
    if inst.tag=='GraphicCommentTextInst':self.addtext(page,'comment',iid,q.get('name',''),font(inst,'TextFont/Defn'),xy,int(q.get('textJustification',0)),int(q.get('rotation',0)));continue
    if inst.tag=='PartInst':
     q=self.part_owner(page,inst)
     lib=self.cachepart(inst)
     if lib:
      for j,g in enumerate(lib[2]):self.graphic(page,'body_stroke',iid+':g'+str(j),g,q,ref,iid)
      numbers={d(z).get('position'):d(z).get('number') for z in lib[1].findall('PhysicalPart/PinNumber')}
      for p in inst.findall('PortInstScalar'):
       z=d(p);pid=z['dbId'];native=self.pins.get((page,pid));ls=[n(z['startX']),n(z['startY'])];lh=[n(z['hotptX']),n(z['hotptY'])];start=transform(*ls,q);hot=transform(*lh,q)
       if native:start=[n(native['actual_start_x']),n(native['actual_start_y'])];hot=[n(native['actual_hot_x']),n(native['actual_hot_y'])]
       self.line(page,'pin_stroke',pid,[hot,start],iid,ref)
       style=self.styles.get((page,iid),{});nv=lib[2];vis=int(z.get('visible',0));namevis=int(style.get('pin_names_visible',val(nv,'IsPinNamesVisible/Defn',default='0')));numvis=int(style.get('pin_numbers_visible',val(nv,'IsPinNumbersVisible/Defn',default='0')))
       # Local official preview pin drawing algorithm; no native GUI pixel claim.
       dx=lh[0]-ls[0];dy=lh[1]-ls[1];length=math.hypot(dx,dy)
       if not length:
        self.unresolved.append({'page':page,'id':pid,'kind':'pin_text','reason':'ZERO_LENGTH_PIN_SIDE_REQUIRES_NATIVE_BOUNDARY'});continue
       # Official computePinSide plus reliable vector fallback for translated one-unit body edge discrepancies.
       side='LEFT' if dx<0 else 'RIGHT' if dx>0 else 'TOP' if dy<0 else 'BOTTOM'
       namedelta,numdelta={'LEFT':((5,0),(20,0)),'RIGHT':((-5,0),(-20,0)),'TOP':((2,10),(0,20)),'BOTTOM':((2,-10),(0,-20))}[side]
       localrot=3 if side in ('TOP','BOTTOM') else 0
       nametypejust=3 if side in ('RIGHT','TOP') else 1;numtypejust=1 if side in ('RIGHT','TOP') else 3
       for typ,txt,show in [('pin_name',native['pin_name'] if native else z.get('name',''),vis and namevis),('pin_number',native['pin_number'] if native else numbers.get(z.get('position'),''),vis and numvis)]:
        if not show:continue
        pref='name' if typ=='pin_name' else 'number';ft={k:style.get(pref+'_font_'+k) for k in ['name','height','width','escapement','orientation','weight','italic']} if style else dict(self.defaultfonts.get('3' if typ=='pin_name' else '4',{}))
        if any(v is not None and str(v).startswith('UNPROBED') for v in ft.values()):ft=dict(self.defaultfonts.get('3' if typ=='pin_name' else '4',{}))
        ft.pop('index',None);ft={k:(v if k=='name' else int(v)) for k,v in ft.items() if v is not None}
        delta=namedelta if typ=='pin_name' else numdelta;origin=ls if typ=='pin_name' else lh;anchor=[origin[0]+delta[0],origin[1]+delta[1]];just=nametypejust if typ=='pin_name' else numtypejust
        before=len(self.text)
        self.addtext(page,typ,pid+':'+typ,txt,ft,anchor,just,localrot,iid,ref,confidence='OFFICIAL_PREVIEW_PIN_LAYOUT_PLUS_XML_FONT_NOT_GUI_VERIFIED',vertical='middle' if typ=='pin_name' else 'bottom',extra={'preview_pin_side':side,'preview_local_anchor':anchor,'preview_local_rotation':localrot,'preview_source':'orPrmDboStreamer::computePinTextDeltas/streamPartPin'})
        if len(self.text)>before:
         t=self.text[-1];o=transform(0,0,q);ex=transform(1,0,q);ey=transform(0,1,q);matrix=[ex[0]-o[0],ey[0]-o[0],ex[1]-o[1],ey[1]-o[1],o[0],o[1]]
         t['geometry']=affine_transform(t['geometry'],matrix);t['anchor']=transform(*anchor,q);t['rotation']=(localrot+int(q.get('rotation',0)))%4;t['bbox']=list(t['geometry'].bounds);t['preview_owner_mirror']=int(q.get('mirror',0))
    else:
     st='OffPageSymbol' if inst.tag=='OffPageConnector' else 'GlobalSymbol';sym=self.cache_symbol(st,inst)
     if sym is not None:
      glyphowner=dict(q);nativehot=self.netsymbols.get((page,iid));sp=sym.find('SymbolPinScalar')
      if nativehot and sp is not None:
       pd=d(sp);predicted=transform(n(pd['hotptX']),n(pd['hotptY']),q)
       glyphowner['locX']=str(int(n(q['locX'])+n(nativehot['actual_hot_x'])-predicted[0]));glyphowner['locY']=str(int(n(q['locY'])+n(nativehot['actual_hot_y'])-predicted[1]))
      for j,g in enumerate(sym):self.graphic(page,'port_glyph' if inst.tag=='OffPageConnector' else 'power_glyph',iid+':g'+str(j),g,glyphowner,'',iid)
    for dp in inst:
     if not dp.tag.endswith('DisplayProp'):continue
     z=d(dp);did=z['dbId'];dt=int(val(dp,'PropDispType/Defn',default='0'))
     if dt==0:continue
     name=z.get('name','');actual=self.dps.get((page,did));txt=''
     if actual:txt=actual['value_string']
     elif name=='Name':txt=q.get('name','')
     elif name=='Part Reference':txt=ref
     elif name=='Value':txt=val(inst,'PartValue/Defn','name')
     else:txt=up.get(name,'')
     anchor=[xy[0]+n(z.get('locX')),xy[1]+n(z.get('locY'))]
     # Native probe's raw SDK anchor is exported as evidence, not silently assumed absolute.
     if actual:anchor=[n(actual['absolute_add_candidate_x']),n(actual['absolute_add_candidate_y'])]
     kind={'PartInst':'part_display','OffPageConnector':'port_name','Global':'power_name'}[inst.tag]
     ft=font(dp,'PropFont/Defn')
     if actual:
      for fk in ['name','height','width','escapement','orientation','weight','italic','underline','strikeout','charset','outprecision','clipprecision','quality','pitchandfamily']:
       source=actual.get('font_'+fk)
       target={'outprecision':'out_precision','clipprecision':'clip_precision','pitchandfamily':'pitch_and_family'}.get(fk,fk)
       if source is not None:ft[target]=source if target=='name' else int(source)
     self.addtext(page,kind,did,txt,ft,anchor,int(z.get('textJustification',0)),int(z.get('rotation',0)),iid,ref,name,extra={'owner_location':xy,'original_offset':[n(z.get('locX')),n(z.get('locY'))],'sdk_anchor_raw':[actual.get('sdk_anchor_raw_x'),actual.get('sdk_anchor_raw_y')] if actual else None})
  return self

def collisions(texts,geom,gap=0):
 allobj=texts+geom;by=collections.defaultdict(list);out=[]
 for o in allobj:by[o['page']].append(o)
 for page,objs in by.items():
  gs=[o['geometry'] for o in objs];tree=STRtree(gs)
  for i,o in enumerate(objs):
   if i>=len([x for x in objs if 'text' in x]):break
   query=o['geometry'].buffer(gap) if gap else o['geometry']
   for j in tree.query(query):
    j=int(j)
    if j==i or (j<i and 'text' in objs[j]):continue
    other=objs[j];inter=o['geometry'].intersection(other['geometry']);area=inter.area
    if area<.02:continue
    out.append({'page':page,'a_kind':o['kind'],'a_id':o['id'],'a_owner':o['owner_id'],'a_ref':o.get('ref',''),'a_text':o['text'],'b_kind':other['kind'],'b_id':other['id'],'b_owner':other['owner_id'],'b_ref':other.get('ref',''),'b_text':other.get('text',''),'ink_intersection_area':area,'a_confidence':o['confidence'],'b_confidence':other['confidence'],'status':'MODEL_CANDIDATE_REQUIRES_CAPTURE_CALIBRATION'})
 return out

def svg(scene,path,page,bounds=None,extra_text=None):
 ts=[o for o in scene.text if o['page']==page];gs=[o for o in scene.geom if o['page']==page]
 if extra_text is not None:ts=extra_text
 if not bounds:
  shapes=[o['geometry'] for o in ts+gs];bb=unary_union(shapes).bounds;bounds=[bb[0]-10,bb[1]-10,bb[2]+10,bb[3]+10]
 x1,y1,x2,y2=bounds;crop=box(*bounds);style={'wire':'#b62929','pin_stroke':'#b62929','body_stroke':'#1261b5','port_glyph':'#218132','power_glyph':'#218132','port_name':'#b00000','alias':'#a32525','power_name':'#b00000','part_display':'#222222','comment':'#777777','pin_name':'#005aa5','pin_number':'#222222'}
 lines=[f'<svg xmlns="http://www.w3.org/2000/svg" width="{(x2-x1)*4:g}" height="{(y2-y1)*4:g}" viewBox="{x1:g} {y1:g} {x2-x1:g} {y2-y1:g}">',f'<rect x="{x1}" y="{y1}" width="{x2-x1}" height="{y2-y1}" fill="white"/>']
 for o in gs+ts:
  g=o['geometry']
  if not g.intersects(crop):continue
  lines.append('<g fill="'+style.get(o['kind'],'#444')+'" stroke="none"><title>'+html.escape(o['kind']+' '+o['id']+' '+o.get('text',''))+'</title>'+g.svg(fill_color=style.get(o['kind'],'#444'),scale_factor=0)+'</g>')
 lines.append('</svg>');path.write_text('\n'.join(lines),encoding='utf-8')
 if not getattr(scene.a,'render_png',False):return
 try:
  import pymupdf as fitz
  doc=fitz.open(path);pdf=fitz.open('pdf',doc.convert_to_pdf());factor=min(1.4,3000/max(pdf[0].rect.width,pdf[0].rect.height));pix=pdf[0].get_pixmap(matrix=fitz.Matrix(factor,factor),alpha=False);pix.save(path.with_suffix('.png'))
 except Exception as e:path.with_suffix('.png_error.txt').write_text(str(e),encoding='utf8')

def validate_bindings(scene):
 """Refuse stale or partial native tables before trusting an offline scene."""
 pages=[pg for pg in scene.root.findall('./Schematic/Page') if not scene.a.page_filter or val(pg,'Defn','name')==scene.a.page_filter]
 names={val(pg,'Defn','name') for pg in pages}
 expected_dp={(val(pg,'Defn','name'),d(dp)['dbId']):dp for pg in pages for owner in pg for dp in owner if dp.tag.endswith('DisplayProp')}
 native_dp={key:row for key,row in scene.dps.items() if key[0] in names}
 if set(expected_dp)!=set(native_dp):raise ValueError('XML and native DisplayProp IDs differ: stale or partial audit')
 for key,dp in expected_dp.items():
  q=d(dp);r=native_dp[key]
  for x,y in [('locX','dp_local_x'),('locY','dp_local_y'),('rotation','rotation'),('textJustification','justification')]:
   if n(q.get(x,0))!=n(r[y]):raise ValueError('XML/native DisplayProp coordinates differ: '+str(key))
 expected_alias={}
 expected_pin={}
 for pg in pages:
  page=val(pg,'Defn','name')
  for part in pg.findall('PartInst'):
   for pin in part.findall('PortInstScalar'):
    q=d(pin);key=(page,q['dbId']);expected_pin[key]=pin;native=scene.pins.get(key)
    if native is None:raise ValueError('XML pin missing from native audit: '+str(key))
    for local_x,local_y,native_x,native_y in [('startX','startY','actual_start_x','actual_start_y'),('hotptX','hotptY','actual_hot_x','actual_hot_y')]:
     candidate=transform(n(q[local_x]),n(q[local_y]),scene.part_owner(page,part))
     if candidate!=[n(native[native_x]),n(native[native_y])]:raise ValueError('XML/native absolute pin coordinates differ: '+str(key))
  for wire in pg.findall('NetScalar/WireScalar'):
   for alias in wire.findall('Alias'):expected_alias[(page,d(alias)['dbId'])]=(alias,d(wire)['dbId'])
 native_alias={(r['page'],r['id']):r for r in table(scene.a.native/'aliases.tsv') if r['page'] in names}
 if set(expected_alias)!=set(native_alias):raise ValueError('XML and native Alias IDs differ: stale or partial audit')
 if set(expected_pin)!={key for key in scene.pins if key[0] in names}:raise ValueError('XML/native placed-pin IDs differ')
 for key,(alias,owner) in expected_alias.items():
  q=d(alias);r=native_alias[key]
  if owner!=r['owner_wire_id'] or q['name']!=r['name'] or [n(q['locX']),n(q['locY'])]!=[n(r['loc_x']),n(r['loc_y'])]:raise ValueError('XML/native Alias attachment differs: '+str(key))
 return {'displayprops':len(expected_dp),'aliases':len(expected_alias),'pins':len(expected_pin),'exact_ID_coordinate_attachment_binding':True}

def main():
 from _dependencies import add_options
 ap=argparse.ArgumentParser(description=__doc__)
 for key in ['xml','native','text-native','output']:
  ap.add_argument('--'+key,required=True,type=pathlib.Path)
 ap.add_argument('--part-frames',type=pathlib.Path,help='Same-save native affine TSV; mandatory for any nonzero PartInst rotation/mirror')
 ap.add_argument('--grid',required=True,type=int,help='Frozen native document-unit grid; this audit never snaps coordinates')
 ap.add_argument('--font-cache',type=pathlib.Path,help='Optional regenerable GDI cache outside the learning library')
 ap.add_argument('--write-font-cache',action='store_true')
 ap.add_argument('--page-filter')
 ap.add_argument('--render-all',action='store_true')
 ap.add_argument('--render-png',action='store_true',help='Also render PNG using optional PyMuPDF')
 ap.add_argument('--skip-collisions',action='store_true')
 add_options(ap);a=ap.parse_args()
 if a.grid<=0:ap.error('--grid must be positive')
 if a.write_font_cache and not a.font_cache:ap.error('--write-font-cache needs --font-cache')
 a.output.mkdir(parents=True,exist_ok=True)
 before=hashlib.sha256(a.xml.read_bytes()).hexdigest();scene=Scene(a).build();binding=validate_bindings(scene)
 if a.write_font_cache:
  save_lines(a.font_cache,[{'key':list(k),'metric':{mk:mv for mk,mv in m.items() if mk not in ('contours','path_commands')},'ink_wkb_hex':g.wkb_hex} for k,(m,g) in scene.metrics.items()])
 rows=[] if a.skip_collisions else collisions(scene.text,scene.geom)
 core={'alias','port_name','power_name','part_display'}
 core_rows=[r for r in rows if r['a_kind'] in core or r['b_kind'] in core]
 save_lines(a.output/'ink_collision_candidates.jsonl',rows)
 save_lines(a.output/'core_collision_candidates.jsonl',core_rows)
 save_lines(a.output/'scene_texts.jsonl',[{k:v for k,v in t.items() if k not in ('geometry','metric_key')} for t in scene.text])
 save_lines(a.output/'scene_geometry.jsonl',[{k:v for k,v in g.items() if k!='geometry'} for g in scene.geom])
 save_json(a.output/'unresolved.json',scene.unresolved);save_json(a.output/'font_issues.json',scene.fontissues)
 pages=[val(pg,'Defn','name') for pg in scene.root.findall('./Schematic/Page') if not a.page_filter or val(pg,'Defn','name')==a.page_filter]
 if a.render_all:
  links=['<!doctype html><meta charset="utf-8"><title>Schematic layout model</title><p>Official preview algorithms and native fonts; native GUI pixels are not verified.</p><ol>']
  for i,page in enumerate(pages):
   prefix='page_'+str(i+1).zfill(2);svg(scene,a.output/(prefix+'.svg'),page)
   links.append('<li>'+html.escape(page)+' <a href="'+prefix+'.svg">SVG</a></li>')
  (a.output/'index.html').write_text('\n'.join(links+['</ol>']),encoding='utf8')
 summary={'input_xml':str(a.xml),'input_sha256':before,'input_unchanged':before==hashlib.sha256(a.xml.read_bytes()).hexdigest(),'grid_document_units':a.grid,'native_binding':binding,'native_part_affine_frames':len(scene.part_frames),'pages':len(pages),'scene_texts':len(scene.text),'scene_geometry':len(scene.geom),'font_issues':len(scene.fontissues),'unresolved':len(scene.unresolved),'collision_scan_performed':not a.skip_collisions,'all_collision_candidates':len(rows),'network_and_property_candidates':len(core_rows),'pin_text_model':'local official preview algorithm plus native/XML fonts; not native GUI pixels','whole_project_GUI_pass':False,'CAD_started':False,'design_written':False}
 save_json(a.output/'summary.json',summary);print(json.dumps(summary,ensure_ascii=True))

if __name__=='__main__':main()

