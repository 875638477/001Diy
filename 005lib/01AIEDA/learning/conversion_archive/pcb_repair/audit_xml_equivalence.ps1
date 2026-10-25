$ErrorActionPreference='Stop'
$repairRoot='D:\001DIY\005lib\01AIEDA\learning\staging\lga1700_pcb_repair_20261023'
$auditBase=Join-Path $repairRoot 'xml_equivalence_audit'
if(Test-Path -LiteralPath $auditBase){throw 'Refuse existing audit directory'}
New-Item -ItemType Directory -Path $auditBase | Out-Null
$driver=Get-Content -LiteralPath (Join-Path $repairRoot 'run_stub_packaging_probe.ps1') -Raw
$start=$driver.IndexOf('function Invoke-ProbeNative');$end=$driver.IndexOf('$results = @()')
. ([ScriptBlock]::Create($driver.Substring($start,$end-$start)))
$env:CDSROOT='C:\Program0\Cadence\SPB172'
$env:PATH="C:\Program0\Cadence\SPB172\tools\bin;C:\Program0\Cadence\SPB172\tools\capture;C:\Program0\Cadence\SPB172\tcltk\bin;$env:PATH"
$traceFunction=@'
proc traceprops {object prefix} {
 set state [DboState];set out {}
 set pi [$object NewEffectivePropsIter $state]
 set n [::DE::cs {}];set v [::DE::cs {}]
 set typ [DboTclHelper_sMakeDboValueType];set editable [DboTclHelper_sMakeInt]
 for {set st [$pi NextEffectiveProp $n $v $typ $editable]} {![$st Failed]} {set st [$pi NextEffectiveProp $n $v $typ $editable]} {
  set name [DboTclHelper_sGetConstCharPtr $n]
  if {[string match AD_* $name]} {
   append out "\n[tsv [list $prefix $name [DboTclHelper_sGetConstCharPtr $v]]]"
  }
 }
 delete_DboEffectivePropsIter $pi
 return $out
}
'@
$inputs=@{before=(Join-Path $repairRoot 'source_repaired_xml_roundtrip\input.DSN');after=(Join-Path $repairRoot 'source_repaired_xml_roundtrip\roundtrip.DSN')}
$results=@()
foreach($side in @('before','after')) {
 $auditRoot=Join-Path $auditBase $side
 New-Item -ItemType Directory -Path (Join-Path $auditRoot 'input') | Out-Null
 Copy-Item -LiteralPath $inputs[$side] -Destination (Join-Path $auditRoot 'input\LGA1700.DSN')
 $hashBefore=(Get-FileHash -LiteralPath $inputs[$side] -Algorithm SHA256).Hash
 foreach($kind in @('main','extra')) {
  $script=Get-Content -LiteralPath (Join-Path $repairRoot "connection_fix_audit\audit_$kind.tcl") -Raw
  $script=$script.Replace('lga1700_pcb_repair_20261023/connection_fix_audit',('lga1700_pcb_repair_20261023/xml_equivalence_audit/'+$side))
  $script=$script.Replace('set code [catch {',($traceFunction+"`n"+'set code [catch {'))
  if($kind -eq 'main') {
   $script=$script.Replace('footprint\tx\ty','footprint\tsource_package\tsource_part\trotation\tmirror\tx\ty')
   $script=$script.Replace('[list $pageName $ref $fullRef $value $footprint]','[list $pageName $ref $fullRef $value $footprint [::DE::str $placed GetSourcePackageName] [::DE::str $placed GetSourcePartName] [$instance GetRotation $state] [$instance GetMirror $state]]')
   $script=$script.Replace('set pageCount 0;','set traces "object\tname\tvalue";set pageCount 0;')
   $script=$script.Replace('incr ni;incr instCount','append traces [traceprops $placed "$pageName|$fullRef"];incr ni;incr instCount')
   $script=$script.Replace('set summary [dict create','::DE::write "$auditRoot/instance_trace_properties.tsv" $traces;set summary [dict create')
  } else {
   $script=$script.Replace('set totals [dict create','set traces "object\tname\tvalue";set totals [dict create')
   $script=$script.Replace('set pointString [join $points {;}]','set pointString [join $points {;}];append traces [traceprops $w "$pn|wire|$pointString"]')
   $script=$script.Replace('dict incr totals $kind;dict incr pagecounts $kind','append traces [traceprops $o "$pn|$kind|$name|[::DE::point [$o GetOffsetHotSpot $state]]"];dict incr totals $kind;dict incr pagecounts $kind')
   $script=$script.Replace('::DE::write "$root/design_properties.tsv" $props','::DE::write "$root/design_properties.tsv" $props;::DE::write "$root/object_trace_properties.tsv" $traces')
  }
  $scriptPath=Join-Path $auditRoot "audit_$kind.tcl"
  $script | Set-Content -LiteralPath $scriptPath -Encoding ASCII
  $code=Invoke-ProbeNative 'C:\Program0\Cadence\SPB172\tcltk\bin\tclsh.exe' @($scriptPath) (Join-Path $auditRoot "audit_${kind}_output.txt")
  $results += [pscustomobject]@{side=$side;kind=$kind;exit=$code}
  if($code -ne 0){throw "Audit failed: $side $kind; see log"}
 }
 $hashAfter=(Get-FileHash -LiteralPath $inputs[$side] -Algorithm SHA256).Hash
 if($hashBefore -ne $hashAfter){throw 'Source hash changed during audit'}
 $results += [pscustomobject]@{side=$side;kind='hash_unchanged';sha256=$hashAfter}
}
$results | ConvertTo-Json -Depth 5 | Set-Content -LiteralPath (Join-Path $auditBase 'audit_run_results.json') -Encoding UTF8
$results | ConvertTo-Json -Compress
