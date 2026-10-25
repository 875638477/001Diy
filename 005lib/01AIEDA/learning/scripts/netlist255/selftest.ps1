param([Parameter(Mandatory=$true)][string]$OutputDirectory)
$ErrorActionPreference='Stop'
$root=[IO.Path]::GetFullPath($OutputDirectory)
if(Test-Path -LiteralPath $root){throw 'Selftest output must be new'}
[void][IO.Directory]::CreateDirectory($root)
$source=Join-Path $root 'SYNTHETIC_INPUT.DSN';$config=Join-Path $root 'allegro.cfg'
[IO.File]::WriteAllText($source,'SYNTHETIC FIXTURE; NOT A CAD FILE')
[IO.File]::WriteAllText($config,'SYNTHETIC CONFIG')
$sourceHash=(Get-FileHash -LiteralPath $source -Algorithm SHA256).Hash
$mock=Join-Path $root 'mock_pstswp.ps1'
$mockCode=@'
param([switch]$pst,[string]$d,[string]$n,[string]$c,[string]$v,[string]$l,[string]$j)
if($l -ne '255'){throw 'Fixture expected explicit character limit255'}
[void][IO.Directory]::CreateDirectory($n)
foreach($name in @('pstchip.dat','pstxnet.dat','pstxprt.dat')){[IO.File]::WriteAllText((Join-Path $n $name),'SYNTHETIC PST '+$name)}
if($env:EDA_FIXTURE_MODE -eq 'FAIL'){
 [IO.File]::WriteAllText((Join-Path $n 'netlist.log'),'ERROR(FAKE): intentional fixture failure')
 $global:LASTEXITCODE=1
}elseif($env:EDA_FIXTURE_MODE -eq 'MUTATE_SOURCE'){
 [IO.File]::WriteAllText($env:EDA_FIXTURE_SOURCE,'EXTERNAL CHANGE SIMULATION')
 [IO.File]::WriteAllText((Join-Path $n 'netlist.log'),'FAKE successful log; source changed independently')
 $global:LASTEXITCODE=0
}else{
 [IO.File]::WriteAllText((Join-Path $n 'netlist.log'),'FAKE no errors')
 $global:LASTEXITCODE=0
}
'@
[IO.File]::WriteAllText($mock,$mockCode,[Text.UTF8Encoding]::new($false))
$exports=Join-Path $root 'exports';$active=Join-Path $root 'active_netlist'
$exporter=Join-Path $PSScriptRoot 'export_pst255.ps1';$publisher=Join-Path $PSScriptRoot 'publish_pst255.ps1'
$savedMode=$env:EDA_FIXTURE_MODE;$savedSource=$env:EDA_FIXTURE_SOURCE
$checks=[Collections.Generic.List[string]]::new()
function InvokeFixture {
 & $publisher -SourceDsn $source -ConfigFile $config -OutputRoot $exports -PublishDirectory $active -ExporterFile $exporter -CadenceRoot $root -PstswpExecutable $mock | Out-Null
}
function RejectFixture([scriptblock]$Operation){
 $failed=$false;try{& $Operation}catch{$failed=$true}
 if(!$failed){throw 'Expected fixture rejection'}
}
try{
 $env:EDA_FIXTURE_MODE='PASS';$env:EDA_FIXTURE_SOURCE=$source
 InvokeFixture
 $published=Get-Content -LiteralPath (Join-Path $exports 'latest_publication.json') -Raw -Encoding UTF8|ConvertFrom-Json
 if($published.status -ne 'PASS_PUBLISHED_VALIDATED_PST255' -or (Get-FileHash -LiteralPath $source -Algorithm SHA256).Hash -ne $sourceHash){throw 'Synthetic publish/source check failed'}
 $checks.Add('Successful mock export publishes three nonempty files; source SHA retained')
 $activeHashes=@{};Get-ChildItem -LiteralPath $active -File|ForEach-Object{$activeHashes[$_.Name]=(Get-FileHash -LiteralPath $_.FullName -Algorithm SHA256).Hash}
 $publishedHash=(Get-FileHash -LiteralPath (Join-Path $exports 'latest_publication.json') -Algorithm SHA256).Hash
 $env:EDA_FIXTURE_MODE='FAIL';RejectFixture {InvokeFixture}
 foreach($name in $activeHashes.Keys){if((Get-FileHash -LiteralPath (Join-Path $active $name) -Algorithm SHA256).Hash -ne $activeHashes[$name]){throw 'Failure changed active output'}}
 if((Get-FileHash -LiteralPath (Join-Path $exports 'latest_publication.json') -Algorithm SHA256).Hash -ne $publishedHash){throw 'Failed export changed publication metadata'}
 $checks.Add('Native-like failure preserves active output and successful publication pointer')
 $env:EDA_FIXTURE_MODE='MUTATE_SOURCE';RejectFixture {InvokeFixture}
 foreach($name in $activeHashes.Keys){if((Get-FileHash -LiteralPath (Join-Path $active $name) -Algorithm SHA256).Hash -ne $activeHashes[$name]){throw 'Source-change rejection altered active output'}}
 [IO.File]::WriteAllText($source,'SYNTHETIC FIXTURE; NOT A CAD FILE')
 $checks.Add('External source change rejects snapshot publication')
 $env:EDA_FIXTURE_MODE='PASS'
 $lock=[IO.File]::Open((Join-Path $exports '.publish.lock'),[IO.FileMode]::OpenOrCreate,[IO.FileAccess]::ReadWrite,[IO.FileShare]::None)
 try{RejectFixture {InvokeFixture}}finally{$lock.Dispose()}
 $checks.Add('Concurrent publisher lock rejected')
 RejectFixture {& $publisher -SourceDsn $source -ConfigFile $config -OutputRoot $exports -PublishDirectory $root -ExporterFile $exporter -CadenceRoot $root -PstswpExecutable $mock}
 $checks.Add('Publish-directory overlap with protected inputs/export storage rejected')
 foreach($p in @($exporter,$publisher)){
  $tokens=$null;$errors=$null;[void][Management.Automation.Language.Parser]::ParseFile($p,[ref]$tokens,[ref]$errors)
  if($errors.Count){throw 'PowerShell parser errors'}
 }
 $checks.Add('Both PowerShell tools pass native parser without loading CAD')
 $report=[ordered]@{status='PASS_SYNTHETIC_PST255_PUBLISH_FIXTURES';checks=@($checks);CAD_started=$false;mock_backend=$true;project_files_read_or_written=$false;scope='Mock backend validates snapshot/publication guards only; not a new Cadence execution or license validation.'}
 $report|ConvertTo-Json -Depth 5|Set-Content -LiteralPath (Join-Path $root 'report.json') -Encoding UTF8
 $report|ConvertTo-Json -Depth 5
}finally{$env:EDA_FIXTURE_MODE=$savedMode;$env:EDA_FIXTURE_SOURCE=$savedSource}
