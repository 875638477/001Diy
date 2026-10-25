# JK native training artifacts

Read `native56_final_report.json` and `../../../notes/lessonJK_native56_20261022.md` before replay. Paths below are relative to the JK lesson root unless explicitly stated. These are training copies, not fabrication release. Existing output paths/tags deliberately refuse overwrite.

- Baseline full CAM: `run_native56_v6.py` historical run, outputs `exports/native_*_TRAINING_NOT_FOR_FAB`.
- J55: `prepare_j55_sources.py`, actual `j55_apply_core_v2.il`, `j55_outer.il`, `run_j55.py`; successful2L try06,4L try01, then separate readonly reopen. Original fingerprint's missing path segments is documented; actual route/role/CAM independent comparisons close manual-copper preservation.
- Corrected CAM: `run_j55_cam_serial.py`, launcher v7.
- Three separate text-review Films: `run_companion_serial.py`, launcher v8, generator boards only. Main15/17 mapping remains unchanged.
- Controlled unplaced ECO: `run_eco_replay.py`; read `eco/execute_plan.json` and native replay result. Never use these PSTs for routed HI/J55/newstack boards.
- Actual new layer functions: final `newstack.il`, successful `run_newstack_try03.py`, then `run_newstack_reopen.py`. L2 actual GND/L3 actual V3V3; old HSE disconnection contract retired. No L2 signal permission.
- Corrected nonempty reference/segment supplement: `native_segments_reader_v2.il` and `newstack_segments_read.scr`. Original empty sample is NOT_EVIDENCE and retained.
- Actual native VALUE exports and new-stack full CAM: `run_values_and_newstack_cam.py`, launcher v9 with official readonly mode for read jobs.

All runtime/environment/output paths must remain inside JK. No globalHOME/01env/public library changes. Independent unrelated user GUIs can coexist; never touch their process/window/files. Only one task-owned native process at a time, identity uses PID plus creation/executable/command/task path.
