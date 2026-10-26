"""Bind all bounded finalFP changes to originalpublished12 for fullXML/PST inversion."""
from pathlib import Path
import copy,json,hashlib
M=Path(__file__).resolve().parent;O=M/'all81_published12_superset_plan13';O.mkdir(exist_ok=True)
jr=lambda p:json.loads(Path(p).read_text('utf-8-sig'));sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest().upper()
basepath=M/'sot34_superset_pst_and_pins_v1/CAPTURE13_PUBLISHED12_SUPERSET_PLAN.json';addpath=M/'capture_all81_plan13/compiled/CAPTURE13_FROZEN_PLAN.json';base=jr(basepath);add=jr(addpath);key=lambda x:(x['page'],x['id'])
assert len(base['pcb_footprint_changes'])==975 and len(add['pcb_footprint_changes'])==56
assert not {key(x) for x in base['pcb_footprint_changes']}&{key(x) for x in add['pcb_footprint_changes']}
p=copy.deepcopy(base);p['pcb_footprint_changes']+=copy.deepcopy(add['pcb_footprint_changes']);p['status']='FROZEN_PUBLISHED12_TO_ALL81_CAPTURE1031_FP_AND_PUBLIC_SOURCE_SUPERSET_REVIEW_ONLY';p['scope']='Original941FP +34SOT +56boundedall81FP fields. Original12source identities relink59Cache/3118instances retained. No other mutations.';p['superset_binding']={'base_plan':str(basepath),'base_plan_sha256':sha(basepath),'additional_plan':str(addpath),'additional_plan_sha256':sha(addpath),'candidate_native_output_directory':'D:/001DIY/004computer/lga1700/13shared_libraries_pc_20261025/w/all81_cn3','not_a_native_apply_plan':True};p['native_script']=None
out=O/'CAPTURE13_PUBLISHED12_ALL81_SUPERSET_PLAN.json';out.write_text(json.dumps(p,ensure_ascii=False,indent=2),encoding='utf-8');print(json.dumps({'path':str(out),'sha256':sha(out),'FP_fields':len(p['pcb_footprint_changes']),'FP_unique_refs':len({x['ref'] for x in p['pcb_footprint_changes']}),'sourceXML':p['source_design_xml'],'sourceXMLsha256':p['source_xml_sha256']},indent=2))
