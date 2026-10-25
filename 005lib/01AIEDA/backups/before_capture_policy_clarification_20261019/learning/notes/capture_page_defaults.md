# Capture 原理图默认 A4 与页面验收规范

用户于 2026-10-19 指定：自行创建的 Capture 原理图默认使用 **A4**。采用横向 **297 × 210 mm**，保持常用引脚间距 **0.100 inch = 2.54 mm**。内容放不下时按功能拆页，不能只放大图纸或把整图缩到文字难以辨认。学习文件、备份、脚本和预览均保存在 01AIEDA。

## 创建与检查

1. 新建每一页后调用 [capture_page_defaults.tcl](../scripts/capture_page_defaults.tcl) 的 `::CapturePageDefaults::apply`。这是后续 AI 创建页面的默认规范。
2. 在 Schematic Page Properties 中核对单位 Millimeters、尺寸 A4、宽 297 mm、高 210 mm；不能把 ANSI A 当成 A4，也不能只改尺寸名称。
3. 检查所有页面的元件、引脚、线、网络名、位号、值和跨页符号。留出页边、标题和页码区域；按功能组织内容，溢出时拆页。
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

旧脚本的无排版方案路径现会在创建文件前拒绝执行，要求显式 A4 坐标和边界检查，防止继续生成小纸张或溢出页面。历史工程与历史网表/ECO证据保留，不能把它们原先通过的连接验收解释成版面验收。

## 本地官方依据

- `C:/Program0/Cadence/spb172/doc/cap_ug/Setting_up_the_Design_Template.html`：英寸对应 A–E，毫米对应 A4–A0。
- `C:/Program0/Cadence/spb172/tools/capture/tclscripts/capCustomSamples/capCustomTitleBlockPageUtil.tcl` 第110行：`210000 × 297000` 为旋转 A4。
- 同目录 `capCustomizePage.tcl` 第168及227行：物理用户单位与绘图单位的转换，以及原生宽高除1000。
- `capAlignObject/capObjectAlignment.tcl` 第2204行：用 `GetDocUnits 1` 核对页面可绘范围。
- [922页官方 API 提取文本](../staging/capture_C_20261019/capture_api_reference.txt)：第400—402、416—418页中的页面尺寸和物理单位接口；第544、569—570页中的局部与偏移热点接口。
