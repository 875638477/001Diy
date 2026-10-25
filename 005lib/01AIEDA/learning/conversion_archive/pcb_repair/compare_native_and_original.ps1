param([string]$Root='D:\001DIY\004computer\lga1700',[string]$Output='D:\001DIY\005lib\01AIEDA\learning\staging\lga1700_pcb_repair_20261023')
$ErrorActionPreference='Stop'
$required=Import-Csv -LiteralPath (Join-Path $Output 'required_part_pin_comparison.csv')
$chipPins=@{};foreach($r in $required){$chipPins[$r.Reference]=@($r.Pins -split ',' | Where-Object {$_})}
$sourceNets=@{}
$net='';$pending=$false
foreach($line in [System.IO.File]::ReadLines((Join-Path $Root '01sch\allegro\pstxnet.dat'))){
 if($line.Trim() -eq 'NET_NAME'){$pending=$true;continue}
 if($pending){$net=[regex]::Match($line,"^\s*'([^']+)'\s*$").Groups[1].Value;$pending=$false;continue}
 $m=[regex]::Match($line,'^NODE_NAME\s+(\S+)\s+(\S+)')
 if($m.Success){$sourceNets[$m.Groups[1].Value+'.'+$m.Groups[2].Value]=$net}
}
$nativeSummaries=[System.Collections.Generic.List[object]]::new()
$allComparisons=[System.Collections.Generic.List[object]]::new()
foreach($kind in @('native_current','native_backup')){
 $cp=Join-Path $Output ($kind+'\components.tsv');$pp=Join-Path $Output ($kind+'\component_pins.tsv')
 $comps=Import-Csv -LiteralPath $cp -Delimiter "`t";$pins=Import-Csv -LiteralPath $pp -Delimiter "`t"
 $cb=@{};foreach($c in $comps){$cb[$c.refdes]=$c}
 $pb=@{};foreach($p in $pins){if(!$pb.ContainsKey($p.refdes)){$pb[$p.refdes]=[System.Collections.Generic.List[object]]::new()};$pb[$p.refdes].Add($p)}
 $rows=@(foreach($r in $required){
  $ref=$r.Reference;$exists=$cb.ContainsKey($ref)
  $want=$chipPins[$ref];$physical=if($pb.ContainsKey($ref)){@($pb[$ref] | Where-Object {$_.physical -eq 't'} | ForEach-Object {$_.pin} | Sort-Object -Unique)}else{@()}
  $miss=@($want | Where-Object {$_ -notin $physical});$extra=@($physical | Where-Object {$_ -notin $want})
  $details=@($miss | ForEach-Object {$_+'='+$sourceNets[$ref+'.'+$_]})
  [pscustomobject]@{Snapshot=$kind;Reference=$ref;ExistsInPCB=$exists;RequiredFootprint=$r.RequiredFootprint;ActualPackage=if($exists){$cb[$ref].package}else{''};RequiredPins=$want.Count;PhysicalPins=$physical.Count;MissingRequiredPins=($miss -join ',');MissingRequiredPinNets=($details -join ';');ExtraPhysicalPins=($extra -join ',');PinSetsEqual=($exists -and !$miss.Count -and !$extra.Count)}
 })
 foreach($r in $rows){$allComparisons.Add($r)}
 $rows | Export-Csv -LiteralPath (Join-Path $Output ($kind+'_required_pin_comparison.csv')) -NoTypeInformation -Encoding UTF8
 $nativeSummaries.Add([pscustomobject]@{Snapshot=$kind;InputHashes=@($cp,$pp) | ForEach-Object {[pscustomobject]@{Path=$_;SHA256=(Get-FileHash -LiteralPath $_ -Algorithm SHA256).Hash}};Components=$comps.Count;PhysicalPinRecords=@($pins | Where-Object {$_.physical -eq 't'}).Count;MissingRequiredReferences=@($rows | Where-Object {!$_.ExistsInPCB} | ForEach-Object {$_.Reference});PCBOnlyReferences=@($cb.Keys | Where-Object {$_ -notin $chipPins.Keys});EqualPinSetParts=@($rows | Where-Object {$_.PinSetsEqual}).Count;ExistingPartsWithMissingPins=@($rows | Where-Object {$_.ExistsInPCB -and $_.MissingRequiredPins}).Count;ExistingPartsWithExtraPins=@($rows | Where-Object {$_.ExistsInPCB -and $_.ExtraPhysicalPins}).Count;ExistingPartDifferences=@($rows | Where-Object {$_.ExistsInPCB -and !$_.PinSetsEqual})})
}
function Parse([string]$line){$r=@{};foreach($f in $line.Split('|')){$i=$f.IndexOf('=');if($i -gt 0){$r[$f.Substring(0,$i)]=$f.Substring($i+1)}};return $r}
$asciiPath=Join-Path $Root 'lga1700_AD\lga1700ascii.pcbdoc'
$ascii=[System.IO.File]::ReadAllText($asciiPath)
$selected=@{};$components=@{}
foreach($m in [regex]::Matches($ascii,'(?m)^\|RECORD=Component\|[^\r\n]*')){$c=Parse $m.Value;if($c.SOURCEDESIGNATOR -match '^MH\d+$|^F_USB[13]$|^Q39$'){$selected[$c.ID]=$c.SOURCEDESIGNATOR;$components[$c.SOURCEDESIGNATOR]=$c}}
$padRows=[System.Collections.Generic.List[object]]::new();$fullPads=[System.Collections.Generic.List[object]]::new()
foreach($m in [regex]::Matches($ascii,'(?m)^\|RECORD=Pad\|[^\r\n]*')){$p=Parse $m.Value;if($selected.ContainsKey($p.COMPONENT)){$ref=$selected[$p.COMPONENT];$padRows.Add([pscustomobject]@{Reference=$ref;ComponentID=$p.COMPONENT;Pattern=$components[$ref].PATTERN;Pin=$p.NAME;NetID=$p.NET;X=$p.X;Y=$p.Y;XSize=$p.XSIZE;YSize=$p.YSIZE;Shape=$p.SHAPE;HoleSize=$p.HOLESIZE;Rotation=$p.ROTATION;Layer=$p.LAYER;Plated=$p.PLATED;UniqueID=$p.UNIQUEID});$fullPads.Add([pscustomobject]@{Reference=$ref;Pad=$p})}}
$originalSummary=@($padRows | Group-Object Reference | Sort-Object Name | ForEach-Object {
 $ref=$_.Name;$g=$_.Group;$oldPins=@($g.Pin | Sort-Object -Unique)
 $new=@(Import-Csv -LiteralPath (Join-Path $Output 'native_current\component_pins.tsv') -Delimiter "`t" | Where-Object {$_.refdes -eq $ref} | ForEach-Object {$_.pin} | Sort-Object -Unique)
 [pscustomobject]@{Reference=$ref;OriginalPattern=$g[0].Pattern;OriginalPadObjects=$g.Count;OriginalPins=$oldPins;OriginalPadNetIDs=@($g.NetID | Sort-Object -Unique);CurrentPins=$new;OriginalVsCurrentPinNamesEqual=(@($oldPins | Where-Object {$_ -notin $new}).Count -eq 0 -and @($new | Where-Object {$_ -notin $oldPins}).Count -eq 0);RequiredPins=$chipPins[$ref];RequiredPinNets=@($chipPins[$ref] | ForEach-Object {$_+'='+$sourceNets[$ref+'.'+$_]})}
})
$padRows | Export-Csv -LiteralPath (Join-Path $Output 'original_ad_target_pad_geometry.csv') -NoTypeInformation -Encoding UTF8
$fullPads | ConvertTo-Json -Depth 10 | Set-Content -LiteralPath (Join-Path $Output 'original_ad_target_pad_fields.json') -Encoding UTF8
$report=[ordered]@{InspectionClientDate='2026-10-23';NativeComparison=$nativeSummaries;OriginalADPCB=[pscustomobject]@{Path=$asciiPath;SHA256=(Get-FileHash -LiteralPath $asciiPath -Algorithm SHA256).Hash;Targets=$originalSummary};Findings=@('Both F_USB1 and F_USB3 already lack pad 2 in the original AD PCB; they have 1,3,4,5,6,7,8,9,10, with pad 9 unassigned. This is not a numbering loss introduced by Allegro conversion.','MH1 through MH4 already have only pads 1,2,3,4 in the original AD PCB. MH5 and MH7 already have only pads 4,5,6,7. All original mounting pads have NET=0 (GND). The source schematic/netlist requires sixteen GND pins per mounting part.','The observed native package pin labels equal the original AD pad labels for every inspected target present in the native component table. F_USB3 is absent from that table; the separate symbol pool must be checked before concluding its physical symbol is absent.','Q39 original three pad numbers 1,2,3 agree with both source schematic and current PCB; only its symbol/package alias is missing by the netlist-required name.');RepairImplications=@('A derived Q39 alias can preserve the existing symbol geometry and its 1,2,3 pad mapping; use the observed board package association, and validate the symbol alias/internal name natively.','Mounting-hole consistency cannot be repaired by renaming a sixteen-pin footprint that does not exist in the original board. A deliberate derived schematic/library correction to the known four physical pad numbers can preserve original board geometry and GND topology; retain original sources and record the logical-pin consolidation.','Do not assign F_USB pin 2 to physical pad 9: pin 2 is a required power node while original pad 9 is unassigned and occupies another location. The connector pin map/part intent must determine whether missing power pad 2 is intentionally omitted or the footprint must change.','R4 and R5 require R0402_PP_2; family candidates exist, but matching two pin numbers alone does not establish geometry.');Limits=@('No source, DSN, BRD, PSM, DRA or PAD file modified.','Native TSVs were supplied by the parent; this script does not execute Cadence APIs.','Original AD pad fields provide geometry evidence; native TSVs here contain pin names/nets but do not contain coordinates, so no native-coordinate equality is claimed.','Net names differ between snapshots after import; pin-set agreement is not a complete electrical connectivity comparison.')}
$report | ConvertTo-Json -Depth 14 | Set-Content -LiteralPath (Join-Path $Output 'required_vs_native_and_original_ad.json') -Encoding UTF8
$nativeSummaries | Select-Object Snapshot,Components,PhysicalPinRecords,EqualPinSetParts,ExistingPartsWithMissingPins,ExistingPartsWithExtraPins | Format-Table -AutoSize
$originalSummary | Select-Object Reference,OriginalPattern,OriginalPadObjects,@{Name='Pins';Expression={$_.OriginalPins -join ','}},OriginalVsCurrentPinNamesEqual | Format-Table -AutoSize
