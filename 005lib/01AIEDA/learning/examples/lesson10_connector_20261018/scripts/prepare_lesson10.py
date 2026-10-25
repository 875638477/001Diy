import pathlib,json,hashlib
B=pathlib.Path(r"D:\001DIY\005lib\01AIEDA\learning\examples\lesson10_connector_20261018")
for n in ["library","scripts","logs","runtime","verification"]:(B/n).mkdir(exist_ok=True)
L=B/"library";S=B/"scripts"
def write(p,t):p.write_text(t,encoding="utf-8",newline="\n")
def pad(n,usage,w,h,shape="RECTANGLE",hole=None):
 t=['<?xml version="1.0" encoding="UTF-8"?>','<!DOCTYPE padstack>','<padstack version="1.0">',f"<padstackname>{n}</padstackname>",f"<padstackusage>{usage}</padstackusage>","<units>Mm</units><accuracy>3</accuracy>"]
 if hole:
  a,b,pl=hole;ht="CIRCLE" if a==b else "OVAL_SLOT"
  t.append(f'<drillinfo><slothole><holetype>{ht}</holetype><plating>{pl}</plating><width>{a:.3f}</width><height>{b:.3f}</height><offset>(0;0)</offset><drillmethod>STANDARD</drillmethod></slothole><drillsymbol><figure>{"CIRCLE" if a==b else "OBLONGX"}</figure><characters>{"N" if pl=="N" else "S"}</characters><width>{a:.3f}</width><height>{b:.3f}</height></drillsymbol></drillinfo>')
 else:t.append("<drillinfo><slothole><holetype>NONE</holetype></slothole></drillinfo>")
 def p(layer,fig,pw,ph):
  t.append(f'<pad><type>REGULAR_PAD</type><layer>{layer}</layer><figure>{fig}</figure><offset>(0;0)</offset><width>{pw:.3f}</width><height>{ph:.3f}</height></pad>')
 for layer in (["BEGIN_LAYER","DEFAULT_INTERNAL","END_LAYER"] if hole else ["BEGIN_LAYER"]):p(layer,shape,w,h)
 if hole and hole[2]=="N":
  for layer in ["TOP_SOLDER_MASK_PAD","BOTTOM_SOLDER_MASK_PAD"]:p(layer,"CIRCLE",hole[0]+.1,hole[1]+.1)
 else:
  for layer in (["TOP_SOLDER_MASK_PAD","BOTTOM_SOLDER_MASK_PAD"] if hole else ["TOP_SOLDER_MASK_PAD"]):p(layer,shape,w+.1,h+.1)
  if not hole:p("TOP_PASTE_MASK_PAD",shape,w,h)
 t.append("</padstack>");write(L/(n+".pxml"),"\n".join(t)+"\n")
pad("l10_usb4105_smd030x115","SMD_PIN",.3,1.15)
pad("l10_usb4105_smd060x115","SMD_PIN",.6,1.15)
pad("l10_usb4105_slot060x170","SLOT",1,2.1,"OBLONG",(.6,1.7,"Y"))
pad("l10_usb4105_slot060x140","SLOT",1,1.8,"OBLONG",(.6,1.4,"Y"))
pad("l10_usb4105_npth065","MECH_HOLE",0,0,"NONE",(.65,.65,"N"))
lands=[("A1_B12",-3.2,"GND",["A1","B12"]),("A4_B9",-2.4,"VBUS",["A4","B9"]),("B8",-1.75,"SBU2",["B8"]),("A5",-1.25,"CC1",["A5"]),("B7",-.75,"Dn2",["B7"]),("A6",-.25,"Dp1",["A6"]),("A7",.25,"Dn1",["A7"]),("B6",.75,"Dp2",["B6"]),("A8",1.25,"SBU1",["A8"]),("B5",1.75,"CC2",["B5"]),("B4_A9",2.4,"VBUS",["B4","A9"]),("B1_A12",3.2,"GND",["B1","A12"])]
spec={"date":"2026-10-18","timezone":"Asia/Shanghai","mpn":"USB4105-GF-A","manufacturer":"Global Connector Technology (GCT)","drawing":"USB4105 Rev B4, 18/12/23, sheet 1/2","source_url":"https://gct.co/files/drawings/usb4105.pdf","source_sha256":hashlib.sha256((B/"source/usb4105.pdf").read_bytes()).hexdigest().upper(),"view":"Recommended PCB Layout: viewed from component side; never copy bottom view without transform","origin":"nominal shell body centre, +Y into PCB; front at y=-3.675","board_edge_y":-3.675,"body":[[-4.47,-3.675],[4.47,3.675]],"height_nominal":3.31,"height_max":3.46,"height_basis":"3.31 unqualified: X.XX general tolerance +/-0.15; MAX=3.46 mm","shell_stake_nominal":.95,"lands":[{"number":n,"x":x,"y":3.68,"w":.6 if len(cs)==2 else .3,"h":1.15,"function":f,"contacts":cs} for n,x,f,cs in lands],"shell":[{"number":n,"x":x,"y":y,"hole":[.6,hh],"land":[1,hh+.4]} for n,x,y,hh in [("SH1",-4.32,3.105,1.7),("SH2",4.32,3.105,1.7),("SH3",-4.32,-1.075,1.4),("SH4",4.32,-1.075,1.4)]],"npth":[[-2.89,2.605],[2.89,2.605]],"npth_diameter":.65,"npth_keepout_square":.85,"place_bound":[[-5.12,-4],[5.12,4.555]],"mating_reference":[[-6,-15.675],[6,-3.675]],"mating_reference_basis":"project learning reserve: 12 mm forward, 12 mm width, not a manufacturer full plug envelope; mating figure has 6.5 mm max plug height and 1.85 mm min axial feature only","mask_expansion_each_side":.05,"paste_smd":"same size as copper for this software exercise; stencil release requires assembly review","paste_shell":"none, soldering process not specified by land drawing","logical_mapping":"12 physical copper lands represent 16 contacts; matching logical part must explicitly combine paired GND/VBUS contacts or use separately validated multi-pin same-land mapping. Generic 16-pin symbols cannot attach unchanged.","shell_mapping":"SH1..SH4 are local tool identifiers for four common shell stakes, not manufacturer terminal numbers. Datasheet SHELL=GND; no PCB net assigned here.","plated_slot_basis":"tool choice: plated mechanically retained solderable shell stakes with 0.2 mm annular land. Manufacturer drawing gives hole/land sizes but does not explicitly label hole-wall plating; confirm finish dimensions/plating and assembly process before fabrication.","third_dimensional_model":"official CAD service exists but local access did not yield a downloadable STEP; no STEP imported or invented","restrictions":"isolated learning artifacts only, no public libraries, user boards or 01env changed","dimension_review":"4.18 and 3.68 are from front stake centre, not PCB edge. Add 2.60 from PCB edge. Root independent reread confirmed after initial datum misread."}
write(B/"spec.json",json.dumps(spec,ensure_ascii=False,indent=2))
pins=[]
for d in spec["lands"]:pins.append([("l10_usb4105_smd060x115" if d["w"]==.6 else "l10_usb4105_smd030x115"),d["x"],d["y"],d["number"]])
for d in spec["shell"]:pins.append([("l10_usb4105_slot060x170" if d["hole"][1]==1.7 else "l10_usb4105_slot060x140"),d["x"],d["y"],d["number"]])
for x,y in spec["npth"]:pins.append(["l10_usb4105_npth065",x,y,None])
write(S/"pins.skill.txt","\n".join(f'list("{p}" {x:.3f}:{y:.3f} '+('nil' if n is None else '"'+n+'"')+')' for p,x,y,n in pins))
for mode,fn,folder in [("create_package","l10CreatePackage","create_package"),("create_board","l10CreateBoard","create_board"),("read_package","l10Read","reopen_package"),("read_board","l10Read","reopen_board")]:
 (B/"logs"/folder).mkdir(exist_ok=True)
 args=f'"{B.as_posix()}" "{(B/"logs"/folder).as_posix()}"' if mode.startswith("create") else f'"{(B/"logs"/folder).as_posix()}"'
 write(S/(mode+".scr"),f'set NOCONFIRM\nskill errset(load("{(S/"lesson10.il").as_posix()}") t)\nskill errset({fn}({args}) t)\nquit\nfillin "yes"\n')
print(json.dumps({"prepared":str(B),"pads":len(list(L.glob("*.pxml"))),"physical_lands":len(lands),"signals":16,"shell_stakes":4,"mechanical_npth":2},indent=2))
