# F阶段层叠与Artwork纠正：独立只读复核

2026-10-19。结论：**PASS_INDEPENDENT_USER_CORRECTION_REVIEW，1717项，0失败**。机器报告为[review.json](review.json)，完整输入SHA为[evidence_manifest.json](evidence_manifest.json)，可重运行代码为[independent_review.py](independent_review.py)。本审查未启动Cadence，未编辑源板、公共库、01env或他人的纠正脚本，仅核对原生保存后新进程只读导出。主执行方的validation.json是独立交叉证据，未拿它的预解析模板当期望值。

## 本轮纠正了原验收遗漏

原先只验了铜层Film和自建F28_DESIGN_OUTLINE，没有逐个验收用户drill2/drill4的15/17个完整Film；还把额外物理MASK行当成可接受的层叠表达，没有落实用户所需Cross Section形式。此前审查跟随了缩窄后的检查范围，漏掉这些要求，不能继续用旧PASS声明本轮要求已满足。旧报告留作历史，本报告对这些要求的结论取代旧结论。

本次重新从原始01env文本独立解析完整axlFilmCreate调用，逐个比较全部原始Options与重开后的真实Film参数、合法层成员，检查的不是脚本返回t或复制出的JSON。首轮比较器曾误报class_table中的propList进程地址不同；已保留review_preliminary.json和independent_review_initial.py。纠正仅归一化dbid/propList地址，其余规则名称、数值、域、成员和属性照常比较。

## 三块最终板的实际状态

| 板 | 实际铜层顺序 | Film数 | 原生MASK物理行 | 重开原生DRC |
| --- | --- | --- | --- | --- |
| ../current/F28_2L_USERFIX.brd | TOP-BOTTOM | 15 | 0 | 0/t |
| ../current/F28_4L_USERFIX.brd | TOP-L2-L3-BOTTOM | 17 | 0 | 0/t |
| ../current/F29_CONSTRAINTS_v4.brd | TOP-L2-L3-BOTTOM | 17 | 0 | 0/t |

三板均保留其他导体、介质、材料、厚度、Dk、loss及制造备注原值；物理MASK删除后CAD铜与介质合计为2层1.5952mm、4层1.5862mm，不把这个合计冒称制造成品的精确总厚。成品的阻焊涂层仍由已有非导电SOLDERMASK类和开窗定义表达，不因Cross Section不含MASK行而消失。01env源文件、原三板和备份SHA均未变化。

三种独立原生读法一致：旧axlGetXSection()、新axlXSectionGet的raw name、ETCH group/axlSubclassRoute均返回大写TOP/L2/L3/BOTTOM。没有证据表明API自动把真实层名标题化为Top/Bottom；截图显示样式不能代替数据库读回。

保持毫米单位，把存储精度从3位提高至4位，使模板undefineLineWidth=0.0025可以精确保存。现有几何和铜/介质值逐字段不变；并非重新输入近似尺寸。

## Artwork完整性与原模板本身的问题

15个共同Film为TOP、BOTTOM、PASTTOP、PASTBOTTOM、SKILTOP、SKILBOTTOM、SOLDTOP、SOLDBOTTOM、DRILL、OUTlie、PDFTOP、PDFBOTTOM、DisTOP、DisBOTTOM、DisAll；4层另含L2、L3，次序按原模板保存。OUTlie与Dis*的原大小写保留。已逐项核对negative、undefined line width、sequence、rotation、offset、shape bounding box、mirror、full contact、所有suppress/draw/vector选项、domains及ipc2581空值；不是把所有fullContact/mirror统一设成nil。sequence保留原值，不把它误当物理层序。

原模板的重复layer引用会被原生去重。本审查按合法成员集合比较，并分别记录原始重复数、过滤项与实际层列表，见review.json的filmReview。以下原有问题必须明示：

- BOARD GEMETRY/SILKSCREEN_TOP、BOTTOM中的GEMETRY是源文件拼写；不是实际类。它们在SKIL/PDF Film中被原生过滤，没有伪造同名错误类，也没有改原01env。
- 2层DisAll仍请求CONSTRAINT REGION/L2、L3；两层板不存在这两项，原生过滤。没有为满足显示Film而增加铜层。
- 原SKIL Film只包括PACKAGE GEOMETRY丝印及上述无效类，不含REF DES/SILKSCREEN，也不含COMPONENT VALUE。完整恢复原模板不等于已经证明制造丝印包含所有位号/数值文字。
- 原模板只调用FilmCreate；Film Control保存在BRD中，General Parameters的art_param.txt、光圈表art_aper.txt及真实CAM文件生成/内容核对是另一项工作。本结论不宣称全套光绘或制造资料已发布。

原生旧F28_DESIGN_OUTLINE Film没有作为缺失Film的替代物保留。模板要求的BOARD GEOMETRY/OUTLINE已存在一份真实几何，与权威root.designOutline指向的BOARD GEOMETRY/DESIGN_OUTLINE八个C2顶点、80×60 bbox逐一相同。三板outline_*均是新的只读进程，exit0且文件SHA未变；真板框root没有被替换。原有keepin/keepout及限高图形也全部保持。

## 删除MASK行没有删掉开窗和电气数据

逐行对比基线与保存后只读结果：22个实际放置pin（含USB内部定位孔及四个机械孔）和1个唯一过孔，在所有铜层、PIN/SOLDERMASK_TOP/BOTTOM及PASTEMASK_TOP/BOTTOM的实际figure、bbox、padstack/usage、坐标均相同。通孔过孔原本NULL的阻焊开窗仍为NULL，未擅自取消盖油；该状态不能泛称每个过孔都开窗。PIN、VIA CLASS、PACKAGE GEOMETRY和BOARD GEOMETRY下的SOLDERMASK_TOP/BOTTOM均仍为真实有效非导电类。

三板80个逻辑器件、69网、272逻辑pin及其中6个NC、5个放置symbol不变。F29的27域网络分类、3差分对、网络真实成员、全部物理/间距/电气CSet、class-class表、GND/VDDA局部例外、逐网继承、DRC模式、许可via、禁止内层一般信号规则均与v3基线一致；未留下临时教学走线或挑战属性。新版TCF官方导出和compare均exit0，No objects were updated，板SHA不变；TCF不能取代逐网/对象映射的原生读回。

## 后续必须继续区分的边界

本轮完成的是用户要求的层叠形式和原模板FilmControl恢复。79个逻辑件仍未布局，尚未完成整板走线、回流路径/去耦/EMI及实际CAM检查。原制造目标与Dk适用频率、USB阻抗几何、2层USB阻焊桥与板厂下限、1.6mm板厚与USB4105插脚/装配工艺匹配仍沿用之前记录的待确认事项，不因DRC0变成制造批准。

官方本机依据：Cadence17.2的axlFilmCreate、axlXSectionDelete、axlDBChangeDesignUnits、axlLayerCreateNonConductor、axlGetXSection接口说明，身份SHA已列入evidence_manifest。物理层删除使用axlXSectionDelete；创建非导电类使用axlLayerCreateNonConductor。Artwork Film列表的Add与Film内Layer的Add作用不同，后者只是把现有class/subclass加入Film，不会增加物理铜层。
