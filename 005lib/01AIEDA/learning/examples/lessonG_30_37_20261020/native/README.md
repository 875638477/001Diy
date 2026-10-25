# G30-37 native workflow and evidence

Session folder follows the 2026-10-20 learning start date; work continued past local midnight. All generated source, logs, native process environment, library snapshots and intermediate boards remain in this folder under 01AIEDA.

This is a reproducible Cadence 17.2 S045 CLI/SKILL exercise. Native GUI menus and interactive mouse placement were not practised. The main Chinese learning record and course acceptance decisions are maintained by the parent task in learning/notes/lessonG_30_37_20261020.md.

## Frozen entry points

- [4L layout](../current/G_4L_LAYOUT_v1.brd): SHA256 2D4A146A61F92AE6459C9E855AB086ED47B42360409608D8A12E30BB7EA21526.
- [2L layout](../current/G_2L_LAYOUT_v1.brd): SHA256 FC411A509940E8727A8CB62D036324D1A63A60E042F9CC8AEAECE10C0425BE7D.
- [Native report](../review/native_final_report.json) has the machine-readable scope and limitations.
- [Native validation](../review/native_validation.json): 3657 checks, zero failures.
- New-process readonly records: logs/final_reopen_4L_01 and logs/final_reopen_2L_01.
- Root visualization inputs: inventory/normalized_actual_4L.json and normalized_actual_2L.json, explicitly bound to these final readonly snapshots.

Both boards contain all 80 placed components, 69 nets, 272 logical pins, 84 symbols including the four original mechanical holes, four real GND vias, zero current DRCs and zero out-of-date dynamic shapes. DRC zero applies to this partially routed layout, not complete electrical routing or product release.

Physical copper names remain TOP-L2-L3-BOTTOM and TOP-BOTTOM. Cross-section physical solder-mask rows remain absent. The 17/15 complete artwork film definitions and all native options remain exactly equal to the corrected input snapshots. Mask apertures in pad definitions are retained; these drawing classes are distinct from physical cross-section rows.

## Input preservation and actual geometry

source/input_manifest.json identifies the two original boards and helper sources. backups/G_4L_INPUT.brd and G_2L_INPUT.brd are immutable study inputs. Final validation rechecks both original source paths and snapshot hashes. Public libraries, 01env templates, original F boards and actual user engineering were not edited.

source/approved_placement_plan.json freezes the approved 80-coordinate plan. The same positions are used in both layer variants as a controlled comparison; this is not a claim that two independently optimized full layouts were designed.

inventory/inventory_4L.json and inventory_2L.json were produced by a fresh readonly native inventory before placement, including all 18 used package definitions loaded from an isolated library snapshot. Footprint origins cannot be assumed to be component centers. In particular, legacy 0603/0805 pin coordinates have offsets from their symbol anchors.

Native axlDBGetPad bbox already reflects actual pin rotation; its bbox is relative to the pin coordinate. Absolute pad bbox is that bbox translated by pin.xy, with no extra pin-angle rotation. Native PlaceBound geometry is already in board coordinates. Final snapshots export instance text origins/rotations separately, without changing library anchor conventions.

The actual package-height default does not certify an MPN height. The root engineering/geometry review checks avoidance of the restricted-height zone and records unresolved real heights.

## Native execution sequence

The launcher is scripts/launchG.py. It creates fresh log/tmp and log/pcbenv directories, sets TMP, TEMP and ALLEGRO_PCBENV there, uses that log directory as cwd, starts the native executable hidden and records PID/start/arguments/exit code/script SHA/input SHA. An exit code of zero is not sufficient: COMPLETE markers, native error text, actual readback and object counts are checked.

1. Readonly inventory: inventoryG.il calls the full inherited mechanical, layer, artwork, connectivity and constraint readers, then loads package definitions in memory without saving the source.
2. Placement: compile_placement.py emits explicit float-coordinate SKILL plans. gPlace in placementG.il uses axlDBCreateSymbol and refreshes the component cache before validating all80 placed symbols.
3. Reconciliation: reconcileG.il performs real axlTransformObject moves/rotations against the already placed checkpoint. The final approved C8/C9/C18 adjustments are recorded in logs/reconcile_*_02. native/G_4L_PLACEMENT_v3.brd and G_2L_PLACEMENT_v3.brd are independent DRC-zero placement checkpoints.
4. Transactional operations: operation_exercisesG_v3.il and logs/exercises_*_03 demonstrate single-symbol move, rotation, origin-Y alignment, actual direct generic-group translation and rollback. axlDBRefreshId is required before reading transformed group members. Both C13 and C14 move by +0.5,+0.5; all80 original poses and absence of the temporary group are verified after rollback. The input board hashes remain unchanged.
5. Local routes: local_loops05.il with local_copperG_v2.il builds six pin-to-cap paths and three cap-side GND vias. Each narrow section starts at the real MCU pin center, goes straight out along the pad axis, then fans away from the neighboring return pin before widening.
6. Real reference copper: axlDBCreateShape creates filled GND etch from the real route-keepin polygon. axlShapeChangeDynamicType and axlShapeDynamicUpdate generate native clearance voids and thermals. This is a real ETCH/L2 polygon on4L and ETCH/BOTTOM polygon on2L, not a drawing or net-labelled boundary. 4L L3 remains unpoured.
7. C16: finalG_v3.il adds the two short0.6mm bulk-cap branches to the C15 group. Native graph proofs cover both branches.
8. Challenges and freeze: challengesG_v2.il temporarily tightens the local rules, inserts a separate outside-region coupon, then restores settings and rolls back the coupon before saving current/G_*_LAYOUT_v1.brd.
9. Independent new-process readonly reopen: final_reopen_*_01.scr reruns native DRC, snapshot and actual graph proofs directly against current files. Frozen hashes remain stable.
10. Official techfile export/compare: export_tcfG.py exports each current board's technology to exports/G_*_RULES_v1.tcf, compares it back in report-only mode and verifies unchanged board hashes. Both compare logs state "No objects were updated." TCF does not replace native net/class/region mapping evidence or constitute a full DCF export.
11. validate_nativeG_final.py checks the final evidence without starting Cadence. Do not rerun earlier preparation scripts over archival filenames; use fresh tags and fresh log directories for further experiments.

A clean reproduction can use the isolated source boards, frozen plan and library snapshots with the explicit official functions above. Preserve the separate2L profile and keep intermediate placement checkpoints. The final saved files and original native logs are the evidence for this run; preparation scripts and failed attempts are retained to explain corrections.

## Real local circuits and their engineering meaning

Actual MCU/cap pairs are U1.24/23-C13, U1.36/35-C14 and U1.48/47-C15. TOP contains 27 manually created segments:11V3V3 and16GND. The normalized route inventory also contains64 reference-layer GND thermal segments; these are generated copper connections, not64 additional manually routed signals.

Each VSS pin has a direct short TOP connection to its own capacitor GND pad, with one cap-side via joining the actual GND reference. The native graph reaches that capacitor and the reference copper. This is a local high-frequency loop with a plane branch; graph reachability does not prove current direction or make the plane a mandatory series route.

All six U1-to-cap targets and both C15-to-C16 targets return targetReached=t after final readonly reopen. Four GND graph proofs reach actual filled reference copper. Three GND vias are added; one original teaching via is preserved. No LDO-to-three-group3V3 feed, switch-mode power, HSE, USB, analog or other full-board signal routing is claimed.

## Explicit local constraint exceptions

The original4L global physical/spacing/electrical CSet values are compared key-by-key and layer-by-layer and remain unchanged. GND's physical-domain class changes deliberately from NC_POWER_LV_P to a new G31_GND_P containing only GND. Its net-level P_GND_PLANE override remains. Spacing/electrical classes remain unchanged. There are28 netclasses instead of27, still207 memberships with every one of69 nets present once in each domain.

One G31_U1_ESCAPE region contains three separate rectangles on CONSTRAINT REGION/TOP:
- (34.2,23.5)-(36.5,25.5)
- (41.5,21.2)-(43.5,23.5)
- (43.5,28.5)-(45.8,30.5)

The4L spacing Region-Class table applies G31_PIN_ESCAPE to NC_POWER_LV_S. Its full values are copied from S_POWER_030, with only smdpin_line and line_line changed from0.30 to0.20mm. It is region-class scoped, not a per-pin property. Other class members such as V5/VDDA remain possible members of that class; the present geometry in these three regions is the relevant V3V3/GND escape.

Physical Region-Class tables use G31_POWER_ESCAPE copied from P_POWER_060 and G31_GND_ESCAPE copied from P_GND_PLANE, preserving distinct per-layer etch permissions. Only maximum neck length changes to1.4mm. axlCNSCreate copies the template values; it does not create a dynamically inherited parent link. Validation compares every copied key and layer with the named source template.

The native center-based narrow path measures1.3657mm. Its first0.6mm lies inside the MCU pad and the external narrow section is approximately0.7657mm. The local1.4mm budget is explicit; the original global1mm is not claimed to accept the whole center-based path. Normal width remains0.6mm, minimum narrow width0.25mm, and the approved via remains0.3mm drill/0.6mm copper.

The2L profile is independent: DEFAULT width/minimum neck0.2032mm and copper spacing0.16mm; only V3V3/GND have the G2L_* direct physical and spacing overrides,0.6mm normal width/0.25mm neck/global neck1mm and spacing0.20mm. Two physical classes contain these two nets for the same local1.4mm neck Region-Class exceptions. The remaining67 nets have no per-net CSet override or netclass and remain under DEFAULT. Full2L power/signal classification is unfinished.2L needs no0.30-to0.20 spacing exception, and no4L inner-layer/USB profile is copied.

## Counterexamples and restoration

4L temporary local spacing0.30 generates30 native spacing DRCs whose source is G31_PIN_ESCAPE; restoring0.20 returns zero. Temporary local neck1mm generates12 native Maximum Neck Length DRCs at actual1.3657mm; restoring1.4 returns zero on both variants.

A separate temporary outside-region coupon produces genuine global spacing and maximum-neck errors:4L S_POWER_030 expects0.30mm at actual0.15mm, and P_POWER_060 expects1mm at actual1.2mm. The2L coupon uses its G2L rules and also fails outside the region. It is rolled back. Final reference polygon/void export and actual copper routes match their pre-challenge checkpoints exactly, and actual instance copper/mask pad exports match byte-for-byte. No challenge vias, routes or temporary setting changes remain.

## Failures retained and lessons

- First symbol creation succeeded in memory, but stale parent caches made component->symbol appear nil. Refreshing IDs before the postcondition fixed the check; no failed board was saved.
- Actual copper, including a non-netted NC pin, matters. C8-to-U3 gap0.1773mm violated0.2. Rotating C9 exposed gap0.1374mm to U3 NC pin4. Native moves corrected both, followed by DRC and actual-pin readback.
- Exact pad-edge starts, and then0.05mm overlap starts, could produce visually contacting copper and DRC zero while native pin connectivity was absent. Final paths use real pin-center attachment and an explicit local neck budget.
- An initial connectivity walker assumed every path-like object returned nested endpoint lists. Native results also included flat lists; the official result semantics are normalized before traversal.
- The generic group transform did move its children. Reading without refreshing the child cache created a false negative. A second trial applied another movement and its explicit postcondition failed; that uncommitted transaction was cancelled without saving. The final direct-transform exercise refreshes before reading and passes exact rollback.
- Optional post-save proof initially used wrong case axlCNSList and unsupported ClassTableFind option'all. The native bulk board had already saved DRC zero. Correct axlCnsList and'netclass are used in final fresh readonly proof.
- A restore assertion used a stale DRC list even after native DRC printed no errors. The final challenge code refreshes after each update before checking.
- Early validator failures were comparator errors: tuple-key GND classification, exact wording of the techfile log, and an overbroad comparison of auxiliary non-ETCH extraction lines. Their JSON attempts remain. The final route comparison is explicitly actual ETCH geometry; actual instance copper/mask pads are checked independently and exactly.

Official API text snapshots and hashes are in source/official_api. All failures are described as failures or reader errors, not omitted to inflate the final result.

## Limits and further work

Native DRC checks the current partial design. It does not certify the unfinished whole-board route, true component heights, selected assembly population, USB90ohm geometry, thermal/current capacity, final return-path continuity, EMI performance or manufacturing output. There was no independent SI/PI waveform simulation. Actual masks and complete films are retained, including the original template's known invalid-reference filtering and REFDES-silkscreen coverage limitations; this exercise does not certify production CAM content.

The parent engineering records, actual-geometry images and independent MCU/power reviews form additional evidence, each with its own manifest. This native manifest intentionally excludes those concurrently authored files to avoid false hash closures.
