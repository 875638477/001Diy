$ErrorActionPreference='Stop'
$repairRoot='D:\001DIY\005lib\01AIEDA\learning\staging\lga1700_pcb_repair_20261023'
$deliveryRoot='D:\001DIY\004computer\lga1700\04AD_original_repair_20261023'
$sourceDsn=Join-Path $deliveryRoot 'sch\LGA1700.DSN'
$auditRoot=Join-Path $deliveryRoot 'verification\final_dsn_readback'
$baseline=Join-Path $repairRoot 'xml_equivalence_audit\after'
if(Test-Path -LiteralPath $auditRoot){throw 'Refuse existing final delivery readback directory'}
$hashBefore=(Get-FileHash -LiteralPath $sourceDsn -Algorithm SHA256).Hash
if($hashBefore -ne '81924DF03109CC8D2222B3558CE0C6B18EF56CBDB078CE522F36632D113BE268'){throw "Unexpected delivery hash: $hashBefore"}
New-Item -ItemType Directory -Path (Join-Path $auditRoot 'input') | Out-Null
$copyDsn=Join-Path $auditRoot 'input\LGA1700.DSN'
Copy-Item -LiteralPath $sourceDsn -Destination $copyDsn
$driver=Get-Content -LiteralPath (Join-Path $repairRoot 'run_stub_packaging_probe.ps1') -Raw
$start=$driver.IndexOf('function Invoke-ProbeNative');$end=$driver.IndexOf('$results = @()')
. ([ScriptBlock]::Create($driver.Substring($start,$end-$start)))
$env:CDSROOT='C:\Program0\Cadence\SPB172'
$env:PATH="C:\Program0\Cadence\SPB172\tools\bin;C:\Program0\Cadence\SPB172\tools\capture;C:\Program0\Cadence\SPB172\tcltk\bin;$env:PATH"
$runs=@()
foreach($kind in @('main','extra')){
 $script=Get-Content -LiteralPath (Join-Path $baseline "audit_$kind.tcl") -Raw
 $script=$script.Replace($baseline.Replace('\','/'),$auditRoot.Replace('\','/'))
 $scriptPath=Join-Path $auditRoot "audit_$kind.tcl"
 $script|Set-Content -LiteralPath $scriptPath -Encoding ASCII
 $exitCode=Invoke-ProbeNative 'C:\Program0\Cadence\SPB172\tcltk\bin\tclsh.exe' @($scriptPath) (Join-Path $auditRoot "audit_${kind}_output.txt")
 $runs += [pscustomobject]@{kind=$kind;exit_code=$exitCode}
 if($exitCode -ne 0){throw "Native readback failed: $kind"}
}
function Compare-DeliveryTable($name,[bool]$omitDesignName=$false){
 $tables=@()
 foreach($folder in @($baseline,$auditRoot)){
  $lines=[IO.File]::ReadAllLines((Join-Path $folder $name))|Select-Object -Skip 1
  $dict=New-Object 'System.Collections.Generic.Dictionary[string,int]' ([StringComparer]::Ordinal)
  foreach($line in $lines){
   if($omitDesignName -and $line.StartsWith("design`tName`t")){continue}
   if($dict.ContainsKey($line)){$dict[$line]++}else{$dict.Add($line,1)}
  }
  $tables+=,$dict
 }
 $removed=@();$added=@()
 foreach($pair in $tables[0].GetEnumerator()){
  $other=0;if($tables[1].ContainsKey($pair.Key)){$other=$tables[1][$pair.Key]}
  if($pair.Value -gt $other){$removed+=[pscustomobject]@{row=$pair.Key;count=($pair.Value-$other)}}
 }
 foreach($pair in $tables[1].GetEnumerator()){
  $other=0;if($tables[0].ContainsKey($pair.Key)){$other=$tables[0][$pair.Key]}
  if($pair.Value -gt $other){$added+=[pscustomobject]@{row=$pair.Key;count=($pair.Value-$other)}}
 }
 [pscustomobject]@{file=$name;equal=($removed.Count -eq 0 -and $added.Count -eq 0);baseline_rows=($tables[0].Values|Measure-Object -Sum).Sum;delivery_rows=($tables[1].Values|Measure-Object -Sum).Sum;removed_sample=@($removed|Select-Object -First 5);added_sample=@($added|Select-Object -First 5);excluded_field=$(if($omitDesignName){'design.Name: audit-copy pathname only'}else{''})}
}
$checks=@()
foreach($file in @('pages.tsv','instances.tsv','pins.tsv','wires.tsv','aliases.tsv','net_objects.tsv','page_object_counts.tsv','instance_trace_properties.tsv','object_trace_properties.tsv')){$checks+=Compare-DeliveryTable $file}
$checks+=Compare-DeliveryTable 'design_properties.tsv' $true
$hashAfter=(Get-FileHash -LiteralPath $sourceDsn -Algorithm SHA256).Hash
$copyHashAfter=(Get-FileHash -LiteralPath $copyDsn -Algorithm SHA256).Hash
$hashPass=($hashBefore -eq $hashAfter -and $hashBefore -eq $copyHashAfter)
$pass=($hashPass -and @($checks|Where-Object{-not $_.equal}).Count -eq 0)
$report=[ordered]@{status=$(if($pass){'PASS_FINAL_DELIVERY_DSN_NATIVE_READBACK'}else{'REQUIRES_REVIEW'});method='Readonly native audits of an independent copy of actual delivered DSN after final pstswp export. Complete TSV multisets compared with the previously validated XML roundtrip snapshot. No DSN/PST modified by this audit.';actual_delivery_dsn=$sourceDsn;stable_sha256=$hashAfter;input_sha256_before=$hashBefore;input_sha256_after=$hashAfter;audit_copy_sha256_after=$copyHashAfter;hash_unchanged=$hashPass;native_runs=$runs;baseline_audit_directory=$baseline;checks=$checks;conclusion='All audited instance/pin identities, source package/part, value, footprint, geometry, pin-net names, wires/aliases, power/offpage objects and AD trace properties are unchanged after the final native export. Only the independent audit copy pathname is excluded from design properties.'}
$report|ConvertTo-Json -Depth 9|Set-Content -LiteralPath (Join-Path $auditRoot 'final_verification.json') -Encoding UTF8
[pscustomobject]@{status=$report.status;stable_sha256=$hashAfter;checks=$checks.Count;failed_checks=@($checks|Where-Object{-not $_.equal});report=(Join-Path $auditRoot 'final_verification.json')}|ConvertTo-Json -Depth 6
