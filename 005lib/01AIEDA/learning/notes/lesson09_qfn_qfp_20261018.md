# 第9课：QFP、QFN与裸露焊盘封装

日期：2026-10-18（Asia/Shanghai）。Cadence 17.2 S045 Windows 64-bit；全部资料、脚本、草稿、日志、练习、校验与预览均在 D:\001DIY\005lib\01AIEDA 内。本课未发布到公共库，也未修改用户工程、HOME、01env或快捷方式。

**已完成本课的软件实操范围：真实 LQFP48 与 QFN16+EP17 的厂家资料核对、细间距编号与坐标生成、铜/阻焊/锡膏定义、中心裸露焊盘独立编号、厂家单窗和教学分窗、独立热过孔几何示例、保存编译、独立进程重开，以及9个放置/90°旋转/底层镜像实例的验收。** 最终机器校验为 [validation.json](../examples/lesson09_qfn_qfp_20261018/validation.json) 中 PASS_CAD_LESSON09。制造焊接、热性能和板级电气/SI/PI/EMI没有据此宣称通过。

统一练习入口：[lesson09_qfn_qfp_20261018](../examples/lesson09_qfn_qfp_20261018)。[几何预览](../examples/lesson09_qfn_qfp_20261018/preview/lesson09_footprints.png) 根据保存后原生读回数据绘制，不是Cadence界面截图；引脚数字为可读示意。

## 1. 学习目标与实际产物

| 实际器件/版本 | DRA/PSM名（均位于本课library） | 实际用途 |
| --- | --- | --- |
| ST STM32F103C8T6，LQFP48 | l09_stm32f103c8_lqfp48 | 48脚0.5mm细间距、厂家PCB land、视图旋转、真实1.6mm高度 |
| TI TPS62130RGTR，RGT0016C | l09_tps62130_rgt16_single | 16个外围端子与独立EP17；厂家单窗锡膏参考 |
| 同一TI器件，教学分窗版本 | l09_tps62130_rgt16_split | 铜、阻焊、编号相同，中心锡膏改4窗，演示工程推导与工艺条件 |
| 独立热过孔示例 | l09_thermal_via020_c040.pad | 孔0.2mm、铜0.4mm；四层几何读回；并非已接地/已填孔生产设计 |
| 9个放置实例验证板 | l09_placement_4layer.brd | 三个封装各TOP0°、TOP90°、BOTTOM0°；共246个pin和5个原生唯一via对象 |

关键文件还包括 lesson09_spec.json、scripts、logs、source、evidence及manifest.json。课程索引和EDA总记录由主任务统一更新。

## 2. 资料来源、页码与真实性

全部直接下载厂家公开PDF。来源链接与日期在 [download_provenance.json](../examples/lesson09_qfn_qfp_20261018/source/download_provenance.json)，PDF元数据、页数与SHA在 [source/manifest.json](../examples/lesson09_qfn_qfp_20261018/source/manifest.json)。本课同时提取全文并渲染机械/land/装配页，不能只靠文本识别来判断视图。

| PDF | 官网/文档 | 本次实读PDF页码 | SHA256 |
| --- | --- | --- | --- |
| stm32f103c8_official.pdf | [ST原文](https://www.st.com/resource/en/datasheet/stm32f103c8.pdf)，DS5319 Rev20 | 98：top/bottom机械图；99：Table62尺寸/最大高度；100：Figure56 PCB footprint | 1E54CE18E6C34C5B4A78986F26E245E143748C721009FC9AF5953795C30686BC |
| tps62130_official.pdf | [TI原文](https://www.ti.com/lit/ds/symlink/tps62130.pdf)，SLVSAG7F；附图RGT0016C 4222419/E 07/2025 | 3：pin用途与EP接地；28：布局要求；40：器件机械；41：PCB land；42：钢网 | F9B1AF285622C0CF1A5991F9641A6E64C5E6D899E52CC0B1632808742019579F |
| slua271b_official.pdf | [TI装配appnote](https://www.ti.com/lit/an/slua271b/slua271b.pdf)，实际下载内容为SLUA271C，2023-12 | 7：EP/热孔/填塞盖油；10：钢网厚度；11：面积比/分窗覆盖 | 4693FD4DF14F57F67088D881B9509A56DB4A084A333CAAC53F81BC5C800B23CE |

注意：SLUA271的URL含b，但内容已经是RevC，应按正文版本记录；TI datasheet主文版本日期2021、附封装图2025、PDF元数据生成2026-09-04可以不同，不能混成单一日期。ST PDF实际页数114而页脚总页数115，证据引用以本地PDF顺序页码为准。

本课使用的是厂家明确标注的PCB land/footprint example，并非直接把IC引线或底部端子尺寸复制成PCB焊盘。ST图100与TI图41分别是PCB依据；图98/99和TI图40仅负责本体/终端/高度/视图核对。

## 3. QFP48：视图、编号与坐标

ST图100推荐land：径向长度1.20、切向宽度0.30、pitch0.50，外跨9.70，内缘间距7.30。径向中心由两条独立尺寸计算：9.70/2−1.20/2=4.25；7.30/2+1.20/2=4.25，两式一致。每边12脚的切向中心是±2.75，外围切向总宽5.80=11×0.50+0.30。

图100原图pin1在底边左端；本课整体顺时针旋转90°，让pin1位于左边上端。转换是(x,y)→(y,−x)，必须对编号、land、本体和pin1标记一起处理，不能只旋焊盘。当前顶视坐标：

- pin1=(-4.25,+2.75)，pin12=(-4.25,−2.75)。
- pin13=(-2.75,−4.25)，pin24=(+2.75,−4.25)。
- pin25=(+4.25,−2.75)，pin36=(+4.25,+2.75)。
- pin37=(+2.75,+4.25)，pin48=(−2.75,+4.25)。

绕器件中心按顶视逆时针递增。上下边的长方形land旋转90°。机械图98同时出现top与bottom view；不能把其中bottom视图当顶层直接描。

QFP铜1.20×0.30、阻焊1.30×0.40（每边外扩0.05）、锡膏1.20×0.30。阻焊和锡膏是教学工程选择，ST图100没有给出完整阻焊/钢网工艺定义。名义同排铜间隙0.20、阻焊桥0.10，应与板厂公差核对。无孔、无底层铜/阻焊/锡膏。

高度按Table62 Amax=1.60mm，PLACE_BOUND_TOP写 PACKAGE_HEIGHT_MAX="1.6 MM"。用户1mm是初始化默认值，真实器件大于1mm不能继续用1mm限制机械占用。7mm本体和pad包络分别核对，放置边界10.2×10.2mm为本课保守工程选择，并非厂家规定courtyard。

## 4. QFN16+EP17：外围与中心焊盘

本课采用当前官方RGT0016C附图，不能与网上旧RGT land（例如0.85×0.28、EP2.1）混用。TI图41给外围land0.60×0.24、pitch0.50、对边中心线跨2.80，因此径向中心±1.40，切向±0.75/±0.25。

顶视pin1=(-1.40,+0.75)，1—4沿左边向下；5—8沿底边向右；9—12沿右边向上；13—16沿顶边向左。图40底视图要与图3顶视功能图及图41PCB图交叉核对，不能再次镜像编号。

图41规定 ALL PAD CORNERS R0.05。本课铜外围0.60×0.24 R0.05，EP铜1.68×1.68 R0.05，原生读回 figureName=ROUNDED_RECTANGLE、radius=0.05、corners=UR-UL-LL-LR；没有用矩形/oblong近似后称为厂家精确形状。

外围阻焊0.74×0.38 R0.12，EP阻焊1.82×1.82 R0.12：每边扩0.07，采用NSMD。TI图41的NSMD开窗允许每边至0.07的示意边界，本课取该值，仍需板厂确认。外围相邻铜间隙0.26、最小名义阻焊桥0.12；EP到外围径向铜间隙也是1.40−0.30−0.84=0.26，阻焊间隔0.12。

**EP必须是独立电气pin17，不能仅画无编号铜形状。** TI图42明确将中心焊盘标为17；图3要求EP连接AGND6、PGND15/16和公共地平面，且必须焊接以保证机械可靠性与散热。16脚名称不代表可以遗漏第17个物理/电气端子。本课只做PCB库，未来原理图符号也应包含17并匹配。

QFN器件本体名义3×3、最大3.1×3.1mm，assembly按最大3.1绘制；高度图40最大1.0mm，与用户默认一致。PLACE_BOUND_TOP写"1 MM"；边界3.9×3.9mm是教学放置间隔选择。

## 5. 锡膏分区、开放率及钢网条件

两个QFN版本的铜/阻焊/编号完全相同，只有中心锡膏不同。必须区分型号特定推荐和通用工程方案。

| 方案 | 中心paste | 面积/开放率 | 适用说明 |
| --- | --- | --- | --- |
| 厂家参考single | 1.55×1.55 R0.05单窗 | 2.400354mm² / 2.820254mm² = 85.1113% | TI图42称约85%，基于0.125mm厚钢网；本课照图实现 |
| 教学split | 四个0.65×0.65方窗，中心(±0.425,±0.425) | 合计1.690000mm²；相对圆角EP=59.9237% | 根据SLUA271C通用50—70%范围设计的分窗练习；不是该RGT型号图42原样推荐 |

分窗之间横纵沟槽0.20mm，整体包络1.50×1.50、相对EP边缘留0.09mm。若用1.68²矩形包络作分母则59.8781%，与按真实圆角铜面积59.9237%不同，应明确分母。圆角面积采用 A=W×H−(4−π)r²；原生polygon面积已独立比对，不只比较bbox。

外围锡膏按图42为0.60×0.24 R0.05，与外围铜相同；不得把EP也一律做1:1满开。过多中心锡膏可能抬高器件并影响外围焊接；窗口形状/分区需与钢网厚度、锡膏颗粒、印刷转移、回流、空洞目标及X-ray检验相配合。

以0.125mm钢网计算：分窗方口area ratio=A/(perimeter×T)=0.65/(4×0.125)=1.30；外围圆角口按真实面积与周长约0.7119，宽厚比0.24/0.125=1.92。SLUA271C图11讨论面积比0.66和宽厚比1.5；本课仅几何满足参考值，不代表实际印刷试验通过。钢网增厚至0.15mm会降低外围面积比，不能随意沿用0.125结论。

实现方式：single中心paste在EP padstack中定义；split的EP padstack不定义paste，4个填充矩形放在 PACKAGE GEOMETRY/PASTEMASK_TOP。不能保留EP pad里的满开paste再叠4窗，否则叠加结果仍可能满开。独立读回确认split EP的PIN/PASTEMASK_TOP为NULL，PACKAGE层确实4窗，且底层实例变为PASTEMASK_BOTTOM。

## 6. 热过孔：实做几何与工艺边界

在隔离四层验证板上，TOP0°的split QFN中心位于(-20,-15)。按TI图41的示例放5个独立via：中心1个和(±0.58,±0.58)四个；孔Ø0.20、铜Ø0.40，名义铜环每侧0.10。via padstack有TOP/DEFAULT_INTERNAL/BOTTOM regular，未定义ANTI/THERMAL/KEEPOUT，未触发用户截图的反焊盘缺thermal警告。不能为了消警告加入与用途无关的热焊盘定义。

实际板铜层为TOP–L2–L3–BOTTOM；via在四铜层均读到Ø0.40、PLATED、isThrough=t。双面mask/paste的独立via开口为NULL。但**via本身无mask开口不等于EP区顶部盖油**：EP整体1.82阻焊开窗仍使顶部via位置暴露。铜孔CAD不能证明树脂填孔、塞孔、电镀盖帽或工厂已完成盖油；放在paste下面的孔必须按TI图41与装配厂确认处理，避免吸锡/空洞。

这些热孔放在board，不固化进每个footprint。不同层数、损耗、地平面面积、板厚和制造能力可能需要不同数量/孔径/接地方式。必须评估孔径/板厚纵横比、镀铜、孔环、填塞盖帽平整度和返修条件。通用appnote的Ø0.3/约1mm起点与本器件图41的Ø0.2/±0.58示例是不同层级建议，本课采用器件图41作几何示例。

本板是未导入逻辑组件的几何实例，5个via读回net为空。本课不把它称为EP接地电连接已实现。曾尝试对未赋逻辑实例pin执行axlDBAssignNet，原生拒绝“Cannot change net on unnassigned pin”；已保留日志并改成明确无网几何示例。实际工程必须在正确网表/逻辑元件导入后，把EP17、AGND6、PGND15/16及热孔连到规定公共地，并检查真实铜连接和回流路径。

FULL_GEOMETRY提取按层重复via，原始输出25行不能当25个via；也不能仅按相同坐标去重证明没有重复对象。补做独立原生只读审计，按dbid去重得到**5个不同对象**，且原生断言length(ids)==5通过：[via_ids.tsv](../examples/lesson09_qfn_qfp_20261018/logs/via_ids_reopen/via_ids.tsv)、via_complete.txt。

## 7. 用户固定文字、层名与丝印冲突

三项文字锚点均独立读回(0,0)：REF DES/SILKSCREEN_TOP、REF DES/ASSEMBLY_TOP、COMPONENT VALUE/ASSEMBLY_TOP。位号U*、值VALUE是占位；坐标是器件局部原点，放入PCB后随器件变换。高度显式带MM单位。

QFN有一个必须公开保留的冲突：按用户强制把silk REF DES锚点放原点，字形会落在中心EP阻焊开窗/器件覆盖区。原点规则已满足，但不能因此宣称丝印可生产。真实PCB应把可见位号挪至器件外适当位置，或按板厂规则在制造光绘中裁掉/隐藏焊盘和器件下的丝印；库仍保留用户规定的默认对象。外围丝印角线与pin1标记不替代这项输出检查。

层名遵守用户规则：2层TOP–BOTTOM；4层TOP–L2–L3–BOTTOM；更多层按序延伸。DEFAULT_INTERNAL是padstack默认内层定义，不是实际PCB层名。01env drill*.txt与快捷方式未改。

## 8. 原生操作顺序、入口与API

1. 读取本机官方Padstack XML DTD/样例与AXL帮助。
2. scripts/prepare.py生成5种PXML、3份create IL/SCR和明确几何spec；源文件在本课目录。
3. padstack_editor.exe -x <pxml>官方非图形导入，检查生成.pad与log。5种最终padstack日志均只有Info-Processing。
4. allegro.exe -product Allegro_performance -safe -nographic -symbol package创建隔离空DRA。脚本仅接受指定新drawing名、空pin列表。
5. axlDBChangeDesignUnits("millimeters" 3)、对称extents；process-local padpath/psmpath只指本课library。
6. axlLoadPadstack、axlDBCreatePin（明确编号/坐标/角度）、axlDBCreateLine（assembly/silk）、axlDBCreateRectangle（filled placebound及paste窗）、axlDBCreateText、axlDBAddProp。
7. axlSaveDesign与axlCompileSymbol生成DRA/PSM；save后重新获取dbid，不能使用失效旧对象。
8. 每个DRA用新进程-readonly重开，scripts/lesson09.il导出pin、pad bbox/radius/corners、placed polygon面积/顶点、shape、text、height与DRC状态。
9. axlXSectionCreate建立L2/L3，在隔离板用axlDBCreateSymbol装入PSM各3种变换，创建5独立via并保存板。
10. 板新进程-readonly重开；再以scripts/via_ids.il按真实对象dbid补验。
11. scripts/validate.py独立比较公式、source尺寸、逐pin变换、圆角面积与9个实例，输出validation.json；scripts/preview.py根据读回数据绘图。

本课调用的是官方CLI/SKILL，不是模拟自造UI。具体菜单/鼠标流程没有冒充已逐步操作；已完成可重现、可读回的数据创建与变换实操。-safe仅用于隔离验证，不改变用户正常启动配置。

官方实现依据：share/pcb/xml-formats/cdn_padstack.dtd，share/pcb/examples/padstack_xml/via1.pxml（ROUNDED_RECTANGLE/corner/ul/ur/ll/lr）；doc/algroskill/02dbdesc.html（pad radius/corners）；03dbcre8.html（Pin/Symbol/Via/Shape/Text）；04parmgt.html（axlIsLayer）；26logacc.html（AssignNet及其对象限制）。

## 9. 验收结果与证据位置

三个封装的create日志均有L09 CREATE COMPLETE，DRA和PSM真实存在；最终reopen03均有L09 READ COMPLETE，原生进程exitCode=0，DRA前后SHA一致。三个封装读取stored drcs=0且drcState=t。

| 验收项 | 实测结果 |
| --- | --- |
| 编号/坐标/视图/原点 | 48、17、17个唯一连续编号；全部逐脚核对 |
| 铜/阻焊/锡膏/孔 | 每脚实值、旋转bbox、圆角半径/4角、实际polygon面积通过；SMD无孔/底层NULL |
| 三项文字/高度 | 三层锚点均0,0；QFP1.6MM，QFN1MM |
| PSM装入 | 三封装各TOP0、TOP90、BOTTOM0，共9实例246脚；逐脚绝对/相对坐标及TOP/BOTTOM铜层验证通过 |
| split镜像 | 每个实例4窗，底层变为PASTEMASK_BOTTOM，单窗面积0.4225总1.69 |
| 四层名/热孔 | TOP/L2/L3/BOTTOM顺序正确；5唯一原生dbid，Ø0.2镀铜孔、四层Ø0.4铜 |
| 只读性 | 3个DRA、placement板及via补验板SHA均不变 |
| 板DRC | stored0，但drcState=nil；**没有把它声明为当前全板DRC通过** |

最终日志：logs/l09_stm32f103c8_lqfp48_reopen03、l09_tps62130_rgt16_single_reopen03、l09_tps62130_rgt16_split_reopen03、board_create03、board_reopen、via_ids_reopen。每个launch.json记录实际PID、命令参数、脚本SHA、退出码和文件前后哈希。补验里的dbid仅在该原生会话中标识对象，不能跨重开把数值当稳定ID。

最终DRA SHA：QFP A278A9843FE662A1FB50435EE341205CFF5D5E434CE84DA240875A3EE9EA713D；single 8D57D7D4E3BD9D75240C8F68A4A22F86FE63828740E251653DAC6FBDC8869FB9；split 4C570314ADD9FE53C1B5FD5851FCD0ED28DCBD99A0B90472925396E422E12292。板SHA 3C202304A710E97DD883B007F041E96968D5D857F4D88BB6BDED9E538F189B2D。完整文件清单以本课manifest.json为准。

## 10. 本次实际问题、修正与防复发

- 首次single中心paste采用方角；复查图42的R0.05后，先将初次PXML/PAD/log归档evidence/single_paste_initial_square，再修正圆角重导入。后续必须检查ALL PAD CORNERS是否同样约束paste与EP。
- 初次共享IL由PowerShell UTF8写出BOM，Cadence把BOM当函数名前缀，报undefined function。进程虽exit0但脚本并未成功；保留evidence/lesson09_initial_BOM.il和首次日志，改ASCII IL。验收必须同时检查COMPLETE、实际文件/数据，不能只看exit0。
- reopen02曾查询DRA不存在的ETCH/L2/L3，出现No match for subclass warning。改用axlIsLayer判断，最终reopen03无此警告；原始输出保留，不通过屏蔽消息消警告。
- 未导入逻辑的package pin不能直接AssignNet；board_create02失败且未保存。保留原始IL与日志，最终board_create03明确仅做几何放置/热孔，不虚构EP接地完成。
- 原生axlDBGetPad的bbox是以pin为中心的局部坐标，但**已含pin旋转**。独立校验器最初把90°宽高当未旋转而失败；已按实际rotation交换宽高，并对placed polygon独立确认，避免重复旋转。
- extract按层可能重复同一对象。原始25行热孔先按坐标核对后，又追加原生唯一dbid证明实际只有5个；不能只用几何去重掩盖重叠重复via。
- Python读取/生成跨PowerShell资料统一utf-8-sig读取、显式UTF8输出；SKILL/SCR采用ASCII或无BOM。文本补丁避免把字面\\n当真实换行。PDF文本输出到文件而非依赖系统GBK控制台。
- SPMHUT-48 Scaled value has been rounded off在创建/单位转换时仍出现，日志完整保留。精确字段来源未确定，本课以保存后逐尺寸/半径/面积读回证实关键几何符合0.001mm精度；不把它写成“全程无警告”。

未在Temp或其他目录自行创建中转文件；本课整个过程遵循record_location_rules.md。重放create须用新隔离目标/新日志并确认drawing不存在，不能对当前已验收样本盲目重跑；先备份修改前数据再做新版本。

## 11. 与PI/SI/EMI及实际装配的联系

封装正确只提供可靠基础。TI图28明确要求AGND/PGND/EP与公共地直接连接，输入/输出电容靠近IC，高di/dt回路短宽、回路面积小，SW高dv/dt区域与FB/VOS等敏感信号隔离；VOS从输出电容实际输出点取样，反馈/AVIN/SS等按推荐近放。不能认为DRC连通、自动布线或散热铜面积足够就完成这些要求。

在MCU QFP上，电源/地pin位置影响去耦电容摆放与回流；应按pin逐组近放电容并保持连续参考面，避免跨平面裂缝和不必要绕行。QFN EP的地连接和热孔既承担散热，也影响电流回流阻抗；把EP仅当机械焊盘或留浮空会破坏要求。层名TOP/L2/L3/BOTTOM是物理顺序，并不自行决定哪个内层为完整地平面。

本课已完成PCB封装CAD训练，不含实物焊接/X-ray空洞评估、填孔工厂验证、实际热计算/测试，也不含完整供电网络和板级SI/PI/EMI签核。单窗作为厂家参考，分窗作为明确标注的工程备选；工程发布时要按具体厂家版本和装配条件再决定，不能把教学备选默认替换生产库。
