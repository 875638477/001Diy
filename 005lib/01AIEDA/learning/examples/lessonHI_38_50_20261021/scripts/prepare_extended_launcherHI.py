from pathlib import Path
R=Path(r'D:\001DIY\005lib\01AIEDA\learning\examples\lessonHI_38_50_20261021')
s=(R/'scripts/launchHI.py').read_text().replace('timeout=120','timeout=600')
needle=" proc=subprocess.Popen(args,cwd=log,env=env,stdout=out,stderr=err,startupinfo=si,creationflags=subprocess.CREATE_NO_WINDOW)"
s=s.replace(needle,needle+"\n (log/'launch_in_progress.json').write_text(json.dumps({'startUTC':start,'pid':proc.pid,'args':args,'sourceSHA256':before,'timeoutSeconds':600},indent=2),encoding='utf8')\n print(json.dumps({'startUTC':start,'pid':proc.pid,'timeoutSeconds':600}),flush=True)")
s=s.replace("'completed':done,","'completed':done,'finishUTC':datetime.datetime.now(datetime.timezone.utc).isoformat(),'timeoutSeconds':600,")
s=s.replace("[-7000:]","[-1500:]")
(R/'scripts/launchHI_600.py').write_text(s,encoding='ascii')
s=(R/'scripts/prepare_readbackHI_v5.py').read_text()
s=s.replace("h+='skill errset(hiRouteRoles(\"'+out+'\") t)\\n'","h+='skill errset(hiRouteRoles(\"'+out+'\") t)\\n'\nh+='skill errset(hiUSBMaskRead(\"'+out+'\") t)\\n'")
(R/'scripts/prepare_readbackHI_v6.py').write_text(s,encoding='ascii')
print('600sec launcher and key actual mask exporter prepared')
