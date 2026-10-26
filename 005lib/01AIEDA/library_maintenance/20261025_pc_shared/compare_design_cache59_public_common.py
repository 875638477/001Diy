"""Strict complete named Cache59 vs external COMMON59 and librarydefaults. No CAD."""
from pathlib import Path
from collections import Counter
import argparse,copy,hashlib,json,xml.etree.ElementTree as E
TYPES={'Package','GlobalSymbol','OffPageSymbol','PortSymbol'}
sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest().upper()
def canonical(e):
 if e is None:return None
 return [e.tag,sorted(e.attrib.items()),e.text if e.text and e.text.strip() else '',[canonical(x) for x in e],e.tail if e.tail and e.tail.strip() else '']
def digest(e):return hashlib.sha256(json.dumps(canonical(e),ensure_ascii=True,separators=(',',':')).encode()).hexdigest().upper()
def d(e):
 x=e.find('Defn')
 if x is None:raise ValueError('MissingDefn '+e.tag)
 return x
def key(e):return(e.tag,d(e).get('name'))
def review(design,lib,identity):
 assert design.tag=='Design' and lib.tag=='Lib'
 cache=design.find('Cache');assert cache is not None
 a=[e for e in cache if e.tag in TYPES];b=[e for e in lib if e.tag in TYPES]
 ax={key(e):e for e in a};bx={key(e):e for e in b}
 assert len(a)==len(ax)==len(b)==len(bx)==59,'59uniqueobjectsrequired'
 assert Counter(e.tag for e in a)==Counter(e.tag for e in b)=={'Package':55,'GlobalSymbol':3,'OffPageSymbol':1},'Cacheobjectkinds/countsdiffer'
 assert set(ax)==set(bx),'Completeobjectmembershipdiffers'
 rows=[]
 for k in sorted(ax):
  p,q=copy.deepcopy(ax[k]),copy.deepcopy(bx[k]);assert d(p).get('sourceLibName')==identity,'Cachelinkdiffers '+str(k)
  assert d(q).get('sourceLibName') in (None,''),'ExternalOLBphantomsource '+str(k)
  d(p).attrib.pop('sourceLibName',None);d(q).attrib.pop('sourceLibName',None)
  assert digest(p)==digest(q),'Completeorderedobjectdiffers '+str(k)
  rows.append({'kind':k[0],'name':k[1],'complete_ordered_normalized_sha256':digest(p),'element_count':sum(1 for _ in p.iter()),'font_nodes':sum('font' in e.tag.lower() for e in p.iter()),'pcbFootprint':d(p).get('pcbFootprint')})
 av,bv=design.find('DefaultValues'),lib.find('DefaultValues');assert av is not None and bv is not None and digest(av)==digest(bv),'AlllibrarylevelDefaultValues/Fonts differ'
 return {'objects':rows,'object_count':59,'packages':55,'network_symbols':4,'all_library_level_defaults_sha256':digest(av),'default_element_count':sum(1 for _ in av.iter()),'default_font_nodes':sum('font' in e.tag.lower() for e in av.iter()),'normalization':'OnlyobjectrootDefn/sourceLibName removed after exactcacheidentity+emptyexternalidentity checks. Fullnames,orderedchildtree,allattributes/text/tail,graphics,pins,fonts,defaults preserved. NoDBID/name/style/size whitelist.'}
def main():
 ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--design-xml',type=Path,required=True);ap.add_argument('--library-xml',type=Path,required=True);ap.add_argument('--olb',type=Path,required=True);ap.add_argument('--public-identity',required=True);ap.add_argument('--out',type=Path,required=True);ap.add_argument('--staging',action='store_true');ap.add_argument('--negative-controls',action='store_true');a=ap.parse_args();assert not a.out.exists(),'Freshoutrequired';a.out.mkdir(parents=True)
 design=E.parse(a.design_xml).getroot();lib=E.parse(a.library_xml).getroot();bindings={'design_xml':str(a.design_xml),'design_xml_sha256':sha(a.design_xml),'library_xml':str(a.library_xml),'library_xml_sha256':sha(a.library_xml),'actual_OLB':str(a.olb),'actual_OLB_sha256':sha(a.olb),'public_cache_identity':a.public_identity,'script_sha256':sha(__file__)}
 try:
  assert str(Path(d(lib).get('name')).resolve()).casefold()==str(a.olb.resolve()).casefold(),'NativeLibidentitydoesnotmatchactualOLB'
  if not a.staging:assert str(a.olb.resolve()).casefold()==str(Path(a.public_identity).resolve()).casefold(),'Finalgate requiresactualpublicpath'
  result=review(design,lib,a.public_identity);controls=[]
  if a.negative_controls:
   def test(name,fn):
    x,y=copy.deepcopy(design),copy.deepcopy(lib);fn(x,y)
    try:review(x,y,a.public_identity)
    except (AssertionError,ValueError,KeyError):controls.append({'case':name,'status':'PASS_REJECTED'})
    else:raise ValueError('Negativecontrolaccepted '+name)
   test('cache_default_FP',lambda x,y:d(x.find('Cache/Package')).set('pcbFootprint','WRONG'))
   test('cache_sourceidentity',lambda x,y:d(x.find('Cache/Package')).set('sourceLibName','WRONG'))
   test('cache_package_deleted',lambda x,y:x.find('Cache').remove(x.find('Cache/Package')))
   test('cache_package_duplicate',lambda x,y:x.find('Cache').append(copy.deepcopy(x.find('Cache/Package'))))
   test('public_package_name',lambda x,y:d(y.find('Package')).set('name','WRONG'))
   test('pin_hotspot',lambda x,y:x.find('Cache/Package//SymbolPinScalar/Defn').set('hotptX','99999'))
   test('graphic_line',lambda x,y:x.find('Cache/Package//Line/Defn').set('x1','99999'))
   test('all_library_DefaultFont_height',lambda x,y:y.find('DefaultValues/DefaultFont/Defn').set('height','99999'))
   test('all_library_DefaultFont_attr_removed',lambda x,y:y.find('DefaultValues/DefaultFont/Defn').attrib.pop('name'))
   test('network_symbol_name',lambda x,y:d(x.find('Cache/OffPageSymbol')).set('name','WRONG'))
  result.update(status='PASS_STAGED_COMMON59_EXACT_CACHE59_AND_ALL_LIBRARY_DEFAULTS_PENDING_PUBLIC_REOPEN' if a.staging else 'PASS_ACTUAL_PUBLIC_COMMON59_EXACT_CACHE59_AND_ALL_LIBRARY_DEFAULTS',negative_controls=controls)
 except Exception as ex:result={'status':'FAIL_COMPLETE_CACHE59_PUBLIC_COMMON59','error':str(ex)}
 result['inputs']=bindings;(a.out/'COMMON59_DESIGN_CACHE_FULL_REVIEW.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8');print(json.dumps({k:v for k,v in result.items() if k not in ('objects',)},ensure_ascii=False,indent=2));return 0 if result['status'].startswith('PASS') else 2
if __name__=='__main__':raise SystemExit(main())
