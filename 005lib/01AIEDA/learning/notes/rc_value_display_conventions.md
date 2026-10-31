# R/C 的 Value 与画布显示统一

空贴标记的工程迁移与门禁见 [NC_ 前缀、独立装配状态及 PCB 文本验收](population_nc_prefix_workflow.md)。非 R/C 的模型 Value 与描述性 User_Value 可有不同语义，应分别保留，不能将本节的 R/C 一致性要求无条件推广到全部器件。

这套约定用于明确要求统一 R/C 显示的工程。先确定当前正式基线，再读取实际字段与来源；工程数据、策略、候选和验收记录放 `<工程根>`。它不改变原用户符号库，也不根据例子替换物料。

## 显示格式

| 类型 | 格式 | 明确输入后的示例 |
| --- | --- | --- |
| 电容 | `电容量/封装/额定电压/精度` | `100nF/0402/25V/10%`、`10uF/0805/25V/10%`、`4.7uF/0603/25V/10%` |
| 电阻 | `阻值/封装/精度` | `100R/0402/1%`、`100K/0603/1%`、`100M/0805/1%` |
| 明确空贴的 R/C | 在上述完整格式前加 `NC_` | `NC_100R/0402/1%`、`NC_100nF/0402/25V/10%` |

这里 `NC_` 是用户定义的“不装／空贴”显示标识。源资料中的独立 `NI` 空贴状态统一为此前缀；它不是电气引脚 No Connect，也不等同于排除 BOM 或禁止转换到 PCB。绝不据此前缀改引脚 NC、网络、`BOM_IGNORE`、`ConvertToPCB` 或 `PSpiceOnly`；这些原有状态分别保留，不能因为加了前缀就从网表删除器件或断开网络。空贴标记不替代实值：只有 `NI` 而无可核实阻值／电容量时仍需复核，不能编成 `0R`，也不由通用 formatter 自选 `TBD` 或 `NI` 占位值。若工程经用户确认允许占位显示，须作为工程专属例外另存计划和依据。

`25V`、`10%`、`1%` 都是示例或已明确选择的工程策略，不是通用工具的默认参数。用户明确要求某类全部按统一精度显示时，将该精度显式写入每条输入，另存原精度、策略来源和适用范围；不能把统一后的显示值称作原始物料规格，也不能自动更换 BOM、型号或采购参数。

本用户已明确默认目标：全部电阻统一为 `1%`，后续工程指令可覆盖这一偏好。生成工程输入时，应给每条 R 记录显式填写 `tolerance: "1%"`，并记录这是用户目标策略；通用 formatter 仍不为缺失字段补默认值。电容的额定电压和精度继续采用实际来源。

原始电阻精度、MPN 和来源证据须另存。源精度与 `1%` 目标不同的条目应列出并核对型号／BOM；统一显示不代表原物料规格已改变，也不能据此自动替换型号或声称已满足采购规格。

电容采用 ASCII `pF/nF/uF`，电阻采用 `R/K/M`；微符号 `µ/μ` 转 `u`，`Ω/ohm` 转相应阻值单位。`100mR` 是 0.1Ω，`100M` 是 100MΩ，大小写不可混用。`0R`、`4K7`、`4R7` 分别规范为 `0R`、`4.7K`、`4.7R`。`100m` 与旧式 `MF` 不猜含义，必须核实。裸数字电容编码、精度字母码及 MPN 不由本工具解码。

## 只从明确字段生成候选

工具：[normalize_rc_values.py](../scripts/normalize_rc_values.py)。它只读 JSON，只新建 JSON 候选，不打开 DSN/OLB，不修改原库，不覆盖已有输出。

输入可以是记录列表，也可以是带 `records` 列表的对象。每条记录需要 `ref`、显式 `family`（R/C）、`raw_value`、字符串 `package`、`tolerance`；电容还需要 `rated_voltage`。其他字段完整保留在输出 `metadata` 中，顶层其他字段保留在 `input_metadata` 中。

```json
{
  "records": [
    {
      "ref": "R_EXAMPLE",
      "family": "R",
      "raw_value": "4K7",
      "package": "0402",
      "tolerance": "1%",
      "source_tolerance": "0.1%",
      "display_policy": {"basis": "Explicit user selection", "tolerance": "1%"}
    },
    {
      "ref": "C_EXAMPLE",
      "family": "C",
      "raw_value": "100nF",
      "package": "0402",
      "rated_voltage": "25V",
      "tolerance": "10%"
    }
  ]
}
```

`raw_value` 宜只含阻值或电容量，完整旧串另存 `source_raw_value`。也接受精确的本类斜线格式，但其中参数与显式字段冲突时停止生成，不能默默以新值覆盖来源。

空贴必须来自明确装配输入。工具支持 `assembly_state` 或 `population` 中完整的 `NI`、`DNP`、`DNI`、`NOT_INSTALLED`、`NOT_FITTED`、`DO_NOT_POPULATE`、`DO_NOT_INSTALL`、`空贴`、`不装`、`不贴`；也支持语义明确的 JSON 布尔字段 `dnp`。对应已装状态是 `POPULATED`、`FITTED`、`INSTALLED`、`ASSEMBLED` 或 `dnp:false`。空字段不产生装配推断；未识别的显式状态及已装／空贴冲突停止生成。

输入已是完整 `NC_100R/0402/1%` 时识别此前缀并输出一次大写 `NC_`；末尾独立 `/NI`、`/DNP` 或 `/DNI` 也作为明确空贴证据，例如带外部封装／精度字段的 `100R/NI`，或完整的 `100nF/0402/25V/10%/NI`。仅有 `NI`、`DNP`、`DNI` 没有实值时输出 `REVIEW_NEEDED`。其他标记位置或未解析的复合串不自动清理。

不扫描封装、MPN、位号、`source_raw_value`、Description 或其他历史 metadata 中的 `NI` 子串来决定空贴；如源装配信息保存在这些字段，调用方须先核实语义并显式填入上述装配字段，同时保留源字段、原文和判定依据。例如 Description 内的独立 NI 可经人工／源资料核实后作为装配证据，但不是任意包含字母 NI 的字符串都有效。这样可避免把 `MINI_0402` 等正常封装名称误判为空贴。输出 `assembly_evidence` 记录采用的原字段／标记，`normalized_fields.assembly_state` 区分 DNP、POPULATED、UNSPECIFIED；没有证据时无前缀只表示未指定空贴，不是已装认证。原输入 metadata 始终完整保留。

字符串额定电压必须带 `V`；数字额定电压的单位明确约定为 V。字符串精度必须是对称百分比；数字精度按百分数的数值解释：`0.1` 表示 `0.1%`，不表示 `10%`。封装必须保留前导零，不能用数字 402 代替字符串 `0402`。同类 `R0402/C0402` 可剥前缀；前缀与器件类型矛盾时需要证据支持的独立封装字段，不能按位号猜。

```text
python normalize_rc_values.py --input <工程根>/rc_input.json --output <工程根>/rc_candidates.json --fail-on-review
```

没有参数时不选工程；输入输出都必须显式指定。工具保留输入 SHA，并在写候选前再次核输入字节。`READY` 只表示本条字段完整、格式可解析且没有冲突，不代表物料选型、额定电压降额或制造通过。

缺值、`TBD`、单位不明、混型、字段冲突或重复物理位号输出 `REVIEW_NEEDED`，`candidate_value=null`，并列出 `missing_fields` 与原因。不能用示例补值，也不把 `TBD` 伪装成精度。普通退出 0 只表示报告成功生成；使用 `--fail-on-review` 时有待核条目返回 2，输入或文件错误返回 1。

## 写入 Capture 前后分别验收

1. 在正式基线副本中逐位号绑定输入与候选，明确区分当前有效属性、源资料与用户显示策略；不从空值推断额定参数。
2. 对本节明确要求标准化的 R/C，精确修改请求范围的 `Value` 与实际画布使用的 `User_Value`，使其符合约定并一致。非 R/C 的模型 Value 与描述性 User_Value 原本可能不同；若仅统一空贴前缀，应分别处理各自原串，不强行复制成同一值。检查真实 DP 显示串与显示模式，不能仅因属性表有值就宣称画布已同步。
3. 保留原始 Value、User_Value、型号、封装、源精度／电压及依据记录；保持 Reference、脚号、网络与源用户库不变。更新 Value 会使器件网表定义发生预期变化，必须使用预先确定的逐位号 before/after 计划验收，不能要求所有 PST 字节不变，也不能据实际失败反向扩大白名单。
4. 原生保存后独立重开，复核 Value/User_Value 与实际显示串、完整有效属性、逐物理引脚网络分区及器件定义的有界变化。较长文字重新检查 Ref/Value／网络／引脚与本体间干涉；几何模型与 GUI 像素验收分别记录。
5. 只有实际需要更新 PCB 时再对最新板副本导入已验网表，并核板级物料属性、规则与物理铜。生成网表成功不等于导入已通过。

配合[自建库优先与模板共享](capture_user_library_first_templates.md)、[文字几何与可读性](capture_text_geometry_and_readability.md)、[网表生成与导入排错](capture_allegro_netlist_troubleshooting.md)使用。

## 工具验证范围

[合成检查工具](../scripts/selftest_normalize_rc_values.py)只使用小型虚构输入，覆盖目标格式、毫欧与兆欧、嵌入小数、微法符号、缺值、混型、冲突、重复位号、源 metadata 保留、显式显示策略、NC_ 前缀与严格装配状态来源、纯 NI 缺实值、MPN／封装子串反例及 CLI 防覆盖。检查报告保存在学习侧工具检查目录；没有运行 Cadence，不能作为具体工程的原生验收。


<a id="pcb-value-text-owner-audit"></a>
## Value 导入 PCB 后的文本与包围框验收

原理图 `Value` 的预期修改可能在 Allegro 逻辑导入后同步到已有 `COMPONENT VALUE/SILKSCREEN_TOP`、`SILKSCREEN_BOTTOM` 等器件值文本。字符串变长时，即使锚点、字体块、方向、镜像和对齐不变，文本几何包围框也可能改变。保留原始严格几何比较的 FAIL、完整差异与输入身份；不能笼统忽略所有 text 或 bBox，也不能把这类 FAIL 直接当作布线变化。

配套只读定义：[allegro_value_text_owner_readonly.il](../scripts/allegro_value_text_owner_readonly.il)。文件没有自动执行入口，不载入或保存板；由独立运行器在只读打开的板中加载定义，调用 `rcTextAudit(outDir)`，再无保存退出。输出目录须由运行器预先创建。运行器同时检查原生退出状态、`COMPLETE.txt` 及输入板前后 SHA；定义文件自身的零保存调用声明不能代替外部文件保护。

验收时先准备来自原理图/PST 的逐位号 Value before/after 计划，再对导入前、保存后及独立重开的板执行相同审计：

1. 通过 `design.symbols -> symbol.children -> text.parent` 取得真实所有者和 `symbol.refdes`，检查 text 的 parent 确为该 symbol。保留每个文本对象和重复次数，不按坐标接近、字符串相等或最近器件猜位号。DBID 只用于当前打开数据库内的身份追踪，跨进程不假定 DBID 相同。
2. 将每个真实 owner 下的文本逐对象绑定到原几何导出的完整 25 列记录。只允许该位号预先计划的字符串转换，并逐项锁定 layer、xy、font、textBlock、justify、rotation、mirror、其余对象属性与多重性；完整保留所有 TextBlock 参数，包括 width、height、charSpace、lineSpace、photoWidth 和原生附加字段。未声明的位号、层、姿态、字体或重复数变化一律拒绝。
3. 对每个允许变字的对象保存实际 before/after bBox，并读取 `axlDBGetExtents(text nil)` 作完整对象 extent 台账。它是官方支持的现有 TEXT 对象只读查询，不是从任意新字符串计算包络的接口。包围框变化必须有具体对象、实际数值和不变参数证据；不能通过全局删列获得 PASS。若另用字符宽度公式验证，限定实际字体/字符/方向的已检验范围，不将单个样例拟合当成通用算法。
4. `component_value` 列可能为 nil，属性缺失也不等于空字符串或逻辑值未变。该列及原始 component/symbol 属性只作辅助记录；逻辑 Value 以已验证的 PST、CFX 与预先声明的逐位号计划核对。文本显示和逻辑值分别验收。
5. 独立检查铜、引脚、焊盘、放置、网络连通分区和规则。特定 Value 文本的有界放行不能放宽这些域，也不代表 DRC 或制造已通过。只有精确替换全部已批准文本记录后，剩余完整几何多重集仍相同，才能给出对应的有界几何结论。

本机官方依据可在当前安装的 `doc/algroskill/02dbdesc.html` 中查 Symbol Attributes、Text Attributes、Textblock Parameter Attributes 与 figure bBox 定义；`doc/algroskill/14dsnctl.html` 的 `axlDBGetExtents` 明确支持 TEXT，第二参数 nil 读取完整对象范围。原生逐对象审计结果与案例数据保存在工程目录，学习库仅保留定义和上述方法。
