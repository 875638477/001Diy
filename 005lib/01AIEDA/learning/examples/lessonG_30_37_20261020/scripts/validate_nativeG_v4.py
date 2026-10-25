from pathlib import Path
import re,json,csv,hashlib,math
from collections import Counter
R=Path(r'D:\001DIY\005lib\01AIEDA\learning\examples\lessonG_30_37_20261020')
V=R/'review';V.mkdir(exist_ok=True)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest().upper()
def sx(s):
 t=re.findall(r'"(?:\\.|[^"\\])*"|\(|\)|[^\s()]+',s);i=0
 def take():
  nonlocal i
  v=t[i];i+=1
  if v=='(':
   q=[]
   while t[i]!=')':q.append(take())
   i+=1;return q
  if v.startswith('"'):return json.loads(v)
  if v=='nil':return None
  if v=='t':return True
  try:return float(v)
  except ValueError:return v
 return take()
def rows(p):return list(csv.DictReader(p.open(encoding='utf8'),delimiter='\t',quotechar='\0'))
def normstr(s):return re.sub(r'(?:dbid|propList):[0-9A-Fa-f]+','OBJECT',s)
def tabdict(p,keys):return {tuple(x[k] for k in keys):x for x in rows(p)}
def csets(p):return {(x['cset'],x['layer']):dict(sx(x['values'])) for x in rows(p)}
checks=[]
def check(label,ok,details=None):
 checks.append({'check':label,'pass':bool(ok),'details':details} if details is not None else {'check':label,'pass':bool(ok)})
plan=json.loads((R/'plans/placement_plan.json').read_text());planned={x['ref']:x for x in plan['placements']}
boards={}
for key,layers,nfilm,reference in [('4L',['TOP','L2','L3','BOTTOM'],17,'ETCH/L2'),('2L',['TOP','BOTTOM'],15,'ETCH/BOTTOM')]:
 B=R/f'logs/final_reopen_{key}_01';S=R/f'logs/inventory_{key}';board=R/f'current/G_{key}_LAYOUT_v1.brd'
 launch=json.loads((B/'launch.json').read_text());n=json.loads((R/f'inventory/normalized_actual_{key}.json').read_text())
 check(f'{key}.readonly_exit',launch['completed'] and launch['exitCode']==0 and launch['readonly'])
 check(f'{key}.readonly_hash',launch['beforeSHA256']==launch['afterSHA256']==sha(board))
 check(f'{key}.no_native_error','*Error*' not in (B/'stdout.txt').read_text())
 native=(B/'native_summary.txt').read_text();check(f'{key}.summary',all(x in native for x in ['components=80','nets=69','symbols=84','drcs=0','drcState=t']))
 ps=n['placements'];check(f'{key}.80_placed',len(ps)==80 and len({x['ref'] for x in ps})==80)
 for p in ps:
  target=planned[p['ref']]
  check(f'{key}.pose.{p["ref"]}',p['xy']==[target['x'],target['y']] and p['rotation']==target['rotation'] and not p['mirrored'])
 before={(x['refdes'],x['pin']):x['net'] for x in rows(S/'component_pins.tsv')}
 after={(x['refdes'],x['pin']):x['net'] for x in rows(B/'component_pins.tsv')}
 check(f'{key}.272_logical_pins',len(after)==272)
 for p,net in before.items():check(f'{key}.logical.{p[0]}.{p[1]}',after.get(p)==net)
 check(f'{key}.mechanical_4',len(n['mechanical'])==4)
 # Native board and keepin/keepout geometry remains byte identical (no process DBIDs in this TSV).
 for name in ['stackup_full.tsv','direct_geometry.tsv','outline_exact.tsv']:
  check(f'{key}.preserve.{name}',(B/name).read_bytes()==(S/name).read_bytes())
 stack=rows(B/'stackup_full.tsv');actual=[sx(x['name']) for x in stack if sx(x['conductor']) is True]
 check(f'{key}.exact_uppercase_layers',actual==layers,actual)
 check(f'{key}.zero_physical_mask',not any(sx(x['type'])=='SOLDERMASK' or (sx(x['name']) or '').upper().startswith('SOLDERMASK') for x in stack))
 films={sx(x['name']):sx(x['attributes']) for x in rows(B/'films_full.tsv')}
 orig={sx(x['name']):sx(x['attributes']) for x in rows(S/'films_full.tsv')}
 check(f'{key}.film_count',len(films)==nfilm)
 check(f'{key}.film_names',set(films)==set(orig))
 for name in orig:check(f'{key}.film_exact.{name}',films.get(name)==orig[name])
 # Full global constraint values are preserved in 4L; local exceptions are explicit copies.
 pc=csets(B/'physical_csets.tsv');sc=csets(B/'spacing_csets.tsv')
 if key=='4L':
  oldp=csets(S/'physical_csets.tsv');olds=csets(S/'spacing_csets.tsv')
  for ident,vals in oldp.items():
   for k,v in vals.items():check(f'{key}.global_physical.{ident[0]}.{ident[1]}.{k}',pc.get(ident,{}).get(k)==v)
  for ident,vals in olds.items():
   for k,v in vals.items():check(f'{key}.global_spacing.{ident[0]}.{ident[1]}.{k}',sc.get(ident,{}).get(k)==v)
  check(f'{key}.electrical_csets_preserved',(B/'electrical_csets.tsv').read_bytes()==(S/'electrical_csets.tsv').read_bytes())
  nr=tabdict(B/'net_rules.tsv',['net']);oldnr=tabdict(S/'net_rules.tsv',['net'])
  for net,old in oldnr.items():
   for field in ['spacingClass','electricalClass','props','inheritedMaxVia','inheritedPhase','inheritedUncoupled']:
    check(f'{key}.netrule.{net}.{field}',nr[net][field]==old[field])
   check(f'{key}.netrule.{net}.physicalClass',nr[net]['physicalClass']==('"G31_GND_P"' if net==('GND',) else old['physicalClass']))
  copies={'G31_POWER_ESCAPE':'P_POWER_060','G31_GND_ESCAPE':'P_GND_PLANE'}
  for layer in layers:
   expect=dict(sc['S_POWER_030',layer]);expect.update(smdpin_line=.2,line_line=.2)
   check(f'{key}.local_spacing_exact_copy_delta.{layer}',sc['G31_PIN_ESCAPE',layer]==expect)
 else:
  copies={'G31_POWER_ESCAPE':'G2L_POWER_DEMO','G31_GND_ESCAPE':'G2L_GND_DEMO'}
  for layer in layers:
   check(f'{key}.default_width.{layer}',pc['DEFAULT',layer]['width_min']==.2032 and pc['DEFAULT',layer]['neckwidth_min']==.2032)
   check(f'{key}.default_spacing.{layer}',sc['DEFAULT',layer]['line_line']==.16)
   for c in ['G2L_POWER_DEMO','G2L_GND_DEMO']:
    check(f'{key}.power_profile.{c}.{layer}',pc[c,layer]['width_min']==.6 and pc[c,layer]['neckwidth_min']==.25 and pc[c,layer]['necklength_max']==1)
 for new,copy in copies.items():
  for layer in layers:
   expect=dict(pc[copy,layer]);expect['necklength_max']=1.4
   check(f'{key}.local_physical_exact_copy_delta.{new}.{layer}',pc[new,layer]==expect)
 gm=rows(B/'group_members.tsv');classes={x['group'] for x in gm if sx(x['groupType'])=='NETCLASS'}
 membership=[x for x in gm if sx(x['groupType'])=='NETCLASS']
 check(f'{key}.classcount',len(classes)==(28 if key=='4L' else 2),len(classes))
 gndclass=[sx(x['member']) for x in gm if x['group']=='G31_GND_P']
 check(f'{key}.gndclass_only_GND',gndclass==['GND'])
 if key=='4L':
  check(f'{key}.all_domains_207_members',len(membership)==207)
  for domain in ['physical','spacing','electrical']:
   nn=Counter(sx(x['member']) for x in membership if sx(x[domain]))
   check(f'{key}.all69_once_{domain}',len(nn)==69 and set(nn.values())=={1})
 proof=(B/'g_final_connectivity_constraints.txt').read_text()
 check(f'{key}.8_connected_targets',proof.count('targetReached=t')==8 and 'targetReached=nil' not in proof)
 check(f'{key}.4_ground_reference_proofs',proof.count('NATIVE_REFERENCE_REACHED')==4 and f'"{reference}"' in proof)
 check(f'{key}.proof_complete','G_FINAL_NATIVE_PROOF_COMPLETE' in proof and 'DYNAMIC_OOD=0' in proof)
 check(f'{key}.three_TOP_regions',proof.count('REGION_SHAPE ')==3 and proof.count('layer "CONSTRAINT REGION/TOP"')==3)
 check(f'{key}.actual_ground_polygon',len(n['planes'])==1 and n['planes'][0]['layer']==reference and n['planes'][0]['net']=='GND' and n['planes'][0]['filled'] and not n['planes'][0]['boundary'])
 check(f'{key}.ground_voids_exported',len(n['planes'][0]['holes'])>0)
 check(f'{key}.via_count_4',len(n['vias'])==4 and 'UNIQUE_VIA_COUNT\t4' in (B/'specific_proof.tsv').read_text())
 for v in n['vias']:
  check(f'{key}.via.{v["xy"]}',v['padstack'].upper()=='L28_VIA030_C060' and v['net']=='GND')
 routes=n['routes'];top=[x for x in routes if x['layer']=='ETCH/TOP']
 check(f'{key}.manual_TOP_segments27',len(top)==27,len(top))
 check(f'{key}.only_local_power_routes',all(x['net'] in ['V3V3','GND'] for x in top))
 check(f'{key}.no_outside_challenge_leak',all(max(p[1] for p in x['startEnd'])<40 for x in top))
 ex=R/f'logs/exercises_{key}_03';et=(ex/'operation_exercises.txt').read_text();el=json.loads((ex/'launch.json').read_text())
 check(f'{key}.exercise_complete','G_NATIVE_EXERCISES_COMPLETE' in et and 'ALL80_POSES_RESTORED_EXACTLY' in et and 'C13=((33.9 24.0984)' in et)
 check(f'{key}.exercise_file_unchanged',el['beforeSHA256']==el['afterSHA256'] and '*Error*' not in (ex/'stdout.txt').read_text())
 ch=R/f'logs/freeze_{key}_02/local_rule_challenges.txt';ct=ch.read_text()
 check(f'{key}.challenges_complete','G_RULE_CHALLENGES_COMPLETE_NO_SAVE' in ct and 'DRC_STATUS\tCHALLENGES_RESTORED\t0\tt' in ct)
 check(f'{key}.neck_challenge12','DRC_STATUS\tLOCAL_NECK_STRICT_1MM\t12\tt' in ct)
 check(f'{key}.outside_global_challenge','OUTSIDE_LINE_SPACING_COUNT=1 OUTSIDE_MAX_NECK_COUNT=1' in ct)
 if key=='4L':check(f'{key}.local_spacing_challenge30','DRC_STATUS\tLOCAL_SPACING_STRICT_030\t30\tt' in ct)
 boards[key]={'path':str(board),'sha256':sha(board),'readback':str(B),'normalized':str(R/f'inventory/normalized_actual_{key}.json'),'placed':80,'logicalPins':272,'nets':69,'drcCount':0,'actualLayers':actual,'physicalMaskRows':0,'filmCount':len(films),'referenceLayer':reference,'generatedGroundShapes':len(n['planes']),'dynamicOutOfDate':0,'manualTopSegments':len(top),'thermalReferenceSegments':len(routes)-len(top),'vias':len(n['vias']),'netclasses':len(classes),'classMembers':len(membership),'couponConnectivity':{'pinCapTargetProofs':8,'groundReferenceProofs':4},'exceptions':{'region':'G31_U1_ESCAPE','shapeCount':3,'layer':'CONSTRAINT REGION/TOP','necklengthNativeMM':1.4,'physicalCSetsCopiedFrom':copies,'widthMM':.6,'neckWidthMM':.25,'outsideRegionNeckLimitMM':1.0,'spacingOnly4L':({'smdpin_line':.2,'line_line':.2} if key=='4L' else None)}}
boards['2L']['independentRuleProfile']={'defaultWidthMM':.2032,'defaultNeckWidthMM':.2032,'defaultCopperSpacingMM':.16,'localPowerGroundSpacingMM':.2,'powerGroundWidthMM':.6,'powerGroundNeckWidthMM':.25,'powerGroundNeckMaxOutsideRegionMM':1.0,'localEscapeNeckMaxMM':1.4,'approvedVia':'L28_VIA030_C060','scope':'Explicit V3V3/GND demo net rules and 2 new physical classes; source4L class scheme, inner-layer exceptions and USB rules were not copied.'}
boards['4L']['classChanges']={'before':27,'after':28,'newPhysicalClass':'G31_GND_P','member':['GND'],'removedFromPhysicalClass':'NC_POWER_LV_P','unchangedSpacingClass':'NC_POWER_LV_S','unchangedElectricalClass':'NC_POWER_LV_E','retainedNetOverride':'P_GND_PLANE','domainMembershipTotal':207}
twonets=rows(R/'logs/final_reopen_2L_01/net_rules.tsv')
for r in twonets:
 if r['net'] not in ['V3V3','GND']:
  check(f'2L.remaining67_default_only.{r["net"]}',all(sx(r[k]) is None for k in ['physicalClass','spacingClass','electricalClass']) and all(k not in r['props'] for k in ['PHYSICAL_CONSTRAINT_SET','SPACING_CONSTRAINT_SET','ELECTRICAL_CONSTRAINT_SET']))
boards['2L']['independentRuleProfile']['remaining67Nets']='No per-net CSet override or netclass; only DEFAULT width .2032mm and copper spacing .16mm. This is incomplete full-board power/signal rule classification.'
inputs=json.loads((R/'source/input_manifest.json').read_text())[:2]
sourceChecks=[]
for x in inputs:
 ok=sha(Path(x['source']))==sha(Path(x['copy']))==x['sha256']
 check('original_input_hash.'+Path(x['source']).name,ok)
 sourceChecks.append({'source':x['source'],'snapshot':x['copy'],'sha256':x['sha256'],'unchanged':ok})
tech=json.loads((R/'exports/export_result.json').read_text())
for key in ['4L','2L']:
 for rec in tech['boards'][key]['records']:check(f'{key}.official_TCF_{rec["step"]}',rec['exitCode']==0 and rec['boardBefore']==rec['boardAfter']==boards[key]['sha256'])
 check(f'{key}.TCF_compare_no_objects_updated','No objects were updated.' in (R/f'exports/techfile_{key}/compare_techfile.log').read_text())
fail=[x for x in checks if not x['pass']]
validation={'status':'PASS_NATIVE_G_LAYOUT_VALIDATION' if not fail else 'FAIL_NATIVE_G_LAYOUT_VALIDATION','checks':len(checks),'failures':len(fail),'failedChecks':fail,'results':checks}
(V/'native_validation.json').write_text(json.dumps(validation,indent=2),encoding='utf8')
report={'status':'PASS_NATIVE_G_LAYOUT_AND_LOCAL_DECOUPLING' if not fail else 'FAIL_NATIVE_VALIDATION','scope':'80 component placements on two controlled 2L/4L variants plus 3 local VDD/VSS decoupling circuits and C16 branches; not full-board routing or manufacturing release. Native CLI/SKILL practice, not GUI practice.','boards':boards,'operationExercises':{'move':True,'rotate':True,'originYAlign':True,'genericGroupDirectTransformAfterDBRefresh':True,'all80PoseRollbackExact':True,'scope':'temporary transactional exercises, file hashes unchanged'},'sourceHashesUnchanged':sourceChecks,'constraintSemantics':'G31 CSets are copies of the named template CSet, not dynamically inheriting parents. All copied key/layer values are independently compared, with only explicit neck/spacing changes. Physical GND class split is an intentional metadata change.','validation':{'path':str(V/'native_validation.json'),'checks':len(checks),'failures':len(fail)},'failedAttempts':[{'log':'logs/place_4L_v1','issue':'parent component symbol cache required axlDBRefreshId after native creates; no output saved'},{'log':'logs/reopen_4L_v1','issue':'C8 pad spacing .1773 under .2; corrected real placement'},{'log':'logs/reconcile_4L_01','issue':'C9 rotation exposed NC pad copper gap .1374 under .2; shifted +.2x'},{'log':'logs/loops_4L_01','issue':'pad-edge start had no native pin attach and 30 spacing DRC; not saved'},{'log':'logs/loops_4L_02','issue':'pin-center attach counted 1.3657 neck; BFS shape/line result-list normalization failed; not saved'},{'log':'logs/loops_4L_03','issue':'pad-edge+overlap DRC0 still not native pin attached; not saved'},{'log':'logs/loops_4L_04','issue':'axlNetClassGet requires 3 arguments; not saved'},{'log':'logs/bulk_4L_01','issue':'bulk was successfully saved DRC0 before optional proof wrong API capitalization; corrected final readonly proof'},{'log':'logs/exercises_2L_02','issue':'generic transform worked but stale member cache caused false negative; second batch doubled movement, transaction automatically cancelled; no save'},{'log':'logs/freeze_4L_01','issue':'post-DRC cache stale after restoring spacing; fixed refresh before assertions; no frozen output saved'}],'limitations':['Same 80 coordinate plan for 2L and 4L is a controlled comparison, not two independently optimized complete layouts.','Only three decoupling VDD/VSS circuits and C16 bulk branches are routed; LDO 3V3 feed, HSE, USB, switch-mode power, analog and all other nets remain to route.','Ground plane is a real dynamic filled polygon with clearance holes and thermals; 4L L3 remains unpoured.','VSS-to-cap HF connection is on TOP with one cap-side ground via per group to the reference; graph reachability does not prove current direction or a mandatory plane path.','Native center-based neck is 1.3657mm <= local1.4; 0.6mm lies inside the pin pad and external neck is0.7657mm. The original global1mm was not claimed to cover the whole center-based segment.','Unknown actual component heights and unselected MPNs are not certified by default package height; root geometry review covers avoiding the restricted-height zone.','USB90ohm geometry/factory release, final assembly variant, thermal/current capacity, full-route return paths and EMI review remain subsequent engineering gates.','Film definitions remain exact to user templates; existing invalid references/filtering and missingREFDES silkscreen template issue are historical known boundaries, not production CAM certification.','No native GUI workflow, independent SI/PI waveform simulation, fabrication output CAM audit or board manufacturing release was performed.']}
(V/'native_final_report.json').write_text(json.dumps(report,indent=2),encoding='utf8')
print(json.dumps({'status':report['status'],'checks':len(checks),'failures':len(fail),'failedChecks':fail,'boards':{k:{'sha256':v['sha256'],'manualTopSegments':v['manualTopSegments'],'netclasses':v['netclasses']} for k,v in boards.items()}},indent=2))
