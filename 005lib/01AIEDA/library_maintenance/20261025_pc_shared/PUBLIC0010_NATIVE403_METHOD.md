# 公共 0010 模块的 403 件封装迁移方法与实际发现

本记录保留各阶段的真实失败与后续修复。2026-10-26 的最终私有候选 `07A0F934…0E82A42` 已独立通过全部 2698 个有类型 pad、原 915 个连接分区全部成员、593 个对象的姿态／文字／属性／字体、101 个实际 device body／class、完整四反馈视图和约束门。公共板替换、引用闭合与旧库退役另以发布回执为准。

源板为 `680500B0…09E1B898`，单位 millimeters、精度 4。原生完整源快照有 572 个逻辑元件、593 个物理 symbol、2698 个 pad。21 个没有位号的物理对象不能放进一个 nil 键；其中 10 个 pad、11 个零 pad 对象及其文本、属性、姿态都必须保留。

源只读 probe 已实际通过全 593／2698 有类型台账并导出 806 个待迁移 pad 的真实连接邻接。台账保留 native nil 与带引号空网络串、重复编号和机械／通孔标志；source806 证据绑定原板与完整公共库 guard，后续同源测试复用此证据，不反复运行原生源 probe。

第一版 Alt403 在首批安全失败，没有保存候选。第二版把 errset 放到 cloak 内逐位号输出阶段、实际与预期 pin、属性和文本，明确发现首件 C90 的 Alt 替换将底层实例变成顶层：源姿态 `((153.75 94.25) 270.0 t)`，Alt 后为 `((153.75 94.25) 270.0 nil)`；对应脚号位置上下反向。SPMHUT-48 的缩放四舍五入警告并不是这次失败的根因。两份失败证据保留，原板和全部 13433 个公共文件字节未变。

第三版先做独立 C90 canary。恢复顺序是：Alt 完成并刷新 DBID；若 isMirrored 与源不同，用 `axlTransformObject(symbol ?mirror t ?origin sourceXY)` 恢复原板面；刷新后仅按实际角差恢复原 rotation；要求完整 XY／rotation／mirror 与源精确相同；然后恢复原 owned text，核仅 C90 改封装的混合 2698 台账与全 593 对象文本、属性。Canary 只保存独立副本，没有 100 件 checkpoint；通过后才运行全 403 件。

此恢复方法已由本地官方接口文档支持，实际 canary／全量是否通过以各独立 RUN_RECEIPT 和 COMPLETE marker 为准，不能把脚本准备或语法检查当原生通过。官方说明见 `C:/Program0/cadence/SPB172/doc/algroskill/06intedt.html` 的 axlTransformObject：symbol 支持 mirror，`?mirror t` 同时做 X 方向镜像与 TOP／BOTTOM 跨层，`'GEOMETRY` 只镜像图形而不换层；顺序为 move、mirror、rotate，旋转角度为逆时针。不能用仅 GEOMETRY 的镜像代替恢复原板面。

全量 Alt 后仍须新网表 IfSame 同步逻辑 package，恢复／严比组件属性和完整 CFX，并在保存重开后核全部 2698 pad、593 symbol／文本、572 逻辑名称、真实 915 连接分区、源 path／symbolEtch／shape 的完整铜。源邻接导出同时展开 `shape->connect` 的实际本网 path 与 segments，避免只看 pin 中心或直接邻接而漏掉藏在 symbolEtch 里的铜桥。

实际进度：最初单件 canary 绕过公共 pc13Replace 初始化，我遗漏了显式 PSMPATH／PADPATH 设置，Alt 在变换前返回 nil；该次失败与镜像算法无关，保留其独立日志。第四版补上与正常全量相同的绝对公共路径初始化后，C90 canary 已原生通过（13.27 秒），镜像和角度恢复两步均执行，原姿态、两脚目标及全体混合 2698／593 文本属性门通过后才保存副本；源 680500 与全 13433 公共文件未变。全量 403 的结果仍需另以实际报告确认。

全量 v4 后续结果：403 件逐件姿态／pin／文字／属性门全部通过，保存后的全 2698 物理台账亦通过，但全工程文字门发现未改封装的 Y3、MN14 增加了 10 条 AUTOSILK_TOP 数字。完整 572 逻辑元件文字对比为原文字零丢失、零改变，只有 Y3 新增 3 条、MN14 新增 7 条；不能仅处理报错中的第一件 Y3。

独立原板 no-op SaveAs 已实际运行，全部 593 对象／572 元件／字体默认设置的前后快照字节完全相同。由此不能把这 10 条解释为“保存本来就会发生”的允许差异，也不能按 AUTOSILK 层名整体跳过。v6 的方法是精确恢复原全 593 文字与属性台账，保留已经完全相同的只读静态文字，只对实际变化对象修复，并在保存后和独立重开后再次完整比较；原来的 10 条不获得任何例外许可。实际恢复／新鲜读回结果另以各原生报告为准。

2026-10-26 实际 v6 保存和独立 fresh 读回均已通过。候选 `public0010_netrev_text_restore13/PUB0010_NETREV_RESTORED.brd` 的 SHA256 为 `008FEDC680EF5806D2C351CBF819F8A664D833D0A8D68D7A122306EE79C0A9AC`；`public0010_restored593_fresh_gate13/FULL593_RESTORED_FRESH_REVIEW.json` 独立完整比较全部 593 对象、572 元件／compdef 属性、全 owned text 多重集、使用字体定义与 21 个非逻辑对象，只逆转精确的 403 个允许定义名，9 种破坏反控全部拒绝。这一结果不批准实际连通和铜。

该候选的完整原生 GetConnect 显示实际连接分区从源 915 变成 1658，即使网表零错误、全 pad 网络名与位置正确也不代表原线路仍接在新 pad 上。必须按每个源真实 path 分支独立处理；同一 pin 可能有多个从 symbolEtch 间接连接的分支，不能每脚任取一个线端便宣称完成。完整 source806／target806 邻接已冻结 877 个实际源分支、4082 个真实线端候选及 2068 条源实际直线段。只读 native 全分支 preflight 得到 834 个可用分支、43 个失败分支（31 个 pin），743 个去重的可用 pad 内 stub；这只是可行性分类，没有创建线或保存。

进一步实际逐线归网诊断把 2068 条分成 1927 条唯一同几何同网原线、54 条唯一同几何但变成 native NIL 的原线，以及 87 条无完全相同线实体的记录。后者可能是并线、分段或实际铜依赖变化，不能直接叫作铜丢失，更不能按近似位置随意重建。源全部 1739 个 via 的 XY、pad 名与全部 user／allegro 属性保持，然而其中 9 个 via 的匿名源网在 IfSame 后变成 NO_NET。全 2698 pad 门无法发现这类 via 回归；必须保留 LonelyBranches 并逐 via 完整核验。

待执行的有界修复使用原板只读原生捕获 54 条原线及其父对象全部属性，并把 11 个原匿名网绑定到原／新 PST 完整相同的 ref-pin 节点。只允许这 54 个明确 NIL 对象通过新 stub 正面积接触来传播原网；新 stub 的完整实际 stroke 仍须在实际目标 REGULAR pad 内，原宽不足 0.127mm 时保留更窄原宽。非 NIL 异网、未知线实体和 143 个原空串 NC 脚不享受这个例外。不得把 PST 的 NC 占位符当共享电气网。

此修复仍是准备状态，不能据此记录迁移完成。执行后还要核全部 54 原线路归网与属性、1739 个 typed via、2068 条原线完整同网铜覆盖、2698 pad／593 对象、完整原 915 个连接分区的成员，以及全部约束。若旧线端装不进新 pad，仅可另外考虑实际源 REGULAR pad 铜的精确子集作 board-owned 旧 landing bridge：先用 native ANDNOT 证明来自源铜、再用 AND 证明没有新增跨网，公共 canonical footprint 不改。原板、公共库和失败证据始终保留。

后续实际执行状态：上述严格 v1 在创建前完整收集到 858 FIT、19 未通过分支，安全退出且没有保存。v2 只创建 766 条已经逐条 native 验证整 stroke 位于实际目标 pad 内的去重短段，保存为明确的 `PUB0010_PARTIAL_UNAPPROVED.brd`（SHA256 `1ABA0FDC27DE553535CDE454840EA245CBEBB5FDC1392A0B07E0218D11CDE26A`），没有把仍待处理的 19 分支签作通过。新短段使全部 9 个 via 自动恢复原网；完整 1739 个 via 的 XY／pad／typed net／全部属性与原源逐行相同。54 条原 NIL 线中 4 条被 Allegro 自动并线，原线实体不再有同样两个端点，但其完整源同网铜均已覆盖；不能把实体合并等同于铜丢失。

该 partial 的实际全 2698 typed pad 和完整 GetConnect 分区已独立通过原 915 个分区的全部成员比较，0 split、0 merge；“先 split 再 merge、数量仍为 915”的破坏反控亦拒绝。原 2068 条线中仍有 25 条源 thermal 铜未全部覆盖；25 条涉及 1V／1V8／3V3，必须继续区分旧 regular pad 内的允许 land 制造变化与 pad 外的真实旧热连接铜，不能因为分区已经相同便省略制造铜审计。本记录不批准该 partial 为最终板。

partial 的实际四反馈视图已通过原 403 个 footprint 逆转和 674 个 FUNC_DES 同功能双射，其余完整字段、Value、所有 pin-net 和隐藏电源／NC 行不变；完整实际 101 个 device body／CLASS 也已通过。完整原源 DCFX／TCFX 所有规则、Origin、日期、revision、scope 和属性同样保留；唯一管理字段是原生双只读字典证明的 `MAX_FILENAME_VALUE` 字符串 `20624 → 20635`，及该完整属性从 Design 第 8 个位置移到第 1 个位置。有限逆转只针对这个精确 source／candidate SHA 和已观察值，6 个破坏反控拒绝，不放宽其它 metadata 或规则。

缓存完整核验已通过：partial 共 70 个缓存定义，其中新 6 个 canonical package 与其当前公库真实 PSM 字节别名在同一 mm4／10 层／完整 64 字体上下文中重新加载的新 definition 完整图逐字段相同；其它 64 个原缓存（包括零 pad 图框／机械对象）相对原源完整图、字体、STEP 与未知字段保持。原 69 个缓存中删除了 5 个旧标准名，新增 6 个标准名，所以成为 70。新 6 包只依赖 4 个独立 PAD；板内真实缓存通过官方导库及两边独立原生 XML 导出后，其完整制造字段精确物理相等，6 个反控拒绝。只有 3 个公库 PAD 原 mils2 与实际板 mm4 的 width／height 使用精确 0.0254 换算，未舍入；其它所有 XML 字段与顺序保留。64 个旧缓存中 60 个仅是原模块内部专用定义，未宣称已外置公库。

原生 cache miss 第一版失败是父 symdefs 集合未刷新导致立即查询新别名失败；返回的真实 definition 已是新 DBID。第二版直接使用 CreateSymbol 返回的 definition 确认新的唯一身份，并用完整包导出器导出其图及依赖；前后完整字体表逐字节相同。失败原始证据保持 FAIL。最终热连接铜恢复后的 board SHA 变化时，必须对最终 fresh 全 70 缓存、2698 pad／915 分区、593 文字与属性、全部制造铜、101 device body、四视图及完整 CFX 再按相同边界核验，不能直接沿用 partial 的结论。

2026-10-26 最终私有候选的实际结果：`public0010_original_thermal_restore_run13_v5_pending/PUB0010_ORIGINAL_THERMAL_UNAPPROVED.brd`，SHA256 `07A0F9340CBC89718BD586DEFCC270E299E24242C6AA7A6FA78973C220E82A42`。原板 21 条真实 thermal 路径以原几何重建后返回 24 个原生 path 对象；这不是重新设计散热盘，也没有复制旧尺寸 pad。独立原生布尔门证明三条源网络的 BOTTOM 铜满足“修改后铜 = 修改前铜 ∪ 原 21 条路径铜”，没有源外新增铜、没有原铜损失、没有异网新增重叠，1739 个 via 的原始位置／焊盘／网络／属性保持。有限铜证明及 14 项破坏反控见 `public0010_original_thermal_restore_run13_v5_pending/FINITE_ORIGINAL21_THERMAL_CU_REVIEW_V5.json`。

随后从已保存的 `07A0…` 独立只读重开，原生快照位于 `w/module0010_final_full28`。实际运行的离线门为：

- `public0010_final2698_partition_gate13_v4`：全 2698 个 pad 的类型、编号、网名、坐标、焊盘、机械／通孔标志及原 915 分区全部成员精确相同，0 split、0 merge；数量抵消的 split＋merge 反控拒绝。
- `public0010_final593_fresh_gate13_v1`：593 对象／572 元件的原姿态、owned text、全部 symbol／component／compdef 属性与使用字体相同，仅逆转 403 个冻结封装名；不允许额外 AUTOSILK。原板 no-op SaveAs 的文本／属性零变化控制仍作为依据。
- `public0010_final4views_gate13_v4`、`public0010_final_actual_body_gate13_v5`：403 封装和 674 个同源函数编号的完整逆转后，所有原始值、引脚／网、隐藏电源／NC、101 个实际 device body 与 class 精确保持。
- `public0010_final_bounded_cfx_gate13_v6`：完整 DCFX／TCFX 原规则、Origin、日期、revision、scope 与其余属性原样；唯一管理台账是原生只读 STRING 字典实测的 `MAX_FILENAME_VALUE` 从 `20624` 到 `20635`，以及该完整属性的外层位置变化。6 项破坏反控拒绝，未给其他管理字段设置白名单。
- `public0010_final_all70_cache_gate13_v2`：59 PACKAGE、6 MECHANICAL、5 FORMAT，共 70 个选定定义的完整图形／字体／STEP／未知字段通过；6 新标准包与同 mm4／10 层／64 字体上下文加载的公库实物一致，64 原定义完整保留，独立 4 个 PAD 的全制造 XML 证明仍精确成立。
- `w/module0010_final_full28/FRESH79_STRICT_TYPED_ID_BIJECTION_REVIEW_V3.json`：补核全部 79 个 symdef，其中另外 9 个是 SHAPE，不能凭 instances 为 nil 称作无依赖垃圾。全部 20080 个对象、43 个 textblock、554973 个递归值在明确 ID 双射下相同；只把原生重开后的 593 外部实例指针和唯一 design parent 做有类型的显式双射，其余字段、未知属性与图形不忽略，0 数值容差。实例语义由上述 593／2698 门绑定，design 语义由完整 CFX 门绑定。

以上证明针对该私有文件 SHA；文件名中的 UNAPPROVED 是阶段遗留标记，不代替发布流程。实际公共路径替换、发布后完整 guard 和全部库引用闭合，以单独发布回执为准。
