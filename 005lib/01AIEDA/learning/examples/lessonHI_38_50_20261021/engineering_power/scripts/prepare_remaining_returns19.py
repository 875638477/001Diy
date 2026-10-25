from pathlib import Path
import json,copy,math
R=Path(r'D:\001DIY\005lib\01AIEDA\learning\examples\lessonHI_38_50_20261021');P=R/'engineering_power'
for v in ['2L','4L']:
 q=json.loads((P/f'source/RIGHT11_UART03_virtual_{v}.json').read_text(encoding='utf-8'))
 b=next(x for x in q['operations'] if x['id']=='RIGHT_BOOT_DIRECT_TOP');b['points']=[[46.8,27.65],[47.27,27.18],[52.8984,27.18],[52.8984,28]]
 (P/f'source/RIGHT11_UART03_BOOT2_virtual_{v}.json').write_text(json.dumps(q,indent=2)+'\n',encoding='utf-8')
 choices=[('NRST',[39.05,42.1],[40.1,42.2]),('UART_TX',[54.85,18.95],[54.45,17.8])]
 if v=='4L':choices += [('CAN_RXD_SOURCE',[61.45,12.2],[61.7,11.2]),('CAN_RXD_DEST',[37.65,16.7],[36.5,16.1]),('VBUS_PRESENT_N',[50.85,12.85],[49.7,13.5])]
 else:choices += [('VBUS_PRESENT_N',[51.15,11.7],[50,11.1])]
 ops=[dict(type='via',id='REM19_RETURN_'+net,net='GND',xy=g,padstack='L28_VIA030_C060',purpose='CandidatecommonGNDreturn for '+net+'; must prove actualcommoncopper after full dynamicrefresh') for net,s,g in choices]
 out=dict(batchId='remaining_returns_'+v+'_v19_01',status='CANDIDATE_PARENT_POINTS_FULL_FUTURE_REVIEW_PENDING',variant=v,operations=ops,engineeringReturns=[dict(signal=net,signalViaXY=s,groundViaXY=g,distanceMM=math.dist(s,g))for net,s,g in choices],scope='Do not treat quietcap/island grounds as common. Geometryon allfuture source+UART03+remaining19; not native approval.')
 (P/f'remaining_returns_{v}_v19_01.json').write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8')
print('Preparedcandidate01 and virtual-onlyBOOT2/source adaptations; frozen files unchanged')