"""Synthetic regression checks for bounded XML review and strict cache merge.
Writes only into a fresh --out directory. Never starts CAD or loads Dbo DLLs."""
from pathlib import Path
import argparse,copy,csv,hashlib,json,subprocess,sys,xml.etree.ElementTree as E
p=argparse.ArgumentParser();p.add_argument("--out",type=Path,required=True);a=p.parse_args()
assert not a.out.exists(),"Use a fresh selftest output directory"
a.out.mkdir(parents=True);tools=Path(__file__).resolve().parent;results=[]
def el(parent,tag,**attrs):
 x=E.SubElement(parent,tag);E.SubElement(x,"Defn",{k:str(v) for k,v in attrs.items()});return x
def write(root,path):E.ElementTree(root).write(path,encoding="utf-8",xml_declaration=True)
def canon(e):return [e.tag,sorted(e.attrib.items()),e.text if e.text and e.text.strip() else "",[canon(x) for x in e],e.tail if e.tail and e.tail.strip() else ""]
def h(e):return hashlib.sha256(json.dumps(canon(e),ensure_ascii=True,separators=(",",":")).encode()).hexdigest().upper()
def fixture():
 r=E.Element("Design");E.SubElement(r,"Defn",name="input.dsn");el(r,"Cache")
 s=el(r,"Schematic",name="S");el(s,"MaxDbId",val=1000);pg=el(s,"Page",name="P")
 el(pg,"PageDateTime",createDate="2020-01-01",createTime="00:00:00",modifyDate="2020-01-01",modifyTime="00:00:00")
 part=el(pg,"PartInst",dbId=30,name="INS1")
 el(part,"PartInstUserProp",name="A",val="one");el(part,"PartInstUserProp",name="B",val="two")
 el(part,"PortInstScalar",dbId=40,name="PIN",hotptX=0,hotptY=0)
 n=el(pg,"NetScalar",dbId=5,name="N")
 w=el(n,"WireScalar",dbId=1,startX=0,startY=0,endX=10,endY=0);el(w,"Alias",dbId=50,name="N");el(w,"Junction",locX=5,locY=0)
 el(n,"WireScalar",dbId=2,startX=0,startY=0,endX=10,endY=0)
 return r
def roundtrip(r):
 q=copy.deepcopy(r);q.find("Defn").set("name","output.dsn");q.find(".//MaxDbId/Defn").set("val","1100")
 q.find(".//PageDateTime/Defn").set("modifyTime","00:00:01");q.find(".//PartInst/Defn").set("name","INS2")
 q.find(".//PortInstScalar/Defn").set("dbId","140");q.find(".//Alias/Defn").set("dbId","150")
 ws=q.findall(".//WireScalar");j=ws[0].find("Junction");ws[0].remove(j);ws[1].append(j)
 part=q.find(".//PartInst");props=part.findall("PartInstUserProp");slots=[i for i,x in enumerate(part) if x.tag=="PartInstUserProp"]
 for i,x in zip(slots,reversed(props)):part[i]=x
 return q
def run_review(label,b,c,expected):
 d=a.out/label;d.mkdir();write(b,d/"before.xml");write(c,d/"after.xml")
 proc=subprocess.run([sys.executable,str(tools/"review_native_roundtrip.py"),"--before",str(d/"before.xml"),"--after",str(d/"after.xml"),"--out",str(d/"report"),"--allow-partinst-userprop-order"],capture_output=True,text=True)
 (d/"stdout.txt").write_text(proc.stdout+proc.stderr,encoding="utf-8")
 ok=(proc.returncode==0)==expected;results.append({"test":label,"expected_equal":expected,"exit_code":proc.returncode,"pass":ok});assert ok,(label,proc.stdout,proc.stderr)
base=fixture();rt=roundtrip(base);run_review("generated_ids_and_same_net_owner_and_userprop_order",base,rt,True)
q=copy.deepcopy(rt);q.find(".//PortInstScalar/Defn").set("name","CHANGED");run_review("pin_attribute_change_rejected",base,q,False)
q=copy.deepcopy(rt);w=q.findall(".//WireScalar")[1];w.remove(w.find("Junction"));run_review("junction_removed_rejected",base,q,False)
q=copy.deepcopy(rt);w=q.findall(".//WireScalar")[1];w.append(copy.deepcopy(w.find("Junction")));run_review("junction_duplicate_rejected",base,q,False)
q=copy.deepcopy(rt);q.find(".//PartInstUserProp/Defn").set("val","CHANGED");run_review("property_value_change_rejected",base,q,False)
q=copy.deepcopy(rt);q.find(".//PortInstScalar/Defn").set("dbId","1");run_review("generated_id_collision_rejected",base,q,False)
q=copy.deepcopy(base);w=q.findall(".//WireScalar")[1];w.find("Defn").set("startX","20");w.find("Defn").set("endX","30");run_review("junction_off_owner_rejected",q,roundtrip(q),False)
# Strict merge fixture: full Package identity may differ, but no electrical field.
r=E.Element("Design");E.SubElement(r,"Defn",name="design.dsn");cache=el(r,"Cache")
for name in ["A","B"]:
 pkg=el(cache,"Package",name=name,sourceLibName="LIB.OLB",pcbFootprint="FOOT",refdesPrefix="R")
 lp=el(pkg,"LibPart",CellName=name);view=el(lp,"NormalView",suffix=".Normal")
 el(view,"SymbolPinScalar",position=0,name="1",type=4,visible=1,startX=0,startY=0,hotptX=5,hotptY=0)
 el(lp,"PhysicalPart",name=name)
# PhysicalPart names are electrical, so they must agree to qualify.
for part in cache.findall("./Package/LibPart/PhysicalPart/Defn"):part.set("name","DEV")
sch=el(r,"Schematic",name="S");pg=el(sch,"Page",name="P")
for ident,name in [(10,"A"),(20,"B")]:
 part=el(pg,"PartInst",dbId=ident,name="INS"+str(ident),pkgName=name,libName="LIB.OLB")
 el(part,"GraphicName",name=name+".Normal");el(part,"Reference",name="R"+str(ident))
el(r,"Occurrences")
normal=copy.deepcopy(cache.find("Package"));nd=normal.find("Defn")
for key in ["name","sourceLibName","timestamp","timezone"]:nd.attrib.pop(key,None)
normal.find("LibPart/Defn").set("CellName","@CELL_0")
d=a.out/"strict_merge";d.mkdir();write(r,d/"input.xml")
plan={"mode":"STRICT_IDENTITY_ONLY","input_xml_sha256":hashlib.sha256((d/"input.xml").read_bytes()).hexdigest().upper(),"merge_count":1,"merges":[{"old_package":"B","old_lib":"LIB.OLB","canonical_package":"A","canonical_lib":"LIB.OLB","full_identity_normalized_sha256":h(normal)}]}
(d/"plan.json").write_text(json.dumps(plan),encoding="utf-8")
cmd=[sys.executable,str(tools/"cache_merge_strict.py"),"--input",str(d/"input.xml"),"--output",str(d/"merged.xml"),"--plan",str(d/"plan.json")]
proc=subprocess.run(cmd,capture_output=True,text=True);assert proc.returncode==0,(proc.stdout,proc.stderr);results.append({"test":"strict_identity_merge","pass":True,"exit_code":proc.returncode})
bad=copy.deepcopy(r);bad.findall("./Cache/Package")[1].find(".//SymbolPinScalar/Defn").set("type","5");write(bad,d/"bad.xml")
plan["input_xml_sha256"]=hashlib.sha256((d/"bad.xml").read_bytes()).hexdigest().upper();(d/"bad_plan.json").write_text(json.dumps(plan),encoding="utf-8")
proc=subprocess.run([sys.executable,str(tools/"cache_merge_strict.py"),"--input",str(d/"bad.xml"),"--output",str(d/"bad_output.xml"),"--plan",str(d/"bad_plan.json")],capture_output=True,text=True)
assert proc.returncode!=0 and not (d/"bad_output.xml").exists();results.append({"test":"pin_electrical_type_difference_blocks_merge_before_output","pass":True,"exit_code":proc.returncode})
summary={"status":"PASS_SYNTHETIC_REGRESSION_NO_CAD","tests":results}
(a.out/"SELFTEST_SUMMARY.json").write_text(json.dumps(summary,indent=2)+"\n",encoding="utf-8");print(json.dumps(summary,indent=2))
