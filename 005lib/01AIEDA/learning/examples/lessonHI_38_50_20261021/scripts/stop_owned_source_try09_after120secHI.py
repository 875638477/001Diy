from pathlib import Path
import json,hashlib,ctypes,ctypes.wintypes as w,datetime,subprocess,os,stat
R=Path(r'D:\001DIY\005lib\01AIEDA\learning\examples\lessonHI_38_50_20261021');B=R/'logs/source_service_2L_b015_guarded_try09_interactive';cfg=json.loads((R/'native_work/source_b015_2L_try09/guard_configuration.json').read_text());L=json.loads((B/'launch_in_progress.json').read_text());assert L['pid']==5476
assert 'HI_INTERMEDIATE_INTERACTIVE_DRC_REQUEST_RETURN' not in (B/'hi_batch_execution.txt').read_text() and not Path(cfg['candidateOutput']).exists()
sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest().upper();assert all(sha(x['path'])==x['sha256'] for x in cfg['protectedOriginals']);assert sha(cfg['scratchReadonlyInput'])==cfg['scratchSHA256']
K=ctypes.WinDLL('kernel32',use_last_error=True);K.OpenProcess.argtypes=[w.DWORD,w.BOOL,w.DWORD];K.OpenProcess.restype=w.HANDLE;K.GetProcessTimes.argtypes=[w.HANDLE,*([ctypes.POINTER(w.FILETIME)]*4)];K.GetProcessTimes.restype=w.BOOL;K.QueryFullProcessImageNameW.argtypes=[w.HANDLE,w.DWORD,w.LPWSTR,ctypes.POINTER(w.DWORD)];K.QueryFullProcessImageNameW.restype=w.BOOL;K.TerminateProcess.argtypes=[w.HANDLE,w.UINT];K.TerminateProcess.restype=w.BOOL;K.WaitForSingleObject.argtypes=[w.HANDLE,w.DWORD];K.WaitForSingleObject.restype=w.DWORD;K.GetExitCodeProcess.argtypes=[w.HANDLE,ctypes.POINTER(w.DWORD)];K.GetExitCodeProcess.restype=w.BOOL;K.CloseHandle.argtypes=[w.HANDLE]
def acquire(pid,exe):
 h=K.OpenProcess(0x1000|0x100000|1,False,pid);assert h
 c,e,k,u=(w.FILETIME() for _ in range(4));assert K.GetProcessTimes(h,ctypes.byref(c),ctypes.byref(e),ctypes.byref(k),ctypes.byref(u));ticks=lambda t:(t.dwHighDateTime<<32)+t.dwLowDateTime
 created=datetime.datetime.fromtimestamp(ticks(c)/1e7-11644473600,datetime.timezone.utc);buf=ctypes.create_unicode_buffer(32768);n=w.DWORD(len(buf));assert K.QueryFullProcessImageNameW(h,0,buf,ctypes.byref(n));assert Path(buf.value).resolve()==Path(exe).resolve();return h,{'pid':pid,'createdUTC':created.isoformat(),'image':buf.value,'cpuSeconds':(ticks(k)+ticks(u))/1e7},created
si=subprocess.STARTUPINFO();si.dwFlags|=subprocess.STARTF_USESHOWWINDOW;si.wShowWindow=0
p=subprocess.run(['powershell','-NoProfile','-Command','Get-CimInstance Win32_Process -Filter "ProcessId=19056" | Select-Object ProcessId,ParentProcessId,ExecutablePath,CommandLine | ConvertTo-Json -Compress'],cwd=B,env={**os.environ,'TEMP':str(B/'tmp'),'TMP':str(B/'tmp')},capture_output=True,text=True,check=True,startupinfo=si,creationflags=subprocess.CREATE_NO_WINDOW);child=json.loads(p.stdout);assert child['ParentProcessId']==L['pid'] and str(B/'tmp').replace('\\','/') in child['CommandLine'].replace('\\','/')
ph,pm,pc=acquire(L['pid'],L['args'][0]);ch,cm,cc=acquire(19056,child['ExecutablePath'])
try:
 assert abs((pc-datetime.datetime.fromisoformat(L['startUTC'])).total_seconds())<5
 elapsed=(datetime.datetime.now(datetime.timezone.utc)-cc).total_seconds();assert elapsed>=120, f'Root authorized stop only after120sec; current={elapsed}'
 inp=B/'tmp/#Taaaafb05476.in';assert sha(inp)==sha(R/'logs/source_service_2L_b015_guarded_try08/tmp/#Taaaacu16604.in');out=B/'tmp/#Taaaafb05476.OUT';assert 'NoGroundPlane' in inp.read_text() and out.stat().st_size==0
 rec={'status':'ROOT_AUTHORIZED_INTENTIONAL_STOP_OF_OWN_UNSAVED_BATCH_T_CALC_NOT_A_PASS','reason':'After>=120sec repeated identical input owned active bem2d NoGroundPlane output remains0. Intermediate scope will use explicit saved DRC_PENDING source with all modes unchanged; nil also repeated identical field-solver block; final batch-t remains mandatory/pending.','parent':pm,'ownedChild':cm,'childParentCIM':child,'elapsedChildSeconds':elapsed,'input':str(inp),'inputSHA256':sha(inp),'outputBytesBefore':out.stat().st_size,'protectedOriginals':cfg['protectedOriginals'],'scratchSHA256':sha(cfg['scratchReadonlyInput']),'candidateNeverSaved':True}
 (B/'owned_termination_evidence.json').write_text(json.dumps(rec,indent=2),encoding='utf8')
 assert K.TerminateProcess(ph,0xFFFFFFFF);assert K.WaitForSingleObject(ph,10000)==0
 # Parent is stopped before solver to prevent a partial result ever being saved as a candidate.
 if K.WaitForSingleObject(ch,0)==258:assert K.TerminateProcess(ch,0xFFFFFFFF)
 assert K.WaitForSingleObject(ch,10000)==0
 for h,key in [(ph,'actualParentExitCode'),(ch,'actualOwnedChildExitCode')]:
  code=w.DWORD();assert K.GetExitCodeProcess(h,ctypes.byref(code));rec[key]=code.value
 rec['protectedAfter']=[{**x,'actualSHA256':sha(x['path'])} for x in cfg['protectedOriginals']];assert all(x['actualSHA256']==x['sha256'] for x in rec['protectedAfter']);rec['sourceSHAAfter']=sha(cfg['scratchReadonlyInput']);assert rec['sourceSHAAfter']==cfg['scratchSHA256'];rec['candidateExistsAfter']=Path(cfg['candidateOutput']).exists();assert not rec['candidateExistsAfter'];rec['stoppedUTC']=datetime.datetime.now(datetime.timezone.utc).isoformat();(B/'owned_termination_evidence.json').write_text(json.dumps(rec,indent=2),encoding='utf8');print(json.dumps({'status':rec['status'],'elapsed':elapsed,'parentExit':rec['actualParentExitCode'],'childExit':rec['actualOwnedChildExitCode'],'sourcesStable':True,'noCandidate':True}))
finally:K.CloseHandle(ph);K.CloseHandle(ch)
