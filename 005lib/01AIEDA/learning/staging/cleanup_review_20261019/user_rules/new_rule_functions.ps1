function Get-CleanupCandidates([string]$Root, [bool]$History=$true, [bool]$Build=$true) {
    $stack = New-Object 'System.Collections.Generic.Stack[string]'
    $stack.Push($Root)
    while ($stack.Count) {
        $directory=$stack.Pop()
        $items=@(Get-ChildItem -LiteralPath $directory -Force -ErrorAction Stop)
        foreach ($file in @($items | Where-Object { -not $_.PSIsContainer })) {
            if ($file.Attributes -band [IO.FileAttributes]::ReparsePoint) { continue }
            $relative=(Assert-UnderRoot $file.FullName $Root).Substring($Root.TrimEnd('\').Length+1)
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
    if ($Relative -match '(?i)(^|[\\/])01AIEDA[\\/]' -and $Name -match '(?i)\.txt(,\d+)?$') { return $null }
    foreach ($pattern in $script:CleanupPatterns) {
        if ($Name -like $pattern) { return "Original cleanup pattern: $pattern" }
    }
    return $null
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

