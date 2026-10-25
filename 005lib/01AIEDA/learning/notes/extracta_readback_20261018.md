# extracta 读取 BRD 方法记录（2026-10-18）

来源：用户从另一个PCB设计窗口提供的操作说明截图。本轮确认本机存在 C:/Program0/Cadence/SPB172/tools/bin/extracta.exe；截图所述调用和对应工程尚未在本课复跑。

有用方法：通过Cadence原生extracta读取.brd并按视图/字段模板导出网络与焊盘关系、器件坐标、线段/弧段、过孔、层信息、丝印及数据库保存的DRC/连接统计，作为布局布线核验的数据来源。后续可与Allegro SKILL读回和图形几何检查交叉核对。具体命令参数、模板字段和兼容版本仍应查本机官方帮助后实跑验收，不凭截图猜调用。

截图里的具体网络数、未连接数和DRC统计属于另一个窗口那次报告，需关联该板文件、模板及日志核实。当前只把它记录为方法来源，不用它更新本轮练习或用户硬件工程的通过状态。

表面PDF/丝印预览可用于查看外观；信号、电源、差分间距、换层回流、参考平面、EMI路径的审查需要实际铜、走线、过孔、层叠及设计意图。后续逐段检查保留来源与几何证据，避免把网络连通/已保存DRC直接当作完整PCB设计质量验收。

## 已查的本机官方入口

C:/Program0/Cadence/SPB172/doc/ecoms/echap.html，extracta条目（约6630行）给出：
`extracta [args] [drawing] [cmdfile] [outfile...]`。
官方说明必须提供cmdfile以取得设计的flattened视图信息，进一步视图/字段见Completing the Design User Guide。acoms/achap.html约10674行说明“!”是extracta字段分隔符，解析不能随意按空格拆；algrostart/chap3.html约1403行提醒某些报告单位配置来源，读取输出时应同时核单位。

本轮只核官方说明及本机程序存在，未把截图对应操作记为本轮已复现。下一次实际使用时保存命令文件、字段、单位、BRD哈希、输出日志，并和SKILL同对象读回交叉验证。
