from pathlib import Path
import sys,json,copy
R=Path(r'D:\001DIY\005lib\01AIEDA\learning\examples\lessonHI_38_50_20261021');P=R/'engineering_power';sys.path.insert(0,str(R/'scripts'));from routing_geometry import CopperScene,load,LineString,box,Polygon
from shapely.ops import unary_union
rows=[]
for v in ['2L','4L']:
 s=load(R/f'engineering_mcu/plans/GPIO_future_{v}_21_snapshot.json');pol=copy.deepcopy(load(R/f'engineering_mcu/plans/GPIO_future_{v}_21_policy.json'))
 sw=next(a for a in pol['reservedAreas']if a['id']=='SWITCHING_BLOCK');sw['layers']=['TOP']
 scene=CopperScene(s,load(R/f'engineering_mcu/plans/GPIO_future_{v}_21_networks.json'),load(R/f'engineering_mcu/plans/GPIO_future_{v}_21_rules.json'),pol)
 hot=[]
 for ob in scene.obstacles:
  if ob['layer']=='TOP'and ob['net']in ['BUCK_SW','BUCK_BOOT','BUCK_FB']:hot.append(ob['geometry'])
 hazards=unary_union(hot);window=box(28.3,23.2,30.9,26.5);cols=[]
 for ix in range(7):
  x=28.4+.4*ix;pts=[[x,23.3],[x,26.4]];center=LineString(pts);cu=center.buffer(.1);topForeign=[ob for ob in scene.obstacles if ob['layer']=='TOP'and ob['net']not in ['GND',None]and ob['kind']not in ['keepout','hole']];projection=unary_union([ob['geometry'].buffer(.3)for ob in topForeign]);projlen=center.intersection(projection).length
  cols.append(dict(centerPoints=pts,width=.2,localBOTTOMClear=scene.path_clear('GPIO_PB1','BOTTOM',pts,.2),minCuGapToActualSW_BOOT_FB_MM=cu.distance(hazards),TOPForeignCuPlusPoint3ProjectionLengthMM=projlen))
 rows.append(dict(variant=v,columns=cols,localCuEnvelope=window.bounds,scope='Onlylocalstraightcolumns not7PBfullroutes; inlet/outlet/transitionpads andfutureGPIOcoordinationnotproved. Bottom-onlyregionalwaiver, TOPoldhotblockremains.'))
out=dict(status='LOCAL_CORRIDOR_STUDY_NOT_ROUTING_RELEASE',date='2026-10-22',engineeringWindow=[[28.3,23.2],[30.9,23.2],[30.9,26.5],[28.3,26.5]],policyChangeIfAdopted='KeepTOP SWITCHING_BLOCK; onBOTTOM replacecoarseboxwithtrueSW/BOOT/FB +>=1mm avoidandactualL1bodyprojection/thermalinputloop; onlylimitedstudiedwindowexception.',variants=rows,limits=['7*.2signal+.2spacingfitslocal2.6mmcolumnenvelope; notproofthatall7sourcescanenter/exit','ExistingV3via33.3,22.5 andBOOT1via32.5,23.7 create tight lowerapproach; solvejointly, do notcutpower/ground ordeclarewaiveralonefixesallGPIO','2L TOPglobalapplicationGND notyetgenerated; currentTOPprojectionlength onlyscreen, requireactualplaneandreturn stitch fortransitions;4LcommonL3mustrefreshafterantipads','Do not move mainfeed merelyfrom10snooutput/greedysearchfailure'])
(P/'readouts/PB_local_switch_corridor_01.json').write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8');print(json.dumps(out))