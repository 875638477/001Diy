"""Offline two-terminal visual template replacement. Never runs CAD or writes DSN/OLB.
Input/output paths, material classification, native frames, calibration and exceptions are data parameters.
"""
import argparse,copy,csv,collections,hashlib,json,pathlib,re,sys,xml.etree.ElementTree as E
sys.path.insert(0,str(pathlib.Path(__file__).resolve().parent))
from template_xml_common import D,C,H,FS,dump,defaults,props,active,applies,VIEWS,J,word
from native_effective_evidence import read_binding,resolve

def mm(A,p):return [A[0][0]*p[0]+A[0][1]*p[1],A[1][0]*p[0]+A[1][1]*p[1]]
def add(a,b):return [a[0]+b[0],a[1]+b[1]]
def sub(a,b):return [a[0]-b[0],a[1]-b[1]]
def pt(d,stem):return [int(d[stem+'X']),int(d[stem+'Y'])]
def findactive(pkg,inst):
 ci,vt=active(pkg,inst);lp=pkg.findall('LibPart')[ci];return lp,lp.find(vt)
def bynumber(pkg,inst):
 lp,v=findactive(pkg,inst);numbers={D(x)['position']:D(x)['number'] for x in lp.findall('PhysicalPart/PinNumber')};return {numbers[D(x)['position']]:x for x in v.findall('SymbolPinScalar')},numbers

def frameoffset(cal,r,m,bbox):
 row=next(x for x in cal['frames'] if x['rotation']==r and x['mirror']==m);base=cal['bbox'];W=int(bbox['x2'])-int(bbox['x1']);HH=int(bbox['y2'])-int(bbox['y1']);assert int(bbox['x1'])==int(bbox['y1'])==0,'Uncalibrated nonzero bbox origin'
 def dim(v):
  opts=[z for z,n in [('ZERO',0),('W',base[2]-base[0]),('H',base[3]-base[1])] if n==v];assert len(opts)==1;return {'ZERO':0,'W':W,'H':HH}[opts[0]]
 sample=row.get('sample_bbox_offset')
 if sample is None:
  keys=[k for k in row if k.startswith('offset_for_bbox_')];assert len(keys)==1;sample=row[keys[0]]
 return row['matrix'],[dim(v) for v in sample]

def append_prop(inst,name,value):
 assert name not in props(inst,'PartInstUserProp');node=E.Element('PartInstUserProp');E.SubElement(node,'Defn',{'name':name,'val':value});children=list(inst);pos=max([i for i,x in enumerate(children) if x.tag=='PartInstUserProp'],default=0)+1;inst.insert(pos,node)

def diffattrs(before,after,path=''):
 assert before.tag==after.tag and len(before)==len(after),'Unexpected instance child structure'
 out=[]
 if before.attrib!=after.attrib:out.append({'path':path,'before':dict(before.attrib),'after':dict(after.attrib)})
 assert (before.text or '').strip()==(after.text or '').strip() and (before.tail or '').strip()==(after.tail or '').strip()
 for i,(x,y) in enumerate(zip(before,after)):out+=diffattrs(x,y,path+'/'+str(i))
 return out

def main():
 ap=argparse.ArgumentParser();
 for name in ['input','reference-xml','reference-frames','native-calibration','effective-binding','material-plan','config','output']:ap.add_argument('--'+name,required=True,type=pathlib.Path)
 a=ap.parse_args();assert not a.output.exists(),'Fresh output directory required';a.output.mkdir(parents=True)
 cfg=json.loads(a.config.read_text(encoding='utf8'));material=json.loads(a.material_plan.read_text(encoding='utf8'));cal=json.loads(a.native_calibration.read_text(encoding='utf-8-sig'));assert cal['status']=='PASS_NATIVE_ALL8_GRAPHIC_POINT_AFFINE_CALIBRATION' and cal['sample_count']==40
 effective_rows,undefined_approval=read_binding(a.effective_binding,FS(a.reference_xml));undefined_preserved=[]
 B=E.parse(a.input).getroot();R=E.parse(a.reference_xml).getroot();F=copy.deepcopy(B);bp={D(x)['name']:x for x in B.findall('Cache/Package')};rp={D(x)['name']:x for x in R.findall('Cache/Package')};bi={D(x)['dbId']:x for x in B.findall('Schematic/Page/PartInst')};ri={D(x)['dbId']:x for x in R.findall('Schematic/Page/PartInst')};fi={D(x)['dbId']:x for x in F.findall('Schematic/Page/PartInst')};assert set(bi)==set(ri)==set(fi)
 frames={r['id']:r for r in csv.DictReader(a.reference_frames.open(encoding='utf-8-sig'),delimiter='\t')};assert set(frames)==set(bi)
 for ident,i in ri.items():
  f=frames[ident];d=D(i);assert all(int(d.get(k,0))==int(f[v]) for k,v in [('locX','ox'),('locY','oy'),('rotation','rotation'),('mirror','mirror')])
 def reference_world(ident,local):
  f=frames[ident];A=[[int(f['a_xx']),int(f['a_xy'])],[int(f['a_yx']),int(f['a_yy'])]];return add([int(f['frame_origin_x']),int(f['frame_origin_y'])],mm(A,local))
 members=collections.defaultdict(list);excluded=[]
 for r in material:
  ident=r['instance_id'];override=cfg.get('explicit_instance_family_overrides',{}).get(ident);family=override['family'] if override else cfg['material_families'].get(r['material'])
  if not family or (cfg.get('enabled_families') and family not in cfg['enabled_families']):continue
  if override:
   assert override.get('basis') and override.get('authorization'), 'Classification override requires recorded evidence and authorization'
   reference=ri[ident];referenceprops=props(reference,'PartInstUserProp')
   assert D(reference.find('PartValue')).get('name','')==override['expected_reference_part_value']
   for key,value in override.get('required_reference_props',{}).items():assert len(referenceprops.get(key,[]))==1 and D(referenceprops[key][0]).get('val','')==value,('Classification override source mismatch',ident,key)
  if ident in cfg.get('hold_instance_ids',[]):excluded.append({'id':ident,'ref':r['ref'],'reason':'Explicit hold in reviewed configuration'});continue
  members[family].append(r)
 additions=[];package_proofs=[];changed=[];newpkgs={};retarget=[];query={};oldnew={};defaults_removed=[]
 for family,rows in members.items():
  spec=cfg['templates'][family];oldnames=sorted({D(bi[r['instance_id']])['pkgName'] for r in rows});canonical=max(oldnames,key=lambda n:sum(D(bi[r['instance_id']])['pkgName']==n for r in rows));old=bp[canonical];library=E.parse(pathlib.Path(spec['library_xml'])).getroot();user=next(x for x in library.findall('Package') if D(x)['name']==spec['package']);ulps=user.findall('LibPart');assert len(ulps)==1 and len(ulps[0].findall('NormalView'))==1 and not ulps[0].findall('ConvertView');uv=ulps[0].find('NormalView')
  oldnormals=old.findall('LibPart/NormalView');assert len(oldnormals)==1 and len(old.findall('LibPart'))==1 and not old.findall('LibPart/ConvertView')
  new=copy.deepcopy(old);nd=new.find('Defn');nd.set('name',family);nd.set('refdesPrefix',spec['refdes_prefix']);nd.set('pcbFootprint','');nd.set('pcbLib','');lp=new.find('LibPart');lp.find('Defn').set('CellName',family);v=lp.find('NormalView');v.find('Defn').set('suffix','.Normal')
  maps={n:defaults(bp[n]) for n in oldnames};keys=set().union(*(set(x) for x in maps.values()));different={k for k in keys if len({J([C(x) for x in maps[n][k]]) if k in maps[n] else '@ABSENT@' for n in oldnames})>1};parents={ch:p for p in new.iter() for ch in p};dn=defaults(new)
  for k in different:
   if '/SymbolDisplayProp/' in k:continue
   for node in dn.get(k,[]):defaults_removed.append({'family':family,'scope':k,'xml':E.tostring(node,encoding='unicode')});parents[node].remove(node)
  # Only the user's drawing primitives and bounding frame are adopted. No user
  # Package/Symbol property, simulation model, pin defaults or function is imported.
  graphic_tags={'Line','Rect','Ellipse','Arc','Polygon','Polyline','CommentText','Text','Bezier','Box'}
  oldbb=v.find('SymbolBBox');bbindex=list(v).index(oldbb);v.remove(oldbb);v.insert(bbindex,copy.deepcopy(uv.find('SymbolBBox')))
  for ch in list(v):
   if ch.tag in graphic_tags:v.remove(ch)
  insert=next((i for i,x in enumerate(v) if x.tag.startswith('SymbolPin')),len(v))
  omitted_comments=[ch for ch in uv if ch.tag=='CommentText' and D(ch).get('name','').strip() in {'1','2'} and spec.get('omit_numeric_comment_labels',False)]
  adopted=[copy.deepcopy(ch) for ch in uv if ch.tag in graphic_tags and ch not in omitted_comments]
  for ch in adopted:v.insert(insert,ch);insert+=1
  upins={D(p)['position']:p for p in uv.findall('SymbolPinScalar')};unum={D(p)['position']:D(p)['number'] for p in ulps[0].findall('PhysicalPart/PinNumber')};upbynum={unum[pos]:p for pos,p in upins.items()};assert set(upbynum)=={'1','2'}
  # Electrical/visibility/shared/NC/PinUserProp payload comes from this design,
  # not the user's library. Canonical positions follow the selected library map.
  olnum={D(x)['position']:D(x)['number'] for x in lp.findall('PhysicalPart/PinNumber')};oldpins={olnum[D(x)['position']]:x for x in v.findall('SymbolPinScalar')};assert set(oldpins)=={'1','2'}
  for num,pin in oldpins.items():
   d=pin.find('Defn');u=D(upbynum[num]);d.set('position',u['position'])
   for k in ['startX','startY','hotptX','hotptY']:d.set(k,u[k])
   for k,val in spec.get('pin_coordinate_overrides',{}).get(num,{}).items():assert k in {'startX','startY','hotptX','hotptY'};d.set(k,str(val))
  for pin in lp.findall('PhysicalPart/PinNumber'):pin.find('Defn').set('position',D(upbynum[D(pin)['number']])['position'])
  # Keep baseline-hidden labels hidden; no larger user-library pin font is imported.
  for tag,value in spec.get('display_flags',{}).items():
   target=v.find(tag)
   if target is None:target=E.SubElement(v,tag);E.SubElement(target,'Defn',{'val':str(value)})
   else:target.find('Defn').set('val',str(value))
  newmap,_=bynumber(new, E.fromstring('<PartInst><Defn/><GraphicName><Defn name="'+family+'.Normal"/></GraphicName></PartInst>'))
  bbox=D(v.find('SymbolBBox'));assert int(bbox['x1'])==int(bbox['y1'])==0
  # Compare complete non-coordinate electrical pin payload by actual physical number.
  def electrical(pin):
   q=copy.deepcopy(pin);d=q.find('Defn')
   for k in ['position','startX','startY','hotptX','hotptY']:d.attrib.pop(k,None)
   return H(q)
  for r in rows:
   ident=r['instance_id'];oldinst=bi[ident];refinst=ri[ident];target=fi[ident];oldpkg=bp[D(oldinst)['pkgName']];refpkg=rp[D(refinst)['pkgName']];oldpins,oldnum=bynumber(oldpkg,oldinst);refpins,refnum=bynumber(refpkg,refinst);assert set(oldpins)==set(newmap)==set(refpins)=={'1','2'}
   for num in oldpins:assert electrical(oldpins[num])==electrical(newmap[num]),('Electrical pin payload differs',r['ref'],num)
   placed={refnum[D(p)['position']]:p for p in refinst.findall('PortInstScalar')};assert set(placed)=={'1','2'};world={num:reference_world(ident,pt(D(pin),'hotpt')) for num,pin in placed.items()};oldworld=copy.deepcopy(world)
   for num,point in cfg.get('pin_hotspot_exceptions',{}).get(ident,{}).items():world[num]=point
   poses=[]
   for rr in range(4):
    for mirror in (0,1):
     A,offset=frameoffset(cal,rr,mirror,bbox);origin=sub(sub(world['1'],mm(A,pt(D(newmap['1']),'hotpt'))),offset)
     if add(add(origin,offset),mm(A,pt(D(newmap['2']),'hotpt')))==world['2']:poses.append((mirror,rr,origin,A,offset))
   assert poses,('No exact library pose for physical pin pair',r['ref'],world,{n:D(p) for n,p in newmap.items()});mirror,rotation,origin,A,offset=min(poses,key=lambda x:(x[0],x[1]));beforeorigin=[int(D(oldinst)['locX']),int(D(oldinst)['locY'])];td=target.find('Defn');td.set('pkgName',family);td.set('locX',str(origin[0]));td.set('locY',str(origin[1]));td.set('rotation',str(rotation));td.set('mirror',str(mirror));target.find('GraphicName/Defn').set('name',family+'.Normal')
   instpins={oldnum[D(p)['position']]:p for p in target.findall('PortInstScalar')};assert set(instpins)=={'1','2'}
   for num,pin in instpins.items():
    d=pin.find('Defn');newd=D(newmap[num]);d.set('position',newd['position'])
    for k in ['startX','startY','hotptX','hotptY']:d.set(k,newd[k])
    assert add(add(origin,offset),mm(A,pt(d.attrib,'hotpt')))==world[num]
   for dp in target.findall('PartInstDisplayProp'):
    d=dp.find('Defn');d.set('locX',str(int(d.get('locX','0'))+beforeorigin[0]-origin[0]));d.set('locY',str(int(d.get('locY','0'))+beforeorigin[1]-origin[1]))
   av=active(oldpkg,oldinst);od=defaults(oldpkg);op=props(oldinst,'PartInstUserProp');ads=[];names={k.split('/')[-1] for k in keys if k.split('/')[1 if k.startswith('Package/') else 2] in {'PackageUserProp','SymbolUserProp'}};query[ident]=sorted(names|set(op)|{'PCB Footprint','PCB Library','User_Value','Part Reference','Value'})
   for name in sorted(names):
    activeold=[node for k,nodes in od.items() if applies(k,av) and k.endswith('/'+name) and ('/PackageUserProp/' in k or '/SymbolUserProp/' in k) for node in nodes]
    changedkeys=[k for k in different if applies(k,av) and k.endswith('/'+name) and ('/PackageUserProp/' in k or '/SymbolUserProp/' in k)]
    if not changedkeys or name in op or not activeold:continue
    observed=resolve(effective_rows,undefined_approval,ident,name)
    if not observed['defined']:
     undefined_preserved.append({'instance_id':ident,'ref':r['ref'],'name':name,**observed});continue
    value=observed['value'];append_prop(target,name,value);ad={'instance_id':ident,'ref':r['ref'],'name':name,'value':value,'source_scope_keys':[k for k in changedkeys if k in od]};ads.append(ad);additions.append(ad)
   # After removing exactly documented materializations, the remaining instance
   # may change only identity/pose, canonical local pin coordinates/position, and DP offsets.
   bare=copy.deepcopy(target)
   for ad in ads:
    p=next(p for p in bare.findall('PartInstUserProp') if D(p)=={'name':ad['name'],'val':ad['value']});bare.remove(p)
   attrs=diffattrs(oldinst,bare)
   oldpaths={};newpaths={}
   def paths(e,path='',res=None):
    if res is None:res={}
    res[path]=e
    for index,ch in enumerate(e):paths(ch,path+'/'+str(index),res)
    return res
   oldpaths=paths(oldinst)
   for change in attrs:
    node=oldpaths[change['path']];parentpath=change['path'].rsplit('/',1)[0];parent=oldpaths.get(parentpath);allowed={'pkgName','locX','locY','rotation','mirror'} if change['path']=='/0' else {'name'} if parent is not None and parent.tag=='GraphicName' else {'position','startX','startY','hotptX','hotptY'} if parent is not None and parent.tag=='PortInstScalar' else {'locX','locY'} if parent is not None and parent.tag=='PartInstDisplayProp' else set();assert {k for k in set(change['before'])|set(change['after']) if change['before'].get(k)!=change['after'].get(k)}<=allowed,(r['ref'],change['path'],allowed)
   changed.append({'instance_id':ident,'ref':r['ref'],'family':family,'old_package':D(oldinst)['pkgName'],'attributes':attrs,'materializations':ads,'old_pin_world':oldworld,'new_pin_world':world,'new_pose':{'rotation':rotation,'mirror':mirror,'origin':origin,'A':A,'offset':offset},'all_DP_absolute_anchors_fonts_rotation_visibility_unchanged':True});retarget.append(ident)
  newpkgs[family]=new;package_proofs.append({'family':family,'source_library_xml':spec['library_xml'],'source_library_sha256':FS(pathlib.Path(spec['library_xml'])),'source_library_package':spec['package'],'instances':len(rows),'body_primitives_adopted':len(adopted),'static_numeric_comment_labels_omitted':len(omitted_comments),'all_original_ordered_electrical_pin_flags_preserved_by_physical_number':True,'library_userprops_models_and_default_fonts_imported':False,'scope_defaults_removed':len([x for x in defaults_removed if x['family']==family]),'pin_coordinate_overrides':spec.get('pin_coordinate_overrides',{}),'display_flags':spec.get('display_flags',{})})
 # Prune only now-unused packages and add exactly one new package per material family.
 used={D(i)['pkgName'] for i in fi.values()};cache=F.find('Cache');removed=[]
 for pkg in list(cache):
  if pkg.tag=='Package' and (D(pkg)['name'] not in used or D(pkg)['name'] in newpkgs):removed.append(D(pkg)['name']);cache.remove(pkg)
 for name,pkg in newpkgs.items():assert name not in {D(p)['name'] for p in cache.findall('Package')};cache.append(pkg)
 wirechanges=[];allw={D(w)['dbId']:w for w in F.findall('Schematic/Page/NetScalar/WireScalar')}
 for spec in cfg.get('wire_endpoint_changes',[]):
  w=allw[spec['id']];d=w.find('Defn');assert all(d.get(k)==str(v) for k,v in spec['before'].items());before=copy.deepcopy(w)
  for k,vv in spec['after'].items():d.set(k,str(vv))
  bb=w.find('WireBBox/Defn');assert bb is not None
  for k,vv in {'x1':min(int(d.get('startX')),int(d.get('endX'))),'y1':min(int(d.get('startY')),int(d.get('endY'))),'x2':max(int(d.get('startX')),int(d.get('endX'))),'y2':max(int(d.get('startY')),int(d.get('endY')))}.items():bb.set(k,str(vv))
  assert not w.findall('Alias') and not w.findall('Junction'),'Wire exception has attached alias/junction';wirechanges.append({'id':spec['id'],'before_xml':E.tostring(before,encoding='unicode'),'after_xml':E.tostring(w,encoding='unicode'),'reason':spec['reason']})
 # Whole-tree inverse plus independent instance attribute whitelist protect all other domains.
 inverse=copy.deepcopy(F);ic=inverse.find('Cache');inverse.remove(ic);inverse.insert(list(B).index(B.find('Cache')),copy.deepcopy(B.find('Cache')));ii={D(x)['dbId']:x for x in inverse.findall('Schematic/Page/PartInst')}
 for row in changed:
  inst=ii[row['instance_id']]
  for ad in row['materializations']:
   p=next(x for x in inst.findall('PartInstUserProp') if D(x)=={'name':ad['name'],'val':ad['value']});inst.remove(p)
  for change in row['attributes']:
   node=inst
   for index in change['path'].split('/')[1:]:node=list(node)[int(index)]
   assert node.attrib==change['after'];node.attrib.clear();node.attrib.update(change['before'])
  assert H(inst)==H(bi[row['instance_id']])
 for row in wirechanges:
  for net in inverse.findall('Schematic/Page/NetScalar'):
   for idx,w in enumerate(list(net)):
    if w.tag=='WireScalar' and D(w)['dbId']==row['id']:net.remove(w);net.insert(idx,E.fromstring(row['before_xml']))
 assert H(inverse)==H(B),'Whole-template inverse differs';assert H(B.find('Occurrences'))==H(F.find('Occurrences'))
 candidate=a.output/'candidate.xml';E.ElementTree(F).write(candidate,encoding='utf-8',xml_declaration=True);assert H(E.parse(candidate).getroot())==H(F)
 dump(a.output/'instance_template_and_inverse_ledger.json',changed);dump(a.output/'template_package_provenance_and_pin_proofs.json',package_proofs);dump(a.output/'scoped_default_materializations.json',additions);dump(a.output/'differing_scoped_defaults_removed.json',defaults_removed);dump(a.output/'wire_endpoint_exception_ledger.json',wirechanges);dump(a.output/'held_instances.json',excluded);dump(a.output/'reviewed_undefined_defaults_not_materialized.json',undefined_preserved);dump(a.output/'pruned_unused_packages.json',removed)
 with (a.output/'effective_query_data.tcldict').open('w',encoding='utf8') as f:
  for ident,names in query.items():f.write(word(ident)+' {'+' '.join(word(n) for n in names)+'}\n')
 summary={'status':'PASS_OFFLINE_SHARED_USER_VISUAL_TEMPLATE_CANDIDATE_NATIVE_GATES_REQUIRED','input_xml_sha256':FS(a.input),'reference_xml_sha256':FS(a.reference_xml),'reference_frame_table_sha256':FS(a.reference_frames),'candidate_xml_sha256':FS(candidate),'packages_before':len(bp),'packages_after':len(F.findall('Cache/Package')),'families':{k:len(v) for k,v in members.items()},'changed_instances':len(changed),'explicit_classification_overrides':cfg.get('explicit_instance_family_overrides',{}),'materializations':len(additions),'materialized_names':dict(collections.Counter(x['name'] for x in additions)),'original_world_pin_hotspots_preserved_except_explicit_exception':True,'explicit_pin_hotspot_exceptions':cfg.get('pin_hotspot_exceptions',{}),'wire_endpoint_changes':len(wirechanges),'all_existing_Instance_reference_value_footprint_MPN_and_other_props_preserved':True,'all_DP_absolute_anchors_fonts_rotation_visibility_unchanged':True,'all_instance_mutations_exact_allowlist':True,'whole_inverse_exact_equal':True,'unknown_changes':0,'source_files_unchanged':True,'native_effective_binding_sha256':FS(a.effective_binding),'reviewed_undefined_defaults_not_materialized':len(undefined_preserved),'future_native_electrical_effective_properties_frames_pin_maps_and_layout_gates':'REQUIRED_NOT_RUN','CAD_started':False};dump(a.output/'summary.json',summary);print(json.dumps(summary,ensure_ascii=True))
if __name__=='__main__':main()
