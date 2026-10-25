# 第 3 课：器件、封装、引脚、网络与放置几何
日期：2026-10-17（Asia/Shanghai）
范围：P1 精细只读查询，进入 P2 焊盘/封装读取基础。创建、编辑、保存真实器件库及数据手册验收仍待后续实操。

## 前提与执行
软件为 Allegro 17.2-S045 Windows SPB 64-bit Edition，使用与第 2 课相同的 Allegro_performance、-safe、-readonly、-nographic、-s、-p 组合。
本课从安装目录复制 demo_ver_17p2.brd 到 learning/examples/lesson03_mapping，在副本上操作。
两次运行均只对启动子进程设置 ALLEGRO_PCBENV；未加载 ai_bridge、未启动 watcher、未创建 command.flag、未主动改全局 HOME 或用户启动文件。

- run01：执行 lesson03_inventory.scr，PID 21708；约 5 秒自行退出，summary 有 COMPLETE，journal 正常结束。
- run02_geometry：执行 lesson03_geometry.scr，PID 16312；约 5 秒自行退出，geometry 有 COMPLETE，journal 正常结束。
- 退出方式沿用 set NOCONFIRM / quit / fillin "yes"，没有保存板。
- 源样例和练习板 SHA256 均为 F2AC54090DEE0E67E2A734752C66AA6CFEFE9C604456324B889C79D9BFA77CB0。
- 本课没有重试桌面连接；第 2 课的 native pipe 不可用状态保留。此次成功来自软件内部官方接口。

## 关系与容易读错的字段

| 对象/字段 | 正确含义 |
| --- | --- |
| design->components | 逻辑器件实例集合，适合统计器件位号 |
| component->name | 位号，例如 U5、C1 |
| component->compdef | 逻辑器件定义；可由其 components 查询共用定义的实例 |
| component->symbol | 一个已放置封装实例；未放置为 nil，不是列表 |
| component->package | 器件封装名；本例与已放置 symbol definition 名对应 |
| symbol->definition | 共用物理封装定义 symdef；其 instances 为实例列表 |
| symbol->xy / rotation / isMirrored | 封装原点、方向和镜像；原点未必是器件中心 |
| pin->number | 物理引脚编号字符串，不能按列表次序当编号 |
| pin->name / definition | Padstack 名称 / 定义，不是电气引脚名称 |
| pin->functionPins~>name | 该 pin 对应的功能引脚名称列表 |
| pin->net | 通常是 net 对象，也可能是 dummy net 的空字符串；脚本先检查 dbid 类型 |
| pin->xy / rotation | 板上绝对坐标 / 绝对方向 |
| pin->relxy / relRotation | 相对未旋转、未镜像封装定义的坐标 / 方向 |

没有凭空使用 pin->padstack 或 axlDBGetPadInfo 等未在本机索引查到的名字。通过数据库集合遍历，没有修改选择集、可见层或过滤器。

## 全板对应关系实测

| 项目 | 结果 | 含义 |
| --- | --- | --- |
| 逻辑器件 | 57 | 56 已放置，Y1 未放置 |
| component pins | 640 | 636 有物理焊盘定义，Y1 的 4 个无定义 |
| 已放置 pin 分类 | 通孔 40、表贴 596 | 不把未放置的 4 个 nil through 标志当作表贴 |
| symbol 实例 | 59 | 56 PACKAGE + 3 MECHANICAL |
| Padstack 定义 | 12 | 包含机械等用途，不能直接当器件封装种类数 |
| 网络 | 95 | 只读取数据库归属，未判断连接质量 |
| 功能引脚记录 | 748 | 多逻辑功能可引用同一个物理编号 |
| component pin 的 owner 不一致 | 0 | 按 dbid 检查回链 |
| 已放置 pin 不在所属 symbol->pins | 0 | 未放置器件单列 |
| functionPin 回链不一致 | 0 | 同时检查所属 component 和 pin->functionPins |
| 重复“位号+编号”键 | 0 | 是本样例结果，不将其泛化成所有封装的规则 |

Y1 是 OSC-1 / OSC_DIP，逻辑 pin 1→UN1OSC1PB0、8→空网络、7→GND、14→VCC。
它的 symbol 为 nil、padstack/definition 为 nil，但 pin->xy 实际读到 (0,0)。因此不能把坐标非 nil 或 (0,0) 当成已放置依据。

三个无逻辑器件归属的机械 symbol 均名为 109，各含一个 pin；位置为 (0,0)、(3800,2100)、(0,2100) mil。它们不是额外三个电气器件。

748 个功能引脚覆盖 556 个唯一“位号+编号”目标：
492 个目标引用一次、8 个两次、52 个四次、4 个八次。640 个 pin 中另有 84 个没有 functionPins（VCC 32、GND 36、空网络 16）。
关系为 748 = (640 - 84) + 192 次重复功能引用。例如 U8 的 DIR→1、-E→19 各被八个逻辑功能引用。
因此不能用 function pin 行数当封装焊盘数。

## 例一：旋转 IC 的引脚与网络
U5：74F04-1 / SOIC14，封装原点 (2250,300) mil，270°，未镜像。

| 引脚编号 | 功能名 | 网络 | 实际坐标（mil） |
| --- | --- | --- | --- |
| 1 | A<0> | RESET | (2400,400) |
| 2 | -Y<0> | RESETL | (2350,400) |
| 14 | 无功能名记录 | VCC | (2400,200) |
| 7 | 无功能名记录 | GND | (2100,400) |

本课 function_pins 的 use 字段仅有 IN 364、OUT 266、TRI 118，没有 POWER/GROUND 记录。读取电源网络与编号成功，不等于验证了原理图 POWER/GROUND 类型或芯片数据手册引脚表。
本例为示范数据库，不推断它是用户 MCU 设计的可复用电路。

## 例二：镜像电容与层别
C1：CAP-.01UF / SMDCAP，封装原点 (825,1800) mil，0°、mirrored=t。

| 编号 | 功能名/网络 | 相对坐标 | 板上绝对坐标 |
| --- | --- | --- | --- |
| 1 | A<0> / VCC | (-100,0) | (925,1800) |
| 2 | B<0> / GND | (95,0) | (730,1800) |

如果简单执行“原点+相对坐标”，pin 1 会误算为 (725,1800)；实值为 (925,1800)。
共享 SMD50_87 padstack 的 span 字段为 TOP/TOP，C1 已镜像实例的 pin span 和非 NULL 焊盘却在 BOTTOM。层别应向实例查询，不能照搬模板层名。
padstack 的 plating 字段即使写 PLATED，也不独立证明有钻孔；本例 SMD hole_type=none、drill_diameter=0、type=smd。

## 按层焊盘、孔和阻焊读取
最小查询：
```skill
pad = axlDBGetPad(pin "ETCH/TOP" "REGULAR")
mask = axlDBGetPad(pin "PIN/SOLDERMASK_TOP" "REGULAR")
ps = pin->definition
polys = axlPolyFromDB(pin ?layer "ETCH/BOTTOM" ?padType 'REGULAR)
axlPadOnLayer(pin "BOTTOM")
```

- pad 的 bBox 永远为局部坐标；offset 相对 pin/via 原点。
- 用实例 pin 调用 axlPolyFromDB 得到放置多边形；本次旋转/镜像实例实测 polygon bbox 在板坐标附近。
- polygon 是临时几何对象，不是 dbid；只读转换没有创建 PCB 图形。
- axlPadOnLayer 默认考虑 pad suppression；第三参数 t 表示忽略 suppression。它回答 pad 是否存在，不证明网络连接或实际生产输出已经合格。
- 钻孔读取 definition 的 holeType、drillDiameter、drillSizeWidth/Height、drillOffset、plating；孔槽或多钻孔不能只看 diameter。
- Mask 查询用 PIN/SOLDERMASK_TOP/BOTTOM；不能直接把铜焊盘尺寸当阻焊开窗。

run01 共做 5088 次按层查询，返回对象中 3576 行 figure_name=NULL、1512 行为非 NULL 图形。对象存在也可能是 NULL 焊盘。
C1 pin1：TOP 为 NULL、on_layer=nil、polygon 数 0；BOTTOM 为 RECTANGLE、on_layer=t、polygon 数 1。
BOTTOM 局部 bbox 为 ((-25,-44),(25,43)) mil，局部范围 50×87 mil；实例 polygon bbox 为 ((900,1756.5),(950,1843.5)) mil，面积 4350 平方 mil。

C21 pin1：通孔 PAD60CIR36D、孔径 36 mil；TOP 圆形 bbox 局部 ((-30,-30),(30,30))，实例位于 (1700,1000)，polygon bbox 为 ((1670,970),(1730,1030))。TOP 铜范围 60×60 mil，TOP 阻焊查询范围 75×75 mil。此处仅记录示例数据库尺寸，尚未按具体器件数据手册验收。

## 本课发现的精度差异
设计单位/精度为 ("mils" 0)。C1 同一 BOTTOM polygon 的 bbox Y 为 1756.5–1843.5，vertices 的 Y 为 1756–1843；高度均 87 mil，位置相差 0.5 mil。
已查官方 polygon 属性和 axlPolyFromDB 说明，未找到该差异的确切原因；不归因于截断、镜像或输出格式。暂不将这一样例用于制造尺寸或边缘间距合格判定。后续编辑与精确尺寸核对需要单独验证几何精度及正确查询方式。

## 文件、复现和当前边界
- learning/scripts/lesson03_inventory.il：只定义查询函数，加载本身不导出；调用 edaL3Export(outDir)。
- learning/scripts/lesson03_geometry.il：只定义代表性实例查询；调用 edaL3Geometry(outPath)，依赖前一脚本的辅助函数。
- 对应 .scr：加载后调用函数，随后 quit，不保存设计。
- learning/logs/lesson03_mapping_20261017/run01：7 份 TSV、摘要、启动参数、journal 和 stdout/stderr。
- run02_geometry：选定 C21、C1、U17、Y1 的 208 次按层几何查询、启动参数与 journal。
- learning/logs/lesson03_result_20261017.json：行数、回链、哈希与运行状态汇总。
- 复现前创建新运行目录并调整 .scr 的输出路径；不要覆盖原始日志。当前 TSV 是该示例的查询输出，非生产 BOM 或贴片坐标交付。

没有导入对应 Capture 原理图，也没有对照真实器件数据手册；因此本课核对的是当前 PCB 数据库内部对应关系。未修改布局、走线、铜皮或规则，未完成去耦/回流/SI/PI/EMI 设计审查。

## 官方出处
- [对象属性](C:/Program0/Cadence/SPB172/doc/algroskill/02dbdesc.html)：Generic/Common Figure、Component、Symbol、Symdef、Pin、FunctionPin、Pad、Padstack 表。
- [读取数据库](C:/Program0/Cadence/SPB172/doc/algroskill/07dbaccs.html)：axlIsDBIDType、axlDBGetPad。
- [多边形操作参考](C:/Program0/Cadence/SPB172/doc/algroskill/20plyopr.html)：polygon 属性、axlPolyFromDB。
- [实例焊盘存在性](C:/Program0/Cadence/SPB172/doc/algroskill/25dbmisc.html)：axlPadOnLayer。
- [局部坐标说明](C:/Program0/Cadence/SPB172/doc/algroskill/sipapd.html)：axlCompAddPin 的未旋转、未镜像符号原点基准。
- [安装自带多边形说明](C:/Program0/Cadence/SPB172/share/pcb/examples/skill/DOC/FUNCS/axlPolyFromDB.txt)。
- 官方 pads.il 混合只读和创建测试，本课未整体执行其测试入口。

下一课：P2 的 Padstack 与简单封装创建/编辑，练习保存后重新打开并按已知练习尺寸读回核对；真实器件库继续以具体数据手册为依据。
