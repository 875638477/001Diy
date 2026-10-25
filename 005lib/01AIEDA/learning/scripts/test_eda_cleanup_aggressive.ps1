# Independent isolated tests for the aggressive cleanup policy; never clean a user project.
$ErrorActionPreference = 'Stop'
$workspace = [IO.Path]::GetFullPath((Join-Path $PSScriptRoot '..\..\..'))
$testsBase = Join-Path $workspace '01AIEDA\learning\staging\cleanup_review_20261019\aggressive\tests'
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
function Throws([scriptblock]$Action) { try { & $Action | Out-Null; return $false } catch { return $true } }
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
function Add-Files([string]$Root,[string[]]$Names) { foreach($name in $Names) { $null=Add-File $Root $name } }
function Check-Files([string]$Root,[string[]]$Names,[bool]$Present,[string]$Prefix) {
    foreach($name in $Names) { Check ($Prefix+' '+$name) ((Exists $Root $name) -eq $Present) }
}
function Get-Snapshot([string]$Root) {
    $pairs = @(Get-ChildItem -LiteralPath $Root -Recurse -File -Force | Sort-Object FullName | ForEach-Object {
        $_.FullName.Substring($Root.Length + 1) + ':' + (Get-FileHash -LiteralPath $_.FullName -Algorithm SHA256).Hash
    })
    return $pairs -join '|'
}
function Set-Time([string]$Root,[string]$Relative,[int]$Day) {
    [IO.File]::SetLastWriteTimeUtc((Join-Path $Root $Relative),[DateTime]::ParseExact(('2020-01-'+$Day.ToString('00')+'T12:00:00Z'),'yyyy-MM-ddTHH:mm:ssZ',[Globalization.CultureInfo]::InvariantCulture).ToUniversalTime())
}
function Add-PureOPJ([string]$Root,[string]$Name,[string]$DSN='design.dsn') {
    $text='(ExpressProject "'+$Name+'"'+[Environment]::NewLine+
      '  (ProjectVersion "19981106")'+[Environment]::NewLine+
      '  (ProjectType "PCB")'+[Environment]::NewLine+
      '  (Folder "Design Resources"'+[Environment]::NewLine+
      '    (Folder "Library" (File "library.olb" (Type "Symbol Library")))'+[Environment]::NewLine+
      '    (File "'+$DSN+'" (Type "Schematic Design"))'+[Environment]::NewLine+
      '    (NoModify))'+[Environment]::NewLine+'  (Folder "Outputs"))'+[Environment]::NewLine
    return Add-File $Root ($Name+'.opj') $text
}

# The production guard is exercised before its fixture-only override.
$guardRoot=New-Fixture 'guard_protected_ancestor'
Check 'Production refuses roots anywhere below 01AIEDA' (Throws { Assert-CleanupRoot $guardRoot })
Check 'Production refuses the drive root' (Throws { Assert-CleanupRoot ([IO.Path]::GetPathRoot($workspace)) })
Check 'Boundary guard rejects sibling with matching prefix' (Throws { Assert-UnderRoot ($workspace+'-sibling\allegro.log') $workspace })
Check 'Boundary guard accepts a literal child path' ((Assert-UnderRoot (Join-Path $workspace "sub !& (x) ' q\allegro.log") $workspace).StartsWith($workspace+'\'))
function Assert-CleanupRoot([string]$Root) {
    $full=[IO.Path]::GetFullPath($Root).TrimEnd('\')
    if (-not $script:AllowedFixtureRoots.Contains($full)) { throw 'Test override rejects roots not created by this test.' }
    if (-not $full.StartsWith($runRoot+'\',[StringComparison]::OrdinalIgnoreCase)) { throw 'Test root escaped fixture area.' }
    $item=Get-Item -LiteralPath $full -Force
    if ($item.Attributes -band [IO.FileAttributes]::ReparsePoint) { throw 'Fixture root cannot be a reparse point.' }
}
function Get-BlockingProcesses { return @() }
Check 'Fixture-only override refuses the real workspace' (Throws { Assert-CleanupRoot $workspace })

$special='literal space !& (x) '' q '+[char]0x6D4B+[char]0x8BD5
$cad=New-Fixture $special
$null=Add-File $cad 'design.dsn'
$cadDelete=@('allegro.log','allegro.log,1','custom.log','CUSTOM.LOG,9','netrev.lst','custom.lst','report.rpt','report.rpt,2','allegro.jrl','capture.jrl','custom.jrl,8','cache.tmp','cache.tmp,2','dump.dmp','extract.iex','checks.drc','tags.tag')
$cadKeep=@('notes.txt','pstxnet.dat','allegro.cfg','constraints.sct','linker.xcl','firmware.hex','firmware.bin','firmware.elf','firmware.axf','source.zip','backup.dbk','orphan_library.obk','netlist.xml','devices.dml','memory.iml','stackup.dcf','converter.cnv','board.pro','control.ctl','batch.baf','output.out','source.c','design.opj','parts.csv','parts.bom','design.edf','library.olb','board.brd','symbol.dra','shape.psm','pin.pad','footprint.lib')
Add-Files $cad $cadDelete
Add-Files $cad $cadKeep
$protected=@('backup','Backups','archive','archives','history','original','release','01AIEDA','01env','.git','lib','library')
foreach($dir in $protected) { $null=Add-File $cad ($dir+'\custom.log');$null=Add-File $cad ($dir+'\cache.tmp') }
$before=Get-Snapshot $cad
Invoke-EDACleanup $cad @('/preview')
Check 'Preview leaves all files byte-identical' ($before -eq (Get-Snapshot $cad))
Invoke-EDACleanup $cad @()
Check-Files $cad $cadDelete $false 'Default removes Cadence generated file'
Check-Files $cad $cadKeep $true 'Default preserves design or current data'
foreach($dir in $protected) { Check ('Protected directory remains untouched '+$dir) ((Exists $cad ($dir+'\custom.log')) -and (Exists $cad ($dir+'\cache.tmp'))) }

$flags=New-Fixture 'legacy_flags_are_compatible'
Add-Files $flags @('design.dsn','custom.jrl','custom.log')
Invoke-EDACleanup $flags @('/history','/build')
Check-Files $flags @('custom.jrl','custom.log') $false 'Legacy positive flags remain accepted'
$unknown=New-Fixture 'unknown_option'
Add-Files $unknown @('design.dsn','custom.log')
Check 'Unknown option fails before deleting' (Throws { Invoke-EDACleanup $unknown @('/anything') })
Check 'Unknown option retains candidate' (Exists $unknown 'custom.log')
$before=Get-Snapshot $unknown
Invoke-EDACleanup $unknown @('/help')
Check 'Help does not modify any files' ($before -eq (Get-Snapshot $unknown))

$none=New-Fixture 'no_source_project'
Add-Files $none @('Objects\test.obj','custom.log','custom.jrl','JLinkLog.txt','scratch.tmp','Objects\scratch.tmp')
Invoke-EDACleanup $none @()
Check-Files $none @('scratch.tmp','Objects\scratch.tmp') $false 'Standalone temporary file removed'
Check-Files $none @('Objects\test.obj','custom.log','custom.jrl','JLinkLog.txt') $true 'No recognized project preserves other files'

foreach($project in @('keil.uvprojx','iar.ewp')) {
    $embedded=New-Fixture ($project.Replace('.','_'))
    $null=Add-File $embedded $project
    $buildDelete=@()
    foreach($extension in @('obj','o','d','dep','crf','lnp','lst','pbi','pbd','browse','linf','pbw','plg','__i','axf','omf','map','htm')) { $buildDelete+=('Objects\generated.'+$extension) }
    $buildDelete+=@('Listings\generated.lst','Debug\generated.obj','Build\generated.axf','Obj_Debug\generated.o','JLinkLog.txt','JLinkARM.log')
    $buildKeep=@('Objects\firmware.hex','Objects\firmware.bin','Objects\library.lib','Objects\library.a','Objects\linker.xcl','Objects\linker.sct','Objects\linker.icf','Objects\settings.cfg','Objects\notes.txt','source\manual.obj','source\memory.map','source\generated.c','include\generated.h','release\generated.axf','release\custom.log')
    Add-Files $embedded $buildDelete
    Add-Files $embedded $buildKeep
    Invoke-EDACleanup $embedded @()
    Check-Files $embedded $buildDelete $false ($project+' default removes rebuildable output')
    Check-Files $embedded $buildKeep $true ($project+' preserves source final firmware and config')
}

$ad=New-Fixture 'altium'
Add-Files $ad @('project.PrjPcb','board.PcbDocPreview','sheet.SchDocPreview','board.pcbdoc_viewstate','board.PCBPreview','sheet.SchPreview','project.PrjPCBStructure','cache.$$$Preview','job.OutJob','project.PrjGrp','board.PcbDoc.Zip','netlist.edf','settings.xml','component.csv')
Invoke-EDACleanup $ad @()
Check-Files $ad @('board.PcbDocPreview','sheet.SchDocPreview','board.pcbdoc_viewstate','board.PCBPreview','sheet.SchPreview','project.PrjPCBStructure','cache.$$$Preview') $false 'Altium preview cache removed'
Check-Files $ad @('job.OutJob','project.PrjGrp','board.PcbDoc.Zip','netlist.edf','settings.xml','component.csv') $true 'Altium project current data or orphan archive retained'

$opj=New-Fixture 'opj_policy'
Add-Files $opj @('design.dsn','library.olb')
$null=Add-PureOPJ $opj 'pure'
$guiText=@'
(ExpressProject "GUI"
  (ProjectVersion "19981106")
  (ProjectType "PCB")
  (Folder "Design Resources"
    (Folder "Library")
    (File ".\design.dsn" (Type "Schematic Design"))
    (BuildFileAddedOrDeleted "x")
    (CompileFileAddedOrDeleted "x")
    (NoModify))
  (Folder "Outputs")
  (Folder "Referenced Projects")
  (PartMRUSelector)
  (GlobalState
    (FileView (Path "Design Resources") (Select "Design Resources" ".\design.dsn" "TOP" "POWER"))
    (HierarchyView)
    (Doc (Type "COrCapturePMDoc") (Frame (Placement "44 2 3 -1 -1 -8 -31 0 200 0 246")) (Tab 0))
    (Doc (Type "COrSchematicDoc")
      (Frame (Placement "44 0 1 -1 -1 -8 -31 104 1655 104 661") (Scroll "0 183") (Zoom "66") (Occurrence "/"))
      (Path ".\design.dsn") (Schematic "TOP") (Page "POWER"))))
'@
$null=Add-File $opj 'gui.opj' $guiText
$null=Add-PureOPJ $opj 'missing' 'missing.dsn'
$null=Add-File $opj 'simulation.opj' '(ExpressProject "simulation" (ProjectType "PSpice") (Folder "Design Resources" (File "design.dsn" (Type "Schematic Design"))) (Folder "Simulation Resources"))'
$null=Add-File $opj 'cis.opj' '(ExpressProject "cis" (ProjectType "PCB") (Folder "Design Resources" (File "design.dsn" (Type "Schematic Design"))) (CISConfiguration "custom.dbc"))'
$null=Add-File $opj 'toolsettings.opj' '(ExpressProject "toolsettings" (ProjectType "PCB") (Folder "Design Resources" (File "design.dsn" (Type "Schematic Design"))) (ToolSettings "custom"))'
$null=Add-File $opj 'unknown.opj' 'unknown proprietary content'
$null=Add-File $opj 'malformed.opj' '(ExpressProject "broken" (ProjectType "PCB") (File "design.dsn" (Type "Schematic Design"))'
$null=Add-File $opj 'empty.opj' ''
Invoke-EDACleanup $opj @()
Check 'Pure schematic OPJ is removed only with existing DSN' (-not (Exists $opj 'pure.opj'))
Check 'Ordinary GUI-saved OPJ with window and MRU state is removed' (-not (Exists $opj 'gui.opj'))
Check-Files $opj @('missing.opj','simulation.opj','cis.opj','toolsettings.opj','unknown.opj','malformed.opj','empty.opj','design.dsn','library.olb') $true 'OPJ policy preserves unproven or specialized project'

$backup=New-Fixture 'backup_recovery_policy'
Add-Files $backup @('design.dsn','design.dbk','symbols.olb','symbols.obk','board.brd','board.brd,1','board.brd.bak','drawing.dra','drawing.sav','report.txt','report.txt,1','board.PcbDoc','board.PcbDoc.Zip','orphan.dbk','orphan.obk','orphan.brd,1','orphan.txt,1','orphan.PcbDoc.Zip','novel.dsn','novel.dbk','novel.brd','novel.brd,1')
$null=Add-File $backup 'empty.dsn' ''
$null=Add-File $backup 'empty.dbk' 'recoverable content'
$null=Add-File $backup 'zero.brd' ''
$null=Add-File $backup 'zero.brd,1' 'recoverable content'
foreach($name in @('design.dsn','symbols.olb','board.brd','drawing.dra','report.txt','board.PcbDoc','novel.dbk','novel.brd,1')) { Set-Time $backup $name 3 }
foreach($name in @('design.dbk','symbols.obk','board.brd,1','board.brd.bak','drawing.sav','report.txt,1','board.PcbDoc.Zip','novel.dsn','novel.brd')) { Set-Time $backup $name 2 }
Invoke-EDACleanup $backup @()
Check-Files $backup @('design.dbk','symbols.obk','board.brd,1','board.brd.bak','drawing.sav','report.txt,1','board.PcbDoc.Zip') $false 'Backup with nonempty newer main file removed'
Check-Files $backup @('orphan.dbk','orphan.obk','orphan.brd,1','orphan.txt,1','orphan.PcbDoc.Zip','novel.dbk','novel.brd,1','empty.dbk','zero.brd,1','design.dsn','symbols.olb','board.brd','report.txt','board.PcbDoc') $true 'Orphan newer recovery backup empty-main backup or main retained'

$copy=New-Fixture 'copy_templates'
$null=Add-File $copy '01env\BOM.txt' 'source BOM'
$null=Add-File $copy '01env\reports.txt' 'source report'
$null=Add-File $copy '01env\drill4noet.txt' 'source drill'
$null=Add-File $copy 'BOM.txt' 'existing user BOM'
$before=Get-Snapshot $copy
Invoke-EDACleanup $copy @('/preview') @('BOM.txt','reports.txt','drill4noet.txt') $true
Check 'Preview prevents template copies' ($before -eq (Get-Snapshot $copy))
Invoke-EDACleanup $copy @() @('BOM.txt','reports.txt','drill4noet.txt') $true
Check 'Template copy never overwrites existing user BOM' ([IO.File]::ReadAllText((Join-Path $copy 'BOM.txt')) -eq 'existing user BOM')
Check 'Template copy creates missing report' ([IO.File]::ReadAllText((Join-Path $copy 'reports.txt')) -eq 'source report')
Check 'Template copy creates missing drill' ([IO.File]::ReadAllText((Join-Path $copy 'drill4noet.txt')) -eq 'source drill')
Check 'Template source is unchanged' ([IO.File]::ReadAllText((Join-Path $copy '01env\BOM.txt')) -eq 'source BOM')

$changed=New-Fixture 'changed_candidate'
$null=Add-File $changed 'design.dsn'
$path=Add-File $changed 'custom.log' 'old'
$candidate=@(Get-CleanupCandidates $changed $true $true)[0]
$null=$candidate.File.Length;$null=$candidate.File.LastWriteTimeUtc
[IO.File]::WriteAllText($path,'changed length and timestamp')
Check 'Candidate modified since enumeration is rejected' (Throws { Assert-CurrentCandidate $candidate $changed })
Check 'Modified candidate is retained' ([IO.File]::Exists($path))

$changedMain=New-Fixture 'backup_main_changed_after_scan'
Add-Files $changedMain @('design.dsn','design.dbk')
Set-Time $changedMain 'design.dsn' 3
Set-Time $changedMain 'design.dbk' 2
$candidate=@(Get-CleanupCandidates $changedMain $true $true | Where-Object { $_.File.Name -eq 'design.dbk' })[0]
Check 'Reliable old backup is initially selected' ($null -ne $candidate)
[IO.File]::WriteAllText((Join-Path $changedMain 'design.dsn'),'')
Check 'Main file becoming empty invalidates backup deletion' (Throws { Assert-CurrentCandidate $candidate $changedMain })
Check 'Recovery backup remains after empty-main rejection' (Exists $changedMain 'design.dbk')
$null=Add-File $changedMain 'design.dsn'
Set-Time $changedMain 'design.dsn' 3
$candidate=@(Get-CleanupCandidates $changedMain $true $true | Where-Object { $_.File.Name -eq 'design.dbk' })[0]
Set-Time $changedMain 'design.dsn' 1
Check 'Main file becoming older invalidates backup deletion' (Throws { Assert-CurrentCandidate $candidate $changedMain })
Check 'Recovery backup remains after older-main rejection' (Exists $changedMain 'design.dbk')

$changedReference=New-Fixture 'opj_reference_changed_after_scan'
Add-Files $changedReference @('design.dsn','library.olb')
$null=Add-PureOPJ $changedReference 'pure'
$candidate=@(Get-CleanupCandidates $changedReference $true $true | Where-Object { $_.File.Name -eq 'pure.opj' })[0]
Check 'Pure OPJ is initially selected before reference change' ($null -ne $candidate)
[IO.File]::WriteAllText((Join-Path $changedReference 'design.dsn'),'')
Check 'DSN becoming empty invalidates OPJ deletion' (Throws { Assert-CurrentCandidate $candidate $changedReference })
Check 'OPJ remains after reference-change rejection' (Exists $changedReference 'pure.opj')

$junctionRoot=New-Fixture 'junction_project'
$outside=New-Fixture 'junction_outside'
$null=Add-File $junctionRoot 'design.dsn'
$null=Add-File $outside 'custom.log' 'outside sentinel'
try {
    New-Item -ItemType Junction -Path (Join-Path $junctionRoot 'linked') -Target $outside -ErrorAction Stop | Out-Null
    Invoke-EDACleanup $junctionRoot @()
    Check 'Directory junction target is never traversed or deleted' (Exists $outside 'custom.log')
} catch { $script:Skips.Add('Junction fixture unavailable: '+$_.Exception.Message) }
$linkRoot=New-Fixture 'file_symlink_project'
$linkOutside=New-Fixture 'file_symlink_outside'
$null=Add-File $linkRoot 'design.dsn'
$outsideLog=Add-File $linkOutside 'outside.log' 'outside regular file sentinel'
try {
    New-Item -ItemType SymbolicLink -Path (Join-Path $linkRoot 'custom.log') -Target $outsideLog -ErrorAction Stop | Out-Null
    Invoke-EDACleanup $linkRoot @()
    Check 'File symlink remains untouched' ([bool](Get-Item -LiteralPath (Join-Path $linkRoot 'custom.log') -Force -ErrorAction SilentlyContinue))
    Check 'File symlink target remains unchanged' ([IO.File]::ReadAllText($outsideLog) -eq 'outside regular file sentinel')
} catch { $script:Skips.Add('File symlink fixture unavailable: '+$_.Exception.Message) }

$failures=@($script:Results | Where-Object { -not $_.pass })
$report=[pscustomobject]@{fixture_root=$runRoot;production_payload_sha256=(Get-FileHash -LiteralPath $payload -Algorithm SHA256).Hash;checks=$script:Results.Count;failures=$failures.Count;skips=$script:Skips.ToArray();results=$script:Results.ToArray()}
$reportPath=Join-Path $runRoot 'results.json'
[IO.File]::WriteAllText($reportPath,($report | ConvertTo-Json -Depth 8),(New-Object Text.UTF8Encoding($false)))
Write-Host "RESULT checks=$($script:Results.Count) failures=$($failures.Count) report=$reportPath"
if($failures.Count){exit 1}
exit 0
