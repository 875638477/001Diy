# 第28课：两层／四层实际层叠与制造参数

日期：2026-10-19，Asia/Shanghai。Cadence Allegro／Padstack Editor 17.2 S045，Windows SPB64。

**本课原生 CAD 实操完成：两套实际层叠、材料与厚度写入、受控错误检出与恢复、过孔／槽脚／纯 NPTH 层映射、Film 对照及保存重开，共402项独立检查通过。** 这里的完成范围是建板和制造定义学习。两层继承 USB 封装存在阻焊桥与教学板厂下限的具体差异，四层 USB 90Ω 线宽／间隙仍须按实际工艺确认，均未称生产释放通过。

## 一、产物与证据入口

练习目录：[lesson28_stackup_20261019](../examples/lesson28_stackup_20261019)。全部源码、下载、渲染、原生文件、日志、失败修正和备份均留在01AIEDA，未修改公共库、01env、快捷方式、全局HOME或用户实际工程。

- [完整规格与来源SHA](../examples/lesson28_stackup_20261019/specification.json)
- [独立验收402项](../examples/lesson28_stackup_20261019/validation.json)／[验收源码](../examples/lesson28_stackup_20261019/scripts/validate28.py)
- [两层原生板](../examples/lesson28_stackup_20261019/native/F28_2L.brd)／[四层原生板](../examples/lesson28_stackup_20261019/native/F28_4L.brd)
- [原生操作SKILL](../examples/lesson28_stackup_20261019/scripts/lesson28.il)／[分步工作流](../examples/lesson28_stackup_20261019/scripts/workflow.py)
- [两层独立重开](../examples/lesson28_stackup_20261019/logs/reopen2_02/readback.txt)／[四层独立重开](../examples/lesson28_stackup_20261019/logs/reopen4_02/readback.txt)
- [全部22个已放物理pin](../examples/lesson28_stackup_20261019/logs/more4_01/placed_pins.tsv)／[实际各层pad](../examples/lesson28_stackup_20261019/logs/more4_01/placed_pads.tsv)
- [层叠预览PNG](../examples/lesson28_stackup_20261019/preview.png)／[SVG](../examples/lesson28_stackup_20261019/preview.svg)：按原生读回绘制，薄层设最低显示高度，非界面截图、非按厚度全比例制造截面。
- [全部文件SHA清单](../examples/lesson28_stackup_20261019/artifact_manifest.json)

输入为第27课 F27_MECHANICAL.brd，SHA256=B6C84686472475F452F13F30EB7E3F99D8B9441CF0AB44B3D33917D615E5B55A。其基础是当前 DE_BASELINE，而非历史 ECO 实验。保留80个逻辑器件、69个网络、5个已放符号（J2及4个机械安装孔）、272逻辑pin。除J2外79个逻辑器件仍未布局。

## 二、两个制造目标分别成立，不混用板厂参数

本次用两家公开且可追溯的完整结构作教学目标，不是报价或板厂选择建议，也未取得本板订单的工艺批准。JLC公开两层能力页没有独立core厚度，不能把1.6减去铜和阻焊后自行推算值当厂商定义，因此两层改用有明确core的OSH Park服务结构。

| 项目 | 两层教学目标 | 四层教学目标 |
| --- | --- | --- |
| 原厂来源 | [OSH Park 2 Layer Prototype](https://docs.oshpark.com/services/two-layer/) | [JLCPCB JLC04161H-7628](https://jlcpcb.com/impedance) |
| 铜层顺序 | TOP-BOTTOM | TOP-L2-L3-BOTTOM |
| 外层铜厚 | 每层0.0356 mm | 每层0.035 mm |
| 内层铜厚 | 无 | L2、L3各0.0152 mm |
| 绝缘结构 | core 1.524 mm | PP7628 0.2104／core 1.065／PP7628 0.2104 mm |
| 标称板厚 | 1.6 mm，独立口径 | 1.6 mm，独立口径 |
| 铜＋绝缘求和 | 1.5952 mm | 1.5862 mm |
| 本次mask模型 | 每面0.0152 mm | 每面C2有效0.01524 mm |
| 含本次mask模型求和 | 1.6256 mm | 1.61668 mm |
| 绝缘Dk来源值 | core 4.5，10 MHz | PP7628 4.4、core 4.6，网页未给频率 |
| mask Dk | 紫色mask未获资格数据 | 原网页3.8，频率未给 |

四层core描述的1.1 mm H/HOZ **含两面内铜**；本次只把1.065写到core绝缘层，两个0.0152分别写L2、L3，不能把1.1再加两次内铜。JLC用“0.5oz”描述内层，但公开截面直接列0.0152；不擅自改成通用换算0.0175。

外铜是选定服务的成品口径，不把孔壁镀铜厚度再次加到外铜上。基铜、外表面电镀、孔壁铜和表面处理是不同项目；ENIG/HASL不是增加一层信号铜。JLC能力页的孔壁18μm是平均值，不是本板实测值或最小验收保证。

标称1.6、铜绝缘求和、含mask模型求和是三种数据。阻焊在裸基材、铜顶、线间具有不同截面；JLC C1/C2/C3为1.2/0.6/1.2 mil，本次Cross Section只存均匀C2有效覆盖层，不代表全部区域真实厚度。丝印和局部表面处理不计入本次均匀模型。不能为了凑1.600而篡改已公布的core/PP厚度。

OSH core公差按源表±0.1524 mm写入；mask为±0.00508。JLC原生各层tolPlus/tolMinus=0表示**未输入逐层公差**，不是零制造公差；其公开成品1.6 mm板厚公差±10%仍需用于机械装配评审。

## 三、介质材料与软件默认值必须分清

[KB6167F原厂数据手册](https://docs.oshpark.com/resources/two-layer-substrate-Kingboard-KB6167F.pdf) 已保存并渲染。第1页同一测试条件下列Dk随频率变化，第2页按玻纤结构及树脂比例分别列数值。OSH服务页的4.5@10MHz与材料手册另一试样/频率的典型值不能互相替换；更不能称所有FR4固定4.2，或把低频Dk直接当USB频段精确值。

本机实测：用一个新的material名称，17.2仍会继承电参默认值。最终2L紫mask的原生Dk=4.3、Df=0.035；这些是软件默认，**不是原厂已确认材料值**。JLC/OSH绝缘及mask中的Df=0.035也未取得对应工艺资格，不作为SI损耗模型。铜层显示Dk=4.5是工具残留字段，对本课导体定义无实际介质意义。规格JSON及预览明确标注这些差异。

OSH服务页链接的Taiyo PSR-4000BN资料为绿色系列，不能因此断言紫色阻焊有相同电参。本课保留链接PDF作为出处审查记录，没有套用绿色数据填紫mask。

这轮没有进行SI/PI仿真。层叠的作用是让后续线宽、间距、参考平面、换层与回流条件有真实物理依据。USB90Ω是接口目标，不能仅因选择4层或填写一个任意宽／隙便宣告达到。官方JLC计算器静态页已存档；当前无浏览器连接，未取得动态计算结果，因此本课不输出伪造的“90Ω推荐线宽”。

## 四、层功能、回流与实际物理层名

两层铜名称只用TOP、BOTTOM；四层只用TOP、L2、L3、BOTTOM。core、PP、mask不是额外铜层，DEFAULT_INTERNAL也不是实际层名。不能把层名改成GND、POWER、IN1。

针对本套低功耗、多路供电MCU教学板，四层功能规划如下。**这是布局布线意图，当前L2/L3尚未生成GND铜面。**

| 物理层 | 规划功能与后续约束 |
| --- | --- |
| TOP | 元件、信号及局部电源，关键信号参考L2 |
| L2 | 连续GND，避免信号下方被槽、避铜或电源分割切断 |
| L3 | 连续GND，为BOTTOM提供直接参考 |
| BOTTOM | 信号及局部电源，参考L3，保持实际回流覆盖 |

选择S/G/G/S是针对本板的工程决定；不把S/G/P/S泛称所有板的最佳结构。若L3改分割电源，必须重新核查BOTTOM参考及参考转换。TOP↔BOTTOM的信号换层仍需附近合适的GND回流过孔，把L2/L3参考连接起来；只有信号via连通并不能证明回路完整。

两层绝缘1.524 mm意味着对侧地参考距离远，BOTTOM应尽量保留连续GND，布线不能随意把地割成细颈／孤岛。四层较近的0.2104 mm参考距离改善条件，但不能代替去耦布局、小热回路、正确地过孔及敏感模拟隔离。中央1.065 mm两层GND间隔也不能冒充紧耦合电源／地平面对去耦电容的替代。

原理依据见TI [High-Speed Layout Guidelines, SCAA082A](https://www.ti.com/lit/pdf/SCAA082A)，PDF第9—10页：参考平面缺口导致回流绕行和更大环路；功能块应集中；层数和回路要在布局前规划。本课采用这些基本设计要求，不直接复制其所有示例层叠评价。原文及相关页渲染在source中。

## 五、原生操作顺序与复现方法

本次实际通过官方CLI／SKILL操作，不是GUI截图记录。图形界面逐项点选仍需桌面连接恢复后单独验证。

1. 只读重开第27课输入，记录源SHA、80件／69网、所有原机械几何、原始物理层序及完整逻辑pin-net关系。
2. 复制为独立F28_2L.brd／F28_4L.brd；启动器子进程TMP、TEMP、ALLEGRO_PCBENV和cwd均指向本课目录。全局HOME不改。
3. 用axlXSectionGet(nil 'all)读取真实物理顺序；检查初始只有TOP/BOTTOM和一个绝缘层，拒绝在未知层叠上盲目追加。
4. 用axlXSectionModify与axlXSectionSet写材料、厚度、Dk及来源标签。四层由上至下保留PP，再在BOTTOM上方依次插入L2、core、L3、PP。不为绝缘层赋ETCH名字。
5. 写入独立mask层及真实厚度口径；原生读取材料、层类型、正负片、位置、导体标志和电参。材料名并不保证默认电参有来源。
6. 用官方PXML导入l28_via030_c060.pad，正常exitCode=0，无Padstack Warning/Error。建立一个GND教学via@(52,35)，用于测试跨层映射。
7. 受控把TOP铜厚临时加0.010 mm，直接原生读回实际错误并检测，再恢复原值。两层0.0356→0.0456→0.0356；四层0.035→0.045→0.035。错误值未作为最终交付保存。
8. 完整复制对应01env模板的铜Film参数到练习板；另建实际DESIGN_OUTLINE的独立Film，不修改模板。
9. axlDRCUpdate(t)实际刷新，最终两层／四层均0错误、drcState=t；保存退出。
10. 两个新进程分别readonly重开，再补三个独立只读进程导出原板／2L／4L的全部已放物理pin，核孔、槽、铜层、库及层映射；每次真实exitCode=0、只读SHA不变。

[官方API摘录副本](../examples/lesson28_stackup_20261019/source/cadence17_2)包含XSection Get/Set/Create/Modify、CreateVia、CreatePadStack、FilmCreate以及Cadence自带xsection.il示例，便于换机追溯。Python工作流保留分步命令与实际启动参数，不能仅看exitCode=0：SKILL errset会吞掉异常，还必须检查COMPLETE、原生文件、重开读回与独立几何验收。

## 六、孔结构、各层Pad与制造能力边界

教学via为普通机械通孔，finished drillDiameter=0.300 mm、各层REGULAR铜Ø0.600 mm、名义径向铜环0.150 mm；不是盲孔、埋孔、激光微孔或填孔。原生Through_via、PLATED、isThrough=t、startEnd=(TOP BOTTOM)，四层的L2/L3由DEFAULT_INTERNAL正确补出铜。0.300是成品孔定义，未伪造实际钻刀直径；钻刀补偿应由板厂工艺确定。

按名义1.6/0.3计算纵横比约5.33只是初筛，不能代替实际厚度、实际钻刀、孔壁铜和加工能力确认。PXML没有mask aperture代表数据上覆盖via，不保证树脂填充、平坦或无漏光，不能据此做via-in-pad装配承诺。

| 检查 | 原生读回结果 |
| --- | --- |
| 源逻辑数据 | 80件／69网／272pin保持，544个原外层pin-net-pad查询记录完全一致 |
| 已放物理对象 | J2的18pin＋4机械安装孔，共22pin保持；44个原外层pad记录相同 |
| 纯NPTH | J2两个Ø0.65＋安装孔四个Ø2，所有2/4铜层均NULL且零bbox，不添铜环 |
| USB槽脚 | 4个镀铜槽保留孔型、尺寸、位置；L2/L3实际OBLONG_X REGULAR铜按内部模板出现 |
| SMD | 仅TOP有实际铜；BOTTOM与内层维持NULL，不因增加内层复制贴片铜 |
| 新via | 每板实际唯一1个GND对象，每层Ø0.6 REGULAR，孔壁镀铜与穿层跨度正确 |
| 机械数据 | 59条原机械形状／文字／属性记录逐条不变；另以显式层查询核对真正DESIGN_OUTLINE、Keepin、Keepout及原生root引用 |
| 最终DRC | 两层、四层均已实际刷新为0/t，仍不代表整板布局布线或制造释放通过 |

原生axlExtractMap对同一个via会返回多个层关联别名，两层3条、四层5条原始记录；独立验收按坐标／名称／跨度／网络去重，得到各1个真实via。不能把重复行当成多打了几个孔。

制造能力分开查各自官方服务，不把JLC的下限套在OSH上。OSH两层公开线宽／间距0.1524、孔0.254、铜环0.127、边距0.381 mm；当前教学via0.3/0.6有名义裕量。JLC四层1oz公开线宽／间距0.09、推荐via孔≥0.2 mm等，当前via几何同样不是挑战极限工艺；后续普通0.20 mm线宽／间距属于工程取值，不能直接当阻抗线宽。以上只筛查所列项目，未把未放置的79件或整板生产细节视为通过。

板框已补充直接证据：[原板](../examples/lesson28_stackup_20261019/logs/mechbase01/mechanical_direct.tsv)、[两层](../examples/lesson28_stackup_20261019/logs/mech2_01/mechanical_direct.tsv)、[四层](../examples/lesson28_stackup_20261019/logs/mech4_01/mechanical_direct.tsv)逐条一致，designOutline／keepinPlace／keepinRoute三root均非空，真正板框bbox为(0,0)—(80,60)、8顶点含四角C2。fgeo_bv视图没有导出该DESIGN_OUTLINE，不能拿59行一致替代这项证明。

**具体制造差异：** 继承USB封装的名义阻焊桥0.100 mm，小于OSH两层公开最小0.1016 mm，差1.6μm。本次没有修改共享封装或把比较结果藏掉；两层整板若采用该制造目标，释放前需修订mask开窗、取得工艺接受或另选适合的工艺。四层JLC 1oz有色mask公开桥下限0.10 mm只是等号条件，颜色、加工补偿和邻近线遮盖仍需确认，不能自动认为所有公差都安全。

另一个必须解决的装配条件：沿用的GCT USB4105-GF-A默认固定脚S=0.95±0.15 mm，是自器件安装／SMT基准面量到脚尖的Shell Stake Length，不是从PCB底面量出的板下突出量。[原厂产品页](https://gct.co/connector/usb4105)列0.60／0.95／1.20 mm脚长选项；[已归档Rev B4图纸](../examples/lesson28_stackup_20261019/source/GCT_USB4105_RevB4_inherited.pdf)保留默认S尺寸。名义1.6 mm板厚与该固定脚的插入、焊接充分程度尚未验证，不能宣称装配匹配或板下突出0.95 mm，须结合具体料号、板厚、公差及焊接工艺确认。

## 七、01env光绘映射与本次发现

[模板只读快照清单](../examples/lesson28_stackup_20261019/film_template_readonly.json)保存drill2.txt／drill4.txt原路径、SHA及Film层引用。最终再次校核原文件SHA完全一致；未执行或改写原模板。

TOP／L2／L3／BOTTOM铜Film实际引用各自ETCH、PIN、VIA CLASS同名层。drill4中sequence为1、25、20、27，属于PDF/Film输出顺序，不是物理层序；真实Cross Section依然TOP-L2-L3-BOTTOM。

首次只复制关键Film字段时，17.2实际省略项继承suppressUnconnectPads=t、drawMissingPadApertures=t，与函数文档所说布尔默认nil不同。已保留首轮读回作为差异证据，再逐项复制模板完整参数，最终重开确认这些参数以及mirrored、negative、fullContact、useApertureRotation等均为模板要求的nil，vectorBasedPad=t、shapeBoundingBox=2.54。

模板引用旧BOARD GEOMETRY/OUTLINE，而第27课真实识别轮廓在BOARD GEOMETRY/DESIGN_OUTLINE，旧层没有重复板框。本课新增独立F28_DESIGN_OUTLINE Film实际引用后者；保留原铜Film映射。日后生产CAM必须确认真正轮廓已进入实际制造产物，不能只看模板中出现OUTLINE字样便认为板框输出齐全。

模板undefinedLineWidth=0.0025，在本板mm/3精度读回0.002，保留为本机参数量化差异。本轮只验Film定义与映射，未生成并审核实际Gerber/钻孔生产包；不能把Film存在当成光绘内容已验收。drill12.txt既有多L12的差异仍按长期规范保留，未碰该模板。

## 八、问题记录、回退与交接

原生所有本课启动均正常结束，最终完整检查0/t。过程问题及修正：

- 未知材料仍继承Dk/Df默认：明确标出未资格数据，不伪装成原厂参数。
- Film布尔默认与文档不符：从省略字段改为完整复制原模板，独立重开验证。
- 第27课同组独立审查发现fgeo_bv没有真正DESIGN_OUTLINE：追加原／2L／4L三次readonly显式层查询、root引用、bbox及顶点比较，全部保持。
- 首次验收JSON保存遇到set不能序列化：保留validate28_serialization_failed.py，修正仅报告编码，再完成402项报告；不是CAD尺寸失败。
- 辅助工作流生成的换行转义和控制台GBK不能打印版权字符：修正课内脚本，PDF正文仍UTF-8；未在错误中转目录写文件。
- GCT产品页本地下载遇到访问挑战：不绕过验证，以已归档原厂PDF及本次web只读观察为来源，并明确原下载时间／本次复用。
- 初期下载MacroFab PDF渲染为空、没有可用正文：保留原下载和空白渲染作为未采用来源，不用于本次层叠数值。
- 最初层叠预览底部文字重叠：重排并重新渲染，最终PNG已逐项视觉检查。

回退方式是丢弃本课副本或复制source中已验证的F27输入；不把修改写回原板。所有受控错误厚度都在保存前恢复；源码／日志保留修正过程。

四层板已交给第29课约束学习，最终SHA256=F004184D46B86A7CF56FFA05C33418A6BEEFA508A3043A3442540B69AFA558D6；两层SHA256=C8624574A5EE8F7001169BFA83EDFFACE5920B2A6BF881F6DD99416687F821CF。第29课可删除教学via或改变后续布局，但应在自己的副本内操作，保持本课验收证据。

待实际设计释放时仍需完成：全部器件布局与连续GND实际铺铜、USB几何与实际板厂阻抗参数确认、各孔/铜/阻焊/边距与公差复核、真实制造包与CAM审查、装配限高及实板验证。这些不是本课未做软件层叠的替代说法，已有CAD产物与验证范围如上可独立复查。
