"""Complete independent CFX/TCFX gate for preproved FP-only/public-library ECO.

Preserves complete Gate payloads with a unique generated-F identity bijection,
complete Part payloads, per-physical-ref expanded PartDefn multiplicities, and
every other ordered section. Only six explicitly planned VIA_LIST strings may
change. Source12 electrical ECO allowances are not inherited.
"""
from pathlib import Path
from collections import Counter
import argparse,ast,collections,copy,hashlib,importlib.util,json,re
import xml.etree.ElementTree as E

R=Path(r'D:\001DIY\004computer\lga1700\13shared_libraries_pc_20261025')
LEGACY=R.parent/'11rc_value_standardized_20261024/w/ni_review/pcb_gate_nc/review_cfx_value_only_eco.py'
SUPPORT=LEGACY.with_name('cfx_value_only_support.py')
W='http://www.cadence.com/xsd/wholeFile';O='http://www.cadence.com/xsd/objects';H='http://www.cadence.com/xsd/header';N={'w':W,'o':O,'h':H,'d':'http://www.cadence.com/xsd/dictionary'}
def need(ok,message):
 if not ok:raise ValueError(message)
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest().upper()
def load(p):return json.loads(Path(p).read_text(encoding='utf-8-sig'))
def module(p,name):
 s=importlib.util.spec_from_file_location(name,p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
need(sha(LEGACY)=='54F45843A7C6401F8CF79AF59F186B5D9AF558AEAE16E8CD596953B7B09A9602','Frozen CFX helper changed')
need(sha(SUPPORT)=='310E7438E2E305EFAEAD27077DFF82C13E01B43FF4A25BFC1C9FEBEA77E74C6F','Frozen PartDefn helper changed')
HELPERS={'canonical','enc','h','local','section','objects','named','wrap','normalize_gate','gate_review','part_review','gate_reference_review','sections','shell'}
tree=ast.parse(LEGACY.read_text(encoding='utf8'));funcs=[n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name in HELPERS]
need({f.name for f in funcs}==HELPERS,'Missing strict CFX helper')
NS={'E':E,'collections':collections,'copy':copy,'hashlib':hashlib,'json':json,'re':re,'W':W,'O':O,'H':H,'N':N,'gate_allowances':{}}
exec(compile(ast.Module(body=funcs,type_ignores=[]),'<unchanged strict CFX functions>','exec'),NS)
section,named,objects,enc,h=[NS[k] for k in ['section','named','objects','enc','h']]
S=module(SUPPORT,'frozen_full_partdefn_payload')
P=module(R/'tools/verify_library13_pst.py','independent_complete_pst_inverse')
VIA_MAP={'VIA_16_28':'VIA_16_28_PC','VIA_1D5_0D9':'VIA_1D5_0D9_PC','VIA_20_30':'VIA_20_30_PC'}
VIA_OWNERS={('PhysicalCSet','DEFAULT'),('PhysicalCSet','GND'),('PhysicalCSet','VCC3V3A'),('PhysicalCSet','VCC3V3'),('PhysicalCSet','VCC5V'),('Region','RUGULER1')}
ADMIN_NATIVE_OBSERVATIONS={
 '49B874ED98BD3F66EC23D115848C88E2F744195DEE9B35DC98F143674E055308':'63', # Final ALL81 native replacement/attachment; exact standalone readonly dictionary probe16.
 '9AE6414A4AE876ED594678A1648965AC6D0B90F8A6BF21D6AE23A63C356D5EF9':'40', # Old Always canary, never publish.
 '49AF5EE7252CA9E8C4C48D8F60AD4D1113DA559814585356B14F6150A195C063':'47', # Final Alt+native via import, exact fresh read-only observation.
}

def source_binding(source_cfx,source_tcfx):
 base=R/'w/b02';q=load(base/'launch_report.json');frozen=load(R/'verification/SOURCE_FREEZE.json')
 need(q['source_sha256_before']==q['source_sha256_after']==frozen['pcb_sha256']==sha(base/'INPUT_COPY.brd'),'Source native CFX board not frozen latest02')
 need(q['input_unchanged'] and q['exit_code']==0 and q['write_candidate'] is False and '-readonly' in q['arguments'],'Source not native readonly complete')
 need(sha(source_cfx)==sha(base/'ACTUAL_SUPPLEMENT.dcfx') and sha(source_tcfx)==sha(base/'ACTUAL_SUPPLEMENT.tcfx'),'CFX source not frozen actual latest02 native audit')
 return {'board_sha256':frozen['pcb_sha256'],'source_cfx_sha256':sha(source_cfx),'source_tcfx_sha256':sha(source_tcfx),'launch_report_sha256':sha(base/'launch_report.json')}
def pst_context(source,candidate,plan_path,proof_path):
 proof=load(proof_path);plan=load(plan_path)
 need(proof['status']=='PASS_COMPLETE_PST_FP_AND_SOURCE_PATH_ONLY','Independent actual PST gate is not PASS')
 need(proof['inputs']['plan_sha256']==sha(plan_path),'PST intent plan changed')
 for d,k in [(source,'source_sha256'),(candidate,'candidate_sha256')]:
  need({n:sha(d/n) for n in P.P.FILES}==proof['inputs'][k],'Actual PST bytes differ from proof')
 a,b=P.P.load_bundle(source),P.P.load_bundle(candidate);fresh=P.review(a,b,P.mappings(plan),P.pathmap(plan))
 need(fresh['status']=='PASS_COMPLETE_PST_FP_AND_SOURCE_PATH_ONLY','Fresh independent complete PST inverse failed')
 for key in ['physical_parts','physical_pins','nets','connectivity_partitions','planned_physical_FP_changes','planned_FP_refs_originally_excluded_from_physical_PST','physical_NC_value_refs_unchanged','generated_primitive_alias_changes','source_primitives','candidate_primitives']:
  need(fresh[key]==proof[key],'PST retained result differs from fresh review '+key)
 need(len(fresh['planned_physical_FP_changes'])==994 and len(fresh['planned_FP_refs_originally_excluded_from_physical_PST'])==31,'PST physical FP/excluded cohort differs from frozen final1031-field/994physical-ref scope')
 need(len(proof['negative_controls'])==7 and all(c['status']=='PASS_REJECTED' for c in proof['negative_controls']),'PST negative controls missing')
 return a,b,fresh
def ref_rows(a,b,definitions):
 rows=[]
 for ref in sorted(a['parts']):
  x,y=a['parts'][ref],b['parts'][ref]
  old=x['primitive']+':'+P.P.property_value(x['body'],'JEDEC_TYPE')+':'+P.P.property_value(x['body'],'VALUE')+':'
  new=y['primitive']+':'+P.P.property_value(y['body'],'JEDEC_TYPE').upper()+':'+P.P.property_value(y['body'],'VALUE')+':'
  need(old in definitions,'Source CFX lacks exact source PST composite '+ref)
  need(P.P.property_value(x['body'],'VALUE')==P.P.property_value(y['body'],'VALUE'),'Unplanned VALUE in identity mapping')
  rows.append({'ref':ref,'old_partdefn':old,'new_partdefn':new,'before_value':P.P.property_value(x['body'],'VALUE'),'after_value':P.P.property_value(y['body'],'VALUE'),'before_footprint':P.P.property_value(x['body'],'JEDEC_TYPE'),'after_footprint':P.P.property_value(y['body'],'JEDEC_TYPE'),'after_native_CFX_footprint_token':P.P.property_value(y['body'],'JEDEC_TYPE').upper(),'native_case_policy':'Only compiled CFX footprint token is uppercase; primitive and VALUE preserve exact PST spelling'})
 need({r['old_partdefn'] for r in rows}==set(definitions),'Unmapped/unreferenced source CFX PartDefn')
 need(sum(r['old_partdefn']!=r['new_partdefn'] for r in rows)==994,'CFX per-ref identity cohort differs from frozen994')
 return rows
def via_expected(base,plan):
 q=copy.deepcopy(base);ledger=[]
 if plan is None:return q,ledger
 need(plan['inverse_all_bytes_equal'] is True and len(plan['changes'])==6,'Via plan lacks exact six/inverse proof')
 need(sha(plan['source_cfx'])==plan['source_sha256'] and sha(plan['candidate_cfx'])==plan['candidate_sha256'],'Via explicit native-input intent artifact changed')
 need({(r['domain'],r['object']) for r in plan['changes']}==VIA_OWNERS,'Via six-owner cohort differs')
 for row in plan['changes']:
  need(':'.join(VIA_MAP.get(t,t) for t in row['old'].split(':'))==row['new'],'Via renaming not exact three approved tokens/list order')
  obj=named(section(q,row['domain']))[row['object']]
  values=obj.findall('o:attribute[@Name="VIA_LIST"]/o:value',N)
  need(len(values)==1 and values[0].get('Value')==row['old'],'Source exact VIA_LIST precondition differs '+repr(row))
  values[0].set('Value',row['new']);ledger.append(row)
 return q,ledger

def admin_property(root):
 design=objects(section(root,'Design'));need(len(design)==1,'Expected exactly one complete Design object')
 attrs=design[0].findall('o:attribute[@Name="MAX_FILENAME_VALUE"]',N)
 need(len(attrs)==1,'MAX_FILENAME_VALUE Design property missing or duplicated')
 values=attrs[0].findall('o:value',N);need(len(values)==1 and set(values[0].attrib)=={'Value'},'MAX_FILENAME_VALUE scalar shape changed')
 return values[0]

def admin_ledger_context(base,actual,plan_path):
 """Authenticate a native read-only property observation once, before controls.
 The validated context licenses only the exact SHA-bound observed value, never
 arbitrary metadata values or an observation from another candidate board.
 """
 if plan_path is None:return None
 p=load(plan_path)
 need(p['schema']=='CFX13_NATIVE_READONLY_ADMIN_METADATA_V1','Unknown admin metadata ledger schema')
 change=p['change'];target=change.get('new')
 need(change=={'domain':'Design','object':'@BOARD_NAME@','property':'MAX_FILENAME_VALUE','field':'attribute/value/@Value','old':'22','new':target,'data_type':'STRING','read_only':True},'Admin ledger field scope exceeds exact native property')
 need(set(p['artifacts'])=={'source_cfx','candidate_cfx','candidate_native_launch','readonly_property_probe','readonly_probe_launch'},'Admin ledger evidence cohort differs')
 evidence={}
 for k,v in p['artifacts'].items():
  path=Path(v['path']);need(sha(path)==v['sha256'],'Admin ledger artifact changed '+k);evidence[k]=path
 need(enc(E.parse(evidence['source_cfx']).getroot())==enc(base),'Admin ledger source CFX not this full input')
 need(enc(E.parse(evidence['candidate_cfx']).getroot())==enc(actual),'Admin ledger candidate CFX not this full input')
 need(evidence['candidate_native_launch'].parent==evidence['candidate_cfx'].parent,'Candidate CFX lacks same-directory native-launch binding')
 qs=[]
 for k in ['candidate_native_launch','readonly_probe_launch']:
  q=load(evidence[k]);need(q['exit_code']==0 and q['input_unchanged'] and q['write_candidate'] is False and '-readonly' in q['arguments'],'Admin evidence not protected native readonly '+k)
  need(q['source_sha256_before']==q['source_sha256_after']==q['staged_sha256']==sha(evidence[k].parent/'INPUT_COPY.brd'),'Admin evidence board byte binding failed '+k)
  need(sha(q['script'])==q['script_sha256'],'Native admin evidence script changed '+k);qs.append(q)
 need(qs[0]['source_sha256_before']==qs[1]['source_sha256_before'],'Read-only MAX property probe did not observe actual final candidate board')
 need(ADMIN_NATIVE_OBSERVATIONS.get(qs[0]['source_sha256_before'])==target,'Admin property value is not explicitly approved for this exact native board SHA')
 need(evidence['readonly_property_probe'].parent==evidence['readonly_probe_launch'].parent,'Read-only property probe not bound to this job')
 text=evidence['readonly_property_probe'].read_text(encoding='utf-8-sig');lines=text.splitlines()
 details=[s for s in lines if s.startswith('ENTRY_DETAILS=')];need(len(details)==1,'Ambiguous native property dictionary')
 for token in ['write t','useCount 1','objects ("designs" "layouts")','name "MAX_FILENAME_VALUE"','dataType "STRING"','readOnly t']:
  need(token in details[0],'Native dictionary does not establish exact read-only STRING Design property '+token)
 for prefix in ['BEFORE=','AFTER_PIN_METADATA=']:
  matches=[s for s in lines if s.startswith(prefix)];need(len(matches)==1 and re.findall(r'\(MAX_FILENAME_VALUE "([^"]*)"\)',matches[0])==[target],'Native read-only probe value is not exactly approved '+target+' '+prefix)
 need(admin_property(base).get('Value')=='22' and admin_property(actual).get('Value')==target,'Actual MAX source/candidate pair is not exact approved22->'+target)
 # CFX itself independently declares the same property as String, valid only Design.
 for root in [base,actual]:
  defs=[e for e in root.iter() if NS['local'](e)=='xml-userPropertyDefinitions'];need(len(defs)==1,'Missing full CFX property definitions')
  attrs=[e for e in defs[0].iter() if NS['local'](e)=='attribute' and e.get('Name')=='MAX_FILENAME_VALUE'];need(len(attrs)==1,'MAX user property declaration missing/duplicated')
  v=attrs[0].find('d:value',N);data=v.find('d:data',N) if v is not None else None
  need(v is not None and v.get('Kind')=='Property' and data is not None and data.attrib=={'Storage':'String','Type':'Scalar'},'MAX declaration not unchanged scalar String Property')
  need([e.text for e in attrs[0].findall('d:objects/d:valid/d:o',N)]==['Design'],'MAX property declaration is not exactly Design-only')
 return {'change':p['change'],'ledger_path':str(plan_path),'ledger_sha256':sha(plan_path),'artifacts':p['artifacts'],'actual_native_board_sha256':qs[0]['source_sha256_before'],'interpretation':'Native dictionary explicitly readOnly STRING, Design/layout administrative property; not an editable design constraint. Only this exact SHA-bound observed22->'+target+' serialization value is inversed; all other complete Design/CFX/TCFX data remain strict.'}

def admin_expected(base,context):
 q=copy.deepcopy(base)
 if context:
  need(admin_property(q).get('Value')=='22','MAX inverse source precondition changed')
  admin_property(q).set('Value',context['change']['new'])
 return q

def region_via_order_inverse(expected,actual,via):
 """Only planned RUGULER1/VIA_LIST may serialize last-attribute->first.
 The complete one attribute (including origin), multiplicity, all other child
 ordering and whole Region section must match after the single move inverse.
 """
 x,y=section(expected,'Region'),section(actual,'Region')
 if h(x)==h(y):return y,[]
 need(len(via)==6 and {tuple((r['domain'],r['object'])) for r in via}==VIA_OWNERS,'Region order inverse requires actual six-via intent cohort')
 old=named(x)['RUGULER1'];new=named(y)['RUGULER1']
 need(old.attrib==new.attrib,'Region RUGULER1 object attributes changed')
 a=[(i,c) for i,c in enumerate(old) if c.tag=='{'+O+'}attribute' and c.get('Name')=='VIA_LIST']
 b=[(i,c) for i,c in enumerate(new) if c.tag=='{'+O+'}attribute' and c.get('Name')=='VIA_LIST']
 need(len(a)==len(b)==1,'Region planned VIA_LIST multiplicity changed')
 (oi,oe),(ni,ne)=a[0],b[0]
 need(oi==62 and ni==0 and len(old)==len(new)==64 and sum(c.tag=='{'+O+'}attribute' for c in old)==63,'Region VIA_LIST order change is not exact last-attribute(index62)->first(index0)')
 need(enc(oe)==enc(ne),'Region VIA_LIST complete attribute payload (value/origin) changed')
 need([enc(c) for i,c in enumerate(old) if i!=oi]==[enc(c) for i,c in enumerate(new) if i!=ni],'Other Region attribute payload/order changed')
 normalized=copy.deepcopy(y);target=named(normalized)['RUGULER1'];moved=target[0];target.remove(moved);target.insert(oi,moved)
 need(enc(x)==enc(normalized),'Complete Region section differs after exact VIA_LIST order inverse')
 ledger=[{'domain':'Region','object':'RUGULER1','property':'VIA_LIST','expected_before_native_import_index':oi,'actual_after_native_import_index':ni,'child_count':len(old),'attribute_count':63,'complete_planned_attribute_sha256':h(oe),'actual_complete_attribute_sha256':h(ne),'inverse_complete_Region_sha256':h(normalized),'source_expected_complete_Region_sha256':h(x),'other_child_order_and_full_payload_exact':True,'multiplicity':1,'scope':'Only this explicitly planned six-via owner attribute moved from final attribute(index62) to first(index0); the SpacingCSet reference(index63) and all other children retain exact relative order/full payload. No other normalization.'}]
 return normalized,ledger
def metadata(a,b):
 result=[]
 for name,root in [('source',a),('candidate',b)]:
  header=root.find('w:xml-Header/h:root',N);design=objects(section(root,'Design'))[0]
  revision=header.find('h:revisionNumber',N)
  need(header.get('Name')==design.get('Name'),'Header/Design board names differ')
  need(revision is not None and (revision.get('physical') or '').isdecimal(),'Unrecognized native physical revision')
  result.append({'side':name,'board_name':header.get('Name'),'physical_revision':revision.get('physical')})
 return result
def validate(base,after,rows,via_plan=None,admin_context=None):
 expected,via=via_expected(base,via_plan)
 expected=admin_expected(expected,admin_context)
 need(NS['shell'](expected)==NS['shell'](after),'Complete CFX outer wrapper/section order differs')
 ss,tt=NS['sections'](expected),NS['sections'](after);need(set(ss)==set(tt),'CFX section cohort differs')
 tt['objects/Region'],region_order=region_via_order_inverse(expected,after,via)
 source_refs=NS['gate_reference_review'](expected);candidate_refs=NS['gate_reference_review'](after)
 gate,gmap=NS['gate_review'](section(expected,'Gate'),section(after,'Gate'),False)
 part=NS['part_review'](section(expected,'Part'),section(after,'Part'))
 definitions,dmap=S.review_definitions(section(expected,'PartDefn'),section(after,'PartDefn'),rows,True)
 checks=[]
 for key,node in ss.items():
  if key in {'objects/Gate','objects/Part','objects/PartDefn'}:continue
  need(h(node)==h(tt[key]),'Complete ordered CFX section differs '+key)
  checks.append({'section':key,'complete_ordered_payload_equal':True,'sha256':h(node)})
 need(len(named(section(after,'DiffPair')))==134 and len(named(section(after,'MatchGroup')))==42,'Differential pair/matched group counts differ')
 return {'Gate':gate,'Part':part,'PartDefn':definitions,'complete_other_sections':checks,'source_external_F_token_contexts':len(source_refs),'candidate_external_F_token_contexts':len(candidate_refs),'actual_unclassified_external_Gate_references':0,'all134_DiffPair_and42_MatchGroup_full_ordered_payloads_preserved':True,'via_list_exact_changes':via,'Region_RUGULER1_VIA_LIST_native_order_ledger':region_order,'native_readonly_admin_metadata':admin_context,'metadata':metadata(base,after)},gmap,dmap
def canonical_tcfx(a,b,via_plan=None,admin_context=None):
 def normalized(r):
  q=copy.deepcopy(r);header=q.find('w:xml-Header/h:root',N)
  if header is not None:
   design=q.find('w:dir-objects/w:xml-objects[@Name="Design"]/o:root/o:object',N)
   if design is not None:
    need(design.get('Name')==header.get('Name'),'TCFX Header/Design board names differ')
    design.set('Name','@BOARD_NAME@')
   header.set('Name','@BOARD_NAME@')
   revision=header.find('h:revisionNumber',N)
   if revision is not None and revision.get('physical') is not None:
    need(revision.get('physical').isdecimal(),'Invalid TCFX physical revision');revision.set('physical','@PHYSICAL_REVISION@')
  return q
 expected,via=via_expected(a,via_plan);expected=admin_expected(expected,admin_context)
 ordered,order_ledger=region_via_order_inverse(expected,b,via)
 candidate=copy.deepcopy(b);target=section(candidate,'Region');target[:]=[copy.deepcopy(e) for e in ordered]
 x,y=normalized(expected),normalized(candidate)
 need(enc(x)==enc(y),'Complete ordered TCFX configuration differs')
 return {'complete_ordered_configuration_preserved':True,'normalized_sha256':h(x),'source_board_name':a.find('w:xml-Header/h:root',N).get('Name'),'candidate_board_name':b.find('w:xml-Header/h:root',N).get('Name'),'exact_six_via_list_changes':via,'Region_VIA_LIST_serialization_order_ledger':order_ledger,'native_readonly_admin_metadata':admin_context,'scope':'Full TCFX inversed only for the same six via lists, same bounded Region attribute move and optional exact read-only administrative property as CFX; matched Header/Design names and existing physical revisions separately normalized. No other configuration field ignored.'}

def tcfx_controls(base,actual,via_plan,admin_context):
 out=[]
 def trial(name,fn):
  z=copy.deepcopy(actual);fn(z)
  try:canonical_tcfx(base,z,via_plan,admin_context)
  except Exception as ex:out.append({'name':name,'status':'PASS_REJECTED','reason':str(ex)[:1500]})
  else:raise ValueError('TCFX negative control accepted '+name)
 def design_other(z):E.SubElement(objects(section(z,'Design'))[0],'{'+O+'}attribute',Name='UNPLANNED_NUMERIC_RULE')
 trial('TCFX_unplanned_design_rule_or_property',design_other)
 if via_plan:
  trial('TCFX_Region_VIA_LIST_origin_changed',lambda z:named(section(z,'Region'))['RUGULER1'].find('o:attribute[@Name="VIA_LIST"]/o:origin/o:v',N).__setattr__('text','WRONG'))
  trial('TCFX_PhysicalCSet_VIA_LIST_wrong',lambda z:named(section(z,'PhysicalCSet'))['DEFAULT'].find('o:attribute[@Name="VIA_LIST"]/o:value',N).set('Value','WRONG'))
 if admin_context:
  bad=str(int(admin_context['change']['new'])+1)
  trial('TCFX_MAX_FILENAME_VALUE_'+bad+'_rejected',lambda z:admin_property(z).set('Value',bad))
 return out
def controls(base,actual,rows,via_plan,admin_context=None):
 out=[]
 def trial(name,fn):
  z=copy.deepcopy(actual);fn(z)
  try:validate(base,z,rows,via_plan,admin_context)
  except Exception as ex:out.append({'name':name,'status':'PASS_REJECTED','reason':str(ex)[:1500]})
  else:raise ValueError('Negative control accepted '+name)
 def first(section_name):return objects(section(actual,section_name))[0].get('Name')
 def attr(z,sec):E.SubElement(named(section(z,sec))[first(sec)],'{'+O+'}attribute',Name='UNPLANNED_CONSTRAINT')
 def alter_pin(z):
  pin=next(e for e in section(z,'Gate').iter() if e.tag=='{'+O+'}object' and e.get('AltName') is not None);pin.set('AltName','WRONG')
 def drop_pin(z):
  p=next(e for e in section(z,'Gate').iter() if e.tag=='{'+O+'}children' and len(e));p.remove(p[0])
 trial('Gate_Pin_AltName_changed',alter_pin);trial('Gate_Pin_removed',drop_pin)
 trial('Gate_constraint_added',lambda z:attr(z,'Gate'))
 trial('Part_constraint_added',lambda z:attr(z,'Part'))
 trial('PartDefn_constraint_added',lambda z:attr(z,'PartDefn'))
 trial('PartDefn_unplanned_composite',lambda z:objects(section(z,'PartDefn'))[0].set('Name','UNPLANNED_VALUE_OR_FP'))
 trial('PartDefn_duplicate_multiplicity',lambda z:section(z,'PartDefn').find('o:root',N).append(copy.deepcopy(objects(section(z,'PartDefn'))[0])))
 trial('DiffPair_member_changed',lambda z:objects(section(z,'DiffPair'))[0].find('o:member',N).set('Name','WRONG'))
 trial('MatchGroup_complete_attribute_added',lambda z:attr(z,'MatchGroup'))
 trial('PhysicalCSet_numeric_rule_not_ignored',lambda z:attr(z,'PhysicalCSet'))
 trial('Stackup_attribute_not_ignored',lambda z:attr(z,'Stackup'))
 trial('unknown_external_Gate_reference',lambda z:objects(section(z,'Design'))[0].set('UNCLASSIFIED_GATE_REFERENCE','F1'))
 trial('unplanned_net_deleted',lambda z:section(z,'Net').find('o:root',N).remove(objects(section(z,'Net'))[0]))
 if via_plan:
  def alter_via(z):named(section(z,'PhysicalCSet'))['DEFAULT'].find('o:attribute[@Name="VIA_LIST"]/o:value',N).set('Value','WRONG')
  trial('VIA_LIST_wrong_token_or_order',alter_via)
  def region_attr(z):return named(section(z,'Region'))['RUGULER1'].find('o:attribute[@Name="VIA_LIST"]',N)
  def region_duplicate(z):named(section(z,'Region'))['RUGULER1'].append(copy.deepcopy(region_attr(z)))
  def region_other_order(z):
   obj=named(section(z,'Region'))['RUGULER1'];indices=[i for i,c in enumerate(obj) if c.get('Name')!='VIA_LIST'];i,j=indices[:2];obj[i],obj[j]=obj[j],obj[i]
  def region_middle(z):
   obj=named(section(z,'Region'))['RUGULER1'];attr=region_attr(z);obj.remove(attr);obj.insert(1,attr)
  trial('Region_VIA_LIST_origin_changed',lambda z:region_attr(z).find('o:origin/o:v',N).__setattr__('text','WRONG'))
  trial('Region_VIA_LIST_value_changed',lambda z:region_attr(z).find('o:value',N).set('Value','WRONG'))
  trial('Region_VIA_LIST_attribute_duplicated',region_duplicate)
  trial('Region_other_attributes_relative_order_changed',region_other_order)
  trial('Region_VIA_LIST_unplanned_middle_position',region_middle)
 if admin_context:
  target=admin_context['change']['new']
  for value in [str(int(target)+1),'0','0'+target,'22','47' if target=='40' else '40']:
   trial('MAX_FILENAME_VALUE_unlicensed_'+value,lambda z,v=value:admin_property(z).set('Value',v))
  def drop_admin(z):
   d=objects(section(z,'Design'))[0];d.remove(d.find('o:attribute[@Name="MAX_FILENAME_VALUE"]',N))
  def duplicate_admin(z):
   d=objects(section(z,'Design'))[0];d.append(copy.deepcopy(d.find('o:attribute[@Name="MAX_FILENAME_VALUE"]',N)))
  def alter_admin_definition(z):
   d=next(e for e in z.iter() if NS['local'](e)=='xml-userPropertyDefinitions')
   attr=next(e for e in d.iter() if NS['local'](e)=='attribute' and e.get('Name')=='MAX_FILENAME_VALUE');attr.find('d:value/d:data',N).set('Storage','Integer')
  trial('MAX_FILENAME_VALUE_Design_property_removed',drop_admin)
  trial('MAX_FILENAME_VALUE_Design_property_duplicated',duplicate_admin)
  trial('MAX_FILENAME_VALUE_property_declaration_changed',alter_admin_definition)
 return out
def main():
 ap=argparse.ArgumentParser(description=__doc__)
 for key in ['source-cfx','source-tcfx','candidate-cfx','candidate-tcfx','source-pst','candidate-pst','plan','pst-proof','out']:ap.add_argument('--'+key,type=Path,required=True)
 ap.add_argument('--via-plan',type=Path);ap.add_argument('--admin-metadata-ledger',type=Path);ap.add_argument('--negative-controls',action='store_true');ar=ap.parse_args()
 need(not ar.out.exists(),'Fresh output required');ar.out.mkdir(parents=True);report={'status':'FAIL_CFX','CAD_started':False,'input_modified':False}
 try:
  report['source_binding']=source_binding(ar.source_cfx,ar.source_tcfx)
  a,b,fresh=pst_context(ar.source_pst,ar.candidate_pst,ar.plan,ar.pst_proof)
  base,actual=E.parse(ar.source_cfx).getroot(),E.parse(ar.candidate_cfx).getroot();definitions=named(section(base,'PartDefn'));rows=ref_rows(a,b,definitions)
  NS.update({'rp':a['parts'],'cp':b['parts'],'rpins':a['pinmap'],'cpins':b['pinmap'],'partset':set(a['parts']),'before_defs':definitions,'weights':Counter(r['new_partdefn'] for r in rows)})
  via=load(ar.via_plan) if ar.via_plan else None
  admin=admin_ledger_context(base,actual,ar.admin_metadata_ledger)
  proof,gates,defs=validate(base,actual,rows,via,admin);source_tcfx=E.parse(ar.source_tcfx).getroot();candidate_tcfx=E.parse(ar.candidate_tcfx).getroot();tcfx=canonical_tcfx(source_tcfx,candidate_tcfx,via,admin)
  report.update({'status':'PASS_COMPLETE_CFX_FP_AND_SIX_VIA_LIST_ONLY' if via else 'PASS_COMPLETE_CFX_FP_ONLY_VIA_RENAMES_NOT_APPLIED','proof':proof,'TCFX':tcfx,'physical_ref_identity_map':rows,'Gate_identity_bijection':gates,'PartDefn_physical_ref_expansion':defs,'fresh_complete_PST_inverse':{'status':fresh['status'],'parts':fresh['physical_parts'],'pins':fresh['physical_pins'],'partitions':fresh['connectivity_partitions']}})
  if admin:report['status']+='_WITH_EXACT_NATIVE_READONLY_ADMIN_METADATA'
  if ar.negative_controls:
   report['negative_controls']=controls(base,actual,rows,via,admin)
   report['TCFX_negative_controls']=tcfx_controls(source_tcfx,candidate_tcfx,via,admin)
 except Exception as ex:report['status']='FAIL_COMPLETE_CFX_BOUNDED_LIBRARY_ECO';report['error']=repr(ex)
 report['inputs']={k:({'path':str(v),'sha256':sha(v)} if v and v.is_file() else str(v)) for k,v in vars(ar).items() if isinstance(v,Path) and k!='out'}
 report['helper_sha256']={'frozen_CFX':sha(LEGACY),'frozen_PartDefn':sha(SUPPORT),'independent_PST':sha(R/'tools/verify_library13_pst.py'),'script':sha(__file__)}
 report['scope']='Complete CFX/TCFX rules, per-ref generated identities and exact six via-list names only. Optional administrative metadata ledger licenses only native-observed read-only String Design MAX_FILENAME_VALUE22->exact SHA-bound value (old canaries or exact final49B874 readonly63), with exact candidate-board probe binding; no numeric design/spacing/timing rules waived. Placement, pads, routing and actual copper continuity require their separate native physical ECO proof.'
 (ar.out/'PUBLIC_LIBRARY_CFX_REVIEW.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf8');print(json.dumps({'status':report['status'],'error':report.get('error'),'report':str(ar.out/'PUBLIC_LIBRARY_CFX_REVIEW.json')},ensure_ascii=False));return 0 if report['status'].startswith('PASS') else 2
if __name__=='__main__':raise SystemExit(main())
