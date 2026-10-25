from pathlib import Path
import json,os,subprocess,shutil,hashlib,datetime
R=Path(r'D:\001DIY\005lib\01AIEDA\learning\examples\lessonHI_38_50_20261021');B=R/'native/private_padstacks';old=B/'hi_via026_c052_tented.pxml';p=B/'hi_via026_c052_tent.pxml';p.write_text(old.read_text().replace('hi_via026_c052_tented','hi_via026_c052_tent'),encoding='utf8')
log=R/'logs/private_via026_import01';log.mkdir(exist_ok=False);env=os.environ.copy()
for key,sub in [('TEMP','tmp'),('TMP','tmp'),('ALLEGRO_PCBENV','pcbenv')]:
 (log/sub).mkdir(exist_ok=True);env[key]=str(log/sub)
env['PATH']=r'C:\Program0\Cadence\SPB172\tools\bin'+';'+env.get('PATH','')
args=[r'C:\Program0\Cadence\SPB172\tools\bin\padstack_editor.exe','-x',str(p)]
si=subprocess.STARTUPINFO();si.dwFlags|=subprocess.STARTF_USESHOWWINDOW;si.wShowWindow=0;start=datetime.datetime.now(datetime.timezone.utc).isoformat()
with (log/'stdout.txt').open('wb') as out,(log/'stderr.txt').open('wb') as err:
 proc=subprocess.Popen(args,cwd=B,env=env,stdout=out,stderr=err,startupinfo=si,creationflags=subprocess.CREATE_NO_WINDOW);code=proc.wait(timeout=60)
rec={'args':args,'pid':proc.pid,'startUTC':start,'finishUTC':datetime.datetime.now(datetime.timezone.utc).isoformat(),'completed':True,'exitCode':code,'cwd':str(B),'processEnvironmentOverrides':{k:env[k] for k in ['TEMP','TMP','ALLEGRO_PCBENV']},'pxmlSHA256':hashlib.sha256(p.read_bytes()).hexdigest().upper()};(log/'launch.json').write_text(json.dumps(rec,indent=2));assert code==0
pad=B/'hi_via026_c052_tent.pad';assert pad.exists();dst=R/'library'/pad.name;assert not dst.exists();shutil.copyfile(pad,dst)
spec=json.loads((B/'spec.json').read_text());spec.update({'status':'NATIVE_BINARY_IMPORTED_WAITING_PAD_DEFINITION_READBACK','name':'HI_VIA026_C052_TENT','pxml':str(p),'pxmlSHA256':rec['pxmlSHA256'],'binary':str(pad),'libraryCopy':str(dst),'binarySHA256':hashlib.sha256(pad.read_bytes()).hexdigest().upper(),'namePreparationCorrection':{'old':'hi_via026_c052_tented','oldLength':21,'new':'hi_via026_c052_tent','newLength':19,'reason':'Official17.2axlLoadPadstack PADLIB search documents20-character limit. Corrected before any native import; old prepared PXML retained.'}});(B/'spec_v2_imported.json').write_text(json.dumps(spec,indent=2));print(json.dumps(rec,indent=2));print('PAD',str(dst),spec['binarySHA256'])
il=r'''procedure(hiInspectPrivatePad(out lib)
 let((f ps pad layers)
  f=outfile(strcat(out "/private_pad_definition.txt"))
  axlSetVariable("padpath" list(lib))
  ps=axlLoadPadstack("HI_VIA026_C052_TENT")
  unless(ps error("Private padstack failed to load\n"))
  fprintf(f "PAD_DEFINITION=%L\nACTUAL_ROUTE_LAYERS=%L\n" ps->?? axlSubclassRoute())
  unless(abs(ps->drillDiameter-0.26)<0.00001 && equal(ps->usage "Through_via") error("Unexpected drill/usage\n"))
  layers=append(mapcar(lambda((x) strcat("ETCH/" x)) axlSubclassRoute()) list('internal "VIA CLASS/SOLDERMASK_TOP" "VIA CLASS/SOLDERMASK_BOTTOM"))
  foreach(layer layers
   foreach(kind list("REGULAR" "ANTI" "THERMAL" "KEEPOUT")
    pad=axlDBGetPad(ps layer kind)
    fprintf(f "PAD_LAYER layer=%L type=%L figure=%L bbox=%L attrs=%L\n" layer kind if(pad then pad->figureName else nil) if(pad then pad->bBox else nil) if(pad then pad->?? else nil))))
  fprintf(f "PRIVATE_PAD_DEFINITION_READ_COMPLETE_NO_SAVE_NO_PLACEMENT_NO_DRC_RECOMPUTE\n") close(f) t))
'''
(R/'scripts/private_pad_inspectHI.il').write_text(il,encoding='ascii')
for v in ['2L','4L']:
 tag='private_pad_inspect_'+v+'_01';h='set NOCONFIRM\nskill errset(load('+json.dumps((R/'scripts/private_pad_inspectHI.il').as_posix())+') t)\nskill errset(hiInspectPrivatePad('+json.dumps((R/'logs'/tag).as_posix())+' '+json.dumps((R/'library').as_posix())+') t)\nquit\nfillin "yes"\n';(R/f'scripts/{tag}.scr').write_text(h,encoding='ascii')
