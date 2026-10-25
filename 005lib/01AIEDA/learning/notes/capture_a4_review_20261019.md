# D和E原理图逐页检查与 A4 排版修订记录

2026-10-19，Asia/Shanghai。用户指出 DE_INTEGRATED_BASELINE.DSN 页面过小，并要求再次检查所有页面。本次检查范围为该设计 TOP 下的全部六个模块；按电路功能重排为 **12 张横向 A4**，80 件器件、272 个物理引脚、69 个网络及 6 个 NC 保持一致。

**同日后续规范更正：** 用户明确 A4 只是起始尺寸，内容放不下可以扩大；普通 MCU 优先单单元放全引脚，CPU 等复杂器件再按功能需要分单元。十二页 A4 保留为当时的排版方案，不是未来设计的纸幅上限或强制拆页模板。原 A1 纸张本身不构成错误，应以实际内容、布局和可读性判断。此规则替代此前“只能拆页、不能扩大”的解释，详见 [纸张规范](capture_page_defaults.md) 和 [符号单元规范](capture_symbol_defaults.md)。本轮规范更正未重建既有 DSN/OLB；U1 原本就在 MCU_CORE 单单元中包含完整 48 脚，外围 MCU_SUPPLY 页面不是 U1 的另一单元。

**当前查看入口：[DE_INTEGRATED_A4.opj](../examples/de_15_26_20261019/a4_review/native/DE_INTEGRATED_A4.opj)**，对应 [DE_INTEGRATED_A4.DSN](../examples/de_15_26_20261019/a4_review/native/DE_INTEGRATED_A4.DSN)。当前用户打开的原 BASELINE 文件保留，未从外部覆盖。新工程在 `a4_review` 下，不能继续打开旧文件来判断本次修改。

## 原六页的实际情况

从用户已保存文件复制只读快照，SHA256 为 `577078ff88dbbae2a55f3184942e0cfa92598a5b526b7f43637e73fd27cd6d6d`。本次结束时原文件与快照仍逐字节一致。快照保存在 [baseline_snapshot.dsn](../staging/a4_review_20261019/baseline_snapshot.dsn)，读回证据见 [before_pages.tsv](../staging/a4_review_20261019/before_pages.tsv)。

| 原页面 | 器件数 | 复查时实际纸张 | 原排版问题 |
| --- | ---: | --- | --- |
| ADC_GPIO | 6 | A1，841 × 594 mm | 元件单列，跨页端口另排一列；按最新规范，是否采用 A1 应依内容和可读性判断 |
| CLOCK_RESET | 12 | A1，841 × 594 mm | 元件纵向延伸，复位、启动、下载和晶振未合理分组 |
| INTERFACES | 13 | Custom，3.3 × 2.2 inch | 内容越界，UART/I²C/SPI 混排 |
| MCU_SUPPLY | 10 | Custom，3.3 × 2.2 inch | MCU 与去耦混排，41 个跨页端口集中列出，超出 A4 范围 |
| POWER | 17 | Custom，3.3 × 2.2 inch | 入口、开关电源和 LDO 按器件清单堆叠，超出纸张 |
| USB_CAN | 22 | Custom，3.3 × 2.2 inch | USB、检测、上拉控制及 CAN 混排，超出纸张 |

创建脚本误把原生宽高 `3300/2200` 当成绘图坐标范围；它们在英制下实际是 3.3/2.2 inch。原验收只检查连接和后端，没有验收纸张与显示，这是本次纠正的问题。

## 十二页的最终分组

全部页面读回均为 **A4，297 × 210 mm，metric=1，PinToPin=2.54 mm**；绘图范围读回 1169 × 826，正文保留边距，标题和页码单列。源模块名保存在 SOURCE_MODULE_PAGE 属性中。

| 新页面 | 件数 | 主要内容及检查重点 |
| --- | ---: | --- |
| ADC_GPIO | 6 | J10—13、R32、C24；GPIO 分组及 ADC 输入滤波，逐针核对网络名 |
| RESET_BOOT | 7 | R27—30、C21、J7—8；复位和 BOOT 条件分组 |
| CLOCK_DEBUG | 5 | J9、Y1、R31、C22—23；SWD 接口及晶振网络 |
| UART_I2C | 7 | J4—5、R16—20；UART 串阻、上拉与 I²C 上拉 |
| SPI | 6 | J6、R21—25；四路 SPI、片选上拉和可选连接 |
| MCU_CORE | 1 | U1 全部 48 脚；跨页端口直接接在线端，不再使用独立长列表 |
| MCU_SUPPLY | 9 | C13—20、R26；数字供电、模拟供电及储能/去耦 |
| POWER_INPUT_LDO | 9 | J1、F1、D1、C1—3、U3、C8—9；入口保护及 3.3V 稳压 |
| POWER_BUCK | 8 | U2、C4—7、L1、R1—2；降压与反馈网络 |
| USB_PORT | 7 | J2、U4、R3—6、C10；USB-C、CC、ESD 和数据串阻 |
| USB_SENSE_ATTACH | 7 | Q1—2、R7—11；VBUS 检测与受控上拉 |
| CAN | 8 | U5、J3、C11—12、R12—15；CAN 收发器、互斥连接和终端 |
| 合计 | **80** | **272 pin，69 net，266 已连接，6 NC** |

## 实际修改

- 新建独立 A4 设计和 OLB，保留位号、值、MPN、装配状态、要求、封装和原电气引脚定义。
- 根据实际页面重算跨页网络，创建 **113 个真实跨页端口**，每个热点落在对应网络导线端点；同页其他引脚继续使用网络别名。
- 端口名称保留可见的 Name 属性。按名称长度调整右侧文字位置，给 VBUS_PRESENT_N、USB_ATTACH_N 等长名称留出箭头间距。
- 添加页面标题、A4 尺寸、修订号及页码。元件位置按显式坐标规划，不再以“纸张 mil 数值”当作绘图宽高。
- [共享 A4 默认函数](../scripts/capture_page_defaults.tcl) 和 [D/E 创建器](../scripts/de_capture_helpers.tcl) 已修正。旧的无排版输入在创建输出前拒绝执行；新流程使用 [显式 A4 方案](../staging/a4_review_20261019/a4_spec.json)。

## 验收与可追溯证据

| 验收 | 结果和证据 |
| --- | --- |
| 保存后新进程重开 | 12 页全部 A4；[after_pages.tsv](../staging/a4_review_20261019/after_pages.tsv) |
| 元件、引脚及连接 | 原生读回 80 件/272 pin/69 net/6 NC；[实例](../staging/a4_review_20261019/after_instances.tsv)、[逐针连接](../staging/a4_review_20261019/after_pins.tsv) |
| 页面几何与端口 | **9375 项通过，0 失败**；包含纸内边界、保守文字范围、模块间距、绝对引脚热点及跨页端口在线端；[validation.json](../staging/a4_review_20261019/validation.json) |
| 真实 Capture→PST 导出 | Cadence `pstswp.exe -pst` 退出 0；[实际网表](../staging/a4_review_20261019/packaging/netlist)、[进程记录](../staging/a4_review_20261019/packaging_verified_process/launch.json) |
| 独立 PST 比较 | **718 项通过，0 失败**；80 件值/封装、272 物理针及网络、69 net/6 NC 全匹配；与原用户保存快照的电气变更为 0；[pst_compare.json](../staging/a4_review_20261019/pst_compare.json) |
| 输入身份和原文件保护 | 打包前工作副本与最终 A4 DSN 同 SHA；打包后源 A4 DSN 不变，用户原 BASELINE 也不变；[输入身份](../staging/a4_review_20261019/pst_input_identity.json) |
| 全部页面辅助视觉检查 | 已查看 12 张独立读回示意图及总览，复核页边、元件间距、长名称、引脚编号与 NC；[总览图](../examples/de_15_26_20261019/a4_review/preview/contact_sheet.png)、[各页 PNG/SVG](../examples/de_15_26_20261019/a4_review/preview) |

预览使用真实实例位置、线段、绝对引脚热点和端口名称显示锚点；它是**数据库读回示意，不是 Capture 截图**。原生无显示会话中 80 个实例的图形边界缓存为零，未将零边界当作通过依据，而是用未旋转原模型、绝对引脚热点、线段和文字保守估算补验。字体、字形边界和端口轮廓仍有近似；**Capture 界面逐页显示、打印预览和完整 ERC 尚待复核**。当前两脚器件仍沿用矩形教学符号，电路流向的正式制图审查继续保留，不能称作生产图纸。

本次十二页真实 PST 导出通过，不改写旧六页失败日志，也没有把新图自动套用旧 BRD/ECO 的 1578 项历史结论。既有 PCB 导入/ECO 证据继续属于原单页设计；本次没有重新导入 PCB 或验证 GUI 反标。

## 学到并修正的方法

1. **页面物理尺寸和绘图坐标分开。** 页面宽高为用户单位 ×1000；从 `GetDocUnits 1` 获取实际可绘范围，保存重开确认。
2. **热点区分局部和绝对。** `GetHotSpot` 是局部；读回验收用 `GetOffsetHotSpot`，放置位置按目标端点减去局部热点计算。初轮误多加端点导致端口断开，未作为交付；修正后全针及真实 PST 都通过。
3. **读取真实库名。** 本机 capsym 的左右文字样式实际为 OFFPAGELEFT-L 和 OFFPAGELEFT-R。初轮不存在的名称在 NULL 检查处正常退出，没有继续调用空对象。
4. **显示属性也要验收。** 逐页检查 Name 显示类型、位置和长名称，不能只检查对象存在或连通。
5. **PST 打包使用工作副本。** 本次证实工具会更新工作 DSN，故记录打包前的 SHA 和打包后源文件不变；不能错误要求工作副本导出后仍逐字节不变。
6. **测试连接与验收版面分开记录。** 图纸大小、内容完整、阅读顺序、文字可见与电气一致分别给出证据。

失败尝试、修改前 A4 副本和原始进程日志均留在 [本次 staging](../staging/a4_review_20261019)。修改前文档和旧创建器保存在 `01AIEDA/backups/before_A4_review_20261019`。学习规范已经同步到 [EDA.md](../../EDA.md)、[课程索引](../../课程索引.md) 和 [长期 A4 规范](capture_page_defaults.md)。

## 继续工作的入口

当前看图使用上方 A4 工程，源生成流程依次为 `capture_a4_prepare.py` → `capture_a4_create.tcl` → `capture_a4_titles.tcl` → 原生重开与 `capture_a4_validate.py` → `capture_a4_export.py` → `capture_a4_pst_compare.py`。创建阶段拒绝覆盖现有设计；历史脚本和修复脚本不应无检查地全部重放。

接下来先在 Capture 17.2 中确认既有十二页的真实显示、页码、打印边界和完整 ERC，再继续 PCB 布局主线。以后从 A4 起步，可按内容扩大纸张；普通 MCU 保持单单元全部引脚，CPU 等复杂器件按实际需要分单元。
