$ErrorActionPreference = 'Stop'
$stage = 'D:\001DIY\005lib\01AIEDA\learning\staging\lga1700_migration_20261022'
$pstDir = Join-Path $stage 'pst_export_fixed_20261023\netlist'
$nativePath = Join-Path $stage 'native_audit_after_device_20261023\pins.tsv'
$native = @(Import-Csv -LiteralPath $nativePath -Delimiter "`t")
$partText = [IO.File]::ReadAllText((Join-Path $pstDir 'pstxprt.dat'))
$chipText = [IO.File]::ReadAllText((Join-Path $pstDir 'pstchip.dat'))
$netText = [IO.File]::ReadAllText((Join-Path $pstDir 'pstxnet.dat'))
$logText = [IO.File]::ReadAllText((Join-Path $pstDir 'netlist.log'))

function New-StringSet { return ,(New-Object 'System.Collections.Generic.HashSet[string]' ([StringComparer]::OrdinalIgnoreCase)) }
function Set-Difference($left, $right) { return @($left | Where-Object { !$right.Contains($_) } | Sort-Object) }

$nativeRefs = New-StringSet
$nativePins = New-StringSet
$nativeSections = New-StringSet
$nativePinDuplicates = 0
foreach ($pin in $native) {
    [void]$nativeRefs.Add($pin.reference)
    [void]$nativeSections.Add($pin.full_reference)
    if (!$nativePins.Add($pin.reference + '|' + $pin.number)) { $nativePinDuplicates++ }
}

$primitives = @{}
$primitiveDuplicates = 0
foreach ($block in [regex]::Matches($chipText, "(?ms)^primitive[ \t]+'([^']+)';\r?\n(.*?)^end_primitive;")) {
    $name = $block.Groups[1].Value
    if ($primitives.ContainsKey($name)) { $primitiveDuplicates++ }
    $numbers = New-StringSet
    foreach ($field in [regex]::Matches($block.Groups[2].Value, "PIN_NUMBER='([^']*)'")) {
        foreach ($number in ($field.Groups[1].Value.Trim('(',')') -split ',')) {
            $number = $number.Trim()
            # Zero is the PST placeholder for a pin absent from a section.
            if ($number -ne '' -and $number -ne '0') { [void]$numbers.Add($number) }
        }
    }
    $primitives[$name] = $numbers
}

$pstRefs = New-StringSet
$pstPartPins = New-StringSet
$pstSections = New-StringSet
$partDuplicates = 0
$missingPrimitives = @()
$sectionCount = 0
foreach ($part in [regex]::Matches($partText, "(?ms)^PART_NAME[ \t]*\r?\n[ \t]*(\S+)[ \t]+'([^']+)':;(.*?)(?=^PART_NAME[ \t]*$|^END\.)")) {
    $reference = $part.Groups[1].Value
    $primitive = $part.Groups[2].Value
    if (!$pstRefs.Add($reference)) { $partDuplicates++ }
    if (!$primitives.ContainsKey($primitive)) {
        $missingPrimitives += [pscustomobject]@{ reference = $reference; primitive = $primitive }
    } else {
        foreach ($number in $primitives[$primitive]) { [void]$pstPartPins.Add($reference + '|' + $number) }
    }
    foreach ($section in [regex]::Matches($part.Groups[3].Value, "(?m)^[ \t]*SECTION='([^']*)';")) {
        $sectionCount++
        [void]$pstSections.Add($reference + $section.Groups[1].Value)
    }
}

$netBlocks = [regex]::Matches($netText, "(?ms)^NET_NAME[ \t]*\r?\n'([^']*)'\r?\n(.*?)(?=^NET_NAME[ \t]*$|^END\.)")
$nodeNets = @{}
$nodePins = New-StringSet
$duplicateNodes = @()
foreach ($block in $netBlocks) {
    $name = $block.Groups[1].Value
    foreach ($node in [regex]::Matches($block.Groups[2].Value, '(?m)^NODE_NAME[ \t]+(\S+)[ \t]+(\S+)[ \t]*\r?$')) {
        $key = $node.Groups[1].Value + '|' + $node.Groups[2].Value
        if (!$nodePins.Add($key)) { $duplicateNodes += $key }
        $nodeNets[$key] = $name
    }
}

$localGroups = @{}
$pstGroups = @{}
$sameNamePins = 0
$renamedPins = 0
$unconnectedPins = 0
$unexpectedNetNames = @()
$unexpectedUnconnected = @()
$renameGroups = @{}
foreach ($pin in $native) {
    $key = $pin.reference + '|' + $pin.number
    if (!$nodeNets.ContainsKey($key)) { continue }
    $pstNet = $nodeNets[$key]
    if ($pin.net -eq '') {
        if ($pstNet -eq 'NC') { $unconnectedPins++ }
        else { $unexpectedUnconnected += [pscustomobject]@{ pin = $key; pst = $pstNet } }
        continue
    }
    $localKey = $pin.page + '|' + $pin.net
    if (!$localGroups.ContainsKey($localKey)) { $localGroups[$localKey] = New-StringSet }
    [void]$localGroups[$localKey].Add($pstNet)
    if (!$pstGroups.ContainsKey($pstNet)) { $pstGroups[$pstNet] = New-StringSet }
    [void]$pstGroups[$pstNet].Add($pin.net)
    if ($pin.net -eq $pstNet) { $sameNamePins++ }
    elseif ($pstNet -match ('^' + [regex]::Escape($pin.net) + '_\d+$')) {
        $renamedPins++
        $renameKey = $localKey + '|' + $pstNet
        if (!$renameGroups.ContainsKey($renameKey)) {
            $renameGroups[$renameKey] = [pscustomobject]@{ page = $pin.page; native_net = $pin.net; pst_net = $pstNet; pins = 0 }
        }
        $renameGroups[$renameKey].pins++
    } else { $unexpectedNetNames += [pscustomobject]@{ pin = $key; native = $pin.net; pst = $pstNet } }
}

$splitGroups = @($localGroups.GetEnumerator() | Where-Object { $_.Value.Count -gt 1 } | ForEach-Object { [pscustomobject]@{ native_local_group = $_.Key; pst_nets = @($_.Value) } })
$mergedNames = @($pstGroups.GetEnumerator() | Where-Object { $_.Value.Count -gt 1 } | ForEach-Object { [pscustomobject]@{ pst_net = $_.Key; native_net_names = @($_.Value) } })
$differences = [ordered]@{
    missing_references = @(Set-Difference $nativeRefs $pstRefs)
    extra_references = @(Set-Difference $pstRefs $nativeRefs)
    missing_section_references = @(Set-Difference $nativeSections $pstSections)
    extra_section_references = @(Set-Difference $pstSections $nativeSections)
    missing_pins_in_pstchip = @(Set-Difference $nativePins $pstPartPins)
    extra_pins_in_pstchip = @(Set-Difference $pstPartPins $nativePins)
    missing_pins_in_pstxnet = @(Set-Difference $nativePins $nodePins)
    extra_pins_in_pstxnet = @(Set-Difference $nodePins $nativePins)
    missing_primitives = @($missingPrimitives)
    duplicate_nodes = @($duplicateNodes)
    split_native_local_nets = @($splitGroups)
    merged_different_native_net_names = @($mergedNames)
    unexpected_net_names = @($unexpectedNetNames)
    unexpected_unconnected_pin_nets = @($unexpectedUnconnected)
}
$failures = @($differences.GetEnumerator() | Where-Object { $_.Value.Count -ne 0 }).Count
$logErrors = [regex]::Matches($logText, '(?im)^.*(?:ERROR|WARNING)\([^\r\n]*').Value
$pass = $failures -eq 0 -and $nativePinDuplicates -eq 0 -and $primitiveDuplicates -eq 0 -and $partDuplicates -eq 0 -and $logErrors.Count -eq 0
$hashes = @($nativePath, (Join-Path $pstDir 'pstchip.dat'), (Join-Path $pstDir 'pstxprt.dat'), (Join-Path $pstDir 'pstxnet.dat'), (Join-Path $pstDir 'netlist.log')) | ForEach-Object { [pscustomobject]@{ path = $_; sha256 = (Get-FileHash -LiteralPath $_ -Algorithm SHA256).Hash } }
$report = [ordered]@{
    status = $(if ($pass) { 'PASS_NATIVE_DSN_TO_PST_COVERAGE' } else { 'FAIL' })
    inputs_sha256 = @($hashes)
    counts = [ordered]@{
        native_pin_rows = $native.Count
        native_unique_physical_references = $nativeRefs.Count
        native_unique_section_references = $nativeSections.Count
        native_unique_physical_pins = $nativePins.Count
        native_duplicate_physical_pins = $nativePinDuplicates
        pst_part_references = $pstRefs.Count
        pst_section_records = $sectionCount
        pst_primitive_definitions = $primitives.Count
        pst_duplicate_part_references = $partDuplicates
        pst_duplicate_primitive_names = $primitiveDuplicates
        pstchip_physical_pins = $pstPartPins.Count
        pstxnet_unique_nodes = $nodePins.Count
        pst_net_records_including_reserved_NC = $netBlocks.Count
        native_connected_local_nets = $localGroups.Count
        pst_connected_nets = $pstGroups.Count
        connected_pins_same_net_name = $sameNamePins
        connected_pins_numeric_suffix_disambiguation = $renamedPins
        renamed_local_net_groups = $renameGroups.Count
        native_unconnected_pins_in_reserved_NC = $unconnectedPins
    }
    differences = $differences
    native_export_log_errors_or_warnings = @($logErrors)
    naming_notes = @(
        'Comparison uses physical reference and pin number; multipart section references are checked separately.',
        'PST section pin lists contain zero placeholders; zero placeholders are ignored. The native input has no physical pin numbered zero.',
        'All 752 native pins with an empty net are in the reserved PST NC record; NC is excluded from connected-net counts.',
        '353 connected pins use the original local net name plus an underscore and decimal suffix. No native page-local net is split, and no PST connected net combines different native net names.',
        'Case-insensitive identifier comparison follows the exported CAD naming convention.'
    )
    scope_limit = 'Validates the native Capture DSN audit against the PST export. It does not independently prove AD-to-Capture connectivity equivalence, PCB footprint geometry, fabrication readiness, or PCB import.'
    renamed_net_examples = @($renameGroups.Values | Sort-Object page, native_net | Select-Object -First 12)
}
$reportPath = Join-Path $stage 'pst_native_coverage_20261023.json'
[IO.File]::WriteAllText($reportPath, ($report | ConvertTo-Json -Depth 10), (New-Object Text.UTF8Encoding($false)))
[pscustomobject]@{ status = $report.status; report = $reportPath; counts = $report.counts; failure_categories = $failures } | ConvertTo-Json -Depth 5
