import pathlib,json,math,shutil
BASE=pathlib.Path(__file__).resolve().parent.parent
LIB=BASE/'library'; SCRIPTS=BASE/'scripts'; LOGS=BASE/'logs'
def write(p,s):p.write_text(s,encoding='utf-8')
def padrow(layer,w,h,r=0):
 s=f'<pad><type>REGULAR_PAD</type><layer>{layer}</layer><figure>{"ROUNDED_RECTANGLE" if r else "RECTANGLE"}</figure><offset>(0;0)</offset><width>{w:.3f}</width><height>{h:.3f}</height>'
 if r:s+=f'<corner>{r:.3f}</corner><ul>Y</ul><ur>Y</ur><ll>Y</ll><lr>Y</lr>'
 return s+'</pad>'
pads={
 'l09_qfp120x030_m05':{'c':[1.2,.3,0],'m':[1.3,.4,0],'p':[1.2,.3,0]},
 'l09_qfn060x024_r005_m07':{'c':[.6,.24,.05],'m':[.74,.38,.12],'p':[.6,.24,.05]},
 'l09_ep168_m07_nopaste':{'c':[1.68,1.68,.05],'m':[1.82,1.82,.12]},
 'l09_ep168_m07_single155':{'c':[1.68,1.68,.05],'m':[1.82,1.82,.12],'p':[1.55,1.55,.05]}}
for name,d in pads.items():
 xml='<?xml version="1.0" encoding="UTF-8"?>\n<!DOCTYPE padstack>\n<padstack version="1.0">'+f'<padstackname>{name}</padstackname><padstackusage>SMD_PIN</padstackusage><units>Mm</units><accuracy>3</accuracy><drillinfo><slothole><holetype>NONE</holetype></slothole></drillinfo>'
 for kind,layer in [('c','BEGIN_LAYER'),('m','TOP_SOLDER_MASK_PAD'),('p','TOP_PASTE_MASK_PAD')]:
  if kind in d:xml+=padrow(layer,*d[kind])
 write(LIB/(name+'.pxml'),xml+'</padstack>\n')
via='l09_thermal_via020_c040'
xml='<?xml version="1.0" encoding="UTF-8"?>\n<!DOCTYPE padstack>\n<padstack version="1.0"><padstackname>'+via+'</padstackname><padstackusage>VIA</padstackusage><units>Mm</units><accuracy>3</accuracy><drillinfo><slothole><holetype>CIRCLE</holetype><plating>Y</plating><width>0.200</width><height>0.200</height><offset>(0;0)</offset><drillmethod>STANDARD</drillmethod></slothole><drillsymbol><figure>CIRCLE</figure><characters>V</characters><width>0.200</width><height>0.200</height></drillsymbol></drillinfo>'
for layer in ['BEGIN_LAYER','DEFAULT_INTERNAL','END_LAYER']:
 xml+=f'<pad><type>REGULAR_PAD</type><layer>{layer}</layer><figure>CIRCLE</figure><offset>(0;0)</offset><width>0.400</width><height>0.400</height></pad>'
write(LIB/(via+'.pxml'),xml+'</padstack>\n')
def perimeter(n,radius,pitch):
 pins=[]; side=n//4; a=(side-1)*pitch/2
 for j in range(side):pins.append({'number':j+1,'xy':[-radius,a-j*pitch],'rotation':0})
 for j in range(side):pins.append({'number':side+j+1,'xy':[-a+j*pitch,-radius],'rotation':90})
 for j in range(side):pins.append({'number':2*side+j+1,'xy':[radius,-a+j*pitch],'rotation':0})
 for j in range(side):pins.append({'number':3*side+j+1,'xy':[a-j*pitch,radius],'rotation':90})
 return pins
specs=[{'name':'l09_stm32f103c8_lqfp48','part':'STM32F103C8T6','pins':perimeter(48,4.25,.5),'pad':'l09_qfp120x030_m05','body':7,'height':1.6,'bound':5.1,'sourcePages':[98,99,100],'land':[1.2,.3],'pasteWindows':[]},
 {'name':'l09_tps62130_rgt16_single','part':'TPS62130RGTR','pins':perimeter(16,1.4,.5),'pad':'l09_qfn060x024_r005_m07','ep':'l09_ep168_m07_single155','body':3.1,'height':1,'bound':1.95,'sourcePages':[3,28,40,41,42],'land':[.6,.24],'pasteWindows':[]},
 {'name':'l09_tps62130_rgt16_split','part':'TPS62130RGTR','pins':perimeter(16,1.4,.5),'pad':'l09_qfn060x024_r005_m07','ep':'l09_ep168_m07_nopaste','body':3.1,'height':1,'bound':1.95,'sourcePages':[3,28,40,41,42],'land':[.6,.24],'pasteWindows':[[x,y,.65,.65] for x in [-.425,.425] for y in [-.425,.425]]}]
for s in specs:
 if 'ep' in s:s['pins'].append({'number':17,'xy':[0,0],'rotation':0,'role':'EP:GND; must connect AGND6/PGND15,16/common ground'})
write(BASE/'lesson09_spec.json',json.dumps({'units':'mm','scope':'Isolated CAD learning only; not published or production approved','pads':pads,'thermalVia':{'name':via,'drill':.2,'copper':.4,'filledPluggedOrTented':'Requires fabricator/assembler agreement; CAD hole is unfilled','centers':[[x,y] for x in [-.58,.58] for y in [-.58,.58]]+[[0,0]]},'packages':specs},indent=2))
def point(v):return f'{v[0]:.3f}:{v[1]:.3f}'
def native_script(lines):return 'set NOCONFIRM\nskill errset(load("'+(SCRIPTS/'lesson09.il').as_posix()+'") t)\n'+''.join('skill errset('+l+' t)\n' for l in lines)+'quit\nfillin "yes"\n'
for s in specs:
 name=s['name']; out=LOGS/(name+'_create');out.mkdir(exist_ok=True)
 lines=[f'procedure(l9Create_{name}()','let((f pad style ns result bound windows)','unless(equal(axlCurrentDesign() "'+name+'") error("Wrong drawing\\n"))','unless(length(axlDBGetDesign()->pins)==0 error("Not empty\\n"))','axlDBChangeDesignUnits("millimeters" 3)','axlDBChangeDesignExtents(list(-12:-12 12:12))',f'axlSetVariable("padpath" list("{LIB.as_posix()}"))',f'axlSetVariable("psmpath" list("{LIB.as_posix()}"))',f'f=outfile("{out.as_posix()}/create.txt")','style=make_axlTextOrientation(?textBlock "2" ?rotation 0 ?mirrored nil ?justify "center")','ns=make_axlTextOrientation(?textBlock "1" ?rotation 0 ?mirrored nil ?justify "center")']
 for p in s['pins']:
  pn=s['ep'] if p['number']==17 and 'ep'in s else s['pad']
  lines += [f'pad=axlLoadPadstack("{pn}")', 'unless(pad error("Pad load failed\\n"))',f'result=axlDBCreatePin(pad {point(p["xy"])} make_axlPinText(?number "{p["number"]}" ?offset 0:0 ?text ns) {p["rotation"]})','unless(result error("Pin create failed\\n"))']
 b=s['body']/2
 lines += [f'unless(axlDBCreateLine(list({-b}:{-b} {b}:{-b} {b}:{b} {-b}:{b} {-b}:{-b}) 0.05 "PACKAGE GEOMETRY/ASSEMBLY_TOP" nil nil) error("Assembly failed\\n"))']
 # Four outer corner silk stubs; avoid terminal mask openings.
 bb=s['bound'];k=bb-.3
 for xsign in [-1,1]:
  for ysign in [-1,1]:
   pts=[[xsign*k,ysign*bb],[xsign*bb,ysign*bb],[xsign*bb,ysign*k]]
   lines += ['unless(axlDBCreateLine(list('+ ' '.join(point(p) for p in pts)+') 0.1 "PACKAGE GEOMETRY/SILKSCREEN_TOP" nil nil) error("Silk failed\\n"))']
 # Pin1 marker in the northwest corner consistently with rotated ST reference and TI top view.
 m=bb-.13
 lines += [f'unless(axlDBCreateLine(list({-m}:{m} {-m+.1}:{m} {-m}:{m-.1} {-m}:{m}) 0.05 "PACKAGE GEOMETRY/SILKSCREEN_TOP" nil nil) error("Marker failed\\n"))',f'result=axlDBCreateRectangle(list({-bb}:{-bb} {bb}:{bb}) t "PACKAGE GEOMETRY/PLACE_BOUND_TOP" nil nil)','unless(result error("Bound failed\\n"))','bound=car(result)',f'unless(axlDBAddProp(list(bound) list("PACKAGE_HEIGHT_MAX" "{s["height"]} MM")) error("Height failed\\n"))']
 for x,y,w,h in s['pasteWindows']:
  lines += [f'unless(axlDBCreateRectangle(list({x-w/2:.3f}:{y-h/2:.3f} {x+w/2:.3f}:{y+h/2:.3f}) t "PACKAGE GEOMETRY/PASTEMASK_TOP" nil nil) error("Paste window failed\\n"))']
 for layer,text in [('REF DES/SILKSCREEN_TOP','U*'),('REF DES/ASSEMBLY_TOP','U*'),('COMPONENT VALUE/ASSEMBLY_TOP','VALUE')]:
  lines += [f'unless(axlDBCreateText("{text}" 0:0 style "{layer}" nil) error("Text failed\\n"))']
 lines += [f'unless(axlSaveDesign(?design "{(LIB/(name+".dra")).as_posix()}" ?noMru t ?noConfirm t) error("Save failed\\n"))',f'unless(axlCompileSymbol(?symbol "{(LIB/name).as_posix()}") error("Compile failed\\n"))','fprintf(f "L09 CREATE COMPLETE\\n")','close(f)','t))']
 write(SCRIPTS/(name+'_create.il'),'\n'.join(lines)+'\n')
 write(SCRIPTS/(name+'_create.scr'),'set NOCONFIRM\nskill errset(load("'+(SCRIPTS/(name+'_create.il')).as_posix()+'") t)\nskill errset(l9Create_'+name+'() t)\nquit\nfillin "yes"\n')
shutil.copyfile(BASE.parents[1]/'examples'/'lesson07_completion_20261018'/'scripts'/'launch_package17.py',SCRIPTS/'launch_package17.py')
print('Prepared',len(specs),'packages and',len(pads)+1,'padstacks; no Cadence started')


