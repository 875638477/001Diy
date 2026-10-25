
## 十六 2026-10-23：对接手动转换 PCB，库路径与封装名称修复

本节更新前文“转换成功”的适用范围：之前通过的是文件生成、结构覆盖和 Capture→PST 导出检查，**没有证明 AD→Capture 电气网络等价，也没有完成对已有 PCB 布线的安全更新**。本次检查发现了明确的转换连接缺陷，因此旧 DSN/PST 不能直接用于整板 ECO。

### 输入与用户确定的范围

用户将原理图复制至 `01sch`，PCB 自行转换至 `02pcb`。本次读取 `01sch/LGA1700.DSN`、`01sch/allegro`、`02pcb/lga1700_17x17.brd`、`02pcb/netrev.lst`，并检查本地 `psm`、`pad`。全程先建立快照，所有原生试验使用独立副本，不覆盖用户的 DSN、BRD 或公共库。

快照的 PCB 为 1065 个逻辑元件、1066 个封装符号、6485 个元件引脚记录、1103 个网络；原理图为 1097 个物理位号、1131 个符号实例、6608 个引脚。两边的数量本来就存在差异。

用户明确选择：**“先保留这些差异，只修库路径和封装名称”**。安装孔和 USB 排针等的引脚映射没有修改；跨页连接和接地修复实验也没有合入交付。

### 发现的路径与名称问题

旧环境的 PSMPATH/PADPATH 只覆盖公共库，未覆盖 `02pcb/psm` 和 `02pcb/pad`。

| 位号 | 原要求 | 本次处理 |
| --- | --- | --- |
| Q39 | `SOT-23-3_L2_9-W1_3-P1_90-LS2_4-BR`，本地不存在 | 修复副本采用 PCB 已使用的 `OT-23-3_L2_9-W1_3-P1_90-LS2_1`；旧值保存为 `AD_ORIGINAL_PCB_FOOTPRINT`。 |
| R4、R5 | `R0402_PP_2`，本地不存在 | 从现有 `r0402_pp.dra` 原生另存、编译同名别名。保留现有同族两脚几何，没有重新按实物资料进行封装选型。 |

Q39 原生审计通过：35 页、1131 个实例、6608 个引脚、8613 段导线保持一致；只有 Q39 的封装字段变化，原值追溯属性读回正确。

### 交付位置与实际测试

交付目录：[03repair_review_20261023](D:/001DIY/004computer/lga1700/03repair_review_20261023)。详细操作见[修复说明.md](D:/001DIY/004computer/lga1700/03repair_review_20261023/修复说明.md)。

- `sch_name_fix`：仅修正 Q39 名称的 DSN、OPJ、OLB。
- `library_fix`：新增 R0402_PP_2 的 DRA、PSM。
- `netlist`：从名称修复副本原生导出的 PST，导出返回 0；没有改写 PST 来掩盖差异。
- `pcbenv/env` 与 `打开PCB检查副本.cmd`：仅给新启动的 Allegro 进程配置本项目库路径，不改系统或正在运行窗口的设置。
- `pcb_review/LGA1700_LIBRARY_CHECK.brd`：未做 ECO 的 PCB 检查快照，SHA256 为 `139B6D456470B5F22A2656D7324B2BDC852C96205A6F6BCE047DCA921377820F`。
- `diagnostics`：引脚差异、原生验证及最终库环境测试日志。

最终直接使用交付目录的项目环境、原 `02pcb/psm`、`02pcb/pad` 和交付网表执行原生 `netrev -e -y 2`；缺失封装诊断 `SPMHNI-194` 为 **0**。输入和输出指定为不同文件，没有启用拆相连铜线或忽略 FIXED。

脚号差异按用户要求保留，因此最终返回 2，16 组器件/符号脚号不匹配，加停止项共 17 个错误，没有生成结果板。严格 `-e` 的统计口径与用户原来的 7 错误/28 警告不同，不能简单比较总数判断修复效果。最终日志：[netrev.lst](D:/001DIY/004computer/lga1700/03repair_review_20261023/diagnostics/final_library_test/netrev.lst)。

### 按要求保留的源设计差异

- MH1、MH2、MH3、MH4、MH5、MH7：原理图各 16 脚，原 AD PCB 及转换板各只有 4 个焊盘；部分实际编号为 4～7。不是所有焊盘都在转换时丢失。
- F_USB1、F_USB3：原理图电源脚 2 在原始 PCB 中没有对应焊盘；原 PCB 另有未连接的脚 9。没有将脚 9 直接改成供电脚 2。
- CN1～CN3 的多个接地焊盘、DIMM/PCH/PCIe 的额外未连接脚或不同编号，均没有强行合并或改号。
- F_USB3 的几何仍在 PCB，但该符号 `refdes=nil`、`component=nil`，九脚网络为空。用全部正常元件共同坐标平移及九脚位置证明身份，误差仅约 0.0008 mil。本次没有恢复关联或重新放置，防止重复。
- 原理图还有 31 个电阻位号没有出现在 PCB 的逻辑元件表中，本次未补放或删除。

### 额外发现：转换连线未保持等价

连接比较依据共同的位号/物理脚号和网络分区，而非仅比较网名。初始结果中，有 506 个 PCB 网络被 Capture 分成多个网络，498 组跨页。PCB 本身只是独立基线，差异不能单独证明原理图错误；以下项目另有源 ASCII 几何/语义证据：

1. 原 AD 项目为 Automatic/Flat 连接语义，无 Sheet Entry，1147 个 RECORD=18 Port 应按同名跨页连接。转换 DSN 却有 0 个 Port、0 个 Off-page，导致 SMB_CLK、RSMRST# 等跨页信号分裂。只剥除网名数字后缀或将所有 NetLabel 全局化，都不能正确解决。
2. 839 个电源对象中，496 个接地符号热点与源接点存在 10 个文档单位偏移。
3. USB32 GEN1 5G_REAR 的源 AD 导线 709 应映射为 `(606,824)→(606,844)`，转换后被延长到 `(606,854)`，碰到了 USB_PN6 数据线。数据线又被拆成两段，因此多出来的第 106 段不是应盲删的“桥”；完整只读诊断见交付 `diagnostics/usb_rear_exact_wire_diagnostics.json`。
4. DIMMA1 的 16 个 DQS 引脚对应源 AD 零长度导线，转换后没有建立 Capture 网络。引脚数量/坐标检查通过，并不代表这些脚已经正确连通。
5. GNDA 与 SIO_GNDA 的多名/作用域关系仍需源 AD 编译网表进一步确认，没有根据 PCB 单边结果强制合并。

隔离实验曾补回 Off-page 并对齐电源符号，分裂从 506 组降至 110 组，但仍有接线端选择、零长度导线和 USB 地线几何问题，验证未通过。另已准备第二版脚本，尚未执行；收到用户限定范围后停止该方向。**这些实验文件均留在 staging，不是交付工程。**

### 证据位置

本次完整工作根目录：

```text
D:\001DIY\005lib\01AIEDA\learning\staging\lga1700_pcb_repair_20261023
```

关键证据包括 `input_snapshot.json`、`native_current`、`native_backup`、`q39_fix_verification.json`、`required_vs_native_and_original_ad.json`、`topology_comparison.json`、`source_port_endpoints.tsv`、`source_semantics/scope_and_conversion_semantics.json`、`usb_rear_exact_wire_diagnostics.json`、`connection_fix_audit/verification.json`。连接修复实验的失败状态已明确保留，没有标记为完成。
