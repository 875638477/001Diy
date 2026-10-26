# PCB 公共库迁移：可复用的原生验证方法

此记录是方法和检查依据。工程、候选板和大体积原生转储保存在 LGA1700 的 13 版工作目录，不作为公共教学库的设计文件。最终板须以主记录发布清单为准。

## 库选择与命名

同类同尺寸的常规电容、电阻、磁珠、电感使用一个 `_pc` 标准。优先从本工程无杂乱后缀的标准封装建立新公共名称，避免为了复用“同名但不同几何”的旧公共文件而大范围改变板上焊盘中心。特殊采样短接、保险丝不按原理图图形类别误合并。

不同直径、极距等真实尺寸保留可解释的尺寸名；不能用简单字符串去后缀替代完整几何审计。电解电容的高度若没有原始证据，不从二维封装推定。

PSM/DRA 的名字、文件字节和引脚数量都不足以证明等价。需要原生加载后逐对象导出完整 pad、孔、层、图形、丝印、装配、机械、文字字体、图形属性，并绑定每个 PAD 的完整原生 XML。135 个同名 PAD 完全等价、3 个过孔有真实差异的本案例表明：同名公共库不能盲目覆盖。

## 可重复的原生审计

1. 对输入板、源库、原公共库制作 SHA-256 清单，运行后再次核对；所有工作用独立新目录和自有副本。
2. 私有与公共 PSM 分开在空板中加载。空板不能预先带同名缓存。加载名称用唯一别名或明确当前 public-only PSMPATH/PADPATH，防止误读板内旧缓存。
3. 库加载和实际 PCB 缓存审计要使用相同铜层上下文。本例 2 层空板每 padstack 导出 12 个派生 pad，实际 4 铜层导出 18 个；TOP/L2/L3/BOTTOM 四层空板才可直接完整比较。
4. `textBlock` 的数字槽位是数据库内索引，不可跨板直接比较；应按该字体块的完整尺寸、字宽、笔宽、间距等数据建立指纹。仍严格比较完整字体块，不能全局忽略文字属性。
5. 每一轮都重新导出“当前板实际缓存”的 81 个 definition。外部文件已验证，不表示当前板旧缓存已更新。本例 68 个旧缓存缺少公共库新增的 PLACE_BOUND，13 个新名缓存完整一致；只去掉 PLACE_BOUND 后相同可用于诊断，不能作为最终通过依据。
6. 已布线板采用逐 ref 的 axlAltSymbolReplace 迁移实际封装，保留原实际连接对象。先逐项核对既有实例文字、位置、姿态、全部pad及连接，再在新封装身份就绪后同步逻辑Package；不把全板Always或缓存刷新调用本身当作连接保持证明。同名缓存的axlRefreshSymbol只能在明确范围和完整读回下使用。批量symbol／mask操作使用axlDBCloak的shape范围，并按每100个目标建立检查点；不默认传text／fanout、不全局忽略FIXED。修改后刷新父symbol及children再读回。

## ECO、文本缓存与网表

netrev -y1为Always，-y2为IfSame。Always虽然保留元件位置，却会重建连通路径。在本原板存在跨网线端的情况下，候选出现4个旧分区拆分和4个新分区合并，已被严格连接分区比较拒绝。这是失败方案，不能照此对已布线板大批量重建路径；对应失败板和报告保留，不改成PASS。

正确顺序是先按冻结映射逐ref执行axlAltSymbolReplace，保留既有实际连接对象，再用新PST、netrev -y2同步逻辑Package。本轮910个物理件逐ref替换已执行；继而IfSame逻辑同步约2秒完成。相对源板2020个连接分区逐项核验，其余既有连接成员保持，剩SC37因标准pad改变造成的一个GND孤脚待局部修复和复验。不能只因分区总数接近或日志为0便放行。若尚未先替换实际封装，直接IfSame曾静默取消放置改名器件；每轮都必须核全部组件存在、放置、姿态、pad和网络。

保存原始所有实例文字的内容、位置、旋转、镜像、对齐、层、字体块、属性。新模板标注不能覆盖原来调整过的板上文字。创建或移动文字后必须axlDBRefreshId(parentSymbol)，再刷新子对象、读取symbol的children；未刷新父缓存会让新建文字看似缺失。批量symbol／mask更新使用axlDBCloak的shape范围、每100个目标检查点和完整阶段报告；执行效率措施不替代实际铜／连接验证。

实际数量是6521个物理pad对象。逐对象匹配须保留带类型身份、位号、脚号、原／批准位置、重复出现序号及未使用对象，不能用(ref,pin)字典丢掉重复编号／无编号pad。源板包含27个nil机械pad及749个net对象存在但name为空字符串的引脚；两种状态独立编码，空字符串也不能直接解释为电气NoConnect标记。完整有序导出和连接图均保留这些对象，不按“无网”过滤。

## 铜、线路与电气连接

原生紧凑导出须打开sstatus(fullPrecision t)，源和目标用同一脚本。不能把高精度目标坐标舍入来强行通过。

网表更新可能反转线段端点、合并共线段或拆分路径容器。使用Decimal到Fraction的精确有理数，把同层、同线宽、同其余属性的共线段转换为投影区间并比较完整并集，不使用坐标容差。路径容器bbox／nSegs可以派生变化，但须递归导出全部子段，保证没有丢弃容器的独立几何属性。弧、过孔、外形、铜边界、文字等其它对象保留完整多重集。

逻辑网表相同、所有线路／铜并集相同，仍不能代替axlDBGetConnect的完整实际连接分区和邻接。应比较源板、无封装变化的netrev control及候选，核每个有类型身份的pad、重复成员、实际路径两端和逐pin网络；分区数量相同也不能代替完整成员集合相同。本轮Always失败正是这个门禁检出了新增split／merge。

标准pad变大且覆盖旧线端，不表示数据库附着点自动连到新pad。本轮SC37留下的GND孤脚拟补一条长20mil、宽2.5mil、完全位于新pad内部的stub；这是明确的局部电气修复，不能因为铜并集不变而省略记录。写入本阶段说明时该stub仍在处理，须保存并新进程重开，再核全部6521物理pad、GetConnect分区／邻接、各pin网络、铜和规则后才能关闭；本文不提前宣称完成或最终出版。

动态铜使用原生polygon布尔比较，包括孔洞和弧。先报告所有差异，再按实际批准的pad改动限制局部差异；不可全局忽略generated shape，也不可只用区域框掩盖其它铜变化。
## 再次导出库：实际81定义与历史目录残留

File→Export→Libraries的实际命令是dlib。官方文档描述导出设计内全部元素；独立dump_libraries的-a是全部Package符号，不是仅按已放置器件名生成清单。保证旧C/R封装不再导出，必须枚举保存并独立重开后的全部设计symdefs，再实际导库核对。不能只根据1066个已放置symbol推断板内没有unused旧定义。

本轮候选在独立新目录w/export_final13运行官方dump_libraries.exe -ac，原生exit_code=0、dump_libraries.log报0错误，导出81个PSM、81个DRA及126个PAD依赖。PSM和DRA的casefold stem分别与w/polys_final_alt13/ALL_PACKAGE_DEFINITIONS.tsv中的全部81定义精确相等；81个定义全部usedCount>0，实例数合计1066。C／R＋尺寸的名字严格为对应唯一_pc，旧无后缀、PP、frame、line或数字后缀数量为0。

独立比对报告在工程verification/package_export13/PACKAGE_EXPORT_NAME_VERIFICATION.json；162个PSM／DRA文件SHA及原生作业／源板绑定在同目录EXPORTED_PACKAGE_FILE_SHA256.json。导出和定义读取两份launch_report都绑定同一候选板SHA：
49AF5EE7252CA9E8C4C48D8F60AD4D1113DA559814585356B14F6150A195C063。
两个输入副本及源板本身的SHA一致，输入均未修改。这个证据只关闭导出名称／全定义清单问题，11项铜皮差异仍另行调查，尚未正式发布；目录名中的final不表示工程已获最终放行。

安全复用步骤：

1. 全部symdefs按name、type、instances枚举，不能只取placed组件。若全部定义都已有实例，不做删除。
2. 官方说明unused symdefs会在保存、刷新等过程中清理；确需手动清时仅对冻结的未使用symdef调用axlDeleteObject。属性表使用instances，不能误删component／net或使用ripup。
3. 新建空输出目录并保护源板；dump_libraries.exe -ac可用于Package验证。该独立工具没有文档化-nographic参数；若用Allegro原生无图会话，可对单symdef调用axlWritePackageFile(symdefDbid outputDirectory)。
4. 比较完整PSM／DRA stem集合和源板SHA，保留日志与每个导出文件SHA。PAD／层叠完整内容仍需对应原生定义验证。
5. 不向公共库根目录或以前导出目录直接测试。官方导出会覆盖同名文件，但不删除这次未生成的旧文件；用户再次导出也应使用新空目录，以免误把旧C0402_3_1／R0402_PP残留当成当前板结果。

本地官方证据：C:/Program0/Cadence/SPB172/doc/dcoms/dchap.html#dlib（34503行起）；share/pcb/batchhelp/dump_libraries.txt；doc/algroskill/26logacc.html#1075894（axlWritePackageFile，2956行起）；doc/algroskill/03dbcre8.html#888504（保存时清unused，4408行及4439行手动删除）；doc/algroskill/02dbdesc.html#609305（Symdef.instances属性）。
## 规则与过孔依赖

未放置但仍在 VIA_LIST 规则里的 PAD 也是有效依赖。新增独立 `_pc` PAD 后，需要精确改对应规则 token，并保持其余完整 CFX/TCFX 内容。导入后必须重新导出比较；仅“导入返回成功”不够。Padstack 原生 XML 改名应只改 padstackname，再用官方工具重新生成、重导和逐字段比较，不能经过单位换算重建而引入舍入。

## 脚本格式与反例

Cadence 17.2 的 SKILL 文件使用 UTF-8 **无 BOM** 或纯 ASCII。Windows PowerShell 5 的 `Set-Content -Encoding UTF8` 会加 BOM，导致 `undefined variable - \\357\\273\\277`。使用 `[IO.File]::WriteAllText(path, text, [Text.UTF8Encoding]::new($false))` 写入，再检查前三字节。

本例完整缓存比较器的反例已验证：0.01mil 引脚中心变动、0.01mil 字体宽变动、L2 pad 边框变动、丢失整个 PLACE_BOUND 均被拒绝；仅数据库局部字体槽编号变化被接受。失败转储和失败报告保留，以免将“诊断性简化”误写成最终证据。
## 本案例已经验证的迁移次序

1. 对普通器件建立唯一公共 `_pc` 标准，并在独立空板加载公共库；同名旧公共资产保持原 SHA，不覆盖冲突定义。
2. 用 `axlAltSymbolReplace` 按逐 ref 冻结表替换现有符号，使用 shape cloak 和每 100 个组件 checkpoint。每个组件的原姿态、完整文字和批准引脚表即时检查。共 910 个组件已完成。
3. 全部实际 placed symbol 已变为新名以后，再以新 PST 执行 `netrev -y2` 同步逻辑 package 和 primitive。必须重新读回检查，不能把该步骤用于实际符号仍是旧名的板。
4. 对 SC37.1 新中心补 2.5mil TOP/GND、20mil 宽短线。它完全在新 pad 内，只用于恢复原数据库附着，不删除原线。
5. `attached_alt13` 候选原生读回已经证明：6521 个实际 pad 的连接分区恢复与源完全相同的 2020 组；所有原有手工线铜并集完整保持，仅多上述批准短线；5169 个其它非 owner 对象完整多重集相同。

本案例还发现：直接 `netrev -y1` 虽能保放置，仍在重组路径时改变 8 对 pin 的连接分区。其 pin 网络名、局部 pad、铜图形都可能看起来正确，且日志 0 error / warning，因此必须保留真实 GetConnect 分区门禁。该候选已拒绝，没有通过放宽 9 个网络状态差异来接受。

## 旧嵌入缓存的边界元数据

最终采用分层且明确的缓存检查：13 个新 `_pc` definition 必须与公共四铜层空板载入的完整 native graph 相同；其余 68 个保留完整源板缓存模型，与公共文件的唯一差异是源缓存原已缺少 PLACE_BOUND。全部 pad、孔、铜、丝印、机械、字体和其它属性都必须相同。68 个模型无非公共 LIBRARY_PATH；实际公共库搜索路径仍指向本机。

原来的“81 全部完整相同”失败记录保留，不能改写为 81 exact。尝试刷新全部 68 个 definition 只会给旧缓存增加本任务不需要的机械边界；单个 XTAL 原生 canary 成功，全 68 批次触发性能超时且没有输出被采用。没有为了消除诊断差异而改变现场机械模型。

源板缓存和私有磁盘库也做了独立闭环，不能用盘上 PSM 冒充实际源缓存：93 个实际旧 definition 的完整外层 native graph 与冻结的私有 PSM 相同；61 个 SMT definition 的 L2/L3 派生 pad 严格 NULL；其余所有非 NULL 内层 padstack 共 71 个出现、50 个独立定义，与公共四层 fixture 的完整 18 层 native graph 相同。由此排除“盘上定义正确、实际源缓存 pad 不同”的隐患。

以上是已通过候选的验证方法。正式文件位置及最终 CFX/TCFX、过孔规则、动态铜和公共索引发布结果以本案例最终发布记录为准。

## 实际端点在铜内但原生连接丢失

后续34个SOT23统一公共封装的真实案例，补充记录在[PCB_PAD_ATTACHMENT_REPAIR.md](PCB_PAD_ATTACHMENT_REPAIR.md)。新pad覆盖228个旧走线端点时，原生分区仍由2020变成2109；按源真实GetConnect路径端点补92条完全位于新pad铜内的短线后，新进程全部6521物理引脚、2020分区完整成员和1118网络状态恢复一致。重复同类迁移时应复用该源邻接、原生完整stroke差集、同网共线区间证明及新进程强门，不能直接套用92条这个项目数量。
