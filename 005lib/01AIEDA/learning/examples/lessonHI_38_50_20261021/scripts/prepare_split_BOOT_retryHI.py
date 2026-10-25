from pathlib import Path
R=Path(r'D:\001DIY\005lib\01AIEDA\learning\examples\lessonHI_38_50_20261021')
p=R/'scripts/batchHI_route_probe_v1.il';s=p.read_text();s=s.replace('let((ret actualPoints actualWidths)','let((ret actualPoints actualWidths paths rr previous index)');s=s.replace('  ret=gRouteNative(net actualPoints actualWidths strcat("ETCH/" layer) f id)','''  if(equal(id "RIGHT_BOOT_DIRECT_TOP") then
   paths=nil previous=car(actualPoints) index=0
   fprintf(f "HI_BOOT_PHYSICAL_NATIVE_NET_NAMES MCU=%L R28=%L targetLogicalNet=%L\\n" gPin("U1" "44")->net->name gPin("R28" "1")->net->name axlDBFindByName('net net)) drain(f)
   foreach(p cdr(actualPoints)
    fprintf(f "HI_BOOT_SINGLE_SEGMENT index=%d start=%L end=%L width=%L\\n" index previous p nth(index actualWidths)) drain(f)
    rr=gRouteNative(net list(previous p) list(nth(index actualWidths)) strcat("ETCH/" layer) f sprintf(nil "%s_SEGMENT_%d" id index))
    paths=append(paths car(rr)) previous=p index=index+1)
   ret=list(paths nil)
  else ret=gRouteNative(net actualPoints actualWidths strcat("ETCH/" layer) f id))''');p.write_text(s,encoding='ascii')
p=R/'scripts/prepare_guarded_source_try05HI.py';s=p.read_text(encoding='utf-8-sig');s=s.replace('source_b015_{v}_try04','source_b015_{v}_try05').replace('source_b015_{v}_try05\';work.mkdir','source_b015_{v}_try06\';work.mkdir').replace('source_service_{v}_b015_guarded_try05','source_service_{v}_b015_guarded_try06').replace("['', '_try02', '_try03', '_try04', '_try05']", "['', '_try02', '_try03', '_try04', '_try05', '_try06']").replace("R/'scripts/launch_source_guardedHI_v4.py'", "R/'scripts/launch_source_guardedHI_v5.py'").replace("R/'scripts/launch_source_guardedHI_v5.py').write_text", "R/'scripts/launch_source_guardedHI_v6.py').write_text")
# The launcher allowed-list replacement must match the previous fifth-version list.
s=s.replace('.replace("[\'\', \'_try02\', \'_try03\', \'_try04\']","[\'\', \'_try02\', \'_try03\', \'_try04\', \'_try05\', \'_try06\']")','.replace("[\'\', \'_try02\', \'_try03\', \'_try04\', \'_try05\']","[\'\', \'_try02\', \'_try03\', \'_try04\', \'_try05\', \'_try06\']")')
(R/'scripts/prepare_guarded_source_try06HI.py').write_text(s,encoding='utf8')
