@echo off
setlocal ENABLEDELAYEDEXPANSION
pushd "%~dp0"

set "ALLEGRO=C:\Program0\Cadence\spb172\tools\bin\allegro.exe"
set "FP=LFBGA408_19X19"
set "PAD=c16"
set "PAD_LIB=D:\001DIY\005lib\01Pad_lib"
set "PSM_LIB=D:\001DIY\005lib\01Psm_lib"
set "scriptDir=%CD%"
set "skillScriptPath=!scriptDir:\=/!"

echo ============================================
echo Build footprint: %FP%
echo Work: %CD%
echo Pad  -> %PAD_LIB%
echo Psm  -> %PSM_LIB%
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
  echo Run: python D:\001DIY\005lib\01AIcadence\ast2400_lib\build_allegro_fp.py
  goto FAIL
)

del /q "%FP%.dra" "%FP%.psm" "lfbga408_19x19.psm" "%PAD%.pad" *.lck 2>nul

echo skill load "!skillScriptPath!/builder.ile" > builder.scr.txt
echo skill changeWorkingDir "!skillScriptPath!" >> builder.scr.txt
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

REM normalize psm name
if exist "lfbga408_19x19.psm" if not exist "%FP%.psm" copy /y "lfbga408_19x19.psm" "%FP%.psm" >nul

echo.
echo ---- 1) bat dir backup (keep local copies) ----
if not exist "backup" mkdir "backup"
copy /y "%FP%.xml" "backup\%FP%.xml" >nul
copy /y "%FP%.bat" "backup\%FP%.bat" >nul
copy /y "builder.ile" "backup\builder.ile" >nul
if exist "%FP%.dra" copy /y "%FP%.dra" "backup\%FP%.dra" >nul
if exist "%PAD%.pad" copy /y "%PAD%.pad" "backup\%PAD%.pad" >nul
if exist "%FP%.psm" copy /y "%FP%.psm" "backup\%FP%.psm" >nul
if exist "lfbga408_19x19.psm" copy /y "lfbga408_19x19.psm" "backup\%FP%.psm" >nul
echo BAK: %CD%\backup\

echo ---- 2) pad source -> 01Pad_lib ----
if not exist "%PAD_LIB%" mkdir "%PAD_LIB%"
if exist "%PAD%.pad" (
  copy /y "%PAD%.pad" "%PAD_LIB%\%PAD%.pad" >nul
  echo PAD: %PAD_LIB%\%PAD%.pad
) else (
  echo WARN: %PAD%.pad not found
)

echo ---- 3) footprint source -> 01Psm_lib ----
if not exist "%PSM_LIB%" mkdir "%PSM_LIB%"
copy /y "%FP%.xml" "%PSM_LIB%\%FP%.xml" >nul
copy /y "%FP%.dra" "%PSM_LIB%\%FP%.dra" >nul
echo PSM: %PSM_LIB%\%FP%.xml
echo PSM: %PSM_LIB%\%FP%.dra
if exist "%FP%.psm" (
  copy /y "%FP%.psm" "%PSM_LIB%\%FP%.psm" >nul
  echo PSM: %PSM_LIB%\%FP%.psm
) else if exist "lfbga408_19x19.psm" (
  copy /y "lfbga408_19x19.psm" "%PSM_LIB%\%FP%.psm" >nul
  echo PSM: %PSM_LIB%\%FP%.psm
) else (
  echo WARN: .psm missing ^(create_sym may have failed; .dra/.xml still copied^)
  echo       Check lfbga408_19x19.log
)

echo.
echo Done. Work dir keeps originals; libs got copies; backup\ is snapshot.
popd
pause
exit /b 0

:FAIL
echo.
echo FAILED. Check allegro.jrl
popd
pause
exit /b 1
