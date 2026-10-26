"""Case checker copy: admit only exact independently proved Cache7 status, never weaken PST review."""
from pathlib import Path
import hashlib
M=Path(__file__).resolve().parent;R=Path(r'D:\001DIY\004computer\lga1700\13shared_libraries_pc_20261025');O=M/'capture_cache7_plan13/v2'
old=R/'tools/verify_library13_pst.py';text=old.read_text('utf-8');assert text.count('R=Path(__file__).resolve().parents[1]')==1;text=text.replace('R=Path(__file__).resolve().parents[1]',"R=Path(r'D:\\001DIY\\004computer\\lga1700\\13shared_libraries_pc_20261025')")
needle="need(proof['status']=='PASS_PUBLIC_LIBRARY_AND_FP_ONLY_FULL_ORDERED_XML' and proof['inputs']['plan_sha256']==P.sha(ar.plan),'XML proof not bound to exact frozen plan')"
assert text.count(needle)==1
replacement="""need(proof['status']=='PASS_PUBLIC_LIBRARY_FP_AND_EXACT_SEVEN_CACHE_DEFAULTS_FULL_ORDERED_XML' and proof['inputs']['plan_sha256']==P.sha(ar.plan),'Exact Cache7 XML proof not bound to frozen plan')
  need(len(plan['cache_default_pcb_footprint_changes'])==7 and proof['cache_default_pcb_footprint_changes']==plan['cache_default_pcb_footprint_changes'],'ExactsevenCacheDefault rows differ from independent proof')
  need(proof['inputs']['script_sha256']==P.sha(R/'tools/verify_library13_cache_defaults_xml.py') and proof['original_checker_sha256']==P.sha(R/'tools/verify_library13_xml.py'),'Cache7 proof checker bindings changed')"""
text=text.replace(needle,replacement);target=O/'verify_library13_cache7_pst.py';target.write_text(text,encoding='utf-8');print(str(target));print(hashlib.sha256(target.read_bytes()).hexdigest().upper())
