# 第27课：板框、安装孔与机械基准

日期：2026-10-19（Asia/Shanghai）。全部下载、源码、中转、日志、图和练习均在 D:\001DIY\005lib\01AIEDA 内。

本课已完成声明范围的原生 CAD 实操及独立复核。输入采用当前 A4 原理图相对应的 DE_BASELINE，而不是第26课受控 ECO 实验。建立被17.2数据库识别的实际板框、机械钻孔、连接器位置与方向、布线/器件区域及限高；通过故意违反规则、原生检出、事务撤回、新进程重开验证效果。它是建板课程，79个逻辑器件仍未布局，不表示已经完成板级布局布线或制造释放。

## 1. 当前文件和来源

- 最终原生板：[F27_MECHANICAL.brd](../examples/lesson27_mechanical_20261019/F27_MECHANICAL.brd)。
- 最终板 SHA256：B6C84686472475F452F13F30EB7E3F99D8B9441CF0AB44B3D33917D615E5B55A。
- [独立验收 validation.json](../examples/lesson27_mechanical_20261019/validation.json)：48项 PASS；各项检查有名称和实际数据，不将此数字解释为制造质量评级。
- [真实读回预览 PNG](../examples/lesson27_mechanical_20261019/preview.png)、[SVG](../examples/lesson27_mechanical_20261019/preview.svg)：由重新打开BRD后的原生坐标、铜和孔数据生成，已目视核对；不是GUI截图。H1—H4是图中的机械基准称呼，不是新增原理图位号。
- [原生读回](../examples/lesson27_mechanical_20261019/readback/)包含元件、272逻辑pin、69网络、层叠、5个已放物理实例、44条两层物理pin读回、实际约束形状、文字和受控挑战。
- [输入清单](../examples/lesson27_mechanical_20261019/source/input_manifest.json)及[依赖身份](../examples/lesson27_mechanical_20261019/source/dependency_manifest.json)记录源文件、源库和SHA；最终全部文件另见课目录 artifact_manifest.json。

权威输入：learning/examples/de_15_26_20261019/native_flow_final/DE_BASELINE.brd。SHA256为 3E0AA1EE367238FDEBB7F18BE07339CF07882BF6656E9B6D51C86A5F6EC764FC。先复制至本课source，再打开副本编辑另存；原始基线和副本均未被改变。保留80个逻辑元件、272个逻辑pin、69个网络、所有pin→net对应及封装身份。当前A4的R19/R20为2.2k；没有误用ECO的3.3k/PB8PB9交换版本。

采用本机官方 Allegro PCB Designer 17.2 S045 Windows SPB 64-bit Edition。依据：
1. 本机官方 algroskill/02dbdesc.html 与 axlDbidDoc.txt：designOutline、keepinPlace、keepinRoute及对象属性。
2. 本机官方 algrolay/chap2.html：Package Keepin为唯一无填充闭合多边形；Package Keepout为填充形状，ALL作用于两面；附加高度范围表示禁止占据的Z区间。
3. 本机官方 propref/properties.html 的 PACKAGE_HEIGHT_MAX/MIN；axlDBAddProp、axlDBCreateShape、axlSetSymbolType、axlCompileSymbol、axlDRCUpdate、axlDBRefreshId、axlDBTransaction*函数说明。
4. GCT USB4105官方Rev B4图，第1页。继承已核验第10课的封装、图纸和尺寸链，原图 [usb4105.pdf](../examples/lesson10_connector_20261018/source/usb4105.pdf)，SHA256 FB331FBABEE8392ED2937ED757C1610CB0F174B84625147C0B580A18EEA8C0E5。
5. 第7课纯无铜NPTH pad：eda_l07c_npth_200_null.pad。本课仅复制该核验过的依赖，不重新用假铜环消除NPTH用途性警告。

本课没有依赖不可用的桌面native pipe，也没有建立自制UI自动化。

## 2. 教学机械条件和基准

以下80×60、孔径及空间都是本次自行确定的教学条件，不是用户指定外壳规格，也不是原厂推荐整板尺寸。

| 项目 | 本次原生定义及核对 |
| --- | --- |
| 坐标和安装方向 | mm；A=(0,0)为理论左下基准交点；+X右、+Y向板内、+Z为TOP；TOP装连接器 |
| 板框 | 80×60mm；四角C2直线切角；8条闭合边，不是8条相互未相接的参考线 |
| 有序板框顶点 | (2,0),(78,0),(80,2),(80,58),(78,60),(2,60),(0,58),(0,2)，隐式闭合回第一点 |
| 面积 | 4800−4×(2×2/2)=4792mm²，独立按读回顶点计算 |
| 四个安装孔中心 | H1(5,5)、H2(75,5)、H3(75,55)、H4(5,55)，中心距70×50 |
| 安装孔 | Ø2.00、NON_PLATED、圆孔、无编号机械pin；两面REGULAR均为NULL。没有把2mm称为已认证的M2成品装配孔 |
| 安装硬件空间 | 每孔Ø5布线及器件禁入；这是教学包络。相对Ø2孔边保留1.5mm径向空间，实际螺钉/垫圈/扭矩/电气间隙尚未指定 |
| 板边加工 | 未假定槽孔及外形公差、分板连接、工艺边、V-cut或铣刀半径已获板厂同意 |
| 机械标注 | 原生USER_MECH_DATUM及USER_MECH_DIMENSIONS层有基准、尺寸、方向和限高说明；标注只是说明，实际约束由下面的keepin/out对象实施 |

板框写入 BOARD GEOMETRY/DESIGN_OUTLINE，重开后根对象 designOutline 非nil。没有把旧OUTLINE辅助线或文字当实际板框；最终文件只有一套被识别的design outline。本课不改01env或全局快捷键，后续出图需确认该实际轮廓进入制造文件。

四个孔最终使用独立MECHANICAL符号 l27_npth_d200_mech.bsm，含一个真实机械孔和装配圆，无虚构实体器件。原生 .dra/.bsm 和复用 .pad 均在课目录library。孔符号不增加原理图逻辑元件，也不伪造螺钉的高度或BOM；硬件占用另用板级有效禁入区定义。

## 3. USB连接器位置、板边与插入空间

J2使用已验证的 L10_GCT_USB4105_GF_A_12LAND；原点(40,3.675)，顶面0°，不镜像。封装本地PCB Edge为y=-3.675，所以真正板边为全局y=0。开口朝−Y，外部插头从−Y侧向+Y插入，拔出为−Y。

| 对象 | 全局坐标 / mm |
| --- | --- |
| 本体名义投影 | x35.53…44.47，y0…7.35；其名义前沿齐真正板边 |
| 前排壳脚槽中心 | (35.68,2.60)、(44.32,2.60)，孔0.60×1.40 |
| 后排壳脚槽中心 | (35.68,6.78)、(44.32,6.78)，孔0.60×1.70 |
| 两定位NPTH | (37.11,6.28)、(42.89,6.28)，Ø0.65，实际两面无铜 |
| 12块SMT land | 全部y7.355，保留16接点→12 land既有映射，未改电气连接 |
| 实际Place Bound | x34.88…45.12，y-0.325…8.23；MAX=3.46 MM |
| 三文字锚点 | J2的REF DES/SILKSCREEN_TOP、REF DES/ASSEMBLY_TOP、COMPONENT VALUE/ASSEMBLY_TOP全为(40,3.675)，对应封装本地原点(0,0) |
| 插拔空间教学包络 | x34…46，外侧至y=-12；实际PACKAGE KEEPOUT/TOP、BOTTOM为y=-12…-0.5，保留连接器自有courtyard范围 |

3.46mm来自第10课厂家图板上高度及一般公差，不使用默认1mm替代。板下壳脚侵入0.80…1.10mm仍作为装配检查输入；板厚、定位柱、焊接工艺、插头壳体、线缆弯曲和外壳开孔须另外确认。

连接器courtyard比名义本体前沿多伸出板外0.325mm。为保持真正开口在y=0，PACKAGE KEEPIN在x34.5…45.5局部延伸到y=-0.5，形成明确边缘安装例外；其余区域约内缩0.5。没有为了清除DRC把接口移离板边，也没有关闭全局检查。插拔禁入在y=-0.5止，避免把同一连接器自己的courtyard误判成插头占用。原封装辅助插拔线只是参考，最终上述板级filled keepout才是有效禁放区。

## 4. 有效区域与主动验证

| 有效对象 | 范围和作用 |
| --- | --- |
| ROUTE KEEPIN/ALL | 实际闭合无填充区域，约距板边0.5mm；切角处偏移后的顶点按0.001mm保留 |
| PACKAGE KEEPIN/ALL | 实际闭合无填充区域；除J2局部courtyard例外外约内缩0.5mm |
| ROUTE KEEPOUT/ALL | 四孔各Ø5填充禁布区；另继承J2两定位孔周已验证的0.85×0.85禁布区 |
| PACKAGE KEEPOUT/ALL | 四孔各Ø5，预留安装硬件不受其他电子器件占用；机械孔符号本身无虚构包络 |
| PACKAGE KEEPOUT/TOP、BOTTOM | 插拔外侧x34…46、y-12…-0.5 |
| TOP低型器件区 | x10…30、y42…52；PACKAGE_HEIGHT_MIN="2 MM"。该区表示Z≥2mm被占用，低于或等于2mm的器件可在下面，不能把MIN误读为器件最低高度要求 |

先开启Package_to_Place_Keepin_Spacing及Package_to_Place_Keepout_Spacing；没有屏蔽报错、豁免机械冲突或关闭其他检查来凑零。实际原生记录：

| 受控动作 | 实际命中 | 撤回结果 |
| --- | --- | --- |
| Ø2安装孔/Ø5禁布范围内横穿一段0.2mm TOP线，(3,5)→(7,5) | 2条：Line to Route Keepout Spacing；Mechanical Drill Hole to Line Spacing，后者现有规则expected0.203mm/actual0 | 事务回退，0DRC/t |
| J2临时移动至(20,47)，进入TOP低型区 | 1条Package to Place Keepout Spacing；source=PACKAGE_HEIGHT_MIN，expected2MM/actual3.46MM | 回退到(40,3.675)，0DRC/t |
| J2临时移动至(5,5)，侵入孔硬件区并跨左边keepin | 2条：Package to Place Keepout Spacing和Package to Place Keepin Spacing | 回退到正式位置，0DRC/t |
| 独立readonly进程中，临时TOP线(0.1,25)→(2,25)跨route keepin边界x0.5 | 1条Line to Route Keepin Spacing | 回退0DRC/t，quit且不保存；BRD SHA不变 |

上述默认0.203mm孔线规则来自输入承载板，不把它当已经评审过的制造规则；本课有效Ø5机械禁布还额外控制实际硬件空间。第29课会把物理规则、来源和例外作为明确课程继续处理。

规则验证不是只看“图上画了矩形”。正例正式位置无机械DRC；受控违规有正确命名的原生DRC与高度actual/expected；回退后重新检查；保存后新进程重开。当前0DRC仅证明当前已放对象和启用检查范围，没有验证79件未布局器件或任何未布线信号的质量。

## 5. 实操步骤与复现入口

代码及所有运行文件位于 [lesson27_mechanical_20261019](../examples/lesson27_mechanical_20261019/)。

1. 读取EDA、根课程索引和record_location_rules；输入采用DE_BASELINE及其已验证library。run27.py复制基线、纯NPTH pad，记录SHA并限制所有路径在01AIEDA内。
2. 子进程使用官方allegro.exe -product Allegro_performance -safe -nographic；.scr先source $TELENV恢复官方/现有入口，再由SKILL设置课内与DE只读依赖库路径。cwd、ALLEGRO_PCBENV、TEMP/TMP都设到本课日志目录，不改HOME、01env或公共库。
3. 使用axlSetSymbolType("mechanical")、axlDBCreatePin(... nil ...)和axlCompileSymbol建立纯孔DRA/BSM。最终成功记录为logs/package03；前两套PACKAGE尝试保留为历史失败候选。
4. 在基线副本中axlDBChangeDesignUnits("millimeters" 3)，设置允许负坐标的design extents。用axlPathStart/axlDBCreateShape创建真正DESIGN_OUTLINE、无填充keepin及填充keepout。
5. axlDBCreateSymbol("J2" 40:3.675 nil 0)放真实逻辑器件；四个孔用MECHANICAL符号加入，不创建额外逻辑组件。为低型区设置MIN2MM；标注仅作为读图说明。
6. 分别启动事务、注入路径或移动J2、axlDRCUpdate(t)检查、保存命名与expected/actual、axlDBTransactionRollback回退，再DRC。DRC更新后axlDBRefreshId(nil)刷新缓存，避免拿旧dbid列表当新结果。
7. 另存F27_MECHANICAL.brd，最终成功日志logs/create06/create.txt有L27_CREATE COMPLETE；实际退出码0，源副本前后SHA相同。实际执行过的SKILL快照为logs/create06/executed_source.il，规范源码为scripts/lesson27.il（仅修正了MIN属性调用表示，不改变当前数据库结果）。
8. run27.py read read01在新的-readonly原生进程导出TSV；read02补文字与route keepin挑战。两次输入BRD前后SHA一致，均有COMPLETE，实际退出码0。
9. scripts/validate27.py从原生TSV、原始基线读回和独立坐标表检查：逻辑组件/引脚/网络未丢失，唯一真实板框、面积/切角、4孔/12land/4slot/2locator、有效边界、真实高度、三锚点、DRC正反例、保存/重开哈希。当前48项PASS。
10. SVG/PNG由实际读回数据生成，已目视核对孔对称性、J2朝向与板边、低型区、边界及文字可读性；没有用一张外观图替代原生几何检查。

复现命令入口为课内scripts/run27.py的package/create/read；脚本带有本次具体路径和日志名，现有交付及日志不可直接覆盖。重新练习应复制脚本到01AIEDA内全新案例目录，调整输入/输出/日志/库路径，并再次核查哈希。run27.py记录实际进程PID/startUTC/退出码，不因exit0单独判成功；所有成功还要求COMPLETE、原生输出和重开数据吻合。

## 6. 失败及修正，必须保留

1. 首次将根对象属性误写为outline，导致“Design outline not recognized”，实际官方属性为designOutline。create01退出0但SKILL报错、无COMPLETE，因此没有验收；没有把exit0包装成成功。更正后新建形状被根对象正确识别。
2. 初次把ROUTE KEEPIN创建为filled，17.2返回SPMHDB-185。按官方文档改成无填充闭合形状；不能把keepout的填充设置照搬给keepin。create02失败原稿/日志保留。
3. 初次照自然语言写PLACE KEEPIN/ALL，实际Cadence类名是PACKAGE KEEPIN/ALL；同理PACKAGE KEEPOUT。create03原生No match for class name及脚本保留。
4. 第一套安装孔用PACKAGE并人为加1mm实体边界，与其板级Ø5禁放区发生自身冲突。删除边界再编译PACKAGE也会由编译器自动补出默认3.81mm实体，所以create04/05均不能作为最终板。改成官方MECHANICAL BSM，表示纯钻孔，不伪造实体高度，不豁免冲突，不增添非预期逻辑器件。两个候选BRD和脚本保留在各次失败目录。
5. J2真实courtyard伸出板外0.325mm，初版外侧插拔禁区一直到y0而产生同一连接器自冲突。保留原厂板边和方向；明确局部keepin例外与插拔禁区止点。不能机械套用“所有器件包络必须严格在板内”。
6. axlDBAddProp对多属性要求list(list(name value) list(name value))。实际执行稿误给一个四元素平表，原生只添加第一个MIN2MM，MAX999没有存入。独立读回及时发现；本课意图本来是从2mm到无穷的禁区，存下来的MIN单属性正确。规范代码现只传MIN2MM，明确记录此错误，禁止通过返回非nil就断言全部属性已写入。
7. axlDRCUpdate后dbid属性可缓存旧列表；初版ROUTE count列表甚至显示旧数/失效nil。通过axlDBRefreshId(nil)后重新取root与drcs，最终真实日志2/1/2/0和额外keepin1/0一致。
8. 标准环境source $TELENV产生~S/~Z read-only alias未改警告；单位/空白设计初始化保留SPMHUT-48 rounding警告。关键机械坐标按0.001mm独立核对通过，没有删除日志或宣称全过程无警告。PyMuPDF预览生成还给出fitz旧导入名弃用提示，不影响原生CAD结果。

失败/拒收文件没有移出学习总目录，也没有替换公共库。所有自建中间文件、脚本、备份、预览和日志均留在01AIEDA本课目录。

## 7. 本课边界及交接

本课实际完成了建板与约束范围：软件知道哪一条是板框；孔是可核验的真实无铜NPTH；USB板边、壳脚/定位孔、原点和方向一致；放置/布线区域和高度规则能真正检出越界，并证明撤回和持久化完整。电子封装J2保留用户三文字原点规范和真实高度；机械钻孔不虚构一个1mm电子器件。

交第28课的输入为本课F27_MECHANICAL.brd及SHA，源承载层名仍严格TOP-BOTTOM。第28课在副本建立两层/四层实际层叠、制造假设及01env映射；第29课继续在层叠副本设置网络分类、物理/电气/差分规则及受控例外。给后续临时规则挑战的空白区为x30…55、y25…40，避免安装孔、USB及低型区；所有临时对象需回退。

仍需后续完成：全部器件关键布局/走线、实际连续参考平面与回流、孔的成品公差/镀槽/外形加工/工艺边、最终紧固件和装配操作包络、外壳开口及完整插头线缆3D、板厚与连接器腿/焊接方式、实物制造装配，以及板级SI/PI/EMI和接口调试。本课没有以网络连通或0DRC代替这些项目，也没有将它们冒充本课已完成验收。
