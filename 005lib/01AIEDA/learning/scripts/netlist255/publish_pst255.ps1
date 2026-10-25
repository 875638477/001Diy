param(
 [Parameter(Mandatory=$true)][string]$SourceDsn,
 [Parameter(Mandatory=$true)][string]$ConfigFile,
 [Parameter(Mandatory=$true)][string]$OutputRoot,
 [Parameter(Mandatory=$true)][string]$PublishDirectory,
 [Parameter(Mandatory=$true)][string]$ExporterFile,
 [Parameter(Mandatory=$true)][string]$CadenceRoot,
 [string]$PstswpExecutable
)
$ErrorActionPreference='Stop'
$lockRoot=[IO.Path]::GetFullPath($OutputRoot);New-Item -ItemType Directory -Path $lockRoot -Force|Out-Null
$publishLock=[IO.File]::Open((Join-Path $lockRoot '.publish.lock'),[IO.FileMode]::OpenOrCreate,[IO.FileAccess]::ReadWrite,[IO.FileShare]::None)
try {
$source=[IO.Path]::GetFullPath($SourceDsn)
$config=[IO.Path]::GetFullPath($ConfigFile);$exporter=[IO.Path]::GetFullPath($ExporterFile)
$publishAbs=[IO.Path]::GetFullPath($PublishDirectory).TrimEnd('\')
foreach($protected in @($source,$config,$exporter,$lockRoot)){
 if($protected -eq $publishAbs -or $protected.StartsWith($publishAbs+'\',[StringComparison]::OrdinalIgnoreCase)){throw 'Publish directory would move a protected input or export root'}
}
if($publishAbs.StartsWith($lockRoot.TrimEnd('\')+'\',[StringComparison]::OrdinalIgnoreCase)){throw 'Publish directory must be separate from per-run export storage'}
$publish=[IO.Path]::GetFullPath($PublishDirectory).TrimEnd('\')
if($publish -eq [IO.Path]::GetPathRoot($publish) -or $publish -eq [IO.Path]::GetDirectoryName($source) -or $source.StartsWith($publish+'\',[StringComparison]::OrdinalIgnoreCase)){throw 'Unsafe publish directory'}
if(!(Test-Path -LiteralPath ([IO.Path]::GetDirectoryName($publish)) -PathType Container)){throw 'Publish parent directory does not exist'}
if(@(Get-Process pstswp,netrev -ErrorAction SilentlyContinue).Count){throw 'Another Cadence netlist operation is running. Wait for it to finish and retry.'}
$report = & ([scriptblock]::Create([IO.File]::ReadAllText($ExporterFile))) -SourceDsn $source -ConfigFile $ConfigFile -OutputRoot $OutputRoot -CadenceRoot $CadenceRoot -PstswpExecutable $PstswpExecutable
if($null -eq $report -or @($report).Count -ne 1){throw 'Exporter did not return exactly one run report'}
if($report.status -ne 'PASS_NATIVE_PST255_EXPORT'){throw 'Native export validation did not pass'}
if((Get-FileHash -LiteralPath $source -Algorithm SHA256).Hash -ne $report.source_sha256_at_snapshot){throw 'Source changed after snapshot. Save the design and retry; active netlist was not changed.'}
$run=Split-Path -Parent $report.netlist_directory
$stage=Join-Path $run 'publish_stage'
$backup=Join-Path $run 'previous_active_netlist'
New-Item -ItemType Directory -Path $stage|Out-Null
foreach($name in @('pstchip.dat','pstxprt.dat','pstxnet.dat','netlist.log')){Copy-Item -LiteralPath (Join-Path $report.netlist_directory $name) -Destination (Join-Path $stage $name)}
Copy-Item -LiteralPath (Join-Path $run 'export_validation.json') -Destination (Join-Path $stage 'export_validation.json')
$hadPrevious=Test-Path -LiteralPath $publish -PathType Container
if(Test-Path -LiteralPath $backup){throw 'Refusing existing backup'}
foreach($dir in @($run,$stage,$backup)){if(!([IO.Path]::GetFullPath($dir)).StartsWith([IO.Path]::GetFullPath($OutputRoot).TrimEnd('\')+'\',[StringComparison]::OrdinalIgnoreCase)){throw 'Output path escaped export root'}}
if($hadPrevious){Move-Item -LiteralPath $publish -Destination $backup}
try{Move-Item -LiteralPath $stage -Destination $publish}catch{if($hadPrevious -and !(Test-Path -LiteralPath $publish)){Move-Item -LiteralPath $backup -Destination $publish};throw}
$validation=[ordered]@{status='PASS_PUBLISHED_VALIDATED_PST255';created_local=[DateTimeOffset]::Now.ToString('o');source=$source;source_sha256=$report.source_sha256_at_snapshot;source_unchanged=$true;published_directory=$publish;native_export_report=(Join-Path $run 'export_validation.json');previous_directory=if($hadPrevious){$backup}else{$null};published_files=@(Get-ChildItem -LiteralPath $publish -File|ForEach-Object{[pscustomobject]@{name=$_.Name;bytes=$_.Length;sha256=(Get-FileHash -LiteralPath $_.FullName -Algorithm SHA256).Hash}})}
$validation|ConvertTo-Json -Depth 5|Set-Content -LiteralPath (Join-Path $OutputRoot 'latest_publication.json') -Encoding UTF8
Write-Output ('Published validated PST255 to: '+$publish)
} finally {$publishLock.Dispose()}
