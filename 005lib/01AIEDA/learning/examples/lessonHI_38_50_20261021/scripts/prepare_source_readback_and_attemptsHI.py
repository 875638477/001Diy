from pathlib import Path
R=Path(r'D:\001DIY\005lib\01AIEDA\learning\examples\lessonHI_38_50_20261021')
s=(R/'scripts/prepare_stored_readbackHI_v3.py').read_text()
needle="for op in d.get('operations',[]):\n if op['type']=='via':il+="
insert="""if d.get('terminalContract'):
 contract='list('+' '.join('list('+Q(x['ref'])+' '+Q(x['pin'])+' '+(Q(x['net']) if x['net'] else 'nil')+' '+Q(x['padstack'])+')' for x in d['terminalContract'])+')'
 il+=' hiPhysicalTerminalContract(f '+contract+')\\n'
"""
assert needle in s;s=s.replace(needle,insert+needle);(R/'scripts/prepare_stored_readbackHI_v4.py').write_text(s,encoding='utf8')
# Save transparent ongoing attempt status without asserting a still-running DRC passed.
import json,hashlib
records=[]
for p in sorted((R/'logs').glob('*ripup*'))+sorted((R/'logs').glob('source_service_*_b015_guarded*')):
 x={'directory':str(p)}
 for name in ['launch.json','launch_in_progress.json']:
  if (p/name).exists():x[name]=json.loads((p/name).read_text())
 text=(p/'stdout.txt').read_text(errors='replace') if (p/'stdout.txt').exists() else ''
 x['reportedSkillError']='*Error*' in text;x['savedCandidateExists']=(R/'native_candidates/HI_2L_source_b015.brd').exists() if '2L' in p.name else (R/'native_candidates/HI_4L_source_b015.brd').exists()
 records.append(x)
d={'status':'IN_PROGRESS_NO_SOURCE_STAGE_DRC_PASS_ASSERTED','officialDeleteDocumentation':'C:/Program0/Cadence/SPB172/share/pcb/examples/skill/DOC/FUNCS/axlDeleteObject.txt','sourceProtection':'All originals are never opened by write batches; task-local readonly scratch memory edited, SaveAs only new candidate, current unchanged until all gates','observedFailures':['Sequential deletion PC15 remaining segment auto-relabeled GND; not skipped.','New combined cached-query scanner caused native 0xC0000005; fresh type-specific matching avoids it. Exact crash mechanism not proven.','BOOT full/reverse/single path creation refused on horizontal crossing old generated-GND fill. Dedicated defer-boundary construction sequence succeeds; final fill restored before final checks.','Launcher v2 first-line encoding failed before native launch; corrected and retained subsequent errors.'],'successfulRipupPilot':str(R/'logs/exact_batch_ripup_pilot_2L_05'),'attempts':records}
(R/'review/source_b015_native_execution_attempts.json').write_text(json.dumps(d,indent=2),encoding='utf8')
print('Stored fresh-readback generator v4 now also checks all272 pin identities; ongoing attempt records saved.')
