"""Complete four actual cached/public manufacturing XML equality.

The three SMD oblong libraries are mils2 while actual0010 is mm4. Only exact
unrounded width/height unit conversion and the explicitly recorded storage
units/accuracy fields are normalized. Every other ordered XML field is exact.
"""
from pathlib import Path
from decimal import Decimal as Q
import argparse,copy,hashlib,json,xml.etree.ElementTree as E
M=Path(__file__).parent
sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest().upper()
def need(v,m):
 if not v:raise ValueError(m)
def canonical(e):return [e.tag,sorted(e.attrib.items()),(e.text or '').strip(),[canonical(c) for c in e]]
def normalized(p,side):
 q=copy.deepcopy(p);name=q.findtext('padstackname');units=q.findtext('units');accuracy=q.findtext('accuracy')
 expected=('mm','4') if side=='cached' or name=='pad_1_1d3' else ('mils','2')
 need((units,accuracy)==expected,'Unapproved actual cached/public unit/accuracy pair '+str((name,side,units,accuracy)))
 ledger=[];factor=Q('.0254') if units=='mils' else Q(1)
 for pad in q.findall('pad'):
  for child in pad:
   if child.tag in ['width','height']:
    raw=child.text;value=Q(raw)*factor;child.text='0' if value==0 else str(value.normalize());ledger.append(dict(layer=pad.findtext('layer'),type=pad.findtext('type'),field=child.tag,before=raw,after_mm=child.text,exact_factor=str(factor),rounding_applied=False))
 # No unknown dimension/schema is ignored. It remains in the complete tuple
 # and therefore causes a mismatch unless it is literally equal on both sides.
 q.find('units').text='mm';q.find('accuracy').text='4'
 return q,dict(name=name,source_format_units=units,source_format_accuracy=accuracy,physical_comparison_units='mm',only_exact_width_height_converted=ledger)
def review(cached,public):
 aa={p.findtext('padstackname'):p for p in cached};bb={p.findtext('padstackname'):p for p in public};names={'pad_1_1d3','smd_o360x300p0s10','smd_o400x640p0s10','smd_o500x400p0s10'}
 need(cached.tag==public.tag=='padstacks' and cached.attrib==public.attrib and len(cached)==len(public)==4 and set(aa)==set(bb)==names,'Full exact cached/public four-PAD cohort changed')
 need([p.findtext('padstackname') for p in cached]==[p.findtext('padstackname') for p in public],'Top ordered PAD object sequence changed')
 rows=[]
 for name in sorted(names):
  x,xl=normalized(aa[name],'cached');y,yl=normalized(bb[name],'public');need(canonical(x)==canonical(y),'Complete manufacturing XML differs after exact unit conversion '+name)
  rows.append(dict(name=name,cached_format=xl,public_format=yl,complete_ordered_payload_normalized_sha256=hashlib.sha256(json.dumps(canonical(x),separators=(',',':')).encode()).hexdigest().upper(),all_other_attributes_options_layers_masks_paste_thermal_antipad_drill_tolerance_unknown_fields_exact=True))
 return rows
def main():
 ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--export-dir',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);a=ap.parse_args();need(not a.out.exists(),'Fresh output required')
 p=a.export_dir/'CACHED_CANONICAL4_PAD_XML_NATIVE_EXPORT.json';j=json.loads(p.read_text());need(j['status']=='COMPLETE_OFFICIAL_CACHE_PUBLIC_FOUR_PAD_XML_PAIRS_REQUIRES_FULL_MANUFACTURING_REVIEW' and j['public_unchanged'] and j['board_sha256_before']==j['board_sha256_after']==sha(j['actual_board']),'Protected native official export not complete')
 need(all(x['exit_code']==0 for x in j['launches']) and len(j['launches'])==3,'Official cached/package and both PAD XML native jobs not complete')
 for row in j['rows']:
  for side in ['cached','public']:need(sha(row[side])==row[side+'_sha256'] and sha(row[side+'_xml'])==row[side+'_xml_sha256'],'Actual exported/current PAD/XML bytes changed')
 cached=E.parse(a.export_dir/'cached_padxml/pad2xml.pxml').getroot();public=E.parse(a.export_dir/'public_padxml/pad2xml.pxml').getroot();rows=review(cached,public);controls=[]
 def reject(name,fn):
  x=copy.deepcopy(cached);fn(x)
  try:review(x,public)
  except (ValueError,KeyError,AttributeError):controls.append(dict(name=name,status='PASS_REJECTED'))
  else:raise ValueError('Negative manufacturing control accepted '+name)
 reject('mask_dimension_one_mm4_grid',lambda x:x[1].findall('pad')[1].find('width').__setattr__('text','0.9653'))
 reject('copper_layer_changed',lambda x:x[1].find('pad/layer').__setattr__('text','END_LAYER'))
 reject('unknown_manufacturing_field_added',lambda x:E.SubElement(x[1],'UNAPPROVED').__setattr__('text','1'))
 reject('suppress_unconnected_changed',lambda x:x[0].find('options/supress_unconnected').__setattr__('text','N'))
 reject('duplicate_pad_definition',lambda x:x.append(copy.deepcopy(x[0])))
 reject('storage_precision_outside_exact_observed_context',lambda x:x[1].find('accuracy').__setattr__('text','3'))
 report=dict(status='PASS_ALL_FOUR_ACTUAL_CACHED_PUBLIC_FULL_MANUFACTURING_XML_EXACT_PHYSICAL_FIELDS',actual_board_sha256=j['board_sha256_before'],native_export=str(p),native_export_sha256=sha(p),canonical_packages=j['canonical_packages'],full_PADs=4,complete_ordered_pad_rows=rows,negative_controls=controls,scope='All XML fields and order retained. Three original public mils2 formats converted width/height by exact0.0254 to actual mm4; no rounding, geometric tolerance, field dropping or name-only manufacture inference.',inputs={str(Path(r[k])):sha(r[k]) for r in j['rows'] for k in ['cached','public','cached_xml','public_xml']})
 a.out.mkdir();out=a.out/'CANONICAL4_ACTUAL_CACHE_PUBLIC_FULL_PAD_XML_REVIEW.json';out.write_text(json.dumps(report,indent=2),'utf-8');print(json.dumps(dict(status=report['status'],report=str(out),sha256=sha(out)),indent=2))
if __name__=='__main__':main()
