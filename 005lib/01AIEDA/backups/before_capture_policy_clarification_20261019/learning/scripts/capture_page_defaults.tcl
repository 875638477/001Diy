# User standard, 2026-10-19. Native sizes are 1000 units/mm in metric mode.
namespace eval ::CapturePageDefaults {
 proc apply {page} {
  if {$page eq "NULL" || $page eq ""} {error "Missing page"}
  # Preserve the standard 0.100 inch pin spacing as 2.540 mm.
  $page SetPageSizeInfo 297000 210000 2540 1
  set name [DboTclHelper_sMakeCString A4]
  set s [$page SetSizeName $name]
  if {[$s Failed]} {error "Cannot set A4 size name"}
  set size [$page GetDocUnits 1]
  return [list [DboTclHelper_sGetCSizeX $size] [DboTclHelper_sGetCSizeY $size]]
 }
 proc requireBounds {page left top right bottom context} {
  set size [$page GetDocUnits 1]
  set w [DboTclHelper_sGetCSizeX $size];set h [DboTclHelper_sGetCSizeY $size]
  if {$left<30 || $top<30 || $right>$w-30 || $bottom>$h-45} {
   error "A4 layout outside reserved margins: $context ($left,$top,$right,$bottom), drawable $w x $h. Split the page."
  }
 }
}
