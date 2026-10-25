# J/K 第51—59课训练资料

日期：2026-10-22—23。所有文件属于学习训练，不是已批准的生产包。入口：[完整学习笔记](../../notes/lessonJK_51_59_20261022.md)、[逐课计划与实际状态](learning_plan.md)、[生产/结课门槛](../../notes/lessonJK_release_gate_20261023.md)。

## 当前实际PCB

| 用途 | 文件 |
| --- | --- |
| 新四层：L2公共GND、L3单V3V3电源 | [JK_4L_L2_GND_L3_V3V3_STACK_TRAINING_NOT_RELEASED.brd](native/4L/JK_4L_L2_GND_L3_V3V3_STACK_TRAINING_NOT_RELEASED.brd) |
| 两层：三文字/高度修正 | [JK_2L_J55_text_height_review_NOT_RELEASED.brd](native/2L/JK_2L_J55_text_height_review_NOT_RELEASED.brd) |
| 旧四层对照：三文字/高度已修，L3仍GND | [JK_4L_J55_text_height_review_NOT_RELEASED.brd](native/4L/JK_4L_J55_text_height_review_NOT_RELEASED.brd) |
| 未布局ECO演示，不是布线成果 | [DE_ECO_REPLAY.brd](eco/DE_REPLAY_ONLY/DE_ECO_REPLAY.brd) |

新四层SHA256：471176A9B25BA8DEF9F117AEFB1E9220CBCBEBBAC5191BCBC6E228F52831F3F9。层名固定TOP-L2-L3-BOTTOM；层功能TOP器件/信号、L2完整公共地、L3电源、BOTTOM信号。完整地不等于消除正常焊盘/过孔反焊盘及机械避让。

每板原有7个GPIO未接、USB数据/共享4网及整板DRC待验未被本轮整改解决。新四层实际plane功能、普通铜保持、参考覆盖、GND—电源参考转换分别审查，不能把实际有平面或共地推导成所有高速返回通过。

## 输出与证据

- 原生命令、输入/SHA、回退与失败：[native/README](native/README.md)、[完整原生记录](../../notes/lessonJK_native56_20261022.md)
- 实际新栈制造文件：[newstack_4L_TRAINING_NOT_FOR_FAB](exports/newstack_4L_TRAINING_NOT_FOR_FAB/)
- 新栈独立CAM：[85项结果](review/independent_CAM_NEWSTACK/summary.json)、[新旧图元34项比较](review/independent_CAM_NEWSTACK/geometry_delta.json)、[实际总览](review/independent_CAM_NEWSTACK/4L/ACTUAL_CAM_CONTACT_SHEET.png)
- 新栈独立实际几何/参考：[报告](review/independent_newstack/review.json)、[笔记](../../notes/lessonJK_newstack_independent_20261023.md)
- 两层和旧四层J55修正CAM：[独立结果](review/independent_CAM_J55/summary.json)
- 原模板未包含的三种文字：[两层伴随输出](exports/supplement_2L_THREE_TEXTS_TRAINING/)、[旧四层伴随输出](exports/supplement_4L_THREE_TEXTS_TRAINING/)、[独立结果](review/companion_and_J55_CAM/summary.json)
- BOM/坐标/装配资料：[两层/旧四层身份索引](assembly/CURRENT_TRAINING_INDEX.md)、[新四层身份入口](assembly/NEWSTACK_4L_L2_GND_L3_V3V3_TRAINING/README.md)
- 隔离ECO：[本轮1453项独审](review/independent_K58/review.json)
- 上电方案/实测表：[第59课笔记](../../notes/lessonJK_59_bench_20261022.md)、[两层空白表](bench/2L_measurement_sheet_NOT_RUN.csv)、[四层旧b019空白表](bench/4L_measurement_sheet_NOT_RUN.csv)

原模板名称/映射和01env不改；3个伴随文字Film不是自动合并的发厂丝印/装配图。每个输出只与所记录源板SHA匹配。新旧板、generator、try工作副本分开，不能互换名称冒充版本。

## 操作复现及验证范围

先读当前EDA.md计划、层名/封装规范和本目录learning_plan，再读native/README中的实际版本、启动环境和命令。需要从输入固定SHA的新副本重新执行，不能对原工程或用户正在编辑的窗口重放历史脚本。初始化/追加记录脚本并非可随意重复运行的入口。过程文件和错误历史保留在本目录，不放到系统临时目录或云文档。

本轮桌面控制仍native pipe/os error2；软件实操使用Cadence17.2官方原生接口和命令行，不能称GUI菜单/交互画面已验。原生参考读取首稿漏遍历path的segments产生空集合，空子守卫和空采样标NOT_EVIDENCE；后续真实线段补读及独立全宽几何检查另有证据。非空采样也不自动等于参考连续通过。

原生artwork退出码1的DRC_OUT_OF_DATE/无photoplot rectangle警告保留，不能写成DRC=0。制造仍有阻焊桥、字体、DNP钢网、采购/真实高度、工厂旋转映射等开放项。第59课全部NOT_RUN，没有实板、波形、EMI或上电成功证据。

## 新栈最终补证入口

新栈独立结构73项、约束/实际补采样8项通过；103个net/layer全宽参考足迹与66个信号过孔返回审查保留性能开放项。[新栈门槛补充](audits/jk_release_gate_newstack4L_supplement_20261023.json)衔接旧77条历史门槛；[policy新旧映射](review/layer_policy_history_mapping.json)明确活动进度来源变化，不修改旧封存清单。
