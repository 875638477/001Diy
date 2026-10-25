set source {D:/001DIY/005lib/01AIEDA/learning/examples/de_15_26_20261019/native/de_integrated_eco_final.dsn}
set backup {D:/001DIY/005lib/01AIEDA/learning/staging/de_15_26_20261019/de_eco_before_attribute_fix.dsn}
if {[file exists $backup]} {error "Attribute fix already backed up; do not replay"}
file copy $source $backup
set s [DboState];set sess $::DboSession_s_pDboSession
set d [::DE::obj [$sess GetDesignAndSchematics [::DE::cs $source] $s] $s Open];lappend ::DE::designs $d
::DE::obj [$d GetRootOccurrence $s] $s Occurrence
set top [::DE::obj [$d GetRootSchematic $s] $s Root]
set pi [$top NewPagesIter $s];set page [::DE::obj [$pi NextPage $s] $s Page];delete_DboSchematicPagesIter $pi
set ii [$page NewPartInstsIter $s];set refs {}
for {set i [$ii NextPartInst $s]} {$i ne "NULL"} {set i [$ii NextPartInst $s]} {
 set placed [DboPartInstToDboPlacedInst $i];if {$placed eq "NULL"} {continue}
 set ref [::DE::str $placed GetReferenceDesignator]
 if {$ref in {R19 R20}} {
  if {[::DE::str $placed GetPartValue] ne "3.3k"} {error "Unexpected ECO value"}
  ::DE::prop $placed source_description {3.3k 1%}
  ::DE::state [$placed MarkModified] MarkModified
  lappend refs $ref
 }
}
delete_DboPagePartInstsIter $ii
if {[lsort $refs] ne {R19 R20}} {error "Attribute targets not found"}
::DE::save $d;::DE::state [$sess RemoveDesign $d] Close;set ::DE::designs {}
list ATTRIBUTE_ALIGNMENT_ONLY $refs
