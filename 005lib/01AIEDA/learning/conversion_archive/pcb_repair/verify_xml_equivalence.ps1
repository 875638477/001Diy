$ErrorActionPreference='Stop'
$repairRoot='D:\001DIY\005lib\01AIEDA\learning\staging\lga1700_pcb_repair_20261023'
$auditRoot=Join-Path $repairRoot 'xml_equivalence_audit'
function Compare-AuditTable($fileName,[string[]]$columns=@()) {
 $paths=@((Join-Path $auditRoot "before\$fileName"),(Join-Path $auditRoot "after\$fileName"))
 $tables=@()
 foreach($path in $paths) {
  $dict=New-Object 'System.Collections.Generic.Dictionary[string,int]' ([StringComparer]::Ordinal)
  if($columns.Count -eq 0) { $lines=[IO.File]::ReadAllLines($path) | Select-Object -Skip 1 }
  else {
   $rows=Import-Csv -LiteralPath $path -Delimiter "`t"
   $lines=foreach($row in $rows) { ($columns | ForEach-Object { [string]$row.$_ }) -join "`t" }
  }
  foreach($line in $lines) {if($dict.ContainsKey($line)){$dict[$line]++}else{$dict.Add($line,1)}}
  $tables += ,$dict
 }
 $removed=@();$added=@()
 foreach($pair in $tables[0].GetEnumerator()) {
  $other=0;if($tables[1].ContainsKey($pair.Key)){$other=$tables[1][$pair.Key]}
  if($pair.Value -gt $other){$removed += [pscustomobject]@{row=$pair.Key;count=($pair.Value-$other)}}
 }
 foreach($pair in $tables[1].GetEnumerator()) {
  $other=0;if($tables[0].ContainsKey($pair.Key)){$other=$tables[0][$pair.Key]}
  if($pair.Value -gt $other){$added += [pscustomobject]@{row=$pair.Key;count=($pair.Value-$other)}}
 }
 [pscustomobject]@{file=$fileName;columns=$columns;equal=($removed.Count -eq 0 -and $added.Count -eq 0);before_rows=($tables[0].Values|Measure-Object -Sum).Sum;after_rows=($tables[1].Values|Measure-Object -Sum).Sum;removed_rows=($removed.count|Measure-Object -Sum).Sum;added_rows=($added.count|Measure-Object -Sum).Sum;removed_sample=@($removed|Select-Object -First 5);added_sample=@($added|Select-Object -First 5)}
}
$checks=@()
foreach($name in @('pages.tsv','instances.tsv','pins.tsv','wires.tsv','aliases.tsv','net_objects.tsv','page_object_counts.tsv','instance_trace_properties.tsv','object_trace_properties.tsv')) {$checks+=Compare-AuditTable $name}
$checks+=Compare-AuditTable 'pins.tsv' @('page','reference','full_reference','number','name','nc','x','y')
$checks+=Compare-AuditTable 'wires.tsv' @('page','points','object_type','line_style','line_width')
$checks+=Compare-AuditTable 'net_objects.tsv' @('page','kind','name','source_symbol','x','y','hot_x','hot_y','rotation','mirror')
$designProps=Compare-AuditTable 'design_properties.tsv'
$counts=[ordered]@{}
foreach($side in @('before','after')) {
 $pages=Import-Csv -LiteralPath (Join-Path $auditRoot "$side\pages.tsv") -Delimiter "`t"
 $objects=Import-Csv -LiteralPath (Join-Path $auditRoot "$side\page_object_counts.tsv") -Delimiter "`t"
 $counts[$side]=[ordered]@{pages=@($pages).Count;instances=($pages.instances|Measure-Object -Sum).Sum;pins=($pages.pins|Measure-Object -Sum).Sum;wires=($pages.wires|Measure-Object -Sum).Sum;offpages=($pages.offpages|Measure-Object -Sum).Sum;globals=($objects.globals|Measure-Object -Sum).Sum;ports=($objects.ports|Measure-Object -Sum).Sum}
}
$report=[ordered]@{status='REQUIRES_REVIEW';scope='Native read-only comparison of isolated copies before and after the official XMATIC design XML roundtrip';counts=$counts;checks=$checks;design_properties_check=$designProps;run_result=(Get-Content -LiteralPath (Join-Path $repairRoot 'source_repaired_xml_roundtrip\run_result.json') -Raw|ConvertFrom-Json);hashes_unchanged=(Get-Content -LiteralPath (Join-Path $auditRoot 'audit_run_results.json') -Raw|ConvertFrom-Json);note='Object IDs intentionally regenerated. Every semantic row comparison excludes IDs. Full AD-gold topology validation is independent and must also pass.'}
if(@($checks|Where-Object {-not $_.equal}).Count -eq 0){$report.status='PASS_NATIVE_GEOMETRY_IDENTITY_TRACE_AND_PIN_NET_EQUIVALENCE'}
$report | ConvertTo-Json -Depth 10 | Set-Content -LiteralPath (Join-Path $auditRoot 'verification.json') -Encoding UTF8
[pscustomobject]@{status=$report.status;counts=$counts;failed_checks=@($checks|Where-Object {-not $_.equal}|Select-Object file,columns,removed_rows,added_rows,removed_sample,added_sample);design_properties_equal=$designProps.equal} | ConvertTo-Json -Depth 7
