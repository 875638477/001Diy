# HI native execution guide (working record)

This directory contains training copies only. The project, public libraries, 01env, and previous G checkpoints are read-only inputs. All process cwd/TMP/TEMP/ALLEGRO_PCBENV and copied library files remain in this HI directory. Current board identity and actual partial-route inventory are in ../inventory/current_4L.json and current_2L.json.

## Native workflow
1. An engineering plan supplies explicit net/layer/points/widths, placements, rule changes, and acceptance intent. The runner does not choose an unrestricted whole-board autoroute.
2. Adapt source plans into ../batches with variant-specific class/CSet names. Keep all superseded plans and failures.
3. Compile with scripts/compile_batchHI_v12.py. All superseded compilers remain as history. Each batch snapshots its loaded helpers and generated program under source/batch_snapshots; readback v8 also snapshots helpers. Each native script uses documented Cadence 17.2 SKILL APIs.
4. Run scripts/launchHI_1800_path.py with an existing board, fresh log directory, and generated SCR. The launcher records PID/start/environment/script and source-board hashes. A process exit code alone is insufficient: inspect stdout errors, completion markers, DRC details, and endpoint proofs.
5. Run a separate --readonly process on the newly saved candidate. Use prepare_readbackHI_v12.py --plan ... --compiled ... to resolve named endpoints using actual geometry rather than volatile merged path IDs.
6. extract_checkpointHI_v4.py updates normalized actual copper, all 69-net physical-terminal connected components, and base net/class rule tables only after a clean readback. These base rules are not a coordinate-dependent effective-rule API; Region-Class and Class-Class rules and native DRC must also be checked.
7. Root and engineering agents independently review geometry, return paths, sensitive interfaces, and pending implementation limits. DRC zero or graph connectivity is not a product-release certificate.

## Preserved structure
Both boards retain 80 placed components, 69 named nets, 272 package pins (266 terminals on named nets and 6 NC pseudo-net pads), four mounting holes, the actual design outline, original padstack/mask apertures, fixed uppercase routing layers, and full 15/17 template Film definitions. The through drill structure is retained. Physical mask thickness rows remain absent.

2L rules were explicitly completed for all 69 nets in 17 classes across three domains, using the independent 2L profile rather than copying the 4L fine-neck limits. USB width/gap remains provisional manufacturing geometry and does not prove 90 ohm impedance.

## Completed operation pilots
- Native cline ripup/rebuild and single-segment delete/recreate; actual pin graph disconnect/reconnect; full transaction rollback.
- Native TOP-via-BOTTOM layer transition and nearby return-via creation; actual graph proof and rollback.
- Static shape creation with permanent void; actual copper/void point tests; rollback.
- Existing dynamic application-GND boundary binding and permanent-void edits on L2/L3; generated ETCH copper removed at test points, restored on rollback, source SHA unchanged and DRC zero.
- Local U2 SW neck challenge: tighten 1.2 mm to 1.0 mm, native Maximum Neck Length violation reports actual 1.15 mm; restoring 1.2 mm clears it without modifying the source checkpoint.

## Current partial-routing checkpoints
Baseline: 171 native remaining connections and independently 171 minimum physical-terminal joins.
First buck batch: 163 remaining on each board, 8/8 endpoint proofs, DRC zero.
Power 02d: 142 remaining on each board, 24/24 endpoint proofs, DRC zero after separate reopen. Four-layer board has actual L2 and L3 application GND fill. The two-layer board has actual BOTTOM application GND plus explicit TOP return bridges.
Power 03c:137 remaining. MCU6:112 remaining. USB8:96 remaining. Four-layer postcritical b010:63 remaining,58 vias,473 actual ETCH segments including generated thermals;68 batch endpoint proofs, fresh readonly zero DRC and stable SHA. Two-layer postcritical b010:62 remaining,58 vias,410 ETCH segments including generated thermals,7 actual GND polygons;68 batch endpoint proofs, fresh readonly zero DRC and stable SHA. The two-layer local TOP patches connect one additional ground terminal compared with four-layer. Current inventory JSON remains the authority for exact checkpoint identity.

The all-net route is still incomplete. See current inventory JSON for exact board SHA and current counts.

## Known pitfalls and scope
- Pin-center endpoints are used for demonstrated physical pin attachment. Earlier pad-edge-only trials could pass DRC yet fail the actual pin-connectivity graph.
- axlDBCreatePath may merge/split path objects. Do not retain path IDs across edits as durable endpoint identity.
- axlDBGetConnect returns flat or endpoint-nested lists by object kind; the graph walker handles both.
- Shape rectangles can be optimized to unsupported OpenShape objects; use actual closed open-shape API paths where required.
- Permanent edits to a dynamic fill belong on BOUNDARY, not generated ETCH. Update and inspect actual generated copper.
- CSet creation copies a template; it does not create a dynamically inherited parent relationship.
- Existing via soldermask figures are NULL on both sides (tented geometry). This does not certify fabrication filling, insulation, or assembly clearance under a connector.
- Older common readback helpers probe ETCH/L2 and ETCH/L3 on a 2L design and emit benign no-subclass warnings. They do not add routing layers.
- Desktop GUI operations remain untested because the native desktop control pipe is unavailable.

## Actual sensitive-ground negative test and final requirement
HSE local island, guard, local capacitor returns, all-layer application-GND permanent voids, and a single bridge via must be tested using actual connectivity. After deleting only the bridge via in a transaction, the local capacitor/guard/island graph must remain mutually connected but fail to reach global VSS or crystal case ground; global case/VSS connections must remain. Restore, update, DRC, and repeat after final pours and stitching vias. The test has been executed successfully on the actual MCU6, USB8 and postcritical island checkpoints, including after two-layer local TOP reference patches were created. It still must be repeated after all final routing, pours and stitching vias.


## Continuation on 2026-10-22
- USB8 uses real geometry to improve shared-pair coupling; connector-pair-only static electrical copy has explicit4mm phase/13.5mm uncoupled teaching budgets. Shared pair retains1mm/6mm, maximumvia2 unchanged. These are planar native length checks, not impedance or barrel-aware delay certification. Two-layer strict3mm phase and strict1mm shared-uncoupled challenge produced actual DRC and cleared on restoration.
- Original120s USB8 four-layer launcher returned while its owned process continued. The original launch record stays unchanged; an extended observation records completion without inventing an exit code. A subsequent independent readonly process exited0 with stable SHA and all proofs.
- Child-only PATH now prepends the existing Cadence tools/bin; bem2d resolves. This did not fix the many internal Field solution failed/default impedance/default propagation warnings. Those computed SI values are not accepted as valid engineering results.
- A documented axlDBControl drcEnable pilot deliberately forced an error, restored online DRC in unwindProtect, caught the real narrow-line DRC, rolled back and recovered zero DRC with source SHA unchanged. Compiler9 uses this controlled temporary assembly state, restores online checks unconditionally, then runs full axlDRCUpdate(t). Intermediate disabled states never count as acceptance.
- Readback/normalizer4 distinguish hand clines from generated thermal spokes using both line.thermal and parent path.thermal. Ordinary-route search may cross dynamic fill and regenerate it; it may not silently cross fixed ground bridges.
- Postcritical07b failed one actual Maximum Neck Length1.4654mm against overlapping old G31 limit1.4mm.07c advances the geometric flare to36.952,25.222, planned neck1.397508801mm, and retains all existing G31/global rules. New scoped ground CSet limit is also1.4mm. The failed candidate remains in native/logs.
- Two-layer GPIO reference patches are dynamic actual copper, with permanent geometry clipped against the HSE application moat. Their region outlines do not prove continuous return copper. Fresh readback samples actual generated or static ETCH shapes and actual voids at at most0.1mm centerline spacing, separately reporting application and quiet ground. Sampling is geometric evidence only; field width, topology and transition return remain engineering reviews.
- Via-mask NULL does not prove the complete mounted assembly is insulated: the U4.5 VBUS land mask opening can expose part of an overlapping via annulus. Exact mask figures are in hi_usb_key_mask_apertures.tsv; manufacturing and assembly disposition remains open.


## Later continuation: explicit interim vs final validation
The2L b011 stitch at37.4,27.4 was first checked inside actual floating TOP copper and globally connected BOTTOM copper. After the actual via, the TOP fragment reached U1.23. The number of physical branches with no component terminal changed1->0. A repeated fresh full electrical recalculation ran for more than20minutes; its own process and child solver were identified and deliberately stopped after root coordination, with source SHA unchanged. Timeout, live-handle exit and safe termination records remain. A separate fresh geometric/connectivity read records storedDRC0 only. This is not a fresh full-check PASS.

Intermediate b012 now contains full four-wire external SPI on both boards, two-layer coplanar return guards and reviewed prefilter ripup/rebuild.2L has58 remaining terminal joins/76 vias;4L59 joins/68 vias. Native build explicitly requested all on-plus-batch checks and returned numeric0; source-to-J6 and all new GND return/guard graphs plus HSE negative passed. Later fresh reads deliberately inspect geometry, branches, rules and storedDRC only. Final whole-board full fresh checking is still mandatory.

Private small mechanically drilled via binary HI_VIA026_C052_TENT is in the task library:0.26mm plated drill,0.52mm regular copper,0.13mm nominal annular ring, NULL masks/anti/thermal; positive dynamic-plane assumptions retained. Both actual2L and4L pad definitions were read back without writing the boards or changing their approved-via rules. The earlier21-character prepared name was shortened to19 before import because official PADLIB loader documentation specifies20characters. It is not a laser microvia or blanket fabrication approval.

Exact deleteVia now matches net+coordinate+padstack uniquely, checks the removed count and preserves every other via signature. Its native transaction pilot deleted only the old PC14 via68->67 and restored68 plus U1.3 graph reachability on rollback, with source SHA stable. The first pilot lacked the gComponent helper dependency and failed before deletion; that failure remains. Approved-via JSON lists are adapted to the officially required colon-separated physical vias string.

Mechanical-pin geometry must not omit empty pin numbers: explicit current reads found six NPTH, including J2's two0.65mm locating holes and four2.0mm mounting holes. Native drill/placement/pad-type evidence is separate from272 electrical package pins; native DEFAULT hole spacing values are raw rules rather than a claimed resolved pairwise clearance. The earlier geometry helper omission is recorded and future reads include all mechanical pins.


## Auxiliary batch b014 and via approval pilots (2026-10-22)
The current intermediate actual boards are HI_2L_USB_aux_2L_b014.brd (45joins/36nets,86vias) and HI_4L_USB_aux_4L_b014.brd (46joins/36nets,77vias). Both build programs restored online DRC, requested the fullboard update and received numeric0; actual control/CC/VBUS endpoints, added APP-GND returns and old-anchor HSE graph negative passed. Independent readonly reopens preserve SHA and record storedDRC0/zero terminal-free native branches only. Final full fresh wholeboard checks remain pending.

The first auxiliary b013 attempt was not saved: restored rules revealed three GND neck violations, a real J2 rectangular route-keepout collision and two CC1 gaps governed by a conservative overlapping region. The approved geometric correction uses .6 normal GND copper, moves VBUS around the real rectangle, and changes only the already-finite old J2 source CSet line_line .5->.2. New CC1 finite rules were challenged using the official USB_CC1-only axlDRCItem: strict .4 caught actual .3, restore .2 returned0; the following fullboard build update independently returned0. Full update took126seconds on2L and7seconds on4L; many field-solution failures remain, so no impedance or timing certification is inferred.

An inbuild no-other-field assertion initially used unsupported GetSpacing constraint symbol all and returned nil, causing an empty comparison. That assertion is not accepted evidence. Complete native spacing tables before/after were compared independently:5445 old values, only TOP/BOTTOM line_line of HI_USB_J2_SOURCE_S_2L changed .5->.2. The helper now uses documented nil for all fields and rejects empty snapshots. Evidence: review/USB_aux_2L_b014_spacing_diff.json. The old failure and helpers remain immutable in their batch snapshots.

Normalizer5 retains exact native ROUTE KEEPOUT polygons and all six embedded mechanical pins, including empty-number J2 holes. Electrical pin counts remain separate. A generator first-line encoding failure occurred before any native readback launch; ASCII-first-line generator3 completed the reopens.

Private throughvia approval was actually challenged on both boards in unsaved transactions. A TOP-only region left3 unapproved layers on4L/1 on2L; extending only the via-approval region to all actual copper layers yielded inside0 while outside remained4/2 Via List DRC. Transaction rollback restored77/86 original vias and unchanged global L28-only approval/SHA. This is rule-API proof, not completion of the pending dense-source fanout. Spacing/neck exceptions must retain their explicit outer-layer scopes and inner allowetch must remain unchanged. Evidence: review/private_via_local_approval_pilots.json.


## Stable cumulative physical-pin contracts
Current b014 native-connected physical-pin components were converted into must-preserve refdes.pin edge contracts:152positive edges on2L,151 on4L. A separate immutable identity contract checks all272 electrical packagepins,266 real-net assignments and6 NC pseudo-net pins, plus the embedded padstack name. Two explicitly authorized readonly native runs verified every identity and baseline edge with unchanged source SHA; no coordinates/old via aliases are used as persistent proof identities. Source moves/ripups must preserve these edges and add new planned critical endpoints. Final complete-routing contract has197 spanning physical-pin edges across all69nets and is not asserted on current partial boards. Evidence: review/cumulative_physical_pin_contract_b014_validation.json and immutable logs/cumulative_pin_contract_*_b014.

An automatic-review scope rejection initially prevented even the proposed readonly runs because an earlier compile-only instruction was interpreted broadly. No process started. The parent explicitly clarified that compile-only covered unapproved SOURCE new copper and authorized only these two existing-board readonly checks; the scoped retry was approved. The rejection/clarification is retained in review/read_only_validation_authorization_20261022.json. No user confirmation was requested.

## b016 当前已保存且独立重开（2026-10-22）

本节只冻结本批实际几何、物理端点、规则差异及 scoped 检查，不代表整板13课已全部完成。两个合格 current 别名仍为 b014，后续只对显式 DRC_PENDING 快照重基。

| 变体 | 当前新候选板 | 板 SHA256 | 实际铜段（manual + generated thermal） | via / 实际铜多边形 | 累计 native proof |
| --- | --- | --- | --- | --- | --- |
| 2L | native_candidates/HI_2L_clearance_remaining_b016_DRC_PENDING.brd | 4AC553CF77DA21A3BA7E2B4E9142DDE1707571B7E4A80B17FCA975C46876D6A5 | 788 = 731 + 57 | 153 / 8 | 304 |
| 4L | native_candidates/HI_4L_clearance_remaining_b016_DRC_PENDING.brd | FD5D93BED7E64FEF14CEBB17FF103443FA29E0CEDF60EEA26B79D9F8D091B1B7 | 837 = 709 + 128 | 143 / 3 | 299 |

两板均保69net、266有网终端+6NC、272实际电气pin身份、172个b015原已连接物理pin边；现剩16个连接/14网（13GPIO与GND3），整板 DRCPENDING 未解除。2L18个普通网 scoped 0；4L15个普通网 scoped 0，fresh再独立PB1/PB10 scoped 0。两板均完成有限SMT字段严格.4→真违规→恢复.2/全部字段相同/正常0，以及quiet唯一anchor负测试。原native modes及主DRC开关t保留。fresh只读重新验证全部身份/证明与源SHA；raw stored0单独列为取证，不是fresh全板重算0。

后续真实修复包含：两板保留误判live R27 feed；J2普通.6地线显式延至真实SH1/SH2 pin中心，原孔内偏置终点未连接的失败保持；南PB12—15八段无硬件终端教学尾线精删，四个虚拟端点证明透明退役至原真实sourcevia，任何实际pin合同不删。2L WEST返回自然恢复，工程审查过的额外WEST桥/孔方案未使用。2L PB15 BOTTOM现存privatevia原缺许可，单.02mm点框复制实际P006只增via-list，其余字段不动；PB1/PB10重叠区域由实际native检查0证实，静态resolver不猜父。

2L剩J2.SH2孤片由一条真实TOP GND .6铜桥(44.32,6.78)→已共地SH4(44.32,2.6)修复，无新增via、无PIN_SHORT或内部金属假设。旧C1.2↔SH2及左右dataGND↔shell↔C10.2、所有新返回均实际通过。2L唯一terminal-free对象仍为旧generated TOP GND岛，最终TOP母边界替换后必须消失或真接地；4L无terminal-free分量。

正式只读输入/后续规划入口：inventory/checkpoints/clearance_{2L,4L}_b016_DRC_PENDING。阶段报告review/b016_native_report.json；逐旧CSet/all-layer及新静态copy差异review/b016_constraint_field_diff.json；4个原2L母边界/永久void/thermal参数/相对priority复验review/b016_2L_reference_preservation.json；根纠正canonical02与实际已执行几何一一对应review/b016_corrected_canonical02_mapping.json。旧01及失败试次保原字节；跨机器复放使用纠正后的最终batch，不能直接重放已退役的01。

复放原生load顺序以source/batch_snapshots/clearance_remaining_2L_b016_DRC_PENDING_try12/inputs_manifest.json及四层try05对应文件为准；这些已冻结helper复制包含所需原始SKILL函数。标准可写工作副本必须新建，原板只作SHA保护，SaveAs只允许不存在的新candidate；官方axlKillDesign丢弃工作内存防fallback保存。不要用只读打开后试图SaveAs，17.2已实证不支持。

最终TOP候选仅只读重基并校验，无实际铺铜：plans/native_prepared/final_TOP_GND_b016_{v}_PREPARED.json；GPIO后须再次锁源SHA与母形/quietguard。NoGroundPlane官方文档研究未找到经验证PCB-DRC专用修复/禁用路径，未改env或关闭检查：review/NoGroundPlane_official_readonly_research.json。