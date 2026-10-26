"""Freeze all81 source packages once: only concrete same-case families, preserved functional schemas explicit."""
from pathlib import Path
from collections import defaultdict,Counter
from decimal import Decimal,ROUND_HALF_UP
import copy,csv,json,hashlib,importlib.util,xml.etree.ElementTree as ET
M=Path(__file__).resolve().parent;R=Path(r'D:\001DIY\004computer\lga1700\13shared_libraries_pc_20261025');O=M/'project81_final_canonical_plan13';O.mkdir(exist_ok=True)
S=importlib.util.spec_from_file_location('native',M/'review_global_suffix_native_chunks.py');N=importlib.util.module_from_spec(S);S.loader.exec_module(N)
jr=N.jread;sha=N.sha;dump=N.dump
idx={}
for folder in ['global_suffix_native_review_v3','global_nonpassive_native_review13','global_nonpassive_increment_review13','global_canonical_targets_review13','project81_current_targets_review13']:
 for f in (M/folder).glob('e*_SCHEMA_GEOMETRY.json'):
  for e in jr(f):
   for n in [e['stem']]+[Path(x).stem for x in e.get('byte_identical_members',[])]:idx[n.lower()]=e
allpublic=jr(M/'global_nonpassive_inventory_v1/ALL_PUBLIC_PSM_INVENTORY.json')['files'];files={r['stem'].lower():r for r in allpublic}
# Existing same-case generic choices. Angles are NEW-component minus OLD-component on nonmirrored placements.
rules={
 'sot23_123':('sot23-3',0,'Same3-pin SOT23 topology; target is existing generic. Record rowpitch/land change.'),
 'ot-23-3_l2_9-w1_3-p1_90-ls2_1':('sot23-3',90,'Same3-pin SOT23 topology. Existing generic is90deg rotated with different land pattern.'),
 'so8_50_150gv':('sop-8-e-150mil',90,'Both are9pad exposed-pad SO8 150mil, withEP numbered9. Existing generic preserves all9numbers; pad spacing/size differs.'),
 'so8_50_150gv_2':('sop-8-e-150mil',90,'Same9pad SO8EP9 family. Do not use ordinary8pad SOP.'),
 'sot23-6p-20051228_1_1':('sot23-6p-20051228',0,'Same6numbered-terminal SOT23 package, orientations/padstack forms recorded.'),
 'sm_sot23_5pin_1':('sm_sot23_5pin',0,'Same5numbered-terminal SOT23 case.'),
 'sm_sot23_5pin_1_1':('sm_sot23_5pin',0,'Same5numbered-terminal SOT23 case.'),
 'dfn3x3-10-0-5_1':('dfn3x3-10-0-5',0,'SameDFN3x3,10signal pads plusEP11,0.5mm pitch.'),
 'dfn3x3-10-0-5_2':('dfn3x3-10-0-5',0,'SameDFN3x3,10signal pads plusEP11,0.5mm pitch.'),
 'dfn2510p10e_1_1':('dfn2510p10e',0,'Same10terminal DFN2510 topology; no extra thermal terminal introduced.'),
 'dfn2510p10e_2':('dfn2510p10e',0,'Same10terminal DFN2510 topology.'),
 'dfn8_3x3mm-gnd_2':('dfn8_3x3mm-gnd',0,'SameDFN3x3,8signal pads plusEP9.'),
 'prpak5x6_2_1':('prpak5x6',0,'Same5numbered physical land groups ofPowerPAK5x6.'),
 'prpak5x6_3_1':('prpak5x6',0,'Same5numbered physical land groups ofPowerPAK5x6.'),
 'prpak5x6_4_1':('prpak5x6',0,'Same5numbered physical land groups ofPowerPAK5x6.'),
 'prpak5x6_5':('prpak5x6',0,'Same5numbered physical land groups ofPowerPAK5x6.'),
 'isen_shortni_2_1':('isen_shortni',0,'Same3pad sense-short structure. Never replace with ordinary2pad resistor.'),
 'pin2x5_2d54_nc10_1':('pin2x5_2d54_nc10',0,'Same9actual pads withposition10absent; original missing USB pin remains absent.'),
 'hdr-th_10p-p2_54_210-82-05gb04_1':('hdr-th_10p-p2_54_210-82-05gb04',0,'Same9actual pads withoriginal absent position preserved.'),
 'mth_156a_1':('mth_156a',0,'Same4physical pads numbered1..4; originalSCH16vsPCB4difference is preserved.'),
 'mth_156a_2':('mth_156a',0,'Same4physical pads numbered1..4; originalSCH16vsPCB4difference is preserved.'),
 'mth_156a_1_1':('mount_156a_p4567_pc',0,'Distinct4pad numbering4/5/6/7 is preserved as its own semantic generic; cloneexactsource.'),
 'smd_bd5_6-d3_6_1':('smd_bd5_6-d3_6',0,'Same4split-number pads1/1_1/1_2/1_3. One0.01mil source coordinate delta is explicitly recorded.'),
 'smd_bd5_6-d3_6_2':('smd_bd5_6-d3_6',0,'Same4split-number pads1/1_1/1_2/1_3.'),
 '1n4148ws-7-sod323':('sod323',0,'Same2terminal SOD323 body; existing generic haspin1onright, preserving numbered topology. Land pitch changes0.147828mm.'),
 '1n4148ws-7-sod323_1_1':('sod323',0,'SameSOD323 model family; existing right-pin1generic standard.'),
 'lqfp48':('lqfp-48',-90,'Same48pin0.5mm pitch LQFP topology; existing generic land rows differ, with-90deg pose correction.'),
 'smd3225':('smd_3225',0,'Same4pin3.2x2.5crystal topology; genericland ypitch differs0.1016mm.'),
 'rtl8111g_qfn32':('qfn32_4x4',-90,'SameQFN4x4 32signal+EP33,0.4mm pitch. Existinggeneric keeps33pins; pad/row/corner deltas recorded.'),
 'ddr4-288p-akl_1':('ddr4_dimm_288p_pc',0,'Rename exactsource288pin DIMM definition to semanticgeneric, no geometry or pin renumbering.')
}
newassets={
 'mount_156a_p4567_pc':{'source':'mth_156a_1_1','reason':'Distinctphysical numbers4/5/6/7; keep independent from1/2/3/4mount.'},
 'ddr4_dimm_288p_pc':{'source':'ddr4-288p-akl_1','reason':'Exactcurrent288pin DIMM connector, without vendor/numeric suffix.'},
}
sourceboard=R/'w/via_alt13/PC13_FINAL.brd';assert sha(sourceboard)=='49AF5EE7252CA9E8C4C48D8F60AD4D1113DA559814585356B14F6150A195C063'
manifest=list(csv.DictReader((R/'w/final_alt13/manifest.tsv').open(encoding='utf-8'),delimiter='\t'));symbols=list(csv.DictReader((R/'w/final_alt13/symbols.tsv').open(encoding='utf-8'),delimiter='\t'));refs=defaultdict(list)
for r in symbols:refs[r['symbol_name'].lower()].append(r)
cached={}
for r in manifest:
 e=N.inspect(Path(r['file']));e.update(stem=r['name'],source_sha256=sha(r['file']));cached[r['name'].lower()]=e
for target,row in newassets.items():
 source=row['source'];assert source in files;row['assets']=[]
 for ext in ['psm','dra']:
  p=Path(files[source]['path']).with_suffix('.'+ext);assert p.is_file();row['assets'].append({'source':str(p),'source_sha256':sha(p),'target':str(p.with_name(target+'.'+ext)),'target_must_be_absent':True,'independent_byte_copy_required':True})
 # Exactclone geometry can be planned from current cached definition without asserting yet-cold output.
 idx[target]=copy.deepcopy(cached[source]);idx[target]['stem']=target
def schema(e):return Counter((p['number'],p['is_mechanical'],p['is_through']) for p in e['pins'])
def rotate(xy,angle):
 x,y=map(Decimal,xy);return {0:(x,y),90:(-y,x),180:(-x,-y),270:(y,-x)}[angle%360]
packages=[];changes=[];pad_deltas=[]
for name,source in cached.items():
 row={'source_package':source['stem'],'actual_refs':[r['refdes'] for r in refs[name]],'physical_instances':len(refs[name]),'pin_count':source['pin_count'],'pin_numbers':source['pin_numbers'],'target':name,'rotation_delta_nonmirrored':0,'action':'KEEP_CURRENT_DISTINCT_OR_ALREADY_STANDARD_GENERIC'}
 if name in rules:
  target,angle,reason=rules[name];assert target in idx,(name,target,'targetmissing');te=idx[target];assert schema(source)==schema(te),(name,target,'numbered/mechanical/throughschemadiff')
  sm={p['number']:p for p in source['pins']};tm={p['number']:p for p in te['pins']};assert len(sm)==len(source['pins']) and len(tm)==len(te['pins'])
  local=[]
  for n in sm:
   s,t=sm[n],tm[n];q=rotate(t['local_xy_mm'],angle);delta=[q[i]-Decimal(s['local_xy_mm'][i]) for i in range(2)]
   local.append({'pin':n,'old_local_mm':s['local_xy_mm'],'new_local_after_pose_delta_mm':list(map(str,q)),'delta_local_in_old_pose_mm':list(map(str,delta)),'old_pad':s['pad_name'],'new_pad':t['pad_name'],'old_local_rotation':s['local_rotation'],'new_local_rotation':t['local_rotation'],'old_pin_summary':N.pin_summary({'pins':[s]})[0],'new_pin_summary':N.pin_summary({'pins':[t]})[0]})
  row.update(target=target,rotation_delta_nonmirrored=angle,action='STANDARDIZE_SAME_CASE_PRESERVING_ALL_NUMBERED_PHYSICAL_PADS',reason=reason,geometry_equivalent_claim=False,target_native_path=te['native_path'],target_native_sha256=te['native_sha256'],new_asset_cold_native_required=target in newassets,pin_delta_local=local)
  for symbol in refs[name]:
   # No old origin changes. Mirrored placements reverse the sign of the angle correction.
   mirrored=symbol['mirrored']=='t';rot_delta=-angle if mirrored else angle
   changes.append({'ref':symbol['refdes'],'from_package':source['stem'],'target_package':target,'delta':rot_delta,'origin_unchanged':True,'old_pose_x':symbol['x'],'old_pose_y':symbol['y'],'old_rotation':symbol['rotation'],'old_mirrored':symbol['mirrored'],'pin_count':source['pin_count'],'source_cached_native':source['native_path'],'source_cached_native_sha256':source['native_sha256'],'target_native':te['native_path'],'target_native_sha256':te['native_sha256'],'geometry_equivalent_claim':False,'native_all6521_GetConnect_and_pin_readback_required':True})
  pad_deltas.append(row)
 else:
  if name=='sot23-akak':row['preserve_reason']='DistinctA/K/KA numbered diode network; cannot replace by1/2/3SOT.'
  elif name in {'diode_1n5817','diode_1n5817_4148'}:row['preserve_reason']='Same2terminal numbering alone does not prove samebody: these actualsource land pitches differ4.5974vs3.974084mm. Keep distinctactualcases;4148token is a deviceidentity, not arbitrarycopyindex.'
  elif name=='pin2x5_2d54_nc8':row['preserve_reason']='Differentabsent-keyposition; never mergewithNC10.'
  elif name.endswith('_pc'):row['preserve_reason']='Alreadyapprovedcanonical; no furtherchange.'
  else:row['preserve_reason']='No confirmedsame-case duplicate target within all81/3383name inventory; retain unique actualfunctionaldefinition.'
 packages.append(row)
assert len(packages)==81 and sum(p['physical_instances'] for p in packages)==1066
dump(O/'ALL81_PACKAGE_CANONICAL_DECISIONS.json',packages);dump(O/'ALL81_PHYSICAL_REF_MIGRATION_ROWS.json',changes);dump(O/'ALL81_PACKAGE_LOCAL_PAD_DELTA_LEDGER.json',pad_deltas);dump(O/'ALL81_NEW_EXACT_CANONICAL_ASSETS.json',{'status':'PROPOSED_TWO_EXACT_GEOMETRY_CLONES_NO_OVERWRITE_NO_PUBLIC_WRITE','targets':newassets})
tsv=O/'ALL81_PHYSICAL_REF_MIGRATION.tsv';tsv.write_text('refdes\tfrom_package\ttarget_package\tdelta\n'+'\n'.join('\t'.join(str(x[k]) for k in ['ref','from_package','target_package','delta']) for x in changes)+'\n',encoding='utf-8')
# Complete1131instances derive from actual latestcn2, retaining every Value and source identity.
xp=R/'w/sot34_xn2/native_design.xml';root=ET.parse(xp).getroot();instrows=[];fpchanges=[]
for page in root.findall('.//Page'):
 pd=page.find('Defn');pn=pd.get('name') if pd is not None else ''
 for inst in page.findall('.//PartInst'):
  d=inst.find('Defn');props={u.find('Defn').get('name'):u.find('Defn') for u in inst.findall('.//PartInstUserProp') if u.find('Defn') is not None}
  fp=props.get('PCB Footprint');refprop=props.get('Reference');ref=refprop.get('val') if refprop is not None else d.get('reference',d.get('name'))
  # Actual sourceXML reference is belowOccurrence/Defn or RefDes; compiler's existing map supplies known identity.
  instrows.append({'page':pn,'id':d.get('dbId'),'instance':d.get('name'),'old_footprint':fp.get('val') if fp is not None else None,'target':rules.get(fp.get('val').lower(),(fp.get('val'),))[0] if fp is not None else None})
assert len(instrows)==1131
dump(O/'LATEST_CN2_COMPLETE_INSTANCE_FP_TARGETS.json',instrows)
report={'status':'FROZEN_ALL81_CURRENT_PACKAGE_DECISIONS_AND_EXACT_DELTAS_NO_CAD_NO_PUBLIC_WRITE','source_board':str(sourceboard),'source_board_sha256':sha(sourceboard),'source_capture':str(R/'w/sot34_cn2/LGA1700.DSN'),'source_capture_sha256':sha(R/'w/sot34_cn2/LGA1700.DSN'),'source_capture_XML':str(xp),'source_capture_XML_sha256':sha(xp),'all_current_cached_package_definitions':81,'all_current_physical_components':1066,'packages_standardized':len(pad_deltas),'physical_refs_standardized_total_including_prior34':len(changes),'physical_refs_remaining_after_prior34':len(changes)-34,'new_exact_geometry_canonical_targets':list(newassets),'source_all_pin_schema_preserved':True,'keep_original_mount_SCH16_PCB4_and_USB_missing_pin':True,'limits':'No pin renumbering, no net assignment edits. Genericcases can differ in landpitch/size; sourcevsnewfullpinledger/localdelta explicitly recorded. Allphysical instances require native6521pad and completeGetConnectpartition gate; endpointoverlap is insufficient. Two newcanonicalclones need coldnative before apply. This is the boundedall81superset, not an invitation to expandafter eachbatch.','outputs':{str(p):sha(p) for p in O.glob('*') if p.is_file() and p.name!='ALL81_PLAN_SUMMARY.json'}}
dump(O/'ALL81_PLAN_SUMMARY.json',report);print(json.dumps(report,ensure_ascii=False,indent=2))
