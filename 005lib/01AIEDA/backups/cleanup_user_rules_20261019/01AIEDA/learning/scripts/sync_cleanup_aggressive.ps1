# Replace only four explicitly inventoried BAT copies; never execute a cleanup.
$ErrorActionPreference='Stop'
$workspace=[IO.Path]::GetFullPath((Join-Path $PSScriptRoot '..\..\..'))
$stage=Join-Path $workspace '01AIEDA\learning\staging\cleanup_review_20261019'
$plan=Get-Content -LiteralPath (Join-Path $stage 'aggressive\external_sync_plan.json') -Raw -Encoding UTF8 | ConvertFrom-Json
$allowed=@(
 'D:\001DIY\000driver\18Brushless\01SCH\0000Ad_Keil_Cadence_dat_iar_txt.bat',
 'D:\001DIY\023USB\07usb_com\004usbtoTTL\01sch\0000Ad_Keil_Cadence_dat_iar_txt.bat',
 'D:\001DIY\023USB\08UsbIPDapLink\01sch\0000Ad_Keil_Cadence_dat_iar_txt.bat',
 'D:\001DIY\023USB\08UsbIPDapLink\02pcb\0000Ad_Keil_Cadence_dat_iar_txt.bat'
)
if ($plan.Count -ne 4) { throw 'Expected exactly four targets.' }
foreach ($entry in $plan) {
    if ([IO.Path]::GetFullPath($entry.target) -notin $allowed) { throw 'Unlisted target refused.' }
    if ($entry.source -ne (Join-Path $workspace '0000Ad_Keil_Cadence_dat_iar_txt.bat')) { throw 'Unexpected source.' }
    if ((Get-FileHash -LiteralPath $entry.source -Algorithm SHA256).Hash -ine $entry.after_sha256) { throw 'Source changed.' }
    if ((Get-FileHash -LiteralPath $entry.target -Algorithm SHA256).Hash -ine $entry.previous_sha256) { throw 'Target changed; keeping it.' }
    if ((Get-FileHash -LiteralPath $entry.backup -Algorithm SHA256).Hash -ine $entry.before_sha256) { throw 'Original backup mismatch.' }
    $parent=Get-Item -LiteralPath $entry.target -Force
    while ($parent) {
        if ($parent.Attributes -band [IO.FileAttributes]::ReparsePoint) { throw 'Reparse-point target/ancestor refused.' }
        if ($parent.PSIsContainer) { $parent=$parent.Parent } else { $parent=$parent.Directory }
    }
}
$results=@()
foreach ($entry in $plan) {
    Copy-Item -LiteralPath $entry.source -Destination $entry.target -Force -ErrorAction Stop
    if ((Get-FileHash -LiteralPath $entry.target -Algorithm SHA256).Hash -ine $entry.after_sha256) { throw 'Copy hash mismatch.' }
    $results += [pscustomobject]@{target=$entry.target;backup=$entry.backup;before_sha256=$entry.before_sha256;after_sha256=$entry.after_sha256;previous_sha256=$entry.previous_sha256;cleanup_executed=$false}
}
$json=$results | ConvertTo-Json -Depth 5
[IO.File]::WriteAllText((Join-Path $stage 'external_sync_result.json'),$json,(New-Object Text.UTF8Encoding($false)))
[IO.File]::WriteAllText((Join-Path $stage 'aggressive\external_sync_result.json'),$json,(New-Object Text.UTF8Encoding($false)))
Write-Output 'Four BAT files updated; no cleanup executed.'
