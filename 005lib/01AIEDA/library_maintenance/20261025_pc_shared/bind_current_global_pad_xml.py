"""Bind current public PAD bytes to prior full native XML, then recompute every classified XML field. Read only."""
from pathlib import Path
from collections import defaultdict
import argparse,hashlib,importlib.util,json,xml.etree.ElementTree as ET
B=Path(r'D:\001DIY\004computer\lga1700\cadence_geometry_merge_20261025')
sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest().upper()
def jr(p):return json.loads(Path(p).read_text(encoding='utf-8-sig'))
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--review',type=Path,required=True);ap.add_argument('--guard',type=Path,required=True);ap.add_argument('--output',type=Path,required=True);a=ap.parse_args();a.output.mkdir(exist_ok=True)
 module=B/'analyze_pad_geometry.py';spec=importlib.util.spec_from_file_location('full_pad_xml_offline',module);g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
 catalog=B/'pad_geometry_groups.json';old=jr(catalog);bysha=defaultdict(list)
 for r in old['definitions']:bysha[r['sha256'].upper()].append(r)
 guards={x['path'].lower():x for x in jr(a.guard)['files']}
 used={}
 for p in a.review.glob('e[0-9]*_SCHEMA_GEOMETRY.json'):
  for e in jr(p):
   for d in e['actual_loaded_pad_files']:used[d['path'].lower()]=d
 xmlcache={};xmlhash={};rows=[];errors=[]
 for key,d in sorted(used.items()):
  p=Path(d['path']);h=sha(p);guard=guards.get(str(p).lower())
  if not guard or h!=guard['sha256'] or h!=d['sha256']:errors.append({'pad':str(p),'error':'CURRENT_NATIVE_OR_FROZEN_SHA_BINDING_FAILED'});continue
  candidates=bysha[h]
  oldrow=next((r for r in candidates if r['path'].lower()==str(p).lower()),candidates[0] if candidates else None)
  if oldrow is None:errors.append({'pad':str(p),'sha256':h,'error':'NO_CURRENT_BYTE_IDENTICAL_PRIOR_NATIVE_XML_SOURCE'});continue
  if oldrow['native_source_sha256'].upper()!=h:errors.append({'pad':str(p),'error':'OLD_NATIVE_SOURCE_BINDING_FAILED'});continue
  xp=Path(oldrow['native_xml_path'])
  if str(xp) not in xmlcache:
   root=ET.parse(xp).getroot();ix=defaultdict(list)
   for el in root.findall('padstack'):ix[(el.findtext('padstackname') or '').lower()].append(el)
   xmlcache[str(xp)]=ix;xmlhash[str(xp)]=sha(xp)
  found=xmlcache[str(xp)][oldrow['native_exported_name'].lower()]
  if len(found)!=1:errors.append({'pad':str(p),'error':'NATIVE_XML_OBJECT_MISSING_OR_AMBIGUOUS'});continue
  el=found[0];unknown=sorted({x.tag for x in el.iter()}-g.KNOWN_TAGS)
  if unknown:errors.append({'pad':str(p),'error':'UNKNOWN_MANUFACTURING_XML_FIELDS','unknown':unknown});continue
  factor=g.FACTORS[el.findtext('units')];signature=g.digest(g.canonical(el,factor,g.IGNORED))
  if signature!=oldrow['geometry_signature']:errors.append({'pad':str(p),'error':'RECOMPUTED_FULL_SCHEMA_SIGNATURE_DIFFERENT'});continue
  refs=[{'kind':x.tag,'name':(x.text or '').strip()} for x in el.iter() if x.tag in ('shapename','flashname') and (x.text or '').strip()]
  rows.append({'path':str(p),'current_sha256':h,'native_loaded_pad_name':d['source_name'],'original_native_exported_name':oldrow['native_exported_name'],'native_xml_path':str(xp),'native_xml_sha256':xmlhash[str(xp)],'full_native_xml_object_sha256':hashlib.sha256(ET.tostring(el)).hexdigest().upper(),'all_classified_manufacturing_fields_signature':signature,'all_manufacturing_fields_except_drill_symbol_signature':g.digest(g.canonical(el,factor,g.IGNORED|{'drillsymbol'})),'parts':{k:g.part(el,factor,k) for k in ('copper','mask_paste','thermal_antipad','drill','drillsymbol','behavior')},'geometry_mm':g.summary(el,factor),'custom_shape_flash_references_preserved_not_erased':refs})
 report={'status':'CURRENT_LOADED_PAD_BYTES_BOUND_TO_COMPLETE_PRIOR_NATIVE_XML_RECOMPUTED' if not errors else 'PARTIAL_COMPLETE_PAD_XML_COVERAGE_REQUIRES_MISSING_NATIVE_EXPORTS','loaded_unique_pad_files':len(used),'full_native_xml_bound':len(rows),'errors':errors,'guard_manifest':str(a.guard),'guard_manifest_sha256':sha(a.guard),'prior_catalog':str(catalog),'prior_catalog_sha256':sha(catalog),'canonicalizer':str(module),'canonicalizer_sha256':sha(module),'records':rows,'limits':['All fields of known full PAD XML schema are preserved except padstackname/units/accuracy representation normalized to exact mm.','Different SHAPE/FLASH names remain different; this report does not erase unresolved helper shapes or infer they are identical.','Prior XML evidence is reused only for exact current PAD SHA bytes and recomputed object signatures, not by old file name alone.','No current file or old evidence was modified; this is not a consolidation or deletion result.']}
 (a.output/'FULL_PAD_XML_BINDING.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
 print(json.dumps({k:v for k,v in report.items() if k not in ('records','limits')},ensure_ascii=False))
if __name__=='__main__':main()
