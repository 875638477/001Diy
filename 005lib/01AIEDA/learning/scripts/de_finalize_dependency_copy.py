import csv,pathlib,json,shutil,hashlib,collections
ROOT=pathlib.Path(__file__).resolve().parents[1]
BASE=ROOT/'examples/de_15_26_20261019';LIB=BASE/'library'
rows=list(csv.DictReader((ROOT/'staging/de_15_26_20261019/dependency_load02/pins.tsv').open(),delimiter='\t'))
padnames=sorted({r['padstack'] for r in rows})
sources={p.stem.upper():p for p in (ROOT.parents[1]/'01Pad_lib').glob('*.pad')}
sources.update({p.stem.upper():p for f in ['lesson09_qfn_qfp_20261018','lesson10_connector_20261018'] for p in (ROOT/'examples'/f/'library').glob('*.pad')})
copied=[]
for name in padnames:
    if not (LIB/(name+'.pad')).exists():
        source=sources[name.upper()];shutil.copy2(source,LIB/source.name)
        copied.append({'source':str(source),'destination':str(LIB/source.name),'sha256':hashlib.sha256(source.read_bytes()).hexdigest()})
top=[r for r in rows if r['layer']=='ETCH/TOP']
packages={}
for row in top:packages.setdefault(row['package'],[]).append(row)
for name in ['0603','0805','1206','do-214ac_sma','do-214aa_smb','L4018','HC-49SMD']:
    assert {r['pin'] for r in packages[name]}=={'1','2'},name
for name,count in [('sot23-6',6),('sot23-5',5),('sot23-3',3),('so8',8),('l09_stm32f103c8_lqfp48',48)]:
    assert {r['pin'] for r in packages[name]}=={str(i) for i in range(1,count+1)},name
for n in [2,3,4,6,8]:
    name=f'pin{n:02d}_2d54MM_1x{n}';pkg=packages[name]
    assert {r['pin'] for r in pkg}=={str(i) for i in range(1,n+1)}
    x=sorted(float(r['x']) for r in pkg);y=sorted(float(r['y']) for r in pkg)
    coords=x if max(x)-min(x)>max(y)-min(y) else y
    assert all(abs(b-a-2.54)<.002 for a,b in zip(coords,coords[1:])),name
    alias=f'DE_HDR1X{n}_254_TH'
    dest=LIB/(alias+'.dra')
    if not dest.exists():shutil.copy2(LIB/(name+'.dra'),dest)
summary={'nativeLoadComplete':(ROOT/'staging/de_15_26_20261019/dependency_load02/summary.txt').read_text(),'nativePackages':{n:{'pins':len(v),'pinNumbers':[x['pin'] for x in v],'padstacks':sorted({x['padstack'] for x in v})} for n,v in packages.items()},'copiedPads':copied,'fallbackPublicAllowedOnlyInitialInventory':True,'finalIsolatedLoad':'pending','notSelected':['L4018','HC-49SMD','xtal3225','sw_PB4_6x6']}
(BASE/'dependency_native_inventory.json').write_text(json.dumps(summary,indent=2),encoding='utf-8')
print(json.dumps({'copiedPads':len(copied),'nativePackages':len(packages),'aliases':[f'DE_HDR1X{n}_254_TH' for n in [2,3,4,6,8]]}))
