# F阶段纠错：PCB层叠与完整Artwork模板

日期：2026-10-19（Asia/Shanghai），用户以Cadence层表及Artwork截图指出错误。已在三块新板完成物理MASK移除、完整模板重放及保存重开补验；原生验收与独立审查均通过。本轮纠正第28课及其派生第29课，原402/99/543/937项检查未覆盖用户全部规范。

## 用户要求与本次失误

固定导电层顺序必须为两层TOP-BOTTOM、四层TOP-L2-L3-BOTTOM、六层TOP-L2-L3-L4-L5-BOTTOM，依此延伸。层功能另记，不以GND/POWER替代层名。Cross Section不额外加入物理Soldermask_Top/Bottom；阻焊制造资料及pad开窗仍保留。Through All是默认通孔跨度，不能当成一层铜或误删。

Artwork的内容由01env对应层数的drill*.txt完整定义；不是只取其中铜Film，也不能自行添加替代Film。这里的Film数量不是物理铜层数。

此前犯了三处错误：

1. 自行加入上下物理MASK层，让层表出现用户不要求的两行。
2. 脚本只提取铜Film，漏掉模板其余13项。
3. 为真实DESIGN_OUTLINE另建F28_DESIGN_OUTLINE，未按用户既有OUTlie/OUTLINE映射衔接。

原验收只核铜Film及自设MASK模型，独立审查也沿用了这个范围，漏了用户标准。因此撤回此前“01env Film精确对照”“已满足完整规范”的笼统结论，保留原数据作为有明确局限的历史证据。检查数量不能替代对用户要求逐条验收。

## 当前纠正版与文件身份

全部新增副本、脚本、运行环境、日志、中转、备份和笔记仍在01AIEDA。原F28/F29文件和01env模板均未改；新板是本轮修正后的当前入口，旧文件可用于追溯，不能继续当当前规范版本。

| 用途 | 当前入口 |
| --- | --- |
| 两层对比板 | [F28_2L_USERFIX.brd](../examples/lessonF_stack_artwork_correction_20261019/current/F28_2L_USERFIX.brd) |
| 四层建板基线 | [F28_4L_USERFIX.brd](../examples/lessonF_stack_artwork_correction_20261019/current/F28_4L_USERFIX.brd) |
| 后续四层布局起点 | [F29_CONSTRAINTS_v4.brd](../examples/lessonF_stack_artwork_correction_20261019/current/F29_CONSTRAINTS_v4.brd) |

原始板和模板身份见[input_manifest.json](../examples/lessonF_stack_artwork_correction_20261019/input_manifest.json)，源文件均有同SHA备份。补验见[原生验证](../examples/lessonF_stack_artwork_correction_20261019/validation.json)、[独立审查](../examples/lessonF_stack_artwork_correction_20261019/review/review.json)，文件身份见[产物清单](../examples/lessonF_stack_artwork_correction_20261019/artifact_manifest.json)。当前笔记/索引修订及历史备份对应见[本轮总清单](../logs/f_stack_artwork_correction_20261019.json)。

## 实际修改与核验

三块新板均由官方17.2 CLI/SKILL修改，保存退出后另进程只读重开，不以setter返回t代替结果：

| 新板 | 原生导电层序 | 物理MASK数 | 模板Film数 | 当前DRC |
| --- | --- | --- | --- | --- |
| F28_2L_USERFIX | TOP-BOTTOM | 0 | 15 | 0 / t |
| F28_4L_USERFIX | TOP-L2-L3-BOTTOM | 0 | 17 | 0 / t |
| F29_CONSTRAINTS_v4 | TOP-L2-L3-BOTTOM | 0 | 17 | 0 / t |

旧/新XSection API原始值、ETCH groupMembers及axlSubclassRoute交叉读取，真实名称是大写TOP/BOTTOM；用户截图中的Top/Bottom显示样式不作为改名依据。原错误F28_DESIGN_OUTLINE已移除。新增与真实板框相同的BOARD GEOMETRY/OUTLINE，供既有模板输出，实际DESIGN_OUTLINE根对象保持。

F29当前技术约束文件另导出为[F29_RULES_v4.tcf](../examples/lessonF_stack_artwork_correction_20261019/exports/F29_RULES_v4.tcf)，官方比较及日志在exports内；旧TCF含已撤销MASK，只保留为历史文件。

移除的是Cross Section物理MASK对象，不是PIN/PACKAGE GEOMETRY/BOARD GEOMETRY的SOLDERMASK_TOP/BOTTOM子类，也不是阻焊开窗。原始元件、孔、槽、pad、网络、位置、限高、keepin/out以及第29课约束须经修改前后比较，不能仅凭Film名称正确便接受。

板厂工艺中的阻焊厚度、材料、电参及总厚口径继续作为制造资料记录，不再为展示这些数据而向用户板的层表增加MASK行。软件铜+介质厚度与板厂名义成品厚度分开记录：两层1.5952mm、四层1.5862mm；不强改成精确1.600mm。

## 完整Artwork验收方法

两层15项，四层17项；四层铜Film为TOP/L2/L3/BOTTOM，两层为TOP/BOTTOM。共同13项为：
PASTTOP、PASTBOTTOM、SKILTOP、SKILBOTTOM、SOLDTOP、SOLDBOTTOM、DRILL、OUTlie、PDFTOP、PDFBOTTOM、DisTOP、DisBOTTOM、DisAll。

1. 读取匹配模板原文和SHA；清除错误/多余Film，完整执行模板，不筛铜、不猜Film名称。
2. 核全部Film集合及每张Film的层成员、sequence、plot mode、mirror、rotation、offset、full contact、vector pad和其他抑制/孔选项。
3. 先读取真实Cross Section导体顺序，再检查模板引用；不得为两层模板的历史L2/L3引用而实际增加内铜。
4. 模板中BOARD GEMETRY拼写、重复引用及不存在层，按原文实际执行结果单独登记，不静默改01env或虚构有效输出。不能把“原文加载”扩大成“所有文字引用都有效”。
5. 实际板框和模板OUTLINE必须都有可读的真实几何。不增自定义Film来代替模板，仍保留真正designOutline root用于机械/DRC。
6. 保存后另进程重开，从实际数据库核层、Film、规则和几何；确认当前有效DRC状态及输入SHA。输出生产包时仍须实际CAM验内容。

本机将三块副本从millimeters/3提高为millimeters/4，独立重开后每张Film的undefineLineWidth均实际保存0.0025；旧板0.002的量化差异已闭合。shapeBoundingBox=2.54及每张不同的fullContact/mirrored等值按原文核对。精度调整不能免除原几何和规则保真比较，详见补验与独立审查。

原生会过滤模板中的无效引用：SKILTOP/SKILBOTTOM及PDFTOP/PDFBOTTOM中的BOARD GEMETRY拼写错误；两层DisAll中的CONSTRAINT REGION/L2与L3不存在。重复引用也会由API合并。当前保留原文、记录实际有效成员，不改01env、不造假class，也不为了两层模板文字而增加内铜。

模板SKILTOP/SKILBOTTOM未包含REF DES/SILKSCREEN_*，PDFTOP/PDFBOTTOM才引用REF DES/ASSEMBLY_*。这意味着按模板加载Film不证明位号已进入丝印Gerber；实际内容待CAM审查。本轮按用户要求沿用模板，未擅改丝印映射。

FilmControl的每张Film及Options存入BRD；General Parameters的设备/格式参数另属art_param.txt，孔径表另属art_aper.txt。drill2/4只有FilmCreate，不设置全部CAM机器参数。本次验证完整Film定义与实际成员，不宣称已完成General Parameters或输出、审核生产包。

## 历史证据与今后防错

原28/29课的BRD、validation、源码及manifest不覆盖；它们仍可复核当时连接、几何和规则，但包含本次已撤销的物理MASK/不完整Artwork做法。父级笔记的更正前字节另有备份，本次记录清单保存修订前后SHA；旧manifest中的笔记SHA指向当时快照，不能误报为当前笔记哈希。

长期规则已补入[pcb_layer_naming.md](pcb_layer_naming.md)；[EDA.md](../../EDA.md)开头、[课程索引](../../课程索引.md)和[F阶段总结](lessonF_27_29_20261019.md)统一指向新v4。以后验收必须包含“物理MASK=0、全部Film集合、全部成员和Options、真实板框进入模板”，不能重复只验铜层的盲点。

本轮仍是学习板；79个器件待布局，L2/L3正式参考铜尚未铺，USB90Ω几何、连接器板厚装配、阻焊桥与实际工艺等开放条件不因本次纠错消失。GUI操作和完整生产包审核仍按原状态单列。
