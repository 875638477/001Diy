# Lesson 28: native two- and four-layer stackups

Full Chinese lesson: [complete note](../../notes/lesson28_stackup_20261019.md).

- Native boards: native/F28_2L.brd and native/F28_4L.brd.
- Actual specifications and public source hashes: specification.json.
- 402 independent checks: validation.json.
- Final primary readback: logs/reopen2_02 and logs/reopen4_02.
- Placed pins / holes / slots: logs/morebase01, logs/more2_01, logs/more4_01.
- Actual recognized design outline / keepin / keepout: logs/mechbase01, logs/mech2_01, logs/mech4_01.
- Copper film template input and immutable hashes: film_template_readonly.json.
- Final explicit film parameter files: native/copper_films_2_exact.il and 4_exact.il.
- Diagram from native readback: preview.svg / preview.png. Thin layers have a minimum display height.

Scope: native CAD stackup editing, native geometry and layer mapping, current DRC, independent new-process reopen.
The 1.6mm nominal order thickness and modeled thickness sums have separate meanings.
This directory is an isolated teaching example. Manufacturing release remains false:
2L inherited USB mask web is below the selected OSH minimum; connector stake length vs 1.6mm board/process is unresolved;
4L USB 90-ohm width/spacing is not qualified; reference plane pours and remaining component placement are future work.
The 0.30mm-hole / 0.60mm-pad GND via at (52,35) is a layer-mapping teaching instance.

Historical partial film settings and helper failures are retained in logs/scripts; final canonical lesson28.il loads exact film settings.
No shared library, 01env template, shortcut, global HOME, or original engineering board was edited.
All process TMP/TEMP/PCBENV/cwd and all newly created material are within 01AIEDA.
