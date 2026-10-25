"""Borrow a user crystal drawing motif while preserving each source pin schema.
No native/CAD execution. Only current source 2/4/5-pin schemas selected in data change.
"""
import argparse,copy,csv,json,pathlib,sys,xml.etree.ElementTree as E
sys.path.insert(0,str(pathlib.Path(__file__).resolve().parent))
from template_xml_common import D,H,FS,dump
from build_shared_visual_templates import mm,add,sub,findactive
GFX={'Line','Rect','Ellipse','Arc','Polygon','Polyline','CommentText','Box'}

def main():
 ap=argparse.ArgumentParser()
 for key in ['input','template-library-xml','config','native-pins','output']:ap.add_argument('--'+key,required=True,type=pathlib.Path)
 a=ap.parse_args();assert not a.output.exists();a.output.mkdir(parents=True);cfg=json.loads(a.config.read_text(encoding='utf-8'));B=E.parse(a.input).getroot();F=copy.deepcopy(B);pk={D(x)['name']:x for x in B.findall('Cache/Package')};bi={D(x)['dbId']:x for x in B.findall('Schematic/Page/PartInst')};fi={D(x)['dbId']:x for x in F.findall('Schematic/Page/PartInst')};library=E.parse(a.template_library_xml).getroot();mother=next(p for p in library.findall('Package') if D(p)['name']==cfg['mother_package']);mv=mother.find('LibPart/NormalView');mb=D(mv.find('SymbolBBox'));assert all(int(mb[k])==0 for k in ['x1','y1']);MW=int(mb['x2']);MH=int(mb['y2']);assert MW>0 and MH>0
 native=list(csv.DictReader(a.native_pins.open(encoding='utf-8-sig'),delimiter='\t'));changed=[];proofs=[];newpkgs={}
 for spec in cfg['schemas']:
  ident=str(spec['instance_id']);oldi=bi[ident];ni=fi[ident];oldpkg=pk[D(oldi)['pkgName']];lp,ov=findactive(oldpkg,oldi);assert len(oldpkg.findall('LibPart'))==1 and not oldpkg.findall('LibPart/ConvertView');oldpins=ov.findall('SymbolPinScalar');numbers={D(p)['position']:D(p)['number'] for p in lp.findall('PhysicalPart/PinNumber')};by_number={numbers[D(p)['position']]:p for p in oldpins};assert len(oldpins)==spec['pin_count'] and sorted(by_number)==sorted(spec['physical_numbers'])
  assert all(D(pin)['type']=='4' and D(pin.find('IsGlobal')).get('val')=='0' for pin in oldpins),'Never inherit user oscillator implicit global or power type'
  currentnative=[p for p in native if p['part_id']==ident];assert len(currentnative)==spec['pin_count'];netbynum={p['pin_number']:p['net_name'] for p in currentnative};assert all(netbynum[n]=='GND' for n in spec['case_pin_numbers']) and all(netbynum[n]!='GND' for n in spec['signal_pin_numbers'])
  new=copy.deepcopy(oldpkg);name=spec['name'];new.find('Defn').set('name',name);new.find('Defn').set('refdesPrefix','Y');nlp,nv=findactive(new,oldi);nlp.find('Defn').set('CellName',name);nv.find('Defn').set('suffix','.Normal')
  if nv.find('Reference/Defn') is not None:nv.find('Reference/Defn').set('name','Y')
  # Keep the source bbox and all source pin coordinates. Fit the shared mother
  # body within that existing canvas; this is a controlled visual change only.
  bb=D(ov.find('SymbolBBox'));x1,y1,x2,y2=[int(bb[k]) for k in ['x1','y1','x2','y2']];TW=x2-x1;TH=y2-y1;assert TW>0 and TH>0
  A=spec['body_axis_matrix'];corners=[mm(A,[x,y]) for x,y in [(0,0),(MW,0),(MW,MH),(0,MH)]];lo=[min(p[k] for p in corners) for k in (0,1)];hi=[max(p[k] for p in corners) for k in (0,1)];sp=[hi[0]-lo[0],hi[1]-lo[1]]
  def point(x,y):
   q=sub(mm(A,[x,y]),lo);return [x1+round(q[0]*TW/sp[0]),y1+round(q[1]*TH/sp[1])]
  def drawing(ch):
   result=copy.deepcopy(ch);d=result.find('Defn');assert d is not None
   for xx,yy in [('x1','y1'),('x2','y2'),('startX','startY'),('endX','endY'),('locX','locY')]:
    if xx in d.attrib or yy in d.attrib:
     assert xx in d.attrib and yy in d.attrib;q=point(int(d.get(xx)),int(d.get(yy)));d.set(xx,str(q[0]));d.set(yy,str(q[1]))
   if ch.tag in {'Rect','Ellipse','Arc','Box'}:
    for low,high in [('x1','x2'),('y1','y2')]:
     aa,bb=int(d.get(low)),int(d.get(high));d.set(low,str(min(aa,bb)));d.set(high,str(max(aa,bb)))
   return result
  adopted=[drawing(ch) for ch in mv if ch.tag in GFX and not (ch.tag=='CommentText' and D(ch).get('name','').strip().isdigit())]
  for ch in list(nv):
   if ch.tag in GFX:nv.remove(ch)
  insert=next(i for i,ch in enumerate(nv) if ch.tag.startswith('SymbolPin'))
  for ch in adopted:nv.insert(insert,ch);insert+=1
  # Source full electrical pin subtrees, physical number order, and view flags
  # are byte-semantic unchanged. No template PinDisplayProp/default/font copied.
  assert [H(p) for p in oldpins]==[H(p) for p in nv.findall('SymbolPinScalar')]
  assert H(lp.find('PhysicalPart'))==H(nlp.find('PhysicalPart'))
  assert [H(p) for p in ov if p.tag.startswith('IsPin')]==[H(p) for p in nv if p.tag.startswith('IsPin')]
  oldgraphic=D(oldi.find('GraphicName'))['name'];ni.find('Defn').set('pkgName',name);ni.find('GraphicName/Defn').set('name',name+'.Normal')
  expected=copy.deepcopy(oldi);expected.find('Defn').set('pkgName',name);expected.find('GraphicName/Defn').set('name',name+'.Normal');assert H(expected)==H(ni)
  newpkgs[name]=new;changed.append({'instance_id':ident,'ref':spec['ref'],'old_package':D(oldi)['pkgName'],'new_package':name,'old_graphic':oldgraphic,'new_graphic':name+'.Normal'})
  proofs.append({'ref':spec['ref'],'name':name,'source_pin_count':len(oldpins),'signal_pin_numbers':spec['signal_pin_numbers'],'case_pin_numbers':spec['case_pin_numbers'],'native_source_net_by_physical_number':netbynum,'source_complete_ordered_pin_subtrees_unchanged':True,'source_PhysicalPart_mapping_exact':True,'all_source_pin_type4_global0_preserved':True,'all_part_instance_nonidentity_subtree_exact':True,'source_canvas_bbox':bb,'mother_package':cfg['mother_package'],'body_axis_matrix':A,'body_primitives':len(adopted),'all_existing_pin_start_hot_DP_fonts_visibility_and_world_locations_exact':True,'template_electrical_and_global_properties_not_copied':True,'source_frequency_value_and_MPN_not_changed':True})
 used={D(i)['pkgName'] for i in fi.values()};cache=F.find('Cache')
 for p in list(cache):
  if p.tag=='Package' and D(p)['name'] not in used:cache.remove(p)
 for name,pkg in newpkgs.items():assert name not in {D(p)['name'] for p in cache.findall('Package')};cache.append(pkg)
 inverse=copy.deepcopy(F);ic=inverse.find('Cache');inverse.remove(ic);inverse.insert(list(B).index(B.find('Cache')),copy.deepcopy(B.find('Cache')));ii={D(x)['dbId']:x for x in inverse.findall('Schematic/Page/PartInst')}
 for row in changed:ii[row['instance_id']].find('Defn').set('pkgName',row['old_package']);ii[row['instance_id']].find('GraphicName/Defn').set('name',row['old_graphic'])
 assert H(inverse)==H(B),'Crystal inverse differs';candidate=a.output/'candidate.xml';E.ElementTree(F).write(candidate,encoding='utf-8',xml_declaration=True);assert H(E.parse(candidate).getroot())==H(F)
 dump(a.output/'crystal_identity_inverse_ledger.json',changed);dump(a.output/'crystal_physical_schema_and_visual_proofs.json',proofs);summary={'status':'PASS_OFFLINE_CRYSTAL_COMMON_MOTIF_SOURCE_PIN_SCHEMAS_NATIVE_REQUIRED','input_xml_sha256':FS(a.input),'candidate_xml_sha256':FS(candidate),'user_template_library_xml_sha256':FS(a.template_library_xml),'source_native_pin_table_sha256':FS(a.native_pins),'package_count_before':len(pk),'package_count_after':len(F.findall('Cache/Package')),'source_crystals':len(changed),'distinct_visual_family':1,'physical_pin_schema_variants':[2,4,5],'all_current_part_instances_only3identity_pairs_changed':True,'all_world_pin_start_hot_and_DP_positions_unchanged':True,'all_full_source_ordered_electrical_pin_schema_and_PhysicalPart_payload_equal':True,'source_pin_schema_including_any_zero_length_pin_preserved':True,'all_noncached_nonpart_objects_exact_by_whole_inverse':True,'whole_inverse_exact_equal':True,'unknown_changes':0,'native_run':False,'GUI_verified':False};dump(a.output/'summary.json',summary);print(json.dumps(summary,ensure_ascii=True))
if __name__=='__main__':main()
