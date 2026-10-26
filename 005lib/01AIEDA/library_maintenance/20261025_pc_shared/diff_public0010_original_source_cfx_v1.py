"""Strict original680500 CFX diff after actual four-view FP/function inverse.

Observation only: no metadata, date, origin or rule difference is waived.
"""
from pathlib import Path
import argparse,hashlib,importlib.util,json,sys,xml.etree.ElementTree as E
M=Path(__file__).parent;R=Path(r'D:\001DIY\004computer\lga1700\13shared_libraries_pc_20261025')
sys.path.insert(0,str(M));from diff_public0010_post_attachment_cfx_v1 import diff
sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest().upper()
def module(p,name):
 s=importlib.util.spec_from_file_location(name,p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
def main():
 ap=argparse.ArgumentParser(description=__doc__)
 for n in ['candidate-native','view-proof','out']:ap.add_argument('--'+n,type=Path,required=True)
 a=ap.parse_args();assert not a.out.exists();C=module(R/'tools/verify_public_module_cfx_v4.py','complete_original_module_cfx');source=M/'w/public_brd0010_source_full13_v2'
 modelpath=R/'verification/public_brd_device_model13_0010_v2/DEVICE_VIEW_EXACT_MODEL.json';planpath=M/'public_four_module_fp_plans13_v4/0010_EXACT_FOOTPRINT_PLAN.json'
 model=C.load(modelpath);plan=C.load(planpath);proof=C.load(a.view_proof);assert proof['status']=='PASS_COMPLETE_PUBLIC_MODULE_VIEWS_ONLY_PLANNED_FP_AND_FUNCTION_IDS' and proof['inputs'][str(planpath)]==sha(planpath)
 targetsha=C.load(a.candidate_native/'launch_report.json')['source_sha256_before'];C.F.bind(source,model['native_source_sha256'],'PUBLIC_BOARD_COMPLETE.txt');C.F.bind(a.candidate_native,targetsha,'PUBLIC_BOARD_COMPLETE.txt');assert [v for p,v in proof['inputs'].items() if p.lower().endswith('.brd')]==[targetsha]
 reports={};inputs=[modelpath,planpath,a.view_proof]
 for ext in ['dcfx','tcfx']:
  sp=source/('ACTUAL_SUPPLEMENT.'+ext);tp=a.candidate_native/('ACTUAL_SUPPLEMENT.'+ext);inputs += [sp,tp]
  x=E.parse(sp).getroot();y=C.F.cfx_inverse(tp,proof['function_renumber_ledger']) if ext=='dcfx' else E.parse(tp).getroot()
  parts=C.inverse_partdefn(x,y,model,plan) if ext=='dcfx' else []
  whole=C.inverse_bound_independent_collections(x,y,model,proof)
  reports[ext]=dict(differences=diff(x,y),exact_device_bound_PartDefn_inverse=parts,source_function_bound_independent_object_order=whole)
 report=dict(status='STRICT_ORIGINAL_SOURCE_CFX_DIAGNOSTIC_NO_DIFFERENCES_WAIVED',source_board_sha256=model['native_source_sha256'],candidate_board_sha256=targetsha,extensions=reports,inputs={str(p):sha(p) for p in inputs})
 a.out.mkdir();p=a.out/'ORIGINAL_SOURCE_CFX_EXACT_DIAGNOSTIC.json';p.write_text(json.dumps(report,indent=2),'utf-8');print(json.dumps(dict(report=str(p),sha256=sha(p),differences={k:v['differences'] for k,v in reports.items()}),indent=2))
if __name__=='__main__':main()
