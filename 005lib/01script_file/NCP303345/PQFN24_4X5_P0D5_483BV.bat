@echo off
chcp 65001 >nul
setlocal ENABLEDELAYEDEXPANSION
pushd "%~dp0"
set "ALLEGRO_BIN=C:\Program0\Cadence\spb172\tools\bin"
set "FP=PQFN24_4X5_P0D5_483BV"
set "PAD_LIB=D:\001DIY\005lib\01Pad_lib"
set "PSM_LIB=D:\001DIY\005lib\01Psm_lib"
set "ARCHIVE_ALG=D:\001DIY\005lib\AUTOlib\NCP303345\01_成品库_ul_NCP303345\AllegroV17_2"
set "CAPTURE_ALG=D:\001DIY\005lib\AUTOlib\NCP303345\03_captureLib_NCP303345\AllegroV17_2"
if not exist "%ALLEGRO_BIN%\allegro.exe" (echo ERROR: allegro.exe not found& goto FAIL)
if not exist "%ALLEGRO_BIN%\padstack_editor.exe" (echo ERROR: padstack_editor.exe not found& goto FAIL)
if not exist "%PAD_LIB%" mkdir "%PAD_LIB%"
if not exist "%PSM_LIB%" mkdir "%PSM_LIB%"
if not exist "%ARCHIVE_ALG%" mkdir "%ARCHIVE_ALG%"
if not exist "%CAPTURE_ALG%" mkdir "%CAPTURE_ALG%"
if exist "ncp_ep28_shape.dra" del /q "ncp_ep28_shape.dra"
if exist "ncp_ep28_shape.ssm" del /q "ncp_ep28_shape.ssm"
START /WAIT "" "%ALLEGRO_BIN%\allegro.exe" -nograph -s "ncp_ep28_shape.scr"
if not exist "ncp_ep28_shape.ssm" (echo ERROR: ncp_ep28_shape.ssm not created& goto FAIL)
copy /Y "ncp_ep28_shape.ssm" "%PSM_LIB%\ncp_ep28_shape.ssm" >nul
set "PSMPATH=%PSM_LIB%;%CD%;%PSMPATH%"
for %%P in (ncp_r54_30 ncp_r47_30 ncp_r30_54 ncp_r30_47 ncp_ep25 ncp_ep26 ncp_ep27 ncp_ep28) do (
  echo [PAD] %%P
  "%ALLEGRO_BIN%\padstack_editor.exe" -x "%%P.pxml"
  if not exist "%%P.pad" (echo ERROR: %%P.pad not created& goto FAIL)
  copy /Y "%%P.pad" "%PAD_LIB%\%%P.pad" >nul
  copy /Y "%%P.pad" "%ARCHIVE_ALG%\%%P.pad" >nul
  copy /Y "%%P.pad" "%CAPTURE_ALG%\%%P.pad" >nul
)
set "PADPATH=%PAD_LIB%;%CD%;%PADPATH%"
if exist "%FP%.dra" del /q "%FP%.dra"
if exist "%FP%.psm" del /q "%FP%.psm"
if exist "%FP%.dra.lck" del /q "%FP%.dra.lck"
START /WAIT "" "%ALLEGRO_BIN%\allegro.exe" -nograph -s "%FP%.scr"
if not exist "%FP%.dra" (echo ERROR: %FP%.dra not created. See allegro.jrl& goto FAIL)
findstr /C:"ERROR(" "allegro.jrl" >nul && (echo ERROR: Allegro journal contains errors& goto FAIL)
if not exist "backup" mkdir "backup"
copy /Y "%FP%.scr" "backup\%FP%.scr" >nul
copy /Y "%FP%.bat" "backup\%FP%.bat" >nul
copy /Y "ncp_ep28_shape.scr" "backup\ncp_ep28_shape.scr" >nul
copy /Y "ncp_ep28_shape.dra" "backup\ncp_ep28_shape.dra" >nul
copy /Y "ncp_ep28_shape.ssm" "backup\ncp_ep28_shape.ssm" >nul
for %%P in (ncp_r54_30 ncp_r47_30 ncp_r30_54 ncp_r30_47 ncp_ep25 ncp_ep26 ncp_ep27 ncp_ep28) do (
  copy /Y "%%P.pxml" "backup\%%P.pxml" >nul
  copy /Y "%%P.pad" "backup\%%P.pad" >nul
)
copy /Y "%FP%.dra" "%PSM_LIB%\%FP%.dra" >nul
if exist "%FP%.psm" copy /Y "%FP%.psm" "%PSM_LIB%\%FP%.psm" >nul
copy /Y "%FP%.dra" "%ARCHIVE_ALG%\%FP%.dra" >nul
copy /Y "%FP%.dra" "%CAPTURE_ALG%\%FP%.dra" >nul
copy /Y "ncp_ep28_shape.dra" "%ARCHIVE_ALG%\ncp_ep28_shape.dra" >nul
copy /Y "ncp_ep28_shape.ssm" "%ARCHIVE_ALG%\ncp_ep28_shape.ssm" >nul
copy /Y "ncp_ep28_shape.dra" "%CAPTURE_ALG%\ncp_ep28_shape.dra" >nul
copy /Y "ncp_ep28_shape.ssm" "%CAPTURE_ALG%\ncp_ep28_shape.ssm" >nul
if exist "%FP%.psm" copy /Y "%FP%.psm" "%ARCHIVE_ALG%\%FP%.psm" >nul
if exist "%FP%.psm" copy /Y "%FP%.psm" "%CAPTURE_ALG%\%FP%.psm" >nul
echo Done: %FP%
popd
exit /b 0
:FAIL
echo FAILED
popd
exit /b 1
