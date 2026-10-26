# 公共封装别名退役前的实际引用闭合方法

本方法只读审计，不启动 CAD，不替换或删除设计、公库。退役必须等各设计的原生连接、铜、属性和完整约束验收通过之后执行。

## 1. 冻结来源，不能把计划中的零引用当成实际结果

源清单包含当前工程 DSN/BRD、37 个公共 OLB（包括 6 个位于子目录的 OLB）、2 个公共 DSN、7 个公共 BRD，共 48 个设计/库来源。另检查实际环境、启动配置及其启用的 replay 脚本和 devpath 设备文件。

每个来源绑定实际文件 SHA256、原生只读导出任务及其输出 SHA256。已发布的候选与正式文件字节相同，可复用该候选的完整原生导出；没有证据的来源必须标记 incomplete，不能计为零。DSN 内置 Design Cache、BRD 内置 symbol definitions 是必需设计内容，仍要检查，不能为消除库文件而删除。

## 2. 完整扫描八类实际引用

对每个旧 stem 明确输出八个非负整数：`project_capture`、`project_brd_declared`、`project_brd_placed`、`public_olb`、`public_dsn`、`public_brd_declared`、`public_brd_placed`、`active_device_map`。

- Capture XML：递归扫描所有 `pcbFootprint` 属性及完整 `PCB Footprint` UserProp，包括 Package/Cell 默认值、Cache 和实例覆盖。`FootprintName` 仅作为历史痕迹另列。官方 `olb.xsd` 中 `SymbolDisplayProp.Defn` 的 name/坐标是显示位置定义，没有 val；不能把它当成丢失属性值。真正 UserProp 缺 val 仍应失败。
- BRD：通过实际 `design.components` 检查所有逻辑 package，包括未放置器件；检查全部符号名称、definition 名称；直接通过 `design.symdefs` 检查所有保存的缓存定义，包括 unused 定义。保留重复行，不能用字典覆盖同名或空脚号对象。
- 路径及设备映射：检查工程生效环境、原环境中启用的脚本和实际 devpath 文本。准确列出的 937 份待退役 self-device TXT 单独核验 SHA、DEVICE HEADER 与 PACKAGE 相同，并与该轮精确删除清单绑定，不能误当成启用的独立映射。

本机路径大小写按 Windows 语义匹配。旧 stem 清单保留原始大小写，并以唯一 casefold 映射查询；不能遗漏 `fB0603`、`FB1206`、`L7050`。

## 3. 目标库须有实际 cold-native 与完整 PAD 证明

1067 个旧 stem 对应 127 个明确目标；裸尺寸等没有单一类别的旧名可以没有 target，但必须实际八类零引用，后续由元件类别选择 c/r/l/fb 标准。

逐目标校验当前公共 PSM SHA 等于实际 cold-native 输入 SHA，重新解析完整原生图，保留完整字段和几何指纹；逐实际 loaded PAD 绑定当前 PAD SHA 与完整原生 XML，重算铜、阻焊/锡膏、热焊盘/避让、钻孔/槽孔、孔符号和行为属性。完整 PAD 的 SHAPE/FLASH 名称不能擦掉后声称相等。实际相同字节的成员须有冻结 manifest 证明，不能凭名称或脚数推断。

本轮独立索引：`canonical_retirement_target127_v127/REQUIRED_CANONICAL_NATIVE_TARGET_INDEX.json`，127 个目标、154 个唯一 PAD 对象、411 份证据。25 个解析和破坏反控记录位于 `retirement_native_negative_controls27/RETIREMENT_NATIVE_NEGATIVE_CONTROLS.json`。

## 4. 可复用脚本与执行顺序

1. `tools/public_all_reference_inventory27.il` / `pub27AllReferenceInventory`：原生只读导出每个公共 BRD 的完整 components、symbols、symdefs 和完成计数。
2. `tools/run_public7_reference_inventory27.py`：顺序执行原生只读清单；可选择板，但前后保护完整 7 板 SHA。原生进程由任务主控制者运行。
3. `tools/build_retirement_sources_manifest_v3_27.py`：冻结原生实际源清单。预检可保留待发布板 incomplete。
4. `tools/verify_retirement_canonical_targets27.py`：生成 127 目标完整图/PAD 索引；`verify_retirement_canonical_targets_v2_27.py` 可重新校验该索引与当前 guard。
5. `tools/complete_retirement_four_brd_sources27.py`：四块公共板原生验收、原件 ZIP、原子发布均成功后，只替换清单中的四条 pending 来源及 guard/state。须证明其它 44 来源、环境配置与目标证明没有变化。
6. `tools/scan_retirement_native_references_final27.py`：实际扫描；预检使用 `--preflight`，最终不加。唯有完整源覆盖、1067×8 全零、完整目标证明通过，才输出 `PASS_NATIVE_REFERENCE_CLOSURE`。

四块最终板 inventory map 使用以下 stem 键：`00012`、`0010`、`006`、`008`，值为各自最终原生只读目录。最终清单必须绑定原子发布后的新 guard；不允许重新扫描建立一份新 guard 来掩盖未授权的库改动。

最终 closure 交给精确退役器；只有清单内的 PSM/DRA/self-device TXT 可删除，PAD/SHAPE、原件 ZIP、脚本和关键记录继续保留。审计失败报告与中间试验保留为校验记录，不能覆盖失败记录以表示通过。

## 本轮实际闭合结果

四块公共 BRD 已由原子发布器发布，回执位于 `public_four_final_native_published28/PUBLISH_RECEIPT.json`。发布后公共 guard 为 `public_four_final_native_published28/PUBLIC_GUARD_AFTER_EXACT4_BRD.json`，SHA256 `C2835B5651C473873A8664AC68520E32795B3D09E8BBF0134AE5BA13BA6DBBEC`。

最终来源清单位于 `final_retirement_source_completion28/completed/FINAL_NATIVE_REFERENCE_SOURCES.json`，SHA256 `81D2ABBB532540323D833AB09C96A469AD434938F59FB5B581552CED8FEA1079`；同目录的 `FOUR_SOURCE_COMPLETION_LEDGER.json` 证明只补入四条最终板记录，其它 44 来源及配置/目标证明不变。

最终实际报告 `final_native_reference_closure28/NATIVE_REFERENCE_CLOSURE.json` 状态为 `PASS_NATIVE_REFERENCE_CLOSURE`，SHA256 `8EA5E5694F18B663FE2D32B30FCB6128F8C7FD8A6F6465F818FA91F9BBABCDEC`。1067 个旧 stem 的八类计数全部为明确整数零；48 个来源、1065 项证据、127 个目标和 154 个唯一 PAD XML 对象均已实际核验。0010 的全部 79 个保存缓存定义（70 used、9 unused）已覆盖，不以 70 个已使用定义代替全库。

以上是退役前的实际闭合验收；删除操作及保留文件不变检查由精确退役器另外生成回执，不能用本报告代替删除回执。

## 精确退役及只读后验完成

`public_retirement_all_confirmed_stage13_v2/APPLY_RECEIPT.json` 已实际通过，SHA256 `2085916124315EBAB13143F2F9E2A76CC8A777238BC575AAA05E26C1303A8607`。1067 个旧 stem 对应的 3069 个明确 PSM/DRA/self-device TXT 目录项已删除，其余六根的 10364 份文件逐 SHA/大小不变；2 个备份 ZIP 的 3103 个成员全部重新读取并核对，原件字节可恢复。

原退役进程已经记录完 START+3069 条删除日志，后验循环因在每个旧文件条目内重复构造 3069 个 resolved path 的集合而出现平方级开销。仅停止该已确认的进程；`tools/resume_retirement_readonly_postcheck28.py` 随后只做完整日志双射、已删条目不存在、剩余文件不变、备份 roundtrip 和 1065 项实际证据复核，补齐缺失的最终回执，未再次删除任何文件。独立记录位于同目录 `READONLY_RESUMED_POSTCHECK.json`。

复用时应在循环外一次构造删除键集合，再用冻结 guard 减该集合得到预期。已完成删除但缺最终回执时，不得重跑 `plan_assets`/`apply`，也不能单凭日志条数宣称通过；必须完成上述只读后验。

?????? `retire_exact_public_assets_v3.py`?SHA256 `20714E6D3E4DADC3BE769365B8F5ABDBE960AAE70B1DA547BCA21DAEF1D7E300`???????????????????????????????????? v2 ???v3 ???????????????????????????????? `tools/verify_post_retirement_and_index_v2_28.py` ???
