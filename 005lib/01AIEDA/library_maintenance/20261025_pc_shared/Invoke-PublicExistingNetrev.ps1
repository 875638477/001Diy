param([Parameter(Mandatory=$true)][string]$InputBoard,[Parameter(Mandatory=$true)][string]$OutputDirectory,[Parameter(Mandatory=$true)][string]$NetlistDirectory)
$ErrorActionPreference='Stop'
$project=[IO.Path]::GetFullPath($PSScriptRoot)
$run=[IO.Path]::GetFullPath($OutputDirectory);$src=[IO.Path]::GetFullPath($InputBoard);$net=[IO.Path]::GetFullPath($NetlistDirectory)
if(!$run.StartsWith((Join-Path $project 'w/'),[StringComparison]::OrdinalIgnoreCase) -or (Test-Path -LiteralPath $run)){throw 'Fresh in-project w output required'}
[void][IO.Directory]::CreateDirectory($run)
$h=(Get-FileHash -LiteralPath $src -Algorithm SHA256).Hash
$copy=Join-Path $run 'INPUT_COPY.brd';$out=Join-Path $run 'LIVE_IMPORTED.brd';Copy-Item -LiteralPath $src -Destination $copy
$pi=[Diagnostics.ProcessStartInfo]::new();$pi.FileName='C:\Program0\Cadence\SPB172\tools\bin\netrev.exe'
$a=@('-y','2','-i',$net,$copy,$out)
$pi.Arguments=($a|ForEach-Object {'"'+$_+'"'}) -join ' ';$pi.WorkingDirectory=$run;$pi.UseShellExecute=$false;$pi.CreateNoWindow=$true;$pi.WindowStyle='Hidden';$pi.RedirectStandardOutput=$true;$pi.RedirectStandardError=$true
$pi.EnvironmentVariables['CDSROOT']='C:\Program0\Cadence\SPB172';$pi.EnvironmentVariables['PATH']='C:\Program0\Cadence\SPB172\tools\bin;'+$pi.EnvironmentVariables['PATH'];$pi.EnvironmentVariables['ALLEGRO_PCBENV']=Join-Path $project 'pcbenv';$pi.EnvironmentVariables['LGA1700_PROJECT_ROOT']=$project.Replace('\','/')
$p=[Diagnostics.Process]::new();$p.StartInfo=$pi;[void]$p.Start();$so=$p.StandardOutput.ReadToEndAsync();$se=$p.StandardError.ReadToEndAsync()
if(!$p.WaitForExit(180000)){$p.Kill();throw 'Owned netrev process timed out'};$p.WaitForExit()
[IO.File]::WriteAllText((Join-Path $run 'stdout.txt'),$so.Result);[IO.File]::WriteAllText((Join-Path $run 'stderr.txt'),$se.Result)
if($p.ExitCode -ne 0 -or !(Test-Path -LiteralPath $out)){throw 'Native netrev failed'}
$log=[IO.File]::ReadAllText((Join-Path $run 'netrev.lst'));$counts=@{};foreach($k in @('ERROR','WARNING','OVERSIGHT')){$counts[$k]=[regex]::Matches($log,($k+'\(')).Count}
if(@($counts.Values|Where-Object {$_ -gt 0}).Count){throw 'Native netrev log contains errors/warnings/oversights'}
if((Get-FileHash -LiteralPath $src -Algorithm SHA256).Hash -cne $h -or (Get-FileHash -LiteralPath $copy -Algorithm SHA256).Hash -cne $h){throw 'Input modified'}
[ordered]@{status='PASS_NATIVE_NETREV_ONLY_PENDING_FULL_READBACK';input=$src;input_sha256=$h;output=$out;output_sha256=(Get-FileHash -LiteralPath $out -Algorithm SHA256).Hash;arguments=$a;counts=$counts;fill_policy='Input retains original wysiwyg; no fill-mode setter, ripup flag or fixed override. The existing public-board path preserves the source DRC control state; no DRC signoff.'}|ConvertTo-Json -Depth 4|Set-Content -LiteralPath (Join-Path $run 'LIVE_NETREV.json') -Encoding UTF8
Write-Output $out
