# Capture 原理图纸张选择与页面验收规范

用户于 2026-10-19 进一步明确：**A4 是新建图纸的起始尺寸，不是纸幅上限。** 默认横向 297 × 210 mm；器件或连线在保持清晰、合理间距后放不下时，可以扩大到 A3、A2、A1 等合适纸张。保持常用引脚间距 0.100 inch = 2.54 mm；不以过小文字、拥挤排布或强行拆分一个普通 MCU 来迁就 A4。学习文件、备份、脚本和预览均保存在 01AIEDA。

**普通器件尤其普通 MCU，优先在一个逻辑单元内完整呈现全部引脚；CPU 等复杂器件才按实际需要分单元。** 详细规则见 [符号单元与引脚完整性规范](capture_symbol_defaults.md)。独立电路模块的分页面与同一器件的符号分单元是不同操作，分别判断。

## 创建与检查

1. 新建页从 A4 开始，先考虑完整器件符号、引脚分组及阅读顺序，再选择合适纸幅。[capture_page_defaults.tcl](../scripts/capture_page_defaults.tcl) 的 `::CapturePageDefaults::apply $page` 默认 A4；`::CapturePageDefaults::apply $page A3` 等可扩大。D/E 创建器可通过 `spec.page_sizes` 逐页指定尺寸，如 `MCU_CORE=A3`。
2. 在 Schematic Page Properties 中核对单位 Millimeters、选定纸张及实际宽高；A4 为 297 × 210 mm，A3 为 420 × 297 mm，依实际需要选择更大纸幅。不能把 ANSI A 当成 A4，也不能只改尺寸名称。
3. 检查所有页面的元件、引脚、线、网络名、位号、值和跨页符号。留出页边、标题和页码区域；保持清晰度，空间不足可扩大纸张或重新布局。不同功能电路可合理分页，但不能为保留 A4 而强行拆分普通 MCU 符号。
4. 用 Cadence 保存后在新进程重开，读回尺寸、单位、引脚间距及几何；重新排版后逐引脚比较网络，并用真实网表检查跨页连通。
5. 最后检查 Capture 中的实际文字显示与打印预览。数据库几何或辅助示意通过，不能代替这一步。

## 17.2 原生数据库单位

`SetPageSizeInfo` 的宽高是用户物理单位的 1000 倍；绘图 CPoint 使用另一套坐标，禁止直接相互比较。

```tcl
$page SetPageSizeInfo 297000 210000 2540 1
$page SetSizeName [DboTclHelper_sMakeCString A4]
set drawable [$page GetDocUnits 1]
```

本机重开读回：`metric=1`、`width=297000`、`height=210000`、`pinToPin=2540`、`docUnitsPerInch=100`，可绘范围 **1169 × 826** 绘图单位。通过 `GetDocUnits 1` 获取当前值，不把这组坐标硬套到其他间距或工程。

`GetHotSpot` 返回符号的局部热点；本次放置实例使用 `GetOffsetHotSpot` 得到页面绝对热点。放置跨页连接器时，实例位置 = 导线端点 − 局部热点，并标记修改后保存。不能多加一次导线端点坐标。

本机无图形显示会话中，新建实例的 `GetBoundingBox` 显示缓存为零；本次以符号模型、实例位置、绝对热点、真实导线、端口外形和保守文字估算补充核验，并在报告中保留此限制。不可将零边界作为“没有越界”的证据。

## 原问题与修订记录

原 DE_INTEGRATED_BASELINE.DSN 创建脚本错误地设置 `3300 × 2200`、英制，实际只有 **3.3 × 2.2 inch**。同时按器件清单堆叠，没有正确换算页面与绘图坐标；跨页连接器另列在左边，进一步拉长页面。用户反馈后，六模块重新分成 12 张 A4。详见 [逐页检查与修订记录](capture_a4_review_20261019.md)。

旧脚本的无排版方案路径现会在创建文件前拒绝执行，要求显式坐标和所选纸张的边界检查，防止继续生成溢出页面。共享函数和 D/E 创建器现支持逐页选择 A4/A3/A2/A1/A0；越界时应扩大纸张或调整布局。`capture_a4_*` 是此前十二页 A4 样例的专用脚本和验收，不代表后续工程必须全部 A4。历史工程与历史网表/ECO证据保留，不能把它们原先通过的连接验收解释成版面验收。

此前“放不下就必须拆页、不能放大”的表述已被本次明确规则取代；十二页 A4 是既有排版方案，不是统一模板要求。本次更新规范与创建器，未重建既有 DSN/OLB。

## 本地官方依据

- `C:/Program0/Cadence/spb172/doc/cap_ug/Setting_up_the_Design_Template.html`：英寸对应 A–E，毫米对应 A4–A0。
- `C:/Program0/Cadence/spb172/tools/capture/tclscripts/capCustomSamples/capCustomTitleBlockPageUtil.tcl` 第110行：`210000 × 297000` 为旋转 A4。
- 同目录 `capCustomizePage.tcl` 第168及227行：物理用户单位与绘图单位的转换，以及原生宽高除1000。
- `capAlignObject/capObjectAlignment.tcl` 第2204行：用 `GetDocUnits 1` 核对页面可绘范围。
- [922页官方 API 提取文本](../staging/capture_C_20261019/capture_api_reference.txt)：第400—402、416—418页中的页面尺寸和物理单位接口；第544、569—570页中的局部与偏移热点接口。
