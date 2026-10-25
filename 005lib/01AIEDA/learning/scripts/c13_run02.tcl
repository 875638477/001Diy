source {D:/001DIY/005lib/01AIEDA/learning/scripts/c13_helpers.tcl}
namespace eval ::C13 {set enum {}; foreach n [concat [info vars ::*PRIMITIVE*] [info vars ::*SCHEMATIC*]] {if {![array exists $n]} {dict set enum $n [set $n]}}}
set ::C13::enum
