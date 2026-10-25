$ErrorActionPreference = 'Stop'
$sourceRoot = 'D:\001DIY\005lib'
$reportRoot = 'D:\001DIY\004computer\lga1700\git_upload_005lib_20261025'
$topDirs = @(Get-ChildItem -LiteralPath $sourceRoot -Directory -Force | Where-Object { $_.Name -like '01*' })
$files = New-Object 'System.Collections.Generic.List[object]'
$reparsePoints = New-Object 'System.Collections.Generic.List[object]'
$gitEntries = New-Object 'System.Collections.Generic.List[object]'
$sensitiveNames = New-Object 'System.Collections.Generic.List[object]'
$scanErrors = New-Object 'System.Collections.Generic.List[object]'
$directories = New-Object 'System.Collections.Generic.List[object]'
foreach ($topDir in $topDirs) {
    $stack = New-Object 'System.Collections.Generic.Stack[string]'
    $stack.Push($topDir.FullName)
    while ($stack.Count -gt 0) {
        $path = $stack.Pop()
        try { $entries = @(Get-ChildItem -LiteralPath $path -Force) }
        catch { $scanErrors.Add([pscustomobject]@{ path=$path; error=$_.Exception.Message }); continue }
        foreach ($entry in $entries) {
            $relative = $entry.FullName.Substring($sourceRoot.Length + 1).Replace('\','/')
            $isReparse = (($entry.Attributes -band [IO.FileAttributes]::ReparsePoint) -ne 0)
            if ($entry.Name -eq '.git') { $gitEntries.Add([pscustomobject]@{source=$entry.FullName;relative=$relative;isDirectory=$entry.PSIsContainer}) }
            if ($isReparse) {
                $reparsePoints.Add([pscustomobject]@{ source=$entry.FullName;relative=$relative;isDirectory=$entry.PSIsContainer;linkType=$entry.LinkType;target=$entry.Target })
            }
            if ($entry.PSIsContainer) {
                $directories.Add([pscustomobject]@{source=$entry.FullName;relative=$relative;isReparse=$isReparse})
                if (-not $isReparse) { $stack.Push($entry.FullName) }
            } else {
                $category = $null
                if ($entry.Name -match '(^\.env($|\.)|^\.git-credentials$|^id_(rsa|dsa|ecdsa|ed25519)(\.pub)?$|credential|secret|token|password)') { $category = 'credential-like-name' }
                elseif ($entry.Extension -match '^\.(pem|pfx|p12|key)$') { $category = 'key-or-certificate-extension' }
                elseif ($entry.Extension -eq '.lic' -or $entry.Name -match '^licen[cs]e\.(dat|txt)$') { $category = 'license-like-name' }
                if ($category) { $sensitiveNames.Add([pscustomobject]@{source=$entry.FullName;relative=$relative;category=$category}) }
                $hash = $null
                if ($entry.Length -gt 50MB -and -not $category) { $hash = (Get-FileHash -LiteralPath $entry.FullName -Algorithm SHA256).Hash.ToLowerInvariant() }
                $files.Add([pscustomobject]@{source=$entry.FullName;relative=$relative;topDirectory=$topDir.Name;size=[long]$entry.Length;attributes=[string]$entry.Attributes;isReparse=$isReparse;sha256=$hash})
            }
        }
    }
}
$summary = foreach ($topDir in $topDirs) {
    $group = @($files | Where-Object {$_.topDirectory -eq $topDir.Name})
    [pscustomobject]@{name=$topDir.Name;fileCount=$group.Count;bytes=[long](($group | Measure-Object size -Sum).Sum);over50MiB=@($group | Where-Object {$_.size -gt 50MB}).Count;over100MiB=@($group | Where-Object {$_.size -gt 100MB}).Count}
}
$result = [pscustomobject]@{
    generatedAt=(Get-Date).ToString('o');sourceRoot=$sourceRoot
    directories=$summary;totalFiles=$files.Count;totalBytes=[long](($files | Measure-Object size -Sum).Sum)
    largeFiles=@($files | Where-Object {$_.size -gt 50MB});reparsePoints=@($reparsePoints.ToArray());gitEntries=@($gitEntries.ToArray());sensitiveNames=@($sensitiveNames.ToArray());scanErrors=@($scanErrors.ToArray())
}
$files | Sort-Object relative | Export-Csv -LiteralPath (Join-Path $reportRoot 'upload_inventory.csv') -NoTypeInformation -Encoding UTF8
$result | ConvertTo-Json -Depth 8 | Set-Content -LiteralPath (Join-Path $reportRoot 'upload_inventory.json') -Encoding UTF8
$result | ConvertTo-Json -Depth 8
