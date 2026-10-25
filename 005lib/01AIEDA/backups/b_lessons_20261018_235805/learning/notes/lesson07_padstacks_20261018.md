# 第7课：圆孔、非镀铜孔、镀铜槽孔与实际四层映射

日期：2026-10-18（Asia/Shanghai）。软件实测：Cadence Allegro / Padstack Editor 17.2 S045 Windows 64-bit。课程目录：D:\001DIY\005lib\01AIEDA\learning\examples\lesson07_padstacks。

**本课结论：三种最终教学 padstack 的孔几何、镀铜属性、0°/90°实例、默认内部焊盘和 TOP–L2–L3–BOTTOM 实际映射已完成，并通过保存后独立进程重开验收。纯无铜 NPTH 的无警告批处理、真实动态铜除铜、负片热焊盘 flash 和制造出图仍待后续。**

本课使用官方 CLI 和 AXL SKILL。属于隔离学习库和教学 coupon；这些尺寸没有真实器件或制造商认证。根目录 EDA.md / 课程索引由主任务统一维护。

## 1. 本课输入、操作顺序与用户固定规范

最终定义保存在 [lesson07_spec_v4.json](../examples/lesson07_padstacks/lesson07_spec_v4.json)。初始 spec_bundle.json、spec_v2/v3 和失败日志保留为学习历史；最终运行和验收以 v4 为准。

操作顺序：

1. 查本机官方 PXML 样例、Padstack Editor / AXL 帮助。
2. 用 padstack_editor.exe -x 逐个导入最终三个 PXML；检查日志与程序实际退出。
3. 新建六孔 PACKAGE coupon，每种孔各一个 0° 和 90°实例；保存 .dra，编译 .psm。
4. 独立进程 -readonly 重开 .dra，读取实际孔、pad、mask、paste、默认内层和 polygon。
5. 新建隔离四层板；用官方 axlXSectionCreate 创建实际内层，放入编译后的 coupon，保存 .brd。
6. 独立进程 -readonly 重开 .brd，检查实际四个铜层。
7. 再次只读重开 coupon，检查用户固定的三项文字锚点和 PACKAGE_HEIGHT_MAX。
8. Python 将保存后读回数据与独立教学 spec 比较，输出 validation.json。

用户层叠命名已应用：四层为 **TOP–L2–L3–BOTTOM**。DEFAULT_INTERNAL 是 padstack 的官方默认内部定义，不是板层名称。板上没有用电源/地网络名替代物理层序号。

用户封装固定规范已在 [reopen_defaults/required_texts.tsv](../examples/lesson07_padstacks/logs/reopen_defaults/required_texts.tsv) 独立读回：

| 对象层 | 文字 | X / Y / rotation |
| --- | --- | --- |
| REF DES/SILKSCREEN_TOP | U* | 0 / 0 / 0 |
| REF DES/ASSEMBLY_TOP | U* | 0 / 0 / 0 |
| COMPONENT VALUE/ASSEMBLY_TOP | VALUE | 0 / 0 / 0 |

[defaults.txt](../examples/lesson07_padstacks/logs/reopen_defaults/defaults.txt) 读回一个 PLACE_BOUND_TOP，bbox = ((-7,-6),(7,6))，属性 PACKAGE_HEIGHT_MAX = "1 MM"。1 mm 是封装最大高度，不是文字字高。

## 2. 最终三个教学定义

全部单位为 mm，drawing accuracy 为 3；所有铜层零偏移，双面阻焊；没有非 NULL 锡膏图形。

| 最终 padstack | 孔 / 镀铜 | 顶 / 底 / 默认内层 REGULAR | 双面阻焊 | THERMAL | ANTI | KEEPOUT |
| --- | --- | --- | --- | --- | --- | --- |
| eda_l07_pth_080_c160 | 圆孔 Ø0.8，Y | CIRCLE Ø1.6 | Ø1.8 | CIRCLE Ø1.8 | CIRCLE Ø2.0 | 无 |
| eda_l07_npth_200_ring | 圆孔 Ø2.0，N | CIRCLE Ø3.0 | Ø3.2 | 无 | 无 | CIRCLE Ø3.5 |
| eda_l07_plated_slot_200x100 | OVAL_SLOT，X2.0 / Y1.0，Y | OBLONG X2.8 / Y1.8 | X3.0 / Y2.0 | OBLONG X3.0 / Y2.0 | OBLONG X3.2 / Y2.2 | OBLONG X3.2 / Y2.2 |

NPTH ring 是**另一个明确用途的有铜环非镀铜孔**：孔壁不镀铜，但板面与内部层可以存在名义铜环。它以无编号机械 pin 创建、不接网。不能把它称为“纯无铜机械孔修复成功”，也不能由 isThrough=t 推定它有导电孔壁或把各层铜环电气连通。

PTH 的 CIRCLE THERMAL 与槽孔的 OBLONG THERMAL 是本课观察的 padstack 数据定义。它们不等于已验证的四辐条负片热连接 flash。正片动态铜连接/除铜规则、辐条参数与负片制造输出没有在本课完成。

## 3. PXML 精确入口与字段

官方非图形入口：

    C:\Program0\Cadence\SPB172\tools\bin\padstack_editor.exe -x <file.pxml>

本课实际逐个通过 PowerShell Start-Process 启动，WindowStyle Hidden、独立工作目录和 ALLEGRO_PCBENV、stdout/stderr、15 秒有界等待；不改全局 HOME、安装文件或执行策略。

PXML 用法：

- padstackusage：THRU_PIN / MECH_HOLE / SLOT。
- slothole holetype：CIRCLE / OVAL_SLOT；槽孔配 SLOT usage。
- plating：Y / N。
- layer：BEGIN_LAYER / DEFAULT_INTERNAL / END_LAYER；板上映射到 TOP / 实际内层 / BOTTOM。
- mask：TOP_SOLDER_MASK_PAD / BOTTOM_SOLDER_MASK_PAD。
- pad type：REGULAR_PAD / THERMAL_PAD / ANTIPAD_PAD / KEEPOUT。
- pad figure：CIRCLE / OBLONG；NONE 用于历史 NULL 尝试。
- offset：(0;0)。
- 槽孔 PXML width=2.000、height=1.000；实际导入后由 drillSizeWidth=2、drillSizeHeight=1 验证了 X/Y 方向。
- 本课 PXML 不发出 paste-mask 定义；读回可能返回 NULL pad 对象，不能只检查 dbid 是否非 nil。

原始 PXML、生成 .pad 和 import.log 全部在 [library](../examples/lesson07_padstacks/library) 与 [logs](../examples/lesson07_padstacks/logs)。最终三份日志都只有 Info-Processing，无 Warning-/Error-，且三次导入进程正常结束。

## 4. NPTH 警告分支与正确解释

以下样本均保留输入、生成输出、日志和进程停止证据，没有隐藏警告或关闭校验：

| 名称 | 定义意图 | 实际结果 / 状态 |
| --- | --- | --- |
| eda_l07_npth_200 | 全层 NULL regular，ANTI + KEEPOUT | 三层报 Thermal pad must be defined when an anti pad is added；主任务停止其所属导入进程 9696 |
| eda_l07_npth_200_ko | 全层 NULL regular，仅 KEEPOUT | 报 no default internal pads；BEGIN/END keepout 缺少 Regular/Thermal/Anti，keepout 会移除；本课安全停止所属进程 1388 |
| eda_l07_npth_200_spot | Ø2 NPTH，Ø0.2 可钻掉 spot，KEEP OUT Ø2.5 | 报三层 Drill hole size exceeds pad size；本课安全停止所属进程 10760 |
| eda_l07_npth_200_ring | Ø2 NPTH，Ø3 nominal 铜环，KEEP OUT Ø3.5 | 无警告导入；几何、非镀铜、机械 pin 和持久性验收通过；属于不同教学用途 |

官方允许 non-plated hole 使用 NULL 或钻掉的小 spotting pad，但 17.2 S045 的通用库检查仍可能报告上述警告并让批处理停在对话框。因此“用途可解释”“.pad 已生成”“批处理可无警告正常退出”是三件不同的事。

17.2 已取消旧 ARK（antipad-as-route-keepout）选项，旧值迁入 Keepout 字段。官方说明 same-layer keepout 需要该层有 regular pad；本次全 NULL + KEEPOUT 导入实际警告并删除外层 keepout，证实仅填写尺寸不能保证有效。

保留真正无铜机械孔意图时，应在后续板级课程建立并验证独立 keepout / hole-to-copper / 动态铜 DRC void 方案。不能为压掉警告而给无铜 NPTH 虚构 thermal 连接铜。本课也没有把官方 spot 方法的警告强行改成成功。

## 5. 实际 API 读回方法与新知识

主要源码：[lesson07.il](../examples/lesson07_padstacks/scripts/lesson07.il)。

孔字段来自 pin->definition：

    holeType / plating / drillDiameter / drillSizeWidth / drillSizeHeight
    drillOffset / usage / isThrough / startEnd
    axlDBGetDrillPlating(ps->name)

实测精化：

| 对象 | drillDiameter | drillSizeWidth / Height | holeType / plating |
| --- | --- | --- | --- |
| PTH 圆孔 | 0.8 | 0 / 0 | circle_drill / PLATED |
| NPTH ring 圆孔 | 2.0 | 0 / 0 | circle_drill / NON_PLATED |
| 镀铜槽孔 | 1.0（不能按圆孔解释） | 2.0 / 1.0 | oval slot / PLATED |

本机 API 与帮助概述不完全相同：**圆孔直径以 drillDiameter 为准，不要求 drillSizeWidth/Height 等于直径；槽孔以两个尺寸和 holeType 为准，不以 drillDiameter 代替槽孔几何。** API 可能返回 oval slot（空格）或不同大小写，验证按语义规范化；axlDBGetDrillPlating 返回 NON PLATED，与字段 NON_PLATED 的拼写也不同。

焊盘读取：

    axlDBGetPad(pin "ETCH/TOP" "REGULAR")
    axlDBGetPad(pin "ETCH/L2" "REGULAR")
    axlDBGetPad(pin "ETCH/L3" "REGULAR")
    axlDBGetPad(pin "ETCH/BOTTOM" "REGULAR")
    axlDBGetPad(ps 'internal "REGULAR")
    axlDBGetPad(ps 'internal "ANTI")
    axlDBGetPad(ps 'internal "THERMAL")
    axlDBGetPad(ps 'internal "KEEPOUT")
    axlDBGetPad(pin "PIN/SOLDERMASK_TOP" "REGULAR")
    axlDBGetPad(pin "PIN/PASTEMASK_TOP" "REGULAR")

同时查各类型 figureName、bBox、width/height，空图形接受 NULL 或不存在。不能用 axlPadOnLayer=t 单独证明正铜存在，因为该 API 也考虑 ANTI/THERMAL 和 pad suppression。

本课 90°槽孔实例的 regular bbox 从 2.8×1.8 变为 1.8×2.8；mask、thermal、anti、keepout 同样换轴。**实例 axlDBGetPad(pin)->bBox 虽相对 pin 原点，但已包含旋转；不能把它当未旋转模板，再旋转一次。** padstack definition 的默认内部 bbox 用于检查原始定义；两者应区分。

axlPolyFromDB(pin ?layer ... ?padType 'REGULAR) 用于核对实际实例的板坐标 bbox。NPTH ring 读回 area=7.068583，正好是 Ø3 外圆面积，说明该多边形读回没有代替最终钻孔扣铜验收。孔属性、铜 pad 属性和制造时钻孔扣除必须分别理解；本课不由这些 area 声称已验证真实剩余铜量。

## 6. 保存前缓存、退出码与持久性

首轮 create_package 中六次 axlDBCreatePin 都成功返回，但保存前 design->pins 计数仍为 0。过早断言导致脚本退出，无保存、无 COMPLETE。此失败源码保存在 logs/create_package/failed_source.il，原日志保留。

随后按已知数据库缓存行为修正：保存前只记录计数，以保存并独立重开的实际数据库为准。create_package02 成功保存、编译；reopen_package 读到完整 6 个 pin。这不是“机械 pin 被放到别的集合”的结论。

本课 .scr 用 errset，因此 SKILL 函数失败时 Allegro 仍可能 exitCode=0。验收同时要求：

- stdout 无未处理目标错误；
- 课程报告 COMPLETE 标记；
- 预期文件实际存在；
- 新进程读回符合 spec；
- -readonly 前后哈希一致。

DRA SHA256：

    7EBAE8163DD7D14025E35D9AFD13D2F9775099F727AFFD72E3B1D47CD8EB9AD2

BRD SHA256：

    2908A28307E096BBABCB4C1AA18A52DF4DD82BE7F5F72E7FED0A3E64A7CEB2CD

封装和四层板分别独立只读重开，均真实 exitCode=0、readonlyHashUnchanged=true。固定文字规范也独立重开确认，DRA 哈希保持不变。

创建封装/板的 stdout 出现 SPMHUT-48（Scaled value has been rounded off）。没有把它归入“无警告导入”表述，也没有擅自断言其具体原因；关键孔与焊盘数值已通过保存后独立读取。此后未为掩盖提示而更改精度或关闭检查。

## 7. 四层板与验收范围

官方 axlXSectionModify / axlXSectionCreate 建立两层内部 conductor，每个新 conductor 后插入 dielectric；axlDBCreateSymbol 从本课私有 .psm 放置六孔 coupon。

[stackup.tsv](../examples/lesson07_padstacks/logs/reopen_board/stackup.tsv) 实际顺序：

    TOP / dielectric / L2 / dielectric / L3 / dielectric / BOTTOM

所有铜层为正片。L2、L3 厚度 0.035 mm；三个 dielectric 各 0.4 mm；TOP/BOTTOM 保留新板默认 0.03048 mm。此处验证层名和映射 API，不是经过板厂确认的物理层叠/阻抗推荐。cross-section 厚度可以保存比 drawing accuracy 更多的小数位。

[validation.json](../examples/lesson07_padstacks/validation.json)：allChecksPass=true，650 项对照检查，failures=[]。

- package 重开：6 pin、72 条 layer/type pad 读回、12 条 regular polygon。
- 四层 board 重开：6 pin、120 条 layer/type pad 读回、24 条 regular polygon。
- 实际 TOP / L2 / L3 / BOTTOM 的 regular / anti / thermal / keepout 和双面 mask/paste 均对照教学 spec。
- 默认内部定义和实际板内层分别验收。
- 两个角度、mechanical 属性、孔镀铜、槽孔方向、编号和板坐标均验证。

四层板读回 stored_drcs=0，但 drc_state=nil；这不是有效完整 DRC 通过的结论。封装 drc_state=t 也不能替代制造出图、真实电气意图或板级铜连接检查。

本课完成状态：**基础孔定义 / 持久化 / 旋转 / 实际四层映射完成**。以下仍未完成：

- 纯无铜 NPTH 的无警告自动批处理流程。
- 动态铜除铜、孔到铜 clearance、keepout 启用和有效性。
- PTH/slot 真实 thermal 辐条及负片 flash / Gerber 输出。
- 制造钻孔扣铜、环宽公差、焊接与实物验证。
- 将这些规则用于带网络的真实电源/信号布线质量审查。

## 8. 可复现材料与下一课

- [最终教学 spec](../examples/lesson07_padstacks/lesson07_spec_v4.json)
- [AXL 源码](../examples/lesson07_padstacks/scripts/lesson07.il)
- [独立 Python 验收源码](../examples/lesson07_padstacks/scripts/validate.py)
- [package 原生启动器](../examples/lesson07_padstacks/scripts/launch_package17.py)
- 公共学习启动器：learning/scripts/launch_cadence17.py（真实 subprocess exitCode、只读哈希、有界等待）
- scripts/create_package02.scr、reopen_package.scr、create_board.scr、reopen_board.scr、read_defaults.scr。
- library 中三份最终 PXML/.pad、coupon .dra/.psm 和 mapping_4layer.brd。
- logs 中每轮命令参数、stdout/stderr、launch.json 和 TSV；警告分支另有 termination.json。
- [artifact_manifest.json](../examples/lesson07_padstacks/artifact_manifest.json) 保存归档文件大小和 SHA256。

再次执行创建应使用新输出名或独立目录；启动器主动拒绝覆盖已有创建目标和已有 launch.json 的日志目录。读取可以使用新的日志目录。PXML 导入可能覆盖同名 pad，不能在公共库里直接重复实验。

下一课可在隔离四层教学板建立明确网络的正片铜、正确机械孔 keepout / hole clearance / copper void，重新计算有效 DRC，再观察真实孔周围铜与返回路径。负片 thermal flash 作为独立制造输出课处理。

## 9. 本机官方出处

以下是本机随软件安装的官方材料，未修改：

- share/pcb/examples/padstack_xml/padstack_xml.docx：usage、hole/figure/units/offset 枚举与 -x 说明。
- share/pcb/examples/padstack_xml/thru_pin.pxml：10–11 行圆孔/Y；43、64、85 行 CIRCLE THERMAL；56 行 DEFAULT_INTERNAL；114、120 行双面 mask。
- share/pcb/examples/padstack_xml/via1.pxml：NON-plated N、偏移、现代 drill 字段与各 pad 类型。
- share/pcb/xml-formats/cdn_padstack.dtd：PXML 结构参考；该安装文件标记 prototype，官方样例与其部分字段次序/可选项并非完全一致，因此最终以官方 importer 检查和实际读回为准。
- doc/pcoms/pchap.html：4629 行层映射；5046/5054 行槽孔 X/Y；5305 行内部 pad 与 DRC；5326 行多种 pad 定义；5343/5629 行 keepout 定义与板级启用；5387、5590–5609 行 negative flash / positive DRC void；5611 行 NPTH NULL/spot；6778 行 -x 检查保存。
- doc/algPN/algPN.html：Keepout Features（约 11779–11816 行），same-layer keepout 与 regular pad 条件。
- doc/PCBmigration17x/coreAllegro.html：1219 行 ARK 淘汰、旧 antipad 转 Keepout。
- doc/algroskill/02dbdesc.html：Pad / Padstack / Pin / Design / XSection 属性。
- share/pcb/examples/skill/DOC/FUNCS/axlDBCreatePin.txt：nil pin text 创建机械 pin，仅在 PACKAGE/MECHANICAL symbol 使用。
- 同目录 axlDBGetPad.txt、axlDBGetDrillPlating.txt、axlPadOnLayer.txt、axlPolyFromDB.txt、axlXSectionCreate.txt、axlXSectionGet.txt、axlXSectionModify.txt、axlCompileSymbol.txt。
- share/pcb/batchhelp/allegro.txt：-safe、-nographic、-readonly、-symbol package、-s、-p 入口。

