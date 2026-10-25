@echo off
chcp 65001 >nul
setlocal DisableDelayedExpansion
rem UTF-8 without BOM / CRLF. Clean the script directory only.
rem Options: /preview /history /build /help. Never clean 01AIEDA or 01env.
rem Default includes journals/build output and proven redundant backups/project wrappers.
set "EDA_CLEAN_SELF=%~f0"
set "EDA_CLEAN_ROOT=%~dp0"
set "EDA_CLEAN_ARG_1=%~1"
set "EDA_CLEAN_ARG_2=%~2"
set "EDA_CLEAN_ARG_3=%~3"
set "EDA_CLEAN_ARG_4=%~4"
set "EDA_CLEAN_ARG_5=%~5"
set "EDA_CLEAN_ARG_6=%~6"
set "EDA_CLEAN_ARG_7=%~7"
set "EDA_CLEAN_ARG_8=%~8"
set "EDA_CLEAN_ARG_9=%~9"
powershell.exe -NoLogo -NoProfile -ExecutionPolicy Bypass -Command "$text=[IO.File]::ReadAllText($env:EDA_CLEAN_SELF,[Text.Encoding]::UTF8);$marker='#__EDA_CLEAN_POWERSHELL__';& ([ScriptBlock]::Create($text.Substring($text.LastIndexOf($marker)+$marker.Length)))"
exit /b %errorlevel%
#__EDA_CLEAN_POWERSHELL__
$script:CleanupTemplates=@()
$script:CleanupHadExtraction=$true
# Embedded in the portable UTF-8 BAT entry points. Windows PowerShell 5.1.
$ErrorActionPreference = 'Stop'
[Console]::OutputEncoding = New-Object System.Text.UTF8Encoding($false)
$OutputEncoding = [Console]::OutputEncoding

function Assert-UnderRoot([string]$Path, [string]$Root) {
    $full = [IO.Path]::GetFullPath($Path)
    $prefix = $Root.TrimEnd('\') + '\'
    if (-not $full.StartsWith($prefix, [StringComparison]::OrdinalIgnoreCase)) {
        throw "Path outside selected directory: $full"
    }
    return $full
}

function Assert-CleanupRoot([string]$Root) {
    if (-not [IO.Directory]::Exists($Root)) { throw "Directory missing: $Root" }
    if ($Root.TrimEnd('\') -eq [IO.Path]::GetPathRoot($Root).TrimEnd('\')) {
        throw 'Refusing to clean a drive root.'
    }
    foreach ($segment in ($Root -split '[\\/]')) {
        if (Test-ProtectedDirectory $segment) { throw "Protected directory/ancestor: $segment" }
    }
    foreach ($systemDir in @($env:WINDIR, $env:ProgramFiles, ${env:ProgramFiles(x86)}, $env:USERPROFILE)) {
        if ($systemDir -and $Root.TrimEnd('\') -eq $systemDir.TrimEnd('\')) {
            throw "Refusing to clean a system/profile directory: $Root"
        }
    }
    $item = Get-Item -LiteralPath $Root -Force
    while ($item) {
        if ($item.Attributes -band [IO.FileAttributes]::ReparsePoint) { throw 'Reparse-point root/ancestor refused.' }
        $item=$item.Parent
    }
}

function Test-ProtectedDirectory([string]$Name) {
    return $Name -match '^(?i:01AIEDA|01env|\.git|\.svn|\.hg|node_modules|\.venv|venv|backups?|archives?|rar|zip|history|originals?|releases?|libs?|librar(?:y|ies))$'
}

function Get-BlockingProcesses {
    return @(Get-Process -ErrorAction SilentlyContinue | Where-Object {
        $_.ProcessName -match '^(?i:capture|allegro|pcb_editor|padstack_editor|dxp|x2|altiumdesigner|uv4|iaridepm|iaride|ewb|devenv_iar)$'
    } | Select-Object -ExpandProperty ProcessName -Unique)
}

function Get-CleanupCandidates([string]$Root, [bool]$History, [bool]$Build) {
    $stack = New-Object 'System.Collections.Generic.Stack[object]'
    $stack.Push([pscustomobject]@{ Path=$Root; Cadence=$false; Embedded=$false; Altium=$false })
    while ($stack.Count) {
        $entry = $stack.Pop()
        $items = @(Get-ChildItem -LiteralPath $entry.Path -Force -ErrorAction Stop)
        $files = @($items | Where-Object { -not $_.PSIsContainer })
        $cadence = $entry.Cadence -or @($files | Where-Object { $_.Extension -match '^(?i:\.dsn|\.brd|\.dra|\.pad|\.psm|\.olb|\.opj)$' }).Count -gt 0
        $embedded = $entry.Embedded -or @($files | Where-Object { $_.Extension -match '^(?i:\.uvprojx?|\.uv2|\.ewp|\.eww)$' }).Count -gt 0
        $altium = $entry.Altium -or @($files | Where-Object { $_.Extension -match '^(?i:\.pcbdoc|\.schdoc|\.pcblib|\.schlib|\.prjpcb)$' }).Count -gt 0
        foreach ($file in $files) {
            if ($file.Attributes -band [IO.FileAttributes]::ReparsePoint) { continue }
            $relative = (Assert-UnderRoot $file.FullName $Root).Substring($Root.TrimEnd('\').Length + 1)
            $reason = Get-CleanupReason $file.Name $relative $cadence $embedded $History $Build $altium
            if (-not $reason -and $History) { $reason = Get-RedundantBackupReason $file }
            if (-not $reason -and $cadence -and $file.Extension -ieq '.opj' -and (Test-PureSchematicProject $file $Root)) {
                $reason = 'Recreatable pure schematic project wrapper (DSN exists)'
            }
            if ($reason) { [pscustomobject]@{ File=$file; Relative=$relative; Reason=$reason } }
        }
        foreach ($dir in @($items | Where-Object { $_.PSIsContainer })) {
            if (($dir.Attributes -band [IO.FileAttributes]::ReparsePoint) -or (Test-ProtectedDirectory $dir.Name)) { continue }
            $null = Assert-UnderRoot $dir.FullName $Root
            $stack.Push([pscustomobject]@{ Path=$dir.FullName; Cadence=$cadence; Embedded=$embedded; Altium=$altium })
        }
    }
}

function Get-CleanupReason([string]$Name, [string]$Relative, [bool]$Cadence, [bool]$Embedded, [bool]$History, [bool]$Build, [bool]$Altium=$false) {
    if ($Name -match '(?i)\.tmp(,\d+)?$') { return 'Temporary file' }
    if ($Altium -and $Name -match '^(?i:.*\.(pcbdoc_viewstate|pcbdocpreview|schdocpreview|pcbpreview|schpreview|prjpcbstructure)|.*\.\$\$\$preview)$') {
        return 'Altium generated preview/state'
    }
    if (($Cadence -or $Embedded -or $Altium) -and $Name -match '(?i)\.(log|lst|rpt|dmp)(,\d+)?$') {
        return 'Generated diagnostic/report in recognized EDA project'
    }
    if ($Cadence -and $Name -match '(?i)\.(iex|drc|tag)(,\d+)?$') {
        return 'Cadence generated check/exchange scratch file'
    }
    if ($Embedded -and $Name -match '^(?i:JLinkLog\.txt|JLinkARM\.log)$') { return 'J-Link diagnostic log' }
    if ($History -and $Cadence -and $Name -match '(?i)\.jrl(,\d+)?$') {
        return 'Cadence session replay history'
    }
    if ($Build -and $Embedded -and $Relative -match '(?i)(^|[\\/])(obj(?:_[^\\/]+)?|objects|list|listings|browse|debug|build)([\\/])' -and $Name -match '(?i)\.(obj|o|d|dep|crf|lnp|lst|pbi|pbd|browse|linf|pbw|plg|__i|axf|omf|map|htm)$') {
        return 'Rebuildable output in recognized source-project build directory'
    }
    return $null
}

function Get-RedundantBackupReason([IO.FileInfo]$File) {
    $names=@(); $name=$File.Name
    if ($name -match '^(.*\.(?:dsn|brd|dra|pad|psm|olb|opj|dat|txt|cfg|cnv|iml|dml|ctl|dcf|xml|csv|bom|log|jrl)),\d+$') {
        $names=@($Matches[1])
    } elseif ($name -match '^(.*\.(?:pcbdoc|pcblib|prjpcb))\.zip$') {
        $names=@($Matches[1])
    } elseif ($File.Extension -match '^(?i:\.dbk|\.obk|\.sav|\.bak)$') {
        $stem=[IO.Path]::GetFileNameWithoutExtension($name)
        $extensions=switch ($File.Extension.ToLowerInvariant()) {
            '.dbk' { @('.dsn') }
            '.obk' { @('.olb') }
            '.sav' { @('.brd','.dra','.pad') }
            '.bak' { @('.dsn','.olb','.brd','.dra','.pad','.opj','.cfg','.c','.h','.cpp','.sct','.xcl','.icf') }
        }
        # foo.brd.bak / foo.brd.sav first refer to the complete original name.
        if ([IO.Path]::GetExtension($stem)) { $names+= $stem }
        $names+=@($extensions | ForEach-Object { $stem+$_ })
        if ($stem -match '^(.*)_\d+$') { $plain=$Matches[1]; $names+=@($extensions | ForEach-Object { $plain+$_ }) }
    }
    $primaries=@()
    foreach ($candidateName in @($names | Select-Object -Unique)) {
        $primary=Get-Item -LiteralPath (Join-Path $File.DirectoryName $candidateName) -Force -ErrorAction SilentlyContinue
        if ($primary -and -not $primary.PSIsContainer -and -not ($primary.Attributes -band [IO.FileAttributes]::ReparsePoint)) { $primaries+= $primary }
    }
    if ($primaries.Count -eq 1 -and $primaries[0].Length -gt 0 -and $primaries[0].LastWriteTimeUtc -ge $File.LastWriteTimeUtc) {
        return 'Old backup/version with nonempty main file at least as recent'
    }
    return $null
}

function Test-PureSchematicProject([IO.FileInfo]$File, [string]$Root) {
    if ($File.Length -eq 0 -or $File.Length -gt 2MB) { return $false }
    $text=[IO.File]::ReadAllText($File.FullName)
    if ($text -notmatch '^\s*\(ExpressProject\s+"' -or $text -notmatch '\(ProjectType\s+"(?:PCB|Schematic)"\s*\)') { return $false }
    if ($text -match '(?i)PSpice|Simulat|CIS|DataSource|ToolSettings|Constraint|\.dbc') { return $false }
    # Validate the entire expression, including balanced parentheses and quoted strings.
    $tokenPattern='"(?:[^"\\]|\\.)*"|[()]|[^\s()"]+'
    if ([regex]::Replace($text,$tokenPattern,'') -match '\S') { return $false }
    $tokens=[regex]::Matches($text,$tokenPattern)
    $depth=0; $expectNode=$false; $roots=0
    $allowed='^(?i:ExpressProject|ProjectVersion|ProjectType|Folder|File|Type|NoModify|GlobalState|FileView|Doc|Frame|Path|Zoom|Window|WindowState|WindowPosition|Left|Right|Top|Bottom|Opened|Selected|Active|Page|PageView|Scroll|Scale|BuildFileAddedOrDeleted|CompileFileAddedOrDeleted|PartMRUSelector|HierarchyView|Select|Placement|Tab|Occurrence|Schematic)$'
    foreach ($token in $tokens) {
        $value=$token.Value
        if ($value -eq '(') { if ($expectNode) { return $false }; if ($depth -eq 0) { $roots++; if ($roots -gt 1) { return $false } }; $depth++; $expectNode=$true; continue }
        if ($value -eq ')') { if ($expectNode -or $depth -le 0) { return $false }; $depth--; continue }
        if ($depth -le 0) { return $false }
        if ($expectNode) { if ($value -notmatch $allowed) { return $false }; $expectNode=$false }
        elseif (-not ($value.StartsWith('"') -or $value -match '^-?\d+(?:\.\d+)?$')) { return $false }
    }
    if ($depth -ne 0 -or $expectNode) { return $false }
    $refs=[regex]::Matches($text,'(?i)\(File\s+"([^"\r\n]+)"')
    $designs=0
    foreach ($ref in $refs) {
        $relative=$ref.Groups[1].Value
        if ([IO.Path]::GetExtension($relative) -notmatch '^(?i:\.dsn|\.olb)$') { return $false }
        try {
            $path=Assert-UnderRoot (Join-Path $File.DirectoryName $relative) $Root
            $item=Get-Item -LiteralPath $path -Force -ErrorAction Stop
            if ($item.PSIsContainer -or ($item.Attributes -band [IO.FileAttributes]::ReparsePoint) -or $item.Length -eq 0) { return $false }
            $parent=$item.Directory
            while ($parent -and $parent.FullName.TrimEnd('\') -ne $Root.TrimEnd('\')) {
                if ($parent.Attributes -band [IO.FileAttributes]::ReparsePoint) { return $false }; $parent=$parent.Parent
            }
        } catch { return $false }
        if ($item.Extension -ieq '.dsn') { $designs++ }
    }
    return $designs -eq 1
}

function Assert-CurrentCandidate([object]$Candidate, [string]$Root) {
    $path = Assert-UnderRoot $Candidate.File.FullName $Root
    $now = Get-Item -LiteralPath $path -Force
    if ($now.PSIsContainer -or ($now.Attributes -band [IO.FileAttributes]::ReparsePoint)) { throw "Not a regular file: $path" }
    if ($now.Length -ne $Candidate.File.Length -or $now.LastWriteTimeUtc -ne $Candidate.File.LastWriteTimeUtc) {
        throw "File changed while scanning; kept: $path"
    }
    if ($Candidate.Reason -like 'Old backup/*' -and -not (Get-RedundantBackupReason $now)) { throw "Main file no longer qualifies; backup kept: $path" }
    if ($Candidate.Reason -like 'Recreatable pure schematic*' -and -not (Test-PureSchematicProject $now $Root)) { throw "Schematic project references changed; kept: $path" }
    $parent = $now.Directory
    while ($parent -and $parent.FullName.TrimEnd('\') -ne $Root.TrimEnd('\')) {
        if (($parent.Attributes -band [IO.FileAttributes]::ReparsePoint) -or (Test-ProtectedDirectory $parent.Name)) {
            throw "Protected/reparse parent: $path"
        }
        $parent = $parent.Parent
    }
    return $path
}

function Copy-MissingTemplates([string]$Root, [string[]]$Names, [bool]$Preview) {
    if (-not $Names.Count) { return }
    $source = $null
    $parent = Get-Item -LiteralPath $Root
    while ($parent) {
        $candidate = Join-Path $parent.FullName '01env'
        if (Test-Path -LiteralPath (Join-Path $candidate 'BOM.txt') -PathType Leaf) { $source=$candidate; break }
        $parent=$parent.Parent
    }
    if (-not $source -and (Test-Path -LiteralPath 'D:\001DIY\005lib\01env\BOM.txt' -PathType Leaf)) { $source='D:\001DIY\005lib\01env' }
    if (-not $source) { Write-Host 'Template source not found; copying skipped.'; return }
    foreach ($name in $Names) {
        if ($name -notin @('BOM.txt','reports.txt','drill4noet.txt')) { throw 'Unrecognized template name.' }
        $dest = Assert-UnderRoot (Join-Path $Root $name) $Root
        $src = Join-Path $source $name
        $existing=Get-Item -LiteralPath $dest -Force -ErrorAction SilentlyContinue
        if ($existing) { Write-Host "KEEP existing template/directory/link: $name"; continue }
        $sourceItem=Get-Item -LiteralPath $src -Force -ErrorAction SilentlyContinue
        if (-not $sourceItem -or $sourceItem.PSIsContainer -or ($sourceItem.Attributes -band [IO.FileAttributes]::ReparsePoint)) { Write-Host "Missing/nonregular source template: $name"; continue }
        $sourceParent=$sourceItem.Directory
        while ($sourceParent) {
            if ($sourceParent.Attributes -band [IO.FileAttributes]::ReparsePoint) { throw "Reparse-point template source refused: $src" }
            $sourceParent=$sourceParent.Parent
        }
        if ($Preview) { Write-Host "WOULD COPY missing template: $name" }
        else { Copy-Item -LiteralPath $src -Destination $dest -ErrorAction Stop; Write-Host "COPIED missing template: $name" }
    }
}

function Invoke-EDACleanup([string]$Root, [string[]]$Options, [string[]]$Templates=@(), [bool]$HadExtraction=$false) {
    $preview=$false; $history=$true; $build=$true
    foreach ($option in $Options) {
        switch ($option.ToLowerInvariant()) {
            '/preview' { $preview=$true }
            '/history' { $history=$true }
            '/build' { $build=$true }
            '/help' {
                Write-Host 'Usage: this.bat [/preview] [/history] [/build]'
                Write-Host 'Default: logs, reports, journals, temporary/preview files, and rebuildable output in recognized build directories.'
                Write-Host 'Old backups with a newer nonempty main file and proven pure-schematic OPJ wrappers are also cleaned.'
                Write-Host '/preview never changes files. /history and /build remain accepted; both are now enabled by default.'
                Write-Host 'Design/library/source/configuration files, current TXT/XML/CSV/DAT, and orphan/newer recovery backups are kept.'
                return
            }
            default { throw "Unknown option: $option (use /help)." }
        }
    }
    $Root=[IO.Path]::GetFullPath($Root).TrimEnd('\')
    Assert-CleanupRoot $Root
    Write-Host "Target (script directory): $Root"
    $busy=@(Get-BlockingProcesses)
    if ($busy.Count -and -not $preview) { throw "Close the design/build tools before cleanup: $($busy -join ', ')" }
    if ($busy.Count) { Write-Host "Preview only; open tools: $($busy -join ', ')" }
    $candidates=@(Get-CleanupCandidates $Root $history $build)
    $failures=0; $bytes=0L; $removed=0
    foreach ($candidate in $candidates) {
        if ($preview) { Write-Host "WOULD REMOVE [$($candidate.Reason)] $($candidate.Relative)"; continue }
        try {
            $path=Assert-CurrentCandidate $candidate $Root
            # Enumerate and remove within PowerShell, using literal, individually checked files.
            Remove-Item -LiteralPath $path -ErrorAction Stop
            $bytes+=$candidate.File.Length; $removed++
            Write-Host "REMOVED [$($candidate.Reason)] $($candidate.Relative)"
        } catch { $failures++; Write-Host "KEPT (error): $($candidate.Relative) -- $($_.Exception.Message)" }
    }
    Copy-MissingTemplates $Root $Templates $preview
    if ($HadExtraction) { Write-Host 'Archive extraction has been separated from cleanup; no archive expanded or environment overwritten.' }
    Write-Host "Candidates=$($candidates.Count); removed=$removed; bytes=$bytes; failures=$failures; preview=$preview"
    if ($failures) { throw "$failures file(s) could not be cleaned; they were kept." }
}

# Tests may import the functions without running a cleanup or weakening its guards.
if ($env:EDA_CLEAN_LOAD_ONLY -eq '1') { return }
try {
    if ([Environment]::GetEnvironmentVariable('EDA_CLEAN_ARG_9')) { throw 'Too many options (maximum eight).' }
    $options=@()
    foreach ($i in 1..9) {
        $option=[Environment]::GetEnvironmentVariable("EDA_CLEAN_ARG_$i")
        if ($option) { $options+=$option }
    }
    Invoke-EDACleanup $env:EDA_CLEAN_ROOT $options $script:CleanupTemplates $script:CleanupHadExtraction
    exit 0
} catch { [Console]::Error.WriteLine($_.Exception.Message); exit 1 }
