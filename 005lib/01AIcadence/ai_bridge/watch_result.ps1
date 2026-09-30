$exch = 'D:\001DIY\005lib\01AIcadence\ai_bridge\exchange'
$flag = Join-Path $exch 'result.flag'
$res  = Join-Path $exch 'result.txt'
$deadline = (Get-Date).AddMinutes(30)

while (-not (Test-Path $flag) -and (Get-Date) -lt $deadline) {
    Start-Sleep -Seconds 2
}

if (Test-Path $flag) {
    Write-Host 'RESULT_READY'
    Get-Content $res
} else {
    Write-Host 'TIMEOUT_NO_RESULT'
}
