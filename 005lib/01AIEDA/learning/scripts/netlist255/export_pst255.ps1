param(
 [Parameter(Mandatory=$true)][string]$SourceDsn,
 [Parameter(Mandatory=$true)][string]$OutputRoot,
 [Parameter(Mandatory=$true)][string]$ConfigFile,
 [Parameter(Mandatory=$true)][string]$CadenceRoot,
 [string]$PstswpExecutable
)
$ErrorActionPreference='Stop'
$source=[IO.Path]::GetFullPath($SourceDsn)
$config=[IO.Path]::GetFullPath($ConfigFile)
$out=[IO.Path]::GetFullPath($OutputRoot)
$exe=if($PstswpExecutable){[IO.Path]::GetFullPath($PstswpExecutable)}else{Join-Path $CadenceRoot 'tools\bin\pstswp.exe'}
foreach($file in @($source,$config,$exe)){if(!(Test-Path -LiteralPath $file -PathType Leaf)){throw "Missing input or executable: $file"}}
$token=(Get-Date -Format 'yyyyMMdd_HHmmss')+'_'+[Guid]::NewGuid().ToString('N').Substring(0,8)
$run=Join-Path $out $token
if(Test-Path -LiteralPath $run){throw 'Refusing to overwrite an existing export run'}
$sch=Join-Path $run 'sch'
$net=Join-Path $run 'netlist'
New-Item -ItemType Directory -Path $sch,$net -Force|Out-Null
$sourceHash=(Get-FileHash -LiteralPath $source -Algorithm SHA256).Hash
$staged=Join-Path $sch ([IO.Path]::GetFileName($source))
$stagedConfig=Join-Path $sch 'allegro.cfg'
Copy-Item -LiteralPath $source -Destination $staged
Copy-Item -LiteralPath $config -Destination $stagedConfig
$copyHash=(Get-FileHash -LiteralPath $staged -Algorithm SHA256).Hash
$afterCopyHash=(Get-FileHash -LiteralPath $source -Algorithm SHA256).Hash
if($sourceHash -ne $copyHash -or $sourceHash -ne $afterCopyHash){throw 'Source changed during snapshot; save the design and rerun'}
$savedCdsRoot=$env:CDSROOT;$savedPath=$env:PATH
$env:CDSROOT=$CadenceRoot
$env:PATH=(Join-Path $CadenceRoot 'tools\bin')+';'+$env:PATH
try { & $exe -pst -d $staged -n $net -c $stagedConfig -v 3 -l 255 -j 'PCB Footprint' *> (Join-Path $run 'console.txt')
$code=$LASTEXITCODE } finally { $env:CDSROOT=$savedCdsRoot;$env:PATH=$savedPath }
$afterExportHash=(Get-FileHash -LiteralPath $source -Algorithm SHA256).Hash
$required=@('pstchip.dat','pstxprt.dat','pstxnet.dat')
$files=@(foreach($name in $required){$p=Join-Path $net $name;if(Test-Path -LiteralPath $p -PathType Leaf){$f=Get-Item -LiteralPath $p;[pscustomobject]@{name=$name;bytes=$f.Length;sha256=(Get-FileHash -LiteralPath $p -Algorithm SHA256).Hash}}})
$logPath=Join-Path $net 'netlist.log'
$log=if(Test-Path -LiteralPath $logPath){[IO.File]::ReadAllText($logPath)}else{''}
$errorCount=([regex]::Matches($log,'ERROR\(')).Count
$partNameTruncationWarnings=([regex]::Matches($log,'ORCAP-36006')).Count
$pass=($afterExportHash -eq $sourceHash -and (Test-Path -LiteralPath $logPath -PathType Leaf) -and $code -eq 0 -and $files.Count -eq 3 -and @($files|Where-Object bytes -le 0).Count -eq 0 -and $errorCount -eq 0 -and $partNameTruncationWarnings -eq 0)
$report=[ordered]@{status=if($pass){'PASS_NATIVE_PST255_EXPORT'}else{'FAIL_NATIVE_PST255_EXPORT'};created_local=[DateTimeOffset]::Now.ToString('o');source=$source;source_sha256_at_snapshot=$sourceHash;source_sha256_after_export=$afterExportHash;source_not_written_by_exporter=$true;source_unchanged=($afterExportHash -eq $sourceHash);staged_dsn=$staged;staged_dsn_sha256_after_packaging=(Get-FileHash -LiteralPath $staged -Algorithm SHA256).Hash;configuration=$config;configuration_sha256=(Get-FileHash -LiteralPath $stagedConfig -Algorithm SHA256).Hash;maximum_name_characters=255;pstswp_executable=$exe;pstswp_executable_sha256=(Get-FileHash -LiteralPath $exe -Algorithm SHA256).Hash;netlist_directory=$net;pstswp_exit=$code;error_count=$errorCount;part_name_truncation_warnings=$partNameTruncationWarnings;files=$files;scope='Native PST export only. Uses a verified saved-file snapshot. Does not include unsaved Capture edits or establish PCB/DRC/manufacturing correctness.'}
$report|ConvertTo-Json -Depth 5|Set-Content -LiteralPath (Join-Path $run 'export_validation.json') -Encoding UTF8
$report|ConvertTo-Json -Depth 5|Set-Content -LiteralPath (Join-Path $out 'latest_export.json') -Encoding UTF8
[pscustomobject]$report
if(!$pass){throw "PST export failed; inspect $logPath"}