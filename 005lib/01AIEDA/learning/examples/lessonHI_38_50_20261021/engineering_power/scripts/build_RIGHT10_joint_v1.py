from pathlib import Path
import json,math,sys
H=Path(r'D:\001DIY\005lib\01AIEDA\learning\examples\lessonHI_38_50_20261021');R=H/'engineering_power';sys.path.insert(0,str(H/'tooling/packages'))
from shapely.geometry import Polygon
b=json.loads((H/'inventory/checkpoints/postcritical_2L_b010/normalized.json').read_text());orig=json.loads((H/'engineering_mcu/plans/mcu_critical_routes_v6.json').read_text())
p=dict(status='DRAFT_FULL_RIGHT10_REWORK_NEEDS_GEOMETRY_AND_NATIVE',batchId='RIGHT10_source_joint_v1',variant='BOTH',operations=[],placementChanges=[dict(ref='C15',xy=[47.3,30.4016],rotation=270,purpose='Free PB8/PB9 source copper, maintain local direct VDD/VSS loop'),dict(ref='R28',xy=[53,28],rotation=180,purpose='BOOT0 pulldown removes old ground pad/thermal obstruction from PB5 fanout')],sourceCheckpoint='postcritical_2L/4L_b010; rebase final SPIb012 geometry',rules=[],requiredProofs=[])
def opvia(i,n,xy,small=False):p['operations'].append(dict(type='via',id=i,net=n,xy=xy,padstack='HI_VIA026_C052_TENT' if small else 'L28_VIA030_C060',purpose='Joint fanout/quiet-anchor rework; native import/plane and negative challenge required'))
def route(i,n,l,pts,w=None,ws=None,purpose='Joint manual fanout, no arbitrary signal over quiet shadow'):
 d=dict(type='route',id=i,net=n,layer=l,points=pts,purpose=purpose)
 if ws is not None:d['widths']=ws
 else:d['width']=w
 p['operations'].append(d)
for i,n,xy in [('OLD_PC14','GPIO_PC14',[45.6,25.2]),('OLD_PC14_GND','GND',[46.95,24.9]),('OLD_HSE_ANCHOR','GND',[45.45,28.85]),('OLD_C15_COMMON_GND','GND',[47.45,28.7252])]:p['operations'].append(dict(type='deleteVia',id=i,net=n,xy=xy,padstack='L28_VIA030_C060',purpose='Exact unique native via removal before net disconnect, preserve unrelated vias'))
oldroutes=[('GND',.25,[[45.05,29.25],[45.45,28.85]]),('GND',.25,[[44.25,29.25],[45.05,29.25]]),('GND',.6,[[45.45,28.85],[46.5,28.7252]]),('GND',.6,[[46.5,28.7252],[47.45,28.7252]]),('GND',.6,[[47.9428,28.7252],[47.45,28.7252]]),('GND',.6,[[48.4,28.268],[47.9428,28.7252]]),('GND',.6,[[49.5,28.268],[48.4,28.268]]),('V3V3',.6,[[45.45,30.15],[46.5,30.3]]),('V3V3',.25,[[45.05,29.75],[45.45,30.15]]),('V3V3',.25,[[44.25,29.75],[45.05,29.75]]),('V3V3',.6,[[49.5,30.3],[46.5,30.3]]),('GPIO_PC14',.2,[[43.6,25.2],[45.6,25.2]])]
for i,(n,w,pts) in enumerate(oldroutes):p['operations'].append(dict(type='deleteSegment',id='RIGHT_RIP_'+str(i),net=n,layer='BOTTOM' if n=='GPIO_PC14' else 'TOP',points=pts,width=w))
route('RIGHT_PC14_SOUTH_BYPASS','GPIO_PC14','BOTTOM',[[43.6,25.2],[44.2,24.6],[44.2,22.7],[49.2,22.7],[49.2,25.2]],.2);opvia('RIGHT_PC14_FINAL','GPIO_PC14',[49.2,25.2]);opvia('RIGHT_PC14_RETURN','GND',[50.2,24.8])
route('RIGHT_VSS47_NECK','GND','TOP',[[44.25,29.25],[45.05,29.25],[45.3,29.5],[45.4,29.5]],.25)
route('RIGHT_VSS47_CAP_GROUND','GND','TOP',[[45.4,29.5],[45.7,29.5],[46.35,29.4],[47.0248,28.7252],[47.3,28.7252],[48.25,28.7252],[48.7072,28.268],[49.5,28.268]],.6)
opvia('HSE_SINGLE_ANCHOR_REWORK','GND',[46.35,29.4]);opvia('RIGHT_C15_COMMON_GND','GND',[48.25,28.7252])
route('RIGHT_VDD48_NECK','V3V3','TOP',[[44.25,29.75],[44.7,29.75],[45.3,30.35]],.25)
route('RIGHT_VDD48_CAP','V3V3','TOP',[[45.3,30.35],[47.3,30.3],[49.5,30.3]],.6)
anchors=[]
for pin,net,y in [(37,'SWCLK',24.25),(38,'GPIO_PA15',24.75),(39,'SWO',25.25),(40,'GPIO_PB4',25.75),(41,'GPIO_PB5',26.25),(42,'I2C_SCL',26.75),(43,'I2C_SDA',27.25),(44,'BOOT0',27.75),(45,'GPIO_PB8',28.25),(46,'GPIO_PB9',28.75)]:
 x=46.2 if pin%2 else 45.7;vy=round(y-.1,4);vi=[x,vy];opvia('RIGHT_'+net+'_VIA',net,vi,True)
 route('RIGHT_'+net+'_TOP',net,'TOP',[[44.25,y],[45,y],[45.1,vy],vi],.16)
 route('RIGHT_'+net+'_BOTTOM_ANCHOR',net,'BOTTOM',[vi,[46.35,vy],[46.4,vy]],ws=[.16,.2])
 anchors.append(dict(pin=pin,net=net,via=vi,anchorLayer='BOTTOM',anchor=[46.4,vy],topNeck_mm=.75+math.sqrt(.02)+x-45.1,bottomNeck_mm=46.35-x))
 p['requiredProofs'].append(dict(net=net,source='U1.'+str(pin),targetXY=[46.4,vy]))
for i,y in enumerate([24.9,26.4,27.9]):opvia('RIGHT_GROUND_STITCH_'+str(i),'GND',[46.99,y],True)
island=[[46,29.3],[46.7,29.3],[46.7,31.25],[46.2,31.75],[46.2,33.2],[47.5,33.2],[47.5,39.4],[37.2,39.4],[37.2,36.8],[40,36.8],[40,32.8],[40.6,32.8],[40.6,31.95],[45.3,31.95],[46,31.25]]
poly=Polygon(island);assert poly.is_valid
void=list(poly.buffer(.35,join_style=2).exterior.coords)[:-1]
p['oscillatorReferenceRework']=dict(source=orig['oscillatorReference'],islandPolygon=island,applicationGroundVoidPolygon=void,localLayer=orig['oscillatorReference']['localLayer'],singleBridgeOperation='HSE_SINGLE_ANCHOR_REWORK',negativeChallenge='Only remove HSE_SINGLE_ANCHOR_REWORK via46.35,29.4; C22/C23/quiet guard and island stay together but lose all VSS47/common/case connectivity. Restore then DRC0/fullfill/readback. Keep TOP HSE guard open ports; no global TOP pour across moat.',allAffectedObjects='Replace original quiet island; replace permanent application voids on every application copper plane; replace HSE shadow keepout/constraint region and all associated parent/child geometries consistently. Root f29 must inventory old objects and prove oldstem copper/keepout removed, not overlay both.',guard='Main HSE guard/case traces remain original, only neck/shadow moved outside right10 source. North open port must remain open.')
p['anchors']=anchors;p['physicalLengths_mm']=dict(VSS47newNeck=.8+math.hypot(.25,.25)+.1,VDD48newNeck=.45+math.hypot(.6,.6),note='Centerline lengths including pad center to flare are conservative upper bounds; native effective neck must be measured and satisfy original1.4 without raising.')
p['rules']=[dict(id='HI_RIGHT10_ESCAPE',layers=['TOP','BOTTOM'],polygon=[[43.5,23.7],[47.5,23.7],[47.5,29.0],[43.5,29.0]],signalNets=[a['net'] for a in anchors],physicalCopyFrom='Each actual own current CSet, preserving every other field',physicalOnlyDelta=dict(neckwidth_min=.16,necklength_max=2.0,viasAdd=['HI_VIA026_C052_TENT']),spacingCopyFrom='Each own current source and explicit class-pair CSet',spacingOnlyDelta=dict(smdpin_line=.16,line_line=.16,smdpin_via=.16,via_line=.16,via_via=.16),groundViaException=dict(net='GND',addApprovedVia='HI_VIA026_C052_TENT',onlySpacingDelta=dict(via_line=.20,via_via=.20),preserve='All GND width/neck/length/thermal/global otherfields unchanged'),purpose='Only dense source .5pitch fanout; external anchors resume .2 normal and original outside-region spacing; .26drill/.52Cu board-private, no public library modification')]
p['manufacturingBasis']=dict(JLC='Official pcb-capabilities drilling and via minimums rechecked2026-10-22; local source lesson28_stackup_20261019/source/jlc_capabilities_20261019.txt lines186-193',OSH='Official2L min drill.254mm/annulus.127mm; .26/.52 gives.13mm nominal annulus. No manufacturing approval implied.',open='Mask tenting/registration, actual laminate aspect ratio/tool and MPN dimensions remain DFM conditions')
p['reworkReason']='PC14 oldvia blocksSWO; quiet oldstem blocksPB9; oldR28 ground pad blocksPB5; frozen geometry must be jointly changed, not global rules relaxed.'
(R/'RIGHT10_source_joint_v1.json').write_text(json.dumps(p,indent=2),encoding='utf-8');print(len(p['operations']),len(anchors),p['physicalLengths_mm'])