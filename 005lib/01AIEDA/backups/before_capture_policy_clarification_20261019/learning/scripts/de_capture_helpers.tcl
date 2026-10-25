# All methods below have documented signatures and check NULL before use.
source [file join [file dirname [info script]] capture_page_defaults.tcl]
namespace eval ::DE {
 variable root {D:/001DIY/005lib/01AIEDA/learning}
 variable base "$root/examples/de_15_26_20261019"
 variable logs "$root/logs/de_15_26_20261019"
 variable designs {}; variable libs {}
 proc cs {v} {DboTclHelper_sMakeCString $v}
 proc pt {x y} {DboTclHelper_sMakeCPoint $x $y}
 proc state {s context} {if {[$s Failed]} {error "DboState failed: $context"}; return $s}
 proc obj {p s context} {state $s $context; if {$p eq "NULL" || $p eq ""} {error "NULL object: $context"}; return $p}
 proc str {p method args} {if {$p eq "NULL"} {error "NULL read $method"}; set c [cs {}]; state [$p $method {*}$args $c] $method; DboTclHelper_sGetConstCharPtr $c}
 proc point {p} {list [DboTclHelper_sGetCPointX $p] [DboTclHelper_sGetCPointY $p]}
 proc prop {p name value} {
  set s [DboState]; set old [$p SetUserPropStringValue [cs $name] [cs $value]]
  if {[$old Failed]} {obj [$p NewUserProp [cs $name] [cs $value] $s] $s "NewUserProp $name"}
 }
 proc write {path text} {file mkdir [file dirname $path];set f [open $path w];fconfigure $f -encoding utf-8 -translation lf;puts $f $text;close $f}
 proc display {part name x y} {
  set s [DboState];set dp [obj [$part NewDisplayProp $s [cs $name] [pt $x $y] 0 [DboTclHelper_sMakeLOGFONT Arial -10 0 0 0 400 0 0 0 0 7 0 1 16] 48] $s DisplayProp]
  state [$dp SetDisplayType 1] DisplayType
 }
 proc library {spec path} {
  variable libs
  if {[file exists $path]} {error "Refusing existing library $path"}
  set session $::DboSession_s_pDboSession;set s [DboState]
  set lib [obj [$session CreateLib [cs $path] $s] $s CreateLib];lappend libs $lib
  dict for {key model} [dict get $spec models] {
   set name [dict get $model name];set w [dict get $model width];set h [dict get $model height]
   set pkg [obj [$lib NewPackage [cs $name] $s] $s NewPackage]
   state [$pkg SetReferenceTemplate [cs U]] SetReferenceTemplate
   state [$pkg SetPCBFootprint [cs [dict get $model footprint]]] SetFootprint
   set cell [obj [$lib NewCell [cs $name] $s] $s NewCell]
   set part [obj [$lib NewPart [cs "$name.Normal"] $s] $s NewPart]
   state [$cell AddPart $part] AddPart;$part SetCellPtr $cell;$part SetPackagePtr $pkg
   state [$part SetBoundingBox [DboTclHelper_sMakeCRect 0 0 $w $h]] BoundingBox
   state [$part SetPartValue [cs $key]] DefaultValue
   state [$part SetReference [cs U]] DefaultReference
   state [$part SetPinNamesAreVisible [expr {[llength [dict get $model pins]]>2}]] PinNames
   state [$part SetPinNumbersAreVisible 1] PinNumbers
   foreach line [list [list 0 0 $w 0] [list $w 0 $w $h] [list $w $h 0 $h] [list 0 $h 0 0]] {
    obj [$part NewLine $s [pt {*}[lrange $line 0 1]] [pt {*}[lrange $line 2 3]] 0 0] $s BodyLine
   }
   prop $part {PCB Footprint} [dict get $model footprint]
   prop $part Source [dict get $model source]
   prop $part {Symbol Revision} DE_20261019_V1
   display $part {Part Reference} 0 -20;display $part Value 0 [expr {$h+30}]
   set pos 0
   foreach pin [dict get $model pins] {
    set p [obj [$part NewSymbolPinScalar $s [cs [dict get $pin name]] [dict get $pin type] [pt {*}[dict get $pin start]] [pt {*}[dict get $pin hot]] 1 $pos] $s NewPin]
    foreach {method value} [list SetIsLong 1 SetIsVisible 1 SetIsNumberVisible 1 SetIsNoConnect [dict get $pin library_nc] SetIsGlobal [expr {[dict get $pin type]==7}]] {state [$p $method $value] $method}
    incr pos
   }
   set dev [obj [$pkg NewDevice [cs {}] 0 $cell $s] $s NewDevice];set pos 0
   foreach pin [dict get $model pins] {
    state [$dev NewPinNumber [cs [dict get $pin number]] [DboTclHelper_sMakeInt $pos] 0 -1] PhysicalNumber;incr pos
   }
   state [$lib SavePackageAll $pkg] SavePackage
  }
  state [$session SaveLib $lib] SaveLib
  state [$session RemoveLib $lib] CloseLib;set libs [lsearch -all -inline -not -exact $libs $lib]
 }
 proc save {design} {
  set s [DboState];set top [obj [$design GetRootSchematic $s] $s Root]
  set pi [$top NewPagesIter $s]
  for {set p [$pi NextPage $s]} {$p ne "NULL"} {set p [$pi NextPage $s]} {
   state [$p MarkModified] PageModified;state [$top MarkModified $p] MarkPage;state [$top SavePage $p] SavePage
  }
  delete_DboSchematicPagesIter $pi
  state [$top MarkModified] SchematicModified;state [$design SaveSchematic $top] SaveSchematic
  state [$::DboSession_s_pDboSession MarkAllLibForSave $design] MarkAllLibForSave
  state [$::DboSession_s_pDboSession SaveDesign $design] SaveDesign
 }
 proc create {spec {tag baseline}} {
  variable base;variable logs;variable libs;variable designs
  set session $::DboSession_s_pDboSession;set s [DboState]
  # Historical table-stacking layouts mixed physical mils with document units.
  # Require a reviewed A4 placement plan before creating any output files.
  foreach c [dict get $spec components] {
   if {![dict exists $c layout]} {error "A4 layout required for [dict get $c ref]; use capture_a4_prepare.py and capture_a4_create.tcl"}
  }
  file mkdir "$base/native" "$base/library" $logs
  set libpath "$base/library/de_training_$tag.olb"
  set dsnpath "$base/native/de_integrated_$tag.dsn"
  if {[file exists $dsnpath]} {error "Refuse existing design"}
  library $spec $libpath
  set lib [obj [$session GetLib [cs $libpath] $s] $s ReopenLibrary];lappend libs $lib
  set d [obj [$session CreateDesign $s [cs $dsnpath] [cs TOP]] $s CreateDesign];lappend designs $d
  set top [obj [$d GetRootSchematic $s] $s Root]
  set pages [dict create];set cursors [dict create]
  set cap [obj [$session GetLib [cs {C:/Program0/Cadence/spb172/tools/capture/library/capsym.olb}] $s] $s Capsym];lappend libs $cap
  set off [obj [$cap GetOffPageSymbol [cs OFFPAGELEFT-L] $s] $s OffPageSymbol]
  set placement "reference\tmodule_id\tpage\tx\ty\tmodel\tfootprint\tvalue"
  foreach activePage [dict get $spec pages] {
  set page [obj [$top NewPage $s [cs $activePage]] $s NewPage]
  ::CapturePageDefaults::apply $page
  dict set pages $activePage $page
  set crossAdded [dict create]
  foreach c [dict get $spec components] {
   if {[dict get $c page] ne $activePage} {continue}
   set key [dict get $c model];set m [dict get $spec models $key];set name [dict get $m name]
   set pkg [obj [$lib GetPackage [cs $name] $s] $s Package]
   set dev [obj [$pkg GetDevice 0 $s] $s Device]
   set cell [obj [$dev GetCell $s] $s Cell];set part [obj [$cell FindPart 0 $s] $s Part]
   set pn [dict get $c page];set page [dict get $pages $pn];lassign [dict get $c layout] x y
   set h [dict get $m height]
   ::CapturePageDefaults::requireBounds $page [expr {$x-190}] [expr {$y-30}] [expr {$x+[dict get $m width]+190}] [expr {$y+$h+60}] [dict get $c ref]
   set inst [obj [$page NewPlacedInst $s [cs [str $part GetName]] [cs $name] $part $dev [pt $x $y]] $s PlacedInstance]
   state [$inst SetReference [cs [dict get $c ref]]] SetReference
   state [$inst SetPartValue [cs [dict get $c value]]] SetValue
   state [$inst SetPCBFootprint [cs [dict get $m footprint]]] SetInstanceFootprint
   dict for {k v} [dict get $c properties] {prop $inst $k $v}
   prop $inst MPN [dict get $c mpn]
   state [$inst MarkModified] InstanceModified
   foreach pin [dict get $m pins] {
    set number [dict get $pin number];set net [dict get $c pins $number]
    lassign [dict get $pin hot] px py;set ax [expr {$x+$px}];set ay [expr {$y+$py}]
    if {$net ne ""} {
     set dx [expr {[dict get $pin side] eq "left" ? -130 : 130}]
     set w [obj [$page NewWireScalar $s [pt $ax $ay] [pt [expr {$ax+$dx}] $ay]] $s PinWire]
     if {[dict exists $spec cross_page_nets $net] && ![dict exists $crossAdded $net]} {
      # Put the real off-page object on the actual pin wire, not in a detached list.
      set symname [expr {$dx<0 ? "OFFPAGELEFT-L" : "OFFPAGELEFT-R"}]
      set symbol [obj [$cap GetOffPageSymbol [cs $symname] $s] $s OffPageSymbol]
      set ex [expr {$ax+$dx}]
      set port [obj [$page NewOffPageConnector $s [cs $net] $symbol [pt $ex $ay]] $s ConnectedOffPage]
      lassign [point [$port GetHotSpot $s]] hx hy
      state [$port SetLocation [pt [expr {$ex-$hx}] [expr {$ay-$hy}]]] AlignOffPageHotSpot
      set nameprop [obj [$port GetDisplayProp [cs Name] $s] $s OffPageName]
      set textx [expr {$dx<0 ? 12 : -max(77,7*[string length $net]+15)}]
      state [$nameprop SetLocation [pt $textx 5]] OffPageNameLocation
      state [$nameprop SetFont [DboTclHelper_sMakeLOGFONT Arial -10 0 0 0 400 0 0 0 0 7 0 1 16]] OffPageNameFont
      state [$port MarkModified] OffPageModified
      dict set crossAdded $net 1
     } else {
      obj [$w NewAlias $s [cs $net] [pt [expr {$ax+($dx<0 ? -120 : 20)}] $ay] [DboTclHelper_sMakeLOGFONT Arial -10 0 0 0 400 0 0 0 0 7 0 1 16] 0 0] $s WireAlias
     }
    } else {
     set pi [$inst NewPinsIter $s]
     for {set p [$pi NextPin $s]} {$p ne "NULL"} {set p [$pi NextPin $s]} {
      if {[str $p GetPinNumber] eq $number} {state [$p SetIsNoConnect 1] InstanceNoConnect}
     }
     delete_DboPartInstPinsIter $pi
    }
   }
   append placement "\n[join [list [dict get $c ref] [dict get $c id] $pn $x $y $name [dict get $m footprint] [dict get $c value]] \t]"
  }
  state [$page MarkModified] ImmediatePageModified
  state [$top MarkModified $page] ImmediateTopModified
  state [$top SavePage $page] ImmediateSavePage
  }
  save $d
  write "$logs/placements_$tag.tsv" $placement
  state [$session RemoveDesign $d] CloseDesign;set designs [lsearch -all -inline -not -exact $designs $d]
  foreach l [list $lib $cap] {state [$session RemoveLib $l] CloseLibrary;set libs [lsearch -all -inline -not -exact $libs $l]}
  return [dict create design $dsnpath library $libpath pages [dict get $spec pages] components [llength [dict get $spec components]] models [dict size [dict get $spec models]]]
 }
 proc verify {path tag} {
  variable logs;variable designs
  set s [DboState];set sess $::DboSession_s_pDboSession
  set d [obj [$sess GetDesignAndSchematics [cs $path] $s] $s VerifyOpen];lappend designs $d
  obj [$d GetRootOccurrence $s] $s InitializePageLoad
  set top [obj [$d GetRootSchematic $s] $s VerifyRoot]
  set instrows "page\treference\tmodule_id\tvalue\tfootprint\tmpn\tx\ty"
  set proprows "reference\tproperty\tvalue"
  set pinrows "page\treference\tnumber\tname\ttype\tnc\thotx\thoty"
  set pi [$top NewPagesIter $s];set np 0;set ni 0
  for {set page [$pi NextPage $s]} {$page ne "NULL"} {set page [$pi NextPage $s]} {
   incr np;set pn [str $page GetName];set ii [$page NewPartInstsIter $s]
   for {set inst [$ii NextPartInst $s]} {$inst ne "NULL"} {set inst [$ii NextPartInst $s]} {
    incr ni;set placed [obj [DboPartInstToDboPlacedInst $inst] $s PlacedCast]
    set ref [str $placed GetReferenceDesignator]
    set module [str $inst GetEffectivePropStringValue [cs MODULE_ID]]
    set mpn [str $inst GetEffectivePropStringValue [cs MPN]]
    foreach key {ASSEMBLY assembly_group REQUIREMENTS source_description MPN_STATUS ECO_REASON} {
     if {[catch {str $inst GetEffectivePropStringValue [cs $key]} val]} {set val __ABSENT__}
     set val [string map [list \t { } \n { } \r { }] $val]
     append proprows "\n[join [list $ref $key $val] \t]"
    }
    append instrows "\n[join [concat [list $pn $ref $module [str $placed GetPartValue] [str $placed GetPCBFootprint] $mpn] [point [$inst GetLocation $s]]] \t]"
    set piter [$inst NewPinsIter $s]
    for {set p [$piter NextPin $s]} {$p ne "NULL"} {set p [$piter NextPin $s]} {
     append pinrows "\n[join [concat [list $pn $ref [str $p GetPinNumber] [str $p GetPinName] [$p GetPinType $s] [$p GetIsNoConnect $s]] [point [$p GetHotSpot $s]]] \t]"
    }
    delete_DboPartInstPinsIter $piter
   }
   delete_DboPagePartInstsIter $ii
  }
  delete_DboSchematicPagesIter $pi
  if {$np>1} {state [$top Expand] ExpandMultiPage}
  obj [$d GetRootOccurrence $s] $s RootOccurrence
  # One expansion for the multi-page TOP. Never use DboFlatNet.NewWiresIter.
  set netrows "net\tpage\treference\tnumber\tname\ttype\tflat_id"
  set fi [$d NewFlatNetsIter $s];set nf 0;set memberships 0
  for {set fn [$fi NextFlatNet $s]} {$fn ne "NULL"} {set fn [$fi NextFlatNet $s]} {
   incr nf;set netname [str $fn GetName];set fid [$fn GetId $s]
   set oi [$fn NewNetOccurrencesIter]
   for {set occ [$oi NextNetOccurrence $s]} {$occ ne "NULL"} {set occ [$oi NextNetOccurrence $s]} {
    set sn [obj [$occ GetNet $s] $s SchematicNet]
    set pins [$sn NewPortInstsIter $s]
    for {set p [$pins NextPortInst $s]} {$p ne "NULL"} {set p [$pins NextPortInst $s]} {
     set inst [obj [$p GetOwner] $s PinOwner];set placed [DboPartInstToDboPlacedInst $inst]
     if {$placed eq "NULL"} {continue}
     set page [obj [$inst GetOwner] $s PageOwner]
     append netrows "\n[join [list $netname [str $page GetName] [str $placed GetReferenceDesignator] [str $p GetPinNumber] [str $p GetPinName] [$p GetPinType $s] $fid] \t]";incr memberships
    }
    delete_DboSchematicNetPortInstsIter $pins
   }
   delete_DboFlatNetNetOccurrencesIter $oi
  }
  delete_DboDesignFlatNetsIter $fi
  write "$logs/instances_$tag.tsv" $instrows;write "$logs/pins_$tag.tsv" $pinrows;write "$logs/connectivity_$tag.tsv" $netrows
  write "$logs/properties_$tag.tsv" $proprows
  state [$sess RemoveDesign $d] VerifyClose;set designs [lsearch -all -inline -not -exact $designs $d]
  return [dict create pages $np components $ni flatnets $nf memberships $memberships]
 }
 proc cleanup {} {
  variable designs;variable libs
  foreach d $designs {if {$d ne "NULL"} {catch {$::DboSession_s_pDboSession RemoveDesign $d}}};set designs {}
  foreach l $libs {if {$l ne "NULL"} {catch {$::DboSession_s_pDboSession RemoveLib $l}}};set libs {}
 }
}
