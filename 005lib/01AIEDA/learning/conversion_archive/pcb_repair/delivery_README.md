# LGA1700：按原 AD 工程修复的 Cadence 工程

本目录是新的独立副本，原 AD 工程、`01sch`、`02pcb` 均未覆盖。原理图与原 AD 原理图比较，PCB 与原 AD PCB 比较；两项转换一致性验证均通过。

## 打开文件

- Capture 17.2：双击 `打开原理图修复工程.cmd`，或直接打开 `sch/LGA1700_AD_REF.opj`；设计文件为 `sch/LGA1700.DSN`。
- Allegro 17.2：双击 `打开PCB修复副本.cmd`，打开 `pcb/LGA1700_AD_PCB_repaired.brd`。启动器只给这个新进程设置本项目库路径。
- `libraries/psm` 是编译封装，`libraries/dra` 是可编辑封装源文件，`libraries/pad` 是焊盘库，`libraries/devices` 是本项目器件定义。
- `sch/netlist` 是从此交付 DSN 原生导出的 Allegro PST 网表；不要直接用它对已有 PCB 做整板 ECO，原因见下文。

启动器中 Cadence 安装位置为 `C:\Program0\Cadence\SPB172`。复制到另一台电脑时，可修改启动器中的 CDSROOT；保持目录结构，库路径随启动器所在目录定位。直接打开 BRD 时，也可在 Allegro 的 Setup → User Preferences → Paths → Library 中，给 psmpath/padpath/devpath 添加本项目相应目录。

## 已修复并验证

原理图保留 35 页、1131 个符号实例和 6608 个引脚。恢复 1147 个跨页连接器，校正 496 个接地符号热点与 493 条源导线端点，恢复 16 个 DIMMA1 DQS 零长度源连线的电气连接。19 个局部标签采用带作用域的名称，保留原名和来源追溯，避免同名局部标签被 Cadence 误合并。GNDA 按 Altium 18 原生编译结果保持 8 个引脚同网。

最终 PST 与 Altium 18 原生编译结果逐脚比较：6608 个引脚无缺失、无额外；1867 个非空网络分区完全一致，网络拆分 0、误合并 0，2,145,791 对同网引脚关系全部保持。部分自动网名和局部限定名不同，不影响连接关系。原生网表导出返回 0、错误 0。

所有元件值、封装、位置、旋转/镜像，以及引脚编号、名称、位置和 NC 状态均经原生读回检查。XML 重建将 USB_PN6 的两条相邻共线段合为一条，与原 AD 连续线段等价，最终为 8628 个 wire 对象。Q39 封装名已与本地 PCB 对齐；R4/R5 所需 R0402_PP_2 已由现有同族封装生成别名。

PCB 在现有 F_USB3 封装上恢复逻辑元件关联和原 AD 的 8 个焊盘网络，没有重复放置、移动、增删焊盘。保存重开后：1066 个元件、1066 个封装、6521 个焊盘、1103 个网络；原 AD PCB 的全部 6521 个焊盘身份及网络保持一致。82408 条显式几何及动态铜皮用户边界记录不变。Allegro 自动重算了局部动态填铜几何，详见 `verification/pcb/验证说明.md`。

## 原 AD 的原理图与 PCB 尚有差异

以下差异在原资料中已经存在，本次没有自行决定电路改版：

- 原理图的 31 个电阻位号在 PCB 逻辑元件中不存在。
- 6 个安装孔原理图各 16 脚，原 PCB 各只有 4 个实际焊盘；部分原始脚号还存在重复或不同编号。
- F_USB1/F_USB3 的原理图有供电脚 2，原 PCB 没有焊盘 2；PCB 的焊盘 9 原本未连接，保持未连接。
- 部分 PCIe、DIMM、PCH 等存在额外 NC 脚或重复编号；原理图局部同名网络与原 PCB 的网络归并也需设计者确认。

因此，这套文件解决了已证实的转换损失和库路径/封装名称问题，**不表示原始 Sch 与 PCB 已经可以无差异前向更新**。后续整板导入需先确定上述设计差异的最终意图，再修改引脚定义/补元件/重导网表；不能把未连接焊盘 9 直接改为供电脚 2。

本次验证范围是转换一致性。Altium 原工程原生编译报告有 12003 条尚未分类的诊断；Allegro 原有 8 个过期动态 shape 仍为 8 个。本目录未作全板 ERC/DRC 和生产签核，不宜据此直接下单。

## 重新导出网表与归档

1. 在 Capture 选中工程的 DSN，执行 Tools → Create Netlist → PCB Editor；输出目录选择新的目录，配置使用 `sch/allegro.cfg`，封装字段使用 `PCB Footprint`。
2. 保持自定义 `Device` 冲突修复；原 AD Device 信息存为 `AD_DEVICE`。外部 OLB 已独立清理 215 个 part 的 Device 属性，其他库数据保持不变。Q39 的外部库 part 被 27 个位号共用，库默认封装未改；Q39 的正确封装在本 DSN 实例中覆盖。不要批量 Update Cache 覆盖实例属性；确需更新时，先备份并复核封装、Device 和连接。
3. 检查网表日志后再做 PCB 导入。现阶段保留上述源设计差异，不能把“生成网表成功”当作“整板 ECO 已成功”。
4. 工程归档应包含本目录的 OPJ、DSN、OLB、BRD、libraries、pcbenv、PST 和验证报告。目录旁的 ZIP 为同一交付快照。

主要证据位于 `verification`。全部脚本、原生运行日志及未采用试验保留在：

最终交付 DSN 的 SHA256 为 `81924DF03109CC8D2222B3558CE0C6B18EF56CBDB078CE522F36632D113BE268`；PCB 为 `1D0760CFCE9CDA2A2AADC6891A4D434E5703424FF4F4C841383BC78586866D25`。XML 重建报告中的 BC541…AC38F 是最后一次 PST 导出前的快照；原生导出更新了文件元数据，随后对实际交付文件再次进行 10 张完整语义/几何/追溯表和 AD 网络验收，均通过。以 `verification/final_dsn_readback/final_verification.json` 及 `文件校验.csv` 为当前文件依据。

完整工作目录：

`D:\001DIY\005lib\01AIEDA\learning\staging\lga1700_pcb_repair_20261023`

完整过程已追加到上一级 `转换记录.md`。旧 `03repair_review_20261023` 是此前仅修名称/库路径的历史快照，本目录为本轮使用入口。
