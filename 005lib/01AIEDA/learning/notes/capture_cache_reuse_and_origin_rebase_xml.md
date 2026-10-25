# Capture 缓存复用、符号原点重基与 XML 严格验收

适用范围：Capture 17.2 官方 XML 导入/导出工作流。工具只分析或生成新的 XML，不启动 Capture、不直接写 DSN/OLB。项目 XML、合并计划、查询数据、截图和报告放在项目目录；本学习库只保存参数化方法、代码和合成反测。

工具目录：[scripts/capture_xml_tools](../scripts/capture_xml_tools)。所有 Python 工具只依赖标准库，先使用 --help 查看参数。它们支持的是当前明确列出的 XML 图元及引用形式，遇到未知坐标框架、继承歧义或结构差异会停止；不能当作任意版本 Capture 的通用转换器。

## 先导出数据，再决定哪些缓存可以合并

原生单进程打开独立副本，导出官方完整 DSN XML，以及缓存 Package/Device、全部有序 Pin 映射、共享脚与可见性标志、图元和实例引用表。锁定 DSN/XML 的 SHA；基线先做一次不修改 XML 的原生往返，保存并在新进程重开，重新导出 XML、PST255 与有效属性。

运行：

~~~powershell
python cache_inventory.py --xml source.xml --out cache_audit
python build_merge_plan.py --audit cache_audit --mode strict --output strict_plan.json
python cache_merge_strict.py --input source.xml --output strict_candidate.xml --plan strict_plan.json
~~~

cache_inventory.py 比较完整 Package 子树，保留所有子节点顺序，尤其是位置索引、PhysicalPart 脚号映射、设备顺序、Normal/Convert view、隐藏/共享/电气脚类型、字体、线条、填充、图形、PCB Footprint 和未知字段。身份归一化只去掉明确的包名、来源路径、时间戳，并对 CellName 做一一对应的身份改名；不凭器件外观或“同为电阻电容”判断可复用。合并器只改已经证明相同的缓存身份与实例 GraphicName 引用，检查所有实例定义及非缓存域只出现白名单变动。

普通器件、Global、电源符号、OffPageConnector、Port 属不同电气域。缓存网络符号可以独立完整比较；页面上多次使用同一符号是正常实例复用。不要把相似箭头、地符号或电源条跨类型合并，也不要只按网络文字去删符号。现有工具对网络符号提供完整审计，不自动改写它们。

## 默认属性不同，必须按作用域保存当前行为

结构相同而默认值不同，只是条件候选。需要逐 Package、Cell、Normal/Convert 和实例/occurrence 建立默认差异表：

- 实例已有显式值时，原样保留，包括显式空串与重复属性。
- 原默认存在、实例未显式覆盖时，先读原生有效值，再决定是否物化到实例。只有计划显式列出的属性名可以物化。 `PackageUserProp` 原始节点不是有效继承证明；若原生查询失败，不得复制 raw 值或填空，保留逐属性的失败状态与审阅依据。读取有定义空串和读取失败必须区分。
- 原默认缺失而新缓存有默认值时，必须阻止新的意外继承。缺失与空串不是同一状态。
- 同名属性有多个继承来源、实例缺少独立 Reference/PartValue，或无法解释 occurrence 覆盖时，自动合并停止。

在人工核对差异表与原生有效值之后才生成条件计划，例如：

~~~powershell
python build_merge_plan.py --audit cache_audit --mode scoped --materialize-property ReviewedProperty --output scoped_plan.json
python cache_merge_scoped.py --input source.xml --output scoped_candidate.xml --plan scoped_plan.json
~~~

合并器在原作用域移除不一致的公共默认项，保留每个当前实例的有效行为。导出的复用库因此可能具有中性的空 Value，未来新放置器件仍需明确填值；不能把“当前实例行为相同”说成“所有未来放置默认值相同”。

effective_property_audit_defs.tcl 只有过程定义。调用方在已打开的副本设计中加载它，再调用：

~~~tcl
source effective_property_audit_defs.tcl
::CaptureCacheReadOnly::auditEffective $design query_data.tcldict effective.tsv
~~~

query_data.tcldict 是本项目生成的 Tcl 字典，键是原生实例 ID，值是要查询的属性名列表。字典是数据，不应作为 Tcl 脚本 source。查询通过实例 GetEffectivePropStringValue 读取，输出 failed、state code、value 和 error。原始读取失败不等于空值，不可将失败记录丢掉。比较工具保留整行内容和重复次数：

~~~powershell
python compare_effective_properties.py --before before.tsv --after after.tsv --out effective_gate
~~~

## 原点重基解决“脚已对格、器件原点不对格”

先完成页面/线/实际引脚的安全网格规划。若库图形采用非整格的局部坐标，直接把器件原点吸到格点会移动实际引脚，破坏连接。应对库局部坐标系做平移，同时反向补偿实例原点。

先从每个已放置实例的 `GetOffsetGraphicPoint` 读取局部 `(0,0)`、`(1,0)`、`(0,1)` 三个基点。它们直接给出实际世界变换 `world = B + A × local`，其中 `B` 不一定等于 XML 中的实例原点 `O`。保存同一版本的页名、实例 ID、原始 O/rotation/mirror、B、A 和 offset=B−O；后续以实际引脚热点再逐项核对。不要仅凭旋转枚举、屏幕方向或库边框推断框架。

本机原生八姿态校准已证实：在边框从 `(0,0)` 开始、宽 W 高 H 的已测普通器件路径中，先镜像 X，rotation=1 的线性部分为 `(x,y)→(y,−x)`；同时存在随边框改变的 offset。`(rotation,mirror)` 的 offset 分别为 `(0,0):(0,0)`、`(0,1):(W,0)`、`(1,0):(0,W)`、`(1,1):(0,0)`、`(2,0):(W,H)`、`(2,1):(0,H)`、`(3,0):(H,0)`、`(3,1):(H,W)`。这不是任意非零边框、嵌套符号或 OffPage 的通用保证；正式计算优先使用每个实例的原生基点表，并在候选原生重开后重新导出复核。

实例 `PartInstDisplayProp` 在已验证路径中的实际锚点为 `O + local`，不套图元的 A 或边框 offset。若器件原点改变，DP 局部偏移只补偿 `O旧−O新`，保持原来的绝对文字锚点；不能随器件姿态重复旋转文字。

纯定义的 [native_affine_audit_defs.tcl](../scripts/capture_xml_tools/native_affine_audit_defs.tcl) 不加载 DLL、不打开设计、不保存，也不自动调用。调用方在单一原生会话中传入已打开的独立设计：

~~~tcl
source native_affine_audit_defs.tcl
::CaptureNativeAffine::auditPartFrames $ownedDesign part_frames.tsv
~~~

从同一缓存 view 的所有实例取共同局部余数 r，要求一致。对于局部原点重基 `local新=local旧−r`，一般关系是 `O新=O旧+offset旧+A×r−offset新`；offset 必须随新边框重新取得或已被同类原生校准验证。缓存图元和实例 PortInst 的 start/hot 坐标同步减 r；DP 局部偏移加 `O旧−O新`。若还把库坐标通过 `q=M×p+t` 统一到共享模板，则要求 `A新=A旧×M⁻¹`，并据实际旧/新框架求 O，使所有世界坐标完全相同。仅有代数逆变换一致还不够，必须再由原生读回新姿态、引脚与基点验证。

旧版 [symbol_origin_rebase.py](../scripts/capture_xml_tools/symbol_origin_rebase.py) 的校准协议只覆盖零 rotation/mirror 的原点重基。它现在明确拒绝任何非零姿态；旧 `O+RM(local)` 论述不得用于旋转/镜像输入。下面的调用仍仅适用于已经核对零姿态的输入，不能把一个手写 PASS JSON 当作八姿态证据：

~~~powershell
python symbol_origin_rebase.py --input grid_candidate.xml --output rebased.xml --grid 5 --expected-input-sha <实际SHA256> --native-frame-calibration zero_pose_native_calibration.json
~~~

用变换前后的独立前向投影比较全部实际图元、针起点/热点、字体/可见性和文本锚点，再逆变换要求整个 XML 重现输入。当前版本只接受已审查的图元词汇和正奇数网格步长；未知嵌套 SymbolVector、Bitmap、PinDisplayProp 坐标框架会阻止自动处理。

这里的 5 是示例文档单位，不等于普遍适用的 mil 值。GridDisplay 的 1/2 pin-to-pin 要先通过当前设计 PinToPin/DocUnits 和原生实际点校准。

缓存针缺于当前实例 PortInst 列表，并不能证明它隐藏、NC 或已删除。记录其位置索引、PhysicalPart/PinShared、NC/visible/numberVisible 原始标志，仍将其随同整个局部坐标系平移；验证虚拟世界坐标完全不变。只对当前实际导出的针声明网格已对齐，未来显示或实例化历史针需另审。

## 原生往返必须先保留原始差异，再做有界解释

~~~powershell
python compare_ordered.py --before expected.xml --after reopened.xml --out raw_review
python review_native_roundtrip.py --before expected.xml --after reopened.xml --out bounded_review
~~~

第一步保留字段级完整有序差异和分区哈希。第二步仅允许已经在不修改往返中证实的表示变化：

- 输出文件名、生成的 INS 数字名称、页时间和 MaxDbId。
- 明确列出的 Alias/显示属性/PortInst ID 再生成；必须一一对应、不与保留 ID 相撞、无残留显式 ref-ID，并且 MaxDbId 覆盖实际 ID。
- Junction 仅允许在原来对应的同一个 Net 容器内重挂 owner wire。完整节点多重集、坐标和重复次数不变，且每个点都在其所属线段上。不能跨网或按整页汇总后宣称一致。

原生确会重排 PartInstUserProp 时，可加 --allow-partinst-userprop-order。这只按完整属性节点内容排序回各自原有槽位，保留所有内容、重复次数及其他子序列。不能递归排序全部 XML。

原生确会将计划移除的 PartValue 重建为空项时，可加 --allow-empty-partvalue-reconstruction；工具单列每一处缺失到空项。这个选项本身不能证明业务等价，还必须有每个当前实例的显式 Value 与原生有效属性对比。不得忽略非空 Value 或其他默认变化。

bounded gate 返回 0 仅说明 XML 变化都被限定解释；仍需独立原生 PST255 检查完整 refdes.pin 连接分区、网名、NC、脚号、器件与 footprint/value。再核原生实际图元/文字坐标和全部页面可读性，保存后新进程重开重验。成功返回码或日志里“import complete”均不能代替这些验收。

## 导出配套 OLB 还要检查库级默认值

DSN Cache 与独立 OLB 的全部 Package 相同，仍可能出现库级 DefaultValues 不同：新 OLB 的默认字体、DefaultPlacedInstIsPrimitive 会影响没有局部字体的针或未来放置。比较器不掩盖这些差异：

~~~powershell
python compare_cache_library.py --design final_design.xml --library reopened_library.xml --out library_gate
~~~

只允许 DSN cache 的 Package.sourceLibName 在外部 OLB 缺省这一已核的身份差异；全部 Package 名称、CellName、字体、属性、脚号、顺序和图元仍严格比较，库级 DefaultValues 另列完整差异。该工具要求 Package 名称唯一，不能把同名不同来源缓存擅自覆盖。

library_defaults_clone_defs.tcl 提供纯定义 helper，调用方将原设计与独立新 OLB 对象传入。它从真实源 GetDefaultFont(index,state) 返回的 LOGFONT 直接复制，检查每种字体全部 14 字段及 primitive 默认值；不能仅按 XML 中较少的字体字段重建 LOGFONT。只改目标内存，不替调用方保存：

~~~tcl
source library_defaults_clone_defs.tcl
::CaptureLibraryDefaults::cloneDefaults $sourceDesign $ownedNewLib apply.tsv expected_defaults.tcldict
# 调用方仅保存独立目标库，随后结束进程。
# 新进程重开目标库后：
::CaptureLibraryDefaults::auditDefaults $reopenedLib expected_defaults.tcldict reopen.tsv
~~~

该 helper 的真实源读取、目标写入、保存后独立新进程重开验证已通过。再原生导出 OLB XML，重做完整 Package + DefaultValues 对比和全缓存六表检查。不要调用 PartInst 对象冒充 DboLib；本机 native 对象类型与指针约定不匹配可能导致进程崩溃。

## 新库内容相同，来源路径仍可能再次制造重复缓存

SourceLibName 对已经缓存的图形显示或现有网表导出，通常不需要重新读原库；它仍参与后续放置、更新和替换的来源身份。把缓存导出为一个新 OLB，并不自动把 DSN 中的库链接改为新库。原生内存试验已证实：从新库放置一个同名、完整定义相同且已缓存的器件，仍可能令缓存包数增加一。不能将来源路径永久视为无作用的历史备注。

先在独立 native session 做不保存的 canary；保护输入 DSN/OLB 的前后 SHA。cache_reuse_canary_defs.tcl 只有过程定义，调用方传入已打开的独立设计、库和一个确实已存在的包名：

~~~tcl
source cache_reuse_canary_defs.tcl
::CacheReuseCanary::probeAndDiscard $session $ownedDesign $sourceLib $cachedPackage fresh_report.tcldict
~~~

它按已验证 NewPlacedInst 签名在内存放置一次，记录实际 SourceLibName/SourcePartName、缓存包来源与包数，再 RemoveDesign；无 Save 调用。函数会丢弃传入的 ownedDesign，返回后不能再用该对象。不要对 GUI 正在编辑的用户设计调用。迭代器返回 NULL 结束时观察到的合法代码 1022 只在那个 EOF 位置处理，其他读取失败仍报错。

若来源不同造成新缓存，只对 Package.Defn.sourceLibName 与对应 PartInst.Defn.libName 做一致的来源重绑；包名、Cell/GraphicName、所有器件默认值、occurrence、针脚和绘图字段均不能顺带修改。cache_source_relink.py 会：

- 校验目标独立 OLB 的真实 SHA，并要求完整 Package 与库级 DefaultValues 与设计缓存相同。
- 要求原生读回的绝对库身份路径与该目标实际文件规范化后为同一位置。
- 只生成新的 XML 和逐字段计划，逆变换要求全树等同原输入。
- 原生保存并新进程重开后，仍需全字段 bounded/PST 门禁及从准确目标库的再次放置 canary；期望缓存包数不增、来源正确、输入文件 SHA 不变。电阻、电容与多单元器件宜各自使用新会话验证。

~~~powershell
python cache_source_relink.py --input accepted.xml --output relinked.xml --expected-input-sha <实际输入SHA> --library-xml verified_library.xml --target-library <准确的绝对OLB路径> --expected-library-sha <该OLB实际SHA> --native-source-identity <原生GetName读回的同一库身份路径>
~~~

当前可靠闭合使用准确的原生绝对路径。相对路径是否与 native 的库查找/缓存身份一致，须在独立 canary 中验证；不能凭字符串看似相同推断可迁移。移动工程或改库名后，要重新核来源链接并做不保存放置测试。

XML 属性中的反斜杠是普通字符，不要按 Tcl 字符串规则手工翻倍。JSON、repr、日志包装可能额外显示一层反斜杠；检查解析后的实际字符及连续反斜杠数量，再比原生返回值。生成器将参数直接写入 XML 属性，不 eval 成 Tcl 命令。


## 缓存身份整理后，PCB 规则导出差异要逐门、逐脚解释

原理图缓存复用可能改变 PST 的 primitive 身份，并让 PCB 的 PartDefn 定义合并、Gate 自动编号重新分配。几何与网表导入成功不能单独证明约束保持；也不能把全部 Gate 名称或整个 PartDefn 区段直接忽略。

先保留原始严格比较报告、原始 CFX 字节与完整有序差异。用前后实际 PST 按物理位号逐一建立 primitive 映射，完整电气定义、全部 pin/body/section、封装和值都必须相同。PartDefn 的复合名称只允许替换这个已证实的 primitive 部分；所有其它名称字段和非身份约束完整保留。多个旧定义合并为一个新定义时，先证明旧定义的全部非身份内容相同，再按明确的旧定义数量展开实际定义作多重集比较，不能通过 set 去重掩盖删除或重复。

Gate 编号只能由完整 pin 成员及全部属性推导对应关系。只在本来属于集合的直接 Pin 子对象之间，按完整子树排序；保留每个 pin 的属性、文本、内部子序列和重复次数。除 Gate 根名称外的完整内容必须相同。对同内容的空 Gate，可以在确认未被引用后建立保留数量的双射；不要凭排序猜测某个空 Gate 原先对应哪个编号。

扫描整个导出树的属性和文本，核实 Gate 身份的外部引用。形如 F 加数字的字符也可能是物理位号或 BGA 球脚号；必须按节点种类，并用两份实际 PST 的物理位号/脚号端点证实，不能笼统当成 Gate 引用或笼统忽略。PinPair 两端也应逐端核对。出现无法分类的潜在引用就停止自动通过。

Part 仅允许完整命名对象集合的顺序差异；其它完整约束区段、Stackup、模式、用户属性及有意义的序列继续严格比较。板名和保存修订计数等元数据只沿用事先明确的最小白名单，不扩展到逻辑修订或规则字段。记录原始字节不相同与有界语义相同这两个不同结论。

最后把独立解释报告绑定实际输入/输出 BRD、实际导出 PST、原生导入日志、几何/引脚/铜连接与网络状态的 SHA，以及原严格报告的 SHA。保留原严格 FAIL；另立有范围、有依据的通过报告。反测至少包括：只排列已声明集合应通过；改变一个 pin 或约束、删除成员、增加重复或引入未知 Gate 引用必须失败。该方法不能替代后续规则 DRC，也不能宣称任意缓存身份更改都安全。

## 官方接口依据与失败边界

在本机 Cadence 安装目录下查：

- doc/cap_ug/Replacing_and_Updating_Cache.html：Replace Cache 与 Update Cache 的范围。Preserve properties 不表示显示位置完全不变。
- doc/capinfomodel/dboimnew.html：实例、occurrence、缓存与 pin/position 对应关系。
- tools/capture/tclscripts/capDB/dsn.xsd、olb.xsd：当前官方 XML 词汇和库/设计差异。
- tools/capture/tclscripts/OrCAD_Capture_TclTk_Extensions.pdf：GetEffectivePropStringValue、ReplaceInst 与缓存方法签名。
- tools/capture/tclscripts/capPSpiceModelApp/PWL/Digital/Gates/OR/tcl/PwlORSymbolCreate.tcl 的 initLib：SetDefaultFont 与 SetDefaultPlacedInstIsPrimitive 官方示例。

历史原生 ReplaceCache/UpdateCache 尝试出现过返回成功但库体未变，以及不匹配调用后空指针问题；不能通过猜布尔参数修复。已验证的逐实例 ReplaceInst 也会影响 refdes/针号可见性，并留下旧缓存，必须显式恢复并新进程核对。官方 XML 路径同样不是无损保证，只是提供可审计输入和白名单变换的途径。

## 工具反测

selftest.py 创建少量合成 XML，无实际项目数据，不加载 CAD。测试允许生成 ID、同网 Junction owner 和已声明属性顺序变化；拒绝针属性、电气类型、属性值、Junction 缺失/重复、ID 碰撞、owner 不在线上等变化。

~~~powershell
python selftest.py --out <一个尚不存在的临时输出目录>
~~~

通过合成测试只能证明比较器和白名单拒绝逻辑工作，不能替代当前项目的原生往返、电气、实际坐标与视觉验收。


按用户长期维护的库统一外观，见[自建库优先模板方法](capture_user_library_first_templates.md)；此时模板图形可以有明确授权的变化，不能把旧的图形不变证明直接套用。
# 仅更新库来源时使用原生接口

来源重定位可使用 [native_cache_source_relink_defs.tcl](../scripts/capture_xml_tools/native_cache_source_relink_defs.tcl)。它只定义函数，不加载 DLL、不打开设计、不保存；调用者须先建立自己独占的原生会话和设计副本。先核对目标 OLB 与设计 Cache 的完整包、默认值及符号内容，再显式传入旧／新来源字符串和预期的各类缓存对象数量，调用 `::CaptureSourceRelink::apply`。

该函数沿用本机 Cadence `capUtils/capReplacePathInCache.tcl` 的 `design ReplaceSourceLibName` 和 `cachedLibObject SetSourceLibName` 两个调用。先完整选择并检查数量，再更新，随后立即读回。它返回 `APPLIED_NOT_SAVED`；保存、独立重开、XML 全字段有界比较、PST 与目标 OLB 的不保存试放仍由调用者完成。缓存对象数量不等于 Package 数量，不能把某个案例的数量当成通用常量。

只修改 DisplayProp 位置时也优先对现有对象调用 `SetLocation`，先检查所属实例、原坐标、实际显示串、完整字体、旋转和对齐，保存后重新读回。不要为文字移动重新创建电气对象。

XML 往返可能把同一网络同一点的 Junction 重新归到另一条 Wire；坐标和网表相同，不等于完整对象树不变。要求仅修改来源或显示属性时，应先采用上述原生路径，并严格保留 Junction 的原有归属。若采用 XML 往返，须单独解释实际变化，不能把它们整体归为无关的运行时 ID。

