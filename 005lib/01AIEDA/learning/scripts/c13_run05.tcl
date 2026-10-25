source {D:/001DIY/005lib/01AIEDA/learning/scripts/c13_helpers.tcl}
namespace eval ::C13 {set ds [$session GetOpenDesign [cs "$root/examples/lesson13_capture/c13_scope_v2.dsn"] $s]; saveClose $ds}
::C13::report c13_scope_v2 v2
