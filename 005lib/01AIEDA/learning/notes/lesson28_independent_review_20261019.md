# 第28课独立复核：实际层叠、制造口径与机械传播

## 2026-10-19用户反馈后的纠正（当前优先）

[层叠与完整Artwork纠错](lessonF_stack_artwork_correction_20261019.md)已更正物理MASK和不完整Artwork。当前布局入口是[F29_CONSTRAINTS_v4.brd](../examples/lessonF_stack_artwork_correction_20261019/current/F29_CONSTRAINTS_v4.brd)，两层/四层建板副本与补验见该纠错记录。本文原402/99/543/937项数字分别是当时的测试范围，未覆盖“不得加入物理MASK、按drill*.txt完整建立全部15/17个Film”，不能代表满足用户全部规范。

下文原BRD、SHA、TCF、预览及日志保留为当时版本证据；涉及增加物理MASK、仅导入铜Film、F28_DESIGN_OUTLINE的做法已经撤销，旧脚本不得直接重放为当前流程。更正前笔记已备份，旧manifest是历史快照；当前身份以纠错清单为准。

日期：2026-10-19（Asia/Shanghai）。审查员独立读取第28课文件，没有运行Cadence、没有修改第28课BRD/脚本/记录；本审查材料只写在01AIEDA的 lesson28_stackup_20261019_review 及本笔记。

当前审查入口：[review.json](../examples/lesson28_stackup_20261019_review/review.json)、[独立审查源码](../examples/lesson28_stackup_20261019_review/review28.py)、[阻焊桥独立复算](../examples/lesson28_stackup_20261019_review/mask_web_review.json)。

## 1. 审查对象和方法

两层F28_2L.brd当前SHA256为C8624574A5EE8F7001169BFA83EDFFACE5920B2A6BF881F6DD99416687F821CF；四层F28_4L.brd为F004184D46B86A7CF56FFA05C33418A6BEEFA508A3043A3442540B69AFA558D6。路径均在 learning/examples/lesson28_stackup_20261019/native。核对current BRD SHA、原生reopen2_02/reopen4_02退出码与前后SHA、更多物理pin读回more2_01/more4_01；不凭该课384项自验结论直接接受。

独立重新解析SKILL S-expression及TSV，从第27课逻辑与物理读回重新比对272个pin→net、80个逻辑组件身份、69网名、四安装孔和J2，独立求和实际层叠厚度、按固定顺序核层名和铜、核film完整groupMembers与各flags。程序最初不能处理nets.tsv空pinIdentities字段，失败稿保留后修复；这个审查器失败不属于CAD错误。

同时在线复查当前官方页面：[OSH两层服务](https://docs.oshpark.com/services/two-layer/)、[JLC层叠](https://jlcpcb.com/impedance)、[JLC能力](https://jlcpcb.com/capabilities/pcb-capabilities)、[GCT USB4105](https://gct.co/connector/usb4105)。本地第28课保留了相应网页/PDF来源；审查JSON记录所核文件SHA与在线复核日期。没有将第三方转载或另一个服务的能力混用到本服务。

## 2. 层叠和厚度口径

| 示例 | 按原生Cross Section的实际顺序 | 铜+介质和 | 加模型阻焊后和 | 对外名义板厚 |
| --- | --- | --- | --- | --- |
| 两层OSH | mask0.0152 / TOP0.0356 / core1.524 / BOTTOM0.0356 / mask0.0152，mm | 1.5952mm | 1.6256mm | 1.6mm |
| 四层JLC04161H-7628 | mask0.01524 / TOP0.035 / PP0.2104 / L2 0.0152 / core1.065 / L3 0.0152 / PP0.2104 / BOTTOM0.035 / mask0.01524，mm | 1.5862mm | 1.61668mm | 1.6mm |

以上数值按当前原生TSV独立求和，与对应官方公开结构一致。三种厚度概念不能互相当成精确相等；没有为了凑1.600000而偷偷改变介质。模型未建立丝印局部油墨厚度、金属表面处理完整轮廓和局部阻焊起伏，因此其总和也不是任何位置都相同的机械实测高度。

OSH核心4.5是在官方页面10MHz条件下的标量输入；四层PP/Core的4.4/4.6来自JLC公布标量，但公布页面未给全部频率/构造实测条件。四层平面C2=0.6mil阻焊模型使用Dk3.8，只表示线顶有效覆盖近似，不等于C1/C2/C3全部轮廓。官方来源：[OSH](https://docs.oshpark.com/services/two-layer/)、[JLC](https://jlcpcb.com/impedance)。

所有原生Df0.035为软件默认、两层紫色阻焊Dk4.3为软件默认、铜上的继承Dk4.5没有所需介质意义；第28课spec已明确不予材料/RF资格，不将这些值误报成实测板材参数。JLC原生逐层tolPlus/Minus=0表示本教学输入没有逐层公差数据，不表示制造零公差；JLC公布名义1.6mm整板厚度另有±10%口径。[JLC制造能力](https://jlcpcb.com/capabilities/pcb-capabilities)

固定铜层名真正为TOP-BOTTOM及TOP-L2-L3-BOTTOM。L2/L3虽然计划连续GND，当前只有铜层定义及一个GND教学过孔，没有铺铜/连成参考平面；原生几何没有ETCH上的plane shape。不能从“层功能写了GND”推断电磁参考面已经存在，90Ω目标也不产生已确认的USB线宽/线距。

## 3. 逻辑、孔和机械约束传播

独立从当前TOP pin-row重新得到272个原逻辑pin→net，与第27课源读回逐个一致；80件逻辑身份、封装和pin数，以及69个网名一致。net→pins查询会忽略部分未放器件，不能只靠它计数；本次改从component->pins对应的pads.tsv核全量，所以79件未布局不造成漏验。

每板实际物理对象为J2的18个pin（含2定位NPTH）加4个MECHANICAL BSM安装孔，共22pin。more*的symbol->pins循环确实包含四个BSM，type=MECHANICAL、refdes=nil；没有把只统计component->pins得到的18pin误称全部机械pin。六个NPTH在两/四个导体上均为NULL且铜bbox零，USB SMT只在TOP有铜，4个壳脚槽的PTH铜按导体层扩展。四安装孔(5,5),(75,5),(75,55),(5,55)及J2(40,3.675)保持。

高度读回也正确保留两种不同语义：J2的filled PLACE_BOUND_TOP带有限MAX=3.46MM；TOP x10…30/y42…52区域仅MIN=2MM，表示从该高度起的禁止占据范围，没有一个已存MAX，不能杜撰成有限高度罩壳。安装孔BSM不伪造实体器件高度。其他59条已导出的机械记录与第28课输入基线完全一致。

教学过孔在(52,35)，GND，Ø0.3/.6，Through_via。旧extract-map可能将同一via重复列成3/5行，按完整对象身份去重后每板确实只有1个；没有据原始行数制造额外via计数，也没有借此宣称参考平面已存在。

## 4. 光绘映射与板框证据

原01env/drill2.txt和drill4.txt SHA不变。铜film的完整groupMembers、正片/镜像/抑制孤立焊盘等flags，当时仅核铜Film对应部分，漏掉模板另外13项；旧检查不代表完整Artwork一致。4层模板L2、L3的sequence数值并非物理铜层上下顺序；实际Cross Section才是层叠依据。

原模板铜film包含旧BOARD GEOMETRY/OUTLINE，而本机械板实际轮廓在DESIGN_OUTLINE。第28课没有修改原模板，在BRD另加独立F28_DESIGN_OUTLINE film指向真实轮廓层。这是额外输出映射，不能据此声称所有生产光绘已经完整生成或板厂批准。

独立复核发现一个证据盲点：官方旧fgeo_bv.txt提取的geometry.tsv不含DESIGN_OUTLINE，输入baseline01也不含。因此“59行几何相同”和“多了一个指向DESIGN_OUTLINE的film”本身不直接证明板框保存成功。已要求第28课补充只读root.designOutline/keepinPlace/keepinRoute及该层explicit shape bbox/vertices证据；它是取证遗漏，不等于已经证实板框丢失。最终处理结果见下方复核结果节。

## 5. 发现的实际制造/装配待办

1. 两层示例所选OSH公开最小阻焊桥0.1016mm；继承GCT库的细pin阻焊宽0.4、pitch0.5，名义桥0.100mm，相差0.0016mm。独立复算来自第10课原生mask读回，且DE库pad和原pad字节SHA完全相同。需要调整阻焊/服务商明确接受/另选工艺后方可释放；不是据层叠输入正确就宣布整板符合OSH。此审查没有重新渲染当前两层板全部mask，来源链和这一范围在mask_web_review.json中明确记录。[OSH最小阻焊桥](https://docs.oshpark.com/services/two-layer/)
2. GCT图的S=0.95±0.15mm是从器件安装/SMT基准面到壳脚尖的stake length，不是成品PCB底面以下剩余突出量。第10课和第27课曾沿用“板下侵入”错误措辞，本审查识别后已修正第27课正文并记录勘误；root负责其余汇总的同步。名义1.6mm示例板与默认0.95mm壳脚尚未证明通孔焊接充分或匹配选定装配工艺。应结合实际板厚、座高和公差重新求关系；不能直接说板底还有0.95mm。[GCT原厂](https://gct.co/connector/usb4105)
3. 两层与四层是不同板厂公开模型，能力不能交叉借用。材料标量Dk、软件默认Df、mask轮廓近似及逐层公差缺省已经限定范围；它们不属于“已认证但出错”的数据，也不能据此进行阻抗/制造承诺。
4. 01env未改，独立轮廓film已建立，但尚未执行全部铜/阻焊/钻孔/外形生产输出和CAM回读；未布局布线的板也不具备SI/PI/EMI验收结论。

以上不影响按来源学习层叠编辑、核对物理顺序与传播的课程范围；会阻止把当前教学板直接称为可投产设计。

## 6. 最终复核结果与证据闭环

第28课已补充三次独立readonly导出，分别为logs/mechbase01、mech2_01、mech4_01。审查员独立解析mechanical_direct.tsv，原板／两层／四层全部显式机械形状逐条一致；DESIGN_OUTLINE的bbox=(0,0)—(80,60)，8个正确C2顶点，designOutline、keepinPlace、keepinRoute三root均为真。每次实际进程exit0且BRD前后SHA不变，先前fgeo提取遗漏已经关闭，不再是未解问题。

最终独立审查 **99项全部通过**，状态PASS_NATIVE_SCOPE_WITH_FABRICATION_OPEN_ITEMS。已再次读取第28课402项最终自验、17.8KB完整笔记及新增制造释放限制，原生层叠、孔/槽/几何、逻辑网络、模板映射、来源身份与所声明范围吻合。审查数字与第28课402项有重叠，不相加成总质量分。

通过范围为实际两层/四层建模、官方公开参数口径、原生保存重开及既有逻辑/机械传播。明确保留本笔记第5节的制造与装配待办，尤其OSH阻焊桥差异和GCT壳脚S的正确基准；当前教学板不具备直接制造放行结论。审查全程没有启动Cadence，也没有修改第28课文件。第27课S文字勘误前快照、修改脚本与本次review身份清单均在独立review目录，原第27课BRD和SHA未变。
