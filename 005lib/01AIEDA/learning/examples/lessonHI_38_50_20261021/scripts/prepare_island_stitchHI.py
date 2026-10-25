from pathlib import Path
import json
R=Path(r'D:\001DIY\005lib\01AIEDA\learning\examples\lessonHI_38_50_20261021')
p=R/'scripts/batchHI_shapes_v3.il';s=p.read_text();body=r'''
procedure(hiGroundPointCheck(f id xy topConnected bottomConnected)
 let((graph shapes expected actual)
  axlShapeDynamicUpdate(nil t) axlDBRefreshId(nil)
  graph=gConnectedObjects(gPin("U1" "23"))
  foreach(layer list("TOP" "BOTTOM")
   expected=if(equal(layer "TOP") then topConnected else bottomConnected)
   shapes=setof(s axlDBGetShapes(strcat("ETCH/" layer)) s->fill && s->net && equal(s->net->name "GND") && !s->shapeIsBoundary && axlGeoPointInShape(xy s t))
   unless(length(shapes)==1 error("Ground stitch point must be inside exactly one actual filled GND shape on each layer, layer=%L shapes=%L\n" layer shapes))
   unless(car(shapes)->shapeBoundary error("Ground stitch point must be in application dynamic copper, not static quiet island\n"))
   actual=if(member(car(shapes) graph) then t else nil)
   fprintf(f "HI_GROUND_POINT_CHECK id=%L layer=%L xy=%L bbox=%L globalPin=U1.23 expectedConnected=%L actualConnected=%L shapeAttrs=%L\n" id layer xy car(shapes)->bBox expected actual car(shapes)->??)
   unless(equal(expected actual) error("Application ground shape connectivity does not match intended stitch pre/post condition\n")))
  t))
'''
assert 'procedure(hiGroundPointCheck' not in s;p.write_text(s+'\n'+body,encoding='ascii')
s=(R/'scripts/compile_batchHI_v9.py').read_text();needle="if typ=='deleteSegment':statements.append"
replace="if typ=='groundPointCheck':statements.append(f'hiGroundPointCheck(f {q(ident)} {pt(op[\"xy\"])} '+('t' if op['topConnected'] else 'nil')+' '+('t' if op['bottomConnected'] else 'nil')+')')\n elif typ=='deleteSegment':statements.append"
assert needle in s;s=s.replace(needle,replace)
(R/'scripts/compile_batchHI_v10.py').write_text(s,encoding='ascii')
p=R/'scripts/prepare_readbackHI_v9.py';s=p.read_text();needle="  else:raise ValueError(p['type'])";replace="  elif p['type']=='groundPoint':\n   il+='  hiGroundPointCheck(f '+json.dumps(p['id'])+' '+pt(p['xy'])+' '+('t' if p['topConnected'] else 'nil')+' '+('t' if p['bottomConnected'] else 'nil')+')\\n'\n  else:raise ValueError(p['type'])";assert needle in s;s=s.replace(needle,replace)
(R/'scripts/prepare_readbackHI_v10.py').write_text(s,encoding='ascii')
d={'status':'ROOT_REVIEWED_GROUND_ISLAND_STITCH_REQUIRE_NATIVE','units':'mm','nativeVariant':'2L','operations':[{'type':'groundPointCheck','id':'ISLAND_BEFORE','net':'GND','xy':[37.4,27.4],'topConnected':False,'bottomConnected':True},{'type':'via','id':'V_HI_GPIO_ISLAND_STITCH','net':'GND','xy':[37.4,27.4],'padstack':'L28_VIA030_C060','purpose':'Connect actual previously floating GPIO TOP reference fragment to application BOTTOM ground.'},{'type':'groundPointCheck','id':'ISLAND_AFTER','net':'GND','xy':[37.4,27.4],'topConnected':True,'bottomConnected':True}],'proofs':[{'from':'V_HI_GPIO_ISLAND_STITCH','to':'U1.23','connected':True}],'postChecks':[{'type':'hseIsolation','anchorXY':[45.45,28.85],'localLayer':'BOTTOM','guardPoints':[[42.2,39.8],[44.2,39.8],[47.8,33.5]]}],'notes':['Root independent copper screen approves37.4,27.4; native precheck must confirm actual TOP island disconnected and actual BOTTOM application copper connected before mutation.','No rules or existing routes changed. Fresh readonly graph/branch audit must find zero terminal-free branches, ground stitch shape reachesU1.23, DRC0, HSEnegative still valid.']}
(R/'batches/island_stitch_2L_b011.json').write_text(json.dumps(d,indent=2),encoding='utf8')
print('stitch explicit pre/post actual copper checks prepared')
