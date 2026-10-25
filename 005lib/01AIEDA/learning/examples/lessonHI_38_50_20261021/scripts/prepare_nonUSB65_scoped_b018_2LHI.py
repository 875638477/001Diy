锘縡rom pathlib import Path
import json,hashlib,shutil
R=Path(r'D:\001DIY\005lib\01AIEDA\learning\examples\lessonHI_38_50_20261021');Q=json.dumps;v='2L';tag=f'nonUSB65_scoped_TOP_trial_{v}_b018_01';plan=json.loads((R/f'batches/TOP_trial_{v}_b018_PRE_NON_USB_65_DRC_PENDING_try06.json').read_text());m=json.loads((R/f'scripts/TOP_trial_{v}_b018_PRE_NON_USB_65_DRC_PENDING_try06_compiled.json').read_text());names=[n for n in plan['all69ScopedDeferredToIndependentReadonlyProcess'] if n not in ['USB_DP','USB_DM','PA11_SHARED','PA12_SHARED']];assert len(names)==len(set(names))==65
out=R/'logs'/tag;pp=R/'scripts'/f'{tag}.il';code='''procedure(hiAll69ReadonlyScoped()
 let((f net count failures)
  f=outfile(OUTFILE) failures=0
  unless(axlDBControl('drcEnable) error("Existing master DRC disabled; stop no mode change\\n"))
  fprintf(f "NON_USB_65_SCOPE=AXL_DRC_ITEM_PER_REAL_NET_NOT_WHOLE_BOARD_UPDATE_NOT_BATCH_ONLY\\nDESIGN=%L\\nPHYSICAL=%L\\nSPACING=%L\\nELECTRICAL=%L\\n" axlCNSDesignModeGet('all) axlCNSPhysicalModeGet('all) axlCNSSpacingModeGet('all) axlCNSEcsetModeGet('all)) drain(f)
  foreach(name NAMES
   net=axlDBFindByName('net name) unless(net error("Actual net missing\\n"))
   fprintf(f "NON_USB_65_NET_BEGIN name=%L time=%L\\n" name getCurrentTime()) drain(f)
   count=axlDRCItem(nil net)
   fprintf(f "NON_USB_65_NET_RESULT name=%L result=%L time=%L\\n" name count getCurrentTime()) drain(f)
   unless(numberp(count) error("Native scoped result not numeric; do not treat as zero\\n"))
   when(count!=0 failures=failures+1 f29DumpDRC(f strcat("NON_USB_65_NONZERO_" name))))
  fprintf(f "NON_USB_65_NET_SCOPED_COMPLETE netCount=65 nonzeroNets=%d masterDRC=%L WHOLE_BOARD_DRC_UNRECOMPUTED=t USB4_NOT_EXECUTED_KNOWN_SOLVER_BLOCK=t\\n" failures axlDBControl('drcEnable)) close(f) t))
'''.replace('OUTFILE',Q((out/'all69_per_net_scoped.txt').as_posix())).replace('NAMES','list('+' '.join(Q(n) for n in names)+')');pp.write_text(code,encoding='ascii');snap=R/'source/readback_snapshots'/tag;snap.mkdir(exist_ok=False);loads=[Path(x['snapshot']) for x in m['helperSnapshots'][:-1]]+[pp];h='set NOCONFIRM\n';records=[]
for i,p in enumerate(loads):
 dst=snap/f'{i:02d}_{p.name}';shutil.copyfile(p,dst);h+='skill errset(load('+Q(dst.as_posix())+') t)\n';records.append({'source':str(p),'snapshot':str(dst),'sha256':hashlib.sha256(dst.read_bytes()).hexdigest().upper()})
h+='skill errset(hiAll69ReadonlyScoped() t)\nskill errset(axlKillDesign() t)\nquit\n';(R/'scripts'/f'{tag}.scr').write_text(h,encoding='ascii');(snap/'manifest.json').write_text(json.dumps(records,indent=2));print(tag)
