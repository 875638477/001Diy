# Isolated behavioral tests. Every created file stays under 01AIEDA.
$ErrorActionPreference = 'Stop'
$workspace = [IO.Path]::GetFullPath((Join-Path $PSScriptRoot '..\..\..'))
$testsBase = Join-Path $workspace '01AIEDA\learning\staging\cleanup_review_20261019\tests'
$runRoot = Join-Path $testsBase ('run_' + [DateTime]::UtcNow.ToString('yyyyMMdd_HHmmss') + '_' + [guid]::NewGuid().ToString('N').Substring(0,8))
[IO.Directory]::CreateDirectory($runRoot) | Out-Null
$script:AllowedFixtureRoots = New-Object 'System.Collections.Generic.List[string]'
$script:Results = New-Object 'System.Collections.Generic.List[object]'
$script:Skips = New-Object 'System.Collections.Generic.List[string]'
$payload = Join-Path $PSScriptRoot 'eda_cleanup_payload.ps1'
$oldLoad = $env:EDA_CLEAN_LOAD_ONLY
$env:EDA_CLEAN_LOAD_ONLY = '1'
try { . ([ScriptBlock]::Create([IO.File]::ReadAllText($payload,[Text.Encoding]::UTF8))) }
finally { $env:EDA_CLEAN_LOAD_ONLY = $oldLoad }

function Check([string]$Name, [bool]$Condition, [string]$Detail='') {
    $script:Results.Add([pscustomobject]@{name=$Name;pass=$Condition;detail=$Detail})
    Write-Host ((@('FAIL','PASS')[[int]$Condition]) + ' ' + $Name)
}
function Throws([scriptblock]$Action) {
    try { & $Action | Out-Null; return $false } catch { return $true }
}
function New-Fixture([string]$Name) {
    $path = [IO.Path]::GetFullPath((Join-Path $runRoot $Name))
    if (-not $path.StartsWith($runRoot + '\',[StringComparison]::OrdinalIgnoreCase)) { throw 'Fixture path escape.' }
    [IO.Directory]::CreateDirectory($path) | Out-Null
    $script:AllowedFixtureRoots.Add($path)
    return $path
}
function Add-File([string]$Root,[string]$Relative,[string]$Content='fixture') {
    $path = [IO.Path]::GetFullPath((Join-Path $Root $Relative))
    if (-not $path.StartsWith($runRoot + '\',[StringComparison]::OrdinalIgnoreCase)) { throw 'Fixture file path escape.' }
    [IO.Directory]::CreateDirectory([IO.Path]::GetDirectoryName($path)) | Out-Null
    [IO.File]::WriteAllText($path,$Content,(New-Object Text.UTF8Encoding($false)))
    return $path
}
function Exists([string]$Root,[string]$Relative) { return [IO.File]::Exists((Join-Path $Root $Relative)) }
function Get-Snapshot([string]$Root) {
    $pairs = @(Get-ChildItem -LiteralPath $Root -Recurse -File -Force | Sort-Object FullName | ForEach-Object {
        $_.FullName.Substring($Root.Length + 1) + ':' + (Get-FileHash -LiteralPath $_.FullName -Algorithm SHA256).Hash
    })
    return $pairs -join '|'
}

# Exercise the unmodified production guards before a narrowly scoped test override.
$guardRoot = New-Fixture 'guard_protected_ancestor'
Check 'Production rejects roots anywhere under 01AIEDA' (Throws { Assert-CleanupRoot $guardRoot })
Check 'Production rejects drive root' (Throws { Assert-CleanupRoot ([IO.Path]::GetPathRoot($workspace)) })
Check 'Boundary guard rejects sibling prefix' (Throws { Assert-UnderRoot ($workspace + '-sibling\allegro.log') $workspace })
Check 'Boundary guard accepts literal child with punctuation' ((Assert-UnderRoot (Join-Path $workspace "sub !& (x) ' q\allegro.log") $workspace).StartsWith($workspace + '\'))

# Only roots created above by this test can enter the full pipeline. All other guards remain intact.
function Assert-CleanupRoot([string]$Root) {
    $full = [IO.Path]::GetFullPath($Root).TrimEnd('\')
    if (-not $script:AllowedFixtureRoots.Contains($full)) { throw 'Test override rejects any root not created by this test.' }
    if (-not $full.StartsWith($runRoot + '\',[StringComparison]::OrdinalIgnoreCase)) { throw 'Test root escaped fixture area.' }
    $item = Get-Item -LiteralPath $full -Force
    if ($item.Attributes -band [IO.FileAttributes]::ReparsePoint) { throw 'Test fixture root cannot be a reparse point.' }
}
function Get-BlockingProcesses { return @() }
Check 'Fixture-only override refuses actual workspace' (Throws { Assert-CleanupRoot $workspace })

$special = 'literal space !& (x) '' q ' + [char]0x6D4B + [char]0x8BD5
$root = New-Fixture $special
$null = Add-File $root 'design.dsn'
foreach ($name in @('allegro.log','allegro.log,1','allegro.LOG','netrev.lst','allegro.jrl','custom.log','notes.txt','pstxnet.dat','allegro.cfg','constraints.sct','linker.xcl','design.opj','firmware.axf','firmware.hex','firmware.bin','firmware.elf','source.zip','backup.dbk','library.obk','netlist.xml','devices.dml','output.out','source.c')) { $null=Add-File $root $name }
foreach ($dir in @('backup','Backups','archive','archives','history','original','release','01AIEDA','01env','.git')) { $null=Add-File $root ($dir+'\allegro.log') }
$before=Get-Snapshot $root
Invoke-EDACleanup $root @('/preview')
Check 'Preview modifies no fixture contents' ($before -eq (Get-Snapshot $root))
Invoke-EDACleanup $root @()
foreach ($name in @('allegro.log','allegro.log,1','netrev.lst')) { Check ('Default removes named log '+$name) (-not (Exists $root $name)) }
foreach ($name in @('allegro.jrl','custom.log','notes.txt','pstxnet.dat','allegro.cfg','constraints.sct','linker.xcl','design.opj','firmware.axf','firmware.hex','firmware.bin','firmware.elf','source.zip','backup.dbk','library.obk','netlist.xml','devices.dml','output.out','source.c')) { Check ('Default preserves '+$name) (Exists $root $name) }
foreach ($dir in @('backup','Backups','archive','archives','history','original','release','01AIEDA','01env','.git')) { Check ('Default excludes '+$dir) (Exists $root ($dir+'\allegro.log')) }
Invoke-EDACleanup $root @('/history')
Check 'History explicitly removes session journal' (-not (Exists $root 'allegro.jrl'))

$unknown = New-Fixture 'unknown_option'
$null=Add-File $unknown 'design.dsn';$null=Add-File $unknown 'allegro.log'
Check 'Unknown option fails before deleting' (Throws { Invoke-EDACleanup $unknown @('/anything') })
Check 'Unknown option retains candidate' (Exists $unknown 'allegro.log')

$none=New-Fixture 'no_source_project'
foreach($relative in @('Objects\test.obj','allegro.log','JLinkLog.txt')) { $null=Add-File $none $relative }
Invoke-EDACleanup $none @('/build','/history')
foreach($relative in @('Objects\test.obj','allegro.log','JLinkLog.txt')) { Check ('No project context preserves '+$relative) (Exists $none $relative) }

$embedded=New-Fixture 'keil_build'
$null=Add-File $embedded 'design.uvprojx'
foreach($relative in @('Objects\test.obj','Objects\test.o','Objects\test.d','Objects\test.dep','Objects\firmware.axf','Objects\firmware.elf','Objects\firmware.hex','Objects\firmware.bin','Objects\library.lib','Objects\library.a','Objects\linker.xcl','source\test.obj','Objects\notes.txt','Listings\test.lst','JLinkLog.txt')) { $null=Add-File $embedded $relative }
Invoke-EDACleanup $embedded @()
Check 'Default preserves opt-in intermediate' (Exists $embedded 'Objects\test.obj')
Check 'Default removes recognized J-Link log' (-not (Exists $embedded 'JLinkLog.txt'))
Invoke-EDACleanup $embedded @('/build')
foreach($relative in @('Objects\test.obj','Objects\test.o','Objects\test.d','Objects\test.dep','Listings\test.lst')) { Check ('Build removes intermediate '+$relative) (-not (Exists $embedded $relative)) }
foreach($relative in @('Objects\firmware.axf','Objects\firmware.elf','Objects\firmware.hex','Objects\firmware.bin','Objects\library.lib','Objects\library.a','Objects\linker.xcl','source\test.obj','Objects\notes.txt')) { Check ('Build preserves '+$relative) (Exists $embedded $relative) }

$version=New-Fixture 'versions'
$null=Add-File $version 'design.dsn'
foreach($dir in @('v1','v2','version1','17.2')) {
    $null=Add-File $version ($dir+'\allegro.log')
    $null=Add-File $version ($dir+'\design.dsn')
}
Invoke-EDACleanup $version @()
foreach($dir in @('v1','v2','version1','17.2')) {
    Check ('Version-named working directory source preserved '+$dir) (Exists $version ($dir+'\design.dsn'))
    Check ('Version-named working directory diagnostic log cleaned '+$dir) (-not (Exists $version ($dir+'\allegro.log')))
}

$ad=New-Fixture 'altium'
$null=Add-File $ad 'project.PrjPcb'
foreach($name in @('board.PcbDocPreview','sheet.SchDocPreview','board.pcbdoc_viewstate','job.OutJob','board.PcbDoc.Zip','project.PrjGrp')) {$null=Add-File $ad $name}
Invoke-EDACleanup $ad @()
foreach($name in @('board.PcbDocPreview','sheet.SchDocPreview','board.pcbdoc_viewstate')) {Check ('Altium preview removed '+$name) (-not (Exists $ad $name))}
foreach($name in @('job.OutJob','board.PcbDoc.Zip','project.PrjGrp')) {Check ('Altium project/output/archive retained '+$name) (Exists $ad $name)}
$notAd=New-Fixture 'unrecognized_altium_extension'
$null=Add-File $notAd 'board.PcbDocPreview'
Invoke-EDACleanup $notAd @()
Check 'Unknown project preview-like extension retained' (Exists $notAd 'board.PcbDocPreview')

$copy=New-Fixture 'copy_templates'
$null=Add-File $copy '01env\BOM.txt' 'source BOM'
$null=Add-File $copy '01env\reports.txt' 'source report'
$null=Add-File $copy '01env\drill4noet.txt' 'source drill'
$null=Add-File $copy 'BOM.txt' 'existing user BOM'
$before=Get-Snapshot $copy
Invoke-EDACleanup $copy @('/preview') @('BOM.txt','reports.txt','drill4noet.txt') $true
Check 'Preview also prevents missing-template copies' ($before -eq (Get-Snapshot $copy))
Invoke-EDACleanup $copy @() @('BOM.txt','reports.txt','drill4noet.txt') $true
Check 'Copy retains existing BOM contents' ([IO.File]::ReadAllText((Join-Path $copy 'BOM.txt')) -eq 'existing user BOM')
Check 'Copy creates only missing report' ([IO.File]::ReadAllText((Join-Path $copy 'reports.txt')) -eq 'source report')
Check 'Copy creates only missing drill' ([IO.File]::ReadAllText((Join-Path $copy 'drill4noet.txt')) -eq 'source drill')
Check 'Source templates remain unchanged' ([IO.File]::ReadAllText((Join-Path $copy '01env\BOM.txt')) -eq 'source BOM')

$changed=New-Fixture 'changed_candidate'
$null=Add-File $changed 'design.dsn';$path=Add-File $changed 'allegro.log' 'old'
$candidate=@(Get-CleanupCandidates $changed $false $false)[0]
$null=$candidate.File.Length;$null=$candidate.File.LastWriteTimeUtc
[IO.File]::WriteAllText($path,'changed length and timestamp')
Check 'Changed candidate is rejected before deletion' (Throws { Assert-CurrentCandidate $candidate $changed })
Check 'Changed file remains present' ([IO.File]::Exists($path))

$junctionRoot=New-Fixture 'junction_project'
$outside=New-Fixture 'junction_outside'
$null=Add-File $junctionRoot 'design.dsn';$null=Add-File $outside 'allegro.log' 'outside sentinel'
$junction=Join-Path $junctionRoot 'linked'
try {
    New-Item -ItemType Junction -Path $junction -Target $outside -ErrorAction Stop | Out-Null
    Invoke-EDACleanup $junctionRoot @('/history','/build')
    Check 'Junction target is never traversed/deleted' (Exists $outside 'allegro.log')
} catch { $script:Skips.Add('Junction fixture could not be created: '+$_.Exception.Message) }

$linkRoot=New-Fixture 'file_symlink_project'
$linkOutside=New-Fixture 'file_symlink_outside'
$null=Add-File $linkRoot 'design.dsn'
$outsideLog=Add-File $linkOutside 'outside.log' 'outside regular file sentinel'
try {
    New-Item -ItemType SymbolicLink -Path (Join-Path $linkRoot 'allegro.log') -Target $outsideLog -ErrorAction Stop | Out-Null
    Invoke-EDACleanup $linkRoot @()
    Check 'File symlink is never selected or deleted' ([bool](Get-Item -LiteralPath (Join-Path $linkRoot 'allegro.log') -Force -ErrorAction SilentlyContinue))
    Check 'File symlink external target remains unchanged' ([IO.File]::ReadAllText($outsideLog) -eq 'outside regular file sentinel')
} catch { $script:Skips.Add('File symlink fixture could not be created: '+$_.Exception.Message) }

$dangling=New-Fixture 'dangling_template_destination'
$null=Add-File $dangling '01env\BOM.txt' 'source BOM'
$null=Add-File $dangling '01env\reports.txt' 'source report'
$missingTarget=Join-Path $linkOutside 'never_create_this.txt'
try {
    New-Item -ItemType SymbolicLink -Path (Join-Path $dangling 'reports.txt') -Target $missingTarget -ErrorAction Stop | Out-Null
    Invoke-EDACleanup $dangling @() @('reports.txt')
    Check 'Dangling destination template symlink retained' ([bool](Get-Item -LiteralPath (Join-Path $dangling 'reports.txt') -Force -ErrorAction SilentlyContinue))
    Check 'Template copy never follows dangling destination link' (-not [IO.File]::Exists($missingTarget))
} catch { $script:Skips.Add('Dangling symlink fixture could not be created: '+$_.Exception.Message) }

$failures=@($script:Results | Where-Object { -not $_.pass })
$report=[pscustomobject]@{fixture_root=$runRoot;production_payload_sha256=(Get-FileHash -LiteralPath $payload -Algorithm SHA256).Hash;checks=$script:Results.Count;failures=$failures.Count;skips=$script:Skips.ToArray();results=$script:Results.ToArray()}
$reportPath=Join-Path $runRoot 'results.json'
[IO.File]::WriteAllText($reportPath,($report | ConvertTo-Json -Depth 8),(New-Object Text.UTF8Encoding($false)))
Write-Host "RESULT checks=$($script:Results.Count) failures=$($failures.Count) report=$reportPath"
if($failures.Count){exit 1}
exit 0
