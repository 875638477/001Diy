"""Prepare, but do not execute, eight cold native exports in main PCB context."""
from pathlib import Path
import hashlib,json
M=Path(__file__).parent;R=Path(r'D:\001DIY\004computer\lga1700\13shared_libraries_pc_20261025')
G=R.parent/'cadence_geometry_merge_20261025';D=M/'project8_mils2_plan13';assert not D.exists();D.mkdir()
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest().upper()
def dump(p,x):p.write_text(json.dumps(x,indent=2),encoding='utf-8')
base=M/'run_global_suffix_psm_native_audit_v3_cold.py';s=base.read_text()
old="job='('+b.q(row['stem'])+' '+b.q(row['audit_output'])+' '+b.q(row['original_units'])+' '+str(row['original_accuracy'])+' '+lit+')'"
new="job='('+b.q(row['stem'])+' '+b.q(row['audit_output'])+' '+b.q('mils')+' 2 ((-33500.0 -33500.0) (33500.0 33500.0)))'\n   row['audit_context_units']='mils';row['audit_context_accuracy']=2;row['audit_context_copper_layers']=['TOP','L2','L3','BOTTOM']"
assert old in s;s=s.replace(old,new)
s=s.replace("'schema':'GLOBAL_SUFFIX_COLD_PER_ASSET_NATIVE_V3'","'schema':'PROJECT8_MAIN_MILS2_FOUR_LAYER_COLD_V1'")
runner=M/'run_project8_mils2_cold.py';assert not runner.exists();runner.write_text(s,encoding='utf-8')
names=['ddr4_dimm_288p_pc','lqfp-48','mount_156a_p4567_pc','qfn32_4x4','smd_3225','sod323','sop-8-e-150mil','sot23-3']
representatives=[]
for name in names:
 p=Path(r'D:\001DIY\005lib\01Psm_lib')/(name+'.psm');assert p.is_file()
 representatives.append(dict(stem=name,path=str(p),sha256=sha(p),byte_identical_members=[str(p)],classification='CURRENT_PROJECT13_NEW_TARGET_PUBLIC_FULL_NATIVE_MAIN_CONTEXT',canonical_candidate=None))
guard=[]
for root in (Path(r'D:\001DIY\005lib\01Psm_lib'),Path(r'D:\001DIY\005lib\01Pad_lib')):
 for p in sorted(root.rglob('*')):
  if p.is_file() and p.suffix.casefold() in ('.psm','.pad','.ssm','.fsm','.bsm','.osm','.lsm'):
   guard.append(dict(path=str(p),sha256=sha(p)))
guardfile=D/'PCB_PUBLIC_GUARD.json';dump(guardfile,{'files':guard})
helper=R/'w/pcb_migration/run_pc_native_audit.py'
helpers=[helper,G/'psm_native_units.il',G/'psm_export.il',M/'fixture4/EMPTY4.brd',G/'symbol_probe/units_view.txt']
plan={'schema':'GLOBAL_SUFFIX_PUBLIC_NATIVE_AUDIT_PLAN_V1','public_guard_manifest':str(guardfile),
 'helpers':[{'path':str(p),'sha256':sha(p)} for p in helpers],
 'psmpath':'D:/001DIY/005lib/01Psm_lib','padpath':'D:/001DIY/005lib/01Pad_lib',
 'representatives':representatives,'purpose':'Eight new current59 embedded-cache names. Every asset is loaded fresh from public paths into empty four-copper-layer fixture at mils2, avoiding any cache reuse. Original PSM unit metadata preserved separately; audit job explicitly uses PCB mils2.'}
dump(D/'PROJECT8_MILS2_PLAN.json',plan)
receipt={'status':'PREPARED_ONLY_ROOT_RUNS_NATIVE','runner':str(runner),'runner_sha256':sha(runner),'plan':str(D/'PROJECT8_MILS2_PLAN.json'),'plan_sha256':sha(D/'PROJECT8_MILS2_PLAN.json'),'public_pcb_guarded_files':len(guard),'names':names,'source_runner_sha256':sha(base)}
dump(D/'PREPARATION.json',receipt);print(json.dumps(receipt,indent=2))
