from pathlib import Path
import json,hashlib,copy
R=Path(r'D:\001DIY\005lib\01AIEDA\learning\examples\lessonHI_38_50_20261021')
body=r'''procedure(hiCCSpacingChallenge(out)
 let((f name result hit hasCC)
  f=outfile(strcat(out "/hi_cc_spacing_challenge.txt")) name="HI_USB_CC1_J2_S_2L" hit=nil
  foreach(key list('smdpin_line 'line_line) unless(abs(axlCNSGetSpacing(name "TOP" key)-0.2)<0.00001 error("Unexpected baseline scopedCC spacing\n")))
  unwindProtect(progn(
   foreach(key list('smdpin_line 'line_line) unless(axlCNSSetSpacing(name nil key "0.4 MM") error("Cannot tighten scoped CC rule\n")))
   axlDBControl('drcEnable t)
   fprintf(f "CC_STRICT_REQUEST time=%L cset=%L twoFieldsNormal=.2 strict=.4 online=%L\n" getCurrentTime() name axlDBControl('drcEnable)) drain(f)
   result=axlDRCUpdate(t) fprintf(f "CC_STRICT_RETURN time=%L result=%L\n" getCurrentTime() result) f29DumpDRC(f "CC1_STRICT_040")
   unless(numberp(result) error("Strict scopedCC DRC did not return numeric result\n"))
   foreach(d axlDBGetDesign()->drcs
    hasCC=nil
    foreach(obj d->violations when(obj->net && equal(obj->net->name "USB_CC1") hasCC=t))
    when(hasCC && abs(atof(d->expected)-0.4)<0.00011 && abs(atof(d->actual)-0.3)<0.00011 hit=t fprintf(f "CC1_REAL_030_NATIVE_DRC=%L\n" d->??)))
   unless(hit error("Tightened CC1 rule did not catch planned real0.3mm gap\n"))
   t) progn(
    foreach(key list('smdpin_line 'line_line) unless(axlCNSSetSpacing(name nil key "0.2 MM") error("Cannot restore scopedCC rule\n")))
    result=axlDRCUpdate(t) fprintf(f "CC_RESTORED_RETURN time=%L result=%L storedDRCs=%d\n" getCurrentTime() result length(axlDBGetDesign()->drcs)) f29DumpDRC(f "CC1_RESTORED_020")
    unless(numberp(result) && length(axlDBGetDesign()->drcs)==0 error("Restored scoped CC rule did not recover zeroDRC\n"))))
  fprintf(f "CC1_SPACING_CHALLENGE_COMPLETE_REAL030_CAUGHT_THEN_RESTORED020_NO_GLOBAL_RELAXATION\n") close(f) t))
'''
p=R/'scripts/batchHI_shapes_v3.il';p.write_text(p.read_text()+'\n'+body,encoding='ascii')
s=(R/'scripts/compile_batchHI_v12.py').read_text();needle=" else:raise ValueError(check['type'])";repl=" elif check['type']=='ccSpacingChallenge':statements.append(f'hiCCSpacingChallenge({q(out.as_posix())})')\n else:raise ValueError(check['type'])";assert needle in s;s=s.replace(needle,repl);(R/'scripts/compile_batchHI_v13.py').write_text(s,encoding='ascii')
for v in ['2L','4L']:
 paths=[R/f'plans/aux_remote_{v}_v9.json',R/f'plans/CC_entry_{v}_v4.json',R/f'plans/VBUS_entry_{v}_v3.json',R/f'plans/USB_aux_returns_{v}_03.json'];plans=[json.loads(p.read_text(encoding='utf8')) for p in paths];ops=copy.deepcopy([o for d in plans for o in d['operations']]);assert len(ops)==len(set(o['id'] for o in ops))
 proofs=[p for d in plans for p in d.get('proofs',[])];proofs+=[{'from':o['id'],'to':'U1.23','connected':True} for o in ops if o['type']=='via' and o['net']=='GND']
 checks=[{'type':'hseIsolation','anchorXY':[45.45,28.85],'localLayer':'BOTTOM' if v=='2L' else 'L2','guardPoints':[[42.2,39.8],[44.2,39.8],[47.8,33.5]]}]
 if v=='2L':checks.append({'type':'ccSpacingChallenge'})
 d={'status':'ROOT_APPROVED_USB_AUX_EXPLICIT_BATCH','nativeVariant':v,'units':'mm','inputBoardIdentity':json.loads((R/f'inventory/current_{v}.json').read_text()),'operations':ops,'constraintOperations':[o for d in plans for o in d.get('constraintOperations',[])],'proofs':proofs,'postChecks':checks,'engineeringSources':[{'path':str(p),'sha256':hashlib.sha256(p.read_bytes()).hexdigest().upper()} for p in paths],'scope':['Root final auxiliary group including actual6mechanicalholes screen. No MCU source joint or HSE rework in this batch.','Fullnative build DRC + source/target/return graphs + oldanchor HSEnegative; separate fresh interim read is geometry/storedDRC only, final wholeboard fullfresh pending.','2L connector CC1 finite ClassClass spacing .2 only; strict .4 real .3 challenge must fail then restore0.','4L CC2 static-Rd via-return distance2.5005mm explicit use-specific engineering exception, not applicable to highspeed DP.']}
 (R/f'batches/USB_aux_{v}_b013.json').write_text(json.dumps(d,indent=2),encoding='utf8');print(v,len(ops),'ops',len(proofs),'proofs')
