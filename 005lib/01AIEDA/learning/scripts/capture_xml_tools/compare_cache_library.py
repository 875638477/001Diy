"""Compare a Capture design cache with its separately exported OLB XML.
Full ordered Package contents are retained. The sole optional normalization is
a cache-only sourceLibName missing from the external OLB Package identity."""
from pathlib import Path
import argparse,collections,copy,csv,hashlib,json,xml.etree.ElementTree as E
p=argparse.ArgumentParser()
p.add_argument("--design",type=Path,required=True);p.add_argument("--library",type=Path,required=True);p.add_argument("--out",type=Path,required=True)
a=p.parse_args();a.out.mkdir(parents=True,exist_ok=True)
def canonical(e):return [e.tag,sorted(e.attrib.items()),e.text if e.text and e.text.strip() else "",[canonical(x) for x in e],e.tail if e.tail and e.tail.strip() else ""]
def sha(e):return hashlib.sha256(json.dumps(canonical(e),ensure_ascii=True,separators=(",",":")).encode()).hexdigest().upper()
def fs(p):return hashlib.sha256(p.read_bytes()).hexdigest().upper()
def d(e):return e.find("Defn").attrib
ds=fs(a.design);ls=fs(a.library);b=E.parse(a.design).getroot();c=E.parse(a.library).getroot()
assert b.tag=="Design" and c.tag=="Lib"
bp=b.findall("./Cache/Package");cp=c.findall("Package")
bi={d(x)["name"]:x for x in bp};ci={d(x)["name"]:x for x in cp}
assert len(bp)==len(bi) and len(cp)==len(ci),"Ambiguous package-name identity; do not collapse sources blindly"
diff=[];rows=[];identity=[]
def walk(x,y,path):
 if x.tag!=y.tag:diff.append({"path":path,"field":"TAG","before":x.tag,"after":y.tag});return
 for key in sorted(set(x.attrib)|set(y.attrib)):
  if x.get(key)!=y.get(key):diff.append({"path":path,"field":"@"+key,"before":x.get(key),"after":y.get(key)})
 for key in ["text","tail"]:
  u=getattr(x,key);v=getattr(y,key);u=u if u and u.strip() else "";v=v if v and v.strip() else ""
  if u!=v:diff.append({"path":path,"field":key,"before":u,"after":v})
 if len(x)!=len(y):diff.append({"path":path,"field":"CHILD_COUNT","before":len(x),"after":len(y)})
 for i,(u,v) in enumerate(zip(x,y)):walk(u,v,path+"/"+u.tag+"["+str(i)+"]")
 for i in range(min(len(x),len(y)),max(len(x),len(y))):diff.append({"path":path+"/"+str(i),"field":"MISSING_CHILD","before":E.tostring(x[i],encoding="unicode") if i<len(x) else None,"after":E.tostring(y[i],encoding="unicode") if i<len(y) else None})
for name in sorted(set(bi)|set(ci)):
 if name not in bi or name not in ci:
  diff.append({"path":"/Package["+name+"]","field":"PACKAGE_MISSING","before":name in bi,"after":name in ci});continue
 x=copy.deepcopy(bi[name]);y=copy.deepcopy(ci[name]);raw_equal=sha(x)==sha(y)
 if "sourceLibName" in d(x) and "sourceLibName" not in d(y):
  identity.append({"package":name,"field":"Package/Defn/@sourceLibName","cache_value":d(x).pop("sourceLibName"),"library_value":"XML_ABSENT_EXTERNAL_OLB"})
 normalized_equal=sha(x)==sha(y)
 if not normalized_equal:walk(x,y,"/Package["+name+"]")
 rows.append({"package":name,"raw_equal":raw_equal,"cache_full_sha256":sha(bi[name]),"library_full_sha256":sha(ci[name]),"normalized_full_ordered_equal":normalized_equal,"normalized_cache_sha256":sha(x),"normalized_library_sha256":sha(y)})
def write(name,items):
 with (a.out/name).open("w",encoding="utf-8-sig",newline="") as f:
  w=csv.DictWriter(f,fieldnames=list(items[0]) if items else ["none"]);w.writeheader();w.writerows(items)
write("package_full_ordered_comparison.csv",rows);write("package_differences.csv",diff);write("cache_only_source_identity.csv",identity)
symbols=[{"type":x.tag,"name":d(x).get("name",""),"full_sha256":sha(x)} for x in b.find("Cache") if x.tag in {"GlobalSymbol","OffPageSymbol","PortSymbol"}]
write("design_resident_network_symbols.csv",symbols)
db=b.find("DefaultValues");lb=c.find("DefaultValues")
defaults_equal=sha(db)==sha(lb) if db is not None and lb is not None else db is None and lb is None
package_diff=diff
diff=[]
if db is not None and lb is not None:walk(db,lb,"/DefaultValues")
elif not defaults_equal:diff.append({"path":"/DefaultValues","field":"MISSING_DEFAULTS","before":db is not None,"after":lb is not None})
write("library_default_values_differences.csv",diff)
default_differences=diff;diff=package_diff
summary={"status":("PASS_COMPLETE_PACKAGE_AND_LIBRARY_DEFAULT_VALUES" if defaults_equal else "PASS_PACKAGE_CONTENT_LIBRARY_DEFAULTS_REVIEW_REQUIRED") if not diff else "FAIL_PACKAGE_CONTENT_DIFFERS",
"design_xml_sha256":ds,"library_xml_sha256":ls,"cache_packages":len(bp),"library_packages":len(cp),"compared_packages":len(rows),"equal_packages":sum(x["normalized_full_ordered_equal"] for x in rows),"difference_count":len(diff),
"cache_only_source_identity_fields":len(identity),"normalization":"Only the cache Package/Defn sourceLibName when wholly absent from matching external OLB Package. Package names, CellName, all ordered pins/devices/views/fonts/properties/flags/graphics are exact.",
"default_values_equal":defaults_equal,"default_value_difference_count":len(default_differences),"default_values_note":"Reported separately; verify any inherited fonts/values if different. Per-object explicit fonts are included in full Package comparison.",
"design_resident_network_symbol_count":len(symbols),"network_symbol_policy":"External OLB completeness is assessed separately from network symbols retained in DSN. No cross-domain network-symbol merge.",
"native_electrical_and_independent_library_reopen":"REQUIRED_EXTERNAL_EVIDENCE"}
assert fs(a.design)==ds and fs(a.library)==ls,"Input changed during comparison"
(a.out/"CACHE_LIBRARY_FULL_XML_COMPARISON.json").write_text(json.dumps(summary,ensure_ascii=True,indent=2)+"\n",encoding="utf-8")
print(json.dumps(summary,ensure_ascii=True,indent=2));raise SystemExit(0 if not diff and defaults_equal else 2)
