import pathlib,csv,json,hashlib,math
ROOT=pathlib.Path(__file__).resolve().parents[1];BASE=ROOT/'examples/de_15_26_20261019';ST=ROOT/'staging/de_15_26_20261019';LIB=BASE/'library'
checks=[]
def ck(ok,label):
    checks.append({'check':label,'pass':bool(ok)})
    assert ok,label
created=list(csv.DictReader((ST/'dependencies_final_create/pins.tsv').open(),delimiter='\t'))
reopened=list(csv.DictReader((ST/'dependencies_final_reopen/pins.tsv').open(),delimiter='\t'))
ck(created==reopened,'all native pin/layer geometry persisted after fresh readonly reopen')
for mode in ['create','reopen']:
    ck(json.loads((ST/('dependencies_final_'+mode+'_cli')/'launch.json').read_text())['exitCode']==0,'native '+mode+' exit0')
    ck('packages=19' in (ST/('dependencies_final_'+mode)/'summary.txt').read_text(),'native '+mode+' complete19')
by={}
for r in reopened:by.setdefault(r['package'].lower(),[]).append(r)
selected=json.loads((BASE/'selected_footprints.json').read_text())['footprints']
ck(set(by)=={x.lower() for x in selected},'exact selected 19 packages loaded using isolated library only')
for n in selected:
    for ext in ['.dra','.psm']:ck((LIB/(n+ext)).is_file(),n+ext+' exists')
expected={n:2 for n in ['0603','0805','1206','do-214ac_sma','do-214aa_smb','de_capradial_6d3_p2d5','de_xal6060_2land']}
expected.update({'sot23-6':6,'sot23-5':5,'sot23-3':3,'so8':8,'de_abm3b_5032':4,'l09_stm32f103c8_lqfp48':48})
expected.update({f'pin{n:02d}_2d54MM_1x{n}'.lower():n for n in [2,3,4,6,8]})
for name,count in expected.items():
    top=[r for r in by[name] if r['layer']=='ETCH/TOP']
    ck({r['pin'] for r in top}=={str(i) for i in range(1,count+1)},name+' exact pin numbers/count')
    for r in top:
        ck(float(r['w'])>0 and float(r['h'])>0,name+'.'+r['pin']+' positive top copper')
usb=[r for r in by['l10_gct_usb4105_gf_a_12land'] if r['layer']=='ETCH/TOP']
ck({r['pin'] for r in usb if r['pin']}=={'A1_B12','A4_B9','B8','A5','B7','A6','A7','B6','A8','B5','B4_A9','B1_A12','SH1','SH2','SH3','SH4'},'USB exact 12 signal/power land +4 shield mapping')
ck(sum(r['mechanical']=='t' and not r['pin'] for r in usb)==2,'USB two unnumbered mechanical pins')
def near(value,expected):return abs(float(value)-expected)<.002
for name,coords,dims in [('de_abm3b_5032',{'1':[-2,-1.2],'2':[2,-1.2],'3':[2,1.2],'4':[-2,1.2]},[1.8,1.2]),('de_xal6060_2land',{'1':[2.02,0],'2':[-2.02,0]},[1.43,5.5]),('de_capradial_6d3_p2d5',{'1':[-1.25,0],'2':[1.25,0]},[1.54,1.54])]:
    for r in by[name]:
        if r['layer']!='ETCH/TOP':continue
        ck(near(r['x'],coords[r['pin']][0]) and near(r['y'],coords[r['pin']][1]),name+'.'+r['pin']+' manufacturer/local top view coordinates')
        ck(near(r['w'],dims[0]) and near(r['h'],dims[1]),name+'.'+r['pin']+' exact copper land dimensions')
for n in [2,3,4,6,8]:
    name=f'pin{n:02d}_2d54MM_1x{n}'.lower();rows=[r for r in by[name] if r['layer']=='ETCH/TOP']
    xs=sorted(float(r['x']) for r in rows);ys=sorted(float(r['y']) for r in rows);v=xs if max(xs)-min(xs)>max(ys)-min(ys) else ys
    ck(all(abs(b-a-2.54)<.002 for a,b in zip(v,v[1:])),name+' native 2.54mm pitch')
    ck(all(r['plating']=='PLATED' and float(r['drill'])>0 for r in rows),name+' native plated through holes')
for r in reopened:
    ck((LIB/(r['padstack']+'.pad')).is_file(),'pad dependency '+r['padstack'])
result={'status':'PASS_NATIVE_DEPENDENCIES','checks':len(checks),'packages':19,'nativePinLayerRows':len(reopened),'limitations':['Generic reused footprints are verified as native geometry/dependencies, not qualified against every final MPN land-pattern drawing.','Capradial body/hole/pitch is a procurement teaching envelope; final MPN selection and solder/lead fit pending.','Soldermask/paste dimensions are learning definitions, assembly process review remains.'],'files':[{'path':str(p),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in sorted(LIB.iterdir()) if p.suffix.lower() in ['.dra','.psm','.pad','.pxml']],'details':checks}
(BASE/'dependency_validation.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
print(json.dumps({k:v for k,v in result.items() if k not in ['files','details']},indent=2))
