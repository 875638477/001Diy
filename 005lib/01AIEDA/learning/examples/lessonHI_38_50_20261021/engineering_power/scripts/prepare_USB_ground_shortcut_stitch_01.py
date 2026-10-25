from pathlib import Path
import sys,json,math
H=Path(r'D:/001DIY/005lib/01AIEDA/learning/examples/lessonHI_38_50_20261021');O=H/'engineering_power';sys.path[:0]=[str(H/'scripts'),str(O/'scripts'),str(H/'tooling/packages')]
from routing_geometry import *
cp=H/'inventory/checkpoints/padentry_2L_b019_DRC_PENDING';n=load(cp/'normalized.json');w=load(cp/'networks.json');r=load(cp/'base_net_rules.json');p=load(O/'N49_2L_policy.json');p['pendingOperations']=[];s=CopperScene(n,w,r,p);ground={l:[]for l in['TOP','BOTTOM']}
for a in n['planes']:
 if a['net']=='GND'and a.get('generated'):ground[a['layer'].removeprefix('ETCH/')].append(plane_from_native(dict(a,holes=a.get('holes')or[])))
for a in n['routes']:
 if a['net']=='GND'and not a.get('generatedThermal'):ground[a['layer'].removeprefix('ETCH/')].append(LineString(a['startEnd']).buffer(a['width']/2,quad_segs=24))
for a in s.obstacles:
 if a['net']=='GND'and a['kind']in['smdpin','thrupin','via']:ground[a['layer']].append(a['geometry'])
ground={l:unary_union(a)for l,a in ground.items()};xy=[42.35,17.0];disk=Point(xy).buffer(.3,quad_segs=64);wire=LineString([[41.97,17.6],[41.97,19.3]]).buffer(.125,quad_segs=24)
evidence={l:dict(diskAreaMM2=disk.area,currentCommonCopperIntersectionMM2=disk.intersection(g).area,fullDiskCovered=g.buffer(.0001).covers(disk),candidateStitchNotYetNative=True)for l,g in ground.items()};evidence['narrowActualTOPcorridor']=dict(geometry=[[41.97,17.6],[41.97,19.3]],testWidthMM=.25,actualCommonCovered=ground['TOP'].buffer(.0001).covers(wire),missingAreaMM2=wire.difference(ground['TOP']).area,meaning='A testwindowonly,notachosennewtraceortotalreturnpath')
plan=dict(status='READ_ONLY_DERIVED_SINGLE_STITCH_COMPARISON_NOT_NATIVE',batchId='USB_COMMON_RETURN_STITCH_2L_01',variant='2L',sourceExpectedSHA256=w['sha256'],operations=[dict(type='via',id='USB_COMMON_RETURN_SHORTCUT_STITCH',net='GND',xy=xy,padstack='L28_VIA030_C060',purpose='JoinexistingactualTOPgroundcorridorbetweenR5/R12totheBOTTOMgroundsouthofATTACHslot; nativeC1.2common/actualCuandshortenedlocalreturnmustbeproved')],placementChanges=[],constraintOperations=[],connectivityProofs=[dict(id='USB_RETURN_NEW_STITCH_C1_COMMON',**{'from':'C1.2'},toAlias='USB_COMMON_RETURN_SHORTCUT_STITCH',connected=True),dict(id='USB_RETURN_STITCH_C14',**{'from':'C14.2'},toAlias='USB_COMMON_RETURN_SHORTCUT_STITCH',connected=True)],geometryEvidence=evidence,pending=['FullallfieldspacingprecheckandSouthfuturemerge','NochangecriticalUSB/C14/HSE/controlsourceorP/S/Ebudgets; globalstockviaalreadyapproved','ActualpostfillGNDallpins/vias/shapes/health/oldedges/HSEnegative','ReturncorridormeshcomparisonisnotHFsolutionor90ohmcertification'])
file=O/'USB_COMMON_RETURN_STITCH_2L_01.json';file.write_text(json.dumps(plan,indent=2)+'\n');print(json.dumps(evidence))
