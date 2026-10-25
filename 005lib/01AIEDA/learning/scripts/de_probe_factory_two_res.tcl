source {D:/001DIY/005lib/01AIEDA/learning/staging/de_15_26_20261019/integrated_spec.tcl}
set ::DE::base {D:/001DIY/005lib/01AIEDA/learning/staging/de_15_26_20261019/minimal_factory}
set ::DE::logs "$::DE::base/logs"
set selected {}
foreach comp [dict get $::DEspec components] {
 if {[dict get $comp ref] in {R5 R32}} {lappend selected $comp}
}
if {[llength $selected]!=2} {error "Need two independent page RES components"}
dict set ::DEspec components $selected
dict set ::DEspec models [dict create RES [dict get $::DEspec models RES]]
dict set ::DEspec cross_page_nets [dict create]
::DE::create $::DEspec two_res
