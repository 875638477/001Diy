$ErrorActionPreference='Stop'
$taskRoot=Split-Path -Parent $PSCommandPath
$beforeRoot=Join-Path $taskRoot 'sch_audit'
$afterRoot=Join-Path $taskRoot 'sch_name_fix_audit'
function ReadRows([string]$root,[string]$name) { @(Import-Csv -LiteralPath (Join-Path $root $name) -Delimiter "`t" -Encoding UTF8) }
function MultisetDiff([string[]]$before,[string[]]$after) {
 $counts=New-Object 'System.Collections.Generic.Dictionary[string,int]' ([System.StringComparer]::Ordinal)
 foreach($line in $before) { if(!$counts.ContainsKey($line)){$counts[$line]=0};$counts[$line]++ }
 foreach($line in $after) { if(!$counts.ContainsKey($line)){$counts[$line]=0};$counts[$line]-- }
 $diff=@();foreach($key in $counts.Keys){if($counts[$key] -ne 0){$diff += [ordered]@{row=$key;before_minus_after_count=$counts[$key]}}};return ,$diff
}
function Sha([string]$path) { (Get-FileHash -Algorithm SHA256 -LiteralPath $path).Hash }
$beforePages=ReadRows $beforeRoot 'pages.tsv';$afterPages=ReadRows $afterRoot 'pages.tsv'
$beforeInstances=ReadRows $beforeRoot 'instances.tsv';$afterInstances=ReadRows $afterRoot 'instances.tsv'
$beforePins=ReadRows $beforeRoot 'pins.tsv';$afterPins=ReadRows $afterRoot 'pins.tsv'
$beforeQ=@($beforeInstances|Where-Object reference -CEQ 'Q39');$afterQ=@($afterInstances|Where-Object reference -CEQ 'Q39')
$expectedNew='OT-23-3_L2_9-W1_3-P1_90-LS2_1'
if($beforeQ.Count -ne 1 -or $afterQ.Count -ne 1){throw 'Q39 must occur exactly once'}
$instanceFieldDiffs=@()
for($i=0;$i -lt $beforeInstances.Count;$i++) {
 $r=$beforeInstances[$i]
 $match=@($afterInstances | Where-Object { $_.page -ceq $r.page -and $_.full_reference -ceq $r.full_reference })
 if($match.Count -ne 1){throw "Nonunique instance identity: $($r.page)/$($r.full_reference)"}
 foreach($field in $r.PSObject.Properties.Name){if($r.$field -cne $match[0].$field){$instanceFieldDiffs += [ordered]@{page=$r.page;reference=$r.reference;full_reference=$r.full_reference;field=$field;before=$r.$field;after=$match[0].$field}}}
}
$pageDiff=MultisetDiff ([IO.File]::ReadAllLines((Join-Path $beforeRoot 'pages.tsv'))) ([IO.File]::ReadAllLines((Join-Path $afterRoot 'pages.tsv')))
$pinDiff=MultisetDiff ([IO.File]::ReadAllLines((Join-Path $beforeRoot 'pins.tsv'))) ([IO.File]::ReadAllLines((Join-Path $afterRoot 'pins.tsv')))
$metadata=@(ReadRows $afterRoot 'Q39_metadata.tsv')
$beforeHash=Get-Content -Raw -LiteralPath (Join-Path $afterRoot 'hashes_before.json')|ConvertFrom-Json
$hashChecks=@();foreach($item in $beforeHash){$actual=Sha $item.Path;$hashChecks += [ordered]@{path=$item.Path;before_sha256=$item.Hash;after_sha256=$actual;unchanged=($actual -ceq $item.Hash)}}
$origHash=Sha (Join-Path $taskRoot 'inputs\LGA1700.DSN')
$baselineHash=Sha (Join-Path $beforeRoot 'input\LGA1700.DSN')
$summaryBefore=[ordered]@{pages=$beforePages.Count;instances=$beforeInstances.Count;pins=$beforePins.Count;wires=[int](($beforePages|Measure-Object wires -Sum).Sum);offpages=[int](($beforePages|Measure-Object offpages -Sum).Sum)}
$summaryAfter=[ordered]@{pages=$afterPages.Count;instances=$afterInstances.Count;pins=$afterPins.Count;wires=[int](($afterPages|Measure-Object wires -Sum).Sum);offpages=[int](($afterPages|Measure-Object offpages -Sum).Sum)}
$onlyExpectedDiff=($instanceFieldDiffs.Count -eq 1 -and $instanceFieldDiffs[0].reference -ceq 'Q39' -and $instanceFieldDiffs[0].field -ceq 'footprint' -and $instanceFieldDiffs[0].after -ceq $expectedNew)
$metadataOk=($metadata.Count -eq 1 -and $metadata[0].full_reference -ceq 'Q39' -and $metadata[0].AD_ORIGINAL_PCB_FOOTPRINT -ceq $beforeQ[0].footprint -and $metadata[0].footprint -ceq $expectedNew)
$allHashesUnchanged=(@($hashChecks|Where-Object {!$_.unchanged}).Count -eq 0)
$summaryOk=($summaryBefore.pages -eq 35 -and $summaryAfter.pages -eq 35 -and $summaryBefore.instances -eq 1131 -and $summaryAfter.instances -eq 1131 -and $summaryBefore.pins -eq 6608 -and $summaryAfter.pins -eq 6608 -and $summaryBefore.wires -eq 8613 -and $summaryAfter.wires -eq 8613 -and $summaryBefore.offpages -eq $summaryAfter.offpages)
$passed=($pageDiff.Count -eq 0 -and $pinDiff.Count -eq 0 -and $onlyExpectedDiff -and $metadataOk -and $allHashesUnchanged -and $summaryOk -and $origHash -ceq $baselineHash)
$result=[ordered]@{
 schema_version=1
 verification='Native read-only Capture Dbo audit of copied derivative DSN compared against native original audit'
 source_dsn=(Join-Path $taskRoot 'inputs\LGA1700.DSN')
 derivative_dsn=(Join-Path $taskRoot 'sch_name_fix\LGA1700.DSN')
 source_audit_input_matches_source=($origHash -ceq $baselineHash)
 native_audit_exit_code=0
 before=$summaryBefore;after=$summaryAfter
 pages_table_identical=($pageDiff.Count -eq 0)
 pages_table_differences=$pageDiff
 pins_table_identical=($pinDiff.Count -eq 0)
 pins_table_differences=$pinDiff
 instance_field_differences=$instanceFieldDiffs
 only_expected_Q39_footprint_changed=$onlyExpectedDiff
 q39_original_footprint_preserved=$metadataOk
 q39_metadata=$metadata
 dsn_hashes_unchanged_by_audit=$allHashesUnchanged
 dsn_hash_checks=$hashChecks
 passed=$passed
 scope_limits=@('Tables cover page counts, instance identity/value/footprint/location, pin number/name/NC/net/location, per-page wire counts and off-page connector counts.','Wire geometry and unsampled properties were not compared; no claim of a full binary semantic diff.','No DSN save or property setter was invoked by the audit. Native audit ran on an isolated copied derivative DSN.')
 evidence=[ordered]@{original_audit=$beforeRoot;derivative_audit=$afterRoot;derivative_native_result=(Join-Path $afterRoot 'audit_result.tcldict')}
}
$result | ConvertTo-Json -Depth 12 | Set-Content -LiteralPath (Join-Path $taskRoot 'q39_fix_verification.json') -Encoding UTF8
$result | ConvertTo-Json -Depth 4
if(!$passed){exit 1}