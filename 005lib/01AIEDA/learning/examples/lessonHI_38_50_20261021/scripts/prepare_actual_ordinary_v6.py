import json,pathlib
h=pathlib.Path(__file__).resolve().parents[1]
for v in ('2L','4L'):
 p=json.loads((h/f'plans/ordinary_policy_{v}_v5.json').read_text(encoding='utf8'))
 p['status']='ACTUAL_POSTCRITICAL_B010_ORDINARY_POLICY_V6'
 p['pendingOperations']=[];p['pendingDeleteSegments']=[];p['sourcePlans']=[]
 p['sourceCheckpoint']=f'inventory/checkpoints/postcritical_{v}_b010'
 p['scope']='Actual postcritical native copper, no virtual already-executed batches. Explicit low-speed paths remain candidates until native DRC and actual reference review.'
 p['bottomCost']=1.45 if v=='2L' else 1.15;p['viaCostMM']=9 if v=='2L' else 5
 if v=='2L':
  p['pendingOperations']=[{'type':'via','id':'pending_GND_island_stitch_b011','net':'GND','xy':[37.4,27.4],'padstack':'L28_VIA030_C060'}]
 (h/f'plans/ordinary_policy_{v}_v6.json').write_text(json.dumps(p,indent=2),encoding='utf8')