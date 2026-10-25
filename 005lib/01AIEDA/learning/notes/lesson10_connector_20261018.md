# 第10课：连接器与受机械约束的PCB封装

日期：2026-10-18，Asia/Shanghai。学习总目录始终为 D:\001DIY\005lib\01AIEDA。

本课已完成声明范围的原生软件实操：按原厂图纸建立真实USB-C连接器的PAD/DRA/PSM，保存、编译、新进程只读重开；在独立PCB放置顶层0°、顶层90°、底层镜像3个实例，再次重开，独立验收。完成不代表实物制造认证、全部连接器工艺掌握或3D装配验证。

## 1. 资料、料号与证据

- 选型：GCT（Global Connector Technology）USB4105-GF-A；USB2.0 Type-C、16接点、PCB顶装、SMT信号端子和4个壳体插脚、2个塑料定位柱。
- 原厂图：USB4105，Rev B4，18/12/23，第1/2页；[原厂下载](https://gct.co/files/drawings/usb4105.pdf)。
- 本地原件：[usb4105.pdf](../examples/lesson10_connector_20261018/source/usb4105.pdf)，164547字节。
- SHA256：FB331FBABEE8392ED2937ED757C1610CB0F174B84625147C0B580A18EEA8C0E5。
- 使用第1页完整图、推荐PCB布局、侧视、正视和底视。完整渲染及3处放大图在该课 source/；文字提取仅为辅助，尺寸基准和合并焊盘必须看图。
- Allegro原生版本17.2 S045 Windows SPB 64-bit Edition，见 create_package/allegro.jrl。没有依靠无法连接的桌面控制，也没有自造UI自动化。

先尝试Molex 105164-0001官网，下载超时；Amphenol 10118194官网及官方CDN返回5604字节HTML访问挑战，未取得PDF。失败响应已明确改名为 failed*.html，不能因为扩展名原为.pdf就把它当图纸。原GCT产品页也返回HTML挑战；GCT图纸直链成功。全部下载和失败资料都在01AIEDA内。

## 2. 视图、原点及尺寸基准

推荐PCB图明确是“从器件侧观察”。最终封装是顶面器件侧视图；未直接照抄底视图。+X向右，+Y进入PCB；本体名义中心是原点(0,0)，接口开口朝−Y。外部插头从−Y侧插入时，运动方向是+Y；拔出运动为−Y。

原厂尺寸必须先找到箭头两端：

| 原厂标注 | 正确基准 | 换算为PCB Edge起的Y | 本课以本体中心为原点的Y |
| --- | --- | --- | --- |
| 前壳脚中心至PCB Edge 2.60 | PCB Edge→前槽中心 | 2.600 | -1.075 |
| 两排壳脚中心距4.18 | 前槽中心→后槽中心 | 6.780 | 3.105 |
| 定位孔至前壳脚中心3.68 | 前槽中心→定位孔中心 | 6.280 | 2.605 |
| 12land下缘与后槽中心同线 | 加上land半高1.15/2 | 7.355 | 3.680 |

独立交叉审核曾把4.18、3.68误认为从PCB Edge起算；第二次放大图核对箭头后已纠正。最终尺寸有根任务独立确认，不使用初读误值。预防：先写尺寸链和零点，再输入坐标；对称性和外观看似合理不能代替基准核对。

本体名义8.94×7.35mm，装配线为x=±4.47、y=±3.675；PCB Edge为y=-3.675。辅助板边线是 PACKAGE GEOMETRY/USER_BOARD_EDGE，不能当成自动切板线；练习板真正板框在 BOARD GEOMETRY/OUTLINE。

## 3. 16接点与12块铜的关系

原厂推荐land只有12块铜：4对GND/VBUS接点各共用一块0.60mm宽land，另8个独立信号land宽0.30mm，全部高1.15mm。不能把它误造为16块独立焊盘，更不能随意合并数据或CC端子。

| 从左到右的本课PAD号 | 原厂接点 | 功能 | X / mm |
| --- | --- | --- | --- |
| A1_B12 | A1、B12 | GND | -3.20 |
| A4_B9 | A4、B9 | VBUS | -2.40 |
| B8 | B8 | SBU2 | -1.75 |
| A5 | A5 | CC1 | -1.25 |
| B7 | B7 | Dn2 | -0.75 |
| A6 | A6 | Dp1 | -0.25 |
| A7 | A7 | Dn1 | 0.25 |
| B6 | B6 | Dp2 | 0.75 |
| A8 | A8 | SBU1 | 1.25 |
| B5 | B5 | CC2 | 1.75 |
| B4_A9 | B4、A9 | VBUS | 2.40 |
| B1_A12 | B1、A12 | GND | 3.20 |

全部Y=3.680mm。这些合并PAD号是本课明确的工具映射，不冒充厂家16个接点编号。后续Capture逻辑件必须把配对GND/VBUS接点归属到这些合并PAD号；也可另行实现并验收多个逻辑pin共用一个物理land，但未经验证的通用16pin符号不能直接关联本课12land封装。A6与B6、A7与B7在本课没有隐式短接，网络和USB实际布线由后续原理图/PCB设计处理。

## 4. 孔、壳脚与工艺边界

4个壳体焊接插脚本课用SH1～SH4命名，明确是本地工具编号。原厂信号表列SHELL=GND；实际工程仍应明确屏蔽壳、机壳地及电路地如何连接，本课没有给PCB实例强行赋网。

| 对象 | 中心坐标 / mm | 孔 | 铜land |
| --- | --- | --- | --- |
| SH1、SH2 后排 | (±4.32, 3.105) | 长圆槽0.60×1.70 | 长圆1.00×2.10 |
| SH3、SH4 前排 | (±4.32, -1.075) | 长圆槽0.60×1.40 | 长圆1.00×1.80 |
| 2个定位孔 | (±2.89, 2.605) | Ø0.65，NPTH | 无铜 |

长圆槽沿本地Y长轴。原生数据库figureName为OBLONG_X，但实际TOP铜poly bbox、vertices确认1.00×2.10和1.00×1.80，不能仅凭名称中的X猜方向；90°实例的实际铜bbox变成2.10×1.00或1.80×1.00，孔定义尺寸保留0.60×1.70/1.40而pin rotation=90°，对应旋转后的槽轴。

图纸明确了槽和solder area尺寸，未明确写孔壁镀铜规范。本课选择镀铜槽来练习混合安装封装及保留0.20mm名义铜环；这是工艺选择，不能拿壳体表面镀层证明孔壁镀层。制造前应与连接器装配工艺及板厂确认成品槽孔尺寸、公差、镀孔方式和铜环能力。

定位孔是 MECH_HOLE、NON_PLATED、机械pin、空编号。BEGIN/DEFAULT_INTERNAL/END三层REGULAR_PAD均为NONE(数据库NULL)，无ANTI、THERMAL或padstack KEEPOUT。不能为了消警告加假铜环。孔周独立的0.85×0.85mm filled ROUTE KEEPOUT/ALL在封装中创建，作为教学保守禁布区，不冒充厂家给定避铜要求。

阻焊：铜land每侧外扩0.05mm；NPTH两面开窗Ø0.75mm。SMT排相邻最小阻焊桥0.10mm，需按实际板厂确认。SMT锡膏暂等于铜land，这是软件练习初值；壳体通孔槽未开锡膏，原图没有提供钢网/PIP图。是否穿孔回流、手工或其他装配方式及钢网开口属于工艺释放条件，不能从“封装保存成功”推断焊接必然合格。

## 5. 边界、限高、插拔空间

- 三项文字：REF DES/SILKSCREEN_TOP、REF DES/ASSEMBLY_TOP、COMPONENT VALUE/ASSEMBLY_TOP，全部锚点(0,0)，按用户要求保留。占位文本J*、J*、VALUE。
- 用户1mm是初始化默认。真实连接器侧视板上高度3.31mm，无单独公差，按X.XX一般公差±0.15取MAX=3.46 MM，写在filled PLACE_BOUND_TOP。不能用前开口高度2.56±0.04或默认1mm替代器件限高。
- 壳脚S=0.95±0.15mm，范围0.80～1.10mm，自器件安装基准面向下量至脚尖，不能直接称PCB底面后的突出量；与板上3.46mm高度分别处理。实际突出量需代入板厚、座高及公差。定位柱长度未在使用图中给出，不虚构。
- 放置边界(-5.12,-4.00)～(5.12,4.555)，容纳本体、铜/阻焊和教学放置余量；它不是厂家要求的courtyard。
- 插拔辅助矩形(-6,-15.675)～(6,-3.675)，即开口前方12mm、宽12mm，为本课工程预留示例。PACKAGE GEOMETRY/USER_MATING_TOP及BOTTOM成对建立，镜像实例实际映射到底面辅助层。
- 辅助矩形只供机械审阅，未自动转成PLACE KEEPOUT或布线禁止区。实际项目应根据选定插头、线缆弯曲、外壳和装配操作空间建立有效约束。
- 图中1.85 MIN和插头6.5 MAX不是完整插头和线缆的3D包络。没有取得可靠STEP，未虚构模型或宣称3D干涉验收；可用3D资料缺失已记录。

官方CAD服务搜索结果曾显示USB4105-15-A-120（1.20mm壳脚）变体，和本课GF-A默认0.95mm不同；没有用错变体模型替代。下载和访问状态见source/downloads.json。

## 6. 实际执行流程和如何复现

工作目录：[lesson10_connector_20261018](../examples/lesson10_connector_20261018/)；脚本、下载、日志、运行目录、JSON、预览全部在该课目录内。

1. prepare_lesson10.py整理机械尺寸表、16接点到12land映射、5种PXML和.scr。
2. run_lesson10.py pads逐个调用官方 padstack_editor.exe -x 导入。全部保留正常检查，不使用nocheck。
3. run_lesson10.py package用 allegro.exe -product Allegro_performance -safe -nographic -symbol package加载官方SKILL，生成18个对象：12电气land、4电气壳脚、2机械NPTH，建立装配/丝印/边界/文字/高度/辅助层，保存DRA并编译PSM。
4. run_lesson10.py read_package在新进程-readonly重开，导出pins/geometry/symbols/summary，读取前后DRA SHA一致。
5. run_lesson10.py board在新PCB放3实例，并设置TOP .035 / dielectric .730 / BOTTOM .035mm，总厚0.8mm。此为教学机械条件，非厂家推荐制造层叠；实际板厚公差仍需复核。层名严格TOP-BOTTOM，未改01env/drill*.txt。
6. run_lesson10.py read_board新进程只读重开，54个pin、324条各层读回行；BRD SHA不变。
7. validate_lesson10.py独立从原厂图尺寸转录spec与native数据逐项对比，生成verification/validation.json和preview.svg/png。预览依据真实重开数据生成，不是Cadence截图。

执行器防止覆盖已有PAD/设计或已有launch.json，复现请用新的隔离案例目录并调整对应guard/路径；不能盲目重跑去覆盖本课证据。保存会使旧dbid失效，后续必须重新取对象。应用使用独立ALLEGRO_PCBENV、TEMP/TMP和cwd，不修改全局HOME或公共库。

## 7. 验收结果、警告与修正

- 5种PAD已生成，DRA/PSM已生成并通过原生保存/编译；package编译报告No DRC errors，重开drcs=0、drcState=t。
- 顶层0°实例(-15,0)、顶层90°实例(26.325,12)、底层镜像实例(15,0)实际加载PSM成功。未变换坐标、相对坐标、编号、几何、铜/阻焊/锡膏层映射均逐项核验。
- 顶层0°与底层镜像接口板边线均在y=-3.675；90°接口板边线在x=30，均与真正PCB轮廓对应。
- 每个实例对应的filled边界和3.46 MM高度、三文字的实例原点、2个独立NPTH禁布形状及插拔辅助线变换已验。
- 独立验收1765项PASS。该数字包括逐对象/逐层检查，仅作为证据索引；不是制造合格或全部SI/PI/EMI通过的证明。
- 练习板保存的drcs=0但drcState=nil：没有宣称PCB完整DRC通过，更没有拿连通性代替机械或信号完整性审阅。本课是物理封装与机械约束，不含完整USB布线。
- SPMHUT-48“Scaled value has been rounded off”在单位/空白设计初始化出现，完整jrl保留。实际关键几何按0.001mm精度读回合格，未删除警告。
- NPTH导入日志保留“No default internal pads are defined”。对纯无铜机械孔这是用途性警告；导入已写出.pad，但原生警告窗口阻塞退出，执行器25秒后仅终止自己Popen拥有的进程（PID/startUTC/终止码均记录），随后用Allegro加载、编译、重开证明孔与全NULL铜。不能把这次导入说成正常exit0，也不使用假铜环/关闭检查消警。
- 本课不再出现“有ANTI未定义THERMAL”或“单独KEEPOUT无regular被删除”警告，因为NPTH不使用那些组合。
- 准备脚本首次写入因scripts子目录未建失败，随后先建课内目录再写，未转移到Temp。
- 独立校验首次因原生OBLONG_X别名失败，随后又发现旋转实例pad bbox已含pin方向。修正为独立期待的0/90°尺寸、真实铜poly绝对bbox、relxy和rotation全量核对；不是放宽检查掩盖错误。DRA/PSM未因这两项校验器修正而修改。
- 预览初稿把开口朝−Y写成插入运动朝−Y，根任务指出后已改为“opening −Y / plug insertion +Y”。

## 8. 交付和学习边界

- [规格和映射](../examples/lesson10_connector_20261018/spec.json)
- [完整验收JSON](../examples/lesson10_connector_20261018/verification/validation.json)
- [封装预览](../examples/lesson10_connector_20261018/preview.png)
- library/内的5组PXML/PAD及l10_gct_usb4105_gf_a_12land.dra/.psm。
- lesson10_connector.brd独立实例板；日志在logs/，源代码在scripts/，源图在source/，全文件清单和SHA在manifest.json。
- 没有改用户工程、公共库、HOME或01env，也没有生成Capture符号。此案例放在学习区，制造与逻辑符号映射未释放前不作为通用公共量产库发布。

本课可复用的能力：以原厂图建立统一机械基准；区分接点与合并铜land；区分壳体插脚、塑料定位柱、镀孔工艺及NPTH禁布；落实真实限高与从安装基准面量起的壳脚长度；建立板边/插拔参考；用原生保存编译和独立几何验证证明旋转/底层镜像结果。真实外壳/线缆完整3D、钢网释放和制造认证需要项目资料与工艺条件，不在本次软件课程完成声明中。

## 2026-10-19复核勘误：壳脚S基准

后续F课程重新核图确认，S是器件安装基准面至脚尖长度，并非穿过任意PCB后的板底突出量。此前“板下侵入”措辞不够准确，正文已更正；0.8mm板的算例不能推广为1.6mm板也有同样突出。原生封装铜/孔/高度不变，既有2026-10-18清单保留当时快照，本次笔记修订身份纳入F阶段新清单。完整依据和工艺条件见[来源与机械基准勘误](lessonF_source_corrections_20261019.md)。
