"""Prepare public-only native SOT34 canary/Alt/readback files; never run CAD."""
from pathlib import Path
import csv,hashlib,json,re
R=Path(r'D:\001DIY\004computer\lga1700\13shared_libraries_pc_20261025')
W=R/'w/pcb_migration';D=W/'sot34_migration'
M=Path(r'D:\001DIY\005lib\01AIEDA\library_maintenance\20261025_pc_shared')
E=M/'sot34_superset_pst_and_pins_v1'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest().upper()
def sk(p):return json.dumps(str(p).replace('\\','/'))
assert not D.exists();D.mkdir()
source=R/'w/via_alt13/PC13_FINAL.brd'
assert sha(source)=='49AF5EE7252CA9E8C4C48D8F60AD4D1113DA559814585356B14F6150A195C063'
with (R/'w/final_alt13/symbols.tsv').open(newline='') as f:symbols=list(csv.DictReader(f,delimiter='\t'))
symbols=[s for s in symbols if s['definition']=='SOT23_123'];assert len(symbols)==34 and all(s['mirrored']=='nil' and s['pin_count']=='3' for s in symbols)
refs={s['refdes'] for s in symbols};changes=json.loads((E/'SOT34_102_EXPECTED_CHANGES.json').read_text());assert len(changes)==102 and {x['ref'] for x in changes}==refs
canary=[];rot=set()
for s in symbols:
 if s['rotation'] not in rot:canary.append(s['refdes']);rot.add(s['rotation'])
assert len(canary)==4 and rot=={'0.0','90.0','180.0','270.0'}
base=(W/'EXPECTED_PINS_V3.ilist').read_text().splitlines();target=(E/'EXPECTED_PINS_SOT34.ilist').read_text().splitlines()
key=lambda s:re.match(r'^\("([^"]+)"\s',s)[1]
b={key(x):x for x in base};t={key(x):x for x in target};assert len(b)==len(t)==1066 and b.keys()==t.keys();assert {k for k in b if b[k]!=t[k]}==refs
(D/'EXPECTED_PINS_SOT34.ilist').write_text('\n'.join(target)+'\n',encoding='utf-8')
(D/'EXPECTED_PINS_CANARY4.ilist').write_text('\n'.join(t[key(x)] if key(x) in canary else x for x in base)+'\n',encoding='utf-8')
header='refdes\tfrom_package\ttarget_package\tdelta\n'
natural=lambda s:[int(x) if x.isdigit() else x for x in re.split(r'(\d+)',s)]
full_rows=[f'{r}\tSOT23_123\tsot23-3\t0' for r in sorted(refs,key=natural)]
mini_rows=[f'{r}\tSOT23_123\tsot23-3\t0' for r in canary]
(D/'SOT34_REPLACEMENTS.tsv').write_text(header+'\n'.join(full_rows)+'\n',encoding='utf-8')
(D/'CANARY4_REPLACEMENTS.tsv').write_text(header+'\n'.join(mini_rows)+'\n',encoding='utf-8')
old=(W/'ALL_REF_REPLACEMENTS.tsv').read_text().splitlines();assert old[0]+'\n'==header and len(old)==911 and not refs & {x.split('\t')[0] for x in old[1:]}
(D/'ALL_APPROVED_944.tsv').write_text('\n'.join(old+full_rows)+'\n',encoding='utf-8')
(D/'EMPTY_APPROVED.tsv').write_text(header,encoding='utf-8')

s='''; Only root owns/launches Cadence. Every input and output is an isolated copy.
load('''+sk(W/'pc13_native_replace_v6.il')+''')
load("D:/001DIY/004computer/lga1700/12electrical_fixed_20261025/tools/rules_eco/composite_readonly.il")
load('''+sk(W/'pc13_export_owned_geometry.il')+''')
load('''+sk(W/'pc13_export_board_definitions.il')+''')
procedure(pc13SotSourceGuard()
 let((count)
  sstatus(fullPrecision t)
  unless(length(axlDBGetDesign()->components)==1066 error("SOT34 source1066 component count failed\\n"))
  pc13LoadExpected('''+sk(W/'EXPECTED_PINS_V3.ilist')+''') count=0
  foreach(c axlDBGetDesign()->components
   pc13ExpectedPins(c->name c->symbol) count=count+length(c->symbol->pins))
  unless(count==6521 error("SOT34 source6521 pin count failed\\n")) t))
procedure(pc13Sot34Canary(dir)
 pc13SotSourceGuard()
 pc13Replace('''+sk(D/'CANARY4_REPLACEMENTS.tsv')+''' dir strcat(dir "/SOT34_CANARY4.brd") "D:/001DIY/005lib/01Psm_lib" "D:/001DIY/005lib/01Pad_lib" 0 '''+sk(D/'EXPECTED_PINS_CANARY4.ilist')+'''))
procedure(pc13Sot34Apply(dir)
 pc13SotSourceGuard()
 pc13Replace('''+sk(D/'SOT34_REPLACEMENTS.tsv')+''' dir strcat(dir "/SOT34_ALT.brd") "D:/001DIY/005lib/01Psm_lib" "D:/001DIY/005lib/01Pad_lib" 0 '''+sk(D/'EXPECTED_PINS_SOT34.ilist')+'''))
procedure(pc13SotFullExports(dir)
 sstatus(fullPrecision t)
 eco12CompositeRead(dir)
 pc13ExportOwnedGeometry(strcat(dir "/owned_geometry.tsv"))
 pc13ExportBoardDefinitions(dir)
 t)
procedure(pc13SotCanaryFresh(snapshotPath dir)
 let((rows c f)
  pc13Readback(snapshotPath '''+sk(D/'EMPTY_APPROVED.tsv')+''' dir '''+sk(D/'EXPECTED_PINS_CANARY4.ilist')+''')
  rows=pc13ReadRows('''+sk(D/'CANARY4_REPLACEMENTS.tsv')+''')
  foreach(row rows
   c=pc13Comp(car(row))
   unless(equal(upperCase(c->package) "SOT23_123") && equal(upperCase(c->symbol->name) "SOT23-3") && equal(upperCase(c->symbol->definition->name) "SOT23-3") error("SOT34 canary pre-netrev package/symbol guard failed\\n")))
  pc13SotFullExports(dir)
  f=outfile(strcat(dir "/SOT34_CANARY_FRESH_COMPLETE.txt")) fprintf(f "ALL6521_PIN_LEDGER_AND1066_TEXT_COMPLETE\\nCANARY4_SYMBOLS_PRE_NETREV_COMPLETE\\n") close(f) t))
procedure(pc13Sot34Fresh(snapshotPath dir)
 let((f)
  pc13Readback(snapshotPath '''+sk(D/'ALL_APPROVED_944.tsv')+''' dir '''+sk(D/'EXPECTED_PINS_SOT34.ilist')+''')
  pc13SotFullExports(dir)
  f=outfile(strcat(dir "/SOT34_FINAL_FRESH_COMPLETE.txt")) fprintf(f "ALL6521_PIN_LEDGER_AND1066_TEXT_COMPLETE\\nALL944_PACKAGE_SYMBOL_DEFINITION_COMPLETE\\n") close(f) t))
procedure(pc13SotRestoreAfterNetrev(snapshotPath dir)
 pc13RestoreAfterNetrev(snapshotPath dir strcat(dir "/SOT34_RESTORED.brd")))
'''
# Avoid accidental string escapes in SKILL diagnostic newlines; no BOM.
depth=0;string=False;escape=False
for line in s.splitlines():
 for c in line:
  if string:
   if escape:escape=False
   elif c=='\\':escape=True
   elif c=='"':string=False
  elif c==';':break
  elif c=='"':string=True
  elif c=='(':depth+=1
  elif c==')':depth-=1;assert depth>=0,line
assert depth==0 and not string,(depth,string)
(D/'sot34_native_migration.il').write_text(s,encoding='utf-8')
receipt=dict(status='PREPARED_NOT_RUN',source_board=str(source),source_sha256=sha(source),native_readback_source=str(R/'w/final_alt13'),refs34=sorted(refs,key=natural),canary4=canary,canary_rotation={s['refdes']:s['rotation'] for s in symbols if s['refdes'] in canary},source_full_pins=6521,source_instances=1066,changed_pin_count=102,source_expected=str(W/'EXPECTED_PINS_V3.ilist'),source_expected_sha256=sha(W/'EXPECTED_PINS_V3.ilist'),target_expected_source=str(E/'EXPECTED_PINS_SOT34.ilist'),target_expected_source_sha256=sha(E/'EXPECTED_PINS_SOT34.ilist'),native_runner=str(R/'tools/pcb_eco/Invoke-NativeLocal.ps1'),netrev_runner=str(R/'tools/pcb_eco/Invoke-LiveNetrev.ps1'),netrev_after_alt_only='-e -d -y2; never full34 PST import into the4-only canary',files={str(p):sha(p) for p in D.iterdir() if p.is_file()})
(D/'SOT34_NATIVE_PREPARATION.json').write_text(json.dumps(receipt,indent=2),encoding='utf-8')
print(json.dumps(dict(directory=str(D),canary4=canary,native_helper_sha256=sha(D/'sot34_native_migration.il'),receipt_sha256=sha(D/'SOT34_NATIVE_PREPARATION.json')),indent=2))
