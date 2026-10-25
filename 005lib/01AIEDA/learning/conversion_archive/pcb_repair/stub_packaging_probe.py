import csv, json, os, pathlib, shutil, subprocess, hashlib

ROOT = pathlib.Path(r'D:\001DIY\005lib\01AIEDA\learning\staging\lga1700_pcb_repair_20261023')
OUT = ROOT / 'stub_packaging_probe'
BASE = ROOT / 'ad_baseline_no_stubs'
CAD = pathlib.Path(r'C:\Program0\Cadence\SPB172')
assert not OUT.exists(), 'Refuse existing experiment root'
OUT.mkdir()
env = os.environ.copy()
env['CDSROOT'] = str(CAD)
env['PATH'] = ';'.join(map(str,[CAD/'tools/bin', CAD/'tools/capture', CAD/'tcltk/bin']))+';'+env.get('PATH','')
env['IGNORE_PROP'] = 'DEVICE'

TCL = r'''
load {C:/Program0/Cadence/spb172/tools/bin/orDb_Dll_Tcl64.dll} DboTclWriteBasic
set ::DboSession_s_pDboSession [DboTclHelper_sCreateSession]
DboSession -this $::DboSession_s_pDboSession
source {D:/001DIY/005lib/01AIEDA/learning/scripts/de_capture_helpers.tcl}
set root {@ROOT@}
set code [catch {
set s [DboState];set sess $::DboSession_s_pDboSession
set design [::DE::obj [$sess GetDesignAndSchematics [::DE::cs "$root/LGA1700.DSN"] $s] $s OpenDesign]
::DE::obj [$design GetRootOccurrence $s] $s RootOccurrence
set top [::DE::obj [$design GetRootSchematic $s] $s Top]
set objects "stage\tpage\tkind\tobject_id\tname\tnet_id\tnet_name\tgeometry"
proc netrow {stage page kind obj name geometry} {
 global objects s
 set net [$obj GetNet $s];set id {};set nn {}
 if {$net ne "NULL"} {set id [$net GetId $s];set nn [::DE::str $net GetNetName]}
 set oid {}
 catch {set oid [$obj GetId $s]}
 append objects "\n[join [list $stage $page $kind $oid $name $id $nn $geometry] \t]"
}
proc audit {stage} {
 global top s
 set pi [$top NewPagesIter $s]
 for {set page [$pi NextPage $s]} {$page ne "NULL"} {set page [$pi NextPage $s]} {
  set pn [::DE::str $page GetName]
  set ii [$page NewPartInstsIter $s]
  for {set inst [$ii NextPartInst $s]} {$inst ne "NULL"} {set inst [$ii NextPartInst $s]} {
   set placed [DboPartInstToDboPlacedInst $inst]
   set ref [::DE::str $placed GetReferenceDesignator]
   set pins [$inst NewPinsIter $s]
   for {set pin [$pins NextPin $s]} {$pin ne "NULL"} {set pin [$pins NextPin $s]} {netrow $stage $pn pin $pin "$ref.[::DE::str $pin GetPinNumber]" {}}
   delete_DboPartInstPinsIter $pins
  }
  delete_DboPagePartInstsIter $ii
  set wi [$page NewWiresIter $s]
  for {set w [$wi NextWire $s]} {$w ne "NULL"} {set w [$wi NextWire $s]} {netrow $stage $pn wire $w {} [list [::DE::point [$w GetStartPoint $s]] [::DE::point [$w GetEndPoint $s]]]}
  delete_DboPageWiresIter $wi
 }
 delete_DboSchematicPagesIter $pi
}
audit before
source {D:/001DIY/005lib/01AIEDA/learning/staging/lga1700_pcb_repair_20261023/ad_baseline_no_stubs/zero_stubs.tcl}
set count 0
set pi [$top NewPagesIter $s]
for {set page [$pi NextPage $s]} {$page ne "NULL"} {set page [$pi NextPage $s]} {
 set pn [::DE::str $page GetName]
 if {[dict exists $zeroStubs $pn]} {
  foreach point [dict get $zeroStubs $pn] {
   lassign $point x y
   set w [::DE::obj [$page NewWireScalar $s [::DE::pt $x $y] [::DE::pt [expr {$x+@LEN@}] $y]] $s NewStub]
   ::DE::prop $w AD_ZERO_LENGTH_WIRE_RESTORED 1
   ::DE::state [$w MarkModified] MarkWire
   incr count
  }
 }
}
delete_DboSchematicPagesIter $pi
audit after
if {$count!=16} {error "Count $count"}
::DE::save $design
::DE::write "$root/objects.tsv" $objects
::DE::state [$sess RemoveDesign $design] CloseDesign
dict create wires_added $count
} result opts]
::DE::write "$root/mutation_result.tcldict" [dict create code $code result $result opts $opts]
puts [dict create code $code result $result]
if {$code} {puts [dict get $opts -errorinfo]}
exit $code
'''

results=[]
for length in [1,10]:
    folder=OUT/('two_pass_len'+str(length));folder.mkdir()
    for name in ['LGA1700.DSN','allegro.cfg']:
        shutil.copy2(BASE/name,folder/name)
    script=folder/'add_stubs.tcl'
    script.write_text(TCL.replace('@ROOT@',folder.as_posix()).replace('@LEN@',str(length)),encoding='utf-8')
    proc=subprocess.run([str(CAD/'tcltk/bin/tclsh.exe'),str(script)],cwd=folder,env=env,capture_output=True,timeout=90)
    (folder/'tcl_output.txt').write_bytes(proc.stdout+proc.stderr)
    record={'variant':folder.name,'tcl_exit':proc.returncode}
    if proc.returncode==0:
        (folder/'netlist').mkdir()
        args=[str(CAD/'tools/bin/pstswp.exe'),'-pst','-d',str(folder/'LGA1700.DSN'),'-n',str(folder/'netlist'),'-c',str(folder/'allegro.cfg'),'-v','3','-l','255','-j','PCB Footprint']
        proc=subprocess.run(args,cwd=folder,env=env,capture_output=True,timeout=90)
        (folder/'pst_output.txt').write_bytes(proc.stdout+proc.stderr)
        record['pst_exit']=proc.returncode
        record['pst_error_count']=(proc.stdout+proc.stderr).count(b'ERROR(')
    results.append(record)
    (OUT/'results.json').write_text(json.dumps(results,indent=2),encoding='utf-8')
    print(json.dumps(record),flush=True)
