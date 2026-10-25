$ErrorActionPreference = 'Stop'
$repairRoot = 'D:\001DIY\005lib\01AIEDA\learning\staging\lga1700_pcb_repair_20261023'
$delivery = 'D:\001DIY\004computer\lga1700\04AD_original_repair_20261023'
if (Test-Path -LiteralPath $delivery) { throw 'Delivery already exists; do not merge an unreviewed output.' }
$dirs = @('sch','sch\netlist','pcb','libraries\psm','libraries\dra','libraries\pad','libraries\devices','pcbenv','verification\pcb','verification\source_manifest','verification\ad_native_gold','verification\xml_roundtrip')
foreach ($sub in $dirs) { [void][IO.Directory]::CreateDirectory((Join-Path $delivery $sub)) }
function Copy-One([string]$From, [string]$To) { Copy-Item -LiteralPath $From -Destination $To -ErrorAction Stop }
Copy-One "$repairRoot\source_repaired_xml_roundtrip\ROUNDTRIP.DSN" "$delivery\sch\LGA1700.DSN"
Copy-One "$repairRoot\repair_plan\pcb_recovery_candidate\LGA1700_AD_PCB_F_USB3_recovered.brd" "$delivery\pcb\LGA1700_AD_PCB_repaired.brd"
foreach ($f in Get-ChildItem -LiteralPath "$repairRoot\library_source" -File) {
    $target = switch ($f.Extension.ToLowerInvariant()) { '.psm' {'psm'} '.dra' {'dra'} '.txt' {'devices'} '.map' {'devices'} default {$null} }
    if ($null -ne $target) { Copy-One $f.FullName "$delivery\libraries\$target\$($f.Name)" }
}
foreach ($f in Get-ChildItem -LiteralPath "$repairRoot\library\pad" -Filter '*.pad' -File) { Copy-One $f.FullName "$delivery\libraries\pad\$($f.Name)" }
Copy-One "$repairRoot\library\psm\r0402_pp_2.psm" "$delivery\libraries\psm\r0402_pp_2.psm"
Copy-One "$repairRoot\library\psm\r0402_pp_2.dra" "$delivery\libraries\dra\r0402_pp_2.dra"
Copy-One "$repairRoot\repair_plan\pcb_recovery_candidate\recover_f_usb3.txt" "$delivery\libraries\devices\recover_f_usb3.txt"
$cfg = 'D:\001DIY\005lib\01AIEDA\learning\examples\lga1700_capture_migration_20261022\netlist_ready\allegro.cfg'
Copy-One $cfg "$delivery\sch\allegro.cfg"
foreach ($name in @('VALIDATION.json','source_ad_pcb_post_recovery_pads.csv','验证说明.md')) { Copy-One "$repairRoot\repair_plan\pcb_recovery_candidate\$name" "$delivery\verification\pcb\$name" }
foreach ($f in Get-ChildItem -LiteralPath "$repairRoot\repair_plan\source_repaired_audit" -File) { Copy-One $f.FullName "$delivery\verification\source_manifest\$($f.Name)" }
foreach ($name in @('native_flat_nets.tsv','native_flat_net_pins.tsv','native_export_status.txt','native_progress.txt','source_original_hashes_before.csv')) { Copy-One "$repairRoot\ad18_native_research\$name" "$delivery\verification\ad_native_gold\$name" }
Copy-One "$repairRoot\source_repaired_xml_roundtrip\run_result.json" "$delivery\verification\xml_roundtrip\run_result.json"
Copy-One "$repairRoot\input_snapshot.json" "$delivery\verification\original_input_snapshot.json"
$opj = @'
(ExpressProject "LGA1700_AD_REF"
  (ProjectVersion "19981106")
  (ProjectType "PCB")
  (Folder "Design Resources"
    (Folder "Library"
      (File ".\ORCAD_LIBRARY.OLB" (Type "Symbol Library")))
    (File ".\LGA1700.DSN" (Type "Schematic Design"))
    (NoModify))
  (Folder "Outputs"))
'@
[IO.File]::WriteAllText("$delivery\sch\LGA1700_AD_REF.opj", $opj, [Text.Encoding]::ASCII)
$cmd = @'
@echo off
setlocal
set "CDSROOT=C:\Program0\Cadence\SPB172"
set "PATH=%CDSROOT%\tools\bin;%PATH%"
set "LGA1700_PROJECT_ROOT=%~dp0"
set "LGA1700_PROJECT_ROOT=%LGA1700_PROJECT_ROOT:~0,-1%"
set "LGA1700_PROJECT_ROOT=%LGA1700_PROJECT_ROOT:\=/%"
set "ALLEGRO_PCBENV=%~dp0pcbenv"
pushd "%~dp0pcb"
start "" "%CDSROOT%\tools\bin\allegro.exe" -product Allegro_performance "%~dp0pcb\LGA1700_AD_PCB_repaired.brd"
popd
endlocal
'@
[IO.File]::WriteAllText("$delivery\打开PCB修复副本.cmd", $cmd, [Text.Encoding]::Default)
$envText = @'
source $TELENV
set psmpath = $LGA1700_PROJECT_ROOT/libraries/psm
set padpath = $LGA1700_PROJECT_ROOT/libraries/pad
set devpath = $LGA1700_PROJECT_ROOT/libraries/devices
'@
[IO.File]::WriteAllText("$delivery\pcbenv\env", $envText, [Text.Encoding]::ASCII)
Copy-One "$repairRoot\delivery_README.md" "$delivery\使用说明.md"
$copyPairs = @(
    @{source="$repairRoot\source_repaired_xml_roundtrip\ROUNDTRIP.DSN";target="$delivery\sch\LGA1700.DSN"},
    @{source="$repairRoot\repair_plan\pcb_recovery_candidate\LGA1700_AD_PCB_F_USB3_recovered.brd";target="$delivery\pcb\LGA1700_AD_PCB_repaired.brd"}
)
$checks = foreach ($p in $copyPairs) {
    $a=(Get-FileHash -LiteralPath $p.source -Algorithm SHA256).Hash
    $b=(Get-FileHash -LiteralPath $p.target -Algorithm SHA256).Hash
    if ($a -ne $b) { throw 'Copy hash mismatch' }
    [pscustomobject]@{source=$p.source;target=$p.target;sha256=$b;equal=$true}
}
$checks | ConvertTo-Json -Depth 5 | Set-Content -LiteralPath "$delivery\verification\delivery_copy_verification.json" -Encoding UTF8
[pscustomobject]@{delivery=$delivery;copies=$checks;files=@(Get-ChildItem -LiteralPath $delivery -Recurse -File).Count} | ConvertTo-Json -Depth 5
