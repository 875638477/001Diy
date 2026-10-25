"""Predict explicit per-ref PST pin declaration changes from two Capture XML files.
Never reads PST files. The strict and bounded PST comparers remain separate gates.
Only references present in the supplied reviewed template classification traces
are eligible; unchanged declarations are omitted from the resulting allowlist.
"""
import argparse,collections,hashlib,json,pathlib,xml.etree.ElementTree as ET

PROVENANCE='SOURCE_AND_TARGET_LIBRARY_XML_BEFORE_PST_EXPORT'

def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest().upper()
def definition(element):
    node=element.find('Defn') if element is not None else None
    return dict(node.attrib) if node is not None else {}
def dump(path,data):path.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

def trace_references(paths):
    result=collections.defaultdict(list);manifest=[]
    for path in paths:
        data=json.loads(path.read_text(encoding='utf-8-sig'));manifest.append({'path':str(path),'sha256':sha(path)})
        if isinstance(data,list):rows=data
        elif isinstance(data,dict) and isinstance(data.get('references'),dict):rows=[dict(value,ref=ref) for ref,value in data['references'].items()]
        elif isinstance(data,dict) and isinstance(data.get('rows'),list):rows=data['rows']
        else:raise ValueError('Unsupported classification trace schema: '+str(path))
        for row in rows:
            ref=row.get('ref') or row.get('reference')
            if not isinstance(ref,str) or not ref:raise ValueError('Trace row lacks explicit physical ref')
            compact={key:row[key] for key in ('ref','reference','instance_id','family','kind','material','old_package','new_package','reason','basis','authorization') if key in row}
            compact['trace_file']=str(path);result[ref].append(compact)
    return dict(result),manifest

def inventory(path,eligible):
    root=ET.parse(path).getroot();packages={definition(p)['name']:p for p in root.findall('Cache/Package')};result={}
    for page in root.findall('Schematic/Page'):
        for inst in page.findall('PartInst'):
            ref=definition(inst.find('Reference')).get('name','')
            if ref not in eligible:continue
            if ref in result:raise ValueError('Eligible reference has multiple units; requires an explicit section-aware plan: '+ref)
            attrs=definition(inst);package=packages[attrs['pkgName']];graphic=definition(inst.find('GraphicName')).get('name')
            matches=[(lp,view) for lp in package.findall('LibPart') for view in lp if view.tag in {'NormalView','ConvertView'} and definition(lp).get('CellName','')+definition(view).get('suffix','')==graphic]
            if len(matches)!=1:raise ValueError('Ambiguous active cache view: '+ref)
            lp,view=matches[0];records=[definition(p) for p in lp.findall('PhysicalPart/PinNumber')]
            if any(not r.get('position','').isdigit() or not r.get('number') for r in records):raise ValueError('Unsupported physical pin mapping: '+ref)
            if len({r['position'] for r in records})!=len(records) or len({r['number'] for r in records})!=len(records):raise ValueError('Repeated physical position/number: '+ref)
            cachepins={definition(pin)['position']:pin for pin in view.findall('SymbolPinScalar')}
            if len(cachepins)!=len(view.findall('SymbolPinScalar')):raise ValueError('Repeated scalar pin position: '+ref)
            if view.findall('SymbolPinBus'):raise ValueError('Bus pin not supported by scalar declaration plan: '+ref)
            sequence=[];payload={}
            for record in sorted(records,key=lambda r:int(r['position'])):
                pos,num=record['position'],record['number']
                if pos not in cachepins:raise ValueError('Missing cache scalar pin for physical mapping: '+ref+'.'+num)
                pin=cachepins[pos];pinattrs=definition(pin)
                # PST uses the fixed cache pin name, not a placed Name override.
                sequence.append({'number':num,'name':pinattrs.get('name','')})
                payload[num]={'type':pinattrs.get('type'),'visible':pinattrs.get('visible'),'flags':{tag:definition(pin.find(tag)) for tag in ('IsClock','IsDot','IsLeftPointing','IsRightPointing','IsNetStyle','IsNoConnect','IsGlobal')},'physical_mapping_fields':{key:value for key,value in record.items() if key!='position'}}
            shared=[definition(p) for p in lp.findall('PhysicalPart/PinShared')]
            if shared:raise ValueError('Shared physical pins require a separate explicit review: '+ref)
            result[ref]={'page':definition(page).get('name',''),'instance_id':attrs['dbId'],'package':attrs['pkgName'],'graphic':graphic,'sequence':sequence,'electrical_by_number':payload,'physical_position_records':records}
    missing=sorted(set(eligible)-set(result))
    if missing:raise ValueError('Classification trace has references absent from XML: '+','.join(missing))
    return result

def generate(source,target,traces):
    eligible,manifest=trace_references(traces);before=inventory(source,eligible);after=inventory(target,eligible);references={}
    for ref in sorted(eligible):
        old,new=before[ref],after[ref]
        if old['instance_id']!=new['instance_id']:raise ValueError('Stable instance identity changed: '+ref)
        if old['electrical_by_number']!=new['electrical_by_number']:raise ValueError('Physical pin number/type/visibility/electrical flags changed: '+ref)
        if old['sequence']==new['sequence']:continue
        references[ref]={'before':old['sequence'],'after':new['sequence'],'source_package':old['package'],'target_package':new['package'],'source_graphic':old['graphic'],'target_graphic':new['graphic'],'instance_id':old['instance_id'],'classification_trace':eligible[ref],'complete_declared_physical_number_and_electrical_fields_equal':True,'declaration_order_rule':'Sort PhysicalPart.PinNumber by integer position; pin name from active SymbolPinScalar.name, never placed instance Name override.'}
    return {'provenance':PROVENANCE,'status':'READY_PRE_EXPORT_XML_DECLARATION_PLAN_NOT_A_PST_PASS','source_xml_sha256':sha(source),'target_xml_sha256':sha(target),'source_xml':str(source),'target_xml':str(target),'classification_trace_files':manifest,'eligible_template_references':len(eligible),'changed_declaration_references':len(references),'references':references,'PST_files_read':False,'scope':'Only these independently predicted ordered pin-name declarations are eligible. The bounded comparer must still require exact physical-number-keyed full PST pin payload, sections and primitive body fields; all other refs remain exact. Connectivity requires a separate partition gate.'}

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    for name in ('source-xml','target-xml','output'):parser.add_argument('--'+name,required=True,type=pathlib.Path)
    parser.add_argument('--classification-trace',required=True,action='append',type=pathlib.Path)
    args=parser.parse_args()
    if args.output.exists():parser.error('Use a fresh output path; keep previous plans as evidence')
    source_sha=sha(args.source_xml);target_sha=sha(args.target_xml);report=generate(args.source_xml,args.target_xml,args.classification_trace)
    assert sha(args.source_xml)==source_sha and sha(args.target_xml)==target_sha
    args.output.parent.mkdir(parents=True,exist_ok=True);dump(args.output,report)
    print(json.dumps({'status':report['status'],'eligible_template_references':report['eligible_template_references'],'changed_declaration_references':report['changed_declaration_references'],'source_xml_sha256':source_sha,'target_xml_sha256':target_sha}))
if __name__=='__main__':main()
