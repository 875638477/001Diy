source {D:/001DIY/005lib/01AIEDA/learning/staging/de_15_26_20261019/integrated_spec.tcl}
set local $::DEspec
set items {}
foreach c [dict get $local components] {
 dict set c properties SOURCE_MODULE_PAGE [dict get $c page]
 dict set c page DE_CONTROL
 lappend items $c
}
dict set local components $items
dict set local pages {DE_CONTROL}
dict set local cross_page_nets [dict create]
::DE::create $local single
