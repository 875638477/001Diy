"""Write the source-bound one-page disposition; retain all stricter FAILs."""
from pathlib import Path
import hashlib,json
W=Path(r'D:\001DIY\004computer\lga1700\13shared_libraries_pc_20261025\w\pcb_migration')
report=W/'FINAL_SOURCE_TOTAL_CU_COVERAGE_V11_REVIEW.json'
strict=W/'FINAL_NATIVE_MATERIAL_V10_REVIEW_REQUIRED.json'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest().upper()
j=json.loads(report.read_text());assert j['outside_source_total_copper_polygons']==17 and j['all150_full_native_arc_and_holes_exact_to_frozen_v10']
text='''# 13版库迁移：有界铜差事实与处理结论

本记录仅绑定源板 `50D3CD8C…94F3341A` 与候选 `49AF5EE7…195C063`。根审接受下述有限铜差用于本轮共享库迁移；后续34颗SOT换封装需单独读回校验。本记录不宣称整板铜完全相等，也不是制造DRC签核。

- 原生593个铜/边界轮廓中582个完整精确相同；11个变化均为GENERATED。全部189个STATIC、87个BOUNDARY、4541个过孔属性及动态/静态设置保持精确一致。
- 对全部11个变化做原生差集，完整保留弧、孔和增减片段；手工线段、非owner几何另有精确门禁。150个新增generated片段与其它网原生铜的直接多边形交集为0，实际6521引脚及2020连通分区、1118网络状态和全部约束已有独立门禁。
- 进一步把150片逐一减去源板原有同网实际pads/vias/whole paths/shapes。133片已被源同网总铜覆盖，包括全部132片L2/L3增量及PC184旧孔区域。
- 余下17片为固定有界新增薄片，总面积 **0.2254311380mil²（0.000145439153mm²）**：BOTTOM GND 12片、TOP GND 4片、TOP +VCCIN_AUX_CPU 1片。逐片坐标、弧、孔及面积均在报告和原生jsonl中，不使用整体bbox或面积阈值代替几何审核。
- PC184旧孔轮廓虽未保留，但源板原有同网总铜已完全覆盖其区域；源/目标同网总铜余片均为0，不能把1641.7222mil²孔面积误算成真实新增铜。
- 额外0.01mil检查边距不是用户规则。其旧严格FAIL原件保留；6个正常margin窗口已按源板真实对象复核。L2负片的原生表示及历史跨网图形交集不能单独推断物理短路。本轮接受依据是固定有界差片、原片直接相交及实际连通/约束门禁，不把该自设margin继续当必需阻塞项。

方法是“完整轮廓抵消→11个原生ANDNOT→冻结150原片→每片与源同网实际总铜再次ANDNOT→连通/规则独立读回”。bbox只用于索引候选对象，不作为允许改铜的区域。源和目标均为独立副本，所有证据绑定原始板SHA，检查未保存或修改源文件。

完整事实：[FINAL_SOURCE_TOTAL_CU_COVERAGE_V11_REVIEW.json](FINAL_SOURCE_TOTAL_CU_COVERAGE_V11_REVIEW.json)。旧严格检查：[FINAL_NATIVE_MATERIAL_V10_REVIEW_REQUIRED.json](FINAL_NATIVE_MATERIAL_V10_REVIEW_REQUIRED.json)。旧FAIL证据不覆盖、不冒称PASS。
'''
out=W/'BOUNDED_COPPER_ACCEPTANCE_V11.md';assert not out.exists();out.write_text(text,encoding='utf-8')
receipt=W/'BOUNDED_COPPER_ACCEPTANCE_V11.json';assert not receipt.exists();receipt.write_text(json.dumps(dict(disposition='ACCEPT_BOUNDED_DIFFERENCES_FOR_LIBRARY_MIGRATION',scope_board_sha256=j['candidate_board']['sha256'],source_board_sha256=j['source_board_sha256'],not_total_copper_equality=True,not_manufacturing_drc_signoff=True,additional_0d01mil_margin_not_user_rule=True,previous_strict_margin_fail_preserved=True,evidence={str(p):sha(p) for p in [out,report,strict]}),indent=2),encoding='utf-8')
for p in [out,receipt,report]:print(p);print(sha(p))
