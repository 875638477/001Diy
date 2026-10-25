from pathlib import Path
import json,hashlib,datetime
R=Path(r'D:\001DIY\005lib\01AIEDA\learning\examples\lessonHI_38_50_20261021')
s=(R/'scripts/launchHI_600.py').read_text().replace('import argparse,pathlib,subprocess,os,json,datetime,hashlib','import argparse,pathlib,subprocess,os,json,datetime,hashlib,shutil')
needle="env.update(TEMP=str(log/'tmp'),TMP=str(log/'tmp'),ALLEGRO_PCBENV=str(log/'pcbenv'))"
s=s.replace(needle,needle+"""
cadence_bin=r'C:\\Program0\\Cadence\\SPB172\\tools\\bin'
original_path=env.get('PATH','')
bem2d_before=shutil.which('bem2d',path=original_path)
env['PATH']=cadence_bin+os.pathsep+original_path
bem2d_after=shutil.which('bem2d',path=env['PATH'])
(log/'child_environment_resolution.json').write_text(json.dumps({'scope':'Child process environment only; no system/user PATH changed','bem2dBefore':bem2d_before,'bem2dAfter':bem2d_after,'prepended':cadence_bin,'originalPATH':original_path,'childPATH':env['PATH']},indent=2),encoding='utf8')
assert bem2d_after and pathlib.Path(bem2d_after).resolve().is_relative_to(pathlib.Path(cadence_bin).resolve())
""")
s=s.replace("'timeoutSeconds':600,","'timeoutSeconds':600,'bem2dBefore':bem2d_before,'bem2dAfter':bem2d_after,")
(R/'scripts/launchHI_600_path.py').write_text(s,encoding='ascii')
B=R/'logs/usb_esd_4L_b008'
old=json.loads((B/'launch.json').read_text());source=Path(old['args'][-1])
board=R/'native/HI_4L_usb_esd_4L_b008.brd'
e={'status':'NATIVE_COMPLETION_OBSERVED_AFTER_INITIAL_LAUNCHER_TIMEOUT','observedUTC':datetime.datetime.now(datetime.timezone.utc).isoformat(),'initialRecord':'launch.json','initialPID':old['pid'],'processGoneConfirmedByGetProcess':True,'processExitCode':None,'exitCodeScope':'The original Python launcher ceased waiting at120s. No handle remained to recover final process exit status; no zero exit code is invented. Separate new-process readback is required.','sourceSHAUnchanged':hashlib.sha256(source.read_bytes()).hexdigest().upper()==old['beforeSHA256'],'candidateBoard':str(board),'candidateSHA256':hashlib.sha256(board.read_bytes()).hexdigest().upper(),'nativeStatus':'DRC0_AND_FULL_NATIVE_BATCH_SNAPSHOT_NETWORK_MARKERS_PRESENT','originalLaunchSHA':hashlib.sha256((B/'launch.json').read_bytes()).hexdigest().upper()}
(B/'extended_completion_observed.json').write_text(json.dumps(e,indent=2),encoding='utf8')
print(json.dumps(e,indent=2))
