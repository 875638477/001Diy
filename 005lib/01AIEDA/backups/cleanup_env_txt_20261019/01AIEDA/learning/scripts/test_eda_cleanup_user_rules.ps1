# Final user rule: preserve all XML/CSV/DAT; preserve TXT in 01AIEDA/env/01env.
# Restore each entry's old deletion masks for all remaining file kinds.
# All fixture creation and any cleanup are restricted to a unique run directory
# below 01AIEDA; this test never cleans the workspace or a real user project.
param([switch]$PrepareOnly)
$ErrorActionPreference = 'Stop'
$workspace = [IO.Path]::GetFullPath((Join-Path $PSScriptRoot '..\..\..'))
$testsBase = Join-Path $workspace '01AIEDA\learning\staging\cleanup_review_20261019\user_rules\tests'
$runRoot = Join-Path $testsBase ('run_' + [DateTime]::UtcNow.ToString('yyyyMMdd_HHmmss') + '_' + [guid]::NewGuid().ToString('N').Substring(0,8))
$script:AllowedFixtureRoots = New-Object 'System.Collections.Generic.List[string]'
$script:Results = New-Object 'System.Collections.Generic.List[object]'
$script:Skips = New-Object 'System.Collections.Generic.List[string]'
$payload = Join-Path $PSScriptRoot 'eda_cleanup_payload.ps1'
$oldLoad = $env:EDA_CLEAN_LOAD_ONLY
$env:EDA_CLEAN_LOAD_ONLY = '1'
try { . ([ScriptBlock]::Create([IO.File]::ReadAllText($payload,[Text.Encoding]::UTF8))) }
finally { $env:EDA_CLEAN_LOAD_ONLY = $oldLoad }
$script:ProductionAIEDATextFile=(Get-Command Test-AIEDATextFile).ScriptBlock

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
function Install-FixtureOnlyOverrides {
    function global:Assert-CleanupRoot([string]$Root) {
        $full=[IO.Path]::GetFullPath($Root).TrimEnd('\')
        if (-not $script:AllowedFixtureRoots.Contains($full)) { throw 'Test override rejects roots not created by this test.' }
        if (-not $full.StartsWith($runRoot+'\',[StringComparison]::OrdinalIgnoreCase)) { throw 'Test root escaped fixture area.' }
        $item=Get-Item -LiteralPath $full -Force
        if ($item.Attributes -band [IO.FileAttributes]::ReparsePoint) { throw 'Fixture root cannot be a reparse point.' }
    }
    function global:Get-BlockingProcesses { return @() }
    function global:Test-AIEDATextFile([IO.FileInfo]$File) {
        # Fixtures must remain in 01AIEDA. Remove only the outer test-container
        # prefix for this path-only predicate; nested 01AIEDA remains meaningful.
        if (-not $File.FullName.StartsWith($runRoot+'\',[StringComparison]::OrdinalIgnoreCase)) {
            throw 'Test AI text predicate refuses files outside this test run.'
        }
        $relative=$File.FullName.Substring($runRoot.Length+1)
        $virtual=Join-Path ([IO.Path]::GetPathRoot($runRoot)) ('CodexCleanupUnit\'+$relative)
        $virtualFile=New-Object IO.FileInfo($virtual)
        return & $script:ProductionAIEDATextFile $virtualFile
    }
}
function Save-TestReport {
    $failures=@($script:Results | Where-Object { -not $_.pass })
    $report=[pscustomobject]@{
        policy='final_preserve_XML_CSV_DAT_and_AIEDA_ENV_TXT_original_other_masks'
        fixture_root=$runRoot
        production_payload_sha256=(Get-FileHash -LiteralPath $payload -Algorithm SHA256).Hash
        checks=$script:Results.Count
        failures=$failures.Count
        skips=$script:Skips.ToArray()
        results=$script:Results.ToArray()
    }
    $reportPath=Join-Path $runRoot 'results.json'
    [IO.File]::WriteAllText($reportPath,($report | ConvertTo-Json -Depth 8),(New-Object Text.UTF8Encoding($false)))
    Write-Host "RESULT checks=$($script:Results.Count) failures=$($failures.Count) report=$reportPath"
    return $failures.Count
}

if ($PrepareOnly) { Write-Host 'Isolated test framework ready; no cleanup executed.'; exit 0 }
[IO.Directory]::CreateDirectory($runRoot) | Out-Null

# Exercise production boundaries before installing a fixture-only root override.
$guardRoot=New-Fixture 'guard_protected_ancestor'
Check 'Production allows a cleanup root below 01AIEDA' (-not (Throws { Assert-CleanupRoot $guardRoot }))
$aiText=Add-File $guardRoot 'notes.txt' 'learning record'
$aiHistory=Add-File $guardRoot 'notes.txt,3' 'older learning record'
$aiLog=Add-File $guardRoot 'allegro.log' 'generated log'
Check 'Production recognizes TXT from the real full 01AIEDA ancestor path' (Test-AIEDATextFile (Get-Item -LiteralPath $aiText))
Check 'Production recognizes numbered TXT from the real 01AIEDA ancestor path' (Test-AIEDATextFile (Get-Item -LiteralPath $aiHistory))
Check 'Production does not protect non-TXT merely because it is in 01AIEDA' (-not (Test-AIEDATextFile (Get-Item -LiteralPath $aiLog)))
$actualCandidates=@(Get-CleanupCandidates $guardRoot $true $true)
Check 'Production scans 01AIEDA logs while retaining its TXT' (($actualCandidates.Count -eq 1) -and ($actualCandidates[0].File.Name -eq 'allegro.log'))
Check '01AIEDA text predicate requires an exact directory segment' (-not (& $script:ProductionAIEDATextFile (New-Object IO.FileInfo('D:\CodexCleanupUnit\01AIEDA_more\notes.txt'))))
Check '01AIEDA text predicate is case insensitive across full ancestors' (& $script:ProductionAIEDATextFile (New-Object IO.FileInfo('D:\CodexCleanupUnit\01aieda\nested\NOTES.TXT,28')))
Check 'Ordinary path TXT has no AIEDA protection' (-not (& $script:ProductionAIEDATextFile (New-Object IO.FileInfo('D:\CodexCleanupUnit\normal\notes.txt'))))
foreach($dir in @('env','ENV','env\child','ENV\child\deeper','01env','01ENV\child')) {
    foreach($name in @('notes.txt','NOTES.TXT,28')) {
        Check ('Full-path TXT predicate protects env ancestor '+$dir+'\'+$name) (& $script:ProductionAIEDATextFile (New-Object IO.FileInfo ('D:\CodexCleanupUnit\'+$dir+'\'+$name)))
    }
    foreach($name in @('allegro.log','settings.cfg')) {
        Check ('Env text predicate does not protect other suffixes '+$dir+'\'+$name) (-not (& $script:ProductionAIEDATextFile (New-Object IO.FileInfo ('D:\CodexCleanupUnit\'+$dir+'\'+$name))))
    }
}
foreach($dir in @('environment','not_env','env_more','someenv','01environment')) {
    Check ('Env text predicate requires an exact directory segment '+$dir) (-not (& $script:ProductionAIEDATextFile (New-Object IO.FileInfo ('D:\CodexCleanupUnit\'+$dir+'\notes.txt'))))
}
Check 'Production refuses a drive root' (Throws { Assert-CleanupRoot ([IO.Path]::GetPathRoot($workspace)) })
Check 'Boundary guard rejects a sibling sharing the root prefix' (Throws { Assert-UnderRoot ($workspace+'-sibling\scratch.txt') $workspace })
Check 'Boundary guard accepts a literal child path' ((Assert-UnderRoot (Join-Path $workspace "sub !& (x) ' q\scratch.txt") $workspace).StartsWith($workspace+'\'))
Install-FixtureOnlyOverrides
Check 'Fixture override refuses the real workspace' (Throws { Assert-CleanupRoot $workspace })

$inventoryPath=Join-Path $workspace '01AIEDA\learning\staging\cleanup_review_20261019\family_inventory.json'
$inventory=[IO.File]::ReadAllText($inventoryPath,[Text.Encoding]::UTF8) | ConvertFrom-Json
$legacyPatterns=@(@($inventory.scripts | ForEach-Object { $_.rules | ForEach-Object { $_.pattern } })+'*.txt' | Sort-Object -Unique)
$script:CleanupPatterns=$legacyPatterns
Check 'Original-family test policy includes active patterns plus TXT' (($legacyPatterns -contains '*.txt') -and ($legacyPatterns -contains '*.xml') -and ($legacyPatterns -contains '*.csv') -and ($legacyPatterns -contains '*.dat') -and ($legacyPatterns -contains '*.opj') -and ($legacyPatterns -contains '*.sct') -and ($legacyPatterns -contains '*.xcl'))

# No Cadence/embedded project marker is required: the user's old patterns apply
# throughout the selected script directory, except protected folders/netlists.
$plain=New-Fixture ('legacy patterns !& (x) '' q '+[char]0x6D4B+[char]0x8BD5)
$delete=@(); $dataKeep=@()
foreach($pattern in $legacyPatterns) {
    $name=$pattern.Replace('*','original').Replace('?','q')
    $null=Add-File $plain $name ('ordinary generated content for '+$pattern)
    if ($name -match '(?i)\.(xml|csv|dat)(,\d+)?$') { $dataKeep+=$name } else { $delete+=$name }
}
$delete=@($delete | Sort-Object -Unique)
$keep=@('design.dsn','board.brd','drawing.dra','shape.psm','pin.pad','library.olb','source.c','header.h','project.uvprojx','project.ewp','firmware.hex','firmware.bin','archive.zip','original.bat','notes.md','script.ps1','schematic.net','pspice.cir','unknown.extension')
$keep+=@($dataKeep | Sort-Object -Unique)
Add-Files $plain $keep
$before=Get-Snapshot $plain
Invoke-EDACleanup $plain @('/preview')
Check 'Preview preserves every file byte-for-byte' ($before -eq (Get-Snapshot $plain))
Invoke-EDACleanup $plain @()
Check-Files $plain $delete $false 'Original deletion pattern is active without project context'
Check-Files $plain $keep $true 'Unlisted source design library firmware or archive remains'

# The per-entry list must govern scope; a Keil-only entry must not acquire the
# Cadence/TXT/XML/DAT deletion list simply because the shared payload supports it.
$narrow=New-Fixture 'per_entry_keil_patterns'
$script:CleanupPatterns=@('*.obj','*.lst','JLinkLog.txt','*.sct','*.txt')
Add-Files $narrow @('root.obj','root.lst','JLinkLog.txt','memory.sct','anything.txt','anything.dat','anything.xml','anything.csv','design.opj','allegro.log','sub\nested.obj','sub\nested.txt')
Invoke-EDACleanup $narrow @()
Check-Files $narrow @('root.obj','root.lst','JLinkLog.txt','memory.sct','sub\nested.obj','anything.txt','sub\nested.txt') $false 'Entry-specific pattern recursively removes its listed file'
Check-Files $narrow @('anything.dat','anything.xml','anything.csv','design.opj','allegro.log') $true 'Entry-specific unlisted file remains'
$script:CleanupPatterns=$legacyPatterns

# Netlist recognition takes precedence over every matching cleanup pattern.
$net=New-Fixture 'schematic_netlist_exception'
$netKeep=@()
foreach($name in @('pstchip.dat','pstxnet.dat','pstxprt.dat','pstdmlmodels.dat')) {
    $null=Add-File $net $name ''
    $netKeep+=$name
}
$headers=@{
    'renamed_chip.txt'="FILE_TYPE = LIBRARY_PARTS;`r`nPART_NAME R1;"
    'renamed_net.dat'="FILE_TYPE = EXPANDEDNETLIST;`r`nNET_NAME GND;"
    'renamed_parts.csv'="FILE_TYPE = EXPANDEDPARTLIST;`r`nPART_NAME U1;"
    'lower_case_header.txt'="file_type = expandednetlist;`nNET_NAME GND;"
}
foreach($name in $headers.Keys) { $null=Add-File $net $name $headers[$name]; $netKeep+=$name }
$edif='(edif demo (edifVersion 2 0 0) (library demo (cell c (view v (viewType NETLIST)))))'
foreach($name in @('schematic.edf','renamed_edif.txt','renamed_edif.dat')) { $null=Add-File $net $name $edif; $netKeep+=$name }
$edifPrefix='(edif boundary '
$boundaryEdif=$edifPrefix+(' '*(65536-$edifPrefix.Length-5))+'(viewType NETLIST))'
$null=Add-File $net 'boundary_edif.edf' $boundaryEdif
$netKeep+='boundary_edif.edf'
$null=Add-File $net 'large_edif.edf' ('(edif large '+(' '*(3*1024*1024))+'(viewType NETLIST))')
$netKeep+='large_edif.edf'
$pads="*PADS-PCB*`r`n*PART*`r`nR1 R0603`r`n*NET*`r`n*SIGNAL* GND`r`nR1.1`r`n*END*"
foreach($name in @('pads_export.txt','pads_export.dat')) { $null=Add-File $net $name $pads; $netKeep+=$name }
$telesis='$PACKAGES'+"`r`n"+'SOIC8!U1'+"`r`n"+'$NETS'+"`r`n"+'CLK;U1.1'+"`r`n"+'$END'
foreach($name in @('telesis_export.txt','telesis_export.dat')) { $null=Add-File $net $name $telesis; $netKeep+=$name }
$xml='<export version="D"><components><comp ref="R1"/></components><nets><net code="1"/></nets></export>'
$xmlNetlist='<netlist><components/><nets/></netlist>'
foreach($name in @('kicad_export.xml','renamed_xml.txt','renamed_xml.dat')) { $null=Add-File $net $name $xml; $netKeep+=$name }
$null=Add-File $net 'structured_netlist.xml' $xmlNetlist
$netKeep+='structured_netlist.xml'
$netDelete=@('netlist_is_only_a_name.txt','netlist.dat','pstchip.dat,1','pstxnet.dat,2','pstxprt.dat,3','pstdmlmodels.dat,1','ordinary.edf','ordinary.xml','malformed.xml','only_components.xml','only_nets.xml','wrong_root.xml','only_edif.txt','symbol_view.edf','partial_pads.txt','partial_telesis.txt','ordinary.cfg','ordinary.dml','large_ordinary.dat')
Add-Files $net $netDelete
$null=Add-File $net 'malformed.xml' '<export><components/><nets></export>'
$null=Add-File $net 'only_components.xml' '<export><components/></export>'
$null=Add-File $net 'only_nets.xml' '<netlist><nets/></netlist>'
$null=Add-File $net 'wrong_root.xml' '<library><components/><nets/></library>'
$null=Add-File $net 'only_edif.txt' '(edif a (edifVersion 2 0 0))'
$null=Add-File $net 'symbol_view.edf' '(edif a (view symbol (viewType SCHEMATIC)))'
$null=Add-File $net 'partial_pads.txt' "*PADS-PCB*`n*PART*`nR1 R0603"
$null=Add-File $net 'partial_telesis.txt' ('$PACKAGES'+"`n"+'SOIC8!U1')
$null=Add-File $net 'large_ordinary.dat' ('ordinary data '+('x'*(3*1024*1024)))
foreach($name in $netKeep) { Check ('Structured or exact-name netlist is recognized '+$name) (Test-SchematicNetlist (Get-Item -LiteralPath (Join-Path $net $name))) }
foreach($name in $netDelete) { Check ('Ordinary content or numbered copy is not a netlist '+$name) (-not (Test-SchematicNetlist (Get-Item -LiteralPath (Join-Path $net $name)))) }
$before=Get-Snapshot $net
Invoke-EDACleanup $net @('/preview')
Check 'Netlist preview preserves all file bytes' ($before -eq (Get-Snapshot $net))
Invoke-EDACleanup $net @()
Check-Files $net $netKeep $true 'Schematic netlist exception preserves file'
$netDataKeep=@($netDelete | Where-Object { $_ -match '(?i)\.(xml|csv|dat)(,\d+)?$' })
$netOrdinaryDelete=@($netDelete | Where-Object { $_ -notmatch '(?i)\.(xml|csv|dat)(,\d+)?$' })
Check-Files $net $netDataKeep $true 'XML CSV DAT and numbered copies remain even when not netlists'
Check-Files $net $netOrdinaryDelete $false 'Original-mask non-data ordinary content is deleted' 

# The latest user preference intentionally removes the previous main-file-age
# and pure-schematic-wrapper conditions for files in each original list.
$legacy=New-Fixture 'unconditional_original_backup_opj_config_rules'
$unconditional=@('orphan.bak','orphan.dbk','orphan.obk','orphan.sav','empty.dbk','newer.dbk','design.opj','simulation.opj','settings.cfg','stackup.dcf','model.dml','memory.iml','linker.sct','linker.xcl','mapping.cnv','plot.ctl','feedback.baf','job.OutJob','project.PrjGrp','ordinary.BOM','notes.txt','data.dat','source.xml','parts.csv','data.dat,1','notes.txt,1','settings.cfg,1','mapping.cnv,1','model.iml,1','board.PcbDoc.Zip')
Add-Files $legacy $unconditional
$null=Add-File $legacy 'empty.dsn' ''
$null=Add-File $legacy 'newer.dsn' 'old design'
$null=Add-File $legacy 'simulation.opj' '(ExpressProject "sim" (ProjectType "PSpice"))'
Set-Time $legacy 'newer.dsn' 1
Set-Time $legacy 'newer.dbk' 3
Invoke-EDACleanup $legacy @()
$unconditionalDataKeep=@($unconditional | Where-Object { $_ -match '(?i)\.(xml|csv|dat)(,\d+)?$' })
$unconditionalDelete=@($unconditional | Where-Object { $_ -notmatch '(?i)\.(xml|csv|dat)(,\d+)?$' })
Check-Files $legacy $unconditionalDelete $false 'Original other pattern deletes without main-file or OPJ specialization conditions'
Check-Files $legacy $unconditionalDataKeep $true 'XML CSV DAT override unconditional old deletion masks' 
Check-Files $legacy @('empty.dsn','newer.dsn') $true 'Primary DSN remains even when empty or older than removed backup'

$protectedFixture=New-Fixture 'protected_directories_and_recursive_scope'
$protected=@('01env','.git','.svn','.hg','node_modules','.venv','venv','backup','backups','archive','archives','rar','zip','history','original','originals')
foreach($dir in $protected) { Add-Files $protectedFixture @(($dir+'\notes.txt'),($dir+'\data.dat'),($dir+'\settings.xml'),($dir+'\session.log')) }
Add-Files $protectedFixture @('root.txt','child\nested.txt','child\nested.dat','child\nested.xml','child\design.dsn')
Invoke-EDACleanup $protectedFixture @()
foreach($dir in $protected) { Check-Files $protectedFixture @(($dir+'\notes.txt'),($dir+'\data.dat'),($dir+'\settings.xml'),($dir+'\session.log')) $true ('Protected directory untouched '+$dir) }
Check-Files $protectedFixture @('root.txt','child\nested.txt') $false 'Unprotected matching TXT is deleted recursively'
Check-Files $protectedFixture @('child\nested.dat','child\nested.xml') $true 'Unprotected XML DAT are globally preserved'
Check 'Unprotected primary DSN remains' (Exists $protectedFixture 'child\design.dsn')

$directoryPolicy=New-Fixture 'AIEDA_env_text_only_and_no_blanket_library_release_protection'
$textOnlyDirs=@('01AIEDA','01AIEDA\nested','env','env\nested','ENV\DEEP\child')
$ordinaryDirs=@('environment','not_env','env_more','someenv','release','releases','lib','libs','library','libraries')
foreach($dir in @($textOnlyDirs+$ordinaryDirs)) {
    foreach($name in @('notes.txt','notes.txt,1','allegro.log','settings.cfg','data.dat','data.dat,19','export.xml','export.xml,22','parts.csv','parts.csv,7')) { $null=Add-File $directoryPolicy ($dir+'\'+$name) }
}
Invoke-EDACleanup $directoryPolicy @()
foreach($dir in @($textOnlyDirs+$ordinaryDirs)) {
    $protectText=$textOnlyDirs -contains $dir
    Check-Files $directoryPolicy @(($dir+'\notes.txt'),($dir+'\notes.txt,1')) $protectText ('AIEDA/env TXT-only protection '+$dir)
    Check-Files $directoryPolicy @(($dir+'\allegro.log'),($dir+'\settings.cfg')) $false ('Other matching junk is cleaned inside '+$dir)
    Check-Files $directoryPolicy @(($dir+'\data.dat'),($dir+'\data.dat,19'),($dir+'\export.xml'),($dir+'\export.xml,22'),($dir+'\parts.csv'),($dir+'\parts.csv,7')) $true ('Data preservation applies inside '+$dir)
}
$envRoot=New-Fixture 'script_placed_directly_in_env\env'
Add-Files $envRoot @('notes.txt','notes.txt,1','child\nested.txt','child\nested.txt,2','allegro.log','settings.cfg','child\session.log','child\layout.cfg')
$before=Get-Snapshot $envRoot
Invoke-EDACleanup $envRoot @('/preview')
Check 'Preview preserves all files when cleanup root itself is env' ($before -eq (Get-Snapshot $envRoot))
Invoke-EDACleanup $envRoot @()
Check-Files $envRoot @('notes.txt','notes.txt,1','child\nested.txt','child\nested.txt,2') $true 'TXT remains when env is cleanup root'
Check-Files $envRoot @('allegro.log','settings.cfg','child\session.log','child\layout.cfg') $false 'Other listed suffixes are cleaned when env is cleanup root'
$script:CleanupPatterns=@('*')
foreach($name in @('a.xml','a.XML,87','a.csv','a.CSV,0','a.dat','a.DAT,33')) { Check ('Global data exclusion beats every configured mask '+$name) (-not (Get-CleanupReason $name $name)) }
$script:CleanupPatterns=$legacyPatterns
$forced=New-Fixture 'delete_time_data_and_AI_text_recheck'
foreach($name in @('data.dat','export.xml','parts.csv','notes.dat,9','01AIEDA\notes.txt','01AIEDA\notes.txt,4','env\notes.txt','env\notes.txt,4','ENV\child\notes.txt','ENV\child\notes.txt,8','01env\notes.txt','01env\notes.txt,9')) {
    $path=Add-File $forced $name 'protected content'
    $item=Get-Item -LiteralPath $path
    $candidate=[pscustomobject]@{File=$item;Relative=$name;Reason='Original cleanup pattern: *'}
    $null=$item.Length; $null=$item.LastWriteTimeUtc
    Check ('Deletion rechecks protected data or AI text '+$name) (Throws { Assert-CurrentCandidate $candidate $forced })
    Check ('Rejected protected candidate remains present '+$name) (Exists $forced $name)
}

$flags=New-Fixture 'legacy_flags_help_and_unknown'
Add-Files $flags @('first.txt','data.dat')
$before=Get-Snapshot $flags
Invoke-EDACleanup $flags @('/help')
Check 'Help does not modify files' ($before -eq (Get-Snapshot $flags))
Check 'Unknown switch fails before changes' (Throws { Invoke-EDACleanup $flags @('/anything') })
Check 'Unknown switch leaves all files unchanged' ($before -eq (Get-Snapshot $flags))
Invoke-EDACleanup $flags @('/history','/build')
Check-Files $flags @('first.txt') $false 'Legacy positive flags remain compatible with restored pattern cleanup'
Check-Files $flags @('data.dat') $true 'DAT preservation overrides compatibility flags'

$changed=New-Fixture 'changed_candidate'
$path=Add-File $changed 'ordinary.txt' 'old'
$candidate=@(Get-CleanupCandidates $changed $true $true)[0]
$null=$candidate.File.Length; $null=$candidate.File.LastWriteTimeUtc
[IO.File]::WriteAllText($path,'changed candidate content length')
Check 'Candidate modified after enumeration is rejected' (Throws { Assert-CurrentCandidate $candidate $changed })
Check 'Modified candidate remains present' (Exists $changed 'ordinary.txt')

$changedNetlist=New-Fixture 'netlist_changed_after_scan_same_metadata'
$path=Add-File $changedNetlist 'renamed.txt' ('x'*128)
$candidate=@(Get-CleanupCandidates $changedNetlist $true $true)[0]
$oldLength=$candidate.File.Length; $oldTime=$candidate.File.LastWriteTimeUtc
$newText='FILE_TYPE = EXPANDEDNETLIST;'+[Environment]::NewLine
$newText=$newText.PadRight(128,' ')
[IO.File]::WriteAllText($path,$newText,(New-Object Text.UTF8Encoding($false)))
[IO.File]::SetLastWriteTimeUtc($path,$oldTime)
Check 'Netlist replacement fixture preserves original size and timestamp' (((Get-Item -LiteralPath $path).Length -eq $oldLength) -and ((Get-Item -LiteralPath $path).LastWriteTimeUtc -eq $oldTime))
Check 'Deletion rechecks netlist protection after scan even with identical metadata' (Throws { Assert-CurrentCandidate $candidate $changedNetlist })
Check 'Newly identified netlist remains present' (Exists $changedNetlist 'renamed.txt')

$junctionRoot=New-Fixture 'junction_project'
$outside=New-Fixture 'junction_outside'
$null=Add-File $outside 'outside.txt' 'outside sentinel'
try {
    New-Item -ItemType Junction -Path (Join-Path $junctionRoot 'linked') -Target $outside -ErrorAction Stop | Out-Null
    Invoke-EDACleanup $junctionRoot @()
    Check 'Directory junction target is never traversed or deleted' (Exists $outside 'outside.txt')
} catch { $script:Skips.Add('Junction fixture unavailable: '+$_.Exception.Message) }
$linkRoot=New-Fixture 'file_symlink_project'
$linkOutside=New-Fixture 'file_symlink_outside'
$outsideTxt=Add-File $linkOutside 'outside.txt' 'outside regular file sentinel'
try {
    New-Item -ItemType SymbolicLink -Path (Join-Path $linkRoot 'linked.txt') -Target $outsideTxt -ErrorAction Stop | Out-Null
    Invoke-EDACleanup $linkRoot @()
    Check 'File symlink remains untouched' ([bool](Get-Item -LiteralPath (Join-Path $linkRoot 'linked.txt') -Force -ErrorAction SilentlyContinue))
    Check 'File symlink target remains unchanged' ([IO.File]::ReadAllText($outsideTxt) -eq 'outside regular file sentinel')
} catch { $script:Skips.Add('File symlink fixture unavailable: '+$_.Exception.Message) }

$failureCount=Save-TestReport
if ($failureCount) { exit 1 }
exit 0
