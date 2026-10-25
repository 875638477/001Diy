from pathlib import Path
R=Path(r'D:\001DIY\005lib\01AIEDA');J=R/'learning/examples/lessonJK_51_59_20261022'
p=R/'learning/notes/lessonJK_51_59_20261022.md';s=p.read_text(encoding='utf8')
s=s.replace('原生保存/独立fresh成功；56个GND pin','原生保存/独立fresh成功，新栈独立结构审查73/73项及约束/补采样后核8/8项通过；56个GND pin',1)
s+='\n### 新四层装配身份与门槛补证\n\n新栈逐件实际VALUE、器件/引脚/文字/高度与源J55匹配后，另出[新栈BOM与坐标入口](../examples/lessonJK_51_59_20261022/assembly/NEWSTACK_4L_L2_GND_L3_V3V3_TRAINING/README.md)，绑定471176A9…新板SHA；旧J55/current索引和旧输出不覆盖。详见[新栈装配身份笔记](lessonJK_newstack4L_identity_20261023.md)。\n\n原77条门槛作为历史快照不改，新栈实际实施/源身份补证与仍开放的SI/PI/制造/实物条件见[新栈门槛补充](../examples/lessonJK_51_59_20261022/audits/jk_release_gate_newstack4L_supplement_20261023.json)。活动层功能policy已由PENDING更新为实际应用状态，导致旧门槛清单一个来源指针的SHA变化；已恢复[原字节快照](../examples/lessonJK_51_59_20261022/backups/layer_function_policy_before_actual_application_20261022.json)，其1188字节和SHA与旧清单完全一致，新旧映射见[记录](../examples/lessonJK_51_59_20261022/review/layer_policy_history_mapping.json)。不将这次有意进度更新冒充所有历史来源均未变化，也不修改旧封存。\n'
p.write_text(s,encoding='utf8')
p=J/'README.md';s=p.read_text(encoding='utf8');s=s.replace('BOM/坐标/装配资料：[当前身份索引](assembly/CURRENT_TRAINING_INDEX.md)','BOM/坐标/装配资料：[两层/旧四层身份索引](assembly/CURRENT_TRAINING_INDEX.md)、[新四层身份入口](assembly/NEWSTACK_4L_L2_GND_L3_V3V3_TRAINING/README.md)')
s+='\n## 新栈最终补证入口\n\n新栈独立结构73项、约束/实际补采样8项通过；103个net/layer全宽参考足迹与66个信号过孔返回审查保留性能开放项。[新栈门槛补充](audits/jk_release_gate_newstack4L_supplement_20261023.json)衔接旧77条历史门槛；[policy新旧映射](review/layer_policy_history_mapping.json)明确活动进度来源变化，不修改旧封存清单。\n'
p.write_text(s,encoding='utf8')
p=J/'learning_plan.md';s=p.read_text(encoding='utf8');s+='\n新增四层默认功能已在[独立新板](native/4L/JK_4L_L2_GND_L3_V3V3_STACK_TRAINING_NOT_RELEASED.brd)实际应用并独立结构审查73项通过；新CAM85项、与旧输出差异34项通过，仅L2/L3变。参考转换/USB/整板DRC/制造/实物仍开放，详见[最新新栈笔记](../../notes/lessonJK_newstack_independent_20261023.md)。\n';p.write_text(s,encoding='utf8')
p=J/'review/root_record_update_corrections.md';s=p.read_text(encoding='utf8');s+='\n- 一个可变层功能进度JSON曾被旧门槛清单当作不可变输入；更新实际应用状态后出现来源SHA漂移。未改旧sealed；按内容逆转新增进度块并恢复CRLF，重建的原1188字节快照SHA精确匹配旧清单121D0220…，新旧映射单独保存。后续封存使用字节快照，不直接引用可变current入口作为永不变化来源。\n';p.write_text(s,encoding='utf8')
print('Final course links and actual scoped results consolidated; old mutable-pointer exception explicitly documented')
