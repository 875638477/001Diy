from pathlib import Path
import json
R=Path(r'D:\001DIY\005lib\01AIEDA\learning\examples\lesson07_completion_20261018')
s=(R/'scripts/validate.py').read_text(encoding='utf-8-sig')
s=s.replace("('create_board02','L7C_BOARD COMPLETE')","('create_board03','L7C_BOARD COMPLETE')").replace("('reopen_board','L7C_READ COMPLETE')","('reopen_board02','L7C_READ COMPLETE')").replace("read('reopen_board')","read('reopen_board02')")
s=s.replace("result={'date':", "result={'status':'PASS_CAD_LESSON07_COMPLETION' if all(c['pass'] for c in checks) else 'FAIL_CAD_LESSON07_COMPLETION','finalBoard':str(R/'library/eda_l07c_clearance_4layer_v2.brd'),'finalSpec':str(R/'spec_v2.json'),'finalReadback':str(R/'logs/reopen_board02/readback.txt'),'date':")
addition='''
# Additional independently checked final-v2 data. Do not count JSON success flags alone.
centers=[x for x in f.get('COPPER_POLY',[]) if x[0]=='ETCH/TOP' and abs(x[2]-math.pi*.4**2)<1e-6]
check('flash exactly five shapes including drilled center',len(f.get('COPPER_POLY',[]))==5 and len(centers)==1)
check('center dot diameter matches drilled hole',centers[0][1]==[[-.4,-.4],[.4,.4]] if centers else False)
for label,rows,origin in [('package',p,[0,0]),('board',b,[20,20])]:
 for number,rel,angle in [('1',[-5,0],0),('2',[5,0],90)]:
  matches=[x for x in rows['PIN'] if x[1]==number]
  check(label+' electrical pin '+number+' geometry',len(matches)==1 and matches[0][2]==[origin[0]+rel[0],origin[1]+rel[1]] and matches[0][3]==angle and matches[0][6]=='PLATED' and abs(matches[0][7]-.8)<1e-9,matches)
 for pad in rows['PAD']:
  if 'pth_' in pad[0].lower() and 'npth' not in pad[0].lower():
   if pad[2]=='REGULAR':check(label+' regular diameter '+pad[1],pad[3]=='CIRCLE' and pad[4]==[[-.8,-.8],[.8,.8]],pad)
   if pad[2]=='ANTI':check(label+' anti diameter '+pad[1],pad[3]=='CIRCLE' and pad[4]==[[-1,-1],[1,1]],pad)
   if pad[2]=='THERMAL':check(label+' native FSM mapping '+pad[1],pad[3]=='FLASH' and pad[5]=='eda_l07c_th4_200_160_w30_d80',pad)
  if 'npth' in pad[0].lower():check(label+' no fabricated NPTH copper '+pad[1]+' '+pad[2],pad[3] in [None,'NULL'] and (pad[4] is None or pad[4]==[[0,0],[0,0]]),pad)
 check(label+' mechanical usage',any(x[0]=='' and x[1]=='Mechanical_hole' and x[2] is None for x in rows.get('PIN_NET',[])))
 checksKO=[x for x in rows.get('SHAPE',[]) if x[0]=='ROUTE KEEPOUT/ALL']
 expectedBox=[[origin[0]-1.5,origin[1]-1.5],[origin[0]+1.5,origin[1]+1.5]]
 check(label+' independent route keepout persisted',len(checksKO)==1 and checksKO[0][1]==expectedBox,checksKO)
for layer in ['ETCH/TOP','ETCH/L2','ETCH/L3','ETCH/BOTTOM']:
 actual=[x for x in b.get('SHAPE',[]) if x[0]==layer]
 check('actual copper GND membership '+layer,len(actual)==1 and actual[0][5]=='GND',actual)
for layer in ['BOUNDARY/TOP','BOUNDARY/L2','BOUNDARY/BOTTOM']:
 actual=[x for x in b.get('BOUNDARY_NET',[]) if x[0]==layer]
 check('explicit boundary GND membership '+layer,len(actual)==1 and actual[0][2]=='GND',actual)
for layer in ['ETCH/TOP','ETCH/L2','ETCH/BOTTOM']:
 paths=[x for x in b.get('THERMAL_CLINE',[]) if x[0]=='1' and x[1]==layer]
 check('four actual GND thermal spokes '+layer,len(paths)==4,paths)
 for i,path in enumerate(paths):
  rr=[math.dist(p,[15,20]) for p in path[3]]
  check('thermal reaches actual copper '+layer+' '+str(i),min(rr)<.8 and max(rr)>.929 and path[2]==.127 and path[4]=='GND',path)
 polys=[x for x in b.get('THERMAL_COPPER_POLY',[]) if x[0]=='1' and x[1]==layer]
 check('actual thermal copper polygons '+layer,len(polys)==4 and all(x[3]>0 for x in polys),polys)
check('OTHER pin has no GND thermal',not any(x[0]=='2' for x in b.get('THERMAL_CLINE',[])))
check('pin nets independently read',sorted((x[0],x[2]) for x in b['PIN_NET'] if x[0])==[('1','GND'),('2','OTHER')],b['PIN_NET'])
challenge=(R/'logs/create_board03/create.txt').read_text()
check('controlled route keepout challenge detected','controlled_intrusion_drc=2' in challenge and 'Line to Route Keepout Spacing' in challenge)
check('controlled mechanical hole challenge detected','Mechanical Drill Hole to Line Spacing' in challenge)
check('rollback followed by full DRC','drc_update=0 state=t' in challenge)
'''
s=s.replace("result={'status'", addition+"\nresult={'status'")
(R/'scripts/validate.py').write_text(s,encoding='utf-8')
spec=json.loads((R/'spec.json').read_text(encoding='utf-8-sig'))
spec.update(revision=2,finalBoard='library/eda_l07c_clearance_4layer_v2.brd',finalReadback='logs/reopen_board02/readback.txt',finalNativeSource='scripts/lesson07c_v2.il',v1Status='Historical: NPTH keepout/clearance valid; dynamic boundary net parameter ignored, so v1 positive shapes not GND. v2 assigns boundary GND explicitly and verifies actual copper and thermal clines.')
spec['copper']['positiveLayers']='Dynamic BOUNDARY explicitly axlDBAssignNet to GND; generated ETCH readback GND.'
spec['positiveThermals']={'pin':'1','layers':['TOP','L2','BOTTOM'],'nativeWidth':.127,'countPerLayer':4,'center':[15,20],'radialEndpoint':.98,'note':'Actual positive dynamic thermal geometry differs from negative-plane flash. Native default width is educational only; current/fabrication must define production rules.'}
(R/'spec_v2.json').write_text(json.dumps(spec,indent=2,ensure_ascii=False),encoding='utf-8')
