"""Offline Capture XML grid candidate. Never starts/loads Capture or writes a DSN.
Checks native attachment geometry before producing a candidate; native PST remains mandatory.
"""
from pathlib import Path
import argparse,csv,collections,hashlib,json,itertools,math,xml.etree.ElementTree as E,sys

def d(e):return e.find('Defn').attrib

def unescape_tsv(value):
 out=[];i=0;esc={'\\':'\\','t':'\t','r':'\r','n':'\n'}
 while i<len(value):
  if value[i]!='\\':out.append(value[i]);i+=1;continue
  if i+1>=len(value) or value[i+1] not in esc:raise ValueError('Native TSV is not in the documented backslash-escaped row format')
  out.append(esc[value[i+1]]);i+=2
 return ''.join(out)

def rows(p):
 return [{k:unescape_tsv(v) for k,v in r.items()} for r in csv.DictReader(p.open(encoding='utf-8-sig',newline=''),delimiter='\t')]


def transform(x,y,a):
 # Each source pin transform is checked against its supplied native actual hotspot.
 if int(a.get('mirror','0')):x=-x
 r=int(a.get('rotation','0'))%4
 if r==1:x,y=y,-x
 elif r==2:x,y=-x,-y
 elif r==3:x,y=-y,x
 return x+int(a.get('locX',0)),y+int(a.get('locY',0))

def on(p,s):
 a,b=s
 return (p[0]-a[0])*(b[1]-a[1])==(p[1]-a[1])*(b[0]-a[0]) and min(a[0],b[0])<=p[0]<=max(a[0],b[0]) and min(a[1],b[1])<=p[1]<=max(a[1],b[1])

def intersect(s,t):
 a,b=s;c,e=t
 if a==b or c==e:raise ValueError('zero segment')
 h=a[1]==b[1];j=c[1]==e[1]
 if h and j:
  if a[1]!=c[1]:return None
  lo=max(min(a[0],b[0]),min(c[0],e[0]));hi=min(max(a[0],b[0]),max(c[0],e[0]))
  return None if lo>hi else ('POINT',(lo,a[1])) if lo==hi else ('OVERLAP',(lo,hi,a[1]))
 if not h and not j:
  if a[0]!=c[0]:return None
  lo=max(min(a[1],b[1]),min(c[1],e[1]));hi=min(max(a[1],b[1]),max(c[1],e[1]))
  return None if lo>hi else ('POINT',(a[0],lo)) if lo==hi else ('OVERLAP',(lo,hi,a[0]))
 p=(c[0],a[1]) if h else (a[0],c[1])
 return ('POINT',p) if on(p,s) and on(p,t) else None

def cells(s,sz=50):
 a,b=s
 for x in range(min(a[0],b[0])//sz,max(a[0],b[0])//sz+1):
  for y in range(min(a[1],b[1])//sz,max(a[1],b[1])//sz+1):yield x,y

def buckets(wires):
 b=collections.defaultdict(set)
 for wid,s in wires.items():
  for c in cells(s):b[c].add(wid)
 return b

def touching(wires,p,b):return {wid for wid in b.get((p[0]//50,p[1]//50),()) if on(p,wires[wid])}

def relation(wires,junctions,terminals):
 b=buckets(wires);pairs=set()
 for v in b.values():pairs.update(itertools.combinations(sorted(v),2))
 j=set(junctions);tp=set(terminals.values());out={}
 for a,z in pairs:
  hit=intersect(wires[a],wires[z])
  if not hit:continue
  if hit[0]=='OVERLAP':kind='OVERLAP'
  else:
   p=hit[1];kind='CONTACT' if p in wires[a] or p in wires[z] or p in j or p in tp else 'CROSS_NO_JUNCTION'
  out[(a,z)]=kind
 attach={(t,w) for t,p in terminals.items() for w in touching(wires,p,b)}
 groups=collections.defaultdict(list)
 for t,p in terminals.items():groups[p].append(t)
 coincidence={tuple(sorted(v)) for g in groups.values() for v in itertools.combinations(g,2)}
 return out,attach,coincidence,b

def diffmap(a,b):
 return [{'pair':list(k),'before':a.get(k),'after':b.get(k)} for k in sorted(a.keys()|b.keys()) if a.get(k)!=b.get(k)]

def line_box(s,box):
 x1,y1,x2,y2=box;a,b=s
 if a[1]==b[1]:return y1<=a[1]<=y2 and max(min(a[0],b[0]),x1)<=min(max(a[0],b[0]),x2)
 return x1<=a[0]<=x2 and max(min(a[1],b[1]),y1)<=min(max(a[1],b[1]),y2)


def reject_unknown_objects(pg):
 # Supported electrical scope is deliberately narrow. Preserve known metadata and
 # documented text/page graphics untouched; they are not claimed grid-corrected.
 allowed={'Defn','TitleblockDisplayed','BorderDisplayed','GridRefDisplayed','PageSizeInfo','PageSize','OuterBorderMagin','OuterLineStyle','OuterLineWidth','OuterBorderIsVisible','InnerBorderMargin','InnerLineStyle','InnerLineWidth','InnerLineVisible','Color','Font','LabelColor','HorizontalCount','HorizontalWidth','HorizontalChar','HorizontalVisible','HorizontalAscending','HorizontalStyle','HorizontalSeparatorWidth','VerticalCount','VerticalWidth','VerticalChar','VerticalVisible','VerticalAscending','VerticalStyle','VerticalSeparatorWidth','PageDateTime','PartInst','NetScalar','OffPageConnector','Global','Port','GraphicCommentTextInst','GraphicPolylineInst'}
 unknown=sorted({e.tag for e in pg if e.tag not in allowed})
 unsupported=sorted({e.tag for e in pg.iter() if e.tag in {'WireBus','NetBus','BusEntry','PortInstBus','DrawnInst','HierarchicalBlock','NetGroup','BundleEntry'}})
 if unknown or unsupported:raise RuntimeError('Unsupported page/electrical object types: '+str({'unknown':unknown,'unsupported':unsupported}))

def self_test():
 tests=[]
 def check(name,ok):
  tests.append({'name':name,'pass':bool(ok)})
  if not ok:raise AssertionError(name)
 w={'1':((0,0),(10,0)),'2':((0,5),(10,5))};old,_,_,_=relation(w,[],{});w['2']=((10,0),(10,5));new,_,_,_=relation(w,[],{});z=diffmap(old,new);check('NEW_ENDPOINT_ON_FOREIGN_WIRE_REJECTED',len(z)==1 and z[0]['after']=='CONTACT')
 w={'1':((0,5),(10,5)),'2':((5,0),(5,10))};old,_,_,_=relation(w,[],{});new,_,_,_=relation(w,[(5,5)],{});z=diffmap(old,new);check('CROSS_WITHOUT_JUNCTION_MUST_NOT_BECOME_CONTACT',len(z)==1 and z[0]['before']=='CROSS_NO_JUNCTION' and z[0]['after']=='CONTACT')
 w={'1':((0,0),(10,0))};_,old,_,_=relation(w,[],{'PIN:1':(0,0)});_,new,_,_=relation(w,[],{'PIN:1':(0,5)});check('DISCONNECTED_PIN_ATTACHMENT_REJECTED',old-new=={('PIN:1','1')})
 w={'1':((0,0),(10,0))};_,_,old,_=relation(w,[],{'PIN:1':(0,0),'PIN:2':(0,5)});_,_,new,_=relation(w,[],{'PIN:1':(0,0),'PIN:2':(0,0)});check('NEW_PIN_PIN_COINCIDENCE_REJECTED',len(new-old)==1)
 print(json.dumps({'status':'ALL_FOUR_NEGATIVE_CONTROLS_DETECTED','tests':tests},indent=2))

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--input-xml',type=Path);ap.add_argument('--native-audit',type=Path);ap.add_argument('--output-dir',type=Path);ap.add_argument('--grid',type=int);ap.add_argument('--pin-spacing-raw',type=int,help='Optional expected native/XML PinToPin value, assertion only; never changes page scale');ap.add_argument('--allow-learning-exercise-output',action='store_true');ap.add_argument('--self-test',action='store_true');a=ap.parse_args()
 if a.self_test:self_test();return
 if not all((a.input_xml,a.native_audit,a.output_dir,a.grid)):ap.error('--input-xml --native-audit --output-dir --grid are required unless --self-test')
 if a.grid<=0:ap.error('--grid must be a positive integer in document units')
 here=Path(__file__).resolve();learning=here.parent.parent
 if learning.name.lower()=='learning' and a.output_dir.resolve().is_relative_to(learning) and not a.allow_learning_exercise_output:ap.error('Real-project outputs must be outside the learning library; course exercises require the explicit exception flag')
 if a.output_dir.exists():raise RuntimeError('fresh output required')
 G=a.grid;Q=lambda v:((v+G//2)//G)*G
 source_bytes=a.input_xml.read_bytes();source_sha=hashlib.sha256(source_bytes).hexdigest().upper();root=E.fromstring(source_bytes);native=a.native_audit
 P={(r['page'],r['id']):r for r in rows(native/'parts.tsv')}
 PIN={(r['page'],r['part_id'],r['pin_position']):r for r in rows(native/'pins.tsv')}
 W={(r['page'],r['id']):r for r in rows(native/'wires.tsv')}
 N={(r['page'],r['kind'],r['id']):r for r in rows(native/'net_symbols.tsv')}
 lib={}
 for pkg in root.findall('./Cache/Package'):
  for lp in pkg.findall('LibPart'):
   nv=lp.find('NormalView')
   if nv is not None:lib[d(lp)['CellName']+d(nv).get('suffix','')]=nv
 pages=[];actions=[];freeends=[];exceptions=[];coverage=collections.Counter();allgates=[];origin_offgrid=[]
 for pg in root.findall('./Schematic/Page'):
  reject_unknown_objects(pg)
  if a.pin_spacing_raw is not None and int(d(pg.find('PageSizeInfo'))['PinToPin'])!=a.pin_spacing_raw:raise RuntimeError('Page PinToPin does not match explicit --pin-spacing-raw assertion')
  pn=d(pg)['name'];partdelta={};term_old={};term_new={};old={};new={};jold=[];jnew=[];bodyboxes=[];wireelements={};specials={};part_ids=[];pin_start_offgrid=[]
  for part in pg.findall('PartInst'):
   pd=d(part);pid=pd['dbId'];pr=P[(pn,pid)];part_ids.append(pid)
   if (int(pd['locX']),int(pd['locY']))!=(int(pr['loc_x']),int(pr['loc_y'])):raise RuntimeError('Part native/XML location mismatch '+pn+'/'+pid)
   pins=part.findall('PortInstScalar');deltas=set()
   for pin in pins:
    q=d(pin);pos=q['position'];nr=PIN[(pn,pid,pos)]
    local=(int(q['hotptX']),int(q['hotptY']));hot=transform(*local,pd)
    if hot!=(int(nr['actual_hot_x']),int(nr['actual_hot_y'])):raise RuntimeError('Native pin/XML transform mismatch '+pn+'/'+pid+'/'+pos)
    deltas.add((Q(hot[0])-hot[0],Q(hot[1])-hot[1]))
    key='PIN:'+pid+':'+pos+':'+nr['pin_number'];term_old[key]=hot;term_new[key]=(Q(hot[0]),Q(hot[1]));coverage['pins']+=1
    start=transform(int(q['startX']),int(q['startY']),pd)
    if start!=(int(nr['actual_start_x']),int(nr['actual_start_y'])):raise RuntimeError('Native pin/XML start mismatch '+pn+'/'+pid+'/'+pos)
    target_start=(start[0]+Q(hot[0])-hot[0],start[1]+Q(hot[1])-hot[1])
    if target_start[0]%G or target_start[1]%G:pin_start_offgrid.append({'pin':key,'new_start':target_start,'reason':'Rigid pin length/start cannot align to requested grid without changing symbol geometry'})
   if len(deltas)!=1:raise RuntimeError('Rigid part pin residues incompatible '+pn+'/'+pid)
   dx,dy=deltas.pop();partdelta[pid]=(dx,dy)
   oldloc=(int(pd['locX']),int(pd['locY']));pd['locX']=str(oldloc[0]+dx);pd['locY']=str(oldloc[1]+dy)
   if int(pd['locX'])%G or int(pd['locY'])%G:origin_offgrid.append({'page':pn,'part_id':pid,'ref':pr['full_ref'],'new_origin':[int(pd['locX']),int(pd['locY'])],'reason':'Pin-local common residue nonzero; rigid body pin geometry preserved, part-origin is not an electrical hotspot.'})
   actions.append({'page':pn,'kind':'PART_TRANSLATE','id':pid,'ref':pr['full_ref'],'delta':[dx,dy],'old_location':oldloc,'new_location':[int(pd['locX']),int(pd['locY'])]})
   nv=lib.get(part.find('GraphicName/Defn').get('name'));pts=[];unknown=[]
   if nv is None:raise RuntimeError('Cache graphic missing '+pid)
   for v in nv:
    if v.tag in ('Defn','SymbolPinScalar','SymbolPinBus','LibPartUserProp','LibPartDisplayProp'):continue
    z=v.find('Defn');q=z.attrib if z is not None else {}
    if v.tag in ('Line','Rect','Box','Ellipse','Arc') and all(k in q for k in ('x1','x2','y1','y2')):
     for x in (float(q['x1']),float(q['x2'])):
      for y in (float(q['y1']),float(q['y2'])):pts.append(transform(x,y,pd))
    elif v.tag in ('Polygon','Polyline'):
     polypts=v.findall('Point')
     if not polypts:unknown.append(v.tag+':UNPARSED_POINTS')
     for point in polypts:q=d(point);pts.append(transform(float(q['x']),float(q['y']),pd))
    elif v.tag not in ('CommentText','Text','PartValue','Reference','IsPinNamesVisible','IsPinNumbersVisible','IsPinNamesRotated','PowerPinsAreVisible','ContentsLibName','ContentsViewName','ContentsViewType','SymbolBBox','SymbolColor','SymbolDisplayProp','SymbolUserProp'):unknown.append(v.tag)
   if pts:bodyboxes.append((pid,(min(p[0] for p in pts),min(p[1] for p in pts),max(p[0] for p in pts),max(p[1] for p in pts))))
   if unknown:exceptions.append({'page':pn,'kind':'BODY_GRAPHIC_TYPE_REVIEW','part_id':pid,'types':sorted(set(unknown))})
   coverage['parts']+=1
  for tag,kind in [('OffPageConnector','offpage'),('Global','global'),('Port','port')]:
   for obj in pg.findall(tag):
    q=d(obj);oid=q['dbId'];nr=N[(pn,kind,oid)]
    loc=(int(q['locX']),int(q['locY']))
    if loc!=(int(nr['loc_x']),int(nr['loc_y'])):raise RuntimeError('Net symbol native/XML location mismatch')
    hot=(int(nr['actual_hot_x']),int(nr['actual_hot_y']));dx=Q(hot[0])-hot[0];dy=Q(hot[1])-hot[1]
    q['locX']=str(loc[0]+dx);q['locY']=str(loc[1]+dy)
    key=kind.upper()+':'+oid;term_old[key]=hot;term_new[key]=(hot[0]+dx,hot[1]+dy)
    actions.append({'page':pn,'kind':kind.upper()+'_TRANSLATE','id':oid,'name':nr['name'],'delta':[dx,dy],'old_hotspot':hot,'new_hotspot':term_new[key]});coverage[kind]+=1
  for net in pg.findall('NetScalar'):
   for wire in net.findall('WireScalar'):
    q=d(wire);wid=q['dbId'];nativepoints=[tuple(map(int,v.split(','))) for v in W[(pn,wid)]['points'].split(';')]
    s=((int(q['startX']),int(q['startY'])),(int(q['endX']),int(q['endY'])))
    if list(s)!=nativepoints:raise RuntimeError('Wire native/XML mismatch '+pn+'/'+wid)
    if s[0][0]!=s[1][0] and s[0][1]!=s[1][1]:raise RuntimeError('Non-Manhattan source wire '+pn+'/'+wid)
    old[wid]=s;new[wid]=tuple((Q(x),Q(y)) for x,y in s);wireelements[wid]=wire
    for j in wire.findall('Junction'):
     z=d(j);p=(int(z['locX']),int(z['locY']));jold.append(p);jnew.append((Q(p[0]),Q(p[1])));z['locX']=str(Q(p[0]));z['locY']=str(Q(p[1]));coverage['junctions']+=1
  oldrel,oldattach,oldcoinc,oldb=relation(old,jold,term_old)
  # A collapsed dangling stub is expanded to one full grid while retaining its direction.
  for wid,s in old.items():
   if new[wid][0]!=new[wid][1]:continue
   candidates=[];wire=wireelements[wid]
   for k,p in enumerate(s):
    if p in set(term_old.values()) or p in set(jold):continue
    if touching(old,p,oldb)!={wid}:continue
    if any((int(d(t)['locX']),int(d(t)['locY']))==p for t in wire.findall('Alias')):continue
    candidates.append(k)
   if not candidates:raise RuntimeError('Collapsed wire has no truly free endpoint '+pn+'/'+wid)
   k=candidates[-1];anchor=new[wid][1-k];v=(s[k][0]-s[1-k][0],s[k][1]-s[1-k][1]);direction=((1 if v[0]>0 else -1) if v[0] else 0,(1 if v[1]>0 else -1) if v[1] else 0)
   fixed=list(new[wid]);fixed[k]=(anchor[0]+G*direction[0],anchor[1]+G*direction[1]);new[wid]=tuple(fixed)
   freeends.append({'page':pn,'wire_id':wid,'net':W[(pn,wid)]['net_name'],'free_endpoint_index':k,'old_segment':s,'new_segment':new[wid],'reason':'Original endpoint has no pin/net-symbol/junction/alias/other-wire attachment. Keep original direction and expand dangling stub to one requested grid; do not delete wire.'})
  newrel,newattach,newcoinc,newb=relation(new,jnew,term_new)
  changes=diffmap(oldrel,newrel);lost=sorted(oldattach-newattach);added=sorted(newattach-oldattach);co_lost=sorted(oldcoinc-newcoinc);co_add=sorted(newcoinc-oldcoinc)
  for f in freeends:
   if f['page']!=pn:continue
   wid=f['wire_id'];s=new[wid];f['foreign_wire_intersections']=[{'wire_id':z,'type':intersect(s,t)[0]} for z,t in new.items() if z!=wid and intersect(s,t)]
   f['foreign_terminal_points']=[t for t,p in term_new.items() if on(p,s) and (t,wid) not in oldattach]
   f['body_bbox_intersections']=[{'part_id':pid,'bbox':b} for pid,b in bodyboxes if line_box(s,b)]
  junction_bad=[list(p) for p in jnew if not any(on(p,t) for t in new.values())]
  offgrid=[t for t,p in term_new.items() if p[0]%G or p[1]%G]
  residue=collections.Counter((x%G,y%G) for p in term_old.values() for x,y in [p]);wr=collections.Counter((x%G,y%G) for s in old.values() for x,y in s)
  pagegates={'wire_pair_relation_changes':changes,'terminal_wire_attachment_lost':lost,'terminal_wire_attachment_added':added,'terminal_coincidence_lost':co_lost,'terminal_coincidence_added':co_add,'junction_not_on_any_wire':junction_bad,'offgrid_electrical_hotspots':offgrid,'pin_starts_offgrid':pin_start_offgrid,'zero_new_wire_count':sum(s[0]==s[1] for s in new.values())}
  passed=not any(pagegates.values());allgates.append(passed)
  pages.append({'page':pn,'strategy':'UNIFORM_PAGE_ELECTRICAL_TRANSLATION' if len(residue)==len(wr)==1 and set(residue)==set(wr) else 'LOCAL_QUANTIZATION_WITH_RIGID_PART_PIN_ALIGNMENT','terminal_residue_counts':{str(k):v for k,v in residue.items()},'wire_endpoint_residue_counts':{str(k):v for k,v in wr.items()},'parts':len(part_ids),'terminals':len(term_old),'wires':len(old),'comparison_domain':{'wire_pair_relations':len(oldrel),'terminal_wire_incidences':len(oldattach),'terminal_coincidence_pairs':len(oldcoinc),'explicit_junction_points':len(jold)},'gates_pass':passed,'gates':pagegates})
  for wid,wire in wireelements.items():
   q=d(wire);s=new[wid]
   q.update(startX=str(s[0][0]),startY=str(s[0][1]),endX=str(s[1][0]),endY=str(s[1][1]))
   box=wire.find('WireBBox/Defn')
   if box is not None:box.attrib.update(x1=str(min(p[0] for p in s)),x2=str(max(p[0] for p in s)),y1=str(min(p[1] for p in s)),y2=str(max(p[1] for p in s)))
   for al in wire.findall('Alias'):
    z=d(al);oldpos=(int(z['locX']),int(z['locY']));z['locX']=str(Q(oldpos[0]));z['locY']=str(Q(oldpos[1]));coverage['aliases']+=1
   actions.append({'page':pn,'kind':'WIRE_POINTS','id':wid,'net':W[(pn,wid)]['net_name'],'old_points':old[wid],'new_points':s})
  coverage['wires']+=len(old)
  # Cached instance bounds are not geometry; omit these optional values for native recomputation.
  for obj in list(pg):
   if obj.tag in ('PartInst','OffPageConnector','Port','Global'):
    for ch in list(obj):
     if 'BBox' in ch.tag:obj.remove(ch)
  # Decorative text/graphics and display-property placement are handled by the independent layout plan.
 badfree=[f for f in freeends if f['foreign_wire_intersections'] or f['foreign_terminal_points'] or f['body_bbox_intersections']]
 summary={'status':'OFFLINE_GEOMETRY_GATE_PASS_NATIVE_PST_REQUIRED' if all(allgates) and not badfree and not exceptions else 'OFFLINE_GEOMETRY_GATE_FAIL_REVIEW_REQUIRED','source_xml':str(a.input_xml.resolve()),'source_xml_sha256':source_sha,'source_sha_after':hashlib.sha256(a.input_xml.read_bytes()).hexdigest().upper(),'native_audit':str(native.resolve()),'grid_doc':G,'origin':[0,0],'pages':len(pages),'uniform_pages':sum(p['strategy'].startswith('UNIFORM') for p in pages),'coverage':dict(coverage),'free_stub_extensions':len(freeends),'free_stub_obstacle_failures':len(badfree),'unparsed_visible_body_types_count':len(exceptions),'part_origin_offgrid_after_pin_alignment':len(origin_offgrid),'all_electrical_attachment_and_crossing_gates_pass':all(allgates),'limitations':['This is an owned offline XML candidate, not an applied CAD result or GUI proof. Native import/reopen and exact PST pin-net partition validation remain mandatory.','Part bodies remain rigid and every effective electrical pin hotspot is on-grid. Some origins may remain off-grid because their local pins share a nonzero residue; no cache pin geometry has been silently altered.','Text/display-property anchors and decorative page graphics are not yet snapped by this electrical geometry stage; independent font/visual layout planning remains required.','Foreign body checks use conservative actual cache graphic bounding envelopes; unsupported graphics are listed for review.','No wire is removed. Collapsed dangling stubs may be extended to one requested grid only after obstacle/attachment checks.']}
 assert summary['source_xml_sha256']==summary['source_sha_after'], 'Input XML changed during offline planning'
 a.output_dir.mkdir(parents=True)
 (a.output_dir/'grid_plan.json').write_text(json.dumps({'summary':summary,'pages':pages,'actions':actions,'free_stub_extensions':freeends,'origin_exceptions':origin_offgrid,'body_graphic_review':exceptions},separators=(',',':')),encoding='utf-8')
 (a.output_dir/'grid_plan_summary.json').write_text(json.dumps(summary,indent=2),encoding='utf-8')
 (a.output_dir/'free_stub_extensions.json').write_text(json.dumps(freeends,indent=2),encoding='utf-8')
 if all(allgates) and not badfree and not exceptions:
  E.indent(root,space='  ');E.ElementTree(root).write(a.output_dir/'grid_candidate.xml',encoding='utf-8',xml_declaration=True)
 print(json.dumps(summary,indent=2))
 if not all(allgates) or badfree or exceptions:sys.exit(2)
if __name__=='__main__':main()
