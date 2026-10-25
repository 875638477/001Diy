from pathlib import Path
R=Path(r'D:\001DIY\005lib\01AIEDA\learning\examples\lessonHI_38_50_20261021')
p=R/'scripts/batchHI_route_probe_v1.il';s=p.read_text();s=s.replace('    rr=gRouteNative(net list(previous p)', '''    when(index==1
     gSnapshot(hiDiagnosticOutput hiDiagnosticLibrary)
     hiRouteRoles(hiDiagnosticOutput)
     hiShapeBoundaryRead(hiDiagnosticOutput)
     fprintf(f "HI_BOOT_FAILED_STAGE_PROVISIONAL_GEOMETRY_DUMP_COMPLETE_NOT_CHECKPOINT\\n") drain(f))
    rr=gRouteNative(net list(previous p)''');p.write_text(s,encoding='ascii')
s=(R/'scripts/compile_batchHI_v23.py').read_text().replace("statements=['hiRegistry=nil','hiNodeDefinitions='+defs]", "statements=['hiRegistry=nil','hiNodeDefinitions='+defs,'hiDiagnosticOutput='+q(out.as_posix()),'hiDiagnosticLibrary='+q((R/'library').as_posix())]");(R/'scripts/compile_batchHI_v24.py').write_text(s,encoding='utf8')
p=R/'scripts/prepare_guarded_source_try06HI.py';s=p.read_text(encoding='utf-8-sig').replace('source_b015_{v}_try05','source_b015_{v}_try06').replace('source_b015_{v}_try06\';work.mkdir','source_b015_{v}_try07\';work.mkdir').replace('source_service_{v}_b015_guarded_try06','source_service_{v}_b015_guarded_try07').replace('compile_batchHI_v23.py','compile_batchHI_v24.py').replace("R/'scripts/launch_source_guardedHI_v5.py'", "R/'scripts/launch_source_guardedHI_v6.py'").replace("R/'scripts/launch_source_guardedHI_v6.py').write_text", "R/'scripts/launch_source_guardedHI_v7.py').write_text").replace(".replace(\"['', '_try02', '_try03', '_try04', '_try05']\",\"['', '_try02', '_try03', '_try04', '_try05', '_try06']\")", ".replace(\"['', '_try02', '_try03', '_try04', '_try05', '_try06']\",\"['', '_try02', '_try03', '_try04', '_try05', '_try06', '_try07']\")");(R/'scripts/prepare_guarded_source_try07HI.py').write_text(s,encoding='utf8')
