# auto_run.ps1 -- watch command.flag and auto-type "ai_run" into Allegro
# Replaces manual typing of ai_run in the Allegro command line.
# Keep this file ASCII only.

$exch = "D:\001DIY\005lib\01AIcadence\ai_bridge\exchange"
$wsh = New-Object -ComObject WScript.Shell

Write-Host "AI auto-run watcher started. Press Ctrl+C to stop."

while ($true) {
    if (Test-Path "$exch\command.flag") {
        $p = Get-Process | Where-Object { $_.MainWindowTitle -like "*Allegro*" } | Select-Object -First 1
        if ($p) {
            if ($wsh.AppActivate($p.Id)) {
                Start-Sleep -Milliseconds 500
                $wsh.SendKeys("ai_run{ENTER}")
                Write-Host ("{0:HH:mm:ss} sent ai_run to '{1}'" -f (Get-Date), $p.MainWindowTitle)
                # wait until the bridge consumes the flag (max 15 s)
                $t0 = Get-Date
                while ((Test-Path "$exch\command.flag") -and ((Get-Date) - $t0).TotalSeconds -lt 15) {
                    Start-Sleep -Milliseconds 300
                }
                if (Test-Path "$exch\command.flag") {
                    Write-Host "WARN: flag still present after 15 s (command not consumed)"
                } else {
                    Write-Host ("{0:HH:mm:ss} command consumed" -f (Get-Date))
                }
            } else {
                Write-Host "WARN: cannot activate Allegro window"
            }
        } else {
            Write-Host "WARN: Allegro window not found"
        }
    }
    Start-Sleep -Milliseconds 800
}
