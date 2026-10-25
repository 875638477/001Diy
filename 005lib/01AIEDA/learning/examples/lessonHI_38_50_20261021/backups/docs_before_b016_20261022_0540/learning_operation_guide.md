# H/I 第38—50课操作与证据索引

记录日期：2026-10-22。全部路径相对于本目录，所有成果集中于01AIEDA。本轮是Cadence 17.2原生数据库实操；桌面控制连接失败，未完成的GUI捕捉/鼠标交互不能用API记录代替。当前尚未达到第45/50课完整板验收。

## 从哪里继续

先读[完整主笔记](../../notes/lessonHI_38_50_20261021.md)的最新日期段，再读[学习计划](learning_plan.md)、[MCU记录](../../notes/lessonHI_mcu_20261021.md)、[电源/接口记录](../../notes/lessonHI_power_20261021.md)。主笔记中的b003/b008/b012是历史阶段，不按其早期“当前”字样找最新板。

- 已验部分布线基线由 inventory/current_2L.json、current_4L.json 及各自不可变检查点确定；当前为USB_aux b014，仍剩45/46连接。
- 最新已存中间板 source b015 位于 native_candidates，文件名带 DRC_PENDING。两板各剩25连接/19网，cached14/20条真实违规待纠；整板重算未完成。详见[实际源报告](review/source_b015_native_report.json)、[进度记录](review/progress_record_20261022_0445.json)。
- plans 与 engineering_*/ 中尚未执行的候选不能当作实际铜；batches、source/batch_snapshots和logs保留具体输入与执行证据。回放旧批必须使用它声明的源SHA，不可直接对“最新板”重放。
- native_work 是每次新生成的工作副本，native/native_candidates 是不可覆盖的阶段文件。原G板、公共库、01env和真实USB工程不改。

## 软件内实操顺序

### 1. 建立真实输入

读Cross Section并核层名TOP-BOTTOM或TOP-L2-L3-BOTTOM，再核15/17个Film的层与options。01env/drill*.txt是光绘模板内容，不能把Film名称当物理层；没有实际内层铜就不能说四层已有平面。检查80逻辑器件、272编号pad、266带网终端、6NC、69网及独立机械孔。读取真实pin net，padBBox已旋转，不能再旋转一次。

复现输入在 inventory/checkpoints/*/normalized.json、networks.json、base_net_rules.json；同一次读取对应的原始目录记在readbackDirectory。几何搜索只是辅助，导出网表或图形提取不能代替Allegro中的实际物理连接验证。

### 2. 分段建线、via与拆线

实际封装pin中心作为起止锚点，points明确每个转角，width/widths明确每一段。现有[hiRoute/hiVia封装](scripts/batchHI.il)调用已验证原生建线和axlDBCreateVia；不直接复用未知板的DBID。建成后核实际net、层、端点、线宽、via铜盘及原生连接图。

拆线先以net+layer+width+两端点唯一定位；数量不是1就停止。多段联合拆除使用[精确批次事务](scripts/batchHI_exact_ripup_v2.il)，先解析全部对象再删除，避免逐段删除后原生改归网络造成误删。不要删除整net来替代局部重布。事务回退后再次读几何/连接，并核输入SHA不变。

### 3. 器件微调与源端预算

移动/旋转先读取实际xy、rotation及pin布局，原生axlTransformObject完成后再读回。新pad主动与旧线/旧via和邻pad检查；PlaceBound AABB只证明此边界范围，不证明真实MPN装配。

线宽小于正常值时核整条连续neck，包括pad内段。源b015实际读取PB1=2.754202mm≤2.8、PB10=2.519239mm≤2.6、VBUS18=1.315685mm≤1.4；这些是当时几何，不是后续返工后的固定结果，见[细颈合同](review/source_b015_fine_neck_contracts.json)。不能因为共享class规则设2.8便给每个网都放大预算。小via通孔铜盘要逐TOP/L2/L3/BOTTOM检查，许可via类型和via_via间距是两种规则。

### 4. 动态Shape与真实铜

静态铜Shape和动态母边界的void顺序必须区分。官方 axlShapeChangeDynamicType 会删除静态Shape原有void；动态地必须先建立dynamic母边界，再在BOUNDARY上添加永久void并读回核验，不能把静态void建立后直接转换视为保留。实现及失败修正见[Shape操作](scripts/batchHI_shapes_v3.il)、source/apiHI及本次批次快照；b016恢复流程仍在原生验证，只有实际保存重开后的版本可作成功复现入口。构造时旧动态地片可能占据未来信号通道；只有在新训练副本里暂卸精确母边界、建线后恢复原边界/void/相对priority及参数并更新，不能靠删除参考放行。

核填充ETCH polygon、holes、spokes/thermal、OOD及连接；母边界/填充颜色不是实铜。弧线按官方axlPolyFromDB规则解释，不拿BBOX作plane；新的重复四位小数弧端点要以误差界处理，原孔不可丢弃。原生面积与转换面积误差需记录。

最终TOP应用地仍是待执行候选：2L替换三处局部母边界，4L当前没有TOP母边界；两板都须避新quiet岛moat和全部真实guard投影。见 plans/final_TOP_GND_candidate_*_01.json，不能直接标为已铺好。

### 5. 连接、规则、回路分别验收

原生端点证明只判断物理连接；规则验证要读effective CSet/类成员/region及实际间距。局部例外复制实际有效父规则，仅改明确字段，保其余layer/field，重叠区不能假定“后加覆盖”。用临时收紧规则使真实几何报错，再恢复原值重查，证明规则确实生效。

真实参考检查要对当前填充铜、孔、开槽和返回过孔进行，不只看同net。2L分别检查TOP与BOTTOM互为参考时的中断、同层地桥/窄颈与绕行；4L核TOP-L2、BOTTOM-L3及换层返回。近旁GND via还要证明接到application GND，quiet岛不能当普通返回。

HSE采用专用岛及单anchor。全部线路/地铜完成后，只删新anchor via(46.35,29.4)：C22/C23/guard/岛应互通，却不能到VSS47、application GND或case；case与VSS应仍相通。事务恢复后重新更新、连接及DRC，不能只靠一次早期反测。

### 6. 保存与复核

Cadence -readonly不能SaveAs，不能以?writeModel=t绕过。标准办法是新建隔离可写工作副本，源SHA与输出白名单保护，输出路径必须不存在；完成后保存新名，再丢弃工作输入，避免退出误存。相关流程见[scratch副本守卫](scripts/launch_source_guardedHI_v11_writable_taskcopy.py)，每个后续批还要核自身配置/输入快照/实际loadorder，不能任意直接运行旧编译脚本。

完整axlDRCUpdate(nil)与t都可能触发内部field计算：nil是整板interactive(on)范围，t额外含batch-only，并非“物理/电气”二分。scoped axlDRCItem按实际网记录，只能证明此范围。未返回的整板DRC写null/待完成；cached0也不能充当新重算0。新进程重开核几何、所有net终端分量、NC、实际铜、规则/film和源SHA；第45/50课要求全69网闭合、无剩余连接、实际回路/参考及DRC均验收。

## 逐课实操证据与未完项

| 课号 | 已有实操/证据入口 | 最终仍须完成 |
| --- | --- | --- |
| 38 | edit_pilot_*_02拆线/重布/via/事务回退；精确批删；实际保存重开 | GUI捕捉和交互待桌面恢复 |
| 39 | source_b015两板MCU联合源；实际细颈合同；拥塞失败/布局取舍 | 13个GPIO长路全组及最终原生检查 |
| 40 | power_b001/b002d/b003c供电、输入回路、反馈、主干和去耦 | 返工后供电/所有瓶颈再核 |
| 41 | 原生dynamic/void/实铜导出、thermal识别和面积核对 | 最终TOP地、孤岛/颈缩和全部GND连接 |
| 42 | HSE真实岛/guard/单anchor反测、ADC/VDDA局部铜 | NRST后续实际路及终板隔离/耦合复查 |
| 43 | USB8/aux14实际线对/ESD通铜、端口分叉及收紧挑战 | J2 GND实际连通和最终参考/返回复查 |
| 44 | SPI12两板原生；UART/I2C/CAN/调试源b015；remaining候选 | 接口长路实际执行、回流及GPIO整组 |
| 45 | 多个两层可回退阶段板 | 全69网及连通/DRC/真实回路三项验收 |
| 46 | 实际TOP-L2-L3-BOTTOM、内层地铜与非GND禁内层规则 | 最终每条关键路径参考投影 |
| 47 | 实际信号/地via及HSE单anchor、全层铜盘问题定位 | 全部新增via真实返回/参考及残桩审查 |
| 48 | 实际plane holes/弧线、moat/guard投影、参考缺口记录 | 最终铜更新后的开口/跨缝与绕行 |
| 49 | USB phase与uncoupled局部预算、真实严格挑战 | 终板端接/残桩/适度匹配及工艺前提 |
| 50 | 同一80件电路的两板阶段文件 | 完整四层板及定量两层比较 |

## 适用条件

低接口时钟不是慢边沿；教学频率/线缆/负载限制尚未成为固件或实测保证。90Ω估计依赖Dk/介质/铜厚及邻地，板厂未确认不能当认证。默认1mm高度不是实际MPN，NULL阻焊盘不等填孔或可靠盖油。装配、晶振启动、ADC采样、温升、反灌、系统ESD/EMI/辐射仍在制造/硬件开放项，不能靠DRC0关闭。

完整失败与修正保留在logs、plans、engineering_*/readouts及主笔记；发现记录乱码须修复并留备份。本索引只是找证据和复现的方法，不把未通过的课程标为已完成。


本轮候选更正及禁止复用入口见[弃用索引](review/deprecated_root_candidates_20261022.json)：cleanup01误删两板R27供电，J2 entry01未通过实际pin连通；只可作为失败记录。新候选仍须原生验收。
