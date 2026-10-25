# G30—37 器件布局工程导读

本目录是2026-10-20第30—37课的隔离练习。完整学习笔记在[主笔记](../../notes/lessonG_30_37_20261020.md)，[MCU专项](../../notes/lessonG_mcu_20261020.md)及[电源/接口专项](../../notes/lessonG_power_20261020.md)保留来源、参数、工程理由、操作、失败与复核证据。所有中转和运行目录都在01AIEDA。

## 从这里打开

| 版本 | 当前原生板 | 实际参考铜 | 导电层 / 完整Film |
| --- | --- | --- | --- |
| 四层 | [G_4L_LAYOUT_v1.brd](current/G_4L_LAYOUT_v1.brd) | L2 GND；L3未铺 | TOP-L2-L3-BOTTOM / 17 |
| 两层 | [G_2L_LAYOUT_v1.brd](current/G_2L_LAYOUT_v1.brd) | BOTTOM GND | TOP-BOTTOM / 15 |

两板各80已放逻辑器件、272逻辑pin、69net、6明确NC，另4安装孔机械符号。三组MCU去耦及C16两支路已用TOP实际铜验证，cap端via连接真实动态GND参考；每板4颗GNDvia包含原有1颗。主局部返回为本层VSS—cap，并非必须绕地平面。原生新进程readonly保存后复核及有效DRC均通过。

每板原生导出的91个route段包含27个TOP局部段（V3V3 11、GND16）和64个参考层GND热连接段；不能把全部91段称为手工走线。地铜是实际生成ETCH polygon，不仅是BOUNDARY。

完整网络尚未布线；LDO主供电、buck热回路/BOOT/反馈、USB/ESD、晶振/ADC等属于H/I。当前地连续性要在后续全部信号加入后重审；本次冻结是布局学习检查点，制造输出与实物释放尚未完成。

## 文件与证据

- [原生最终报告](review/native_final_report.json)：当前板SHA、实际网络/层/Film/约束、操作回退、局部铜/地铜导电图、DRC、受控规则挑战、源身份和限制。
- [根独立几何审查](review/root_geometry_review.json)：最终重开两板各597项、272pin及实际器件边界；[最终读回](inventory/)保存统一JSON和原始数据来源。
- [MCU独立局部铜审查](engineering_mcu/local_copper_independent_precheck.json)：阶段证据；[最终实铜独审](engineering_mcu/local_copper_independent_final_review.json)两板各19项通过；[电源接口独审](engineering_power/readouts/final_native_power_review.json)绑定PLACEMENT_v3历史检查点，不冒充后加铜的审核。
- [最终预览](review_figures/layout_overview.png)、[MCU近图](review_figures/mcu_decoupling_clock.png)、[电源区](review_figures/power_lc_input.png)、[USB区](review_figures/usb_protection.png)：真实原生几何/最终位姿及TOP铜；审查标签不是实际丝印，绿色背景不是铜。实际铜的证据以原生图连通、area/fill/OOD为准。
- [计划](learning_plan.md)、[最终80件放置方案](plans/placement_plan.json)、[全局修订依据](plans/root_overrides.json)、[源/数据手册](source/)；专项来源也在engineering_mcu和engineering_power。
- [原生操作详解](native/README.md)、[脚本](scripts/)、[原始日志](logs/)、[历史检查点](native/)、[TCF及原生导出结果](exports/export_result.json)；失败/挑战和post-read脚本错误原样留存。
- [总验收](../../logs/g_lessons_30_37_20261020.json)、[产物SHA清单](review/deliverable_manifest.json)。

## 必须带着走的设计信息

一个G31_U1_ESCAPE区域组含3个TOP矩形。局部physical CSet从相应常规模板复制，仅maxneck从1改1.4mm，四层局部spacing仅smdpin_line/line_line .30→.20mm；它们不是动态parent，且区域/类作用不等于逐pin绑定。实际颈段1.365685mm包含pad内.600000和外部.765685。全局规则保留，内外受控挑战与回退可追溯；改器件位置、pin分组或常规CSet后必须重核覆盖和差异。

两层有独立规则而非照搬四层内层限制，但本轮只给V3V3/GND演示网专用physical class/CSet；其余67网仍DEFAULT .2032mm宽/.16mm间距，完整两层全网分类/专用规则须在整板布线前补齐。物理MASK未添加，15/17项Artwork按完整drill2/4映射，01env模板与既有快捷方式不改。当前源为DE_BASELINE 2.2k方案，不混入历史3.3k ECO，也不交换PB8/PB9。

制造/硬件开放项包含USB4105板厚/固定脚装配、USB22Ω和90Ω、有效电容/MPN、两层阻焊桥、LDO热与反灌、晶振负载/起振/局部地、ADC采样及系统ESD/EMI。默认package height 1mm不证明物料高度；当前所有器件避开限高区。完整丝印、装配、测试点、CAM等仍按后续课程验收。

## 重现与回退

使用本机Cadence17.2S045与Allegro_performance。scripts/launchG.py是官方-nographic/SKILL启动封装，会核路径，限制cwd/TEMP/TMP/ALLEGRO_PCBENV到本目录日志，不使用系统Temp。启动器只凭exit0不能确认工程通过，必须同时核完整结束标记、原生对象和保存后回读。

复核时先复制current板/相应SKILL脚本到新的01AIEDA子目录，替换脚本内输出路径，并使用新的log目录运行；不要重跑现有脚本向已封存日志路径写数据。只读查询用--readonly，并比较前后SHA。任何规则/铜挑战在事务内操作，回退后核80件位姿、约束与DRC，挑战板不替代current。所有本机路径可从launch.json重建。

scripts/review_layout.py读取最终normalized_actual_2L/4L与原生inventory及放置方案；scripts/render_layout.py可从指定normalized JSON重绘审查图。这里的原生API实操不等于GUI拖动/菜单操作已掌握；既有GUI待验保留。下一主线第38课“逐段交互走线与精确几何操作”。