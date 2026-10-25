# 新四层实际栈的装配身份补充（2026-10-23）

本补充绑定 `JK_4L_L2_GND_L3_V3V3_STACK_TRAINING_NOT_RELEASED.brd`，SHA256 `@@BOARD_SHA@@`。实际层名仍是 **TOP-L2-L3-BOTTOM**；L2共地、L3已实作V3V3，独立结构审查通过。本次没有启动Cadence，只审原生新进程读回并生成独立装配副本。旧J55及放行门槛封存记录保持原身份和原状态。

对旧J55_4L逐项核对：80件ref/package/pose、272电气pin、278含机械孔的实际pin记录、247实例文字及573封装几何记录完全相同。247文字含240个三文字目标和7个包装丝印文字；80个PlaceBound shape高度中72个用户1mm默认、8个原显式值保留，另4个legacy path保持。字体、旋转、镜像及位置字段均未改变。

80件VALUE由新旧两板的原生instance/compdef属性与官方`axlWriteDeviceFile`的`PACKAGEPROP VALUE`双重核对，逐件与BOM相同；没有从设备文件名或deviceType拼写推测值。封装原点坐标、原生旋转及pin1实际坐标保持，工厂旋转继续空白，不把封装原点认作已核准吸取中心。

[新装配包](../examples/lessonJK_51_59_20261022/assembly/NEWSTACK_4L_L2_GND_L3_V3V3_TRAINING/)含80件BOM、66组BOM、80件坐标、65个SMT候选和15个非SMT/DNP项。除3份坐标类CSV的源板SHA外，字段与旧包一致；BOM用[source_identity.json](../examples/lessonJK_51_59_20261022/assembly/NEWSTACK_4L_L2_GND_L3_V3V3_TRAINING/source_identity.json)和新清单绑定此板。68件仍需采购选型；6个NPTH机械孔不计为BOM元件。

新L2连续共地已替代旧振荡器独立岛/void，旧anchor删除后仍共地，旧单anchor隔离结论不再适用。L3从GND改V3V3也改变BOTTOM参考：新栈结构通过不能替代真实回流、去耦及USB/SI/PI/EMI评审。仍有7个GPIO连接，USB4与完整DRC待验收；阻焊桥、钢网、DNP开口、插装及实物高度、工厂旋转等开放项继续保留。全部输出均为 **TRAINING_NOT_FOR_ASSEMBLY**，不能投产。

依据见[装配身份逐项审计](../examples/lessonJK_51_59_20261022/audits/jk_newstack4L_assembly_identity_review.json)、[新栈独立结构报告](../examples/lessonJK_51_59_20261022/review/independent_newstack/review.json)、[新身份放行门槛补充](../examples/lessonJK_51_59_20261022/audits/jk_release_gate_newstack4L_supplement_20261023.json)及[本补充SHA清单](../examples/lessonJK_51_59_20261022/audits/jk_newstack4L_identity_manifest.json)。原J55清单和原77项门槛未改写。另发现旧门槛清单引用的活动四层规则入口已随新栈进展更新；补充JSON明确记录其历史与当前SHA差异，未以重写旧清单掩盖差异。

本次生成过程保留了链接检查顺序错误、活动入口SHA守卫中止及中文编码错误。最终改为显式UTF-8模板，独立重查中文、全部链接、CSV及SHA清单；失败原稿仅存新补充的build_history，不混作有效教学产物。

活动规则入口差异已可复现：见[历史SHA映射](../examples/lessonJK_51_59_20261022/review/layer_policy_history_mapping.json)与[旧规则逐字节快照](../examples/lessonJK_51_59_20261022/backups/layer_function_policy_before_actual_application_20261022.json)。快照SHA精确恢复旧清单期待的121D0220…，当前活动入口为CF767B40…；固定层名及用户层功能规则未改变。本补充未修改旧CURRENT_TRAINING_INDEX或旧装配包。
