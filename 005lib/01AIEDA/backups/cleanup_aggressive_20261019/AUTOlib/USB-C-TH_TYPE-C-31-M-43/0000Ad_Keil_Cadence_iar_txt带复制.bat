@echo off
chcp 65001 >nul
setlocal DisableDelayedExpansion
rem UTF-8 without BOM / CRLF. Clean the script directory only.
rem Options: /preview /history /build /help. Never clean 01AIEDA or 01env.
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
$script:CleanupTemplates=@('BOM.txt','reports.txt','drill4noet.txt')
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
    return $Name -match '^(?i:01AIEDA|01env|\.git|\.svn|\.hg|node_modules|\.venv|venv|backups?|archives?|rar|zip|history|originals?|releases?)$'
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
    if ($Altium -and $Name -match '^(?i:.*\.(pcbdoc_viewstate|pcbdocpreview|schdocpreview|pcbpreview|schpreview|prjpcbstructure)|.*\.\$\$\$preview)$') {
        return 'Altium generated preview/state'
    }
    if ($Cadence -and $Name -match '^(?i:allegro\.log|padstack\.log|padstack_editor\.log|netlist\.log|netrev\.lst|dev_check\.log|genfeed\.log|swp\.log|extract\.log|dbdoctor\.log|batch_drc\.log)(,\d+)?$') {
        return 'Named Cadence diagnostic log'
    }
    if ($Embedded -and $Name -match '^(?i:JLinkLog\.txt|JLinkARM\.log)$') { return 'J-Link diagnostic log' }
    if ($History -and $Cadence -and $Name -match '^(?i:allegro|padstack_editor)\.jrl(,\d+)?$') {
        return 'Optional session replay history'
    }
    if ($Build -and $Embedded -and $Relative -match '(?i)(^|[\\/])(obj|objects|list|listings|browse)([\\/])' -and $Name -match '(?i)\.(obj|o|d|dep|crf|lnp|lst|pbi|pbd|browse|linf|pbw|plg)$') {
        return 'Optional rebuildable intermediate (recognized source project)'
    }
    return $null
}

function Assert-CurrentCandidate([object]$Candidate, [string]$Root) {
    $path = Assert-UnderRoot $Candidate.File.FullName $Root
    $now = Get-Item -LiteralPath $path -Force
    if ($now.PSIsContainer -or ($now.Attributes -band [IO.FileAttributes]::ReparsePoint)) { throw "Not a regular file: $path" }
    if ($now.Length -ne $Candidate.File.Length -or $now.LastWriteTimeUtc -ne $Candidate.File.LastWriteTimeUtc) {
        throw "File changed while scanning; kept: $path"
    }
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
    $preview=$false; $history=$false; $build=$false
    foreach ($option in $Options) {
        switch ($option.ToLowerInvariant()) {
            '/preview' { $preview=$true }
            '/history' { $history=$true }
            '/build' { $build=$true }
            '/help' {
                Write-Host 'Usage: this.bat [/preview] [/history] [/build]'
                Write-Host 'Default: named diagnostic logs and generated previews. /preview never changes files.'
                Write-Host '/history adds replay journals. /build adds intermediates inside recognized source-project build directories.'
                Write-Host 'Source files, configuration, OPJ, netlists, models, backups and final firmware are kept.'
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
