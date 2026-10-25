"""Bounded semantic review of a Capture XML native import/export.
Retains raw differences; proves only generated IDs/names, page dates and
same-Net junction container ownership differ. No native execution."""
from pathlib import Path
import argparse,collections,copy,csv,hashlib,json,re,xml.etree.ElementTree as E
P=argparse.ArgumentParser();P.add_argument("--before",type=Path,required=True);P.add_argument("--after",type=Path,required=True);P.add_argument("--out",type=Path,required=True);P.add_argument("--allow-empty-partvalue-reconstruction",action="store_true");P.add_argument("--allow-partinst-userprop-order",action="store_true");A=P.parse_args();A.out.mkdir(parents=True,exist_ok=True)
def D(e):return e.find("Defn").attrib if e.find("Defn") is not None else {}
def c(e):return [e.tag,sorted(e.attrib.items()),e.text if e.text and e.text.strip() else "",[c(x) for x in e],e.tail if e.tail and e.tail.strip() else ""]
def j(v):return json.dumps(v,ensure_ascii=True,separators=(",",":"))
def h(e):return hashlib.sha256(j(c(e)).encode()).hexdigest().upper()
def fs(p):return hashlib.sha256(p.read_bytes()).hexdigest().upper()
def csvw(n,rs):
 with (A.out/n).open("w",encoding="utf-8-sig",newline="") as f:
  w=csv.DictWriter(f,fieldnames=list(rs[0]) if rs else ["none"]);w.writeheader();w.writerows(rs)
b=E.parse(A.before).getroot();a=E.parse(A.after).getroot();B=copy.deepcopy(b);A2=copy.deepcopy(a)
date_rows=[];id_rows=[];name_rows=[];jr=[];fail=[]
neutral_defaults=[];property_order=[]
if A.allow_empty_partvalue_reconstruction:
 bi={D(x).get("name"):x for x in B.findall("./Cache/Package")};ai={D(x).get("name"):x for x in A2.findall("./Cache/Package")}
 assert set(bi)==set(ai)
 for name,old in bi.items():
  new=ai[name];ol=old.findall("LibPart");nl=new.findall("LibPart");assert len(ol)==len(nl)
  for ci,(u,v) in enumerate(zip(ol,nl)):
   for view in ["NormalView","ConvertView"]:
    uv=u.find(view);vv=v.find(view)
    assert (uv is None)==(vv is None)
    if uv is None:continue
    op=uv.findall("PartValue");np=vv.findall("PartValue")
    if not op and np:
     assert len(np)==1 and set(D(np[0]))=={"name"} and D(np[0])["name"]=="",("Unexpected reconstructed default",name,ci,view)
     neutral_defaults.append({"package":name,"cell_index":ci,"view":view,"before":"ABSENT_BY_CONDITIONAL_PLAN","after":"EXPLICIT_EMPTY_PARTVALUE_NATIVE_RECONSTRUCTION","current_instances":"All active instances retain their own explicit PartValue; native effective query gate is required"})
     vv.remove(np[0])
if A.allow_partinst_userprop_order:
 for side,rr in [("before",B),("after",A2)]:
  for inst in rr.findall(".//Page/PartInst"):
   slots=[i for i,x in enumerate(list(inst)) if x.tag=="PartInstUserProp"]
   nodes=[list(inst)[i] for i in slots];ordered=sorted(nodes,key=lambda e:j(c(e)))
   if [j(c(e)) for e in nodes]!=[j(c(e)) for e in ordered]:property_order.append({"side":side,"instance_id":D(inst).get("dbId"),"property_count":len(nodes),"normalization":"Only PartInstUserProp full-content multiset order, duplicate count retained"})
   for i,e in zip(slots,ordered):inst[i]=e
idtypes={"Alias","GlobalDisplayProp","OffPageConnectorDisplayProp","PartInstDisplayProp","PortInstScalar"}
# Walk in unchanged element order; junctions are handled separately, so no
# traversal below a WireScalar needs to be correlated by child index here.
def metadata(x,y,path):
 if x.tag!=y.tag:fail.append({"kind":"ELEMENT_TAG","path":path});return
 if x.tag=="Defn":return
 if x.tag=="PageDateTime":
  date_rows.append({"path":path,"before":j(D(x)),"after":j(D(y))})
  allowed={"createDate","createTime","modifyDate","modifyTime"}
  if set(D(x))!=set(D(y)) or not set(D(x))<=allowed:fail.append({"kind":"UNEXPECTED_PAGE_DATE_FIELDS","path":path})
  for k in allowed:
   x.find("Defn").attrib.pop(k,None);y.find("Defn").attrib.pop(k,None)
  return
 xd=x.find("Defn");yd=y.find("Defn")
 if xd is not None and yd is not None:
  if x.tag=="Design":
   name_rows.append({"kind":"DESIGN_OUTPUT_PATH","path":path,"before":xd.get("name"),"after":yd.get("name")})
   xd.set("name","@OUTPUT_DSN_PATH@");yd.set("name","@OUTPUT_DSN_PATH@")
  elif x.tag=="MaxDbId":
   name_rows.append({"kind":"MAX_DB_ID","path":path,"before":xd.get("val"),"after":yd.get("val")})
   xd.set("val","@MAX_DB_ID@");yd.set("val","@MAX_DB_ID@")
  elif x.tag=="PartInst":
   if xd.get("name")!=yd.get("name"):
    if not(re.fullmatch(r"INS\d+",xd.get("name","")) and re.fullmatch(r"INS\d+",yd.get("name",""))):fail.append({"kind":"NON_GENERATED_INSTANCE_NAME_CHANGE","path":path})
    name_rows.append({"kind":"GENERATED_INSTANCE_NAME","path":path,"before":xd.get("name"),"after":yd.get("name")})
    xd.set("name","@GENERATED_INSTANCE_NAME@");yd.set("name","@GENERATED_INSTANCE_NAME@")
  if x.tag in idtypes and xd.get("dbId")!=yd.get("dbId"):
   id_rows.append({"kind":x.tag,"path":path,"before":xd.get("dbId"),"after":yd.get("dbId")})
   xd.set("dbId","@REGENERATED_DISPLAY_OR_PIN_ID@");yd.set("dbId","@REGENERATED_DISPLAY_OR_PIN_ID@")
 if x.tag in {"WireScalar","WireBus"}:return
 xx=list(x);yy=list(y)
 if len(xx)!=len(yy):fail.append({"kind":"CHILD_COUNT_OUTSIDE_WIRE","path":path,"before":len(xx),"after":len(yy)})
 for i,(u,v) in enumerate(zip(xx,yy)):metadata(u,v,path+"/"+u.tag+"["+str(i)+"]")
metadata(B,A2,"/Design")
# Alias IDs live within wires; compare their stable complete order independent
# of junction ownership and normalize only the allowed Alias/Defn/dbId.
def segment_has(w,xy):
 d=D(w)
 try:
  x,y=xy;x1=int(d["startX"]);x2=int(d["endX"]);y1=int(d["startY"]);y2=int(d["endY"])
  return (x-x1)*(y2-y1)==(y-y1)*(x2-x1) and min(x1,x2)<=x<=max(x1,x2) and min(y1,y2)<=y<=max(y1,y2)
 except Exception:return None
netrows=[];offowner=[]
bp=B.findall(".//Page");ap=A2.findall(".//Page")
assert len(bp)==len(ap)
for p,q in zip(bp,ap):
 page=D(p).get("name","");assert page==D(q).get("name","")
 nets1=[x for x in p if x.tag in {"NetScalar","NetBus"}];nets2=[x for x in q if x.tag in {"NetScalar","NetBus"}]
 assert len(nets1)==len(nets2)
 for ni,(n,m) in enumerate(zip(nets1,nets2)):
  w1=[x for x in n if x.tag in {"WireScalar","WireBus"}];w2=[x for x in m if x.tag in {"WireScalar","WireBus"}]
  assert len(w1)==len(w2)
  alljs=[[],[]];owners=[collections.Counter(),collections.Counter()]
  for wi,(u,v) in enumerate(zip(w1,w2)):
   uid=D(u).get("dbId");vid=D(v).get("dbId")
   if uid!=vid:fail.append({"kind":"WIRE_STABLE_ID_CHANGED","page":page,"net_index":ni,"wire_index":wi})
   ua=u.findall("Alias");va=v.findall("Alias")
   assert len(ua)==len(va)
   for ai,(au,av) in enumerate(zip(ua,va)):
    adu=au.find("Defn");adv=av.find("Defn")
    if adu.get("dbId")!=adv.get("dbId"):
     id_rows.append({"kind":"Alias","path":page+"/Net[%d]/Wire[%s]/Alias[%d]"%(ni,uid,ai),"before":adu.get("dbId"),"after":adv.get("dbId")})
     adu.set("dbId","@REGENERATED_DISPLAY_OR_PIN_ID@");adv.set("dbId","@REGENERATED_DISPLAY_OR_PIN_ID@")
   for side,w in enumerate((u,v)):
    for jun in list(w.findall("Junction")):
     enc=j(c(jun));alljs[side].append((enc,jun));owners[side][(D(w).get("dbId"),enc)]+=1
     dd=D(jun);xy=(int(dd["locX"]),int(dd["locY"]))
     if segment_has(w,xy) is not True:offowner.append({"side":"before" if side==0 else "after","page":page,"net_index":ni,"wire":D(w).get("dbId"),"junction":j(xy),"junction_on_owner_segment":segment_has(w,xy)})
     w.remove(jun)
  cnt1=collections.Counter(x[0] for x in alljs[0]);cnt2=collections.Counter(x[0] for x in alljs[1])
  eq=cnt1==cnt2
  netrows.append({"page":page,"net_index":ni,"net_type":n.tag,"wires":len(w1),"junctions_before":len(alljs[0]),"junctions_after":len(alljs[1]),"junction_full_multiset_equal":eq,"owner_pairs_removed":sum((owners[0]-owners[1]).values()),"owner_pairs_added":sum((owners[1]-owners[0]).values())})
  if not eq:fail.append({"kind":"JUNCTION_CONTENT_OR_MULTIPLICITY_CHANGED","page":page,"net_index":ni})
  # Keep all junction content and multiplicity; only their owner wire/order is
  # normalized, bounded to the same originally corresponding NetScalar/NetBus.
  for side,z in enumerate((n,m)):
   group=E.Element("ROUNDTRIP_JUNCTION_FULL_MULTISET")
   for enc,jun in sorted(alljs[side],key=lambda x:x[0]):group.append(jun)
   z.append(group)
  for (wid,enc),count in (owners[0]-owners[1]).items():jr.append({"page":page,"net_index":ni,"direction":"REMOVED_OWNER_PAIR","wire_id":wid,"junction_full_json":enc,"count":count})
  for (wid,enc),count in (owners[1]-owners[0]).items():jr.append({"page":page,"net_index":ni,"direction":"ADDED_OWNER_PAIR","wire_id":wid,"junction_full_json":enc,"count":count})
# Check ID changes are a bijection, do not collide with unchanged persisted IDs,
# and that all explicit reference-ID fields remain valid/unchanged.
oldnew={};newold={};offsets=collections.Counter()
for x in id_rows:
 o=x["before"];n=x["after"]
 if o in oldnew and oldnew[o]!=n:fail.append({"kind":"ID_MAPPING_NOT_FUNCTION","id":o})
 if n in newold and newold[n]!=o:fail.append({"kind":"ID_MAPPING_NOT_INJECTIVE","id":n})
 oldnew[o]=n;newold[n]=o;offsets[int(n)-int(o)]+=1
allb=[x.get("dbId") for x in b.iter() if "dbId" in x.attrib];alla=[x.get("dbId") for x in a.iter() if "dbId" in x.attrib]
unchanged=set(allb)-set(oldnew)
collision=unchanged&set(newold)
if collision:fail.append({"kind":"ID_COLLISION_WITH_UNCHANGED","ids":sorted(collision)})
refs_b=[(x.tag,k,v) for x in b.iter() for k,v in x.attrib.items() if k.lower().startswith("ref") and k.lower().endswith("id")]
refs_a=[(x.tag,k,v) for x in a.iter() for k,v in x.attrib.items() if k.lower().startswith("ref") and k.lower().endswith("id")]
if refs_b!=refs_a:fail.append({"kind":"EXPLICIT_REFERENCE_ID_FIELDS_CHANGED"})
for tag,k,v in refs_b:
 if v in oldnew:fail.append({"kind":"REGENERATED_ID_HAS_EXPLICIT_STALE_REFERENCE","field":k,"id":v})
if offowner:fail.append({"kind":"JUNCTION_NOT_ON_OWNER_SEGMENT","count":len(offowner)})
if len(oldnew)!=len(newold) or len(oldnew)!=len(id_rows):fail.append({"kind":"ID_MAPPING_NOT_ONE_ROW_PER_DISTINCT_ID"})
for side,rr in [("before",b),("after",a)]:
 for sch in rr.findall("Schematic"):
  maxnode=sch.find("MaxDbId/Defn")
  if maxnode is not None:
   maximum=int(maxnode.get("val"));ids=[int(x.get("dbId")) for x in sch.iter() if x.get("dbId", "").lstrip("-").isdigit()]
   if ids and maximum<max(ids):fail.append({"kind":"MAX_DB_ID_BELOW_EXISTING_ID","side":side})
equal=h(B)==h(A2)
if not equal:fail.append({"kind":"FULL_XML_AFTER_BOUNDED_NORMALIZATION_STILL_DIFFERS"})
s={"status":"PASS_ONLY_DOCUMENTED_ROUNDTRIP_REPRESENTATION_CHANGES" if not fail else "REVIEW_REQUIRED",
 "before_xml_sha256":fs(A.before),"after_xml_sha256":fs(A.after),"full_bounded_normalized_equal":equal,
 "generated_identity_changes":len(name_rows),"generated_id_changes":len(id_rows),"id_mapping_bijection":len(oldnew)==len(newold)==len(id_rows),
 "id_offset_counts":dict(offsets),"id_collisions_with_unchanged":len(collision),"explicit_reference_id_fields_equal":refs_b==refs_a,
 "page_date_records":len(date_rows),"net_container_count":len(netrows),"junction_multiset_failures":sum(not x["junction_full_multiset_equal"] for x in netrows),
 "junction_total_before":sum(x["junctions_before"] for x in netrows),"junction_total_after":sum(x["junctions_after"] for x in netrows),
 "junction_owner_pairs_removed":sum(x["owner_pairs_removed"] for x in netrows),"junction_owner_pairs_added":sum(x["owner_pairs_added"] for x in netrows),
 "junction_not_on_owner_segment_records":len(offowner),
 "normalization":"Generated INS names (pattern checked) + Design output path + MaxDbId + PageDateTime + explicit five allowed object ID kinds (bijective/no stale refs) + complete Junction multisets WITH DUPLICATES only within corresponding same Net container. Optional flags normalize only complete PartInstUserProp multisets in their own slots and absent-to-empty PartValue reconstruction; the latter requires a separate native effective-value proof. All other values/order retained.",
 "native_pst_electrical_gate":"REQUIRED_EXTERNAL_ROOT_RESULT","native_empty_default_reconstructions":len(neutral_defaults),"partinst_userprop_order_normalized_records":len(property_order),"failures":fail}
csvw("native_empty_default_reconstructions.csv",neutral_defaults);csvw("partinst_userprop_order_normalization.csv",property_order);csvw("junction_same_net_multisets.csv",netrows);csvw("junction_owner_reassignments.csv",jr);csvw("generated_identity_names.csv",name_rows);csvw("regenerated_id_bijection.csv",id_rows);csvw("page_date_records.csv",date_rows);csvw("junction_owner_segment_review.csv",offowner)
(A.out/"ROUNDTRIP_BOUNDED_SEMANTIC_REVIEW.json").write_text(json.dumps(s,ensure_ascii=True,indent=2)+"\n",encoding="utf-8")
print(json.dumps(s,ensure_ascii=True,indent=2))
raise SystemExit(0 if not fail else 2)
