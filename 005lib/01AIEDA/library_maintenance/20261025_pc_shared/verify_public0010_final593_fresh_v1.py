"""Independent final593 typed source inverse using the actual source-no-op control."""
from pathlib import Path
import argparse,copy,hashlib,importlib.util,json
M=Path(__file__).parent;sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest().upper();jr=lambda p:json.loads(Path(p).read_text('utf-8-sig'))
s=importlib.util.spec_from_file_location('full593_typed_snapshot',M/'review_public0010_restored593_native.py');F=importlib.util.module_from_spec(s);s.loader.exec_module(F)
def main():
 ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--native-job',type=Path,required=True);ap.add_argument('--candidate-sha256',required=True);ap.add_argument('--out',type=Path,required=True);a=ap.parse_args();F.need(not a.out.exists(),'Fresh proof directory required')
 q=jr(a.native_job/'launch_report.json');h=a.candidate_sha256.upper();F.need(q['source_sha256_before']==q['source_sha256_after']==q['staged_sha256']==h and q['input_unchanged'] and not q['write_candidate'] and q['exit_code']==0 and '-readonly' in q['arguments'],'Final native candidate protected readonly binding failed');F.need(sha(a.native_job/'INPUT_COPY.brd')==h,'Final staged board bytes differ')
 marker=a.native_job/'FINAL_FULL2698_593_READONLY_COMPLETE.txt';F.need(marker.read_text('utf-8').startswith('FINAL_FRESH_ALL2698_TYPED_PINS_ALL593_POSE_OWNED_TEXT_SYMBOL_COMPONENT_COMPDEF_PROPERTIES_AND_USED_FONTS_EXACT_SOURCE_ONLY403_DEFINITION_NAMES'),'Final complete593/2698 native marker missing')
 control=M/'public0010_source_noop_save13';source=control/'CONTROL_BEFORE_ALL593_TEXT_PROPS.ilist';after=control/'CONTROL_AFTER_ALL593_TEXT_PROPS.ilist';F.need(source.read_bytes()==after.read_bytes(),'Original source no-op control had nonzero text/props changes')
 cr=jr(control/'RUN_RECEIPT.json');F.need(cr['status']=='PASS_NATIVE_CASE_PHASE_ONLY' and cr['source_sha256_before']==cr['source_sha256_after']=='680500B07BC97F2B9D47064F83A01D0376AE43ADD486171F9B46087109E1B898','Original control source not frozen')
 plan=M/'public_four_module_fp_plans13_v4/0010_EXACT_FOOTPRINT_PLAN.json';mapping={r['ref']:r for r in jr(plan)['changes']};target=a.native_job/'FINAL_FRESH_ALL593_TEXT_PROPS.ilist';x,y=F.read(source),F.read(target);review=F.review(x,y,mapping)
 controls=[]
 def reject(name,fn):
  z=copy.deepcopy(y);fn(z)
  try:F.review(x,z,mapping)
  except (ValueError,KeyError):controls.append(dict(name=name,status='PASS_REJECTED'))
  else:raise ValueError('Final full593 negative control accepted '+name)
 sym=lambda z:next(r for r in z if r[0]=='symbol' and r[1][0]=='LOGICAL' and r[2])
 reject('changed_original_text',lambda z:sym(z)[2][0].__setitem__(0,'UNAPPROVED'))
 reject('extra_autosilk_number',lambda z:sym(z)[2].append(copy.deepcopy(sym(z)[2][0])))
 reject('nonlogical_object_removed',lambda z:z.remove(next(r for r in z if r[0]=='symbol' and r[1][0]=='NONLOGICAL')))
 reject('component_property_changed',lambda z:next(r for r in z if r[0]=='component').__setitem__(3,[[F.Atom('VALUE'),'WRONG']]))
 report=dict(status='PASS_FINAL_FRESH_FULL593_SOURCE_ONLY403_DEFINITION_NAMES',source_board_sha256=cr['source_sha256_before'],candidate_board_sha256=h,all_source_noop_control_text_props_bytes_exact=True,autosilk_additions_allowed=0,review=review,negative_controls=controls,inputs={str(p):sha(p) for p in [a.native_job/'launch_report.json',marker,source,after,control/'RUN_RECEIPT.json',target,plan]},not_connection_copper_CFX_or_library_cache_approval=True)
 a.out.mkdir();p=a.out/'FINAL_FULL593_SOURCE_FRESH_REVIEW.json';p.write_text(json.dumps(report,indent=2),'utf-8');print(json.dumps(dict(status=report['status'],report=str(p),sha256=sha(p)),indent=2))
if __name__=='__main__':main()
