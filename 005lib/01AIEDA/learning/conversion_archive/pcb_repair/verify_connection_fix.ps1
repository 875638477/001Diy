$ErrorActionPreference='Stop'
$taskRoot=Split-Path -Parent $PSCommandPath
$before=Join-Path $taskRoot 'connection_baseline_audit';$after=Join-Path $taskRoot 'connection_fix_audit';$beforeMain=Join-Path $taskRoot 'sch_audit'
function Rows($root,$file){@(Import-Csv -LiteralPath (Join-Path $root $file) -Delimiter "`t" -Encoding UTF8)}
function Project($rows,[string[]]$fields){foreach($r in $rows){$values=@();foreach($f in $fields){$values += [string]$r.$f};$values -join "`t"}}
function Diff([string[]]$a,[string[]]$b){$d=New-Object 'System.Collections.Generic.Dictionary[string,int]' ([StringComparer]::Ordinal);foreach($x in $a){if(!$d.ContainsKey($x)){$d[$x]=0};$d[$x]++};foreach($x in $b){if(!$d.ContainsKey($x)){$d[$x]=0};$d[$x]--};$out=@();foreach($k in $d.Keys){if($d[$k] -ne 0){$out += [ordered]@{row=$k;before_minus_after_count=$d[$k]}}};return ,$out}
$origP=Rows $beforeMain 'pages.tsv';$fixedP=Rows $after 'pages.tsv'
$origI=Rows $beforeMain 'instances.tsv';$fixedI=Rows $after 'instances.tsv'
$origPins=Rows $beforeMain 'pins.tsv';$fixedPins=Rows $after 'pins.tsv'
$origA=Rows $before 'aliases.tsv';$fixedA=Rows $after 'aliases.tsv'
$origW=Rows $before 'wires.tsv';$fixedW=Rows $after 'wires.tsv'
$fixedN=Rows $after 'net_objects.tsv';$origN=Rows $before 'net_objects.tsv'
$targets=Rows (Join-Path $taskRoot 'connection_fix') 'source_identifiers_native.tsv'
$deltaPages=Diff @(Project $origP @('page','instances','pins','wires')) @(Project $fixedP @('page','instances','pins','wires'))
$deltaInst=Diff @(Project $origI @('page','reference','full_reference','value','x','y')) @(Project $fixedI @('page','reference','full_reference','value','x','y'))
$deltaPins=Diff @(Project $origPins @('page','reference','full_reference','number','name','nc','x','y')) @(Project $fixedPins @('page','reference','full_reference','number','name','nc','x','y'))
$deltaAliases=Diff @(Project $origA @('page','name','x','y','rotation','wire_points')) @(Project $fixedA @('page','name','x','y','rotation','wire_points'))
$deltaWires=Diff @(Project $origW @('page','points','object_type','line_style','line_width')) @(Project $fixedW @('page','points','object_type','line_style','line_width'))
$deltaPowers=Diff @(Project @($targets|Where-Object record -EQ '17') @('page','name','x','y')) @(Project @($fixedN|Where-Object kind -EQ 'global') @('page','name','hot_x','hot_y'))
$deltaOffpages=Diff @(Project @($targets|Where-Object record -EQ '18') @('page','name','x','y')) @(Project @($fixedN|Where-Object kind -EQ 'offpage') @('page','name','hot_x','hot_y'))
$deltaGlobalDefs=Diff @(Project $origN @('page','name','source_symbol','rotation','mirror')) @(Project @($fixedN|Where-Object kind -EQ 'global') @('page','name','source_symbol','rotation','mirror'))
$footprintDiffs=@();$lookup=@{};foreach($i in $fixedI){$lookup[$i.page+'|'+$i.full_reference]=$i};foreach($i in $origI){$other=$lookup[$i.page+'|'+$i.full_reference];if($i.footprint -cne $other.footprint){$footprintDiffs += [ordered]@{page=$i.page;reference=$i.reference;before=$i.footprint;after=$other.footprint}}}
$usb=@($fixedPins|Where-Object { $_.page -ceq 'USB32 GEN1 5G_REAR' -and (($_.reference -ceq 'Q37' -and $_.number -ceq '4') -or ($_.reference -ceq 'USB2' -and $_.number -ceq 'U6')) })
$dqs=@($fixedPins|Where-Object {$_.reference -in @('DIMMA1','DIMMB1') -and $_.name -match '^DQS[0-7]_[CT]$'})
$missingDqs=@($dqs|Where-Object net -CEQ '')
$globalNameNetConflicts=@($fixedN|Where-Object {$_.kind -ceq 'global' -and $_.name -cne $_.net})
$hashBefore=Get-Content -Raw -LiteralPath (Join-Path $after 'hashes_before.json')|ConvertFrom-Json
$hashCheck=@();foreach($h in $hashBefore){$now=(Get-FileHash -Algorithm SHA256 -LiteralPath $h.Path).Hash;$hashCheck += [ordered]@{path=$h.Path;sha256_before=$h.Hash;sha256_after=$now;unchanged=($now -ceq $h.Hash)}}
$allHashes=(@($hashCheck|Where-Object {!$_.unchanged}).Count -eq 0)
$geometryOk=($deltaPages.Count -eq 0 -and $deltaInst.Count -eq 0 -and $deltaPins.Count -eq 0 -and $deltaAliases.Count -eq 0 -and $deltaWires.Count -eq 0)
$hotspotsOk=($deltaPowers.Count -eq 0 -and $deltaOffpages.Count -eq 0 -and $deltaGlobalDefs.Count -eq 0)
$usbOk=($usb.Count -eq 2 -and @($usb|Where-Object net -CNE 'USB_PN6').Count -eq 0)
$result=[ordered]@{
 passed=($geometryOk -and $hotspotsOk -and $allHashes -and $usbOk -and $missingDqs.Count -eq 0 -and $globalNameNetConflicts.Count -eq 0)
 native_audit_exit_codes=@(0,0,0)
 counts=[ordered]@{pages=$fixedP.Count;instances=$fixedI.Count;pins=$fixedPins.Count;wires=$fixedW.Count;aliases=$fixedA.Count;globals=@($fixedN|Where-Object kind -EQ 'global').Count;ports=@($fixedN|Where-Object kind -EQ 'port').Count;offpages=@($fixedN|Where-Object kind -EQ 'offpage').Count}
 unchanged_geometry_and_aliases=$geometryOk
 page_geometry_differences=$deltaPages;instance_geometry_differences=$deltaInst;pin_geometry_differences=$deltaPins;alias_differences=$deltaAliases;wire_geometry_differences=$deltaWires
 instance_footprint_differences=$footprintDiffs
 all839_global_hotspots_match_source=($deltaPowers.Count -eq 0);global_hotspot_differences=$deltaPowers
 all1147_offpage_names_and_hotspots_match_source=($deltaOffpages.Count -eq 0);offpage_differences=$deltaOffpages
 global_symbol_identity_rotation_mirror_unchanged=($deltaGlobalDefs.Count -eq 0);global_definition_differences=$deltaGlobalDefs
 usb_target_pin_names_restored=$usbOk;usb_target_pins=$usb
 global_name_net_conflict_count=$globalNameNetConflicts.Count;global_name_net_conflicts=$globalNameNetConflicts
 dimm_dqs_target_pin_count=$dqs.Count;dimm_dqs_missing_net_count=$missingDqs.Count;dimm_dqs_pins=$dqs
 dsn_unchanged_by_readonly_audit=$allHashes;hash_checks=$hashCheck
 limits=@('Checks confirm geometry and source identifier placement, not whole-design electrical equivalence; separate PST-to-PCB topology comparison is required.','DQS0..7_C/T on DIMMA1 and DIMMB1 are the targeted DQS pins. Pins outside that set may be intentionally unused.','Read-only native audit was performed only on isolated copied DSN files. No save or property setters were invoked.')
}
$result|ConvertTo-Json -Depth 10|Set-Content -LiteralPath (Join-Path $after 'verification.json') -Encoding UTF8
[ordered]@{passed=$result.passed;counts=$result.counts;geometry_ok=$geometryOk;hotspots_ok=$hotspotsOk;usb_ok=$usbOk;missing_dqs=$missingDqs.Count;global_name_net_conflicts=$globalNameNetConflicts.Count;hashes_unchanged=$allHashes;footprint_differences=$footprintDiffs}|ConvertTo-Json -Depth 5