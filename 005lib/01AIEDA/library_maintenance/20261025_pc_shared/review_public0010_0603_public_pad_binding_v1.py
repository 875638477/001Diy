"""Bind actual candidate 0603 padstacks to current public PSM/PAD/full native XML."""
from pathlib import Path
from collections import Counter
import hashlib,json,re,sys
M=Path(__file__).parent
G=Path('D:/001DIY/004computer/lga1700/cadence_geometry_merge_20261025')
sys.path.insert(0,str(G))
from compare_native_geometry import Native
sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest().upper()
def profile(path):
 n=Native(path)
 root=next(k for k,(a,p) in n.nodes.items() if str(a.get('objType'))=='padstack')
 rootdata=n.nodes[root][0];assert rootdata['name']=='SMD_O360X300P0S10'
 # Compare the complete default padstack and each complete pad independently;
 # the board has 10 copper layers and the public cold fixture has 4.
 rootdata.pop('pads')
 root_signature=n.node(root)
 outer=[];internal={}
 for k,(a,p) in n.nodes.items():
  if str(a.get('objType'))!='pad':continue
  layer=str(a['layer']);typ=str(a['type'])
  if re.fullmatch(r'ETCH/L(?:AYER)?\d+',layer):
   assert a.get('figureName')=='NULL',('Nonempty internal layer cannot be context-normalized',layer,a)
   a['layer']='ETCH/INTERNAL_DEFAULT_EMPTY'
   internal.setdefault(layer,[]).append((typ,n.node(k)))
  else:outer.append((layer,typ,n.node(k)))
 assert len(internal)>0 and len(outer)==12 and not n.issues and not n.unknown
 specs={tuple(sorted(v)) for v in internal.values()};assert len(specs)==1
 return dict(root_signature=root_signature,outer_mask_paste_and_thermal_full_pad_signatures=sorted(outer),internal_empty_default_specification=sorted(next(iter(specs))),actual_internal_expansion_layers=sorted(internal),issues=n.issues,unclassified_numeric_fields=dict(n.unknown))
def main():
 bindings=json.loads((M/'global_canonical_targets_review13/FULL_PAD_XML_BINDING.json').read_text('utf-8-sig'))
 xml=next(x for x in bindings['records'] if x['native_loaded_pad_name'].casefold()=='smd_o360x300p0s10')
 assert sha(xml['path'])==xml['current_sha256'] and sha(xml['native_xml_path'])==xml['native_xml_sha256']
 rows=[]
 for target,actualfile,cold in [('c0603_pc','def_0065.sexp','e00002'),('r0603_pc','def_0066.sexp','e00032')]:
  ap=M/'w/module0010_partial_full27'/actualfile
  mf=M/'global_canonical_targets_native13'/cold/'manifest.json';manifest=json.loads(mf.read_text('utf-8-sig'));assert len(manifest)==1
  cp=Path(manifest[0]['audit_output']);psm=Path(manifest[0]['path']);assert manifest[0]['stem']==target and sha(psm)==manifest[0]['source_sha256']
  a=profile(ap);b=profile(cp)
  for k in ['root_signature','outer_mask_paste_and_thermal_full_pad_signatures','internal_empty_default_specification']:assert a[k]==b[k],(target,k)
  rows.append(dict(target=target,current_public_psm=str(psm),current_public_psm_sha256=sha(psm),actual_board_cache_native=str(ap),actual_board_cache_native_sha256=sha(ap),public_cold_native=str(cp),public_cold_native_sha256=sha(cp),cold_manifest=str(mf),cold_manifest_sha256=sha(mf),complete_padstack_root_properties_signature=a['root_signature'],complete_outer_mask_paste_thermal_pad_signatures=a['outer_mask_paste_and_thermal_full_pad_signatures'],all_internal_default_specs_empty_and_exact=True,board_internal_default_expansions=a['actual_internal_expansion_layers'],public_fixture_internal_expansions=b['actual_internal_expansion_layers'],zero_numeric_tolerance=True,zero_unclassified_fields=True))
 report=dict(status='PASS_ACTUAL_0603_PADSTACK_COMPLETE_PUBLIC_DEFINITION_BINDING_WITH_EXACT_EMPTY_INTERNAL_LAYER_EXPANSION',candidate_board_sha256='1ABA0FDC27DE553535CDE454840EA245CBEBB5FDC1392A0B07E0218D11CDE26A',scope='Complete physical padstack, outer copper/thermal/antipad/mask/paste fields and every internal empty default; this is not a full PSM body/text/cache graph claim.',public_PAD_complete_native_XML_binding=xml,public_PAD_binding_catalog=str(M/'global_canonical_targets_review13/FULL_PAD_XML_BINDING.json'),public_PAD_binding_catalog_sha256=sha(M/'global_canonical_targets_review13/FULL_PAD_XML_BINDING.json'),native_comparator=str(G/'compare_native_geometry.py'),native_comparator_sha256=sha(G/'compare_native_geometry.py'),rows=rows)
 out=M/'public0010_source25_owner_probe_run13_v2/ACTUAL_0603_COMPLETE_PUBLIC_PAD_BINDING.json';out.write_text(json.dumps(report,indent=2)+'\n','utf-8');print(json.dumps(dict(report=str(out),sha256=sha(out)),indent=2))
if __name__=='__main__':main()
