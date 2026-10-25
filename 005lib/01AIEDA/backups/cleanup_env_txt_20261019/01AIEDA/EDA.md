# AI 辅助 EDA 设计协作记录


我刚刚在另外一个窗口设计pcb  这是你的一些操作 对于你学习是否有帮助 
另外 你做好记录  pcb的层叠顺序 必须按照 
2层 TOP-BOTTOM 
4层 TOP-L2-L3-BOTTOM  
6层 TOP-L2-L3-L4-L5-BOTTOM  
的格式延伸  
01env drill*.txt是对应的光绘的层叠信息 
按照这样设计 我的快捷方式就不用更改

## 当前学习计划（2026-10-19，D和E合并课程）

完整课程目录见根目录 [课程索引.md](课程索引.md)：60课主线及5个按需进阶专题。按用户最新指令，D/E第15—26课以STM32F103C8T6整合学习，第15—25课理论/来源/计算及原生连接范围已完成，第26课真实导出/PCB导入/ECO/逆向比较1578项通过，GUI ERC/应用SWP待验。当前完整记录见[D/E合并总结](learning/notes/lessonDE_15_26_20261019.md)及第26节，下一主线第27课。C阶段及第6/11课界面待验项保留，51编程教程继续暂缓；本轮MCU硬件课程依据新指令开展。

**统一学习目录：D:\001Diy\005lib\01AIEDA。** 用户要求把学习计划放在本文开头，并将学习资料、记录、脚本和练习成果集中在这个文件夹。路径迁移已完成；当前按课程推进软件内实操，并保留脚本、原始结果与复核记录。

### 学习目标与执行方式

**2026-10-19 最新纸张与符号规范：** A4 横向 297 × 210 mm 仅为起始尺寸，器件/连线放不下时可扩大到 A3/A2 等，优先保证可读性和器件完整性。普通器件尤其普通 MCU 优先在一个符号单元中放全引脚；CPU 等复杂器件才按实际需要分单元。详见 [纸张规范](learning/notes/capture_page_defaults.md) 和 [符号单元规范](learning/notes/capture_symbol_defaults.md)。此前 D/E 六模块已整理成 [12页 A4 工程](learning/examples/de_15_26_20261019/a4_review/native/DE_INTEGRATED_A4.opj)，保存重开、9375项几何/连接检查和718项真实PST比较通过；十二页是既有方案，不是以后必须全用A4的要求。Capture界面/打印预览/ERC待验，详见 [逐页修订记录](learning/notes/capture_a4_review_20261019.md)，先完成此复核再接第27课。

- 目标：掌握 Cadence 17.2 的符号/焊盘/封装、原理图、器件布局、两层与四层走线及审查操作。
- SI、PI、EMI 是布局布线的基本要求；按器件、回路、供电和参考平面落实，不把当前任务改成仿真任务。
- 每项学习依次完成：读资料 → 记录前提与步骤 → 在练习工程副本复现 → 核对实际结果 → 保存方法与问题。
- 每次操作记录来源/页码或时间点、版本、命令或参数、工程理由、检查结果和验证状态。
- Capture 原理图从 A4 起步，内容放不下可扩大纸张；每页核对尺寸、坐标单位、元件/文字边界和跨页连接，独立电路模块可合理分页。
- 原理图符号优先单单元呈现全部引脚，普通 MCU 保持完整单单元；CPU 等复杂器件可按功能分单元，各单元仍对应同一物理器件、基础位号及 PCB 封装。
- 修改练习时按小范围、可回退的步骤进行；布线先预判路径，再分段执行并检查，遵守当前工程实际指定的层与规则。


### 封装默认规范（用户指定，2026-10-17）

封装文字至少包含以下三项，锚点统一为封装局部原点 **(0,0)**：

| 内容 | Class / Subclass | 坐标 |
| --- | --- | --- |
| 位号 | REF DES / SILKSCREEN_TOP | (0,0) |
| 位号 | REF DES / ASSEMBLY_TOP | (0,0) |
| VALUE | COMPONENT VALUE / ASSEMBLY_TOP | (0,0) |

器件默认 package height 为 **1 mm**；Cadence 在填充 Place Bound 上显式设置 PACKAGE_HEIGHT_MAX="1 MM"（未设 MIN 时下界默认 0）。
当前两脚练习封装已按此更新、重新编译并重开验证。详细规范见 [package_defaults.md](learning/notes/package_defaults.md)；具体器件仍需核对实际引脚、尺寸和高度。

### PCB 层名固定规范（用户指定，2026-10-18）

2层 **TOP-BOTTOM**；4层 **TOP-L2-L3-BOTTOM**；6层 **TOP-L2-L3-L4-L5-BOTTOM**；更多层依此连续延伸。层功能另行记录，保持现有快捷方式可用。01env/drill*.txt为对应光绘模板，先按实际Cross Section核对物理层序，再核光绘映射。长期规范见 [pcb_layer_naming.md](learning/notes/pcb_layer_naming.md)；drill12.txt现有多出L12的差异已记录，未改模板。

### 分阶段计划与验收

| 阶段 | 学习内容 | 验收标准 | 当前进度 |
| --- | --- | --- | --- |
| P0 新机环境与目录迁移 | 程序/版本、HOME、启动入口、资料编码、桌面控制与桥接路径 | Capture/Allegro 分别完成可核对的无副作用操作；路径存在、结果可返回 | 目录迁移完成；Allegro读写/Padstack批处理与Capture官方17.2原生数据库SDK已验证；桌面及Capture GUI内部命令窗待验 |
| P1 基本操作与只读接口 | 视图、网格、过滤器、层、撤销；Capture Tcl；Allegro SKILL 与数据库查询 | 读取练习工程的器件、网络、层和几何，形成带出处的操作记录 | Allegro过滤/网格/回退等原生子项通过；Capture原生设计/两页/保存回退及网络查询通过，GUI部分保留 |
| P2 符号、焊盘与封装 | 引脚编号/类型、Padstack、尺寸、方向、丝印与装配边界 | 依据数据手册逐项核对符号引脚与封装焊盘 | B7—10原生实操完成；C12两套QMI符号及suffix修订完成，C13多单元/作用域17项，C14受控更新81项通过；OLB/PAD/DRA/PSM完整，GUI Cache菜单待验 |
| P3 原理图 | MCU 供电、去耦、复位、时钟、调试及接口/滤波；网络与封装关联 | 接法有依据，ERC 问题有处理记录，导入 PCB 后网络一致 | D/E合并课80件/272pin/69net，266连接及6NC通过；真实PST/BRD/ECO1578项、逆向比较通过。GUI ERC/应用SWP、硬件实测/制造释放待续 |
| P4 关键器件布局 | MCU 出线、去耦回路、开关电源、LC、接口保护与敏感信号 | 能解释关键电流/回流路径，检查地的连续性及耦合风险 | 待开始 |
| P5 两层与四层走线 | 关键网络优先、逐段走线、线宽/间距、过孔、差分/必要匹配、铺铜及换层回流 | 结合板厂层叠和规则核查实际铜皮、回路及路径；不能只看连通性或 DRC | 待开始 |
| P6 审查与生产输出 | 电气/几何审查、去耦与电源回路、参考平面、接口/EMI、制造输出 | 问题逐项闭环，生产输出与最终工程一致 | 待开始，具体输出按任务需要 |
| P7 可迁移操作库 | 操作手册、截图、示例工程、Tcl/SKILL、必要时创建 Codex 技能 | 文档和脚本在工程副本中可复现，含版本、路径配置、日志和回退方法 | 已保存只读、创建与重开核对脚本及日志；尚未创建 Codex 技能 |

### 当前优先事项

1. D/E第15—26课合并学习与工程基线见第26节及[合并记录](learning/notes/lessonDE_15_26_20261019.md)，下一主线第27课板框与机械基准。第26课GUI ERC/应用SWP、第11课GUI/OPJ及第14课Cache菜单需补验，第6课界面部分保留。
2. 桌面控制仍待恢复；Capture官方数据库SDK已验证，不能据此声称GUI内部通道已通过。后续仅使用已验证安全的原生接口，不重放已停用的NULL/FlatNet崩溃探针。
3. 后续按需验证 ai_bridge IPC 往返；本课没有加载桥接或启动 watcher。
4. 继续使用本地官方帮助；收到 PDF/视频后建立章节、页码或时间点索引。图片 PDF 结合页面图像识读，文本 PDF 结合文字与图形核对。

### 学习文件组织

**2026-10-19 清理脚本最终范围：** 以用户最新明确的“XML、CSV、DAT保留，其他按清理项删除，01AIEDA内TXT不删”为准。25个入口按各自原始删除名单恢复，并统一增加TXT清理；全局保留XML/CSV/DAT及数字历史副本，01AIEDA任何层级的TXT及数字副本保留。原名单中的配置、模型、OPJ和备份不再套用前版的工程/新旧条件；DSN/PCB/库/源码等未列入的主文件保留。01AIEDA不再整目录跳过，LOG等其他命中项可清；01env运行模板、版本环境及备份归档目录仍保护。UTF-8无BOM/CRLF，`/preview`只预览，本轮未执行真实工程清理。最终规则、保护目录和本轮验证见 [最新清理规范](learning/notes/cleanup_user_rules_20261019.md)；[前版规则](learning/notes/cleanup_aggressive_20261019.md)与[初始审查](learning/notes/cleanup_file_policy_20261019.md)保留历史。

**强制目录规则：学习笔记、脚本、草稿、中转JSON、辅助校验代码和练习成果全部放在01AIEDA内部；我自行创建的临时中转文件使用learning/staging，不再放到系统Temp。结束前同时核对正式文件和中转文件。** 详见 [目录失误与预防规则](learning/notes/record_location_rules.md)。

- EDA.md：当前计划、进度、新机问题和历史讨论。
- ai_bridge/：现有 Allegro 桥接与加载入口；exchange/ 为该桥接的交换目录。
- learning/scripts/：本轮只读探针及后续学习脚本。
- learning/sources/、learning/notes/、learning/examples/、learning/logs/：教程、分主题笔记、练习工程和验证日志。
- backups/：迁移前原文件及逐文件哈希清单。
- 原有 ast2400_lib、hpm5361*、tmc6460_lib、routing、usbipdaplink_20261009 等目录保留各自结构。

### 新机状态摘要

以下保留新机最初盘点历史；当前Capture原生SDK及后端导入/ECO进展以第25/26节和本文开头为准。

- 已读回旧版 EDA.md，SHA256 与上次保存一致；这只证明文件内容一致，未核实它是如何迁移的。
- Allegro 与 Padstack Editor 运行日志已确认 17.2-S045；Allegro_performance 参数下只读及新建 PACKAGE 成功，Padstack XML 导入成功；Capture 内部与其他产品/选件状态未验证。
- 独立 Tcl 解释器运行成功：8.6.0。它不证明 Capture 内部数据库接口已可用。
- Windows Computer Use 本课复核仍返回 native pipe 不存在，原因未确定；Allegro 软件内 SKILL 已独立验证成功，Capture 内部 Tcl 待验证。
- 本轮没有打开修改真实硬件工程；旧机器及其他历史笔记的成功记录不等于新机已验证。

下文第 1—12 节保留 2026-10-16 的讨论快照；其中“未创建/未验证”指当时本聊天的操作状态。其他历史笔记和目录中已有的脚本应单独审查与复核。新机环境日志见第 13 节；第 2 课只读实测见第 14 节；第 3 课对应关系与几何见第 15 节；第 4 课焊盘/封装创建见第 16 节。

---


记录日期：2026-10-16（Asia/Shanghai）  
来源：本次关于 KiCad、Cadence 与 AI 参与硬件设计的对话。  
用途：供后续协作读取，保留用户要求、选择依据、实际环境证据和尚未验证的能力。以下“已验证”仅指本次工具实际返回的结果。

## 1. 用户的目标与设计要求

用户正在评估让 AI 实际参与完整硬件设计的工具与执行能力。本次属于软件选择和能力讨论，尚未提出具体板子的工程修改任务。用户明确提及的设计范围包括：

1. 原理图符号及元件库设计。
2. PCB 焊盘、过孔、封装及其与符号的引脚映射。
3. 原理图设计。
4. PCB 器件布局。
5. PCB 走线，以及与布局布线相关的电气质量要求。

铺铜、设计检查和生产文件输出是讨论中补充的后续衔接环节，是否需要具体交付以实际项目任务为准。

用户重点关心 MCU 引脚出线、去耦/滤波电容、电感与 LC 网络、电源器件布局，以及两层、四层 PCB 的布线质量。

**必须保留的核心要求：信号完整性（SI）、电源完整性（PI）、EMI 与辐射控制，是布局走线的基本设计考虑。用户在本次对话中并未要求使用软件进行这些项目的仿真。**

用户明确不接受把任务简化为：
- 自动布线后完成网络连通。
- 只检查原理图与 PCB 的电气连接一致。
- 把 SI、PI、EMI 的要求转述成需要购买仿真软件或开展仿真。

后续讨论应围绕“如何把电气要求落实为器件位置、方向、走线、过孔、参考平面及电流路径”，避免再次偏离到仿真软件比较。

## 2. 术语与基本流程

- 用户所说“原理图封装”，通常对应原理图符号，表达引脚名称、编号、电气类型和连接关系。
- PCB 封装表达焊盘、尺寸、间距、丝印、装配边界等实际安装信息。
- 原理图符号与 PCB 封装必须按实际器件的引脚编号正确对应；依据具体数据手册和封装机械图核对。
- Padstack 表达焊盘/孔在各层上的结构，PCB 封装会使用相应焊盘定义。

完整协作流程应从数据手册、器件和机械要求开始，经过符号/封装、原理图、层叠与规则、布局、关键网络布线、其他网络布线、铺铜和审查，再输出制造文件。

常见输出包括 Gerber、钻孔、BOM 和贴片坐标；具体项目以实际制造需求为准。

## 3. 布局与布线应落实的工程判断

### 3.1 MCU 去耦、滤波与供电

- 按具体 MCU 的供电、接地、模拟电源、内部稳压电容等引脚要求设计，不统一套用固定电容值。
- 根据对应引脚安排电容位置、方向与连接方式。
- 检查供电引脚、电容、过孔、地平面和芯片接地之间的完整高频回路，尽量减小回路面积和连接电感。
- “电容看起来离芯片近”不足以证明连接合理，还需要检查实际走线、过孔和回流路径。
- 供电铜宽、过孔数量及位置需要结合电流、压降、热和制造能力安排。

### 3.2 电感、电容、LC 网络与开关电源

- 根据具体电源拓扑识别高 di/dt 电流回路，再安排输入电容、开关器件、电感及输出电容。
- 控制开关节点的铜区和耦合影响，保护反馈、采样与其他敏感信号。
- LC 滤波还应考虑源/负载条件、谐振、阻尼和电源稳定性，不能仅按元件连接顺序摆放。
- 优先核查数据手册布局建议及参考设计，并结合实际板子的结构调整。

### 3.3 MCU 信号与信号完整性

- 按接口和功能分类处理晶振、复位、启动配置、模拟输入、时钟和通信信号。
- 根据边沿速度、互连长度、接口要求和实际层叠判断阻抗、间距、端接、长度/延时匹配等需求。
- 普通 GPIO 不需要全部统一等长；差分信号也需要检查参考平面、过孔和不连续处。
- MCU 出线需要同时兼顾引脚功能、器件位置、布线空间及回流路径。

### 3.4 两层、四层与回流路径

- 先规划层叠、供电与回流，再进行关键器件布局和走线。
- 两层板尤其需要避免走线切碎地铜，检查关键信号下方/附近的回流连续性。
- 四层板需要按板厂实际层叠安排信号参考平面、电源铜区与换层回流。
- 关键信号应避免跨越参考平面的裂缝或分割；换层时需要处理参考平面和回流转换。
- 层数本身不决定电气质量，增加层数不能自动消除 SI、PI 或 EMI 问题。

### 3.5 电源完整性与 EMI

- 检查直流压降、动态负载下的供电路径、共用路径阻抗、去耦网络及噪声耦合。
- 检查噪声源、高频电流回路、敏感区域，以及通过连接器和线缆传播噪声的路径。
- 接口滤波、保护器件的位置与接地连接也会影响性能。
- 机壳、屏蔽、连接器和线缆属于系统层面的 EMI 影响因素，不能仅凭 PCB 连通性作出结论。
- ERC/DRC 是必要的工具检查，覆盖不了全部工程判断；检查通过不能单独证明功能、SI、PI 或 EMI 达标。
- 本次任务没有要求仿真；若以后需要定量验证或 EMC 合规结论，再根据项目要求安排分析与样板测量。

## 4. 软件选择：最终澄清后的结论

需要区分三个问题：
1. 人工学习、操作和修改是否方便。
2. AI 是否容易取得设计数据、执行精确修改并核对结果。
3. 软件的复杂约束管理能力及其分析生态。

本次讨论形成的是有条件的判断，而不是“某软件天然能做出更好的 PCB”：

| 场景 | 本次判断 |
| --- | --- |
| 从零开始普通 MCU、USB、电源组成的两层或四层板，希望 AI 多承担工程生成、修改与检查 | 倾向 KiCad，主要因为更容易建立可检查、可重复执行的操作流程 |
| 已有 Cadence 工程、元件库、环境和使用习惯 | 通常优先保留现有工程，避免为 AI 操作便利而承担无必要的迁移成本 |
| 大量复杂电气约束、密集高速网络 | Cadence Allegro 的约束管理值得优先评估；仍取决于实际版本和产品授权 |
| 将来明确要求系统 SI/PI/电磁仿真 | Cadence 配套 Sigrity、Clarity 等生态有优势；这是额外能力，不是本次用户提出的任务要求 |

对 AI 而言，“KiCad 更容易设计”这一表述过宽。**准确表述应为：KiCad 更容易让 AI 建立可靠的工程数据读写、精确修改、检查和迭代流程。** 设计判断及电气质量仍需要逐项落实。

补充软件取舍：
- 嘉立创 EDA 专业版：立创选料及嘉立创制造衔接便利，是考虑器件采购和打样流程时的候选工具。
- Altium Designer：若已有 AD 工程、库和使用经验，继续使用也合理；它支持脚本自动化。
- 本次没有实际操作或验证嘉立创 EDA、AD 或 KiCad 的本机环境。

## 5. KiCad 对 AI 的具体便利与边界

### 5.1 便利之处

- 符号、封装、原理图与 PCB 使用有公开文档的文本格式，便于结构化读取、生成与修改。
- 可以取得器件位置、旋转、焊盘、网络、走线、过孔和铜区等设计信息，方便程序处理和前后比较。
- 文本工程便于 Git 跟踪、审阅修改与回退。
- 命令行工具提供 ERC、DRC 及多种输出功能，便于反复检查。
- PCB 自动化接口提供另一条与软件交互的途径；具体能力应按安装版本核实。

这些特点有助于形成：读取数据 → 作出工程判断 → 精确修改 → 检查并查看图形 → 再调整的流程。

### 5.2 不能从这些特点推导出的结论

- 直接改文本不等于工程一定有效，仍需正确处理格式、对象关联、库引用及检查。
- 编程创建线段不等于已经获得完整交互式推挤、绕障或智能布线能力。
- ERC/DRC 和脚本检查不会代替对去耦、回流、供电或 EMI 的工程判断。
- 原理图与 PCB 自动化接口的覆盖范围可能不同，不能宣称所有编辑器均有相同 API 能力。
- 本次没有验证本机 KiCad 安装、版本、接口连接或具体设计操作。
- KiCad 自身具备认真布局布线所需的交互式工具，不应描述为只能完成网络连通。已查阅的 KiCad 10 文档包含推挤布线、差分、按层叠计算走线几何、长度/延时调整和自定义规则。

## 6. Cadence 对 AI 的难点与可行路线

本次 PCB 讨论中的 Cadence 主要指 OrCAD Capture 与 Allegro PCB Editor 配合的流程。

### 6.1 已知自动化途径

- OrCAD Capture：Tcl/Tk 及相应设计数据库接口。
- Allegro PCB Editor：SKILL、数据库接口与脚本机制。
- Padstack Editor：负责相关焊盘/过孔结构的编辑。
- 这里的 SKILL 是 Cadence 的脚本语言，与 AI 助手的技能文件概念不同。

Cadence 支持自动化。不能将其原生工程不便直接按文本修改，描述成“无法操作”或“没有接口”。

### 6.2 实际难点

1. **取得完整设计数据。** 读取菜单/按钮不等于取得 PCB 几何、网络、走线、铜区及参考层关系；需要验证数据库查询或合适的导出方式。
2. **建立执行与反馈通道。** Capture 和 Allegro 使用不同接口，需要分别确认脚本加载、执行、错误处理、保存与修改后查询。
3. **适配实际安装环境。** 按 17.2 的接口、版本补丁、库路径和实际授权工作，不能套用当前新版功能。
4. **控制交互状态。** 精细选择、拖动、推挤与绕障受到当前命令、选择过滤、活动层、缩放和网格等影响。
5. **验证电气相关修改。** 移动电容后，需要检查连接、过孔、铜区及设计规则结果，不能只凭脚本返回成功或画面显示位置变化判断完成。

图形画布操作中的一些困难两款软件都有。KiCad 的优势主要是更容易减少对逐次屏幕点击的依赖；在 Cadence 建立稳定 Tcl/SKILL 通道后，也可以减少这类依赖。

## 7. 本次实际环境证据与验证状态

### 7.1 工作环境

- 操作系统环境：Windows，使用 PowerShell。
- 本次工作目录：D:\001DIY\023USB\08UsbIPDapLink。
- 用户指定的记录文件：D:\001Diy\005lib\01AIEDA\EDA.md。
- 环境信息只作为本次会话快照，后续操作应重新确认当前软件与工程状态。

### 7.2 实际检测到的软件

| 项目 | 本次工具返回的事实 |
| --- | --- |
| OrCAD Capture | 运行中，窗口标题为 OrCAD Capture - [Start Page] |
| Capture 版本 | 启动页控件显示 Installed: 17.2-2016-S045 |
| Capture 可执行文件 | C:\Program0\Cadence\SPB172\tools\bin\Capture.exe |
| PCB Editor | 检测到安装项，检查时没有运行窗口 |
| PCB Editor 可执行文件 | C:\Program0\Cadence\SPB172\tools\bin\allegro.exe |
| Padstack Editor | 检测到安装项，检查时没有运行窗口 |
| Padstack Editor 可执行文件 | C:\Program0\Cadence\SPB172\tools\bin\padstack_editor.exe |

安装项名称和程序存在不证明当前许可证包含哪些编辑或分析能力；本次没有完成许可证档次核验。

### 7.3 已完成和未完成的验证

已完成：
- 通过 Windows 桌面控制工具列出相关软件及运行窗口。
- 选中并读取 OrCAD Capture 窗口控件，取得启动页、菜单和版本信息。
- 定位到本机 Cadence 的 SKILL、Tcl 相关文档目录及部分 HTML 文件名。

遇到的问题：
- Capture 画面截图采集曾返回：FrameArrived timed out: timed out waiting on channel。
- 随后通过重新选择窗口并只读取控件文本成功取得信息。
- 截图问题尚未确认已经解决。

尚未验证：
- Allegro 窗口的读取与控制。
- Capture Tcl 与 Allegro SKILL 的实际加载、执行和数据库反馈。
- 对具体工程的器件移动、焊盘/封装修改、走线编辑、推挤布线、铺铜和保存。
- 本机 KiCad 的安装及实际操作能力。
- 完整设计流程与电气性能检查能力。

本次没有实际打开审查某个原理图/PCB、执行电路设计修改或完成一块板子。不能把“读到了 Capture 窗口”扩大为“已验证完整 Cadence 设计能力”。

### 7.4 已定位的本地文档

文档根目录：C:\Program0\Cadence\SPB172\doc。

已列出的相关目录包括：algroskill、orcadtclgsg、orctclcap、orctclsample、capinfomodel 等。

已定位的文件示例：
- [Allegro SKILL 概述](C:/Program0/Cadence/SPB172/doc/algroskill/01ovrvew.html)
- [Allegro SKILL 数据库访问](C:/Program0/Cadence/SPB172/doc/algroskill/07dbaccs.html)
- [OrCAD Tcl 入门标题页](C:/Program0/Cadence/SPB172/doc/orcadtclgsg/Title_Page.html)

本次确认的是目录与文件存在，尚未逐章读取这些文档或用其中接口完成设计操作。

## 8. 后续协作的工作原则

- 默认持续遵守用户已说明的布局布线质量要求，无需再次把 SI/PI/EMI 理解成仿真任务。
- 先读取实际原理图、PCB、器件数据手册与制造条件，再提出针对具体模块的修改。
- 软件选择以用户现有资产与可验证的执行能力为依据，避免仅凭文件易编辑就要求迁移。
- 对 Cadence，优先在工程副本中验证：读取设计对象 → 精确移动一个器件 → 修改一段连接 → 查询结果并检查 → 保存并重新读取。
- 验证基础操作通道后，再用于去耦、电源或 MCU 等具体模块的专业布局走线。
- 每次说明清楚哪些事实已验证、哪些属于判断、哪些能力仍待验证。
- 设计修改应能解释原因、查看实际结果并回退；不能将 DRC 通过当作全部电气要求已满足。

本次尚未确认具体 MCU 型号、USB 速率、电源拓扑与电流、实际板厂层叠、板框机械约束、制造规则或 EMI 指标，不应替用户擅自补成项目事实。

## 9. 本次查阅的主要官方资料

以下链接用于追溯本次讨论的依据；不能将最新版功能自动视为本机旧版已具备或已授权的功能。

- [KiCad 官网](https://www.kicad.org/)
- [KiCad 文件格式](https://dev-docs.kicad.org/en/file-formats/sexpr-intro/)
- [KiCad IPC API 能力与限制](https://dev-docs.kicad.org/en/apis-and-binding/ipc-api/for-addon-developers/index.html)
- [KiCad 10 命令行检查与导出](https://docs.kicad.org/10.0/en/cli/cli.html)
- [KiCad 10 PCB 编辑器](https://docs.kicad.org/10.0/en/pcbnew/pcbnew.html)
- [Cadence：Allegro SKILL 自动化](https://community.cadence.com/cadence_blogs_8/b/pcb/posts/extending-layout-with-skill)
- [Cadence：OrCAD Capture Tcl/Tk 自动化](https://support1.cadence.com/public/docs/content/20469530.html)
- [Altium Designer 脚本](https://www.altium.com/documentation/altium-designer/scripting)
- [嘉立创 EDA 专业版介绍](https://prodocs.easyeda.com/en/introduction/introduction/index.html)
- [ST：STM32F4 硬件开发与布局指南](https://www.st.com/resource/en/application_note/an4488-getting-started-with-stm32f4xxxx-mcu-hardware-development-stmicroelectronics.pdf)
- [TI：DC/DC 布局与 EMI 控制指南 AN-2155](https://www.ti.com/lit/an/snva638a/snva638a.pdf)
- [Cadence Sigrity](https://www.cadence.com/en_US/home/tools/sigrity-x.html)
- [Cadence Clarity](https://www.cadence.com/en_US/home/tools/system-analysis/em-solver/clarity-3d-solver.html)



## 10. 视频教程学习：流程、产物与能力边界

### 10.1 用户追加的说明与关注

- 用户说明旁边打开的文档属于自己的工程资料；本次没有独立识别其具体文件名或读取工程内容。
- 用户继续探索 EDA 软件的实际使用能力，提出假设：如果提供几乎全部 Cadence 操作视频，AI 能否掌握并使用软件。
- 用户随后关注学习过程如何保存，以及换一台电脑后是否还能继续使用学习成果。
- 这些问题属于能力与保存方式的讨论，不等于已经提供视频、要求创建技能库，或授权修改具体硬件工程。

### 10.2 视频能够提供的操作知识

- 菜单、快捷键、命令、参数和操作顺序。
- 当前命令状态、选择过滤器、活动层、缩放、网格等操作前提。
- 器件精确移动和旋转、焊盘/封装编辑、引脚出线、已有走线调整、推挤、换层与铺铜。
- 布局布线调整的工程理由，以及出错时的判断和恢复方法。
- 教程越贴近实际使用的 Cadence 17.2 版本、越包含完整前后状态和配套工程，越便于复现验证。

视频可以帮助补充操作知识；截图超时、接口连接、脚本执行反馈等环境问题仍须在本机验证，不能靠看完教程直接认定已解决。

### 10.3 建议的学习与验证流程

1. **按具体任务拆分资料。** 例如符号创建、焊盘定义、器件布局、走线调整、铺铜检查，建立主题及视频时间点索引。
2. **提取操作前提和步骤。** 结合可读取的字幕、讲义与关键画面，记录版本、起始状态、菜单/命令、参数及预期结果。长视频分段处理，是否能够抽取画面或转写音频取决于实际文件和工具，不预先认定所有视频链接都可访问或完整读取。
3. **在工程副本中重现。** 通过实际操作核对器件、网络、走线、过孔和铜区的变化；需要时结合软件数据库查询和检查报告。
4. **改变条件再验证。** 换一组器件、方向或布局条件，核查能否正确应用，而非只复制视频中的屏幕坐标。
5. **记录验证结论。** 明确区分“教程中见到”“已在当前版本复现”“仍待验证”，保存失败原因、恢复方法及适用条件。
6. **保存并复用。** 将验证过的流程写成手册；适合确定性执行的部分保存为 Tcl/SKILL 脚本；需要可重复调用时再整理为 Codex 技能。

### 10.4 每项操作建议记录的内容

| 字段 | 记录内容 |
| --- | --- |
| 来源 | 视频文件/链接、时间点、字幕或讲义、关键截图 |
| 环境 | Cadence 产品、版本补丁、必要授权或接口、相关库路径 |
| 目标和前提 | 操作目的、选中对象、当前命令/层/过滤器、起始工程状态 |
| 执行步骤 | 菜单、快捷键、命令、参数或脚本入口 |
| 工程理由 | 为什么这样布局或走线，以及与回路、供电、参考平面和 EMI 的关系 |
| 成功判据 | 实际对象和连接变化、图形审查、相关规则检查结果 |
| 验证状态 | 已复现或待验证、验证样例、失败原因、恢复/回退方法 |

例如 MCU 去耦布局，需要同时记录“如何移动、旋转并连接电容”和“依据供电引脚、接地过孔及完整回路选择位置的理由”。学习软件操作始终服务于用户已说明的电气质量要求。

### 10.5 学习的含义

- 本次所说“学习”，指在对话中理解资料，并把可复用知识保存为文档、示例和脚本，后续读取后应用。
- 阅读视频不会直接、永久修改当前模型本身的参数。
- 看过教程不等于已经能够稳定执行；完整掌握某项任务需要实际操作和结果验证。
- 当前聊天上下文有助于连续讨论，不能作为完整长期操作库的唯一保存方式。

## 11. 学习成果保存与跨电脑复用

### 11.1 推荐保存的产物

| 产物 | 用途 | 跨电脑复用方式 |
| --- | --- | --- |
| EDA.md | 保存总体要求、选择依据、环境证据、学习索引和进度 | 复制/同步文件后让助手读取 |
| 分主题 Markdown 手册及关键截图 | 保存操作前提、步骤、理由和验证结论 | 随资料文件夹迁移，按任务查阅 |
| Tcl/SKILL 脚本 | 复用已验证的确定性操作 | 迁移后适配新电脑路径和软件环境，并重新验证 |
| Codex 技能文件夹 | 用 SKILL.md 声明适用任务、流程、检查方式，并关联资料和脚本 | 在新电脑支持的位置配置/安装后调用 |
| 示例工程 | 保存操作前后样例，支持复现与核对 | 随工程及依赖库迁移 |
| 云文档 | 跨电脑查阅文字资料 | 两台电脑均取得相应服务访问权限后读取 |

Codex 技能由 SKILL.md 及可选 references、scripts、assets 等资源组成。技能需要被新电脑上的客户端发现或显式读取；仅有文件不保证已经加载。这里的技能与 Cadence SKILL 脚本语言是两个不同概念。

推荐以 D:\001Diy\005lib\01AIEDA 作为资料的统一整理目录，按需要设置操作手册、脚本、关键截图、示例工程及技能等子目录。**这是讨论中的建议，目前没有创建这些子目录或新增技能。**

### 11.2 本地文件、云文档与本地记忆的区别

- 已保存的 EDA.md 是本机文件；本次没有另外创建云文档或配置上传/同步。
- 可以按用户选择，通过复制、备份、同步盘或 Git 仓库迁移资料。这些是可选方案，本次没有执行任何上传、远程仓库创建或同步配置。
- 云文档方便跨电脑查阅；本地脚本、示例工程与软件环境仍需在执行操作的电脑上可用。
- 根据本次查阅的官方文档，Codex 有独立的本地记忆功能，可从符合条件的历史聊天中生成本地记忆文件；默认位置位于 Codex home 下的 memories 目录，通常是 ~/.codex/memories。
- 本次没有检查该电脑的记忆功能是否启用，也没有确认本次聊天已被写入自动记忆。
- 本地记忆是辅助回忆层。重要规则、完整操作手册和脚本应保存在明确的文档/技能中。
- 仅登录相同账号，不能假定本地资料、技能、记忆和软件配置全部自动同步到另一台电脑。

### 11.3 换电脑后继续工作的条件

1. 将操作手册、脚本、截图、示例工程和技能等所需资料复制或同步到新电脑。
2. 告知助手资料的实际位置，先读取总体记录及与当前任务相关的操作文档。
3. 如需按技能调用，将技能配置到当前客户端支持的位置并确认可用。
4. 核对新电脑的 Cadence 产品版本、许可证、元件/封装库、工程依赖及路径。
5. 重新验证桌面控制、截图反馈、Capture Tcl、Allegro SKILL 和设计数据库查询等所需通道。
6. 在工程副本中执行一项小范围操作，核查结果后再继续具体设计任务。

资料保留后可以利用既有知识继续工作；新电脑上的执行能力仍须结合环境验证，不能照搬旧电脑的窗口状态、屏幕坐标、临时对象或绝对路径。

### 11.4 本次会话结束时的实际状态

- 已保存：本文件中的设计要求、软件比较、环境检测、能力边界，以及视频学习和跨电脑复用的讨论。
- 尚未接收并学习任何 Cadence 操作视频。
- 尚未创建 Cadence 操作技能、视频知识库或 Tcl/SKILL 操作脚本。
- 尚未创建云文档、上传资料或配置跨电脑同步。
- 尚未核验自动本地记忆的启用或生成状态。
- 尚未完成前文列明的 Allegro 读写和精细布局布线验证。
- 后续开始视频学习时，应逐项追加来源、步骤和实际验证结果，保持计划、资料内容与已验证能力分开记录。

## 12. 视频学习与持久保存相关的补充官方资料

- [OpenAI：图像输入](https://learn.chatgpt.com/docs/image-inputs)
- [OpenAI：桌面操作](https://learn.chatgpt.com/docs/computer-use)
- [OpenAI：构建与加载技能](https://learn.chatgpt.com/docs/build-skills)
- [OpenAI：Codex 本地记忆](https://learn.chatgpt.com/docs/customization/memories)

以上平台功能说明属于本次查阅时的资料。后续迁移或配置时，应核对实际客户端版本与可用功能。



## 13. 新电脑续学与目录整理日志（2026-10-17）

### 13.1 用户本轮要求

- 换电脑后按原计划继续学习并做好记录；用户说明环境基本一致。
- 将当前学习计划放在 EDA.md 开头。
- 将学习资料、记录、脚本和练习成果统一到 D:\001Diy\005lib\01AIEDA。
- 用户询问 native pipe 找不到的含义：它是 Codex Windows 桌面控制工具与本机控制服务的通信通道未连接，不是已确认的 Cadence 程序或工程文件缺失；具体原因未确定。

### 13.2 本轮环境核查

| 项目 | 结果与依据 |
| --- | --- |
| EDA.md 迁移前内容 | 23857 字节，SHA256：92BF200D1FB3F7A291DF273A6CE7B3D1DD6C135D8E1A45D6D8E6EF1C184BBD90，与旧机最终保存一致 |
| Cadence 程序 | C:\Program0\Cadence\SPB172\tools\bin 下 Capture.exe、allegro.exe、padstack_editor.exe 均存在；文件版本为 17.2-2016 |
| 运行状态 | 核查时未发现上述三个运行进程 |
| 实际 HOME | 当前进程环境为 C:\Program0\Cadence\SPB_Data；只读核查，未修改 |
| 旧笔记 HOME | SPBData172 与本轮实际 HOME 不同，不能照抄为新机配置 |
| 初始化文件 | 本轮检查的实际 HOME/pcbenv、旧 SPBData172/pcbenv 以及安装目录两个常见位置均未发现 allegro.ilinit；未穷举所有可能的启动入口 |
| 桌面控制 | sky.list_apps 返回 Computer Use native pipe is unavailable，os error 2；未据此认定 Cadence 内部接口不可用 |
| PowerShell 脚本文件 | 直接调用本地 .ps1 被当前执行策略拒绝；本轮未修改策略 |
| Tcl 运行时 | C:\Program0\Cadence\SPB172\tcltk\bin\tclsh.exe 执行只读 info 探针成功，TclVersion=8.6，PatchLevel=8.6.0 |
| 原有公共库目录 | 01captureLib、01Pad_lib、01Psm_lib、01script_file 存在；作为既有环境依赖保留引用，不将软件安装及公共库误当学习临时目录 |

### 13.3 已阅读的资料与第一课结论

本轮实际阅读了本机官方文档的以下内容：

- [Capture Tcl 环境介绍](C:/Program0/Cadence/SPB172/doc/orcadtclgsg/Introduction_to_the_OrCAD_TCL_Environment.html)：命令窗入口为 View → Toolbar → Command Window；Capture 内置 Tcl 可访问界面及其数据库。
- [Capture Tcl 环境设置](C:/Program0/Cadence/SPB172/doc/orcadtclgsg/Setting_up_the_OrCAD_TCL_Environment.html)：17.2 随安装提供 Tcl/Tk，文档列 Tcl 8.6；独立解释器与 Capture 内部命令需分别验证。
- [Allegro AXL-SKILL 概述](C:/Program0/Cadence/SPB172/doc/algroskill/01ovrvew.html)：AXL-SKILL 提供数据库、显示和界面访问；程序启动会读取相应 env/ilinit；具体加载位置必须结合实际环境核查。
- [axlDBGetDesign 说明](C:/Program0/Cadence/SPB172/doc/algroskill/07dbaccs.html)：返回根设计 dbid 或 nil；整体器件/网络查询优先访问设计属性，不能把根设计对象直接当普通可编辑对象。

第一课需要保留的操作知识：

1. 独立 tclsh 成功只验证 Tcl 运行时，不验证 Capture 的设计数据库命令。
2. Allegro 对象 dbid 有作用域与生命周期；切换设计、某些编辑和 shell 命令后需要重新取得/刷新，不能跨会话保存临时对象。
3. 选取过滤器和可见层会影响基于选择的查询；全板清单优先采用数据库集合查询，并核对查询范围。
4. 历史笔记记载过桥接和布线实验，但本轮没有复核那些板子、数量和性能数据，不能直接记为当前新机成果。

### 13.4 路径与编码整理

- 旧 D:\001DIY\005lib\01AIcadence 目录的桥接、watcher 和 exchange 关键路径均不存在，现有资料实际位于 01AIEDA。
- 本轮发现 31 个文本脚本/操作文档含旧目录引用，采用完整 ASCII 目录段替换为 01AIEDA；迁移前原字节保存在 backups 下，逐文件变更及哈希见迁移清单。
- 对旧笔记中非 UTF-8 的文件，严格 UTF-8 解码失败后用 GB18030 读取可恢复中文。本轮路径替换保留原编码和换行，不把显示乱码直接认定成原文件损坏。
- 当前桥接原 command.il 属于另一工程，包含停止桥接和加载另一项目脚本的操作。本轮先备份，再将默认测试入口改为只读查询；不创建 command.flag，不执行该历史命令。
- 桥接路径整理不等于桥接恢复成功。加载入口已集中到 ai_bridge 下，实际加载、IPC watcher、命令/结果往返仍待 Allegro 内验证。
- 执行 load_bridge.scr 会通过 ai_bridge.il 末尾的 AIB_start() 自动启动 watcher，属于实际运行操作；本轮仅准备入口，尚未加载或启动。
- 本轮没有修改全局 HOME，也没有把旧笔记中的 ilinit 自动配置直接套到新机。

### 13.5 教程材料状态

- 支持按任务读取文本 PDF、扫描/图片 PDF 及混合 PDF；需要核对模糊文字、引脚号、尺寸和软件截图。
- 用户曾请求《Cadence 17.2 电路设计与仿真从入门到精通》（ISBN 9787115508805）。此前找到公开试读和正版在线阅读/借阅入口，但没有取得完整电子书文件。
- 本轮目录检查发现一个 .crdownload 未完成下载文件；它不算已取得的完整 PDF。本轮未改名或继续该下载。
- 尚未接收完整教程视频或可用的完整教程 PDF，当前学习来源为本地官方帮助及现有笔记。

### 13.6 本轮产物与待验证项

- EDA.md：开头新增当前阶段计划，末尾追加本日志，保留原讨论。
- learning/scripts/probe_tcl_readonly.tcl：只读版本与可执行路径探针，可先用于独立 Tcl，后续在 Capture 中按实际接口加载。
- learning/scripts/probe_allegro_readonly.il：准备的只读设计名、器件数与网络数查询，尚未在 Allegro 内执行。
- ai_bridge/load_bridge.scr：集中保存的桥接加载入口，尚未执行。
- learning/logs/environment_20261017.json：本轮核查结果与验证状态。
- backups 下的迁移清单：逐文件原哈希、更新后哈希及备份位置。

下一步先解决/确认桌面控制服务连接，并在 Cadence 内验证只读查询和结果返回；随后按 P2—P7 进行实际练习。后续每次学习继续维护本文开头的状态和相应日志。



## 14. 第 2 课：新机 Allegro 内部只读查询实测（2026-10-17）

### 14.1 本课成果
- 实测 allegro.exe -version 返回 17.2-S045；成功运行日志确认 Windows SPB 64-bit Edition。Capture 与 Padstack Editor 的补丁/授权未由此得到验证。
- 通过官方 -s / -readonly / -nographic 入口，在学习目录的官方示例板副本中执行 SKILL，报告返回 COMPLETE。
- 查询到 57 个器件、95 个网络、59 个 symbol、("mils" 0) 单位/精度和 PRIMARY 层叠的 6 个铜层。
- 使用安装自带脚本的 set NOCONFIRM + quit + fillin "yes" 退出组合，程序自行退出，journal 正常结束；源样例及运行副本 SHA256 一致。
- 这是软件内只读查询与结果返回的验证，不代表布局/布线、Capture Tcl、IPC 桥接或电气质量审查已完成。

### 14.2 操作知识与限制
1. 先读单位，再解释几何数据。完整层叠含空气和介质，铜层数按 conductor 属性区分。
2. 根设计 bBox 是设计图形范围，不是制造板框；原始报告字段 board_bbox 命名不够准确，脚本已修正为 design_bbox，原报告保留。
3. 本例存储 DRC 数为 0，但 drcState=nil，不能判定 DRC 通过；本课未重新执行 DRC。
4. GND/VCC 层名不证明实际铜区连续或网络归属正确；SI/PI/EMI 检查仍须落实到实际位置、铜、走线和回流路径。
5. 当前示例为 6 层，只用于接口和数据库学习；两层/四层练习按原计划另行建立。
6. -safe 是诊断模式；-readonly 禁保存设计，但仍产生运行日志和锁文件。只对本次子进程设置 ALLEGRO_PCBENV，未主动修改全局 HOME 或用户启动文件。

### 14.3 故障、纠正及通道状态
- Windows 桌面连接本轮重新核查：sky.list_windows() 仍返回 native pipe unavailable / os error 2。未点击、键入或更改服务配置；原因仍未确定。
- 首次脚本的 skill exit(0) 没有使进程退出；在报告完整返回后，仅结束已确认的本次 PID 1612。原因未确定。
- 第二次采用官方 mgx 脚本的 quit 退出方式，PID 22116 自行退出。PowerShell ExitCode 为空，未将它记为 0；以报告完成、进程退出、journal 结束、板哈希一致核验。
- 官方自带退出脚本也使用 LF，不能把首次失败归因于换行。Windows -nographic 在本次指定配置已实测可用，不泛化到所有交互命令。
- 没有加载 ai_bridge，没有启动其 watcher，没有创建 command.flag；官方 -s 查询成功与现有 IPC 桥接成功是两项验收。

### 14.4 记录和下一步
详细命令、结果、来源与复现限制见 [第 2 课笔记](learning/notes/lesson02_allegro_readonly_20261017.md)。
成功运行证据保存在 learning/logs/lesson02_readonly_quit_20261017；状态汇总见 learning/logs/lesson02_result_20261017.json；更新前文件保存在 backups/lesson02_20261017。

下一步继续读取器件、封装、引脚与网络对应关系及几何，接入 P2 焊盘/封装核对；桌面操作和 Capture 内部 Tcl 保持独立待验证项。


## 15. 第 3 课：器件—封装—引脚—网络与几何（2026-10-17）

### 15.1 实操结果
在新的官方示例板副本中执行两次只读 SKILL，均返回 COMPLETE、正常退出，journal 正常结束；原样例和副本 SHA256 一致。
- 57 个器件：56 已放置，Y1 未放置；640 个 component pin 中 636 有物理定义，4 个为 Y1 逻辑引脚。
- 59 个 symbol：56 PACKAGE + 3 MECHANICAL，不能把 symbol 数直接当电气器件数。
- 12 个 padstack、95 个网络、748 条功能引脚记录；器件 owner、已放置 pin 的 symbol membership、functionPin 回链不一致均为 0。
- 功能引脚多对一：748 行覆盖 556 个唯一物理编号，另有 84 个 pin 无 functionPins；不能把功能记录数当焊盘数。
- 已导出器件、符号、引脚、功能引脚、按层焊盘、padstack 和网络 7 份 TSV。

### 15.2 关键操作知识
- component->name 才是器件位号；pin->number 是编号，pin->name 是 padstack 名；功能名来自 functionPins。
- 未放置 pin 可能返回 (0,0)，须结合 component->symbol 和 pin->definition 判断，不能当作真实摆放位置。
- pin->xy/rotation 为绝对位置/方向；relxy/relRotation 相对未旋转、未镜像的封装定义。C1 镜像实测说明直接加坐标会算错。
- 共享焊盘定义标 TOP/TOP，不代表镜像实例也在 TOP。C1 的 SMD 实例在 BOTTOM，TOP 查询返回 NULL。
- axlDBGetPad 的对象存在不证明有铜焊盘；应区分 NULL、实际层和 suppression。pad->bBox 为局部坐标，本课还实测了实例 polygon 的板上范围。
- 本课读到了孔径、孔型、阻焊范围和模板尺寸，未按器件数据手册验收，不能宣称封装正确或布局电气质量合格。

### 15.3 保留问题与能力边界
C1 同一 polygon 的 bbox 与 vertices Y 坐标有 0.5 mil 差异。官方帮助未找到确切解释，原因待核；不据该样例给制造尺寸/边缘间距合格判定。
本次没有 Capture 原理图对照，use 字段也没有 POWER/GROUND 记录；只核对 PCB 内部数据对应关系。
桌面连接本课未重试，沿用上课不可用状态；未运行 ai_bridge、watcher 或 command.flag，没有修改真实工程。

### 15.4 资料和下一课
详细步骤、具体 IC/电容例子和官方出处见 [第 3 课笔记](learning/notes/lesson03_mapping_geometry_20261017.md)。
实测数据在 learning/logs/lesson03_mapping_20261017/run01 与 run02_geometry；汇总见 learning/logs/lesson03_result_20261017.json。
下一课进入 P2：练习 Padstack 和简单封装创建/编辑、保存、重新打开与尺寸读回。真实器件库仍需依据具体数据手册。


## 16. 第 4 课：真实创建焊盘与两脚练习封装（2026-10-17）

### 16.1 已完成
- 官方 Padstack Editor -x 读取新建 PXML，生成独立 .pad；其 journal 确认版本 17.2-S045。
- Allegro 新建 PACKAGE drawing，创建编号 1/2、丝印、装配外形、填充 Place Bound 和 U* 位号占位文字，保存 .dra、编译 .psm。
- 另起只读进程重开磁盘 .dra，核对引脚、铜/阻焊/锡膏、轮廓端点/线宽/闭合、边界填充与位号；18 项规格/持久性检查通过。
- native 编译日志完成，DRC 日志为 0，重开 drcState=t；不将此当作真实器件、制造或 SI/PI/EMI 验收。
- .pad/.dra/.psm 重开前后哈希一致，所有测试进程已退出。

### 16.2 练习尺寸与文件
使用毫米、精度 3；引脚中心 (-1,0)/(1,0)，中心距 2 mm；TOP 铜 1.0×1.5、阻焊 1.1×1.6、锡膏 0.9×1.4 mm，无孔。
丝印中心线范围 3.4×2.0 mm、线宽 0.10；装配范围 1.6×1.0、线宽 0.05；填充 Place Bound 3.6×2.2 mm。
这些尺寸仅用于课程，不对应某真实器件推荐封装。

产物在 learning/examples/lesson04_package/library：
eda_l04_smd_1000x1500.pad（3648 字节）、eda_l04_two_pin_training.dra（65556 字节）、同名 .psm（6644 字节）。
独立规格为上层 training_spec.json；preview.png 是数据库查询绘制预览，不是 Cadence 截图。

### 16.3 本课纠正与保留问题
- 新 drawing 默认 extents 不包含负坐标，第一次 pin 创建失败；显式设 (-10,-10)～(10,10) mm 后解决。
- REF** 占位文字被接口拒绝；采用官方 U* 示例后成功。
- FULL_GEOMETRY 实际返回独立 line；补读直接 line/arc 后取得 8 条外形线段，不能把先前 segments=0 当作外形缺失。
- Windows PID 可复用，进程判断结合程序名、启动时间及 WaitForExit；原始失败证据均保留。
- XML 导入及新绘图区单位设置有 SPMHUT-48 舍入警告，具体字段未指出；已核对规格未见偏差。上课 0.5 mil 差异仍未解决。
- 未放置 .psm 到 PCB，未建配套 Capture 符号，未做真实器件数据手册认证。

### 16.4 记录与下一步
详细操作和官方来源见 [第 4 课笔记](learning/notes/lesson04_pad_package_20261017.md)。
脚本为 learning/scripts/lesson04_create.*、lesson04_verify.*；原始过程在 learning/logs/lesson04_package_20261017/run01—run06 对应目录；汇总为 learning/logs/lesson04_result_20261017.json。
下一课验证编译封装在练习 PCB 中的放置、旋转、镜像及引脚/图层映射。用户原有工程和全局 HOME/启动文件未主动修改。


## 17. 用户指定封装文字与高度默认规范（2026-10-17）

用户明确要求后续封装文字至少包含 REF DES/SILKSCREEN_TOP、REF DES/ASSEMBLY_TOP、COMPONENT VALUE/ASSEMBLY_TOP，三个文字锚点均在器件原点中心 (0,0)；默认 package height 1 mm。

本轮已记录为本文开头的默认规范，并更新当前两脚练习 .dra/.psm：
- 原有顶层位号 U* 从 (0,1.6) 移至 (0,0)。
- 增加装配层位号 U* 和装配层 VALUE 占位，坐标均为 (0,0)。
- 填充 PLACE_BOUND_TOP 写入 PACKAGE_HEIGHT_MAX="1 MM"，仅设 MAX 时默认下界为 0。
- 新进程只读重开，三个文字坐标及高度属性均核对成功；保存/编译日志完成，重开未改变已保存文件哈希。
- 本次只修改原有教学封装，不改其他工程；修改前库文件、规格和预览已备份。

长期规范见 learning/notes/package_defaults.md；日志见 learning/logs/package_defaults_20261017；最新规格与预览仍在 learning/examples/lesson04_package。
第 4 课原始笔记、原始日志和原始哈希保留为历史快照；最新封装以本节与新的验证结果为准。该封装仍是自定义两脚 SMD 练习尺寸，尚未按真实器件数据手册认证。


## 18. 完整课程目录与索引位置（2026-10-17）

用户要求补全将要学习的全部课程，并将索引从 learning 移到 01AIEDA 根目录。本轮确认实际文件为 D:\001DIY\005lib\01AIEDA\课程索引.md，原 learning 下同名文件不存在。已在根目录补全 60 课主线、5 个按需进阶专题、每课主要内容/验收/状态及已有记录链接。覆盖库与 Capture、MCU/电源/滤波/接口原理图、布局、两层/四层逐段走线、SI/PI/EMI 基本设计要求、生产输出、综合工程、实物闭环及资料迁移。三文字层原点和默认高度 1 mm 已纳入封装验收。第 5 课及以后仍为计划，本轮没有执行这些后续课程。

## 19. QMI8610 真实 PCB 封装与公共库交付（2026-10-18）

用户指定源 D:\004Document\016Sensor\06IMU\矽睿\QMI8610 Datasheet Rev. A.pdf，要求按 lib文本索引.md 存入公共库。讨论 Capture 能力时已如实说明：此前完成的是 PCB 焊盘/封装，Capture 创建保存 OLB 尚未实操；用户最终明确“那就只做pcb封装”。本轮范围固定为 PCB，不创建原理图符号。

已完成 qmi8610_lga16_3d3_p0d5.dra/.psm → 01Psm_lib，qmi8610_smd061x032_m05_p100.pad → 01Pad_lib。采用指定 Rev A 第 79 页推荐 land：本体3.30×3.30、16脚、pitch0.50、铜0.61×0.32、最大高度1mm；第8页核顶视编号与中心不可焊接，未增中心焊盘。阻焊铜每边外扩0.05、钢网1:1为单独记录的工程选择。

三项指定文字锚点均为(0,0)，填充 Place Bound 上 PACKAGE_HEIGHT_MAX="1 MM"。原生保存/编译完成，独立重开16pins/0DRC/drcState=t，逐项核尺寸/旋转/轮廓/文字/高度。公共副本哈希与已核验版本一致，公共DRA独立重开无变化；编译PSM从公共路径载入新练习PCB，顶层0°、顶层90°、底层镜像共48pins变换检查通过。

本次知识修正：axlDBGetPad(pin) 的局部 bbox 已包含 pin 旋转；保存前 root pins 列表本次未及时反映创建结果，保存后和新进程重开均正确。首次失败尝试、SPMHUT-48警告及修正过程完整保留。使用原生命令通道不代表桌面 native pipe 恢复；Capture 仅查官方 Tcl 启动示例，仍未执行内部接口验证。

完整出处、规格、工程取值、复现步骤与边界见 [QMI8610案例](learning/examples/qmi8610/README.md)，课程关联见 [实操笔记](learning/notes/qmi8610_package_20261018.md)。本次完成第8课真实器件封装CAD实操，并覆盖第5课部分实例变换内容；第5课剩余项目和Capture课程仍待学习。用户真实硬件工程与全局环境未改动。

## 20. 第 5—7 课续学与实操验收（2026-10-18）

用户授权继续下一步或两三课程，并要求完整记录、确认真正学过。本轮完成第5课声明范围、第7课基础孔/层叠声明范围，以及第6课原生接口子项；界面和未验收工程项明确保留，不把读资料或试过一次当作掌握。

| 课程 | 本轮已实操并验收 | 状态及边界 |
| --- | --- | --- |
| 5 PCB实例变换 | 公共PSM载入；真实move/rotate/mirror；48pins×6层、铜多边形、9文字和3PB高度；保存重开；独立复现实验 | 本课声明范围完成。独立验证13,088项通过。初次返回类型包装错误与Qt退出ASSERT保留；新的repeat创建/重开均exit0、12份TSV一致、ASSERT未复现，原因未定位 |
| 6 精确操作与回退 | 可见性、过滤框选、网格显式恢复；事务Start/Mark/Oops/Rollback/Commit；9个小坐标量化；0.101mm线bbox/vertices；提交后重开 | 原生子项通过，整课部分完成。桌面仍native pipe缺失；交互菜单/视图/撤销待做；半DBU差异已在新mm/3板复现，旧mil/0根因仍未证明 |
| 7 孔与层叠 | PTH、带铜环NPTH、镀铜slot；0°/90°6pins；package保存编译重开；TOP-L2-L3-BOTTOM四层映射重开；默认文字/高度重开 | 基础几何/层叠范围完成，650项几何检查通过。纯无铜NPTH无人值守干净导入、真实dynamicshape避铜、负片thermal flash和制造输出仍未验收 |

完整学习笔记：
- [第5课：实例移动/旋转/镜像](learning/notes/lesson05_instances_20261018.md)
- [第6课：精确坐标/过滤/网格/事务](learning/notes/lesson06_operations_20261018.md)
- [第7课：PTH/NPTH/槽孔/层叠](learning/notes/lesson07_padstacks_20261018.md)

每课均保留源码、SCR入口、练习原生文件、原始失败尝试、stdout/stderr/journal、启动参数/进程结束、只读前后哈希与JSON外部验收。产物分别在learning/examples/lesson05_instances、lesson06_operations、lesson07_padstacks；本轮统一验收索引见learning/logs/lessons05_07_result_20261018.json。

第7课警告已实际学习并保留：
1. NULL机械孔先定义ANTI却无THERMAL，触发三层配对警告。
2. 改为NULL+KEEPOUT后，因无有效pad支撑Keepout被删除，并提示无默认内部pad；这是实际定义失效，不能当作避铜通过。
3. 官方允许的会被钻掉的小spot pad仍触发“drill exceeds pad”尺寸警告，是用途可解释但批处理有警告的案例，未擅自关闭校验。
4. 最终另建有铜环的NON_PLATED孔教学样例，正常导入并读回；它不是对纯无铜孔的伪修复。孔壁镀铜与板面铜环、跨层连接是不同概念。
5. 圆孔实测用drillDiameter，drillSizeWidth/Height返回0；槽孔用Width/Height核X/Y，不能用单一diameter概括槽。详细出处与证据见第7课笔记。

公共QMI8610库及用户实际硬件工程未修改；隔离实验脚本不改变全局HOME/快捷方式。成功的原生操作不表示桌面连接已恢复。

## 21. 用户固定PCB层名和光绘模板规则（2026-10-18）

用户明确要求：2层TOP-BOTTOM；4层TOP-L2-L3-BOTTOM；6层TOP-L2-L3-L4-L5-BOTTOM；更多层按TOP、L2至L(N−1)、BOTTOM延伸。今后所有PCB建板及设计遵守大写准确名称和物理次序，层功能另行记录，保持现有快捷方式与模板可用。

D:\001DIY\005lib\01env\drill*.txt 是对应光绘层信息/脚本。本轮只读盘点13份并保存各文件原始SHA、铜Film/ETCH映射；未执行、未改模板或快捷方式。第7四层练习实际读回TOP-L2-L3-BOTTOM。

发现一处现有模板差异：drill12.txt第67—72行多定义L12/ETCH/L12，整个铜Film名单为TOP,L2…L12,BOTTOM，共13项；按12层规则应到L11。此差异已单列，未擅改文件。Film的?sequence参数不能代替Cross Section物理次序。

长期规范见 [pcb_layer_naming.md](learning/notes/pcb_layer_naming.md)，原始盘点见 [模板清单](learning/logs/layer_template_inventory_20261018.json)。

## 22. 另一个窗口提供的extracta方法（2026-10-18）

用户提供了另窗口说明截图：通过Cadence原生extracta读取BRD并导出网络/引脚、器件、线段、过孔、层及已保存检查统计。该方法有助于后续精细几何核验，本轮确认17.2安装目录有extracta.exe，并查到官方ecoms/echap.html的extracta帮助；本轮没有运行截图对应工程。

截图具体统计作为另窗口报告来源保留，实际结论需关联源BRD、模板、日志。布线、回流、差分间距、PI/SI/EMI质量仍按实际铜、层叠和设计意图审查。详细方法及待实测项见 [extracta记录](learning/notes/extracta_readback_20261018.md)。

## 23. 学习中转文件目录失误与整改（2026-10-18）

用户已要求所有学习资料集中于 D:\001DIY\005lib\01AIEDA。本次仍在 C:\Users\Administrator\AppData\Local\Temp 创建了中转脚本、JSON输入包、笔记草稿和子任务审查文件；工具变更列表显示其中6个文件，用户据此指出目录不一致。

这是执行失误：把可写Temp当作中转位置，没有把统一目录要求落实到每个阶段和子任务。随后只核对了正式笔记路径，回答“没有换总目录”时漏说外部中转文件，说明不完整。不能以“只是临时文件”排除用户的统一存放要求。

整改已完成：明确白名单中的29份中转文件全部复制到 learning/staging_archive_20261018/files，逐项SHA256一致后清理对应Temp原副本；仅清理本任务文件，其他Temp内容未动。正式课程笔记、脚本、日志和练习文件保留原位置，没有用旧草稿覆盖当前版本。迁移清单见 [manifest.json](learning/staging_archive_20261018/manifest.json)。

预防规则：
- 后续自行创建的脚本、草稿、中转文件统一放 learning/staging 或本课隔离目录，全路径必须在01AIEDA内部。
- 分派子任务时同时明确此规则；不再让子任务先写系统Temp再统一归档。
- 工具默认目录或权限问题不构成擅自换目录的理由，使用可写入已授权目标的文件操作通道；若无法实现则明确说明实际阻碍。
- 每次结束前盘点根记录、分课笔记、脚本、日志、练习和中转文件；说明当前实际位置，不以工具变更面板代替完整文件清单。
- 迁移先复制、校验、保存清单，再清理本任务原副本；备份与历史输入也留在01AIEDA。

长期执行规范见 [record_location_rules.md](learning/notes/record_location_rules.md)。正式公共库交付继续遵守用户指定的lib文本索引.md；其学习资料和过程记录仍统一存入01AIEDA。

## 24. B阶段第7—10课全部完成与完整记录（2026-10-18）

按用户“今天把B.焊盘与物理封装第7—10课学习完毕后做好所有记录”的要求，已完成本阶段原生CAD实操、独立重开验收和完整笔记。当前进度以本节及本文开头为准；第20节等历史快照中的第7课待验收项已由本轮补齐。

| 课号 | 本次完成与验收 | 完整记录 |
| --- | --- | --- |
| 7 | 纯NULL NPTH、独立有效keepout、四层实际除铜、负片四辐条FSM及正片真实GND热连接；受控穿孔产生2条DRC，rollback后0DRC/state=t；补验157项PASS | [基础](learning/notes/lesson07_padstacks_20261018.md) / [补齐](learning/notes/lesson07_completion_20261018.md) |
| 8 | QMI8610指定Rev A来源/尺寸/16脚/无中心焊盘，原生文件与公共库SHA复核，文字/高度及原PSM变换证据通过 | [完整复习](learning/notes/lesson08_real_package_20261018.md) |
| 9 | LQFP48与QFN16+EP17、厂家单窗/教学4窗、5个原生热via；3封装9实例246pin，独立读回PASS | [完整笔记](learning/notes/lesson09_qfn_qfp_20261018.md) |
| 10 | USB4105-GF-A的12land/16接点映射、4槽脚、2NPTH、板边/插拔辅助边界和真实高度；3实例保存重开，1765项PASS | [完整笔记](learning/notes/lesson10_connector_20261018.md) |

统一复习入口：[B阶段完成记录](learning/notes/lessonB_07_10_20261018.md)；来源、输入、全部成功/失败脚本、PXML、原生文件、日志、读回、验收JSON、预览与SHA清单均在01AIEDA内。总索引：[验收及文件清单](learning/logs/b_lessons_07_10_20261018.json)。本次新建教学封装只放学习目录，未发布公共库；既有QMI8610公共库哈希不变。

已记录重要修正：BOUNDARY创建net参数会被忽略，须显式赋网并核实际铜；正片0.127热辐条与负片FSM0.3来自不同定义；槽方向看真实polygon而非OBLONG_X名称；提取对象重复看dbid；连接器尺寸箭头基准、开口方向与插入运动分别核对。纯NULL孔用途性警告和受控终止状态完整保留，未靠假铜环或关闭校验消除。

三文字锚点(0,0)与固定层名继续遵守。真实最大高度按手册覆盖初始化1mm：LQFP48=1.6MM，USB4105=3.46MM，板下stake另算。QFN原点丝印与EP开窗冲突已记录，实际PCB应移动实例位号并检查输出。

完成范围是焊盘与物理封装CAD课程；第9热孔为无网几何样例，第9/10验证板DRC状态nil、连接器STEP缺失、制造/焊接和板级SI/PI/EMI未据此认证。桌面native pipe仍不可用；第6课GUI待续，下一主线第11课Capture基本操作与内部Tcl接口。

## 25. C阶段第11—14课原生实作、验收和完整记录（2026-10-19）

按用户要求继续学习Capture符号与库管理，学习记录、脚本、失败快照、JSON及原生文件全部留在01AIEDA内，未自行使用系统Temp中转。完整入口：[C阶段学习记录](learning/notes/lessonC_11_14_20261019.md)。根课程索引和本文更新前已备份到backups/before_capture_C_20261019。

| 课号 | 本轮实作与验收 | 完整记录 |
| --- | --- | --- |
| 11 | 官方17.2 DLL/Tcl8.6原生会话；DSN的TOP/两页/U101；未保存丢弃、标脏保存、基线恢复、新进程重开；OPJ已生成并核资源路径 | [第11课](learning/notes/lesson11_capture_basics_20261019.md)；GUI命令窗/OPJ图形打开未验，整体保留部分完成 |
| 12 | QMI8610指定RevA，HOST_I2C/HOST_SPI4两套16脚OLB；304项源表独立比较，保存重开及单单元suffix修订通过 | [第12课](learning/notes/lesson12_capture_symbols_20261019.md)；新工程用_single正式库 |
| 13 | 74HC00四门同base U1、完整U1A—U1D、14个物理编号；alias/off-page/hierarchical port/global/visible POWER/bus；v8独立重开17/17项 | [第13课](learning/notes/lesson13_completion_20261019.md) |
| 14 | 既有工程由V1更新V2；受控ReplaceInst加显式位号/覆盖策略；独立重开81/81项，10个唯一连接成员不变，OLB/PAD/DRA/PSM齐全 | [第14课](learning/notes/lesson14_library_propagation_20261019.md)；GUI缓存菜单与失败API不计通过 |

最终入口：第11课[final目录](learning/examples/lesson11_capture/final)、第12课[I²C正式库](learning/examples/lesson12_capture/c12_qmi8610_single.olb)和[SPI4正式库](learning/examples/lesson12_capture/c12_qmi8610_spi4_single.olb)、第13课[c13_scope_v8.dsn](learning/examples/lesson13_capture/c13_scope_v8.dsn)、第14课[c14_ready.dsn](learning/examples/lesson14_capture/final/c14_ready.dsn)。第14课ready为库关联教学工程，V2/MPN为传播试验字符串，继续真实设计前应恢复真实Value/料号并完成后续电路审查。

重要修正已保存：新页面必须SavePage后SaveDesign；修改已有实例需MarkModified后保存；完整位号从PlacedInst读取，不能把raw Reference当full；visible POWER的rawGlobal=1不能代替实际网络作用域；多页TOP需按实测安全路线展开，完整单页重复Expand会产生重复旧容器。UpdateCache返回success但未传播不算成功，实际通过的是受控替换和保存重读。

用户看到的tclsh应用程序错误与即时调试器选择框来自本轮原生探索异常，未主动打开VS。危险NULL转换/FlatNet迭代入口已停用；检查时异常进程已退出，未更改系统调试器设置、未终止不明归属Capture。详见[异常事件记录](learning/logs/capture_C_20261019/native_exception_incident_20261019.md)。

公共元件库和用户Cadence环境未修改。历史B8发布路径中的公共QMI文件本轮未找到；当前可用物理依赖以学习目录现存副本为准，第14课final/library复制件SHA与B8学习源相同。本节代表当前状态，前面各日期的旧进度保留历史。

统一SHA/链接核对清单：[c_stage_manifest.json](learning/logs/capture_C_20261019/c_stage_manifest.json)。GUI通道恢复后先补第11课和Cache菜单；随后主线第15课，单片机教程仍暂缓，不将当前原生结果写成C阶段无条件全部完成。

## 26. D与E第15—26课合并学习和完整工程记录（2026-10-19）

用户决定把工程需求/MCU与电源/接口/原理图审查合并学习。本轮选STM32F103C8T6 LQFP48，串联9—16V受控输入、反极性与保险丝、TPS54202 5V、TLV75533P 3.3V、MCU供电/BOOT/复位/SWD/8MHz晶体/ADC及USB-C/CAN/UART/I2C/SPI。全部来源、草稿、脚本、JSON、BOM、原生文件、失败及备份放在01AIEDA内。

完整入口：[第15—26课合并记录](learning/notes/lessonDE_15_26_20261019.md)；[MCU第15—19课](learning/notes/lessonDE_mcu_15_19_20261019.md)、[电源/接口第20—25课](learning/notes/lessonDE_power_interfaces_20_25_20261019.md)、[第26课真实后端](learning/notes/lesson26_native_backend_20261019.md)。保留原课号，课程总目录已合并为D/E单元。

权威基线：[DE_CONTROL.opj](learning/examples/de_15_26_20261019/native/DE_CONTROL.opj) / [de_integrated_single.dsn](learning/examples/de_15_26_20261019/native/de_integrated_single.dsn)。ECO：[de_integrated_eco_final.dsn](learning/examples/de_15_26_20261019/native/de_integrated_eco_final.dsn)。实际板：[DE_BASELINE.brd](learning/examples/de_15_26_20261019/native_flow_final/DE_BASELINE.brd)和[DE_ECO.brd](learning/examples/de_15_26_20261019/native_flow_final/DE_ECO.brd)。同为80件、272物理pin、69net、266连接及6明确NC；BRD为尚未放置/布线的逻辑导入基线。

本轮实际验收：原生DSN读回与自定义规则1519项通过；MCU独立复核53项；电源接口独立复核1577项；准备库19种封装原生装载/保存/新进程重开717项（实际电路用18种，SMB为未用候选）；真实PST→BRD→ECO逐pin/net/value/footprint1578项通过。各类检查存在重叠，不加总。逆向VIEW/SWP比较无非预期改名/交换/属性变化；GUI应用SWP另列待验。

ECO明确只有R19/R20上拉2.2k→3.3k和J13.7/J13.8的PB8/PB9互换，MCU45/46不动，无增删件或其他网络变化。电阻源描述也修为3.3k1%并重跑最终后端。基线2.2k优先继续，ECO3.3k/100pF的Fast-mode上升沿预算余量较小；教学默认I2C100kHz，400kHz需另核实际时序。

主要学习修正：USB/CAN共享专用RAM不能并行；USB4105的12land/16电气pad编号与Capture必须逐脚对应；TCAN332的5/8脚均NC；USB VBUS只做检测/ESD，不反供板；晶体负载电容按CL/ESR/C0/stray计算；ADC低频输入的1k+100nF不是100S/s抗混叠证明；LDO反灌不能由有无EN推定。BOM已保留完整容差/耐压/装配/采购状态，未选料不伪造MPN。

最终教学约束由120mA/0—50℃修订为正常总负载150mA、0—40℃、GPIO及全部header外载合计≤10mA；这是MCU全速+CAN重载+上拉/偏置预算核对后的修正。最坏一阶LDO结温估算约105.7℃，不是实板热测试。故障电流、浪涌与系统ESD不据此保证；最终采购和实板释放条件独立保留。

六页原生设计虽然几何存盘，Expand/PST包装只产生部分连通并报错，根因未解决；采用通过全部网络与物理导入验收的单页六模块版，失败文件留历史不冒称已修复。初次SKILL退出异常及逆向缺cdsz回退DAT的信息完整保留，没有用部分DAT导入出的BRD当成功。当前原生层序真实读回TOP/未命名介质/BOTTOM，仅为逻辑承载板，生产层叠待第28课。

当前第15—25课完成范围是资料、计算、约束和原生CAD；第26课GUI完整ERC/应用SWP尚未验收，硬件上电/晶振/ADC/USB/CAN/温升/反灌及后续PCB布局布线/制造均未冒称完成。下次从第27课板框机械基准继续，既有GUI待验项并行保留。

统一交付/哈希/链接清单：[deliverable_manifest.json](learning/logs/de_15_26_20261019/deliverable_manifest.json)。更新前根记录和课程索引已备份在backups/before_DE_15_26_20261019，原预算快照另存learning/staging/de_15_26_20261019。
