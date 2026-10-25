"""Independently compare native PST nodes against fresh native BRD readback."""
import argparse,csv,json,pathlib,re
p=argparse.ArgumentParser();p.add_argument('out');p.add_argument('--expected-baseline');p.add_argument('--expected-eco');a=p.parse_args();out=pathlib.Path(a.out).resolve()
assert out.is_relative_to(pathlib.Path(__file__).resolve().parents[1])
def parsepst(netdir):
    text=(netdir/'pstchip.dat').read_text()
    primitives={}
    for name,body in re.findall(r"primitive '([^']+)';(.*?)end_primitive;",text,re.S):
        body=body.split('  body',1)[1]
        primitives[name]=dict(re.findall(r"([\w_]+)='([^']*)';",body))
    parttext=(netdir/'pstxprt.dat').read_text()
    parts={ref:primitives[model] for ref,model in re.findall(r"PART_NAME\s+(\S+) '([^']+)':",parttext)}
    pins={};net=None
    for line in (netdir/'pstxnet.dat').read_text().splitlines():
        if line=='NET_NAME':net='NEXT';continue
        if net=='NEXT':
            net=line.strip().strip("'");continue
        match=re.match(r'NODE_NAME\s+(\S+)\s+(\S+)',line)
        if match:pins[tuple(match.groups())]='' if net=='NC' else net
    return parts,pins
def readbrd(folder):
    parts={r['refdes']:r for r in csv.DictReader((folder/'components.tsv').open(),delimiter='\t')}
    pins={(r['refdes'],r['pin']):r['net'] for r in csv.DictReader((folder/'component_pins.tsv').open(),delimiter='\t')}
    return parts,pins
checks=[]
def ck(ok,label):checks.append({'pass':bool(ok),'check':label});assert ok,label
maps={};partmaps={}
for case in ['baseline','eco']:
    parts,pins=parsepst(out/case/'netlist');actual,actualpins=readbrd(out/(case+'_readback'));partmaps[case]=parts;maps[case]=pins
    ck(set(parts)==set(actual),case+' exact native refdes set')
    ck(set(pins)==set(actualpins),case+' exact native pin set')
    for ref,attrs in parts.items():ck(attrs['JEDEC_TYPE'].lower()==actual[ref]['package'].lower(),case+' '+ref+' footprint')
    for key,net in pins.items():ck(actualpins[key]==net,case+' '+'.'.join(key)+' native connectivity')
    expectedfile=getattr(a,'expected_'+case)
    if expectedfile:
        spec=json.loads(pathlib.Path(expectedfile).read_text(encoding='utf-8'))
        expectedparts={c['ref']:c for c in spec['components']}
        # JSON null denotes an explicit NC; native BRD represents this as no net.
        expectedpins={(c['ref'],str(pin)):('' if net is None else net) for c in spec['components'] for pin,net in c['pins'].items()}
        ck(set(parts)==set(expectedparts),case+' original requirement exact refdes set')
        ck(set(pins)==set(expectedpins),case+' original requirement exact physical pin set')
        for key,net in expectedpins.items():ck(pins[key]==net,case+' original requirement '+'.'.join(key)+' net')
        for ref,c in expectedparts.items():
            ck(parts[ref]['JEDEC_TYPE'].lower()==spec['models'][c['model']]['footprint'].lower(),case+' original requirement '+ref+' footprint')
            ck(parts[ref].get('VALUE','').upper()==c['value'].upper(),case+' original requirement '+ref+' value')
pinChanges=[{'refdes':key[0],'pin':key[1],'before':maps['baseline'].get(key),'after':maps['eco'].get(key)} for key in sorted(set(maps['baseline'])|set(maps['eco'])) if maps['baseline'].get(key)!=maps['eco'].get(key)]
added=sorted(set(partmaps['eco'])-set(partmaps['baseline']));removed=sorted(set(partmaps['baseline'])-set(partmaps['eco']))
propChanges=[{'refdes':r,'before':partmaps['baseline'][r],'after':partmaps['eco'][r]} for r in sorted(set(partmaps['baseline'])&set(partmaps['eco'])) if partmaps['baseline'][r]!=partmaps['eco'][r]]
swp=(out/'feedback/DE_ECO.swp').read_text()
ck(not re.search(r'^\s*(?:CHANGEREF|PINSWAP|GATESWAP|CHANGEPIN)\b',swp,re.M),'native reverse SWP contains no unexpected renames/swaps')
ck(not re.search(r'^\.Section\d+ (?!Flags)',swp,re.M),'native reverse SWP contains no property delta sections')
result={'status':'PASS_NATIVE_FLOW_COMPARE','checks':len(checks),'baselineComponents':len(partmaps['baseline']),'ecoComponents':len(partmaps['eco']),'baselinePins':len(maps['baseline']),'ecoPins':len(maps['eco']),'addedComponents':added,'removedComponents':removed,'pinChanges':pinChanges,'propertyChanges':propChanges,'details':checks}
(out/'independent_compare.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
print(json.dumps({k:v for k,v in result.items() if k!='details'},indent=2))
