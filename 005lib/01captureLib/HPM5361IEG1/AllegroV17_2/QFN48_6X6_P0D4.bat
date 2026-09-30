@echo off
chcp 65001 >nul
setlocal ENABLEDELAYEDEXPANSION
pushd "%~dp0"

set "ALLEGRO_BIN=C:\Program0\Cadence\spb172\tools\bin"
set "FP=QFN48_6X6_P0D4"
set "PAD_LIB=D:\001DIY\005lib\01Pad_lib"
set "PSM_LIB=D:\001DIY\005lib\01Psm_lib"

echo ============================================
echo Build footprint: %FP%
echo Work: %CD%
echo ============================================

if not exist "%ALLEGRO_BIN%\allegro.exe" (
  echo ERROR: allegro.exe not found
  goto FAIL
)
if not exist "%ALLEGRO_BIN%\padstack_editor.exe" (
  echo ERROR: padstack_editor.exe not found
  goto FAIL
)

if not exist "%PAD_LIB%" mkdir "%PAD_LIB%"
if not exist "%PSM_LIB%" mkdir "%PSM_LIB%"

echo ---- 1) padstack pxml -^> .pad ----
for %%P in (r85_20 r20_85 r420) do (
  echo [PAD] %%P
  "%ALLEGRO_BIN%\padstack_editor.exe" -x "%%P.pxml"
  if exist "%%P.pad" copy /Y "%%P.pad" "%PAD_LIB%\%%P.pad" >nul
  if not exist "%%P.pad" (
    echo ERROR: %%P.pad not created
    goto FAIL
  )
)

set "PADPATH=%PAD_LIB%;%CD%;%PADPATH%"

echo ---- 2) Allegro package symbol ----
if exist "%FP%.dra" del /q "%FP%.dra"
if exist "%FP%.psm" del /q "%FP%.psm"
if exist "%FP%.dra.lck" del /q "%FP%.dra.lck"

START /WAIT "" "%ALLEGRO_BIN%\allegro.exe" -nograph -s "%FP%.scr"
if not exist "%FP%.dra" (
  echo ERROR: %FP%.dra not created. See allegro.jrl
  goto FAIL
)

if not exist "backup" mkdir "backup"
copy /Y "%FP%.scr" "backup\%FP%.scr" >nul
copy /Y "%FP%.bat" "backup\%FP%.bat" >nul
for %%P in (r85_20 r20_85 r420) do (
  if exist "%%P.pxml" copy /Y "%%P.pxml" "backup\%%P.pxml" >nul
  if exist "%%P.pad" copy /Y "%%P.pad" "backup\%%P.pad" >nul
)
if exist "%FP%.dra" copy /Y "%FP%.dra" "backup\%FP%.dra" >nul
if exist "%FP%.psm" copy /Y "%FP%.psm" "backup\%FP%.psm" >nul

copy /Y "%FP%.dra" "%PSM_LIB%\%FP%.dra" >nul
if exist "%FP%.psm" copy /Y "%FP%.psm" "%PSM_LIB%\%FP%.psm" >nul

echo.
echo Done.
echo   Pad -^> %PAD_LIB%
echo   Psm -^> %PSM_LIB%
popd
exit /b 0

:FAIL
echo FAILED
popd
exit /b 1
