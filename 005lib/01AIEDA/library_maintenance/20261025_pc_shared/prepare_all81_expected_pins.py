"""All6521 native typed pads for bounded84-ref plan. Read-only, no inferred net changes."""
from pathlib import Path
from collections import defaultdict,Counter
from decimal import Decimal,ROUND_HALF_UP
import csv,copy,json,hashlib,importlib.util
M=Path(__file__).resolve().parent;R=Path(r'D:\001DIY\004computer\lga1700\13shared_libraries_pc_20261025');D=M/'project81_final_canonical_plan13';O=M/'project81_expected_pins13';O.mkdir(exist_ok=True)
jr=lambda p:json.loads(Path(p).read_text('utf-8-sig'));sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest().upper()
def put(n,v):p=O/n;p.write_text(json.dumps(v,ensure_ascii=False,indent=2),encoding='utf-8');return p
source=R/'w/pcb_migration/EXPECTED_BOARD_PINS_V3.json';base=jr(source);plans=jr(D/'ALL81_PHYSICAL_REF_MIGRATION_ROWS.json');package={r['source_package']:r for r in jr(D/'ALL81_PACKAGE_LOCAL_PAD_DELTA_LEDGER.json')};allpins=list(csv.DictReader((R/'w/final_alt13/all_symbol_pins.tsv').open(encoding='utf-8'),delimiter='\t'))
q=lambda v:Decimal(v).quantize(Decimal('0.01'),rounding=ROUND_HALF_UP)
norm=lambda v:str(q(v).normalize())
rawkey=lambda r:(r['refdes'],r['number'],norm(r['x']),norm(r['y']),r['net'],r['mechanical'],r['through'],r['padstack'])
oldkey=lambda r:(r['ref'],r['pin'],norm(r['expected_x']),norm(r['expected_y']),r['net'],r['isMech'],r['isThrough'],r['new_padstack'])
assert len(base)==len(allpins)==6521 and Counter(map(rawkey,allpins))==Counter(map(oldkey,base))
actual=defaultdict(list)
for p in allpins:actual[p['refdes']].append(p)
mats=[((1,0),(0,1)),((0,-1),(1,0)),((-1,0),(0,-1)),((0,1),(-1,0)),((-1,0),(0,1)),((1,0),(0,-1)),((0,1),(1,0)),((0,-1),(-1,0))]
def transform(mat,xy):x,y=map(Decimal,xy);return(mat[0][0]*x+mat[0][1]*y,mat[1][0]*x+mat[1][1]*y)
expected={};poseproof=[]
for row in plans:
 ref=row['ref'];p=package[row['from_package']];pins=p['pin_delta_local'];src={x['pin']:x for x in pins};origin=list(map(Decimal,[row['old_pose_x'],row['old_pose_y']]))
 possible=[]
 for mat in mats:
  err=[]
  for a in actual[ref]:
   pin=src[a['number']];s=transform(mat,[Decimal(v)/Decimal('.0254') for v in pin['old_local_mm']]);err+= [abs(s[i]+origin[i]-Decimal(a['x' if i==0 else 'y'])) for i in range(2)]
  if max(err,default=Decimal(0))<=Decimal('0.0000001'):possible.append((mat,max(err,default=Decimal(0))))
 assert possible,(ref,'No exact old worldpin D4posefit')
 # Pin1/2collinear footprints have mirrored equivalent solutions; native pose resolves their handedness.
 # Use original native mirror + worldrotation to disambiguate when the pin set alone is rank1.
 rot=int(Decimal(row['old_rotation']))%360;mir=row['old_mirrored']=='t'
 native_rot={0:((1,0),(0,1)),90:((0,-1),(1,0)),180:((-1,0),(0,-1)),270:((0,1),(-1,0))}[rot]
 # Allegro mirrored symbols reflect local x; sourceworld observations are authoritative if they disagree.
 preferred=(( -native_rot[0][0],native_rot[0][1]),(-native_rot[1][0],native_rot[1][1])) if mir else native_rot
 mat=next((m for m,e in possible if m==preferred),possible[0][0])
 # target coordinates already include R(delta) in old-local coordinates, then source actualD4pose transforms.
 for a in actual[ref]:
  pin=src[a['number']];n=pin['new_pin_summary'];txy=[Decimal(v)/Decimal('.0254') for v in pin['new_local_after_pose_delta_mm']]
  # Each native target local is first converted to the destination mils2 DB grid.
  txy=[q(v) for v in txy];local=transform(mat,txy);world=[str(q(local[i]+origin[i])) for i in range(2)]
  k=(ref,a['number']);assert k not in expected
  expected[k]={'world':world,'pad':pin['new_pad'],'mech':'t' if n['is_mechanical'] else 'nil','through':'t' if n['is_through'] else 'nil','target':row['target_package'],'source_record':copy.deepcopy(a),'source_pose_matrix':mat}
 poseproof.append({'ref':ref,'source_rotation':row['old_rotation'],'source_mirrored':row['old_mirrored'],'fitted_source_D4_matrix':mat,'all_worldpin_fit_error_lt_mil':'.0000001','target_rotation_delta':row['delta'],'native_actual_target_must_verify':True})
result=copy.deepcopy(base);changes=[]
for x in result:
 k=(x['ref'],x['pin'])
 if k not in expected:continue
 e=expected[k];old=copy.deepcopy(x);assert x['isMech']==e['mech'] and x['isThrough']==e['through']
 x['old_x'],x['old_y']=x['expected_x'],x['expected_y'];x['old_padstack']=x['new_padstack'];x['expected_x'],x['expected_y']=e['world'];x['new_padstack']=e['pad'];x['target']=e['target'];changes.append({'ref':x['ref'],'pin':x['pin'],'before':old,'after':copy.deepcopy(x),'world_coordinate_changed':list(map(norm,[old['expected_x'],old['expected_y']]))!=list(map(norm,e['world']))})
assert len(changes)==len(expected) and len(result)==6521
assert [x for x in base if(x['ref'],x['pin']) not in expected]==[x for x in result if(x['ref'],x['pin']) not in expected]
qstr=lambda s:json.dumps(s,ensure_ascii=False);byref=defaultdict(list)
for x in result:
 net='nil' if x['native_net_type']=='NIL' else qstr(x['net']);byref[x['ref']].append('('+qstr(x['pin'])+' ('+x['expected_x']+' '+x['expected_y']+') '+net+' '+x['isMech']+' '+x['isThrough']+' '+qstr(x['new_padstack'])+')')
ip=O/'ALL81_EXPECTED_PINS6521.ilist';ip.write_text('\n'.join('('+qstr(k)+' ('+' '.join(v)+'))' for k,v in sorted(byref.items()))+'\n',encoding='utf-8')
jp=put('ALL81_EXPECTED_BOARD_PINS6521.json',result);cp=put('ALL81_PIN_CHANGES.json',changes);pp=put('ALL81_SOURCE_POSE_EXACT_FITS.json',poseproof)
report={'status':'ALL81_84REF_FULL6521_TYPED_EXPECTED_PIN_LEDGER_PREPARED_NO_CAD','source_expected':str(source),'source_expected_sha256':sha(source),'source_board':str(R/'w/via_alt13/PC13_FINAL.brd'),'source_board_sha256':sha(R/'w/via_alt13/PC13_FINAL.brd'),'physical_components':len(byref),'physical_pad_count':len(result),'target_changed_refs':len(plans),'target_mapped_pad_records':len(changes),'pad_center_coordinate_changes':sum(x['world_coordinate_changed'] for x in changes),'unaltered_pad_records':len(result)-len(changes),'native_nil_nets':sum(x['native_net_type']=='NIL' for x in result),'native_empty_string_nets':sum(x['native_net_type']=='STRING' and x['net']=='' for x in result),'all_source_net_names_types_and_pin_number_multisets_preserved':True,'SC37_new_coordinates_preserved':True,'quantization':'Destination boardmils2; targetlocal rounded0.01mil, then actualsourceD4pose+unchangedorigin, final0.01mil grid. Actualnative targetpad readback required.','not_connection_approval':'Fullnative6521pad+typednet+completeGetConnectpartitions and targetland/stub object checks are required. Earlier34overlappreflight was insufficient to predict connectivity.','outputs':{str(p):sha(p) for p in [ip,jp,cp,pp]}}
put('ALL81_EXPECTED_LEDGER_READY.json',report);print(json.dumps(report,indent=2))
