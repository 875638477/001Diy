"""Read native exports only; write training assembly CSVs and explicit instance-correction contracts."""
from pathlib import Path
import json,csv,re,hashlib,math,collections,sys,xml.sax.saxutils as xml
R=Path('D:/001DIY/005lib/01AIEDA'); J=R/'learning/examples/lessonJK_51_59_20261022'; H=R/'learning/examples/lessonHI_38_50_20261021'; D=R/'learning/examples/de_15_26_20261019'
STATUS='TRAINING_NOT_FOR_ASSEMBLY'
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest().upper()
def load(p):return json.loads(Path(p).read_text(encoding='utf-8-sig'))
def dump(p,x):Path(p).write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def csvout(p,rows,fields=None):
 rows=list(rows);fields=fields or list(rows[0]);
 with Path(p).open('w',encoding='utf-8-sig',newline='') as f:
  w=csv.DictWriter(f,fieldnames=fields,extrasaction='raise');w.writeheader();w.writerows(rows)
 with Path(p).open(encoding='utf-8-sig',newline='') as f:
  got=list(csv.DictReader(f));assert len(got)==len(rows);assert set(got[0])==set(fields) if got else True
 return got
def sx(s):
 ts=re.findall(r'"(?:\\.|[^"\\])*"|\(|\)|[^\s()]+',s);i=0
 def take():
  nonlocal i
  v=ts[i];i+=1
  if v=='(':
   out=[]
   while ts[i]!=')':out.append(take())
   i+=1;return out
  if v.startswith('"'):return json.loads(v)
  if v=='nil':return None
  if v=='t':return True
  try:return float(v)
  except ValueError:return v
 out=take();assert i==len(ts);return out
def rawrows(p):return list(csv.DictReader(Path(p).open(encoding='utf-8-sig'),delimiter='\t',quotechar='\0'))
def srows(p):return [{k:sx(v) for k,v in x.items()} for x in rawrows(p)]
def sortref(s):return (re.sub(r'\d','',s),int(''.join(re.findall(r'\d',s)) or '0'))
def attrs(a):return dict(zip(a[::2],a[1::2])) if a else {}
def heights(p):
 return [dict(g['props'] or []) for g in p['geometry'] if g['layer']=='PACKAGE GEOMETRY/PLACE_BOUND_TOP']
def textsel(t):return {k:t.get(k) for k in ('layer','text','xy','rotation','mirrored','justify','textBlock','bbox')}
req=['REF DES/SILKSCREEN_TOP','REF DES/ASSEMBLY_TOP','COMPONENT VALUE/ASSEMBLY_TOP']
spec=load(D/'integrated_circuit.json');cs={c['ref']:c for c in spec['components']};assert len(cs)==80
basebom={r['Reference']:r for r in csv.DictReader((D/'BOM_baseline.csv').open(encoding='utf-8-sig'))};assert set(basebom)==set(cs)
pst=D/'native_flow_final/baseline/netlist';a4=R/'learning/staging/a4_review_20261019/packaging/netlist'
def parsepst(root):
 parts=dict(re.findall(r"PART_NAME\s+(\S+)\s+'([^']+)'",(root/'pstxprt.dat').read_text()))
 prim={}
 for name,body in re.findall(r"primitive\s+'([^']+)';(.*?)end_primitive;",(root/'pstchip.dat').read_text(),re.S):
  b=re.search(r'\bbody\s+(.*?)end_body;',body,re.S).group(1);prim[name]=dict(re.findall(r"(\w+)='([^']*)'",b))
 return parts,prim
pp,pr=parsepst(pst);ap,ar=parsepst(a4);assert len(pp)==len(ap)==80
sources=[D/'integrated_circuit.json',D/'BOM_baseline.csv',R/'learning/notes/record_location_rules.md',R/'learning/notes/lessonF_source_corrections_20261019.md',R/'learning/staging/a4_review_20261019/pst_compare.json']+[p/f for p in [pst,a4] for f in ['pstxprt.dat','pstchip.dat','pstxnet.dat']]
issues=[]
def issue(id,title,scope,kind,evidence,action):issues.append(dict(issueID=id,title=title,scope=scope,status=kind,evidence=evidence,nextAction=action))
issue('JK57-001','采购料号及生产旋转标准未定','BOTH','OPEN_RELEASE',{'mpnSpecified':12,'mpnPending':68},'逐件定MPN并与装配厂确认封装零度、吸取中心和顶底镜像转换；当前CSV保留CAD原点/原生角度。')
issue('JK57-002','默认USB和CAN备选料互斥','BOTH','OPEN_RELEASE',spec['assembly_profiles'],'本轮输出默认USB：R5/R6装22R，R12/R13 DNP；22R为历史工程值，未硬件验证；CAN配置只能受控另出BOM和固件。')
issue('JK55-005','USB安装脚长与约1.6mm板厚装配尚未匹配','BOTH','OPEN_RELEASE',{'connector':'USB4105-GF-A','stakeLengthBelowSeatingPlaneMM':'0.95 ±0.15','note':str(R/'learning/notes/lessonF_source_corrections_20261019.md')},'确认座高/成品板厚公差/壳脚焊接工艺，不将S误解为板底突出量。')
issue('JK55-006','USB两层阻焊桥0.100mm小于所选公开目标0.1016mm','2L','OPEN_RELEASE',{'nominalMaskBridgeMM':.1,'publicMinimumMM':.1016},'与板厂确认可行工艺或受控改开窗/厂商；不能以差1.6um忽略。')
issue('JK55-007','DNP焊盘仍在原生钢网定义中','BOTH','OPEN_PROCESS',{'DNP':['R12','R13']},'根据不装位焊料策略决定是否屏蔽钢网开口；当前全PAD钢网并非已批准装配变体。')
issue('JK55-008','默认高度和PlaceBound不等实物尺寸','BOTH','OPEN_RELEASE',{'defaultHeightMM':1,'heightSource':'User default / existing explicit library properties'},'1mm缺省只代表教学占位；68件无MPN及实际courtyard/连接器插拔/装配公差仍待核，不把PlaceBound叫真实器件body。')
issue('JK55-009','测试点/极性/定位与生产装配输出待确认','BOTH','OPEN_RELEASE',{'dedicatedTestPointApproval':False},'导出每件pin1实际坐标并按原理图极性核对；排针/裸pad不能自动作为量产探针方案；需测试夹具/接触/可达性。')
allbom=[];plans={};summ={};allchecks=[]
for v in ['2L','4L']:
 C=H/f'inventory/checkpoints/padentry_{v}_b019_DRC_PENDING';S=load(C/'normalized.json');L=Path(S['readbackDirectory']);B=H/f'native_candidates/HI_{v}_padentry_normalized_b019_DRC_PENDING.brd'
 sources += [C/'normalized.json',C/'networks.json',C/'base_net_rules.json',B]+[L/f for f in ['components.tsv','board_instance_texts.tsv','g_actual_symbols.tsv','g_package_geometry.tsv','placed_pins.tsv','physical_pad_layers.tsv','hi_mechanical_pins.tsv','mechanical_direct.tsv','films_full.tsv','stackup_full.tsv','structure.txt']]
 P={p['ref']:p for p in S['placements']};assert set(P)==set(cs);comp={r['refdes']:r for r in rawrows(L/'components.tsv')};assert set(comp)==set(P)
 check=[]
 for ref,c in cs.items():
  p=P[ref];pn=pp[ref];native=comp[ref]['deviceType'];b=pr[pn]
  check.append(dict(ref=ref,pstPrimitive=pn,nativePrimitive=native,primitiveMatch=pn.upper()==native.upper(),value=b['VALUE'],nativeMetadataValue=p['value'],valueMatch=b['VALUE'].upper()==p['value'].upper(),package=b['JEDEC_TYPE'],nativePackage=p['package'],packageMatch=b['JEDEC_TYPE'].upper()==p['package'].upper(),a4Match=ar[ap[ref]]['VALUE'].upper()==b['VALUE'].upper() and ar[ap[ref]]['JEDEC_TYPE'].upper()==b['JEDEC_TYPE'].upper()))
 assert all(x[k] for x in check for k in ['primitiveMatch','valueMatch','packageMatch','a4Match']);dump(J/f'audits/j57_{v}_pst_identity_b019.json',check);allchecks+=check
 placed=srows(L/'placed_pins.tsv');proc=[];bom=[];co=[];ta=[];ha=[];fix=[];missing=collections.Counter();off=collections.Counter();hm=0;fitcounts=collections.Counter()
 for ref in sorted(P,key=sortref):
  p=P[ref];c=cs[ref];bm=basebom[ref];pins=[x for x in placed if x['refdes']==ref and not x['mechanical']];th=[x for x in pins if x['through']];sm=[x for x in pins if not x['through']]
  process='MIXED_SMD_PTH' if th and sm else 'THROUGH_HOLE' if th else 'SMD';dn=ref in ['R12','R13'];populate='DNP' if dn else 'FIT';smt='EXCLUDE_DNP' if dn else 'EXCLUDE_THT_FROM_SMT' if process=='THROUGH_HOLE' else 'SMT_CANDIDATE_REVIEW_REQUIRED'
  hs=heights(p);maxs=[z['PACKAGE_HEIGHT_MAX'] for z in hs if 'PACKAGE_HEIGHT_MAX' in z];hval=maxs[0] if maxs else '';hm+=not bool(maxs)
  side='BOTTOM' if p['mirrored'] else 'TOP';rot=p['rotation'];pin1=next((q for q in p['pins'] if q['number']=='1'),None)
  if not pin1 and ref=='J2':pin1=next(q for q in p['pins'] if q['number']=='A1_B12')
  row=dict(Status=STATUS,Reference=ref,Value=p['value'],Model=c['model'],MPN=c['mpn'],Procurement_Status=c['properties']['MPN_STATUS'],Specification=bm['Specification'],Requirements=bm['Requirements'],Package=p['package'],Assembly_USB=populate,Assembly_CAN='DNP' if ref in ['R5','R6'] else 'FIT' if ref in ['R12','R13'] else populate,Process=process,SMT_Handling=smt,Page=c['page'],CAD_Height_Max=hval,Height_Status='EXPLICIT_CAD_NOT_ASSEMBLY_APPROVAL' if hval else 'MISSING_DEFAULT_1MM_REQUIRED')
  bom.append(row);fitcounts[(populate,process)]+=1
  co.append(dict(Status=STATUS,Variant=v,Reference=ref,Value=p['value'],Package=p['package'],X_mm=p['xy'][0],Y_mm=p['xy'][1],Units='mm',Origin='CAD_DATABASE_X0_Y0',Position_Meaning='SYMBOL_ORIGIN_NOT_VERIFIED_PICK_CENTRE',Side=side,CAD_Rotation_deg=rot,Rotation_Convention='CAD_NATIVE_CCW_FROM_PACKAGE_ZERO_TOP_VIEW',Assembly_Factory_Rotation_deg='',Rotation_Status='FACTORY_MAPPING_PENDING',Pin1_ID=pin1['number'] if pin1 else '',Pin1_X_mm=pin1['xy'][0] if pin1 else '',Pin1_Y_mm=pin1['xy'][1] if pin1 else '',Assembly_USB=populate,Process=process,SMT_Handling=smt,Source_BRD_SHA256=sha(B)))
  ts=p['texts'];ra=[t for t in ts if t['layer']==req[1]];assert len(ra)==1;template=ra[0];targets=[]
  for layer in req:
   tt=[t for t in ts if t['layer']==layer];exp=p['value'] if layer.startswith('COMPONENT VALUE/') else ref
   match=[t for t in ts if t['layer']=='COMPONENT VALUE/SILKSCREEN_TOP'] if layer.startswith('COMPONENT VALUE/') and not tt else []
   assert len(tt)<=1 and len(match)<=1
   old=tt[0] if tt else match[0] if match else None
   action='UPDATE_EXISTING' if tt else 'MIGRATE_VALUE_FROM_SILK' if match else 'CREATE_FROM_REFDES_STYLE'
   tar=dict(layer=layer,text=exp,xy=p['xy'],rotation=rot,mirrored=bool(p['mirrored']),justify=(old or template)['justify'],textBlock=(old or template)['textBlock'])
   targets.append(dict(action=action,oldSelector=textsel(old) if old else None,styleTemplateSelector=textsel(old or template),target=tar))
   if not tt:missing[layer]+=1
   if tt and math.dist(tt[0]['xy'],p['xy'])>.00001:off[layer]+=1
   ta.append(dict(Variant=v,Reference=ref,Package=p['package'],RequiredLayer=layer,Present=bool(tt),Text=tt[0]['text'] if tt else '',ExpectedText=exp,AnchorX_mm=p['xy'][0],AnchorY_mm=p['xy'][1],TextX_mm=tt[0]['xy'][0] if tt else '',TextY_mm=tt[0]['xy'][1] if tt else '',Offset_mm=round(math.dist(tt[0]['xy'],p['xy']),6) if tt else '',TextCorrect=bool(tt and tt[0]['text']==exp),TextBlock=tt[0]['textBlock'] if tt else '',Justify=tt[0]['justify'] if tt else '',CurrentRotation=tt[0]['rotation'] if tt else '',TargetRotation=rot,Result='PASS' if tt and tt[0]['text']==exp and math.dist(tt[0]['xy'],p['xy'])<.00001 and tt[0]['rotation']==rot else 'NEEDS_INSTANCE_CORRECTION'))
  fix.append(dict(ref=ref,package=p['package'],originXY=p['xy'],rotation=rot,mirrored=bool(p['mirrored']),texts=targets,removeAnyRemainingComponentValueSilk=True,preservePackageGeometrySilkText=True,height=dict(action='PRESERVE_EXPLICIT' if maxs else 'ADD_DEFAULT_ON_EXISTING_PLACE_BOUND',existingPlaceBounds=[dict(type=g['type'],bbox=g['bbox'],props=g['props'],vertices=g['vertices']) for g in p['geometry'] if g['layer']=='PACKAGE GEOMETRY/PLACE_BOUND_TOP'],targetMax='1 MM' if not maxs else maxs[0],meaning='USER_DEFAULT_PLACEHOLDER_NOT_VERIFIED_PHYSICAL_HEIGHT' if not maxs else 'EXISTING_EXPLICIT_CAD_HEIGHT_PRESERVED')))
  ha.append(dict(Variant=v,Reference=ref,Package=p['package'],CAD_Max=hval,Target_Max=hval or '1 MM',Action='PRESERVE_EXPLICIT' if maxs else 'ADD_USER_DEFAULT',MPN=c['mpn'],Physical_Height_Approval='PENDING',PlaceBound_Is='NATIVE_PLACEMENT_ENVELOPE'))
 assert len(bom)==len(co)==len(fix)==80
 csvout(J/f'assembly/BOM_80_{v}_b019_TRAINING.csv',bom);csvout(J/f'assembly/coordinates_all80_{v}_b019_TRAINING.csv',co)
 csvout(J/f'assembly/SMT_candidates_{v}_b019_TRAINING.csv',[r for r in co if r['SMT_Handling']=='SMT_CANDIDATE_REVIEW_REQUIRED'])
 csvout(J/f'assembly/non_SMT_and_DNP_{v}_b019_TRAINING.csv',[r for r in co if r['SMT_Handling']!='SMT_CANDIDATE_REVIEW_REQUIRED'])
 groups=collections.defaultdict(list)
 groupfields=['Value','Model','MPN','Procurement_Status','Specification','Requirements','Package','Assembly_USB','Assembly_CAN','Process','SMT_Handling']
 for row in bom:groups[tuple(row[k] for k in groupfields)].append(row['Reference'])
 grouped=[dict(Status=STATUS,References=' '.join(sorted(refs,key=sortref)),Quantity=len(refs),**dict(zip(groupfields,key))) for key,refs in groups.items()];assert sum(x['Quantity'] for x in grouped)==80
 csvout(J/f'assembly/BOM_grouped_{v}_b019_TRAINING.csv',grouped);csvout(J/f'audits/j55_{v}_three_texts_b019.csv',ta);csvout(J/f'audits/j55_{v}_height_b019.csv',ha)
 films=srows(L/'films_full.tsv');fs={r['name']:attrs(r['attributes']) for r in films};dump(J/f'audits/j55_57_{v}_film_scope_b019.json',fs)
 mech=[{k:x.get(k) for k in ['symbol','refdes','pin','padstack','xy','through','mechanical','holeType','plating','drillDiameter','drillX','drillY']} for x in S['mechanicalPins']];dump(J/f'assembly/mechanical_NPTH_{v}_b019_TRAINING.json',dict(status=STATUS,excludedFromBOMAndPickPlace=True,count=len(mech),holes=mech))
 dump(J/f'audits/j55_57_{v}_hole_inventory_b019.json',dict(status=STATUS,logicalComponentCount=80,logicalPins=sum(int(r['pins']) for r in comp.values()),allPlacedPinRows=len(placed),mechanicalNPTH=mech,electricalDrilledPins=[p for p in placed if p['through'] and not p['mechanical']],viaCounts=collections.Counter(x['padstack'] for x in S['vias']),viaDrillMM=sorted({x['drill'] for x in S['vias']})))
 plans[v]=dict(inputBoard=str(B),inputSHA256=sha(B),normalized=str(C/'normalized.json'),nativeTextExport=str(L/'board_instance_texts.tsv'),instances=fix)
 summ[v]=dict(components=80,textInstances=sum(len(p['texts']) for p in P.values()),missingRequiredTexts=dict(missing),offsetRequiredTexts=dict(off),heightMissing=hm,heightExplicit=80-hm,fitProcessCounts={str(k):val for k,val in fitcounts.items()},groupedBOMRows=len(grouped),coordinatesAll=80,smtCandidateCount=sum(r['SMT_Handling']=='SMT_CANDIDATE_REVIEW_REQUIRED' for r in co),mechanicalNPTH=len(mech),films=len(films),sourceSHA256=sha(B))
 issue('JK55-001','三文字层缺失',v,'CORRECTION_READY',dict(missing),'按逐实例修正合同添加/迁层，保留普通PACKAGE GEOMETRY丝印极性字。')
 issue('JK55-002','必要文字锚点偏离器件原点',v,'CORRECTION_READY',dict(off),'原生实例更正xy/rotation/mirror，保持textBlock和justify；重开读回240个三文字锚点。')
 issue('JK55-003','72件缺省高度未实际写入',v,'CORRECTION_READY',{'missingCount':hm,'explicitCount':80-hm},'只向缺失PlaceBound添加1MM占位，保留8件明确高度及MIN属性。')
 issue('JK57-003','原01env PDFTOP并非完整装配图',v,'OPEN_PROCESS',{'PDFTOPGroups':fs['PDFTOP']['groupMembers']},'原Film保留；JK独立装配输出另包含PACKAGE GEOMETRY/ASSEMBLY_TOP、REF DES/ASSEMBLY_TOP、COMPONENT VALUE/ASSEMBLY_TOP及板框/孔，不称旧PDFTOP已输出value。')
 # Independent training vector view. Rendered labels are review callouts, not native Cadence font glyphs.
 lines=['<svg xmlns="http://www.w3.org/2000/svg" width="1440" height="1050" viewBox="-6 -10 96 80">','<rect x="-6" y="-10" width="96" height="80" fill="white"/>',f'<text x="0" y="-6" font-size="2" fill="#a00000">{v} b019 TRAINING_NOT_FOR_ASSEMBLY</text>','<text x="0" y="-3" font-size="1.1">CAD origin, mm, top view; labels are review callouts; not a native assembly film.</text>','<g transform="translate(0,60) scale(1,-1)">','<path d="M2 0 H78 L80 2 V58 L78 60 H2 L0 58 V2 Z" fill="#f9fafb" stroke="#111" stroke-width=".15"/>']
 for x in S['mechanicalPins']:
  xx,yy=x['xy'];lines.append(f'<circle cx="{xx}" cy="{yy}" r="{x["drillDiameter"]/2}" fill="white" stroke="#111" stroke-width=".1"/>')
 for ref in sorted(P,key=sortref):
  p=P[ref];box=p['bodyExtent'];color='#b45309' if ref in ['R12','R13'] else '#0369a1';x,y=p['xy'];
  lines.append(f'<rect x="{box[0][0]}" y="{box[0][1]}" width="{box[1][0]-box[0][0]}" height="{box[1][1]-box[0][1]}" fill="none" stroke="{color}" stroke-width=".09"/>')
  lines.append(f'<path d="M{x-.25} {y} h.5 M{x} {y-.25} v.5" stroke="#c40000" stroke-width=".09"/>')
  lines.append(f'<text transform="translate({x},{y}) scale(1,-1)" font-family="Arial" font-size=".85" text-anchor="middle" fill="{color}">{xml.escape(ref)}</text>')
 lines += ['</g>','<text x="0" y="66" font-size="1.1">Blue: placed footprint envelope. Brown: USB-profile DNP. Red cross: actual symbol origin.</text>','<text x="0" y="68" font-size="1.1">All 80 components retained. NPTH 6 holes are separate. Heights / MPN / factory rotation remain open.</text>','</svg>'];(J/f'assembly/assembly_review_{v}_b019_TRAINING.svg').write_text('\n'.join(lines),encoding='utf-8')
# Delta never uses stale dbid across processes. Resolve each oldSelector inside current process; fail on nonunique.
dump(J/'audits/j55_instance_correction_delta_b019.json',dict(status='READY_FOR_JK_COPY_NATIVE_INSTANCE_CORRECTION',purpose=STATUS,inputProtection='Never modify HI b019, public library or 01env. All mutations only on JK copies.',selectorPolicy='Exact ref+package+layer+text+xy+rotation+textBlock+justify; runtime dbid must be resolved and logged uniquely in current native process; source export contains only parent dbid, not stable text id.',preserve=['80 component identities','272 electrical pin mappings','all source placement anchors/rotations/mirroring','all routes/vias/copper including HSE single-anchor topology','stackup','Film definitions','public symbol definitions and source files'],postconditions=['Each of80 instances has exactly one required text per required layer; native xy equals symbol origin, actual ref/value correct; rotation/mirror follow instance; original style textBlock/justify retained.','No COMPONENT VALUE/SILKSCREEN_TOP remains. Preserve PACKAGE GEOMETRY silk pin/polarity symbols.','Add user1MM height only to72 missing actual shape PlaceBounds; preserve8 explicit shape maxima, existing minima, and4 legacy PlaceBound paths without assigning new height.','Reopen native process, read exact text fields/PlaceBound properties and compare source invariant geometry/net/route/pad/plane data; report any automatic shape refresh separately.'],variants=plans,baselineSummary=summ))
dump(J/'audits/j55_57_issues_b019.json',dict(status=STATUS,issues=issues))
dump(J/'audits/j55_57_summary_b019.json',dict(status=STATUS,summary=summ,pstBOMIdentityChecks=len(allchecks)*4,course55='INSTANCE_CORRECTION_READY_MANUFACTURING_OPEN',course57='TRAINING_CSV_EXPORTED_FACTORY_MAPPING_OPEN',sourceHashes=[dict(path=str(p),sha256=sha(p)) for p in sorted(set(sources))]))
print(json.dumps(summ,indent=2));print('outputs',len(list((J/'assembly').glob('*'))),'assembly items; correction contract ready')
