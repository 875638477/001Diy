# 第 5 课：从公共 PSM 到 PCB 实例，移动、旋转、镜像与持久性

记录日期：2026-10-18。环境：Windows，Allegro PCB Designer 17.2-S045，`Allegro_performance` 产品入口。

状态：create02 已完成实例操作和保存；独立新进程只读重开已完成；标准库 Python 独立数值验收 PASS，13,088 条断言、0 个问题。本文基于create02/reopen及已完成的repeat独立复现实验，后者创建/重开实际exitCode均为0，原始Qt异常本次未复现，原因未定位。原始 create02 的 Qt ASSERT 必须保留，不把持久性通过写成日志完全正常。

## 1. 学习目标与本课范围

1. 把已编译的公共 `.psm` 加载为真实 BOARD 中的 PACKAGE 实例，区分封装定义和实例。
2. 通过 Allegro 原生 SKILL 实际移动、旋转、镜像实例，读取所属引脚和非引脚子对象，验证操作结果。
3. 验证铜、阻焊、锡膏的实际图层映射；核对铜焊盘真实多边形 bbox、顶点和面积。
4. 验证三项文字随实例变换，Place Bound 随实例换层，1 mm 高度属性仍保留。
5. 保存后重新取得对象，并在另一个原生只读进程重开，核对数据持久性。

本课的三个对象是 `refdes=nil` 的未分配 PACKAGE symbol 实例。没有把它们误记为三颗已通过 Capture 网表连接的器件；未验收网络、电路功能、布局布线或 SI/PI/EMI。SI/PI/EMI 是后续实际布局布线的基本要求，本课未以仿真代替这些要求。

## 2. 官方资料与准确锚点

本机官方帮助根目录：`C:/Program0/Cadence/SPB172/doc/`。以下为真实 HTML 文件、锚点和辅助行号；可以在本机浏览器打开文件后查对应锚点。

| 主题 | 相对官方帮助根目录的文件与锚点 | 行号 |
|---|---|---:|
| axlDBCreateSymbol | `algroskill/03dbcre8.html#439738` | 3350 |
| axlTransformObject | `algroskill/06intedt.html#821370` | 4201 |
| Symbol 属性表 | `algroskill/02dbdesc.html#604789` | 4492 |
| Pin 属性表 | `algroskill/02dbdesc.html#610509` | 3659 |
| Text 属性表 | `algroskill/02dbdesc.html#604970` | 4904 |
| axlDBGetDesign | `algroskill/07dbaccs.html#700317` | 652 |
| axlIsDBIDType | `algroskill/07dbaccs.html#705289` | 771 |
| axlDBGetAttachedText | `algroskill/07dbaccs.html#700342` | 818 |
| axlDBGetPad | `algroskill/07dbaccs.html#700355` | 865 |
| axlDBGetProperties | `algroskill/07dbaccs.html#700383` | 1392 |
| axlDBGetDesignUnits | `algroskill/07dbaccs.html#700396` | 1525 |
| axlDBRefreshId | `algroskill/07dbaccs.html#700407` | 1557 |
| 仅刷新当前对象、不递归刷新子对象 | `algroskill/07dbaccs.html#700412` | 1582 |
| axlPolyFromDB | `algroskill/20plyopr.html#1076123` | 749 |
| axlPadOnLayer | `algroskill/25dbmisc.html#1095281` | 1754 |
| axlGeoRotatePt | `algroskill/24mthutl.html#1082761` | 586 |
| axlSaveDesign | `algroskill/14dsnctl.html#690505` | 993 |
| 保存清除 dbid handles/selection set | `algroskill/14dsnctl.html#729827` | 1024 |
| axlDBChangeDesignExtents | `algroskill/14dsnctl.html#706236` | 1132 |
| axlDBChangeDesignOrigin：offset 语义 | `algroskill/14dsnctl.html#706271` | 1186 |
| axlDBChangeDesignUnits | `algroskill/14dsnctl.html#706311` | 1229 |
| 高度属性附于 frectangle/shape | `algrolibdev/chap3.html#1037120` | 1561 |
| PlaceBound TOP/BOTTOM | `algrolibdev/chap3.html#1037123` / `#1037122` | 1600 / 1586 |
| Place Bound 仅有 MAX 时 MIN 默认 0 | `algrolibdev/chap3.html#1046148` | 1520 |
| PACKAGE_HEIGHT_MAX/MIN 总说明 | `propref/properties.html#973754`，另有 `#package_height_max` / `#package_height_min` | 12833 |

`axlTransformObject` 支持表及注意事项位于该函数条目下：多项同时传入时执行顺序为 move → mirror → rotate；正角逆时针；symbol 支持 move/mirror/rotate，表中不支持 `'GEOMETRY`。不支持的变换可能静默忽略；`?allOrNone t` 只处理数据库失败，不能保证每个请求都已执行。不要把同一个 symbol 与其 pins 一起传入变换列表（行 4787）。

## 3. 输入、规格和实例目标

工程根目录：`D:/001DIY/005lib/01AIEDA/learning/examples/lesson05_instances/`，下文记作 `$base`。

输入公共库（本课只读加载，不修改）：

- PSM：`D:/001DIY/005lib/01Psm_lib/qmi8610_lga16_3d3_p0d5.psm`
- 对应 DRA：`D:/001DIY/005lib/01Psm_lib/qmi8610_lga16_3d3_p0d5.dra`
- Padstack：`D:/001DIY/005lib/01Pad_lib/qmi8610_smd061x032_m05_p100.pad`
- 封装源规格：`D:/001DIY/005lib/01AIEDA/learning/examples/qmi8610/qmi8610_spec.json`
- 本课目标规格：`$base/spec.json`

封装源规格为 16 个周边引脚，无中心焊盘；铜/paste 0.61×0.32 mm，mask 0.71×0.42 mm。铜/paste、mask 的尺寸是已保存的源规格；其中 mask/paste 为工程选型，不能改写为数据手册直接规定。

本课设置 mm、accuracy=3，drawing extents `(-30,-15)–(30,15)`。实例 ID 是验证器的案例名称，不是板中 refdes。

| 案例 | 初始原点 mm | 操作 | 最终原点 mm | 最终旋转 | 最终面 |
|---|---|---|---|---:|---|
| MOVE | (-10,-2) | 增量 (1.877,5.456) | (-8.123,3.456) | 0° | TOP |
| ROTATE | (0,-2) | 围绕自身原点 +90° | (0,-2) | 90° | TOP |
| MIRROR | (10,-2) | 围绕自身原点 mirror=t | (10,-2) | 0° | BOTTOM |

## 4. 原生操作步骤

### 4.1 创建独立 BOARD 并从 PSM 放置实例

本课用 Allegro 官方命令行 `-s` 执行 `.scr`，由 `.scr` 加载本地 SKILL 文件；没有用自制画布点击控制。

create02 的启动参数记录在 `$base/logs/create02/launch.json`：

```text
C:/Program0/Cadence/SPB172/tools/bin/allegro.exe
  -product Allegro_performance -safe -nographic
  -s $base/scripts/create.scr
  -p $base/logs/create02
  $base/lesson05_instances.brd
```

`$base` 是此处说明用的占位符，原始 `.scr` 内为绝对路径。实际复现必须按第 9 节创建新的运行目录，不直接重复覆盖上述产物。

`l5Create(base)` 先检查当前 drawing basename 为 `lesson05_instances` 且 `axlDesignType(t)="BOARD"`，设置单位、精度和边界，再设置隔离的 `padpath/psmpath` 并创建三个实例：

```lisp
axlDBChangeDesignUnits("millimeters" 3)
axlDBChangeDesignExtents(list(-30.0:-15.0 30.0:15.0))
axlSetVariable("padpath" list("D:/001DIY/005lib/01Pad_lib"
                              "D:/001DIY/005lib/01Psm_lib"))
axlSetVariable("psmpath" list("D:/001DIY/005lib/01Psm_lib"))
a=car(axlDBCreateSymbol(list("qmi8610_lga16_3d3_p0d5" "PACKAGE")
                       -10.0:-2.0 nil 0.0))
```

另两个实例原点为 `(0,-2)` 和 `(10,-2)`。`axlDBCreateSymbol` 会先找 drawing 内的 definition，再找 PSMPATH；此入口用于 BOARD，官方明确不用于 symbol editor。第一参数为 `("symbolName" "PACKAGE")` 且未给 refdes，因此本课 symbol 的 refdes 为 nil。

### 4.2 导出 before 快照

`l5Dump(symbols outDir)` 输出 `symbols.tsv / pins.tsv / children.tsv`。读取 symbol、pin、children 前分别调用 `axlDBRefreshId`，避免把缓存属性当新状态。`symbol->children` 是非 pin 图形，pins 单独来自 `symbol->pins`。

每个引脚查询六层：

```text
ETCH/TOP                       ETCH/BOTTOM
PIN/SOLDERMASK_TOP              PIN/SOLDERMASK_BOTTOM
PIN/PASTEMASK_TOP               PIN/PASTEMASK_BOTTOM
```

`axlDBGetPad(p layer "REGULAR")` 读取具体层的焊盘；铜层另外用 `axlPolyFromDB(p ?layer layer ?padType 'REGULAR)` 取得真实实例多边形。Pad bbox 为相对 pin anchor 的范围，并已包含 pin 的旋转；不能不看 rotation 就把其宽高与 padstack 未旋转尺寸比较。`axlPolyFromDB` 结果为临时 polygon，不是 dbid。

当前导出的 `on_layer` 是 `axlPadOnLayer(p "TOP"/"BOTTOM")` 的铜面查询；它并非独立的 mask/paste 是否存在查询。mask/paste 的有效性本课由 `figureName` 与尺寸读回核对。

### 4.3 实际移动、旋转、镜像

```lisp
r=axlTransformObject(a ?move 1.877:5.456 ?allOrNone t)
r=axlTransformObject(b ?angle 90.0 ?origin b->xy ?allOrNone t)
r=axlTransformObject(c ?mirror t ?origin c->xy ?allOrNone t)
```

每次操作后，先兼容实际返回类型，再刷新对应 symbol，读取 `xy/rotation/isMirrored`，最后导出 after 快照。镜像 `t` 同时反转 X 几何并映射 TOP/BOTTOM；不能把它仅解释为视觉翻转。此处每次只传一个完整 symbol，不单独变换其 pins。

### 4.4 保存、重新取得 dbid，再新进程只读重开

```lisp
saved=axlSaveDesign(?design strcat(base "/lesson05_instances.brd")
                    ?noMru t ?noConfirm t)
unless(saved error("Save failed\n"))
syms=axlDBGetDesign()->symbols
l5Dump(syms strcat(base "/logs/create02/after_save"))
```

不能继续解引用保存前的 dbid。官方说明保存清除全部 dbid handles 和 selection set；本课保存后重新取得 symbols 并导出 after_save。

随后启动另一进程只读重开，参数记录在 `$base/logs/reopen/launch.json`：

```text
allegro.exe -product Allegro_performance -safe -nographic -readonly
  -s $base/scripts/read.scr -p $base/logs/reopen
  $base/lesson05_instances.brd
```

两份 `.scr` 末尾为 `set NOCONFIRM` 配合 `quit`；原文件还带 `fillin "yes"`，本次只读 journal 显示程序在 `quit` 后已经结束，后者没有执行。不要改写成必须靠 fillin 才能退出。

## 5. 独立坐标、方向和几何验收方法

设规格中的局部 pin 中心为 `(u,v)`，实例原点为 `(ox,oy)`，读回实例角度为 θ。镜像时先令 `u=-u`，然后：

```text
x = ox + u cosθ - v sinθ
y = oy + u sinθ + v cosθ
```

未镜像 pin 的绝对角度为 `θ+α`；镜像后为 `θ−α`，按 360° 取模，α 为源规格 pin rotation。`relxy/relRotation` 仍对照未变换的封装局部定义。真实例子：MIRROR 的 pin16 `relRotation=90°`、绝对 `rotation=270°`，不是 90°。

对矩形铜/mask/paste，把中心四个局部角点按 α 旋转，再按 symbol 镜像和 θ 变换，得到期望 bbox 和真实铜多边形顶点。验证器独立使用 Python 数学函数，没有调用 Cadence 变换 API来生成期望值。铜 polygon 还核对顶点数、直边半径=0、bbox 与顶点极值、鞋带公式面积，避免仅凭尺寸相同就判定位置正确。

三项文字锚点均来自源规格 `(0,0)`，因此实例中应等于 symbol 原点；文字 angle/mirror 和 layer 同时核对。PlaceBound 四角按相同实例变换，检查 TOP/BOTTOM、filled=t、`PACKAGE_HEIGHT_MAX="1 MM"`。本课没有额外设置 MIN；官方规则为只设 MAX 时 MIN 默认 0。

## 6. 已验证结果

独立验证器仅用 Python 标准库，数值误差阈值为 `1e-7 mm`，不是放宽到 0.001 mm 后容忍一格误差。before、after、after_save、reopen 四阶段分别与规格/预期状态核对，共 13,088 条断言，0 个问题。

每阶段均为：

| 项目 | 数量/结果 |
|---|---|
| symbol | 3，每个 pins=16、children=11 |
| 物理引脚 | 48 |
| 六层焊盘查询行 | 288 |
| 有效 RECTANGLE / NULL | 144 / 144 |
| 铜真实 polygon / 顶点 | 48 / 192 |
| 文字 / PlaceBound / path | 9 / 3 / 21 |
| after→after_save | 三表语义与字节完全一致 |
| after_save→reopen | 三表语义与字节完全一致 |

文字结果：MOVE 的三项锚点 `(-8.123,3.456)`、角度 0、未镜像、TOP；ROTATE 的三项锚点 `(0,-2)`、角度 90、未镜像、TOP；MIRROR 的三项锚点 `(10,-2)`、角度 0、镜像 t、均正确转到 BOTTOM。每个实例为 `U* / U* / VALUE`，没有多漏。

PlaceBound 结果：

- MOVE：`(-10.123,1.456)–(-6.123,5.456)`，TOP。
- ROTATE：`(-2,-4)–(2,0)`，TOP。
- MIRROR：`(8,-4)–(12,0)`，BOTTOM。
- 三者均 filled=t、高度 `1 MM`。

重开摘要为 `units=("millimeters" 3) symbols=3 drcs=0 drcState=t`，含 `LESSON05_READ COMPLETE`。`logs/reopen/allegro.jrl` 含 Journal end。

重开前后 BOARD SHA256 均为：

```text
DC3B9C79C8E102F59A2BA9BD581A6759CE139BAEEE8840326EEEA4A46C9C4EF4
```

独立验证器运行期间，所有读取的本课输入及 source spec 哈希不变。这项检查只证明本次验证器未改变所读文件，不能替代上面专门记录的原生只读重开前后 BOARD 哈希。

## 7. 实际错误、修正与未解决异常

### 7.1 单对象返回类型不能无条件 car

初次 `logs/create/stdout.txt` 记录：

```text
E- *Error* car: argument #1 should be a list ... - dbid:...
```

官方说明返回列表，但本机这次单对象 `axlTransformObject` 实际返回 dbid。错误发生在脚本对返回值无条件 `car`；不能据此写成底层移动功能失败。create02 改为：

```lisp
unless(r error("Transform failed\n"))
a=if(axlIsDBIDType(r) then r else car(r))
a=axlDBRefreshId(a)
```

本地应兼容已观察到的 dbid/list 两种返回，不把该配置观察直接推断为所有版本的统一行为。初次日志保留用于复现，不与成功阶段的数据混用。

### 7.2 dbid 类型不等于当前有效

create02 记录 `old_symbol_dbid_is_type_after_save=t`。`axlIsDBIDType` 只用于类型判断，不能证明保存前对象现在可安全解引用。本课刻意不读旧对象属性，重新取得 root/symbols 后再导出。`axlDBRefreshId` 刷新缓存，不会修复已经 out-of-scope 的 dbid，也不会递归刷新所有子对象。

### 7.3 Qt ASSERT

`logs/create02/stderr.txt` 含 `ASSERT failure in QCoreApplication::sendEvent`，说明涉及跨线程发送 Qt 事件。create02 的 `operations.txt` 已完整，after_save 数据存在，且新进程重开与独立几何/持久性验收通过，所以持久性结论为 PASS；但原始日志不是完全正常，也未在本课证明 ASSERT 原因已解决。root 后续重复运行及退出状态应独立补录，不删除或改写这次异常证据。

## 8. 产物索引

以 `$base=D:/001DIY/005lib/01AIEDA/learning/examples/lesson05_instances` 为根：

- `spec.json`：目标位置、角度、镜像、精度、源规格索引。
- `lesson05_instances.brd`：已保存的 BOARD。
- `scripts/lesson05.il`：`l5Create / l5Read / l5Dump`。
- `scripts/create.scr / read.scr`：原生入口脚本。
- `logs/create/`：初次返回类型处理错误，含 attempt01.il、before 三表、stdout/stderr、journal、launch、batch_drc。
- `logs/create02/before/`：变换前 `symbols.tsv / pins.tsv / children.tsv`。
- `logs/create02/after/`：变换后同三表。
- `logs/create02/after_save/`：保存并重新取 dbid 后同三表。
- `logs/create02/operations.txt`：逐项操作、保存和 COMPLETE。
- `logs/create02/launch.json / stderr.txt / stdout.txt / allegro.jrl / batch_drc.log / master.tag`：运行原始证据；不要因 stdout/journal 空而删除它们。
- `logs/reopen/symbols.tsv / pins.tsv / children.tsv`：独立只读重开导出。
- `logs/reopen/summary.txt / launch.json / allegro.jrl / stdout.txt / stderr.txt`：只读状态、哈希和退出证据。

独立复核原始临时目录（验证器已归档到examples/lesson05_instances/scripts/validate_lesson05.py，报告已归档validation.json）：`C:/Users/Administrator/AppData/Local/Temp/codex-lesson05-review-b641c0a2b5484e84932e44de7455b4fc/`：

- `validate_lesson05.py`：可复用标准库只读验证器。
- `report.json`：13,088 条断言结果、逐阶段计数、持久性比较、输入 SHA256、局限。
- `lesson05_instances_notes_20261018.md`：本文，已归档至learning/notes/lesson05_instances_20261018.md。
- `lesson06_native_operations_suggestion.il`：仅建议的下一课源代码；未在 Cadence 加载/执行，不计为已验证能力。

## 9. 复现与文件保护

只复核既有结果时，可以重新运行标准库验证器，报告放新的 temp 路径：

```powershell
& 'D:/001DIY/005lib/01AIEDA/learning/tools/python_3_14_0/python.exe' `
  '<验证器路径>/validate_lesson05.py' `
  --base 'D:/001DIY/005lib/01AIEDA/learning/examples/lesson05_instances' `
  --report '<新的临时目录>/report.json'
```

重新做原生创建实验时，先建立新的练习运行目录，仅复制 spec 和 scripts；不要把现有 BOARD 当作空板继续创建。修改 `.scr` 的绝对 base 路径并预建四个日志目录，确认目标 drawing basename 与脚本 guard 一致。保存目标只能是新目录里的练习板。已有脚本 `?noConfirm t` 会覆盖同名文件，因此复现必须使用新目录，不能直接重复旧 `create.scr`。保持公共 DRA/PSM/PAD 只读加载。

只读重开时保留 `-readonly`，运行前后计算 BOARD SHA256，检查 COMPLETE、实际导出、journal/退出和日志，不能只依赖进程结束或 DRC=0。

本课没有修改公共库、系统 HOME、全局启动文件，没有触发旧 bridge/flag，也没有操作历史示例板。新 mm/3 结果通过不能解释第3课 mil/0 中 bbox 与 vertices 的 0.5 mil 位置差；该疑点需在新空板中单独做精度、网格和 origin 实验。

## 10. 验收范围和下一课衔接

当前 TSV 只有铜层真实 polygon；mask/paste 验收为 `axlDBGetPad` 尺寸和面映射。path 只有 bbox、没有逐段端点/width，文字核对了属性与 bbox 变换、未渲染查看字形。不能宣称完整图形细节和生产输出已经验收。

第6课建议使用新练习板副本，验证事务 Start/Mark/Oops/Rollback/Commit、网格/可见性/findfilter 的显式保存恢复，以及 mm/3 坐标量化和 origin offset。其 API 官方来源为 `17dbtran.html`、`04parmgt.html`、`05selfnd.html`、`14dsnctl.html`；事务不能跨 Allegro 命令持有，保存/打开会取消事务，GridSet 不可 undo，应另行恢复。下一课源代码建议没有运行，不能记为课程已经完成。

## 11. 最终独立复现与本轮后续（2026-10-18）

在全新repeat子目录再次执行相同原生操作，可靠subprocess启动器记录创建PID17028、重开PID19252，两者正常exitCode0，无Qt ASSERT；12份原生TSV与原实验逐字节一致。readonly前后板SHA为A39169ED7D2C9A31CCFB93F2C1122826CCE212D56AB3E16F63566B941D5352EC。repeat/validation.json保存对比证据，原始create02 ASSERT仍保留，异常原因未推断。

已补 [读回预览](../examples/lesson05_instances/preview.png) 与绘图源码scripts/draw_preview.py，图中文字只显示锚点/方向。第6课实际执行的是另行审查修正后的lesson06_operations/scripts/lesson06.il，精确操作/回退子项通过，见[第6课笔记](lesson06_operations_20261018.md)；旧建议源码未执行与实际第6课结果分别记录。

本课声明范围已完成。当前层叠命名统一遵守[PCB层名规范](pcb_layer_naming.md)，后续双/四/六层不能另起GND/POWER/IN1等替代层名。
