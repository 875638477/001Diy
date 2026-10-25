# User standard, 2026-10-19. Native sizes are 1000 units/mm in metric mode.
namespace eval ::CapturePageDefaults {
 variable sheetSizes [dict create A4 {297000 210000} A3 {420000 297000} A2 {594000 420000} A1 {841000 594000} A0 {1189000 841000}]
 proc dimensions {{sheet A4}} {
  variable sheetSizes
  set sheet [string toupper $sheet]
  if {![dict exists $sheetSizes $sheet]} {error "Unsupported sheet size: $sheet"}
  return [dict get $sheetSizes $sheet]
 }
 proc apply {page {sheet A4}} {
  if {$page eq "NULL" || $page eq ""} {error "Missing page"}
  set sheet [string toupper $sheet]
  lassign [dimensions $sheet] width height
  # Preserve the standard 0.100 inch pin spacing as 2.540 mm.
  # A4 is the starting size; use larger sheets to keep a complete symbol legible.
  $page SetPageSizeInfo $width $height 2540 1
  set name [DboTclHelper_sMakeCString $sheet]
  set s [$page SetSizeName $name]
  if {[$s Failed]} {error "Cannot set sheet size name: $sheet"}
  set size [$page GetDocUnits 1]
  return [list [DboTclHelper_sGetCSizeX $size] [DboTclHelper_sGetCSizeY $size]]
 }
 proc requireBounds {page left top right bottom context} {
  set size [$page GetDocUnits 1]
  set w [DboTclHelper_sGetCSizeX $size];set h [DboTclHelper_sGetCSizeY $size]
  if {$left<30 || $top<30 || $right>$w-30 || $bottom>$h-45} {
   error "Layout outside selected sheet margins: $context ($left,$top,$right,$bottom), drawable $w x $h. Enlarge the sheet or revise the layout while keeping ordinary MCU symbols complete."
  }
 }
}
