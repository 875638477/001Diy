"""Prepare exactly seven CachePackage defaultFP updates, newestcn3. No CAD or librarywrites."""
from pathlib import Path
import copy,hashlib,json,subprocess,xml.etree.ElementTree as ET
M=Path(__file__).resolve().parent;R=Path(r'D:\001DIY\004computer\lga1700\13shared_libraries_pc_20261025');O=M/'capture_cache7_plan13';O.mkdir(exist_ok=True)
jr=lambda p:json.loads(Path(p).read_text('utf-8-sig'));sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest().upper()
put=lambda p,v:p.write_text(json.dumps(v,ensure_ascii=False,indent=2),encoding='utf-8')
xp=R/'w/all81_xn3/native_design.xml';dsn=R/'w/all81_cn3/LGA1700.DSN';tree=ET.parse(xp).getroot();aliases=jr(M/'nonpassive_additional_aliases13/NONPASSIVE_ADDITIONAL_ALIAS_PLAN.json');targets={r['source']:r['target'] for r in aliases['rows']}
cache=[];fullattrs={}
for e in tree.findall('./Cache/Package'):
 d=e.find('Defn');old=d.get('pcbFootprint')
 if old and old.lower() in targets:
  cache.append({'kind':'Package','name':d.get('name'),'attribute':'pcbFootprint','before':old,'after':targets[old.lower()],'xpath':"./Cache/Package/Defn[@name="+repr(d.get('name'))+"]"});fullattrs[d.get('name')]=dict(d.attrib)
assert len(cache)==7
source=jr(M/'capture_all81_plan13/ALL81_LATEST_CN2_SOURCE_PLAN.json');source.update(source_design_xml=str(xp),source_design_xml_sha256=sha(xp),source_xml_sha256=sha(xp),source_DSN=str(dsn),source_DSN_sha256=sha(dsn),cache_default_pcb_footprint_changes=cache,cache_default_CN3_before_full_attribute_audit=fullattrs,pcb_footprint_changes=[],scope='ExactlysevennamedCachePackageDefn pcbFootprint defaults. All1131explicitFP,Values,NC,3118source identities,fonts/graphics/geometry unchanged.',allowed_source_identity_mutations=0)
sourcepath=O/'CACHE7_LATEST_CN3_SOURCE_PLAN.json';put(sourcepath,source)
oldmap={str(r['dbid']):r for r in jr(R/'w/pcb_migration/FINAL_INSTANCE_MAPPING.json')};mapping=[]
for page in tree.findall('./Schematic/Page'):
 for e in page.findall('PartInst'):
  d=e.find('Defn');p={x.find('Defn').get('name'):x.find('Defn').get('val') for x in e.findall('PartInstUserProp')};row=copy.deepcopy(oldmap[d.get('dbId')]);row.update(old_footprint=p['PCB Footprint'],proposed_target=p['PCB Footprint'],target=p['PCB Footprint']);mapping.append(row)
assert len(mapping)==1131
mappath=O/'CACHE7_COMPLETE_1131_UNCHANGED_FP_MAP.json';put(mappath,mapping)
compiler=O/'compile_cache7_guards_only.py';text=(R/'tools/compile_capture13_native_plan.py').read_text('utf-8');assert text.count('assert len(fpchanges)>0')==1;text=text.replace('assert len(fpchanges)>0','assert len(fpchanges)==0, "Cache7 must not edit instanceFP"');compiler.write_text(text,encoding='utf-8')
compiled=O/'compiled';assert not compiled.exists(),'Fresh compiler output required'
subprocess.run([r'C:\Users\Administrator\.local\bin\python3.15.exe',str(compiler),'--source-plan',str(sourcepath),'--instance-map',str(mappath),'--out',str(compiled),'--new-source-identity',r'D:\001DIY\005LIB\01CAPTURELIB\COMMON_PC.OLB'],check=True)
native=(M/'capture_all81_plan13/apply_all81_capture_footprints_only.tcl').read_text('utf-8')
block='''# Bind exactcached DboPackage via the proven placed-instance GetPackage API.
# PublicOLB sameDboPackage GetPCBFootprint/SetPCBFootprint are already nativelyproven.
if {![info exists cacheDefaultPlan] || [dict size $cacheDefaultPlan] != 7 || [dict size $footprintPlan] != 0} {error {Cache7 exactplan required}}
set defaultBound {}
dict for {ikey ibinding} $instanceBound {
 if {[lindex $ikey 0] ne {PartInst}} {continue}
 lassign $ibinding inst placed guard
 set s [DboState];set pkg [::LAY::obj [$inst GetPackage $s] $s GetCachedPackageViaInstance]
 set pn [::LAY::str $pkg GetName]
 if {![dict exists $cacheDefaultPlan $pn]} {continue}
 set r [dict get $cacheDefaultPlan $pn]
 if {[$pkg GetObjectType] ne $::DboBaseObject_PACKAGE} {error "CachePackage type differs: $pn"}
 if {[::LAY::str $pkg GetPCBFootprint] ne [dict get $r before]} {error "Cachedefault exactbefore differs: $pn"}
 if {![dict exists $defaultBound $pn]} {dict set defaultBound $pn [list $pkg $r]}
}
if {[dict size $defaultBound] != 7} {error {CachePackage exactseven selection incomplete}}
set f [::LAY::channel $reportDir CACHE_DEFAULT_FP_IMMEDIATE_READBACK.tsv {package before after}]
dict for {pn binding} $defaultBound {
 lassign $binding pkg r
 ::LAY::state [$pkg SetPCBFootprint [::LAY::cs [dict get $r after]]] "CachePCBFootprint $pn"
 if {[::LAY::str $pkg GetPCBFootprint] ne [dict get $r after]} {error "Cachedefault immediate readback differs: $pn"}
 puts $f [::LAY::row [list $pn [dict get $r before] [dict get $r after]]]
}
close $f
'''
needle='set f [::LAY::channel $reportDir FOOTPRINT_IMMEDIATE_READBACK.tsv';assert native.count(needle)==1;native=native.replace(needle,block+needle);native=native.replace('# SOT34FPonly.','# Cache7defaultsOnly.');native=native.replace('Source edits forbidden in SOT34 plan','Source edits forbidden in Cache7 plan');native=native.replace('footprint_changes [dict size $footprintPlan] pages','footprint_changes [dict size $footprintPlan] cache_default_footprint_changes [dict size $cacheDefaultPlan] pages')
script=O/'apply_capture_cache7_defaults_only.tcl';script.write_text(native,encoding='utf-8')
tp=compiled/'CAPTURE13_FROZEN_PLAN.tcl';t=tp.read_text('utf-8');t+='\nset cacheDefaultPlan [dict create]\n'
q=lambda s:'"'+str(s).replace('\\','\\\\').replace('"','\\"').replace('$','\\$').replace('[','\\[').replace(']','\\]')+'"'
for r in cache:t+='dict set cacheDefaultPlan '+q(r['name'])+' [dict create before '+q(r['before'])+' after '+q(r['after'])+']\n'
tp.write_text(t,encoding='utf-8')
plan=jr(compiled/'CAPTURE13_FROZEN_PLAN.json');assert not plan['pcb_footprint_changes'];plan['cache_default_pcb_footprint_changes']=cache;plan['native_script']=str(script);put(compiled/'CAPTURE13_FROZEN_PLAN.json',plan)
supsource=M/'all81_published12_superset_plan13/CAPTURE13_PUBLISHED12_ALL81_SUPERSET_PLAN.json';sup=jr(supsource);sup['cache_default_pcb_footprint_changes']=cache;sup['scope']+=' ExactlysevenCachePackage defaultpcbFootprint attribute edits.';sup['cache7_additional_binding']={'plan':str(compiled/'CAPTURE13_FROZEN_PLAN.json'),'sha256':sha(compiled/'CAPTURE13_FROZEN_PLAN.json')};sp=O/'PUBLISHED12_ALL1031_FP_AND_CACHE7_SUPERSET_PLAN.json';put(sp,sup)
check=O/'check_cache7_tcl_only.tcl';check.write_text('set f [open {'+str(script).replace('\\','/')+'} r]\nset s [read $f];close $f\nif {![info complete $s]} {error {IncompleteTcl}}\nsource {'+str(tp).replace('\\','/')+'}\nif {[dict size $cacheDefaultPlan]!=7 || [dict size $footprintPlan]!=0 || [dict size $instanceGuards]!=3118 || [llength $sourceSelectors]!=231} {error {Wrongexactcounts}}\nputs {PASS Tclsyntax+frozenguards;noCAD}\n',encoding='utf-8');subprocess.run([r'C:\Program0\cadence\SPB172\tcltk\bin\tclsh.exe',str(check)],check=True)
report={'status':'CACHE7_ONLY_NATIVE_PLAN_PREPARED_NO_CAD','source_DSN':str(dsn),'source_DSN_sha256':sha(dsn),'source_XML':str(xp),'source_XML_sha256':sha(xp),'exact_cache_default_changes':cache,'explicit_instance_FP_changes':0,'all1131_part_instances_3118_sources_231cache_bindings_guarded':True,'native_script':str(script),'native_script_sha256':sha(script),'local_plan':str(compiled/'CAPTURE13_FROZEN_PLAN.json'),'local_plan_sha256':sha(compiled/'CAPTURE13_FROZEN_PLAN.json'),'plan_Tcl':str(tp),'plan_Tcl_sha256':sha(tp),'published12_superset_plan':str(sp),'published12_superset_plan_sha256':sha(sp),'native_argv':'inputDSN freshTargetDSN planTcl freshReportDirectory','root_required':'Freshcn4+independentreopen; fullXML exact7inverse; publicCOMMON_PC same7default edits+full59objects/font/defaultproof; allactive1131FP must remainexplicitunchanged.'};put(O/'CACHE7_PLAN_READY.json',report);print(json.dumps({k:v for k,v in report.items() if k!='exact_cache_default_changes'},indent=2))
