from pathlib import Path
R=Path(r'D:\001DIY\005lib\01AIEDA\learning\examples\lessonG_30_37_20261020\engineering_power')
p=R/'scripts/review_final_native.py'
text=p.read_text(encoding='utf-8')
text=text.replace("p['net']==net)","(p['net'] or None)==net)").replace("np['net']==net and","(np['net'] or None)==net and")
needle="   ck(prefix+ref+'.'+n+':padstack',p['padstack']==lp['padstack'])"
new=needle+"""
   ib=lp['regularPadBBox'];pts=[transform([x,y],[0,0],expected['rotation']) for x in (ib[0][0],ib[1][0]) for y in (ib[0][1],ib[1][1])]
   expectedPadBBox=[[min(z[i] for z in pts) for i in (0,1)],[max(z[i] for z in pts) for i in (0,1)]]
   ck(prefix+ref+'.'+n+':rotatedPadBBox',all(near(x,y) for x,y in zip(p['padbbox'],expectedPadBBox)))
"""
text=text.replace(needle,new)
needle2="   ck(prefix+ref+'.'+n+':normalizedPin',(np['net'] or None)==net and near(np['xy'],p['xy']))"
new2=needle2+"""
   normalizedBBox=[[p['xy'][i]+p['padbbox'][j][i] for i in (0,1)] for j in (0,1)]
   ck(prefix+ref+'.'+n+':normalizedPadBBox',all(near(x,y) for x,y in zip(np['padBBox'],normalizedBBox)))
"""
text=text.replace(needle2,new2)
p.write_text(text,encoding='utf-8')
