"""Compare complete native effective-property rows, including failed-read state.
Undefined/failed reads are never converted to blank values."""
from pathlib import Path
import argparse,collections,csv,hashlib,json
p=argparse.ArgumentParser()
p.add_argument("--before",type=Path,required=True);p.add_argument("--after",type=Path,required=True);p.add_argument("--out",type=Path,required=True)
a=p.parse_args();a.out.mkdir(parents=True,exist_ok=True)
def read(path):
 with path.open(encoding="utf-8-sig",newline="") as f:
  r=csv.DictReader(f,delimiter="\t");columns=r.fieldnames;rows=list(r)
 required={"page","instance_id","refdes","property","read_failed","state_code","value","error"}
 assert columns and set(columns)==required,("Unexpected report fields",columns)
 assert all(None not in x and None not in x.values() for x in rows),"Malformed TSV"
 return columns,rows
cb,b=read(a.before);ca,c=read(a.after);assert cb==ca,"Column order differs"
def counter(rows):return collections.Counter(tuple(x[k] for k in cb) for x in rows)
bc=counter(b);cc=counter(c);delta=[]
for kind,values in [("REMOVED",bc-cc),("ADDED",cc-bc)]:
 for values_,count in sorted(values.items()):
  delta.append({"direction":kind,"count":count,**dict(zip(cb,values_))})
with (a.out/"effective_property_row_deltas.csv").open("w",encoding="utf-8-sig",newline="") as f:
 w=csv.DictWriter(f,fieldnames=["direction","count"]+cb);w.writeheader();w.writerows(delta)
s={"status":"PASS_COMPLETE_NATIVE_EFFECTIVE_ROWS_EQUAL" if not delta else "FAIL_NATIVE_EFFECTIVE_ROWS_DIFFER",
"before_sha256":hashlib.sha256(a.before.read_bytes()).hexdigest().upper(),"after_sha256":hashlib.sha256(a.after.read_bytes()).hexdigest().upper(),
"before_rows":len(b),"after_rows":len(c),"before_failed_reads":sum(x["read_failed"]!="0" for x in b),"after_failed_reads":sum(x["read_failed"]!="0" for x in c),
"removed_rows":sum((bc-cc).values()),"added_rows":sum((cc-bc).values()),"comparison":"Full row multiset, duplicate count and failed/code/error/value preserved; instance IDs must still match."}
(a.out/"EFFECTIVE_PROPERTY_COMPARISON.json").write_text(json.dumps(s,indent=2)+"\n",encoding="utf-8")
print(json.dumps(s,indent=2));raise SystemExit(0 if not delta else 2)
