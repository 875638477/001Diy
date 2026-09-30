# -*- coding: utf-8 -*-
"""Build AST2400 Allegro footprint; bat named after footprint; outputs to Pad/Psm libs."""
from __future__ import annotations

import importlib.util
import re
import shutil
from pathlib import Path

ROOT = Path(r"D:\001DIY\005lib")
WORK = ROOT / "AUTOlib" / "ul_AST2400" / "AllegroV17_2"
PAD_LIB = ROOT / "01Pad_lib"
PSM_LIB = ROOT / "01Psm_lib"
SCRIPT_DIR = ROOT / "01script_file" / "AST2400"
UL_BUILDER = ROOT / "AUTOlib" / "ul_TPS65217CRSLR" / "AllegroV17_2" / "builder.ile"
ALLEGRO = Path(r"C:\Program0\Cadence\spb172\tools\bin\allegro.exe")
FP_NAME = "LFBGA408_19X19"
PAD_NAME = "c16"  # ~0.40mm land
ROW_ORDER = [
    "A", "B", "C", "D", "E", "F", "G", "H", "J", "K", "L", "M",
    "N", "P", "R", "T", "U", "V", "W", "Y", "AA", "AB",
]

spec = importlib.util.spec_from_file_location(
    "evb", ROOT / "01AIcadence" / "ast2400_lib" / "gen_ul_ast2400_evb.py"
)
evb = importlib.util.module_from_spec(spec)
spec.loader.exec_module(evb)


def mm_to_mil(mm: float) -> float:
    return mm / 0.0254


def ball_xy_mil(ball: str) -> tuple[float, float]:
    m = re.match(r"^([A-Z]+)(\d+)$", ball)
    row, col = m.group(1), int(m.group(2))
    ri = ROW_ORDER.index(row)
    x = (col - 11.5) * mm_to_mil(0.8)
    y = (10.5 - ri) * mm_to_mil(0.8)
    return x, y


def all_balls() -> list[str]:
    balls: list[str] = []
    for letter in "ABCD":
        for _label, left, right in evb.LAYOUT[letter]:
            balls.extend(left)
            balls.extend(right)
    seen, out = set(), []
    for b in balls:
        if b not in seen:
            seen.add(b)
            out.append(b)
    return out


def write_footprint_xml(path: Path, balls: list[str]) -> None:
    pad = mm_to_mil(0.40)
    mask = mm_to_mil(0.50)
    half = mm_to_mil(19.0) / 2
    cy = half + mm_to_mil(0.25)
    a1x, a1y = ball_xy_mil("A1") if "A1" in balls else (-half, half)

    pin_lines = [
        f'    <Pin number="{b}" padName="{PAD_NAME}" '
        f'originX="{x:.4f}" originY="{y:.4f}" rotation="0" isMechanical="no" textBlk="1" />'
        for b in balls
        for x, y in [ball_xy_mil(b)]
    ]

    def rect_layer(layer: str, half_sz: float, lw: float = 5) -> str:
        pts = [(-half_sz, -half_sz), (-half_sz, half_sz), (half_sz, half_sz),
               (half_sz, -half_sz), (-half_sz, -half_sz)]
        pts_xml = "\n".join(f'        <Point x="{x:.4f}" y="{y:.4f}" />' for x, y in pts)
        return (
            f'    <Layer name="{layer}" packageHeight="0" >\n'
            f'      <Path lineWidth="{lw}" type="open" >\n{pts_xml}\n'
            f"      </Path>\n    </Layer>\n"
        )

    # Multiline UL style; no <?xml?> declaration (UL tokenizer rejects it)
    xml = f"""<Footprint name="{FP_NAME}" >
  <Units type="mils" precision="3" />
  <Extents minX="{-cy-50:.4f}" minY="{-cy-50:.4f}" width="{2*cy+100:.4f}" height="{2*cy+100:.4f}" />
  <Padstack name="{PAD_NAME}" type="single" > 
    <Layers>
      <Layer name="TOP" >
        <Pad shape="circle" width="{pad:.4f}" height="{pad:.4f}" /> 
      </Layer>
      <Layer name="PASTEMASK_TOP" >
        <Pad shape="circle" width="{pad:.4f}" height="{pad:.4f}" /> 
      </Layer>
      <Layer name="SOLDERMASK_TOP" >
        <Pad shape="circle" width="{mask:.4f}" height="{mask:.4f}" /> 
      </Layer>
    </Layers>
  </Padstack>

  <TextBlocks>
    <TextBlock name="17" width="6.25" height="25" lineSpacing="25" characterSpacing="6.25" /> 
  </TextBlocks>

  <Pins>
{chr(10).join(pin_lines)}
  </Pins>
  <Vias>
  </Vias>
  <Layers>
{rect_layer("PACKAGE GEOMETRY/ASSEMBLY_TOP", half, 5)}{rect_layer("PACKAGE GEOMETRY/PLACE_BOUND_TOP", cy, 0)}{rect_layer("PACKAGE GEOMETRY/SILKSCREEN_TOP", half, 5)}    <Layer name="PACKAGE GEOMETRY/SILKSCREEN_TOP" packageHeight="0" >
      <Path lineWidth="0" type="shape" >
        <Point x="{a1x - 20:.4f}" y="{a1y + 20:.4f}" />
        <Point x="{a1x - 5:.4f}" y="{a1y + 20:.4f}" />
        <Point x="{a1x - 5:.4f}" y="{a1y + 5:.4f}" />
        <Point x="{a1x - 20:.4f}" y="{a1y + 5:.4f}" />
        <Point x="{a1x - 20:.4f}" y="{a1y + 20:.4f}" />
      </Path>
    </Layer>
  </Layers>
  <Heights>
  </Heights>
</Footprint>
"""
    path.write_text(xml, encoding="ascii", newline="\n")


def write_bat(path: Path) -> None:
    """Bat name must be footprint name (no date). Copies outputs to Pad/Psm libs."""
    content = f"""@echo off
setlocal ENABLEDELAYEDEXPANSION
pushd "%~dp0"

set "ALLEGRO={ALLEGRO}"
set "FP={FP_NAME}"
set "PAD={PAD_NAME}"
set "PAD_LIB={PAD_LIB}"
set "PSM_LIB={PSM_LIB}"
set "scriptDir=%CD%"
set "skillScriptPath=!scriptDir:\\=/!"

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
  echo Run: python D:\\001DIY\\005lib\\01AIcadence\\ast2400_lib\\build_allegro_fp.py
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
copy /y "%FP%.xml" "backup\\%FP%.xml" >nul
copy /y "%FP%.bat" "backup\\%FP%.bat" >nul
copy /y "builder.ile" "backup\\builder.ile" >nul
if exist "%FP%.dra" copy /y "%FP%.dra" "backup\\%FP%.dra" >nul
if exist "%PAD%.pad" copy /y "%PAD%.pad" "backup\\%PAD%.pad" >nul
if exist "%FP%.psm" copy /y "%FP%.psm" "backup\\%FP%.psm" >nul
if exist "lfbga408_19x19.psm" copy /y "lfbga408_19x19.psm" "backup\\%FP%.psm" >nul
echo BAK: %CD%\\backup\\

echo ---- 2) pad source -> 01Pad_lib ----
if not exist "%PAD_LIB%" mkdir "%PAD_LIB%"
if exist "%PAD%.pad" (
  copy /y "%PAD%.pad" "%PAD_LIB%\\%PAD%.pad" >nul
  echo PAD: %PAD_LIB%\\%PAD%.pad
) else (
  echo WARN: %PAD%.pad not found
)

echo ---- 3) footprint source -> 01Psm_lib ----
if not exist "%PSM_LIB%" mkdir "%PSM_LIB%"
copy /y "%FP%.xml" "%PSM_LIB%\\%FP%.xml" >nul
copy /y "%FP%.dra" "%PSM_LIB%\\%FP%.dra" >nul
echo PSM: %PSM_LIB%\\%FP%.xml
echo PSM: %PSM_LIB%\\%FP%.dra
if exist "%FP%.psm" (
  copy /y "%FP%.psm" "%PSM_LIB%\\%FP%.psm" >nul
  echo PSM: %PSM_LIB%\\%FP%.psm
) else if exist "lfbga408_19x19.psm" (
  copy /y "lfbga408_19x19.psm" "%PSM_LIB%\\%FP%.psm" >nul
  echo PSM: %PSM_LIB%\\%FP%.psm
) else (
  echo WARN: .psm missing ^(create_sym may have failed; .dra/.xml still copied^)
  echo       Check lfbga408_19x19.log
)

echo.
echo Done. Work dir keeps originals; libs got copies; backup\\ is snapshot.
popd
pause
exit /b 0

:FAIL
echo.
echo FAILED. Check allegro.jrl
popd
pause
exit /b 1
"""
    path.write_text(content, encoding="ascii", errors="replace", newline="\r\n")


def main() -> None:
    balls = all_balls()
    print(f"balls={len(balls)} unique={len(set(balls))}")
    assert len(balls) == 408 and len(set(balls)) == 408

    WORK.mkdir(parents=True, exist_ok=True)
    PAD_LIB.mkdir(parents=True, exist_ok=True)
    PSM_LIB.mkdir(parents=True, exist_ok=True)
    SCRIPT_DIR.mkdir(parents=True, exist_ok=True)

    # clean date-named bats in work dir
    for f in WORK.glob("*.bat"):
        if f.name != f"{FP_NAME}.bat":
            try:
                f.unlink()
                print("removed old bat", f.name)
            except OSError:
                pass

    xml_path = WORK / f"{FP_NAME}.xml"
    bat_path = WORK / f"{FP_NAME}.bat"
    write_footprint_xml(xml_path, balls)
    if UL_BUILDER.exists():
        shutil.copy2(UL_BUILDER, WORK / "builder.ile")
    write_bat(bat_path)

    # also keep script + xml source copies for archive
    shutil.copy2(bat_path, SCRIPT_DIR / f"{FP_NAME}.bat")
    shutil.copy2(xml_path, SCRIPT_DIR / f"{FP_NAME}.xml")
    # footprint xml is ·â×°Ô´ ¡ª put into Psm lib now (before allegro run)
    shutil.copy2(xml_path, PSM_LIB / f"{FP_NAME}.xml")

    print("OK xml ", xml_path)
    print("OK bat ", bat_path)
    print("OK src ", PSM_LIB / f"{FP_NAME}.xml")
    print()
    print("Next: double-click")
    print(f"  {bat_path}")
    print("It will run Allegro then copy .pad -> 01Pad_lib, .dra/.psm -> 01Psm_lib")


if __name__ == "__main__":
    main()
