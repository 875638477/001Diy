param([Parameter(Mandatory=$true)][string]$InputBoard,[Parameter(Mandatory=$true)][string]$OutputDirectory,[Parameter(Mandatory=$true)][string]$SkillFile,[Parameter(Mandatory=$true)][string]$Expression,[switch]$WriteCandidate,[int]$TimeoutSeconds=180,[string]$CompareBoard)
$ErrorActionPreference='Stop'
$project=[IO.Path]::GetFullPath($PSScriptRoot)
$source=[IO.Path]::GetFullPath($InputBoard);$run=[IO.Path]::GetFullPath($OutputDirectory);$script=[IO.Path]::GetFullPath($SkillFile)
if(Test-Path -LiteralPath $run){throw 'Fresh output directory required'}
if(!$run.StartsWith((Join-Path $project 'w/'),[StringComparison]::OrdinalIgnoreCase)){throw 'Native job must remain below project13/w'}
$shaBefore=(Get-FileHash -LiteralPath $source -Algorithm SHA256).Hash
[void][IO.Directory]::CreateDirectory($run)
[void][IO.Directory]::CreateDirectory((Join-Path $run 'before'))
[void][IO.Directory]::CreateDirectory((Join-Path $run 'after'))
foreach($n in @('after_fill_off','after_delete','after_restore')){[void][IO.Directory]::CreateDirectory((Join-Path $run $n))}
$copy=Join-Path $run 'INPUT_COPY.brd';Copy-Item -LiteralPath $source -Destination $copy
if($CompareBoard){$compareSource=[IO.Path]::GetFullPath($CompareBoard);$compareSha=(Get-FileHash -LiteralPath $compareSource -Algorithm SHA256).Hash;$compareCopy=Join-Path $run 'COMPARE_COPY.brd';Copy-Item -LiteralPath $compareSource -Destination $compareCopy}
if($Expression -match '^[A-Za-z_][A-Za-z0-9_]*$'){$Expression=$Expression+'("'+$run.Replace('\','/')+'")'}
function S([string]$x){if($x.Contains('"')){throw 'Unsupported quote'};'"'+$x.Replace('\','/')+'"'}
$scr=Join-Path $run 'run.scr'
[IO.File]::WriteAllLines($scr,@('set NOCONFIRM',('skill errset(load('+(S $script)+') t)'),('skill errset('+$Expression.Replace('{RUN}', $run.Replace('\','/'))+' t)'),'quit','fillin "yes"'),[Text.Encoding]::ASCII)
$args=@('-product','Allegro_performance','-safe','-nographic');if(!$WriteCandidate){$args+='-readonly'};$args+=@('-s',$scr,'-p',$run,$copy)
$pi=[Diagnostics.ProcessStartInfo]::new();$pi.FileName='C:\Program0\Cadence\SPB172\tools\bin\allegro.exe';$pi.Arguments=($args|ForEach-Object {S $_}) -join ' ';$pi.WorkingDirectory=$run;$pi.UseShellExecute=$false;$pi.CreateNoWindow=$true;$pi.WindowStyle=[Diagnostics.ProcessWindowStyle]::Hidden;$pi.RedirectStandardOutput=$true;$pi.RedirectStandardError=$true
$pi.EnvironmentVariables['CDSROOT']='C:\Program0\Cadence\SPB172';$pi.EnvironmentVariables['PATH']='C:\Program0\Cadence\SPB172\tools\bin;'+$pi.EnvironmentVariables['PATH'];$pi.EnvironmentVariables['ALLEGRO_PCBENV']=Join-Path $project 'pcbenv';$pi.EnvironmentVariables['LGA1700_PROJECT_ROOT']=$project.Replace('\','/')
$proc=[Diagnostics.Process]::new();$proc.StartInfo=$pi;[void]$proc.Start();$so=$proc.StandardOutput.ReadToEndAsync();$se=$proc.StandardError.ReadToEndAsync();if(!$proc.WaitForExit($TimeoutSeconds*1000)){$proc.Kill();throw 'Native process timeout'};$proc.WaitForExit()
[IO.File]::WriteAllText((Join-Path $run 'stdout.txt'),$so.Result);[IO.File]::WriteAllText((Join-Path $run 'stderr.txt'),$se.Result)
$shaAfter=(Get-FileHash -LiteralPath $source -Algorithm SHA256).Hash
$report=[ordered]@{source=$source;source_sha256_before=$shaBefore;source_sha256_after=$shaAfter;input_unchanged=($shaBefore -ceq $shaAfter);staged_input=$copy;staged_sha256=(Get-FileHash -LiteralPath $copy -Algorithm SHA256).Hash;script=$script;script_sha256=(Get-FileHash -LiteralPath $script -Algorithm SHA256).Hash;arguments=$args;expression=$Expression;exit_code=$proc.ExitCode;write_candidate=[bool]$WriteCandidate;created_local=[DateTimeOffset]::Now.ToString('o')}
if($CompareBoard){$compareAfter=(Get-FileHash -LiteralPath $compareSource -Algorithm SHA256).Hash;$report['compare_source']=$compareSource;$report['compare_source_sha256_before']=$compareSha;$report['compare_source_sha256_after']=$compareAfter;$report['compare_copy_sha256']=(Get-FileHash -LiteralPath $compareCopy -Algorithm SHA256).Hash;if($compareAfter -cne $compareSha -or $report['compare_copy_sha256'] -cne $compareSha){throw 'Comparison board changed'}}
$report|ConvertTo-Json -Depth 6|Set-Content -LiteralPath (Join-Path $run 'launch_report.json') -Encoding UTF8
if($shaAfter -cne $shaBefore){throw 'Native job modified source input'}
$report|ConvertTo-Json -Depth 6
