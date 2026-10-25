from pathlib import Path
import json,ctypes,ctypes.wintypes as w,datetime,time,hashlib,argparse
R=Path(r'D:\001DIY\005lib\01AIEDA\learning\examples\lessonHI_38_50_20261021').resolve()
P=argparse.ArgumentParser();P.add_argument('--log',required=True);P.add_argument('--seconds',type=int,default=1800);a=P.parse_args();B=Path(a.log).resolve();assert B.is_relative_to(R)
L=json.loads((B/'launch.json').read_text());assert L['completed'] is False and L['exitCode'] is None
K=ctypes.WinDLL('kernel32',use_last_error=True)
K.OpenProcess.argtypes=[w.DWORD,w.BOOL,w.DWORD];K.OpenProcess.restype=w.HANDLE
K.GetProcessTimes.argtypes=[w.HANDLE,ctypes.POINTER(w.FILETIME),ctypes.POINTER(w.FILETIME),ctypes.POINTER(w.FILETIME),ctypes.POINTER(w.FILETIME)];K.GetProcessTimes.restype=w.BOOL
K.QueryFullProcessImageNameW.argtypes=[w.HANDLE,w.DWORD,w.LPWSTR,ctypes.POINTER(w.DWORD)];K.QueryFullProcessImageNameW.restype=w.BOOL
K.GetExitCodeProcess.argtypes=[w.HANDLE,ctypes.POINTER(w.DWORD)];K.GetExitCodeProcess.restype=w.BOOL
K.WaitForSingleObject.argtypes=[w.HANDLE,w.DWORD];K.WaitForSingleObject.restype=w.DWORD
K.CloseHandle.argtypes=[w.HANDLE];K.CloseHandle.restype=w.BOOL
h=K.OpenProcess(0x100000|0x1000,False,L['pid']);assert h,'Original process is no longer available; do not invent its exit code'
try:
 c,e,k,u=(w.FILETIME() for _ in range(4));assert K.GetProcessTimes(h,ctypes.byref(c),ctypes.byref(e),ctypes.byref(k),ctypes.byref(u))
 ticks=(c.dwHighDateTime<<32)+c.dwLowDateTime;created=datetime.datetime.fromtimestamp(ticks/10000000-11644473600,datetime.timezone.utc)
 original=datetime.datetime.fromisoformat(L['startUTC']);assert abs((created-original).total_seconds())<5
 buf=ctypes.create_unicode_buffer(32768);n=w.DWORD(len(buf));assert K.QueryFullProcessImageNameW(h,0,buf,ctypes.byref(n));assert Path(buf.value).resolve()==Path(L['args'][0]).resolve()
 board=Path(L['args'][-1]);sha=lambda:hashlib.sha256(board.read_bytes()).hexdigest().upper();assert sha()==L['beforeSHA256']
 base={'pid':L['pid'],'originalStartUTC':L['startUTC'],'verifiedProcessCreatedUTC':created.isoformat(),'verifiedExecutable':buf.value,'originalLaunchRecordUnmodified':True,'method':'OpenProcess(SYNCHRONIZE|QUERY_LIMITED_INFORMATION), validate live handle creation time and image, WaitForSingleObject, GetExitCodeProcess; actual handle retained across exit.','beforeSHA256':sha()}
 print(json.dumps(base),flush=True);start=time.monotonic();nextProgress=0
 while True:
  state=K.WaitForSingleObject(h,1000)
  if state==0:break
  assert state==258, f'Unexpected wait state{state}'
  if time.monotonic()-start>nextProgress:
   progress={**base,'observerUTC':datetime.datetime.now(datetime.timezone.utc).isoformat(),'active':True,'sourceSHA256':sha(),'secondsSinceOriginalStart':(datetime.datetime.now(datetime.timezone.utc)-original).total_seconds()}
   (B/'adopted_progress.json').write_text(json.dumps(progress,indent=2),encoding='utf8');nextProgress+=30
  if time.monotonic()-start>a.seconds:
   (B/'adopted_exit_observation.json').write_text(json.dumps({**base,'completed':False,'exitCode':None,'afterSHA256':sha(),'observerTimeout':True},indent=2));raise TimeoutError('Owned process remains active; no stop issued')
 code=w.DWORD();assert K.GetExitCodeProcess(h,ctypes.byref(code));record={**base,'completed':True,'exitCode':code.value,'afterSHA256':sha(),'observedExitUTC':datetime.datetime.now(datetime.timezone.utc).isoformat()}
 (B/'adopted_exit_observation.json').write_text(json.dumps(record,indent=2),encoding='utf8');print(json.dumps(record,indent=2),flush=True);assert code.value==0 and record['beforeSHA256']==record['afterSHA256']
finally:K.CloseHandle(h)
