from pathlib import Path
R=Path(r'D:\001DIY\005lib\01AIEDA\learning\examples\lessonHI_38_50_20261021')
p=R/'scripts/batchHI_shapes_v3.il';s=p.read_text();start=s.index('procedure(hiReferenceCoverageRead(out step)');end=s.index('\nprocedure(',start+1)
body=s[start:end]
body=body.replace('sampleCount p)','sampleCount p globalGraph connected floating)')
body=body.replace('staticQuietCount\\n','staticQuietCount\\tapplicationGlobalConnectedCount\\tapplicationWithoutGlobalPinConnectionCount\\n')
body=body.replace('seen=nil manualCount=0 sampleCount=0','seen=nil manualCount=0 sampleCount=0 globalGraph=gConnectedObjects(gPin("U1" "47"))')
body=body.replace('app=0 quiet=0','app=0 quiet=0 connected=0 floating=0')
body=body.replace('if(s->shapeBoundary then app=app+1 else quiet=quiet+1)', 'if(s->shapeBoundary then\n         app=app+1\n         if(member(s globalGraph) then connected=connected+1 else floating=floating+1)\n        else quiet=quiet+1)')
body=body.replace('%L\\t%d\\t%d\\n"','%L\\t%d\\t%d\\t%d\\t%d\\n"')
body=body.replace('i*1.0/n xy app quiet)','i*1.0/n xy app quiet connected floating)')
body=body.replace('classification=Application dynamic GND vs local static quiet GND kept separate.', 'classification=Application dynamic GND vs local static quiet GND kept separate. Dynamic GND shapes additionally distinguished by actual graph reachability to application pin U1.47; same net label alone is not sufficient.')
assert 'applicationGlobalConnectedCount' in body and 'globalGraph=' in body
p.write_text(s+'\n\n; Connectivity-aware reference sampling override; historical immutable readbacks retain their original version.\n'+body,encoding='ascii')
print('future reference sampler adds actual global-pin connectivity, preserves all geometric-only counts')
