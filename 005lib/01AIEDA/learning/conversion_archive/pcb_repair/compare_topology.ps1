param(
 [string]$NetlistDir='D:\001DIY\005lib\01AIEDA\learning\staging\lga1700_pcb_repair_20261023\trial_paths_names\netlist',
 [string]$Output='D:\001DIY\005lib\01AIEDA\learning\staging\lga1700_pcb_repair_20261023\topology_comparison.json'
)
$ErrorActionPreference = 'Stop'
$root = 'D:\001DIY\005lib\01AIEDA\learning\staging\lga1700_pcb_repair_20261023'
$pcbPath = Join-Path $root 'native_current\component_pins.tsv'
$pstPath = Join-Path $NetlistDir 'pstxnet.dat'
$pagePath = 'D:\001DIY\005lib\01AIEDA\learning\staging\lga1700_migration_20261022\native_audit_after_device_20261023\pins.tsv'
$pcbRows = @(Import-Csv -LiteralPath $pcbPath -Delimiter "`t")
$pstText = [IO.File]::ReadAllText($pstPath)
function New-Set { return ,(New-Object 'System.Collections.Generic.HashSet[string]' ([StringComparer]::OrdinalIgnoreCase)) }
function Add-ToGroup($groups, $group, $value) {
    if (!$groups.ContainsKey($group)) { $groups[$group] = New-Set }
    [void]$groups[$group].Add($value)
}
function Connected($name) { return $null -ne $name -and $name.Trim() -ne '' -and $name -ne 'NC' -and $name -ne 'nil' }
$sch = @{}
$schRefs = New-Set
$schDuplicates = New-Object 'System.Collections.Generic.List[string]'
foreach ($block in [regex]::Matches($pstText, "(?ms)^NET_NAME[ \t]*\r?\n'([^']*)'\r?\n(.*?)(?=^NET_NAME[ \t]*$|^END\.)")) {
    foreach ($node in [regex]::Matches($block.Groups[2].Value, '(?m)^NODE_NAME[ \t]+(\S+)[ \t]+(\S+)[ \t]*\r?$')) {
        $ref = $node.Groups[1].Value
        $pin = $node.Groups[2].Value
        $key = $ref + '|' + $pin
        if ($sch.ContainsKey($key)) { $schDuplicates.Add($key) }
        $sch[$key] = [pscustomobject]@{ refdes=$ref; pin=$pin; net=$block.Groups[1].Value }
        [void]$schRefs.Add($ref)
    }
}
$pcb = @{}
$pcbRefs = New-Set
$pcbDuplicates = New-Object 'System.Collections.Generic.List[string]'
foreach ($row in $pcbRows) {
    $key = $row.refdes + '|' + $row.pin
    if ($pcb.ContainsKey($key)) { $pcbDuplicates.Add($key) }
    $pcb[$key] = $row
    [void]$pcbRefs.Add($row.refdes)
}
$pages = @{}
if (Test-Path -LiteralPath $pagePath) {
    foreach ($pin in (Import-Csv -LiteralPath $pagePath -Delimiter "`t")) {
        $pages[$pin.reference + '|' + $pin.number] = $pin.page
    }
}
$missingRefs = @($schRefs | Where-Object { !$pcbRefs.Contains($_) } | Sort-Object)
$extraRefs = @($pcbRefs | Where-Object { !$schRefs.Contains($_) } | Sort-Object)
$missingRefPins = @($sch.Keys | Where-Object { !$pcbRefs.Contains($sch[$_].refdes) })
$missingPinsOnPresentRefs = @($sch.Keys | Where-Object { $pcbRefs.Contains($sch[$_].refdes) -and !$pcb.ContainsKey($_) } | Sort-Object)
$extraPinsOnPresentRefs = @($pcb.Keys | Where-Object { $schRefs.Contains($pcb[$_].refdes) -and !$sch.ContainsKey($_) } | Sort-Object)
$commonKeys = @($sch.Keys | Where-Object { $pcb.ContainsKey($_) } | Sort-Object)
$bothConnected = New-Object 'System.Collections.Generic.List[string]'
$schConnectedPcbEmpty = New-Object 'System.Collections.Generic.List[object]'
$pcbConnectedSchEmpty = New-Object 'System.Collections.Generic.List[object]'
$bothEmpty = 0
$schGroups = @{}
$pcbGroups = @{}
$schToPcb = @{}
$pcbToSch = @{}
foreach ($key in $commonKeys) {
    $sn = $sch[$key].net
    $pn = $pcb[$key].net
    $sc = Connected $sn
    $pc = Connected $pn
    if ($sc -and $pc) {
        $bothConnected.Add($key)
        Add-ToGroup $schGroups $sn $key
        Add-ToGroup $pcbGroups $pn $key
        Add-ToGroup $schToPcb $sn $pn
        Add-ToGroup $pcbToSch $pn $sn
    } elseif ($sc) {
        $schConnectedPcbEmpty.Add([pscustomobject]@{pin=$key;page=$pages[$key];sch_net=$sn;pcb_net=$pn})
    } elseif ($pc) {
        $pcbConnectedSchEmpty.Add([pscustomobject]@{pin=$key;page=$pages[$key];sch_net=$sn;pcb_net=$pn})
    } else { $bothEmpty++ }
}
function Group-Detail($direction, $name) {
    if ($direction -eq 'PCB_SPLIT_BY_SCH') {
        $children = $pcbToSch[$name]
        $allPins = $pcbGroups[$name]
    } else {
        $children = $schToPcb[$name]
        $allPins = $schGroups[$name]
    }
    $pageSet = New-Set
    foreach ($key in $allPins) { if ($pages.ContainsKey($key)) {[void]$pageSet.Add($pages[$key])} }
    $groups = @()
    foreach ($child in @($children | Sort-Object)) {
        $keys = @($allPins | Where-Object { $(if ($direction -eq 'PCB_SPLIT_BY_SCH') {$sch[$_].net} else {$pcb[$_].net}) -eq $child } | Sort-Object)
        $childPages = @($keys | ForEach-Object {$pages[$_]} | Where-Object {$_} | Sort-Object -Unique)
        $groups += [pscustomobject]@{net=$child;pin_count=$keys.Count;pages=$childPages;pins=$keys}
    }
    return [pscustomobject]@{
        net=$name
        matched_pin_count=$allPins.Count
        other_net_count=$children.Count
        page_count=$pageSet.Count
        pages=@($pageSet | Sort-Object)
        groups=$groups
    }
}
$splitNames = @($pcbToSch.Keys | Where-Object {$pcbToSch[$_].Count -gt 1})
$mergeNames = @($schToPcb.Keys | Where-Object {$schToPcb[$_].Count -gt 1})
$splitDetails = @($splitNames | ForEach-Object { Group-Detail 'PCB_SPLIT_BY_SCH' $_ } | Sort-Object matched_pin_count -Descending)
$mergeDetails = @($mergeNames | ForEach-Object { Group-Detail 'SCH_MERGES_PCB' $_ } | Sort-Object matched_pin_count -Descending)
$equivalent = New-Object 'System.Collections.Generic.List[object]'
foreach ($sn in $schToPcb.Keys) {
    if ($schToPcb[$sn].Count -ne 1) {continue}
    $pn = @($schToPcb[$sn])[0]
    if ($pcbToSch[$pn].Count -eq 1) {
        $equivalent.Add([pscustomobject]@{sch_net=$sn;pcb_net=$pn;pin_count=$schGroups[$sn].Count;names_equal=($sn -eq $pn)})
    }
}
$splitPins = New-Set
foreach ($name in $splitNames) { foreach ($key in $pcbGroups[$name]) {[void]$splitPins.Add($key)} }
$mergePins = New-Set
foreach ($name in $mergeNames) { foreach ($key in $schGroups[$name]) {[void]$mergePins.Add($key)} }
$crossPageSplit = @($splitDetails | Where-Object {$_.page_count -gt 1})
$oneSide = @($schConnectedPcbEmpty.ToArray()) + @($pcbConnectedSchEmpty.ToArray())
$pairRelationsLost = [long]0
foreach ($name in $splitNames) {
    $n = [long]$pcbGroups[$name].Count
    $allPairs = $n*($n-1)/2
    $keptPairs = [long]0
    foreach ($sn in $pcbToSch[$name]) {
        $n2 = [long]@($pcbGroups[$name] | Where-Object {$sch[$_].net -eq $sn}).Count
        $keptPairs += $n2*($n2-1)/2
    }
    $pairRelationsLost += ($allPairs-$keptPairs)
}
$pairRelationsGained = [long]0
foreach ($name in $mergeNames) {
    $n = [long]$schGroups[$name].Count
    $allPairs = $n*($n-1)/2
    $keptPairs = [long]0
    foreach ($pn in $schToPcb[$name]) {
        $n2 = [long]@($schGroups[$name] | Where-Object {$pcb[$_].net -eq $pn}).Count
        $keptPairs += $n2*($n2-1)/2
    }
    $pairRelationsGained += ($allPairs-$keptPairs)
}
$report = [ordered]@{
    status='TOPOLOGY_DIFF_FOUND'
    safe_to_direct_eco_existing_routing=$false
    comparison_basis='Case-insensitive physical reference plus physical pin number. Compare connectivity partitions after restricting to pins present and connected on both sides. Net names are labels only; anonymous names are not treated as topology changes by themselves.'
    excluded_missing_reference_policy='All pins belonging to schematic-only references are excluded from shared-pin topology comparison. Existing-reference pin-number differences and connected/unconnected changes are listed separately, not silently normalized.'
    counts=[ordered]@{
        schematic_references=$schRefs.Count;pcb_references=$pcbRefs.Count
        schematic_physical_pins=$sch.Count;pcb_physical_pins=$pcb.Count
        missing_reference_count=$missingRefs.Count;extra_reference_count=$extraRefs.Count
        excluded_pins_on_missing_references=$missingRefPins.Count
        schematic_only_pins_on_present_references=$missingPinsOnPresentRefs.Count
        pcb_only_pins_on_present_references=$extraPinsOnPresentRefs.Count
        shared_physical_pins=$commonKeys.Count;shared_connected_both=$bothConnected.Count
        shared_unconnected_both=$bothEmpty
        schematic_connected_pcb_unconnected=$schConnectedPcbEmpty.Count
        pcb_connected_schematic_unconnected=$pcbConnectedSchEmpty.Count
        sch_connected_groups_restricted=$schGroups.Count;pcb_connected_groups_restricted=$pcbGroups.Count
        sch_net_to_multiple_pcb_nets_groups=$mergeNames.Count
        pcb_net_to_multiple_sch_nets_groups=$splitNames.Count
        sch_merge_affected_shared_pins=$mergePins.Count
        pcb_split_affected_shared_pins=$splitPins.Count
        pcb_split_groups_spanning_capture_pages=$crossPageSplit.Count
        identical_pinset_net_pairs=$equivalent.Count
        identical_pinset_pairs_with_different_names=@($equivalent | Where-Object {!$_.names_equal}).Count
        identical_pinset_multpin_pairs=@($equivalent | Where-Object {$_.pin_count -gt 1}).Count
        co_net_shared_pin_pairs_lost_by_schematic=$pairRelationsLost
        co_net_shared_pin_pairs_gained_by_schematic=$pairRelationsGained
        duplicate_schematic_pin_keys=$schDuplicates.Count;duplicate_pcb_pin_keys=$pcbDuplicates.Count
    }
    missing_references=$missingRefs;extra_references=$extraRefs
    missing_pins_on_present_references=$missingPinsOnPresentRefs
    extra_pins_on_present_references=$extraPinsOnPresentRefs
    pcb_nets_split_by_schematic=$splitDetails
    schematic_nets_merging_pcb_nets=$mergeDetails
    pcb_connected_schematic_unconnected=@($pcbConnectedSchEmpty.ToArray())
    schematic_connected_pcb_unconnected=@($schConnectedPcbEmpty.ToArray())
    identical_pinset_renames=@($equivalent | Where-Object {!$_.names_equal} | Sort-Object pin_count -Descending)
    limitations=@(
        'The current PCB is an independent logical baseline; a difference does not alone prove which side is electrically correct.',
        'No compiled Altium connectivity netlist was available for an independent three-way electrical equivalence proof.',
        'Page annotations come from the earlier audited Capture DSN. The trial changes footprint names only, so annotations remain useful for locating potential cross-page fragmentation.',
        'No PST, DSN, BRD or public library file was edited; only this report and its comparison script are written.'
    )
    inputs=@($pcbPath,$pstPath,$pagePath) | ForEach-Object {[pscustomobject]@{path=$_;sha256=(Get-FileHash -LiteralPath $_ -Algorithm SHA256).Hash}}
}
if ($mergeNames.Count -eq 0 -and $splitNames.Count -eq 0 -and $oneSide.Count -eq 0 -and $schDuplicates.Count -eq 0 -and $pcbDuplicates.Count -eq 0) {
    $report.status='SHARED_PIN_TOPOLOGY_MATCH'
    # Missing references and pin-number differences still prevent an unconditional safe ECO claim.
}
$outPath = $Output
[IO.File]::WriteAllText($outPath,($report|ConvertTo-Json -Depth 12),(New-Object Text.UTF8Encoding($false)))
[pscustomobject]@{report=$outPath;status=$report.status;counts=$report.counts;largest_pcb_splits=@($splitDetails|Select-Object -First 4 net,matched_pin_count,other_net_count,pages);largest_sch_merges=@($mergeDetails|Select-Object -First 4 net,matched_pin_count,other_net_count,pages)}|ConvertTo-Json -Depth 6
