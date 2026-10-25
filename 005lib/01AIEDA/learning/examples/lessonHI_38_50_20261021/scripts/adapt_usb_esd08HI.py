from pathlib import Path
import json,copy,hashlib,math
R=Path(r'D:\001DIY\005lib\01AIEDA\learning\examples\lessonHI_38_50_20261021')
src=R/'engineering_mcu/plans/usb_critical_routes_v8.json';d=json.loads(src.read_text(encoding='utf8'))
es=R/'engineering_power/ESD_ground_routes_04c.json';esd=json.loads(es.read_text(encoding='utf8'))
components={x['ref'] for x in json.loads((R/'inventory/normalized_actual_4L.json').read_text(encoding='utf8'))['placements']}
for v in ['4L','2L']:
 psource='P_USB_PROVISIONAL' if v=='4L' else 'HI2L_P_USB_FS'
 pclass='HI_USB_DP_P_'+v;mirror='HI_USB_MIRROR_P_'+v
 constraints=[{'type':'netClass','name':pclass,'domain':'physical','cset':psource,'nets':['USB_DP']},
 {'type':'csetCopy','domain':'physical','name':mirror,'copyFrom':psource,'values':{},'layerValues':{'BOTTOM':{'allow_etch':True}}},
 {'type':'region','id':'HI_J2_MIRROR_BOTTOM','layer':'BOTTOM','polygon':[[39.35,5.3],[41.15,5.3],[41.15,6.7],[39.35,6.7]],'assignments':[{'domain':'physical','netClass':pclass,'cset':mirror}]}]
 constraints.append({'type':'ecsetCopy','name':'HI_E_USB_CONNECTOR_'+v,'copyFrom':'E_USB_FS_BUDGET' if v=='4L' else 'HI2L_E_USB_BUDGET','pair':'DP_USB_CONNECTOR','values':{'Differential_Pair_Phase_Tolerance':'4 MM','Differential_Pair_Max_Uncoupled_Length':'13.5 MM'}})
 if v=='2L':
  constraints.extend([
   {'type':'csetCopy','domain':'spacing','name':'HI_USB_J2_SOURCE_S_2L','copyFrom':'HI2L_S_CLASSCLASS_10','values':{'smdpin_line':'0.2 MM'}},
   {'type':'region','id':'HI_USB_J2_SOURCE_ESCAPE','layer':'TOP','polygon':[[38.95,7.25],[39.55,7.25],[39.55,8.55],[38.95,8.55]],'assignments':[{'domain':'spacing','netClass':'HI2L_USB_FS_S','otherNetClass':'HI2L_USB_AUX_S','cset':'HI_USB_J2_SOURCE_S_2L'}]}
  ])
 sc='NC_USB_FS_S' if v=='4L' else 'HI2L_USB_FS_S' 
 others=[('NC_DIGITAL_GENERAL_S','S_USB_OTHER_050')] if v=='4L' else [('HI2L_UART_CAN_DIGITAL_S','HI2L_S_CLASSCLASS_8'),('HI2L_RESET_BOOT_SWD_S','HI2L_S_CLASSCLASS_6')]
 assigns=[]
 for i,(other,source) in enumerate(others):
  name='HI_USB_MCU_S_'+str(i+1)+'_'+v
  constraints.append({'type':'csetCopy','domain':'spacing','name':name,'copyFrom':source,'values':{'smdpin_line':'0.2 MM','line_line':'0.2 MM'}})
  assigns.append({'domain':'spacing','netClass':sc,'otherNetClass':other,'cset':name})
 constraints.append({'type':'region','id':'HI_USB_MCU_ESCAPE','layer':'TOP','polygon':[[39.8,21.2],[41.6,21.2],[41.6,23.4],[39.8,23.4]],'assignments':assigns})
 original=copy.deepcopy(d['commonOperations']+d['variantOperations'][v]+esd['operations'])
 aliases=[];vias=[x for x in original if x['type']=='via']
 for op in original:
  if op['type']=='via' and op['padstack']=='L28_VIA030_C060_OR_VERIFIED_TENTED_PRIVATE_VARIANT':
   op['engineeringPlaceholderPadstack']=op['padstack'];op['padstack']='L28_VIA030_C060';op['padstackResolution']='Existing embedded and HI-library standard through-via. Native actual TOP/BOTTOM mask figureNULL and Film drawMissingPadApertures=false were verified in edit_pilot_4L_02/2L_02; no new variant required.'
  if op['type']!='route':continue
  for key,point in [('from',op['points'][0]),('to',op['points'][-1])]:
   if isinstance(op.get(key),list):
    ref,pin=op[key]
    if ref in components:op[key]=ref+'.'+str(pin)
    else:
     op[key]=ref
     aliases.append({'id':ref,'net':op['net'],'layer':op['layer'],'xy':point})
  for key,point in [('from',op['points'][0]),('to',op['points'][-1])]:
   if not op.get(key):
    near=[x for x in vias if x['net']==op['net'] and math.dist(x['xy'],point)<1e-5]
    if len(near)==1:op[key]=near[0]['id']
 if v=='2L':
  original.append({'type':'shape','id':'HI_USB_TOP_REFERENCE','net':'GND','layer':'TOP','polygon':d['referenceAndReturn']['topReferencePatch'],'dynamic':True,'purpose':'Actual limited application GND patch for BOTTOM mirror branch, auto-cleared around real TOP signal copper. Coverage discontinuities require independent measurement.'})
 proofs=[{'from':a,'to':b,'connected':True} for a,b in [('J2.A6','U4.6'),('J2.B6','U4.6'),('J2.A7','U4.4'),('J2.B7','U4.4'),('U4.1','R5.2'),('U4.3','R6.2'),('R11.2','R5.2'),('R5.1','U1.33'),('R6.1','U1.32'),('U4.2','U1.47'),('C10.2','U1.47')]]
 if v=='2L':proofs.extend([{'from':'USB_RETURN_LEFT','to':'HI_USB_TOP_REFERENCE','connected':True},{'from':'USB_RETURN_RIGHT','to':'HI_USB_TOP_REFERENCE','connected':True}])
 o={'status':'ENGINEERING_CANDIDATE_REQUIRE_NATIVE_DRC_AND_DIFFERENTIAL_RULE_FEEDBACK','units':'mm','nativeVariant':v,'placementChanges':d['placementChanges'],'constraintOperations':constraints,'operations':original,'aliases':aliases,'proofs':proofs,'postChecks':[{'type':'hseIsolation','anchorXY':[45.45,28.85],'localLayer':'L2' if v=='4L' else 'BOTTOM','guardPoints':[[42.2,39.8],[44.2,39.8],[47.8,33.5]]}],'engineeringSources':[{'path':str(s),'sha256':hashlib.sha256(s.read_bytes()).hexdigest().upper()} for s in [src,es]],'notes':['Original phase1/uncoupled6 failed natively in b006a. USB8 uses reviewed connector-pair-only static ECSet copy phase4mm/uncoupled13.5mm/maxvia2; shared pair original phase1/uncoupled6 unchanged, new DM geometry intended to improve actual coupling. These are explicit planar teaching budgets, not USB specification or SI acceptance.','USB_DP alone split into physical class to allow BOTTOM only in connector mirror region. All other domains and outside layer permissions preserved.','Actual explicit protected bulk widths: 4L.26 or2L1.15. Minimum native width remains.20 at connector/ESD/MCU ports; path is nonuniform, not certified90ohm.','Original source via mask figures NULL and ArtworkdrawMissingPadApertures false; manufacturing underside insulation/clearance still open.']}
 (R/f'batches/usb_esd_{v}_b008.json').write_text(json.dumps(o,indent=2),encoding='utf8')
 print(v,len(original),'operations',len(proofs),'additional proofs')
