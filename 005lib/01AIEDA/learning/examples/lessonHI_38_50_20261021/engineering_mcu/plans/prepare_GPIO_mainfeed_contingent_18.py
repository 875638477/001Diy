import pathlib,json,math
P=pathlib.Path(r'D:\001DIY\005lib\01AIEDA\learning\examples\lessonHI_38_50_20261021\engineering_mcu\plans')
for v in ['4L','2L']:
 n=json.loads((P/f'GPIO_future_{v}_17_snapshot.json').read_text());removed=[]
 for a,b in [[[30.7,32],[37,25.7]],[[37,25.7],[37,24]]]:
  ms=[r for r in n['routes'] if r['net']=='V3V3' and r['layer']=='ETCH/BOTTOM' and r['startEnd'] in [[a,b],[b,a]]];assert len(ms)==1;removed+=ms;n['routes'].remove(ms[0])
 ms=[z for z in n['vias'] if z['net']=='V3V3' and z['xy']==[37,24]];assert len(ms)==1;n['vias'].remove(ms[0])
 n['status']='CONTINGENT_GPIO_CORRIDOR_STUDY_MAIN_POWER_NOT_COMPLETE';n['mainFeedDependency']='Original BOTTOM mainSTAR temporarily removed for explicit GPIO corridor co-design; f28 must provide legal .6 mainfeed before any native batch. This disconnected-power scene is NOT a working board or executable netcomplete route.';n['hypotheticalRemovedMainFeed']=removed+ms
 (P/f'GPIO_future_{v}_18_snapshot.json').write_text(json.dumps(n,indent=2),encoding='utf8')
print('contingent co-design scenes only, no executable power claim')
