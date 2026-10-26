# Definitions only. No DLL load, open, Save, or automatic call.
# Caller must pass the source design and a separately owned target library.
# Native signatures: DboLib.GetDefaultFont(index, DboState&) returns LOGFONT;
# SetDefaultFont(index, LOGFONT&); GetDefaultPlacedInstIsPrimitive(DboState&);
# SetDefaultPlacedInstIsPrimitive(int). Never call through a PartInst object.
namespace eval ::CaptureLibraryDefaults {}
proc ::CaptureLibraryDefaults::valid {obj} {
 if {$obj eq {} || $obj eq {NULL}} {error {NULL library/design object}}
}
proc ::CaptureLibraryDefaults::fontFields {font} {
 if {$font eq {} || $font eq {NULL}} {error {NULL LOGFONT}}
 set n [DboTclHelper_sMakeCString {}]
 DboTclHelper_sGetLFName $font $n
 set face [DboTclHelper_sGetConstCharPtr $n]
 catch {DboTclHelper_sDeleteCString $n}
 set fields [dict create Name $face]
 foreach field {Height Width Escapement Orientation Weight Italic Underline StrikeOut CharSet OutPrecision ClipPrecision Quality PitchAndFamily} {
  set cmd DboTclHelper_sGetLF$field
  dict set fields $field [$cmd $font]
 }
 return $fields
}
proc ::CaptureLibraryDefaults::getFont {lib index} {
 valid $lib
 set state [DboState]
 set font [$lib GetDefaultFont $index $state]
 if {[$state Failed]} {error "GetDefaultFont failed index=$index code=[$state Code]"}
 if {$font eq {} || $font eq {NULL}} {error "GetDefaultFont returned NULL index=$index"}
 return $font
}
proc ::CaptureLibraryDefaults::readSpec {lib} {
 valid $lib
 set spec [dict create]
 for {set i 0} {$i<24} {incr i} {
  set font [getFont $lib $i]
  dict set spec fonts $i [fontFields $font]
 }
 set state [DboState]
 set primitive [$lib GetDefaultPlacedInstIsPrimitive $state]
 if {[$state Failed]} {error "GetDefaultPlacedInstIsPrimitive failed code=[$state Code]"}
 if {$primitive ni {0 1}} {error "Unexpected primitive boolean: $primitive"}
 dict set spec DefaultPlacedInstIsPrimitive $primitive
 return $spec
}
proc ::CaptureLibraryDefaults::tsv {items} {
 set out {};foreach x $items {lappend out [string map [list \\ \\\\ \t {\t} \r {\r} \n {\n}] $x]}
 return [join $out \t]
}
proc ::CaptureLibraryDefaults::writeComparison {expected before actual report} {
 if {[file exists $report]} {error "Report already exists: $report"}
 file mkdir [file dirname $report]
 set f [open $report w];fconfigure $f -encoding utf-8 -translation lf
 puts $f [tsv {kind index field expected before actual equal}]
 set failed 0
 for {set i 0} {$i<24} {incr i} {
  foreach field [dict keys [dict get $expected fonts $i]] {
   set e [dict get $expected fonts $i $field];set b [dict get $before fonts $i $field];set a [dict get $actual fonts $i $field]
   set eq [expr {$e eq $a}];if {!$eq} {incr failed}
   puts $f [tsv [list font $i $field $e $b $a $eq]]
  }
 }
 set e [dict get $expected DefaultPlacedInstIsPrimitive];set b [dict get $before DefaultPlacedInstIsPrimitive];set a [dict get $actual DefaultPlacedInstIsPrimitive]
 set eq [expr {$e eq $a}];if {!$eq} {incr failed}
 puts $f [tsv [list library {} DefaultPlacedInstIsPrimitive $e $b $a $eq]]
 close $f
 if {$failed} {error "Default clone/readback failed $failed field(s); do not publish target"}
 return [dict create status PASS_ALL_24_FONTS_14_FIELDS_AND_PRIMITIVE font_count 24 fields_per_font 14 failures 0 report $report]
}
proc ::CaptureLibraryDefaults::cloneDefaults {source target report expectedPath} {
 valid $source;valid $target
 if {$source eq $target} {error {Source and target objects must differ}}
 if {[file exists $report] || [file exists $expectedPath]} {error {Fresh report and expected-spec output paths required}}
 # Preflight every source and target getter before any target mutation.
 set expected [readSpec $source];set before [readSpec $target]
 for {set i 0} {$i<24} {incr i} {
  # Borrow the exact source LOGFONT. Do not reconstruct omitted XML fields.
  set font [getFont $source $i]
  $target SetDefaultFont $i $font
 }
 $target SetDefaultPlacedInstIsPrimitive [dict get $expected DefaultPlacedInstIsPrimitive]
 set actual [readSpec $target]
 set result [writeComparison $expected $before $actual $report]
 file mkdir [file dirname $expectedPath]
 set f [open $expectedPath w];fconfigure $f -encoding utf-8 -translation lf
 puts $f $expected;close $f
 dict set result expected_spec $expectedPath
 dict set result save_status CURRENT_MEMORY_ONLY_CALLER_MUST_SAVE_OWNED_TARGET_AND_REOPEN_NEW_PROCESS
 return $result
}
proc ::CaptureLibraryDefaults::auditDefaults {target expectedPath report} {
 valid $target
 set f [open $expectedPath r];fconfigure $f -encoding utf-8
 set expected [string trim [read $f]];close $f
 dict size $expected
 set actual [readSpec $target]
 return [writeComparison $expected $actual $actual $report]
}
