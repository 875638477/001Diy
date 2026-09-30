@echo off
setlocal ENABLEDELAYEDEXPANSION
pushd "%~dp0"

set "ALLEGRO=C:\Program0\Cadence\spb172\tools\bin\allegro.exe"
set "FP_XML=LFBGA408_19X19.xml"
set "scriptDir=%CD%"
set "skillScriptPath=!scriptDir:\=/!"

echo ============================================
echo AST2400 Allegro footprint builder
echo Dir: %CD%
echo Allegro: %ALLEGRO%
echo XML: %FP_XML%
echo ============================================

if not exist "%ALLEGRO%" (
  echo ERROR: allegro.exe not found:
  echo   %ALLEGRO%
  echo Edit ALLEGRO= path in this bat.
  goto FAIL
)
if not exist "builder.ile" (
  echo ERROR: builder.ile missing in this folder.
  goto FAIL
)
if not exist "%FP_XML%" (
  echo ERROR: footprint XML missing: %FP_XML%
  echo This is why Allegro flashed and exited with nothing created.
  echo Re-run: python ...\ast2400_lib\build_allegro_fp.py
  goto FAIL
)

echo skill load "!skillScriptPath!/builder.ile" > builder.scr.txt
echo skill changeWorkingDir "!skillScriptPath!" >> builder.scr.txt
echo skill LB_createFootprint "!skillScriptPath!/%FP_XML%" >> builder.scr.txt
echo exit >> builder.scr.txt

echo ---- builder.scr.txt ----
type builder.scr.txt
echo -------------------------
echo Creating footprint...
START /WAIT "" "%ALLEGRO%" -s builder.scr.txt
set ERR=!ERRORLEVEL!

echo.
if exist "LFBGA408_19X19.dra" (
  echo OK: LFBGA408_19X19.dra created
) else if exist "LFBGA408_19X19.psm" (
  echo OK: LFBGA408_19X19.psm created
) else (
  echo WARN: no .dra/.psm found. Check allegro.jrl for skill errors.
  echo ERRLEVEL=!ERR!
  goto FAIL
)

echo Done. Copy .pad/.psm to 01Pad_lib / 01Psm_lib when ready.
popd
echo.
pause
exit /b 0

:FAIL
echo.
echo FAILED. Window kept open for diagnosis.
popd
pause
exit /b 1
