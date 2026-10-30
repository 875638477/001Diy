# Capture 文字几何与可读性检查

此方法处理网络标签、跨页端口、电源名、器件位号和器件值的显示位置。先完成库去重、网格和符号原点调整，再从同一个已保存并重新打开的设计导出官方 XML、原生坐标表与文字表。保存后数据库 ID 可能重建，旧计划不能直接套到新设计。

与[库、网格和文字清理总流程](capture_cache_grid_text_cleanup.md)配合使用。有关原理图和 PCB 的电气验收，另见[网络文字布局规则](capture_netlabel_layout_rules.md)与[网表问题排查](capture_allegro_netlist_troubleshooting.md)。

库内容整理后还要核[缓存来源身份与实际复用](capture_cache_reuse_and_origin_rebase_xml.md)。新OLB内容相同不代表现有实例已指向它；旧来源路径可能让后续放置再生成重复缓存。来源重绑定应是单独白名单变换，配合完整库内容、默认值及不保存的原生放置小样核查。

## 文字不能只看数据库边框

缓存中的 `R.Normal` 等图形名可能同时来自多个 OLB，且官方保存重开可能改变缓存枚举顺序。构建预览必须按实例的 `pkgName + libName + GraphicName` 匹配缓存的包名、来源库和视图名，统一路径分隔符与大小写；不能用同名视图字典的最后一项覆盖前项。翻页端口和电源符号同样按符号类别、`symbolName`、`libName`匹配。同名符号可能有不同的图形或脚号注释。实际使用的来源缺失或不唯一时停止规划。原生仿射坐标正确不代表库图形来源已绑定正确，两项必须分别检查。

DisplayProp 的边框可能为零或标记 dirty。不能把它当作准确文字范围，也不能把 dirty 等同于没有碰撞。记录实际显示字符串、完整 LOGFONT、局部位置、旋转、水平对齐和所属对象，再用 Windows GDI 获取真实字形轮廓。字宽、正负字号、字符集、字体替换及缺字都必须保留或报告。

本机原厂 `orPrmDboStreamer.tcl` 的预览算法提供不同锚点：DisplayProp 使用 LEFT/TOP；Alias 的默认文字流使用 LEFT/BOTTOM。不能把两者都当作左上角。引脚名和脚号应按原厂引脚方向、Start/Hot、偏移与整体镜像旋转算法建模。此模型有原厂依据，仍应与 Capture 中的实际显示复核；导出预览不等于已经完成 GUI 像素核验。

普通 PartInst 的旋转/镜像也不能按 `O+RM(local)` 猜算：实际图元变换可能包含随库边框变化的 offset。应以同一保存版本每个实例 `GetOffsetGraphicPoint` 的三个基点构造原生仿射矩阵，见[原生坐标与缓存重基](capture_cache_reuse_and_origin_rebase_xml.md)。模型工具通过 `--part-frames <part_frames.tsv>` 读取；非零姿态缺少该表会停止，不再绘制一个看似合理但位置错误的符号。

旋转电源符号尤其要使用原生读回的绝对 hotspot 校准图形。仅把库局部图形按实例 loc/mirror/rotation 直接换算，可能出现图形与实际连接点分离。热点、针段和电气导线应逐一对齐验证。

## 避让次序与器件关联性

先保护真实导线、器件本体、引脚图形、可见针名脚号和其他显示文字，再选择显示属性的新位置。隐藏针号没有可见字形，不应凭空加一个数字文字障碍；针段本身仍是受保护图形。对于可见但零长度的特殊引脚，如果原生接口不暴露可靠的文字锚点，应按原厂最大偏移和真实字号建立保守范围，单列核查，保持引脚不动。

优先只改 DisplayProp 的局部偏移、明确的水平对齐或必要的显示旋转，保持器件图形、热点和导线不动。Alias 的电气锚点必须留在原所属 wire 上；可以沿原 wire 的网格点寻找清晰位置，不应把它移到空白处而脱离导线。

“没有文字交叠”只是条件之一。Value 移到很远、夹在其他网络标签间，仍会难以判断它属于哪个器件。限制属性移动距离，增加与自身器件及 RefDes 的关联性检查。搜索范围内无清楚且靠近的位置时，应保留待审项、检查局部冗余文字，避免无限扩大搜索或缩小字号。

## 冗余 Alias 的归并证据

先明确保留哪个可见标识。只有名称完全一致、原生编译的网 ID/网名一致，并且 Alias 所属 wire 与保留 Port hotspot 之间存在真实连续导线时，才进入可归并候选。最容易审核的是同一 owner wire 同时包含 Alias 坐标与 Port 绝对 hotspot。

跨多个 wire 时，逐段保存原生 wire ID、端点、junction 或真实端点连接计数；不能把中间交叉线、名字相似或距离较近当作连接。保留的标识必须仍清楚可读。远处用于追踪网络的重复标签可能有意义，不能仅按同名进行全局删除。

每次删除保留原 Alias XML、原始名称/坐标/父 wire、实际 net、保留对象、连续路径及局部图像。若只是解决局部器件值被挤远的问题，应限定受影响局部，不扩大成全工程重复标签清空。

## 只有必要时延长导线

无法在原 wire 上放清楚的独有长网名，才考虑延长真正空闲端。要求原生端点连接计数为一，没有针、端口、junction、NC 或其他附件；原有整段导线必须成为新段的子集。新增部分不得碰到其他导线、端子、图形或文字，端点仍在既定网格和页边距内。同步更新派生 WireBBox，并将端点与边框变化列入严格白名单。

这类动作会改变导线几何，必须独立原生保存重开和逐脚连接检查。参数化的默认候选工具不自动延线或删除 Alias。

## 参数化离线工具

工具位于 [capture_layout_tools](../scripts/capture_layout_tools/capture_layout_scene.py)，仅读官方 XML/原生 TSV 并生成模型、预览或计划，不启动 CAD，不写 DSN。需要 Windows GDI、Shapely 及其 NumPy 依赖；输出 PNG 时另需 PyMuPDF。通过 `--python-module-dir` 指定模块目录，可重复使用；也可使用 `CAPTURE_LAYOUT_PYTHON_MODULE_DIRS` 环境变量。没有固定工程路径。

非零器件姿态还需 `--part-frames <同版本原生仿射表>`；也可在原生坐标目录提供默认名 `part_frames.tsv`。必要输入为 `--xml <官方XML>`、`--native <原生坐标目录>`、`--text-native <原生文字目录>`、`--output <工程临时输出目录>`、`--grid <文档单位网格>`。`capture_layout_scene.py` 可用 `--render-all` 生成逐页 SVG，`--render-png` 另出 PNG。使用 `--page-filter <页名>` 可先核查局部；此时结果只覆盖该页。

[候选生成器](../scripts/capture_layout_tools/capture_layout_candidates.py)只生成显示属性位置或 Alias 沿原 wire 移动计划。`--max-property-displacement` 限制属性与当前器件的关联距离；无解项进入 `reviews.json`。计划仍需人工审核、严格 XML 差异白名单、官方导入保存重开及电气验收，不能直接把计划数量当作完成数量。

[几何辅助函数](../scripts/capture_layout_tools/layout_geometry.py)提供精确点在线段判断、原 wire 网格点、同 wire 同网同名证据及连续路径查找。返回证据不等于授权删除。字体缓存可由 `--font-cache <工程临时缓存>` 读取；只有明确加 `--write-font-cache` 才写出。这类轮廓缓存可很大，是可重新生成的中间物，不放学习库或最终交付包。

原生坐标目录需要同一保存版本的 `pins.tsv`、`page_grid.tsv`、`net_symbols.tsv`、`wires.tsv`、`aliases.tsv`；文字目录需要 `displayprops.tsv`、`part_pin_style.tsv`。字段由模型按名称读取；缺失、版本不一致或特殊未知对象必须先核实，不能把模型结果当作通用 DRC 结论。

## 验收与清理

保存重开可能合并共线导线，不能仅按 wire 对象数量判断丢线。[覆盖比较工具](../scripts/compare_capture_wire_coverage.py)读取前后官方 XML 和同版本原生 `wires.tsv`（`page/id/net_name`列），按页、网络、颜色、线型、线宽归一化整数共线区间，再精确比较覆盖；规划新增的 wire ID 必须由审核过的计划补齐网络映射。用 `--reference-xml`、`--candidate-xml`、`--reference-map`、`--candidate-map`和`--output <新JSON>`指定输入输出。此检查不能替代完整 PST 逐脚连接分区和结点检查。

最终以实际保存重开的 XML 和新原生坐标/字体再次建模。核查用户关心的网络/属性文字碰撞、器件关联性和所有页预览；正常针号与自身标准图形关系另列，不为消除模型交集而改电气符号。保留未知锚点的保守核查与限制说明。

核对所有非显示内容仅有明确授权的变化，并比较原生网表的逐 ref.pin 分区、网名、属性、封装和实例。若改过导线或删除冗余 Alias，更不能省略电气检查。完成后保留最终设计、参数化工具、轻量计划/证明、关键前后图及最终逐页预览；字体轮廓缓存、重复场景转储与过时候选预览在确认无进程使用后按清单清理。

交付逐页图可采用PNG加本地索引，不必同时复制全部大型SVG。若后续只改库来源身份，先证明完整变换白名单及原生重开后的实际图形、位置、字符串、字体和可见性均不变，再保存已核预览的SHA清单并复用；不能仅凭“只改了路径”的操作意图跳过验证。离线原厂预览模型、实际GUI像素和电气门禁各有独立状态。


自建库优先的转换见[共享模板流程](capture_user_library_first_templates.md)：先核真实材料／脚号，再共用图形，原生核有效继承及PST缓存脚名；短针距、H镜像热点和来源身份分别留证。另见[实例引脚覆盖限制](capture_generic_symbol_pin_override_limits.md)。
