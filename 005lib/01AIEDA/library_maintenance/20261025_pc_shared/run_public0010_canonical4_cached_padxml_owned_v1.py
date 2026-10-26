"""Root-invoked official cached-library export and fresh four-PAD XML pairs.

dump_libraries -ac exports actual board packages/dependencies to a fresh private
directory. Only the four PADs used by six new canonical packages are copied to
two isolated padstack_editor -xo jobs. No source/public modifications or CAD UI.
Native success is not equivalence: complete manufacturing XML review follows.
"""
from pathlib import Path
import argparse,hashlib,importlib.util,json,os,shutil,subprocess,time,xml.etree.ElementTree as E
M=Path(__file__).parent;CAD=Path(r'C:\Program0\cadence\SPB172');PUBLIC=Path(r'D:\001DIY\005lib')
NAMES=['smd_o360x300p0s10','smd_o400x640p0s10','smd_o500x400p0s10','pad_1_1d3']
sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest().upper();jr=lambda p:json.loads(Path(p).read_text('utf-8-sig'))
def need(ok,msg):
 if not ok:raise ValueError(msg)
def main():
 ap=argparse.ArgumentParser(description=__doc__)
 for n in ['board','guard','out']:ap.add_argument('--'+n,type=Path,required=True)
 ap.add_argument('--board-sha256',required=True);ap.add_argument('--timeout',type=int,default=240);a=ap.parse_args();need(not a.out.exists() and a.out.resolve().is_relative_to(M.resolve()),'Fresh private output required')
 expected=a.board_sha256.upper();need(sha(a.board)==expected,'Actual board SHA changed')
 spec=importlib.util.spec_from_file_location('gh',M/'publish_exact_public_olbs.py');g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g);guard=jr(a.guard);before=g.verify_guard(guard)
 a.out.mkdir();export=a.out/'official_export';export.mkdir();copy=a.out/'INPUT_COPY.brd';shutil.copyfile(a.board,copy);need(sha(copy)==expected,'Independent board copy mismatch')
 env=os.environ.copy();env['CDSROOT']=str(CAD);env['PATH']=str(CAD/'tools/bin')+os.pathsep+env.get('PATH','');(a.out/'temp').mkdir();env['TEMP']=env['TMP']=str(a.out/'temp')
 launches=[]
 def launch(args,cwd,label):
  started=time.time()
  with (cwd/(label+'_stdout.txt')).open('wb') as so,(cwd/(label+'_stderr.txt')).open('wb') as se:
   p=subprocess.Popen(list(map(str,args)),cwd=cwd,env=env,stdout=so,stderr=se,creationflags=subprocess.CREATE_NO_WINDOW)
   (cwd/(label+'_OWNED_PROCESS.json')).write_text(json.dumps(dict(pid=p.pid,command=list(map(str,args))),indent=2),'utf-8')
   try:code=p.wait(timeout=a.timeout)
   except subprocess.TimeoutExpired:p.terminate();p.wait(timeout=30);raise RuntimeError('Only owned native process timed out: '+label)
  row=dict(command=list(map(str,args)),cwd=str(cwd),exit_code=code,seconds=time.time()-started);launches.append(row);need(code==0,'Official native export failed '+label);return row
 launch([CAD/'tools/bin/dump_libraries.exe','-ac',copy],export,'dump_libraries')
 need(sha(a.board)==sha(copy)==expected,'Official library exporter modified protected board')
 lookup={p.name.casefold():p for p in export.iterdir() if p.is_file()};rows=[]
 for name in NAMES:
  cached=lookup.get((name+'.pad').casefold());public=PUBLIC/'01Pad_lib'/(name+'.pad');need(cached is not None and public.is_file(),'Canonical cached/public PAD missing '+name)
  rows.append(dict(name=name,cached=str(cached),cached_sha256=sha(cached),public=str(public),public_sha256=sha(public)))
 for side in ['cached','public']:
  d=a.out/(side+'_padxml');d.mkdir()
  for row in rows:shutil.copyfile(row[side],d/(row['name']+'.pad'));need(sha(d/(row['name']+'.pad'))==row[side+'_sha256'],'Independent PAD copy differs')
  launch([CAD/'tools/bin/padstack_editor.exe','-xo','*.pad'],d,'padstack_editor')
  xp=d/'pad2xml.pxml';root=E.parse(xp).getroot();pads=root.findall('padstack');need(len(pads)==4 and {p.findtext('padstackname').casefold() for p in pads}==set(NAMES),'Complete exact four native PAD XML definition cohort differs')
  for row in rows:
   need(sha(d/(row['name']+'.pad'))==row[side+'_sha256'],'XML export changed input PAD copy')
   row[side+'_xml']=str(xp);row[side+'_xml_sha256']=sha(xp)
 after=g.verify_guard(guard);need(sha(a.board)==sha(copy)==expected,'Protected board changed')
 for row in rows:need(sha(row['public'])==row['public_sha256'],'Public PAD changed during readonly export')
 result=dict(status='COMPLETE_OFFICIAL_CACHE_PUBLIC_FOUR_PAD_XML_PAIRS_REQUIRES_FULL_MANUFACTURING_REVIEW',actual_board=str(a.board),board_sha256_before=expected,board_sha256_after=sha(a.board),public_unchanged=True,guard=str(a.guard),guard_sha256=sha(a.guard),full_public_files_before=before,full_public_files_after=after,canonical_packages=['c0603_pc','c0805_pc','c1206_pc','r0603_pc','fb0805_pc','l0805_pc'],canonical_unique_PAD_count=4,rows=rows,launches=launches,script_sha256=sha(__file__),official_local_docs=['C:/Program0/cadence/SPB172/share/pcb/batchhelp/dump_libraries.txt','C:/Program0/cadence/SPB172/doc/dcoms/dchap.html#dlib'],no_equivalence_approval=True)
 p=a.out/'CACHED_CANONICAL4_PAD_XML_NATIVE_EXPORT.json';p.write_text(json.dumps(result,indent=2),'utf-8');print(json.dumps(dict(status=result['status'],report=str(p),sha256=sha(p)),indent=2))
if __name__=='__main__':main()
