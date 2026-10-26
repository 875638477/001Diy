"""Prepare6 publiccold jobs in unchanged main PCB units/layers/font context.
Never modifies a design or a library. Root alone invokes the native runner.
"""
from pathlib import Path
import sys,csv,json,hashlib
M=Path(__file__).parent;R=Path(r'D:\001DIY\004computer\lga1700\13shared_libraries_pc_20261025');G=R.parent/'cadence_geometry_merge_20261025';sys.path.insert(0,str(G));from sexpr import parse_many,attrs,Atom
D=M/'project6_mainfont_plan13';assert not D.exists();D.mkdir()
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest().upper()
def q(p):return json.dumps(str(p).replace('\\','/'))
def dump(p,x):p.write_text(json.dumps(x,indent=2),encoding='utf-8')
source=R/'w/all81_full15/all_textblocks.tsv';original=R/'w/final_alt13/all_textblocks.tsv';assert sha(source)==sha(original)=='D28EEA764D760E1801DE7961A2DA275A1E4D38EE45DA6E84D9A3B5C6552B05C8'
with source.open(newline='') as f:rows=list(csv.DictReader(f,delimiter='\t'))
assert [int(x['index']) for x in rows]==list(range(1,65))
allowed={'objType','userDefined','name','width','photoWidth','lineSpace','height','charSpace'}
for row in rows:
 a=attrs(parse_many(row['all_attributes'])[0]);assert set(a)==allowed and a['objType']=='paramTextBlock' and str(a['name'])==row['index']
fontfile=D/'MAIN_SOURCE64_FONT_CONTEXT.ilist';fontfile.write_text('\n'.join('('+json.dumps(row['index'])+' '+row['all_attributes']+')' for row in rows)+'\n',encoding='utf-8')
fonthelper=D/'mainfont_context.il'
fonthelper.write_text('''procedure(pc13MainFontContextApply(s)
 let((f row rows p i expected a)
  unless(equal(axlDBGetDesignUnits() '("mils" 2)) error("Main font context requires exactmils2\\n"))
  unless(null(axlDBGetDesign()->symdefs) && null(axlDBGetDesign()->padstacks) error("Font context may only be applied to an empty cold fixture\\n"))
  f=infile('''+q(fontfile)+''') rows=nil while(row=lineread(f) rows=cons(car(row) rows)) close(f) rows=reverse(rows)
  unless(length(rows)==64 error("Full unchanged source64 font context missing\\n"))
  ; Allocate all missing slots first, before setting source user-defined names.
  for(i 1 64
   unless(axlGetParam(sprintf(nil "paramTextBlock:%d" i))
    unless(equal(axlDBTextBlockCreate(1) i) error("Cannot allocate exact source font slot\\n"))))
  foreach(row rows
   expected=cadr(row) p=axlGetParam(strcat("paramTextBlock:" car(row)))
   p->width=cadr(memq('width expected)) p->height=cadr(memq('height expected))
   p->lineSpace=cadr(memq('lineSpace expected)) p->charSpace=cadr(memq('charSpace expected)) p->photoWidth=cadr(memq('photoWidth expected))
   unless(axlSetParam(p) error("Official source font parameter copy failed\\n"))
   p=axlGetParam(strcat("paramTextBlock:" car(row)))
   unless(equal(p->userDefined cadr(memq('userDefined expected)))
    unless(axlDBTextBlockSetName(atoi(car(row)) cadr(memq('userDefined expected))) error("Source font user-defined name copy failed\\n")))
   p=axlGetParam(strcat("paramTextBlock:" car(row)))
   unless(equal(p->?? expected) error("Complete original source font spec mismatch at slot%s %L %L\\n" car(row) expected p->??))
   fprintf(s "MAIN_SOURCE_FONT_EXACT\\t%s\\t%L\\n" car(row) p->??) drain(s))
  fprintf(s "MAIN_SOURCE_ALL64_FONT_CONTEXT_EXACT_COMPLETE\\n") drain(s) t))
''',encoding='utf-8')
# Use the already-proven cold-first helper; add context initialization only.
basehelper=M/'psm_native_units_alternating_v2.il';h=basehelper.read_text()
h='load('+q(fonthelper)+')\n'+h
needle='  fprintf(s "AFTER_EXTENTS\\t%L\\n" car(job)) drain(s)\n  t))'
assert needle in h;h=h.replace(needle,'  fprintf(s "AFTER_EXTENTS\\t%L\\n" car(job)) drain(s)\n  pc13MainFontContextApply(s)\n  t))')
native=M/'psm_native_units_mainfont_v1.il';assert not native.exists();native.write_text(h,encoding='utf-8')
base=M/'run_project8_mils2_cold.py';r=base.read_text();old="native=pathlib.Path(__file__).with_name('psm_native_units_alternating_v2.il')";assert old in r;r=r.replace(old,"native=pathlib.Path(__file__).with_name('psm_native_units_mainfont_v1.il')")
r=r.replace("'schema':'PROJECT8_MAIN_MILS2_FOUR_LAYER_COLD_V1'","'schema':'PROJECT6_MAIN_MILS2_FOUR_LAYER_ALL64_FONT_CONTEXT_COLD_V1'")
runner=M/'run_project6_mainfont_cold.py';assert not runner.exists();runner.write_text(r,encoding='utf-8')
plan=json.loads((M/'project8_mils2_plan13/PROJECT8_MILS2_PLAN.json').read_text())
plan['representatives']=[x for x in plan['representatives'] if x['stem'] not in ('mount_156a_p4567_pc','ddr4_dimm_288p_pc')];assert len(plan['representatives'])==6
plan['helpers'].extend({'path':str(p),'sha256':sha(p)} for p in (source,original,fontfile,fonthelper,native))
plan['purpose']='Current59 eightnew targets:6 fontsensitive public packages, same mainmils2/4layers/unchanged fullsource64 textblock table. Two exactclones already passed prior8cold. No source or PCB font edits and no ignored text fields.'
dump(D/'PROJECT6_MAINFONT_PLAN.json',plan)
receipt={'status':'PREPARED_NOT_NATIVE_RUN','font_slots':64,'all_source_font_attrs_per_slot':sorted(allowed),'source_and_current_allfont_tsv_identical_sha256':sha(source),
 'runner':str(runner),'runner_sha256':sha(runner),'native_helper':str(native),'native_helper_sha256':sha(native),
 'plan':str(D/'PROJECT6_MAINFONT_PLAN.json'),'plan_sha256':sha(D/'PROJECT6_MAINFONT_PLAN.json'),
 'font_initializer':str(fonthelper),'font_initializer_sha256':sha(fonthelper)}
dump(D/'PREPARATION.json',receipt);print(json.dumps(receipt,indent=2))
