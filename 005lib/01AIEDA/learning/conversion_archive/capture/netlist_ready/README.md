# LGA1700 OrCAD Capture 工程

2026-10-23，Cadence 17.2。打开 `LGA1700_CAPTURE.opj` 使用完整工程，或直接打开 `LGA1700.DSN` 查看原理图。

本目录包含原理图 DSN、符号库 ORCAD_LIBRARY.OLB、工程 OPJ 和 netlist 目录中的三份 Allegro 网表。工程引用均为相对路径，复制整个目录后保持文件之间的位置即可。

## 已完成检查

原生数据库保存重开成功，包含 35 页、1131 个符号实例、1097 个唯一位号和 6608 个物理引脚。与 AD 源文件逐页数量、全部位号和每个物理引脚编号集合对照，均无缺失或新增。

PST 原生网表器返回码为 0，生成 pstchip.dat、pstxprt.dat、pstxnet.dat。导网表兼容修正前后，页面统计、元件位置/值/封装及逐引脚网络记录完全一致。复核数据位于 verification 目录。

## 转换兼容处理

转换时临时设置 Capture 进程的 CDSROOT 为 C:/Program0/cadence/SPB172，使转换器找到 CAPSYM.OLB。未修改系统环境变量。

AD 的自定义 Device 属性会被 Capture 网表器解释为强制器件定义名称，引发 ORCAP-36001 冲突。本 DSN 的实例和内部符号缓存已将该属性原值保存为 AD_DEVICE，并移除冲突的 Device 属性。Source Part、Source Package、位号、引脚、原理图几何和 PCB Footprint 保留；逐项改动见 verification/device_changes.tsv。原始转换 DSN 另行保留，没有被覆盖。

## 再次生成网表

在 Capture 保存设计，在工程管理器选中 LGA1700.DSN，使用 Tools > Create Netlist > PCB Editor，选择 Create PCB Editor Netlist，输出到 netlist，封装属性使用 PCB Footprint。原生导出使用的 allegro.cfg 已放在本目录。

## 复核范围

本次确认了文件可由原生数据库读取、结构与物理引脚覆盖、属性修正不改变转换后的连接记录，以及 PST 成功生成。AD 到 Capture 的完整连接拓扑等价、页面图形排版和 GUI ERC 仍需复核；OPJ 采用本机官方示例格式，相对引用已检查。

原目录 ASCII PCB 比原理图少 31 个电阻位号，版本/装配差异尚未确定。向现有 Allegro 板导入前，需要在 BRD 副本中检查封装库、位号、引脚网络和自动网名映射。本包没有更新现有 PCB，也没有包含经认证的 Allegro PSM/PAD 封装库。
