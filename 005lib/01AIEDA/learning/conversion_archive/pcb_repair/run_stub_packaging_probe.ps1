$ErrorActionPreference = 'Stop'
$repairRoot = 'D:\001DIY\005lib\01AIEDA\learning\staging\lga1700_pcb_repair_20261023'
$probeRoot = Join-Path $repairRoot 'stub_packaging_probe_v8'
if (Test-Path -LiteralPath $probeRoot) { throw 'Refuse existing experiment folder' }
New-Item -ItemType Directory -Path $probeRoot | Out-Null
$pythonSource = Get-Content -LiteralPath (Join-Path $repairRoot 'stub_packaging_probe.py') -Raw
$tclMatch = [regex]::Match($pythonSource, "TCL = r'''(.*?)'''", [System.Text.RegularExpressions.RegexOptions]::Singleline)
if (-not $tclMatch.Success) { throw 'Tcl template missing' }
$tclTemplate = $tclMatch.Groups[1].Value
$cadRoot = 'C:\Program0\Cadence\SPB172'
$env:CDSROOT = $cadRoot
$env:PATH = "$cadRoot\tools\bin;$cadRoot\tools\capture;$cadRoot\tcltk\bin;$env:PATH"
$env:IGNORE_PROP = 'DEVICE'
function Invoke-ProbeNative($exePath, [string[]]$nativeArgs, $logPath) {
    $startInfo = New-Object System.Diagnostics.ProcessStartInfo
    $startInfo.FileName = $exePath
    $startInfo.Arguments = (($nativeArgs | ForEach-Object { '"' + $_.Replace('"','\"') + '"' }) -join ' ')
    $startInfo.UseShellExecute = $false
    $startInfo.CreateNoWindow = $true
    $startInfo.RedirectStandardOutput = $true
    $startInfo.RedirectStandardError = $true
    $process = New-Object System.Diagnostics.Process
    $process.StartInfo = $startInfo
    [void]$process.Start()
    $readOut = $process.StandardOutput.ReadToEndAsync()
    $readErr = $process.StandardError.ReadToEndAsync()
    if (-not $process.WaitForExit(60000)) { $process.Kill(); throw 'Owned native process timed out' }
    $outText = $readOut.GetAwaiter().GetResult() + $readErr.GetAwaiter().GetResult()
    [IO.File]::WriteAllText($logPath, $outText, [Text.UTF8Encoding]::new($false))
    return $process.ExitCode
}
$results = @()
foreach ($saveScope in @('replace_one_b0')) {
    $folder = Join-Path $probeRoot $saveScope
    New-Item -ItemType Directory -Path $folder | Out-Null
    foreach ($name in @('LGA1700.DSN','allegro.cfg')) {
        Copy-Item -LiteralPath (Join-Path $repairRoot "ad_baseline_no_stubs\$name") -Destination (Join-Path $folder $name)
    }
    $scriptPath = Join-Path $folder 'add_stubs.tcl'
    $saveTcl = switch ($saveScope) {
      'replace_one_b0' { @'
set b0page [$top GetPage [::DE::cs {DDR4_UDIMM CHANNEL-B0}] $s]
set ii2 [$b0page NewPartInstsIter $s]
set target NULL
for {set ins2 [$ii2 NextPartInst $s]} {$ins2 ne "NULL"} {set ins2 [$ii2 NextPartInst $s]} {
 set pl2 [DboPartInstToDboPlacedInst $ins2]
 if {[::DE::str $pl2 GetReferenceDesignator] eq {C82}} {set target $pl2}
}
delete_DboPagePartInstsIter $ii2
if {$target eq "NULL"} {error "C82 not found"}
set sourcePackage [::DE::str $target GetSourcePackageName]
set samePart [::DE::obj [$target GetPart $s] $s SamePart]
set sameDevice [::DE::obj [$target GetDevice $s] $s SameDevice]
set newInst [::DE::obj [$b0page ReplaceInst $target [::DE::cs $sourcePackage] $samePart $sameDevice $s 1] $s ReplaceSameSymbol]
::DE::state [$newInst MarkModified] MarkReplaced
::DE::save $design
'@ }
      'build_map_flat' { '::DE::state [$top BuildIDMap] BuildIDMap; $top UpdateFlatNetsOfAllInstantiatingDesigns; ::DE::save $design' }
      'save_as' { '::DE::state [$sess MarkAllLibForSave $design] MarkAll; ::DE::state [$sess SaveDesignAs $design [::DE::cs "$root/LGA1700_SAVEAS.DSN"]] SaveAs' }
      'cache_parts' { '::DE::save $design' }
      'expand_id_map' { '::DE::state [$top BuildIDMap] BuildIDMap; ::DE::state [$top Expand] Expand; $top UpdateFlatNetsOfAllInstantiatingDesigns; ::DE::save $design' }
      'official_session_save' { '::DE::state [$sess MarkAllLibForSave $design] MarkAllLibForSave; ::DE::state [$sess SaveDesign $design] SaveDesign' }
      'mark_a0_no_savepage' { @'
set pi2 [$top NewPagesIter $s]
for {set pg [$pi2 NextPage $s]} {$pg ne "NULL"} {set pg [$pi2 NextPage $s]} {
 if {[::DE::str $pg GetName] eq {DDR4_UDIMM CHANNEL-A0}} {
  ::DE::state [$pg MarkModified] MarkPage
  ::DE::state [$top MarkModified $pg] MarkChangedPage
 }
}
delete_DboSchematicPagesIter $pi2
::DE::state [$top MarkModified] MarkTop
::DE::state [$design SaveSchematic $top] SaveSchematic
::DE::state [$sess SaveDesign $design] SaveDesign
'@ }
      'savepage_bval1' { @'
set pi2 [$top NewPagesIter $s]
for {set pg [$pi2 NextPage $s]} {$pg ne "NULL"} {set pg [$pi2 NextPage $s]} {
 ::DE::state [$pg MarkModified] MarkPage
 ::DE::state [$top MarkModified $pg] MarkChangedPage
 ::DE::state [$top SavePage $pg 1] SaveChangedPage
}
delete_DboSchematicPagesIter $pi2
::DE::state [$top MarkModified] MarkTop
::DE::state [$design SaveSchematic $top] SaveSchematic
::DE::state [$sess SaveDesign $design] SaveDesign
'@ }
      'no_root_occurrence' { '::DE::save $design' }
    }
    $variantTcl = $tclTemplate.Replace('@ROOT@',$folder.Replace('\','/')).Replace('@LEN@','1').Replace('::DE::save $design',$saveTcl)
    if ($saveScope -eq 'cache_parts') {
        $variantTcl = $variantTcl.Replace('audit before','::DE::state [$top ReadAllPages] ReadAllPages; audit before')
        $variantTcl = $variantTcl.Replace('set pins [$inst NewPinsIter $s]', @'
set cachedPart [::DE::obj [$placed GetPart $s] $s InstancePart]
set cachedPackage [::DE::obj [$placed GetPackage $s] $s InstancePackage]
set cachedDevice [::DE::obj [$placed GetDevice $s] $s InstanceDevice]
set cachedCell [::DE::obj [$cachedDevice GetCell $s] $s DeviceCell]
set pins [$inst NewPinsIter $s]
'@)
    }
    if ($saveScope -eq 'no_root_occurrence') { $variantTcl=$variantTcl.Replace('::DE::obj [$design GetRootOccurrence $s] $s RootOccurrence','') }
    $variantTcl | Set-Content -LiteralPath $scriptPath -Encoding ASCII
    Push-Location -LiteralPath $folder
    try {
        $tclExit = Invoke-ProbeNative "$cadRoot\tcltk\bin\tclsh.exe" @($scriptPath) (Join-Path $folder 'tcl_output.txt')
        $record = [ordered]@{variant=$saveScope;tcl_exit=$tclExit}
        if ($tclExit -eq 0) {
            $netlistFolder = Join-Path $folder 'netlist'
            New-Item -ItemType Directory -Path $netlistFolder | Out-Null
            $netlistDsn = Join-Path $folder 'LGA1700.DSN'
            if ($saveScope -eq 'save_as') { $netlistDsn=Join-Path $folder 'LGA1700_SAVEAS.DSN' }
            $record.pst_exit = Invoke-ProbeNative "$cadRoot\tools\bin\pstswp.exe" @('-pst','-d',$netlistDsn,'-n',$netlistFolder,'-c',(Join-Path $folder 'allegro.cfg'),'-v','3','-l','255','-j','PCB Footprint') (Join-Path $folder 'pst_output.txt')
            $record.pst_error_count = @([regex]::Matches((Get-Content -LiteralPath (Join-Path $folder 'pst_output.txt') -Raw),'ERROR\(')).Count
        }
        $results += [pscustomobject]$record
        $results | ConvertTo-Json -Depth 4 | Set-Content -LiteralPath (Join-Path $probeRoot 'results.json') -Encoding UTF8
        $record | ConvertTo-Json -Compress
    } finally { Pop-Location }
}
