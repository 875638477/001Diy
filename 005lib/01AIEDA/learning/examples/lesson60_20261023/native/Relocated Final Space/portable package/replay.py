"""Self-contained Windows/Cadence17.2 training replay. Python stdlib only."""
from pathlib import Path
import argparse, datetime, hashlib, json, os, re, shutil, subprocess, sys, traceback
ROOT=Path(__file__).resolve().parent
FIXTURE=ROOT/'fixture/training_4L.brd'
EXPECTED='471176A9B25BA8DEF9F117AEFB1E9220CBCBEBBAC5191BCBC6E228F52831F3F9'
def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest().upper()
def now(): return datetime.datetime.now(datetime.timezone.utc).isoformat()
def dump(p, value): p.write_text(json.dumps(value,indent=2,ensure_ascii=True),encoding='utf8')
def ps(code,timeout=45):
    si=subprocess.STARTUPINFO(); si.dwFlags|=subprocess.STARTF_USESHOWWINDOW; si.wShowWindow=0
    p=subprocess.run(['powershell','-NoProfile','-NonInteractive','-Command',code],capture_output=True,text=True,timeout=timeout,startupinfo=si,creationflags=subprocess.CREATE_NO_WINDOW)
    if p.returncode: raise RuntimeError('PowerShell identity query failed: '+p.stderr[-1000:])
    return json.loads(p.stdout) if p.stdout.strip() else None

def processes(pid=None):
    filt=('ProcessId='+str(int(pid))) if pid else "Name='allegro.exe'"
    data=ps("@(Get-CimInstance Win32_Process -Filter \""+filt+"\" | ForEach-Object { [PSCustomObject]@{pid=$_.ProcessId;parent=$_.ParentProcessId;exe=$_.ExecutablePath;created=$_.CreationDate.ToUniversalTime().ToString('o');command=$_.CommandLine} }) | ConvertTo-Json -Compress")
    return [] if data is None else ([data] if isinstance(data,dict) else data)

def config(path):
    c=json.loads(path.read_text(encoding='utf-8-sig'))
    c['exe']=str((Path(c['cadence_root'])/'tools/bin/allegro.exe').resolve())
    assert re.fullmatch(r'[A-Za-z0-9_]+',c['product']), 'Invalid product string'
    assert 30<=int(c['timeout_seconds'])<=600, 'Timeout must be 30..600 seconds'
    return c

def manifest_check():
    data=json.loads((ROOT/'package_manifest.json').read_text(encoding='utf8'))
    checks=[]
    for rel, expected in data['files'].items():
        p=(ROOT/rel).resolve(); assert p.is_relative_to(ROOT), 'Manifest path escapes package'
        checks.append({'path':rel,'expected':expected,'actual':sha(p) if p.is_file() else None})
    assert checks and all(r['expected']==r['actual'] for r in checks), 'Package integrity mismatch'
    return checks

def probe(c):
    checks=manifest_check()
    assert sha(FIXTURE)==EXPECTED, 'Fixture source differs'
    assert Path(c['exe']).is_file(), 'Set cadence_root to a legal installed Cadence17.2 root'
    assert (Path(c['cadence_root'])/'share/pcb/text/env').is_file(), 'Cadence default TELENV resource missing'
    live=processes()
    owned=[]; unrelated=[]
    for q in live:
        assert q['created'] and q['exe'] and q['command'], 'Incomplete process identity; refuse run'
        if str(ROOT).lower() in q['command'].lower(): owned.append(q)
        else: unrelated.append(q)
    assert not owned, 'Task-local Allegro process already active: inspect its recorded PID, never blanket kill'
    return {'status':'STATIC_PROBE_PASS_LICENSE_NOT_YET_TESTED','utc':now(),'python':sys.version,'platform':sys.platform,'packageRoot':str(ROOT),'cadenceRoot':c['cadence_root'],'exeSHA256':sha(c['exe']),'fixtureSHA256':sha(FIXTURE),'manifestChecks':checks,'unownedProcessesExcluded':unrelated,'license':'Not probed separately; actual native execution must succeed. No license installation or bypass.'}

def launch(c,phase,runroot,board,script,readonly=False):
    job=runroot/phase; job.mkdir(); (job/'tmp').mkdir(); (job/'pcbenv').mkdir()
    env=os.environ.copy(); env.update(TEMP=str(job/'tmp'),TMP=str(job/'tmp'),ALLEGRO_PCBENV=str(job/'pcbenv'),CDSROOT=c['cadence_root'])
    env['PATH']=str(Path(c['exe']).parent)+os.pathsep+env.get('PATH','')
    for k in ('PYTHONPATH','PYTHONHOME'): env.pop(k,None)
    env['PYTHONNOUSERSITE']='1'
    (job/'pcbenv/env').write_text('source $TELENV\nunset autosave\nset autosave_time = 0\nset psmpath = .\nset padpath = .\n',encoding='ascii')
    args=[c['exe'],'-product',c['product'],'-safe','-nographic','-s',str(script),'-p',str(job)]
    if readonly: args.append('-readonly')
    args.append(str(board))
    si=subprocess.STARTUPINFO(); si.dwFlags|=subprocess.STARTF_USESHOWWINDOW; si.wShowWindow=0
    record={'utcStart':now(),'args':args,'cwd':str(job),'sourceBoard':str(board),'sourceSHA256':sha(board),'environment':{k:env[k] for k in ('TEMP','TMP','ALLEGRO_PCBENV','CDSROOT')},'nativeUIControl':False,'pythonIsolation':{'launcherIsolatedMode':bool(sys.flags.isolated),'childRemovedVariables':['PYTHONPATH','PYTHONHOME'],'childPYTHONNOUSERSITE':'1'},'environmentScope':'Task pcbenv/TEMP/path overrides only; other system and legitimate license environment inherited without recording their values.'}
    with (job/'stdout.txt').open('wb') as stdout,(job/'stderr.txt').open('wb') as stderr:
        p=subprocess.Popen(args,cwd=job,env=env,stdout=stdout,stderr=stderr,startupinfo=si,creationflags=subprocess.CREATE_NO_WINDOW)
        record['pid']=p.pid; record['launcherPID']=os.getpid(); dump(job/'process.json',record)
        try:
            candidates=processes(p.pid)
            assert len(candidates)==1, 'Native child exited before ownership identity captured'
            identity=candidates[0]
            assert identity['parent']==os.getpid() and identity['exe'].lower()==c['exe'].lower()
            assert all(str(v).lower() in identity['command'].lower() for v in (script,job,board)), 'Command identity does not match task paths'
            record['identity']=identity; dump(job/'process.json',record)
            try:
                rc=p.wait(timeout=int(c['timeout_seconds']))
                record.update(exitCode=rc,timedOut=False)
            except subprocess.TimeoutExpired:
                current=processes(p.pid)
                same=(len(current)==1 and all(current[0].get(k)==identity.get(k) for k in ('pid','parent','exe','created','command')))
                record.update(timedOut=True,timeoutIdentityMatches=same)
                if same:
                    p.kill(); p.wait(timeout=15); record['ownedProcessKilled']=True
                else: record['ownedProcessKilled']=False
                raise RuntimeError('Native timeout; exact owned-child identity check logged. Do not kill unrelated GUI processes.')
        finally:
            record['utcFinish']=now(); record['sourceAfterSHA256']=sha(board); dump(job/'process.json',record)
    assert record['exitCode']==0, 'Native nonzero exit; retain all stdout, stderr, journals and process.json'
    assert record['sourceSHA256']==record['sourceAfterSHA256'], 'Native input file changed'
    return record

def text(p): return Path(p).as_posix().replace('"','\\"')
def skill_script(p,expression):
    p.write_text('set NOCONFIRM\nskill errset(load("'+text(ROOT/'scripts/replay.il')+'") t)\nskill errset('+expression+' t)\nskill axlKillDesign()\nquit\n',encoding='ascii')

def parse_summary(p):
    rows=p.read_text(encoding='ascii').splitlines(); result={}; marker=[]
    assert rows[-1]=='L60_NATIVE_READ_COMPLETE'
    for line in rows[:-1]:
        row=line.split('\t')
        if row[0]=='MARKER': marker.append(row[1:])
        else: result[row[0]]=row[1]
    result['markers']=marker
    return result

def verify(runroot):
    checks=[]
    def check(name,ok,detail=None):
        checks.append({'name':name,'pass':bool(ok),'detail':detail})
    for phase in ('before','memory','fresh'):
        p=runroot/(('build' if phase!='fresh' else 'fresh')+'/'+phase+'_summary.tsv')
        s=parse_summary(p)
        check(phase+'_80_components',s['components']=='80')
        check(phase+'_272_logical_pins',s['logicalPins']=='272')
        check(phase+'_69_nets',s['nets']=='69')
        for key,expected in [('etchSegments','932'),('manualSegments','750'),('thermalSegments','182')]: check(phase+'_'+key+'_nonempty_expected',s[key]==expected)
        check(phase+'_layer_order',s['layers']=='("TOP" "L2" "L3" "BOTTOM")')
        check(phase+'_MM_units',s['units'].startswith('("millimeters" '))
        if phase=='before': check('source_marker_absent',s['markerCount']=='0' and not s['markers'])
        else:
            m=s['markers']
            check(phase+'_unique_marker',s['markerCount']=='1' and len(m)==1)
            check(phase+'_marker_text_layer',len(m)==1 and m[0][:2]==['"L60_REPLAY"','"BOARD GEOMETRY/ASSEMBLY_NOTES"'])
            check(phase+'_marker_exact_MM_xy_rotation',len(m)==1 and [float(x) for x in m[0][2:]]==[4.0,4.0,0.0])
    geometry=[runroot/'build/before_geometry.txt',runroot/'build/memory_geometry.txt',runroot/'fresh/fresh_geometry.txt']
    hashes=[sha(p) for p in geometry]
    check('nonempty_native_geometry_readback',all(p.stat().st_size>10000 for p in geometry))
    check('geometry_before_memory_fresh_identical',len(set(hashes))==1,hashes)
    check('fixture_unchanged',sha(FIXTURE)==EXPECTED)
    for phase in ('build','fresh'):
        r=json.loads((runroot/phase/'process.json').read_text())
        check(phase+'_native_exit_zero',r['exitCode']==0 and not r['timedOut'])
        check(phase+'_input_file_unchanged',r['sourceSHA256']==r['sourceAfterSHA256'])
        check(phase+'_owned_identity_logged',bool(r.get('identity')))
    check('saved_new_board_exists',(runroot/'work/L60_replayed.brd').is_file())
    check('save_result_explicit','L60_SAVED_NEW_BOARD' in (runroot/'build/build_result.txt').read_text())
    manifest_check()
    report={'status':'PASS' if all(x['pass'] for x in checks) else 'FAIL','utc':now(),'checks':checks,'passCount':sum(x['pass'] for x in checks),'totalCount':len(checks),'fixtureSHA256':sha(FIXTURE),'savedBoardSHA256':sha(runroot/'work/L60_replayed.brd'),'nativeGeometrySHA256':hashes[0],'limits':['Two directory locations on this machine, not a second physical computer.','One board-note text replay; no GUI competence, routing, SI/PI/EMI, DRC or fabrication signoff claimed.','Knowledge/records travel with this package; Cadence installation, license and executable runtime must be rebuilt independently.']}
    dump(runroot/'verification.json',report)
    assert report['status']=='PASS', 'Verification failed: see verification.json'
    return report

def main():
    assert sys.flags.isolated, 'Use Python -I to isolate user site/PYTHONPATH startup configuration'
    assert str(ROOT).isascii(), 'Only ASCII package paths (spaces supported) are validated; Chinese/non-ASCII native paths are not supported by this package'
    a=argparse.ArgumentParser(description=__doc__); a.add_argument('action',choices=['probe','plan','run','verify']); a.add_argument('--config',type=Path,default=ROOT/'config.local.json'); a.add_argument('--tag',default='run01'); n=a.parse_args()
    assert re.fullmatch(r'[A-Za-z0-9_]{1,40}',n.tag), 'Use a safe unique tag'
    c=config(n.config); assert c['cadence_root'].isascii(), 'Cadence installation path must be ASCII for this package'; runroot=ROOT/'runs'/n.tag
    if n.action=='probe':
        r=probe(c); print(json.dumps(r,ensure_ascii=True)); return
    if n.action=='plan':
        manifest_check(); print(json.dumps({'packageRoot':str(ROOT),'runRoot':str(runroot),'fixture':str(FIXTURE),'savedOutput':str(runroot/'work/L60_replayed.brd'),'cadenceExecutable':c['exe'],'phases':['new scratch input','isolated native marker SaveAs','fresh readonly native reread','verify source and exact geometry'],'runExistsRefuseOverwrite':runroot.exists()},indent=2)); return
    if n.action=='verify':
        r=verify(runroot); print(json.dumps({'status':r['status'],'checks':r['totalCount'],'runRoot':str(runroot)})); return
    assert not runroot.exists(), 'Refuse overwrite: choose a new tag, retain previous failure evidence'
    before=probe(c); runroot.mkdir(parents=True); dump(runroot/'probe.json',before)
    (runroot/'work').mkdir(); scratch=runroot/'work/INPUT_COPY.brd'; shutil.copy2(FIXTURE,scratch)
    output=runroot/'work/L60_replayed.brd'
    try:
        script=runroot/'build.scr'; skill_script(script,'l60Build("'+text(runroot/'build')+'" "'+text(output)+'")')
        launch(c,'build',runroot,scratch,script)
        assert output.is_file() and output.stat().st_size>100000, 'No saved board; read build logs'
        script=runroot/'fresh.scr'; skill_script(script,'l60Read("'+text(runroot/'fresh')+'" "fresh")')
        launch(c,'fresh',runroot,output,script,readonly=True)
        r=verify(runroot); print(json.dumps({'status':r['status'],'checks':r['totalCount'],'runRoot':str(runroot)}))
    except Exception:
        dump(runroot/'failure.json',{'utc':now(),'traceback':traceback.format_exc(),'fixtureSHA256':sha(FIXTURE),'neverDeleteEvidence':True}); raise
if __name__=='__main__': main()
