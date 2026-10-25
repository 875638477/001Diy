@echo off
chcp 65001 >nul
setlocal DisableDelayedExpansion
rem UTF-8 without BOM / CRLF. Clean the script directory only.
rem Options: /preview /history /build /help. Keep XML/CSV/DAT and TXT under 01AIEDA/env/01env.
rem Restore this entry's original deletion patterns and add TXT cleanup.
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
$script:CleanupHadExtraction=$false
$script:CleanupPatterns=@('*.pcbdoc_viewstate','*.PCBDOCPreview','*.PrjGrp','*.SchDocPreview','*.PcbLib.Zip','*.PrjPCBStructure','*.PcbDoc.Zip','*.OutJob','*.PrjPCB.Zip','*.bak','*.ddk','*.edk','*.lst','*.lnp','*.mpf','*.mpj','*.obj','*.omf','*.plg','*.rpt','*.tmp','*.__i','*.crf','*.o','*.d','*.axf','*.tra','*.dep','JLinkLog.txt','*.iex','*.sct','*.map','*.htm','*.log','*.edf','*.opj','*.dbk','*.cfg','*.cfg,1','*.jrl','*.dmp','*.baf','*.ctl','*.sav','*.txt','*.DRC','*.dml','*.tag','*.dat','*.dat,1','*.dat,2','*.dat,3','*.dcf','*.pro','*.OBK')
# Embedded in the portable UTF-8 BAT entry points. Windows PowerShell 5.1.
$ErrorActionPreference = 'Stop'
[Console]::OutputEncoding = New-Object System.Text.UTF8Encoding($false)
$OutputEncoding = [Console]::OutputEncoding

if (-not (Get-Variable -Name CleanupPatterns -Scope Script -ErrorAction SilentlyContinue)) {
    $script:CleanupPatterns=@('*.$$$preview','*.__i','*.axf','*.baf','*.bak','*.bom','*.browse','*.cfg','*.cfg,1','*.cnv','*.cnv,1','*.crf','*.csv','*.ctl','*.d','*.dat','*.dat,1','*.dat,2','*.dat,3','*.db','*.dbk','*.dcf','*.ddk','*.dep','*.dml','*.dml,','*.dml,1','*.dml,2','*.dmp','*.drc','*.edf','*.edk','*.htm','*.iex','*.iml','*.iml,1','*.jrl','*.jrl,1','*.jrl,2','*.jrl,3','*.linf','*.lnp','*.log','*.log,1','*.log,2','*.log,3','*.lst','*.map','*.mpf','*.mpj','*.o','*.obj','*.obk','*.omf','*.opj','*.outjob','*.pbd','*.pbi','*.pbw','*.pcbdoc.zip','*.pcbdoc_viewstate','*.pcbdocpreview','*.pcblib.zip','*.pcbpreview','*.plg','*.prjgrp','*.prjpcb.zip','*.prjpcbstructure','*.pro','*.rpt','*.sav','*.schdocpreview','*.schpreview','*.sct','*.tag','*.tmp','*.tra','*.txt','*.txt,1','*.xcl','*.xml','jlinklog.txt')
}

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
    return $Name -match '^(?i:01env|\.git|\.svn|\.hg|node_modules|\.venv|venv|backups?|archives?|rar|zip|history|originals?)$'
}

function Get-BlockingProcesses {
    return @(Get-Process -ErrorAction SilentlyContinue | Where-Object {
        $_.ProcessName -match '^(?i:capture|allegro|pcb_editor|padstack_editor|dxp|x2|altiumdesigner|uv4|iaridepm|iaride|ewb|devenv_iar)$'
    } | Select-Object -ExpandProperty ProcessName -Unique)
}

function Get-CleanupCandidates([string]$Root, [bool]$History=$true, [bool]$Build=$true) {
    $stack = New-Object 'System.Collections.Generic.Stack[string]'
    $stack.Push($Root)
    while ($stack.Count) {
        $directory=$stack.Pop()
        $items=@(Get-ChildItem -LiteralPath $directory -Force -ErrorAction Stop)
        foreach ($file in @($items | Where-Object { -not $_.PSIsContainer })) {
            if ($file.Attributes -band [IO.FileAttributes]::ReparsePoint) { continue }
            $relative=(Assert-UnderRoot $file.FullName $Root).Substring($Root.TrimEnd('\').Length+1)
            if (Test-AIEDATextFile $file) { continue }
            $reason=Get-CleanupReason $file.Name $relative
            if (-not $reason) { continue }
            try {
                if (Test-SchematicNetlist $file) { continue }
            } catch { Write-Host "KEPT (cannot inspect netlist content): $relative"; continue }
            [pscustomobject]@{File=$file;Relative=$relative;Reason=$reason}
        }
        foreach ($dir in @($items | Where-Object { $_.PSIsContainer })) {
            if (($dir.Attributes -band [IO.FileAttributes]::ReparsePoint) -or (Test-ProtectedDirectory $dir.Name)) { continue }
            $null=Assert-UnderRoot $dir.FullName $Root
            $stack.Push($dir.FullName)
        }
    }
}

function Get-CleanupReason([string]$Name,[string]$Relative,[bool]$Cadence=$false,[bool]$Embedded=$false,[bool]$History=$true,[bool]$Build=$true,[bool]$Altium=$false) {
    if ($Name -match '(?i)\.(xml|csv|dat)(,\d+)?$') { return $null }
    foreach ($pattern in $script:CleanupPatterns) {
        if ($Name -like $pattern) { return "Original cleanup pattern: $pattern" }
    }
    return $null
}

function Test-AIEDATextFile([IO.FileInfo]$File) {
    # Historical function name retained for callers; protect all requested TXT directories.
    return $File.Name -match '(?i)\.txt(,\d+)?$' -and $File.FullName -match '(?i)(^|[\\/])(?:01AIEDA|01env|env)[\\/]'
}

function Test-SchematicNetlist([IO.FileInfo]$File) {
    # These four are the Capture PCB Editor handoff, including its optional model file.
    if ($File.Name -match '^(?i:pstchip\.dat|pstxnet\.dat|pstxprt\.dat|pstdmlmodels\.dat)$') { return $true }
    if ($File.Extension -notmatch '^(?i:\.dat|\.txt|\.xml|\.csv|\.edf|\.edif|\.net)$' -or $File.Length -eq 0) { return $false }
    $reader=New-Object IO.StreamReader($File.FullName,[Text.Encoding]::UTF8,$true)
    try {
        $buffer=New-Object char[] 65536
        $count=$reader.ReadBlock($buffer,0,$buffer.Length)
        $head=New-Object string($buffer,0,$count)
        if ($head -match '(?im)^\s*FILE_TYPE\s*=\s*(LIBRARY_PARTS|EXPANDEDNETLIST|EXPANDEDPARTLIST)\s*;') { return $true }
        $edif=$head -match '^\s*\(edif\s'
        $pads=$head -match '(?im)^\s*\*PADS-PCB\*'
        $telesis=$head -match '(?im)^\s*\$PACKAGES\b'
        $hasParts=$false; $hasNets=$false; $chunk=$head
        if ($edif -or $pads -or $telesis) {
            do {
                if ($edif -and $chunk -match '(?i)\(viewType\s+NETLIST\s*\)') { return $true }
                if ($pads) {
                    $hasParts=$hasParts -or $chunk -match '(?im)^\s*\*PART\*'
                    $hasNets=$hasNets -or $chunk -match '(?im)^\s*\*(NET|SIGNAL)\*'
                    if ($hasParts -and $hasNets) { return $true }
                }
                if ($telesis -and $chunk -match '(?im)^\s*\$NETS\b') { return $true }
                $tail=$chunk.Substring([Math]::Max(0,$chunk.Length-256))
                $count=$reader.ReadBlock($buffer,0,$buffer.Length)
                $chunk=$tail+(New-Object string($buffer,0,$count))
            } while ($count -gt 0)
        }
        # XML netlists require their format root and both components and connectivity.
        if ($head -match '^\s*<') {
            $settings=New-Object Xml.XmlReaderSettings
            $settings.DtdProcessing=[Xml.DtdProcessing]::Prohibit
            $settings.XmlResolver=$null
            $xml=$null
            try {
                $xml=[Xml.XmlReader]::Create($File.FullName,$settings)
                $rootName=$null; $components=$false; $nets=$false
                while ($xml.Read()) {
                    if ($xml.NodeType -ne [Xml.XmlNodeType]::Element) { continue }
                    if (-not $rootName) {
                        $rootName=$xml.LocalName.ToLowerInvariant()
                        if ($rootName -notin @('netlist','export')) { return $false }
                    }
                    if ($xml.LocalName -ieq 'components') { $components=$true }
                    if ($xml.LocalName -ieq 'nets') { $nets=$true }
                }
                return $components -and $nets
            } catch [Xml.XmlException] { return $false }
            finally { if ($xml) { $xml.Dispose() } }
        }
        return $false
    } finally { $reader.Dispose() }
}


function Assert-CurrentCandidate([object]$Candidate, [string]$Root) {
    $path = Assert-UnderRoot $Candidate.File.FullName $Root
    $now = Get-Item -LiteralPath $path -Force
    if ($now.PSIsContainer -or ($now.Attributes -band [IO.FileAttributes]::ReparsePoint)) { throw "Not a regular file: $path" }
    if ($now.Length -ne $Candidate.File.Length -or $now.LastWriteTimeUtc -ne $Candidate.File.LastWriteTimeUtc) {
        throw "File changed while scanning; kept: $path"
    }
    if (Test-AIEDATextFile $now) { throw "01AIEDA/env text kept: $path" }
    if ($now.Name -match '(?i)\.(xml|csv|dat)(,\d+)?$') { throw "Preserved XML/CSV/DAT: $path" }
    if (Test-SchematicNetlist $now) { throw "Schematic netlist kept: $path" }
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
                Write-Host 'Default: this entry original deletion patterns plus TXT cleanup.'
                Write-Host 'All XML/CSV/DAT (and numbered copies) are kept. TXT under 01AIEDA, env or 01env ancestors is kept.'
                Write-Host 'Recognized schematic netlists, workflow templates under 01env, and archive/version-control directories are kept.'
                Write-Host '/preview never changes files. /history and /build are accepted for compatibility.'
                Write-Host 'DSN/PCB/library/source extensions absent from the original patterns are not deleted.'
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
