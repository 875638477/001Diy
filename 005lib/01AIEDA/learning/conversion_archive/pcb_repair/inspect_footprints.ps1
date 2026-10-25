param(
 [string]$SourceRoot='D:\001DIY\004computer\lga1700',
 [string]$Output='D:\001DIY\005lib\01AIEDA\learning\staging\lga1700_pcb_repair_20261023'
)
$ErrorActionPreference='Stop'
$psmRoot=Join-Path $SourceRoot '02pcb\psm'
$padRoot=Join-Path $SourceRoot '02pcb\pad'
$chip=Join-Path $SourceRoot '01sch\allegro\pstchip.dat'
$xprt=Join-Path $SourceRoot '01sch\allegro\pstxprt.dat'
function ParseDevice([string]$path){
 if(!(Test-Path -LiteralPath $path)){return [pscustomobject]@{Exists=$false;DeclaredPinCount=$null;Pins=@();DuplicatePins=@()}}
 $t=[System.IO.File]::ReadAllText($path)
 $count=[regex]::Match($t,'(?m)^PINCOUNT\s+(\d+)').Groups[1].Value
 $m=[regex]::Match($t,"(?ms)^PINORDER[ \t]+(?:'[^']*'|\S+)[ \t]+(.*?)(?=^PINUSE|^FUNCTION|^END)")
 $pins=@($m.Groups[1].Value -split '[,\s]+' | Where-Object {$_})
 return [pscustomobject]@{Exists=$true;DeclaredPinCount=if($count){[int]$count}else{$null};Pins=$pins;DuplicatePins=@($pins | Group-Object | Where-Object {$_.Count -gt 1} | ForEach-Object {$_.Name})}
}
$available=[System.Collections.Generic.List[object]]::new()
$byName=@{}
foreach($f in Get-ChildItem -LiteralPath $psmRoot -File -Filter '*.psm' | Sort-Object Name){
 $dra=Join-Path $psmRoot ($f.BaseName+'.dra')
 $txt=Join-Path $psmRoot ($f.BaseName+'.txt')
 $device=ParseDevice $txt
 $entry=[pscustomobject]@{Name=$f.BaseName;NameLength=$f.BaseName.Length;PSM=$f.FullName;PSMBytes=$f.Length;PSMSHA256=(Get-FileHash -LiteralPath $f.FullName -Algorithm SHA256).Hash;DRA=$dra;DRAExists=Test-Path -LiteralPath $dra;TXT=$txt;TXTExists=$device.Exists;DeclaredPins=$device.DeclaredPinCount;PinRecords=$device.Pins.Count;UniquePins=@($device.Pins | Sort-Object -Unique).Count;Pins=($device.Pins -join ',');DuplicatePins=($device.DuplicatePins -join ',')}
 $available.Add($entry)
 $byName[$f.BaseName]=$entry
}
$primitiveToRef=@{}
$partText=[System.IO.File]::ReadAllText($xprt)
foreach($m in [regex]::Matches($partText,"(?m)^PART_NAME\s+(\S+)\s+'([^']+)':")){$primitiveToRef[$m.Groups[2].Value]=$m.Groups[1].Value}
$parts=[System.Collections.Generic.List[object]]::new()
$chipText=[System.IO.File]::ReadAllText($chip)
foreach($m in [regex]::Matches($chipText,"(?ms)^primitive '([^']+)';(.*?)^end_primitive;")){
 $primitive=$m.Groups[1].Value;$body=$m.Groups[2].Value
 $footprint=[regex]::Match($body,"JEDEC_TYPE='([^']*)';").Groups[1].Value
 $ref=if($primitiveToRef.ContainsKey($primitive)){$primitiveToRef[$primitive]}else{''}
 $rawPins=@(foreach($pm in [regex]::Matches($body,"PIN_NUMBER='\(([^)]*)\)';")){$pm.Groups[1].Value -split ',' | ForEach-Object {$_.Trim()} | Where-Object {$_}})
 $pins=@($rawPins | Where-Object {$_ -ne '0'} | Sort-Object -Unique)
 $found=$byName.ContainsKey($footprint)
 $actual=if($found){$byName[$footprint]}else{$null}
 $have=if($actual -and $actual.Pins){@($actual.Pins -split ',')}else{@()}
 $missing=@($pins | Where-Object {$_ -notin $have})
 $extra=@($have | Where-Object {$_ -notin $pins})
 $parts.Add([pscustomobject]@{Reference=$ref;Primitive=$primitive;RequiredFootprint=$footprint;RequiredNameLength=$footprint.Length;PhysicalPinCount=$pins.Count;Pins=($pins -join ',');ZeroSectionPlaceholders=@($rawPins | Where-Object {$_ -eq '0'}).Count;PSMFound=$found;ActualPSMName=if($found){$actual.Name}else{''};CaseExact=if($found){$footprint -ceq $actual.Name}else{$false};DRAFound=if($found){$actual.DRAExists}else{$false};TXTFound=if($found){$actual.TXTExists}else{$false};SymbolPinCount=$have.Count;RequiredPinsAbsentFromSymbol=($missing -join ',');SymbolPinsAbsentFromPart=($extra -join ',');PinSetsEqual=($found -and $actual.TXTExists -and !$missing.Count -and !$extra.Count)})
}
$footprints=@($parts | Group-Object RequiredFootprint | Sort-Object Name | ForEach-Object {
 $g=$_.Group;$first=$g[0]
 [pscustomobject]@{RequiredName=$_.Name;NameLength=$_.Name.Length;PartCount=$g.Count;References=($g.Reference -join ',');PSMFound=$first.PSMFound;ActualPSMName=$first.ActualPSMName;CaseExact=$first.CaseExact;DRAFound=$first.DRAFound;TXTFound=$first.TXTFound;DifferentRequiredPinSets=@($g.Pins | Sort-Object -Unique).Count;SymbolPinCount=$first.SymbolPinCount;ExactPinSetParts=@($g | Where-Object {$_.PinSetsEqual}).Count;MissingRequiredPinParts=@($g | Where-Object {$_.RequiredPinsAbsentFromSymbol}).Count;ExtraSymbolPinParts=@($g | Where-Object {$_.SymbolPinsAbsentFromPart}).Count}
})
$candidates=[System.Collections.Generic.List[object]]::new()
foreach($n in @('r0402_pp','r0402_pp_1')){
 $a=$byName[$n]
 $candidates.Add([pscustomobject]@{RequiredName='R0402_PP_2';References=@('R4','R5');CandidateName=$a.Name;PSM=$a.PSM;DRA=$a.DRA;CandidatePins=$a.Pins;RequiredPins='1,2';PinSetEqual=@($a.Pins -split ',' | Sort-Object) -join ',' -eq '1,2';Evidence='Same R0402_PP name family and matching physical pin labels. R4/R5 were absent from the original ASCII PCB.';GeometryVerified=$false;RecommendedAutomaticRename=$false})
}
$a=$byName['ot-23-3_l2_9-w1_3-p1_90-ls2_1']
$candidates.Add([pscustomobject]@{RequiredName='SOT-23-3_L2_9-W1_3-P1_90-LS2_4-BR';References=@('Q39');CandidateName=$a.Name;PSM=$a.PSM;DRA=$a.DRA;CandidatePins=$a.Pins;RequiredPins='1,2,3';PinSetEqual=$true;Evidence='02pcb/eco.txt Q39 row already names OT-23-3_L2_9-W1_3-P1_90-LS2_1. The old ASCII PCB Pattern is SOT-23-3_L2.9-W1.3-P1.90-LS2.4-BR. This is an observed association, not a geometry check.';GeometryVerified=$false;RecommendedAutomaticRename=$false})
$padInventory=@(Get-ChildItem -LiteralPath $padRoot -File -Filter '*.pad' | Sort-Object Name | ForEach-Object {[pscustomobject]@{Name=$_.BaseName;NameLength=$_.BaseName.Length;Path=$_.FullName;Bytes=$_.Length;SHA256=(Get-FileHash -LiteralPath $_.FullName -Algorithm SHA256).Hash}})
$summary=[ordered]@{
 InspectionClientDate='2026-10-23';SourceRoot=$SourceRoot
 Inputs=@($chip,$xprt,(Join-Path $SourceRoot '02pcb\eco.txt')) | ForEach-Object {[pscustomobject]@{Path=$_;SHA256=(Get-FileHash -LiteralPath $_ -Algorithm SHA256).Hash}}
 PrimitiveCount=$parts.Count;PartReferences=@($parts.Reference | Sort-Object -Unique).Count;UnmappedPrimitives=@($parts | Where-Object {!$_.Reference}).Count
 DistinctRequiredFootprints=$footprints.Count;RequiredFootprintNamesOver31=@($footprints | Where-Object {$_.NameLength -gt 31} | Select-Object RequiredName,NameLength,References)
 AvailablePSM=$available.Count;AvailableDRA=@($available | Where-Object {$_.DRAExists}).Count;AvailableTXT=@($available | Where-Object {$_.TXTExists}).Count;AvailablePAD=$padInventory.Count
 ExactCaseMatches=@($footprints | Where-Object {$_.PSMFound -and $_.CaseExact}).Count;CaseInsensitiveOnlyMatches=@($footprints | Where-Object {$_.PSMFound -and !$_.CaseExact}).Count
 MissingFootprints=@($footprints | Where-Object {!$_.PSMFound} | Select-Object RequiredName,References,PartCount)
 FoundNamePartCount=@($parts | Where-Object {$_.PSMFound}).Count
 EqualPhysicalPinSetPartCount=@($parts | Where-Object {$_.PinSetsEqual}).Count
 MatchedNamePartsWithMissingRequiredPins=@($parts | Where-Object {$_.PSMFound -and $_.RequiredPinsAbsentFromSymbol}).Count
 MatchedNamePartsWithExtraSymbolPins=@($parts | Where-Object {$_.PSMFound -and $_.SymbolPinsAbsentFromPart}).Count
 MatchedNamePartsWithPinDifferences=@($parts | Where-Object {$_.PSMFound -and !$_.PinSetsEqual} | Select-Object Reference,RequiredFootprint,PhysicalPinCount,SymbolPinCount,RequiredPinsAbsentFromSymbol,SymbolPinsAbsentFromPart)
 CandidateMappings=$candidates
 Limits=@('Read-only file comparison; no DSN/BRD or library edits, renames, or native API calls.','Filename existence does not prove Allegro PSMPATH/PADPATH configuration.','Package pin labels are parsed from existing psm/*.txt device reports, not freshly queried from binary PSM/DRA.','PST multi-section PIN_NUMBER zero placeholders are excluded from physical pin sets.','Pin-set equality does not verify package geometry, padstack availability per symbol, electrical connectivity, or pin-to-pad placement.','Case-only differences are reported separately; Windows file matching is case insensitive.','Both candidate mappings require geometry and pad/pin placement review before use.')
}
$available | Export-Csv -LiteralPath (Join-Path $Output 'available_symbols.csv') -NoTypeInformation -Encoding UTF8
$padInventory | Export-Csv -LiteralPath (Join-Path $Output 'available_padstacks.csv') -NoTypeInformation -Encoding UTF8
$parts | Export-Csv -LiteralPath (Join-Path $Output 'required_part_pin_comparison.csv') -NoTypeInformation -Encoding UTF8
$footprints | Export-Csv -LiteralPath (Join-Path $Output 'required_footprint_map.csv') -NoTypeInformation -Encoding UTF8
$candidates | ConvertTo-Json -Depth 7 | Set-Content -LiteralPath (Join-Path $Output 'candidate_mapping.json') -Encoding UTF8
$summary | ConvertTo-Json -Depth 12 | Set-Content -LiteralPath (Join-Path $Output 'footprint_inventory.json') -Encoding UTF8
[pscustomobject]$summary | Select-Object PrimitiveCount,PartReferences,DistinctRequiredFootprints,AvailablePSM,AvailableDRA,AvailableTXT,AvailablePAD,ExactCaseMatches,CaseInsensitiveOnlyMatches,FoundNamePartCount,EqualPhysicalPinSetPartCount,MatchedNamePartsWithMissingRequiredPins,MatchedNamePartsWithExtraSymbolPins | Format-List
$summary.MissingFootprints | Format-Table -AutoSize
$summary.MatchedNamePartsWithPinDifferences | Format-Table -AutoSize
