from pathlib import Path
import re,json,csv,hashlib
R=Path(r'D:\001DIY\005lib\01AIEDA\learning\examples\lessonHI_38_50_20261021')
s=(R/'scripts/normalize_HI_actual_v4.py').read_text();exec(s[s.index('def sx('):s.index('symbols=')])
for v,tag in [('4L','private_pad_inspect_4L_01'),('2L','private_pad_inspect_2L_02')]:
 B=R/'logs'/tag;L=json.loads((B/'launch.json').read_text());assert L['completed'] and L['exitCode']==0 and L['beforeSHA256']==L['afterSHA256'];assert '*Error*' not in (B/'stdout.txt').read_text()
 pins=[ssrow(x) for x in rows(B/'hi_mechanical_pins.tsv')];pads=[ssrow(x) for x in rows(B/'hi_mechanical_pad_layers.tsv')]
 for p in pins:p['pads']=[x for x in pads if x['refdes']==p['refdes'] and x['padstack']==p['padstack'] and x['xy']==p['xy']]
 loc=[p for p in pins if p['refdes']=='J2'];assert len(loc)==2 and sorted(p['xy'] for p in loc)==[[37.11,6.28],[42.89,6.28]];assert all(p['drillDiameter']==.65 and p['plating']=='NON_PLATED' for p in loc)
 data={'status':'NATIVE_EMBEDDED_MECHANICAL_PINS_EXPLICITLY_READ','board':L['args'][-1],'sha256':L['beforeSHA256'],'readback':str(B),'pinCount':len(pins),'mechanicalPins':pins,'holesForGeometry':[{'ref':p['refdes'],'pin':p['pin'],'xy':p['xy'],'diameterMM':p['drillDiameter'],'plating':p['plating'],'source':'Embedded native definition; not padstack-name inference'} for p in pins if p['holeType']=='circle_drill' and p['plating']=='NON_PLATED']}
 (R/f'inventory/mechanical_pins_{v}_b012.json').write_text(json.dumps(data,indent=2),encoding='utf8');print(v,'mechanical pins',len(pins),'holes',data['holesForGeometry'])
 text=(B/'private_pad_definition.txt').read_text();assert 'PRIVATE_PAD_DEFINITION_READ_COMPLETE' in text
 assert 'name "HI_VIA026_C052_TENT"' in text and 'drillDiameter 0.26' in text and 'usage "Through_via"' in text
 assert 'VIA CLASS/SOLDERMASK_TOP" type="REGULAR" figure="NULL"' in text and 'VIA CLASS/SOLDERMASK_BOTTOM" type="REGULAR" figure="NULL"' in text
B=R/'native/private_padstacks';spec=json.loads((B/'spec_v2_imported.json').read_text());spec['status']='NATIVE_BINARY_AND_2L_4L_PAD_DEFINITION_READBACK_VERIFIED_NOT_BOARD_APPROVED';spec['definitionReadbacks']={v:str(R/'logs'/tag/'private_pad_definition.txt') for v,tag in [('4L','private_pad_inspect_4L_01'),('2L','private_pad_inspect_2L_02')]};spec['actualNativeName']='HI_VIA026_C052_TENT';spec['verificationScope']='Binary successfully loads into both actual layer stacks. .26mm plated Through_via, regular CIRCLE diameter.52 on every actual copper layer and DEFAULT_INTERNAL; ANTI/THERMAL/KEEPOUT NULL; top/bottom mask NULL. No via instance placed, no production board or approvedvia list modified, no new full DRC requested.';(B/'validation.json').write_text(json.dumps(spec,indent=2),encoding='utf8');print('private pad definition-only verified')
