"""Compare saved native readback, preserving raw Tcl reports as evidence."""
from pathlib import Path
import csv, hashlib, json, shutil, sys, tkinter
sys.stdout.reconfigure(encoding='utf-8')
root=Path(__file__).resolve().parents[1]
logs=root/'logs/lesson14_capture_20261019/independent_natural'
out=root/'examples/lesson14_capture/final'
tcl=tkinter.Tcl()
def seq(value):return tcl.splitlist(value)
def dct(value):
    x=seq(value);return dict(zip(x[::2],x[1::2]))
def report(path):return dct(seq(path.read_text(encoding='utf-8'))[1])
def part(snapshot):
    p=report(snapshot/'package.tcldict')
    device=dct(seq(p['devices'])[0]);body=dct(seq(device['parts'])[0])
    body['props']=dct(body['properties']);body['pins']=[dct(x) for x in seq(body['pins'])]
    body['vectors']=[dct(x) for x in seq(body['vectors'])]
    return p,body
def instance(snapshot,reference):
    x=report(snapshot/(reference+'.tcldict'));x['props']=dct(x['properties']);x['pins']=[dct(p) for p in seq(x['pins'])];return x
def connectivity(mode):
    with (logs/mode/'connectivity.tsv').open(encoding='utf-8') as f:
        return {tuple(x[k] for k in ('flat_net','reference','pin_number','pin_name','page')) for x in csv.DictReader(f,delimiter='\t')}
errors=[];checks=[]
def check(condition,label):
    checks.append({'check':label,'passed':bool(condition)})
    if not condition:errors.append(label)
base=logs/'baseline/snapshot';bp,bb=part(base);bn=connectivity('baseline')
check(len(bb['vectors'])==4,'Baseline has four native body vectors')
check({p['number'] for p in bb['pins']}=={str(n) for n in range(1,17)},'Baseline has physical pins 1..16 and no EP17')
summary={}
for mode in ('update_preserve','relocated_preserve','replace_properties'):
    snap=logs/mode/'snapshot';pkg,body=part(snap)
    check(len(body['vectors'])==5,mode+': native V2 has five body vectors')
    check(body['props']['LIB_REV']=='C14_V2',mode+': native saved cache is V2')
    check(body['props']['MPN']=='QMI8610_MPN_V2',mode+': cached MPN updated')
    check(body['value']=='QMI8610_V2',mode+': cached Value updated')
    compare=('number','name','type','start','hotSpot','visible','noConnect')
    pinmap=lambda b:{p['number']:tuple(p[k] for k in compare) for p in b['pins']}
    check(pinmap(body)==pinmap(bb),mode+': source numbering/electrical types/pin geometry unchanged')
    check(all(p['numberVisible']=='1' for p in body['pins']),mode+': final cached physical pin numbers remain visible')
    check(connectivity(mode)==bn,mode+': complete saved native connectivity set unchanged')
    summary[mode]={'vectors':len(body['vectors']),'LIB_REV':body['props']['LIB_REV'],'instances':{},'connectivity_unique_rows':len(bn)}
    for ref in ('U1401','U1402'):
        old=instance(base,ref);new=instance(snap,ref)
        check(new['reference']==old['reference']==ref,mode+': '+ref+' reference preserved')
        check(new['location']==old['location'],mode+': '+ref+' location preserved')
        comparep=lambda x:{p['number']:tuple(p[k] for k in ('number','name','type','hotSpot','visible')) for p in x['pins']}
        check(comparep(new)==comparep(old),mode+': '+ref+' physical pins and hotspots preserved')
        keep=(mode!='replace_properties' and ref=='U1402')
        expected_value='INSTANCE_VALUE_OVERRIDE' if keep else 'QMI8610_V2'
        expected_mpn='INSTANCE_MPN_OVERRIDE' if keep else 'QMI8610_MPN_V2'
        expected_custom='INSTANCE_CUSTOM_OVERRIDE' if keep else 'LIB_DEFAULT_V2'
        expected_fp='C14_PROP_SENTINEL_NOT_FOR_PCB' if keep else 'qmi8610_lga16_3d3_p0d5'
        check(new['props']['Value']==expected_value,mode+': '+ref+' Value policy')
        check(new['props']['MPN']==expected_mpn,mode+': '+ref+' MPN policy')
        check(new['props']['C14_INST_OVERRIDE']==expected_custom,mode+': '+ref+' custom property policy')
        check(new['footprint']==expected_fp,mode+': '+ref+' footprint policy')
        active_source=new['sourceLibrary'].replace('/','\\').upper()
        check(active_source.endswith('LESSON14_CAPTURE\\FINAL\\LIBRARY\\C14_QMI8610_V2.OLB'),mode+': '+ref+' active source points to delivered V2 OLB')
        summary[mode]['instances'][ref]={k:new['props'][k] for k in ('Value','MPN','LIB_REV','C14_INST_OVERRIDE')}
        summary[mode]['instances'][ref]['footprint']=new['footprint']
    cache=report(snap/'cache.tcldict')
    paths={dct(x)['sourceLibrary'] for x in seq(cache['objects'])}
    check(any('LESSON14_CAPTURE\\FINAL\\LIBRARY\\C14_QMI8610_V2.OLB' in p.upper() for p in paths),mode+': V2 OLB is present in cache provenance')
    summary[mode]['source_libraries']=sorted(paths)
dependency_source=root/'examples/qmi8610/library'
dependencies=[]
for path in sorted(dependency_source.iterdir()):
    if path.suffix.lower() in ('.dra','.psm','.pad'):
        target=out/'library'/path.name
        if not target.exists():shutil.copy2(path,target)
        sha=lambda x:hashlib.sha256(x.read_bytes()).hexdigest()
        check(sha(path)==sha(target),'Delivered dependency byte-identical: '+path.name)
        dependencies.append({'source':str(path),'path':str(target),'bytes':target.stat().st_size,'sha256':sha(target)})
ready=out/'c14_ready.dsn'
if not ready.exists():shutil.copy2(out/'c14_replace_properties.dsn',ready)
delivery=report(logs/'delivery_olb.tcldict')
delivery_device=dct(seq(delivery['devices'])[0]);delivery_body=dct(seq(delivery_device['parts'])[0])
delivery_pins=[dct(p) for p in seq(delivery_body['pins'])]
check(all(p['numberVisible']=='1' for p in delivery_pins),'Delivered final OLB pin numbering visibility matches placed cache')
for ref in ('U1401','U1402'):
    x=instance(logs/'ready/snapshot',ref)
    check(x['footprint']=='qmi8610_lga16_3d3_p0d5','Ready design '+ref+' uses real footprint')
check(connectivity('ready')==bn,'Ready design connectivity preserved in an independent native process')
observations=[
 'Initial validation retained as validation_initial.json: it tested experimental per-pin number visibility propagation and absence of unused old caches. Those two expectations were not met.',
 'Native ReplaceInst normalized experimental pin4 numberVisible=0 to 1. Final delivery OLB was explicitly restored to visible numbering; both source and placed cache were then reopened and matched.',
 'Native ReplaceInst retains old unused cache entries. Active instance GetSourceLibName is checked directly; it points to final/library/c14_qmi8610_v2.olb.',
 'UpdateCache/ReplaceCache attempts did not meet acceptance; actual successful route is ReplaceInst followed by explicit RefDes and selected override restoration.',
 'The two preserve-mode exercises intentionally retain the footprint sentinel on U1402. Only c14_ready.dsn / c14_replace_properties.dsn use the real footprint on both instances.',
 'Final connectivity readback uses naturally loaded single-page schematics with no forced Expand. Earlier expanded snapshots are preserved as history because forced Expand duplicated containers.'
]
with (logs/'baseline/connectivity.tsv').open(encoding='utf-8') as f:raw_rows=len(list(csv.DictReader(f,delimiter='\t')))
result={'date':'2026-10-19 Asia/Shanghai','status':'passed' if not errors else 'failed','errors':errors,'checks':checks,'summary':summary,'connectivity_raw_rows_per_design':raw_rows,'connectivity_unique_rows':len(bn),'dependencies':dependencies,'ready_design':str(ready),'method':'Native ReplaceInst plus explicit saved reference and selected instance override policy; UpdateCache/ReplaceCache API attempts are not counted as successful.','observations':observations}
dest=root/'logs/lesson14_capture_20261019/validation.json'
dest.write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({'status':result['status'],'check_count':len(checks),'errors':errors,'summary':summary,'dependencies':dependencies},ensure_ascii=False,indent=2))
sys.exit(bool(errors))
