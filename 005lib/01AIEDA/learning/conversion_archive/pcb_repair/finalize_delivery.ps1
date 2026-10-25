$ErrorActionPreference='Stop'
$repairRoot='D:\001DIY\005lib\01AIEDA\learning\staging\lga1700_pcb_repair_20261023'
$delivery='D:\001DIY\004computer\lga1700\04AD_original_repair_20261023'
$projectRoot='D:\001DIY\004computer\lga1700'
$actualDsn="$delivery\sch\LGA1700.DSN"
$actualBoard="$delivery\pcb\LGA1700_AD_PCB_repaired.brd"
$dsnHash=(Get-FileHash -LiteralPath $actualDsn).Hash
$boardHash=(Get-FileHash -LiteralPath $actualBoard).Hash
if($dsnHash -ne '81924DF03109CC8D2222B3558CE0C6B18EF56CBDB078CE522F36632D113BE268'){throw 'Final DSN hash changed'}
if($boardHash -ne '1D0760CFCE9CDA2A2AADC6891A4D434E5703424FF4F4C841383BC78586866D25'){throw 'Final board hash changed'}
$pst=Get-Content -LiteralPath "$delivery\verification\final_pst_export.json" -Raw -Encoding UTF8 | ConvertFrom-Json
$gold=Get-Content -LiteralPath "$delivery\verification\ad_native_partition\final_delivery_verification.json" -Raw -Encoding UTF8 | ConvertFrom-Json
$readback=Get-Content -LiteralPath "$delivery\verification\final_dsn_readback\final_verification.json" -Raw -Encoding UTF8 | ConvertFrom-Json
$pcb=Get-Content -LiteralPath "$delivery\verification\pcb\VALIDATION.json" -Raw -Encoding UTF8 | ConvertFrom-Json
$olb=Get-Content -LiteralPath "$delivery\verification\library\VALIDATION.json" -Raw -Encoding UTF8 | ConvertFrom-Json
$import=Get-Content -LiteralPath "$delivery\verification\library_import_test\validation.json" -Raw -Encoding UTF8 | ConvertFrom-Json
if($pst.exit_code -ne 0 -or $gold.status -ne 'PASS_FINAL_DELIVERY_AD_NATIVE_PARTITION' -or $readback.status -ne 'PASS_FINAL_DELIVERY_DSN_NATIVE_READBACK' -or -not $pcb.Passed -or -not $olb.Passed -or $import.missing_footprint_diagnostics -ne 0){throw 'A release check failed'}
Copy-Item -LiteralPath "$repairRoot\delivery_README.md" -Destination "$delivery\使用说明.md"
$original=Get-Content -LiteralPath "$delivery\verification\original_files_unchanged.json" -Raw -Encoding UTF8 | ConvertFrom-Json
$libActual=(Get-FileHash -LiteralPath $olb.OriginalLibrary).Hash
if($libActual -ne $olb.OriginalLibrarySHA256){throw 'Original library changed'}
$original.checks=@($original.checks)+[pscustomobject]@{path=$olb.OriginalLibrary;baseline=$olb.OriginalLibrarySHA256;actual=$libActual;unchanged=$true}
$original.count=@($original.checks).Count
$original | ConvertTo-Json -Depth 6 | Set-Content -LiteralPath "$delivery\verification\original_files_unchanged.json" -Encoding UTF8
$reportPath="$projectRoot\转换记录.md"
$report=[IO.File]::ReadAllText($reportPath)
if($report.Contains('## 十七 2026-10-23：')){throw 'Section 17 already exists'}
$old='最新状态（2026-10-23）：已完成库路径、Q39 与 R4/R5 封装名称的独立修复副本；用户选择保留引脚差异。进一步发现跨页端口和 USB 接地等转换连接缺陷，当前 DSN/PST 不可直接更新已有 PCB 布线。详见第十六节及 03repair_review_20261023/修复说明.md。'
$new='最新状态（2026-10-23）：已按原 AD 分别修复 Cadence 原理图和 PCB 转换损失，交付在 04AD_original_repair_20261023。原理图 6608 个引脚的完整网络分区与 AD 原生编译结果一致；PCB 6521 个焊盘身份及网络与原 AD PCB 一致。库路径/名称问题已解决。原 Sch/PCB 本来存在的引脚等差异仍保留，整板 ECO 尚不能直接通过。当前入口与完整证据见第十七节。'
if(-not $report.Contains($old)){throw 'Record header unexpectedly changed'}
$report=$report.Replace($old,$new).Replace('后续优先打开整理后的工程：','首次转换时整理的工程（历史结果；当前使用入口见第十七节）：')
$report=$report.TrimEnd()+"`r`n"+[IO.File]::ReadAllText("$repairRoot\conversion_record_section17.md")
[IO.File]::WriteAllText($reportPath,$report,[Text.UTF8Encoding]::new($false))
Copy-Item -LiteralPath $reportPath -Destination "$delivery\转换记录.md"
$gate=[pscustomobject]@{
 status='PASS_CONVERSION_FIDELITY_WITH_PRESERVED_SOURCE_SCH_PCB_DIFFERENCES'
 generated_utc=[DateTime]::UtcNow.ToString('o')
 dsn=@{path=$actualDsn;sha256=$dsnHash;electrical_gold_status=$gold.status;readback_status=$readback.status}
 pcb=@{path=$actualBoard;sha256=$boardHash;pads=6521;source_net_splits=0;target_net_merges=0}
 original_files_verified=$original.count
 original_files_changed=0
 native_pst_exit=0
 missing_footprints=0
 strict_import_exit=$import.exit_code
 strict_import_output_created=$import.output_created
 limits=@('Source Sch/PCB pin definitions still differ; strict ECO stops with 16 device/symbol groups plus one stop item.','Altium source diagnostics and full-board ERC/DRC/manufacturing sign-off are outside the passed conversion-fidelity checks.')
}
$gate | ConvertTo-Json -Depth 7 | Set-Content -LiteralPath "$delivery\verification\release_gate.json" -Encoding UTF8
$manifestPath="$delivery\文件校验.csv"
$manifest=@(Get-ChildItem -LiteralPath $delivery -Recurse -File | Where-Object {$_.FullName -ne $manifestPath} | Sort-Object FullName | ForEach-Object {
 [pscustomobject]@{RelativePath=$_.FullName.Substring($delivery.Length+1);Bytes=$_.Length;SHA256=(Get-FileHash -LiteralPath $_.FullName -Algorithm SHA256).Hash}
})
$manifest | Export-Csv -LiteralPath $manifestPath -NoTypeInformation -Encoding UTF8
Add-Type -AssemblyName System.IO.Compression.FileSystem
$zipPath="$projectRoot\LGA1700_AD_original_repaired_20261023.zip"
if(Test-Path -LiteralPath $zipPath){throw 'ZIP already exists; will not overwrite'}
[IO.Compression.ZipFile]::CreateFromDirectory($delivery,$zipPath,[IO.Compression.CompressionLevel]::Optimal,$true)
$archive=[IO.Compression.ZipFile]::OpenRead($zipPath)
$verified=0
$totalBytes=[long]0
try {
 foreach($entry in $archive.Entries){
  $entryPath=$entry.FullName.Replace('\','/')
  if($entryPath.EndsWith('/')){continue}
  $prefix=[IO.Path]::GetFileName($delivery)+'/'
  if(-not $entryPath.StartsWith($prefix,[StringComparison]::Ordinal)){throw 'Unexpected archive path'}
  $rel=$entryPath.Substring($prefix.Length).Replace('/','\')
  $originalPath=Join-Path $delivery $rel
  if(-not (Test-Path -LiteralPath $originalPath -PathType Leaf)){throw 'Unexpected archive file'}
  $stream=$entry.Open()
  $sha=[Security.Cryptography.SHA256]::Create()
  try {$zipHash=[BitConverter]::ToString($sha.ComputeHash($stream)).Replace('-','')} finally {$stream.Dispose();$sha.Dispose()}
  $diskHash=(Get-FileHash -LiteralPath $originalPath -Algorithm SHA256).Hash
  if($zipHash -ne $diskHash){throw "ZIP entry hash mismatch: $rel"}
  $verified++
  $totalBytes+=$entry.Length
 }
} finally {$archive.Dispose()}
$diskCount=@(Get-ChildItem -LiteralPath $delivery -Recurse -File).Count
if($verified -ne $diskCount){throw 'ZIP file count mismatch'}
$zipHash=(Get-FileHash -LiteralPath $zipPath -Algorithm SHA256).Hash
[IO.File]::WriteAllText($zipPath+'.sha256',$zipHash+'  '+[IO.Path]::GetFileName($zipPath)+"`r`n",[Text.Encoding]::ASCII)
$archiveCheck=[pscustomobject]@{status='PASS_ZIP_ALL_ENTRIES_MATCH_FINAL_DELIVERY';zip=$zipPath;sha256=$zipHash;zip_bytes=(Get-Item -LiteralPath $zipPath).Length;files_verified=$verified;uncompressed_bytes=$totalBytes;manifest_entries=$manifest.Count;original_files_verified=$original.count;dsn_sha256=$dsnHash;pcb_sha256=$boardHash}
$archiveCheck | ConvertTo-Json -Depth 5 | Set-Content -LiteralPath "$repairRoot\final_archive_verification.json" -Encoding UTF8
$archiveCheck | ConvertTo-Json -Depth 5
