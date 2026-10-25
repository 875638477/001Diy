# Native Allegro dependency inventory batch 01 incident

2026-10-19 Asia/Shanghai, 10:43:43–10:43:45. Owned Allegro PID 9472; actual exitCode 3. Batch stdout in `../dependency_load01_cli/stdout.txt`; launched arguments/PID/times in `launch.json`; original generated script in `failed_generated.il`.

The initial generated SKILL source omitted a closing parenthesis for each nested pin loop. Allegro's reader reported unclosed parentheses and inserted closing parentheses at EOF. `errset` allowed a partially interpreted function to run, and the process saved a coupon board before an abnormal exit wrote `allegro_S04517.2_AllegroMiniDump.dmp` and a recovery SAV. The malformed source and failed board are excluded from all acceptance results. Exact internal cause of the final native exception is not proven from the dump; do not infer that a saved file means a successful native run.

The initial path is retired; its dump, BRD and SAV were moved here within the learning root. No Windows exception/debugger settings were changed. No unknown native APIs or Capture GUI calls were involved. The corrected source closed every loop, batch 02 ended normally with exitCode 0, and the final selected 19 package symbols loaded in a fresh board using only the isolated library, saved normally, and reopened in a separate readonly process normally. The final TSVs compare exactly; 717 independent checks pass. Final delivery is `examples/de_15_26_20261019/dependencies_verified.brd`, not either initial coupon.

Future generated SKILL is checked for balanced parentheses and terminated strings before native startup, in addition to native exit codes, COMPLETE markers, saved artifacts and fresh-process reopen verification.
