@echo off
setlocal ENABLEDELAYEDEXPANSION
pushd "%~dp0"

set "ALLEGRO=C:\Program0\Cadence\spb172\tools\bin\allegro.exe"
set "FP=TQFN38_5X7"
set "PAD1=r25_70"
set "PAD2=r315_515"
set "PAD_LIB=D:\001DIY\005lib\01Pad_lib"
set "PSM_LIB=D:\001DIY\005lib\01Psm_lib"
set "scriptDir=%CD%"
set "skillScriptPath=!scriptDir:\=/!"

echo ============================================
echo Build footprint: %FP%
echo Work: %CD%
echo ============================================

if not exist "%ALLEGRO%" (
  echo ERROR: allegro.exe not found: %ALLEGRO%
  goto FAIL
)
if not exist "builder.ile" (
  echo ERROR: builder.ile missing
  goto FAIL
)
if not exist "%FP%.xml" (
  echo ERROR: missing %FP%.xml
  goto FAIL
)

del /q "%FP%.dra" "%FP%.psm" "tqfn38_5x7.psm" "%PAD1%.pad" "%PAD2%.pad" *.lck 2>nul

echo skill load "!skillScriptPath!/builder.ile" > builder.scr.txt
echo skill changeWorkingDir "!skillScriptPath%" >> builder.scr.txt
echo skill LB_createFootprint "!skillScriptPath!/%FP%.xml" >> builder.scr.txt
echo exit >> builder.scr.txt

echo ---- builder.scr.txt ----
type builder.scr.txt
echo -------------------------
echo Running Allegro...
START /WAIT "" "%ALLEGRO%" -s builder.scr.txt

if not exist "%FP%.dra" (
  echo ERROR: %FP%.dra not created. See allegro.jrl / %FP%.log
  goto FAIL
)

if exist "tqfn38_5x7.psm" if not exist "%FP%.psm" copy /y "tqfn38_5x7.psm" "%FP%.psm" >nul

if not exist "backup" mkdir "backup"
copy /y "%FP%.xml" "backup\%FP%.xml" >nul
copy /y "%FP%.bat" "backup\%FP%.bat" >nul
copy /y "builder.ile" "backup\builder.ile" >nul
if exist "%FP%.dra" copy /y "%FP%.dra" "backup\%FP%.dra" >nul
if exist "%PAD1%.pad" copy /y "%PAD1%.pad" "backup\%PAD1%.pad" >nul
if exist "%PAD2%.pad" copy /y "%PAD2%.pad" "backup\%PAD2%.pad" >nul
if exist "%FP%.psm" copy /y "%FP%.psm" "backup\%FP%.psm" >nul

if not exist "%PAD_LIB%" mkdir "%PAD_LIB%"
if exist "%PAD1%.pad" copy /y "%PAD1%.pad" "%PAD_LIB%\%PAD1%.pad" >nul
if exist "%PAD2%.pad" copy /y "%PAD2%.pad" "%PAD_LIB%\%PAD2%.pad" >nul

if not exist "%PSM_LIB%" mkdir "%PSM_LIB%"
copy /y "%FP%.xml" "%PSM_LIB%\%FP%.xml" >nul
copy /y "%FP%.dra" "%PSM_LIB%\%FP%.dra" >nul
if exist "%FP%.psm" copy /y "%FP%.psm" "%PSM_LIB%\%FP%.psm" >nul
if exist "tqfn38_5x7.psm" if not exist "%PSM_LIB%\%FP%.psm" copy /y "tqfn38_5x7.psm" "%PSM_LIB%\%FP%.psm" >nul

echo.
echo Done.
echo   Pad -> %PAD_LIB%
echo   Psm -> %PSM_LIB%
popd
pause
exit /b 0

:FAIL
echo.
echo FAILED. Check allegro.jrl
popd
pause
exit /b 1
