import pathlib,json,hashlib,datetime,argparse,csv
ROOT=pathlib.Path(__file__).resolve().parents[1];BASE=ROOT/'examples/de_15_26_20261019'
p=argparse.ArgumentParser();p.add_argument('--flow-dir',choices=['native_flow','native_flow_final'],default='native_flow_final');args=p.parse_args();FLOW=BASE/args.flow_dir
comparison=json.loads((FLOW/'independent_compare.json').read_text(encoding='utf-8'))
assert comparison['status']=='PASS_NATIVE_FLOW_COMPARE'
assert comparison['baselineComponents']==comparison['ecoComponents']==80
assert comparison['baselinePins']==comparison['ecoPins']==272
assert comparison['addedComponents']==comparison['removedComponents']==[]
assert comparison['pinChanges']==[{'refdes':'J13','pin':'7','before':'GPIO_PB8','after':'GPIO_PB9'},{'refdes':'J13','pin':'8','before':'GPIO_PB9','after':'GPIO_PB8'}]
assert {x['refdes'] for x in comparison['propertyChanges']}=={'R19','R20'}
for x in comparison['propertyChanges']:
    assert {k:(x['before'].get(k),x['after'].get(k)) for k in set(x['before'])|set(x['after']) if x['before'].get(k)!=x['after'].get(k)}=={'VALUE':('2.2k','3.3k')}
processes=[]
for p in sorted((FLOW/'logs').glob('*/launch.json')):
    m=json.loads(p.read_text());assert m['exitCode']==0 and m['completed']
    processes.append({'stage':p.parent.name,**m})
assert len(processes)==8
result=json.loads((FLOW/'flow_result.json').read_text())
crossSections={}
for case in ['baseline','eco']:
    rows=list(csv.DictReader((FLOW/(case+'_readback')/'cross_section.tsv').open(),delimiter='\t'))
    for row in rows:
        row['name']=row['name'].strip('"');row['layerType']=row['layerType'].strip('"')
    crossSections[case]=rows
assert crossSections['baseline']==crossSections['eco'],'ECO changed physical cross section'
conductors=[row['name'] for row in crossSections['baseline'] if row['layerType']=='CONDUCTOR']
assert conductors[0]=='TOP' and conductors[-1]=='BOTTOM','Outer conductor naming does not follow TOP to BOTTOM'
layerEvidence={'status':'PASS_NATIVE_LAYER_NAMING_READBACK','nativeCrossSection':crossSections,'conductorOrder':conductors,'interpretation':'Default netlist-host cross section only. No manufacturing stackup, dielectric/material/impedance or production layer-count approval is claimed. F28 defines and verifies the actual PCB stackup.'}
(FLOW/'native_layer_evidence.json').write_text(json.dumps(layerEvidence,indent=2),encoding='utf-8')
result.update(status='PASS_NATIVE_EXPORT_IMPORT_ECO_REVERSE_COMPARE',independentChecks=comparison['checks'],independentReport='independent_compare.json',nativeProcesses=processes,baselineComponents=80,ecoComponents=80,physicalPinsPerDesign=272,netsPerDesign=69,placedSymbolsPerDesign=0,explicitNoConnectPinsPerDesign=6,logicalECOChanges={'resistors':['R19 2.2k -> 3.3k','R20 2.2k -> 3.3k'],'connectorPins':['J13.7 GPIO_PB8 -> GPIO_PB9','J13.8 GPIO_PB9 -> GPIO_PB8']},nativeECOReport='logs/import_eco/eco.txt',reverseSWP='feedback/DE_ECO.swp',nonfatalDiagnostic='pstswp reverse mode attempts feedbackview.cdsz unzip first; absent archive emits stderr then the program reads all four VIEW DAT files, generates a Flags-only SWP, and exits 0. Diagnostic is preserved.',acceptedSchematicPagePolicy='Single-page native DSN with six circuit modules; preliminary six-page SDK designs failed native packaging and are excluded.')
result['layerEvidence']='native_layer_evidence.json'
(FLOW/'flow_result.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
files=[]
for directory in [BASE/'native',BASE/'library',FLOW]:
    for path in sorted(directory.rglob('*')):
        if path.is_file() and path.suffix.lower() in ['.dsn','.olb','.dra','.psm','.pad','.pxml','.dat','.swp','.brd','.cfg','.csv','.tsv','.json','.txt','.scr']:
            files.append({'path':str(path.relative_to(BASE)),'bytes':path.stat().st_size,'sha256':hashlib.sha256(path.read_bytes()).hexdigest()})
for path in [BASE/'integrated_circuit.json',BASE/'integrated_circuit_eco.json',BASE/'BOM_baseline.csv',BASE/'BOM_eco.csv',BASE/'selected_footprints.json',BASE/'custom_package_specs.json']:
    assert path.is_file()
    files.append({'path':str(path.relative_to(BASE)),'bytes':path.stat().st_size,'sha256':hashlib.sha256(path.read_bytes()).hexdigest()})
(BASE/'native_backend_manifest.json').write_text(json.dumps({'dateAsiaShanghai':'2026-10-19','status':result['status'],'authoritativeBaseline':'native/de_integrated_single.dsn','authoritativeECO':'native/de_integrated_eco_final.dsn','nativeFlow':args.flow_dir+'/flow_result.json','layerEvidence':args.flow_dir+'/native_layer_evidence.json','dependencyValidation':'dependency_validation.json','historicalFlow':'native_flow','excludedPreliminaryDesigns':['native/DE_INTEGRATED_V1.DSN','native/DE_INTEGRATED_BASELINE.DSN','native/DE_INTEGRATED_SEQUENTIAL.DSN','native/de_integrated_eco.dsn'],'files':files},indent=2),encoding='utf-8')
print(json.dumps({'status':result['status'],'nativeProcesses':len(processes),'independentChecks':comparison['checks'],'manifestFiles':len(files)},indent=2))
