from pathlib import Path
import json,copy,hashlib
R=Path(r'D:\001DIY\005lib\01AIEDA\learning\examples\lessonHI_38_50_20261021')
p=R/'scripts/batchHI_shapes_v3.il';s=p.read_text();body=(R/'scripts/batchHI.il').read_text();i=body.index('procedure(hiFinalize(');fn=body[i:]
fn=fn.replace('let((count)','let((count drcResult)')
fn=fn.replace('  axlDRCUpdate(t) f29DumpDRC(f "HI_BATCH_FINAL")','''  fprintf(f "HI_FULL_DRC_REQUEST_BEGIN time=%L g_mode=t online=%L physicalModes=%L spacingModes=%L electricalModes=%L\\n" getCurrentTime() axlDBControl('drcEnable) axlCNSPhysicalModeGet('all) axlCNSSpacingModeGet('all) axlCNSEcsetModeGet('all)) drain(f)
  drcResult=axlDRCUpdate(t)
  fprintf(f "HI_FULL_DRC_REQUEST_RETURN time=%L result=%L online=%L storedDRCs=%d\\n" getCurrentTime() drcResult axlDBControl('drcEnable) length(axlDBGetDesign()->drcs)) drain(f)
  unless(numberp(drcResult) error("Full DRC update returned nil/non-numeric; stored zero cannot be accepted as recomputed zero\\n"))
  f29DumpDRC(f "HI_BATCH_FINAL")''')
assert 'HI_FULL_DRC_REQUEST_RETURN' in fn;p.write_text(s+'\n; Instrument exact unchanged all-on-plus-batch DRC request and result.\n'+fn,encoding='ascii')
for v,name in [('2L','SPI_external_2L_engineered_v10.json'),('4L','SPI_external_4L_engineered_v6.json')]:
 src=R/'engineering_power'/name;d=json.loads(src.read_text(encoding='utf8'));ops=copy.deepcopy(d['operations']);defs=[];proofs=[{'from':p['source'],'to':p['target'],'connected':True} for p in d['requiredProofs']]
 for o in ops:
  if o['type']=='via' and o['net']=='GND':proofs.append({'from':o['id'],'to':'U1.23','connected':True})
  if o['type']=='route' and o['net']=='GND':proofs.append({'from':o['id'],'to':'U1.23','connected':True})
 if v=='2L':proofs.append({'from':'C9.1','to':'SPI_PREFILTER_ROW_SHIFT','connected':True})
 current=json.loads((R/f'inventory/current_{v}.json').read_text());out={'status':'ROOT_APPROVED_EXPLICIT_SPI_ADAPTED_FOR_NATIVE','nativeVariant':v,'units':'mm','inputBoardIdentity':current,'engineeringSource':str(src),'engineeringSourceSHA256':hashlib.sha256(src.read_bytes()).hexdigest().upper(),'operations':ops,'proofs':proofs,'postChecks':[{'type':'hseIsolation','anchorXY':[45.45,28.85],'localLayer':'BOTTOM' if v=='2L' else 'L2','guardPoints':[[42.2,39.8],[44.2,39.8],[47.8,33.5]]}],'notes':['Source rebase only the independently verified2L GND stitch37.4,27.4; all original manual copper deletions remain unique.','Native all-on-plus-batch DRC request/return/modes/timestamps instrumented. Fresh interim readback may inspect stored state; final whole-board fresh fullcheck remains mandatory.']}
 (R/f'batches/SPI_external_{v}_b012.json').write_text(json.dumps(out,indent=2),encoding='utf8');print(v,len(ops),'ops',len(proofs),'proofs')
