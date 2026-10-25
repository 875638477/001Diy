"""Full ordered XML comparison: only formatting whitespace/attribute order ignored."""
from pathlib import Path
import argparse,collections,csv,hashlib,json,xml.etree.ElementTree as E
P=argparse.ArgumentParser();P.add_argument("--before",type=Path,required=True);P.add_argument("--after",type=Path,required=True);P.add_argument("--out",type=Path,required=True);A=P.parse_args();A.out.mkdir(parents=True,exist_ok=True)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest().upper()
def canon(e):return [e.tag,sorted(e.attrib.items()),e.text if e.text and e.text.strip() else "",[canon(c) for c in e],e.tail if e.tail and e.tail.strip() else ""]
def h(e):return hashlib.sha256(json.dumps(canon(e),ensure_ascii=True,separators=(",",":")).encode()).hexdigest().upper()
bs=sha(A.before);ass=sha(A.after);b=E.parse(A.before).getroot();a=E.parse(A.after).getroot()
diffs=[]
def record(path,field,old,new):diffs.append({"path":path,"field":field,"before":old,"after":new})
def walk(b,a,path):
 if b.tag!=a.tag:record(path,"ELEMENT_TAG",b.tag,a.tag);return
 for k in sorted(set(b.attrib)|set(a.attrib)):
  if b.attrib.get(k)!=a.attrib.get(k):record(path,"@"+k,b.attrib.get(k),a.attrib.get(k))
 for field in ["text","tail"]:
  bv=getattr(b,field);av=getattr(a,field);bv=bv if bv and bv.strip() else "";av=av if av and av.strip() else ""
  if bv!=av:record(path,field,bv,av)
 bl=list(b);al=list(a)
 if len(bl)!=len(al):record(path,"CHILD_COUNT",len(bl),len(al))
 for i in range(min(len(bl),len(al))):
  n=bl[i];de=n.find("Defn");ident=de.get("name") if de is not None else None
  suffix="["+str(i)+"]"+("{"+ident+"}" if ident else "")
  walk(n,al[i],path+"/"+n.tag+suffix)
 for i in range(min(len(bl),len(al)),max(len(bl),len(al))):
  record(path+"/"+str(i),"MISSING_CHILD",E.tostring(bl[i],encoding="unicode") if i<len(bl) else None,E.tostring(al[i],encoding="unicode") if i<len(al) else None)
walk(b,a,"/Design")
def section_map(r):
 out={}
 for i,n in enumerate(r):
  if n.tag=="Schematic":
   sd=n.find("Defn");sn=sd.get("name","") if sd is not None else ""
   for p in n.findall("Page"):out["Page|"+sn+"|"+p.find("Defn").get("name","")]=p
  elif n.tag=="Cache":
   for p in n:
    d=p.find("Defn");name=d.get("name","") if d is not None else ""
    out["Cache|"+p.tag+"|"+name]=p
  else:out[n.tag+"|"+str(i)]=n
 return out
bm=section_map(b);am=section_map(a);sections=[]
for key in sorted(set(bm)|set(am)):
 bh=h(bm[key]) if key in bm else None;ah=h(am[key]) if key in am else None
 sections.append({"key":key,"before_sha256":bh,"after_sha256":ah,"equal":bh==ah})
for name,rows in [("full_ordered_differences.csv",diffs),("section_hashes.csv",sections)]:
 with (A.out/name).open("w",encoding="utf-8-sig",newline="") as f:
  cols=list(rows[0]) if rows else ["none"];w=csv.DictWriter(f,fieldnames=cols);w.writeheader();w.writerows(rows)
s={"status":"EXACT_ORDERED_XML_SEMANTICS_EQUAL" if not diffs else "RAW_SEMANTIC_DIFFERENCES_REVIEW_REQUIRED",
 "before":str(A.before),"after":str(A.after),"before_sha256":bs,"after_sha256":ass,
 "difference_count":len(diffs),"difference_fields":dict(collections.Counter(x["field"] for x in diffs)),
 "section_count":len(sections),"section_different":sum(not x["equal"] for x in sections),
 "normalization":"Only XML attribute serialization order and element indentation whitespace. NO fields, IDs, dates, name, refs, property or child order omitted.",
 "first_differences":diffs[:20]}
(A.out/"FULL_XML_COMPARE_SUMMARY.json").write_text(json.dumps(s,ensure_ascii=True,indent=2)+"\n",encoding="utf-8")
assert sha(A.before)==bs and sha(A.after)==ass
print(json.dumps(s,ensure_ascii=True,indent=2))
