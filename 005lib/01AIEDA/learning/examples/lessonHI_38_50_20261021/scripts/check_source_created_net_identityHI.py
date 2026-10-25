from pathlib import Path
import re,json
R=Path(r'D:\001DIY\005lib\01AIEDA\learning\examples\lessonHI_38_50_20261021');p=R/'review/source_b015_native_report.json';d=json.loads(p.read_text())
for v in ['2L','4L']:
 text=Path(d['variants'][v]['buildLog'],'hi_batch_execution.txt').read_text();m=re.findall(r'HI_CREATED_ROUTE_NATIVE_NET id="([^"]+)" expected="([^"]+)" object=([^\s]+) actualNet="([^"]+)" layer="([^"]+)"',text);assert len(m)>40 and all(e==n for _,e,_,n,_ in m);d['variants'][v]['createdPathNativeNetReadbacks']=len(m);d['variants'][v]['everyCreatedPathActualNetMatchesRequested']=True
p.write_text(json.dumps(d,indent=2),encoding='utf8');print({v:d['variants'][v]['createdPathNativeNetReadbacks'] for v in ['2L','4L']})
