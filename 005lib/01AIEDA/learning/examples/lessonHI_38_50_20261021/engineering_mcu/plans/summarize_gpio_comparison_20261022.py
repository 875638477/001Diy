import pathlib,json,math,hashlib,datetime
P=pathlib.Path(r'D:\001DIY\005lib\01AIEDA\learning\examples\lessonHI_38_50_20261021\engineering_mcu\plans');H=P.parents[1]
def load(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def metrics(z):
 out=[]
 for net in ['GPIO_PB1','GPIO_PB10','GPIO_PB11','GPIO_PB12','GPIO_PB13','GPIO_PB14','GPIO_PB15']:
  ops=[o for o in z.get('operations',[])if o['net']==net];route=[o for o in ops if o['type']=='route'];via=[o for o in ops if o['type']=='via'];out.append(dict(net=net,pathFound=bool(route),incrementalLengthMM=round(sum(math.dist(a,b)for o in route for a,b in zip(o['points'],o['points'][1:])),4),newSignalVias=len(via)))
 return out
out=dict(status='ENGINEERING_COMPARISON_NOT_NATIVE_APPROVAL',date='2026-10-22',headerNativeXY=[40,55],headerComparisonXY=[18,9],rotation=90,preserved=['All original live R27/C11 V3 copper','J2 fixed mechanical datum','North51 six routed signal paths','MCU direct VDD/cap/GND loops','HSE unique anchor/guards/moat','ADC/C9/MCU pose and main feed geometry for comparisons 59/68/71/72'],variants={})
for v in ['2L','4L']:
 entries={}
 for label,fn in [('nativeNorthHeaderIndependent59',f'GPIO7_{v}_independent59.json'),('southHeaderIndependent71',f'GPIO7_{v}_independent71.json'),('southHeaderJoint72',f'GPIO7_{v}_negotiated72.json')]:
  f=P/fn;z=load(f);entries[label]=dict(path=str(f),sha256=hashlib.sha256(f.read_bytes()).hexdigest(),status=z['status'],metrics=metrics(z),conflicts=len(z.get('conflicts',[])),jointIteration=z.get('round'),notions='Independent path lengths are not simultaneous routing feasibility. PB15 explicit access bridge 59 is not included in helper route metric; add its own length and 2 vias when comparing physical whole paths.')
 d=load(P/f'GPIO_PB1_inward_{v}_80_delta.json');ck=load(P/f'GPIO_PB1_inward_{v}_80_check.json');src=next(z for z in load(P/f'GPIO_PB1_inward_{v}_80_snapshot.json')['vias']if z['net']=='GPIO_PB1'and z['xy']==[41.9,26.79]);entries['manualPB1Inward80']=dict(status='LOCAL_GEOMETRY_CANDIDATE_NOT_FULL_NET',allNewFeaturesContinuousCopperClear=all(c['clear']for c in ck),newPB1LengthToWestHookMM=sum(math.dist(a,b)for o in d if o['type']=='route'and o['net']=='GPIO_PB1'for a,b in zip(o['points'],o['points'][1:])),westernConnectedHook=[34.2,20],newBodyVia=src['xy'],newTinySignalViaCount=3,oldSignalViaRetired=[38.3,27.35],V3PTHold=[37,24],V3PTHnew=[37.2,24.3],V3ViaCountDelta=0,requires=['Parent geometric and PI/reference review','New all-layer tiny via approvals, inherited global classes unchanged','Old stitch aliases explicitly migrate and native all-pin edges remain','Native graph/DRC/fresh reopen/HSE negative/reference review','Full source hook to moved J12 terminal route'])
 out['variants'][v]=entries
out['jointBottleneck']='Several South native source accesses independently choose the same BOTTOM x36.4..36.8/y17.45 transition followed by TOP diagonal to x34.65/y15.3..15.7 and BOTTOM west toward new header. Actual UART_RXD/VBUS_PRESENT_N/CAN_RXD and source return copper constrain that narrow crossing; independent clear paths do not reserve simultaneous lanes. 72 bounded joint iterations did not converge and are not executable.'
out['next']='Pause global negotiated loops. Inspect actual TOP/BOTTOM coordinate preview; compare manual source/access corridor allocation, then route all 7 with explicit layer changes and actual return. No header relocation has been executed.'
f=P/'GPIO7_comparison_state_20261022.json';f.write_text(json.dumps(out,indent=2),encoding='utf8');print(json.dumps(out,indent=2))
