# J/K 结课与生产门槛登记

2026-10-23。本文件只汇总已取得证据和仍需满足的门槛；未执行Cadence、未改原问题或封存清单。当前完整两板结课、生产释放、实物测量均未通过。

[JSON登记](../examples/lessonJK_51_59_20261022/audits/jk_release_gate_register.json) 与 [CSV登记](../examples/lessonJK_51_59_20261022/audits/jk_release_gate_register.csv) 共77条：J51—54来源54条、J55/57来源17条、新门槛6条。每条保原ID、原完整payload、来源路径/SHA和JSON位置；J51—54原状态字段叫nature，J55/57叫status，CSV明确分列，未私自重写原状态。77条包含已验证事实、已闭环实例问题和开放问题，数量不等于77个待修缺陷。

J55三文字/原点/缺省高度的JK55-001/002/003已由两板实际保存、fresh和1644项独立检查关闭；原71条中的其它状态保持来源。BOM/坐标是TRAINING_NOT_FOR_ASSEMBLY，68件采购及工厂吸取/角度等仍待定。

| 新门槛 | 当前证据和未完成条件 |
| --- | --- |
| K56_TEMPLATE_TEXT | 修正CAM两板独立77/85项通过；逐Film22/24项通过，仅PDFTOP目标文字几何改变，其他原Film几何完全相同。每板另3份非空MM3.6伴随图，分别映射80个原生REF丝印/REF装配/VALUE装配实例。原SKILTOP只含PACKAGE GEOMETRY丝印，PDFTOP未含VALUE装配，最终生产包必须明确纳入补充图或另经批准的完整约定。 |
| K56_NATIVE_OOD | 实际photoplot.log保留DRC_OUT_OF_DATE；USB/整板当前检查和剩余连接待完成。CAM可解析不代表已消除OOD。 |
| K58_FULL_TWO_BOARD_COMPLETION | 两板现有审查谱系各7个GPIO连接待做，完整源→PCB→输出及SI/PI/EMI/制造门槛尚未闭环。 |
| K58_ISOLATED_ECO_REPLAY | DE未布局工程已在隔离目录原生netrev重演并fresh，本轮独立1453项/0失败；devfile VALUE与原生compdef双核、80/272/69/6NC/placed0，仅2个VALUE+2个PIN变化，119源保持。该示范通过，与完整两套已布线板结课分开。 |
| K59_NOT_RUN | 两板各17个候选测点、共34项实际测量均NOT_RUN/null；限流值未擅填，候选pad未认证为量产测试点。下一步须有合格实物、仪器和可追溯记录。 |
| K4L_NEW_STACK_REQUIRED | 新推荐固定TOP-L2-L3-BOTTOM，L2完整GND/L3电源；原J55仍历史L2/L3 GND。新四层仍在准备/审批重试，本登记尚未消费原生完成证据，因此旧栈问题保持开放，不能提前关闭。 |

每个门槛的来源文件和SHA见登记内sourceEvidenceFiles；原问题的当前状态、优先级、下一步及验收条件保留完整。来源证据更新或新四层完成后，只对这份派生登记建立新版/新快照，不回写旧sealed审查。更新记录还需重新核来源SHA、CSV行数/状态、源payload逐项一致及旧文件未改。

[生成/重读验证](../examples/lessonJK_51_59_20261022/audits/jk_release_gate_validation.json) 和 [独立清单](../examples/lessonJK_51_59_20261022/audits/jk_release_gate_manifest.json) 提供复现与完整性记录，脚本是scripts/jk_release_gate_register.py。此汇总保留软件训练、完整工程结课和生产/实物验收各自的证据边界。
