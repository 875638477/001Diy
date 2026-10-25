$ErrorActionPreference='Stop'
$repairRoot='D:\001DIY\005lib\01AIEDA\learning\staging\lga1700_pcb_repair_20261023'
$delivery='D:\001DIY\004computer\lga1700\04AD_original_repair_20261023'
$zipPath='D:\001DIY\004computer\lga1700\LGA1700_AD_original_repaired_20261023.zip'
Add-Type -AssemblyName System.IO.Compression.FileSystem
$archive=[IO.Compression.ZipFile]::OpenRead($zipPath)
$verified=0
$totalBytes=[long]0
$seen=[Collections.Generic.HashSet[string]]::new([StringComparer]::OrdinalIgnoreCase)
try {
 foreach($entry in $archive.Entries){
  $entryPath=$entry.FullName.Replace('\','/')
  if($entryPath.EndsWith('/')){continue}
  $prefix=[IO.Path]::GetFileName($delivery)+'/'
  if(-not $entryPath.StartsWith($prefix,[StringComparison]::Ordinal)){throw 'Unexpected archive path'}
  $rel=$entryPath.Substring($prefix.Length).Replace('/','\')
  if(-not $seen.Add($rel)){throw 'Duplicate archive entry'}
  $originalPath=[IO.Path]::GetFullPath((Join-Path $delivery $rel))
  if(-not $originalPath.StartsWith($delivery+'\',[StringComparison]::OrdinalIgnoreCase)){throw 'Archive path escaped delivery'}
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
$manifest=@(Import-Csv -LiteralPath "$delivery\文件校验.csv")
foreach($row in $manifest){
 $path=Join-Path $delivery $row.RelativePath
 if((Get-FileHash -LiteralPath $path).Hash -ne $row.SHA256){throw 'Manifest hash mismatch'}
}
$original=Get-Content -LiteralPath "$delivery\verification\original_files_unchanged.json" -Raw -Encoding UTF8 | ConvertFrom-Json
foreach($row in $original.checks){if((Get-FileHash -LiteralPath $row.path).Hash -ne $row.baseline){throw 'Original file no longer matches snapshot'}}
$zipHash=(Get-FileHash -LiteralPath $zipPath -Algorithm SHA256).Hash
[IO.File]::WriteAllText($zipPath+'.sha256',$zipHash+'  '+[IO.Path]::GetFileName($zipPath)+"`r`n",[Text.Encoding]::ASCII)
$archiveCheck=[pscustomobject]@{status='PASS_ZIP_ALL_ENTRIES_AND_MANIFEST_MATCH_FINAL_DELIVERY';zip=$zipPath;sha256=$zipHash;zip_bytes=(Get-Item -LiteralPath $zipPath).Length;files_verified=$verified;uncompressed_bytes=$totalBytes;manifest_entries=$manifest.Count;original_files_verified=$original.count;dsn_sha256=(Get-FileHash -LiteralPath "$delivery\sch\LGA1700.DSN").Hash;pcb_sha256=(Get-FileHash -LiteralPath "$delivery\pcb\LGA1700_AD_PCB_repaired.brd").Hash}
$archiveCheck | ConvertTo-Json -Depth 5 | Set-Content -LiteralPath "$repairRoot\final_archive_verification.json" -Encoding UTF8
$archiveCheck | ConvertTo-Json -Depth 5
