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
set "EDA_CLEAN_POWERSHELL=%SystemRoot%\System32\WindowsPowerShell\v1.0\powershell.exe"
if exist "%EDA_CLEAN_POWERSHELL%" goto EDA_CLEAN_RUN
echo [Cleanup] ERROR - Windows PowerShell was not found: "%EDA_CLEAN_POWERSHELL%"
set "EDA_CLEAN_EXIT=9009"
goto EDA_CLEAN_RESULT
:EDA_CLEAN_RUN
"%EDA_CLEAN_POWERSHELL%" -NoLogo -NoProfile -ExecutionPolicy Bypass -Command "$text=[IO.File]::ReadAllText($env:EDA_CLEAN_SELF,[Text.Encoding]::UTF8);$marker='#__EDA_CLEAN_POWERSHELL__';& ([ScriptBlock]::Create($text.Substring($text.LastIndexOf($marker)+$marker.Length)))"
set "EDA_CLEAN_EXIT=%errorlevel%"
:EDA_CLEAN_RESULT
echo.
if "%EDA_CLEAN_EXIT%"=="0" (
    echo [Cleanup] OK - command completed.
) else (
    echo [Cleanup] FAILED - command did not complete. Exit code: %EDA_CLEAN_EXIT%
    echo [Cleanup] Read the error above. If design tools are open, close them before cleaning.
)
if not "%~1"=="" goto EDA_CLEAN_EXIT
echo [Cleanup] Press any key to close this window.
pause >nul
:EDA_CLEAN_EXIT
exit /b %EDA_CLEAN_EXIT%
#__EDA_CLEAN_POWERSHELL__
$ErrorActionPreference='Stop'
Write-Host ('STUB_ROOT=' + $env:EDA_CLEAN_ROOT)
Write-Host ('STUB_SELF=' + $env:EDA_CLEAN_SELF)
Write-Host ('STUB_ARG_1=' + $env:EDA_CLEAN_ARG_1)
Write-Host ('STUB_ARG_2=' + $env:EDA_CLEAN_ARG_2)
if($env:EDA_CLEAN_ARG_1 -eq '/invalid') {
    Write-Host 'STUB_INVALID_OPTION'
    Write-Host 'STUB_READY_FOR_WRAPPER'
    exit 37
}
if($env:EDA_TEST_FORCE_FAILURE -eq '1') {
    Write-Host 'STUB_FORCED_FAILURE'
    Write-Host 'STUB_READY_FOR_WRAPPER'
    exit 23
}
Write-Host 'STUB_READY_FOR_WRAPPER'
exit 0
