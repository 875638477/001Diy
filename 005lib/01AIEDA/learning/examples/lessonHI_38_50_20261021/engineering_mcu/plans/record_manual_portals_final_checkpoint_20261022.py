from pathlib import Path
import hashlib,json
R=Path(r'D:\001DIY\005lib\01AIEDA');H=R/'learning/examples/lessonHI_38_50_20261021';P=H/'engineering_mcu/plans';N=R/'learning/notes/lessonHI_mcu_20261021.md'
text='''

### 17.5 补充比较：保原北排针与避免去耦下方内层 slot

后续 [94 两层原北 J12 完整比较](../examples/lessonHI_38_50_20261021/engineering_mcu/plans/PB10_original_header_2L_94.json) 和 [94 四层比较](../examples/lessonHI_38_50_20261021/engineering_mcu/plans/PB10_original_header_4L_94.json) 在 f29 v46 源门户基础上，完成 U1.21→原北 J12.4 的手动几何路径，长度均46.06476 mm，比南置92少31.49209 mm；需要5个新增 private signal PTH，以及6个 GND return PTH/两条 BOTTOM .6 返回桥。它们尚未组合其余6个 South GPIO 长路，不能与南置81混成“全7路”。全部22项新增外层对象检查通过，仍不是原生 DRC。

94 还把 PC13 接收孔从 v46 的 `(29.25,40.05)` 移到 `(29.25,40.95)`，TOP 前段到 `(24,46.2)` 后，必须横到 `(23,46.2)` 接回原 x+y=69.2 长尾。曾错接到69.3，导致邻 GND16.9,53.3 铜距仅 .2364<.3、邻 PA2 孔仅 .1657<.2，已在同轮几何核中修正，未执行原生。PB10 一个转层到既有共地孔约2.57 mm，并未实现所有过孔返回≤1.5 mm；实际 TOP 同层共地/返回绕行仍需补验。

[95 更新后的四层 PB15 比较](../examples/lessonHI_38_50_20261021/engineering_mcu/plans/PB15_4L_short_L2_comparison_95.json) 取代89作为内层对比的首选读物，89保留历史。89虽外层检查无碰撞，其 L2 走向会投到 C16 的供电/地 pad 下方；这说明只检查外层 DRC 不能证明电源回路和参考条件良好。95 绕开 C15/C16/R17 pad，L2 增至9.33543 mm，完整PB15=51.11220 mm，仍12项几何检查通过，没有原生执行/内层许可批准。

[95 实际参考几何审查](../examples/lessonHI_38_50_20261021/engineering_mcu/plans/PB15_4L_L2_reference_95.json) 使用实际 b019 的 L3 GND 填铜：候选内层线及 .2铜宽投影原先全部覆盖；按新 signal PTH 半径.26加保留.30 GND间距，估计两端共1.15206 mm参考开口。该 anti-pad 是明确平面估计，实际 native repour 仍必须读回。计划 L2 slot 会使 TOP 的 BOOT0约1.1314 mm、PA15 .8 mm、PB4约1.0528 mm、SCL约1.1314 mm、GND支路约 .6255 mm中心线投影失去原L2参考；不能因为新L2线能参考L3，就忽略原TOP线受到的影响。C16地 pad 到计划slot最近仅 .21872 mm，仍是需要PI/场宽复核的边界，不称性能合格。

截至本补记，所有95/94/92/87均为只读工程比较；最新真实板保持b019、两板各7个待接GPIO。root已在当前用户状态回复中明确未完成整板验收。本阶段不再扩大无收益的广域搜索；下一轮应由root统一选择可解释的布局/层功能取舍，再叠全7路径、做完整回流与原生验收。
'''
with N.open('a',encoding='utf8')as f:f.write(text)
files=[P/x for x in ['PB15_attach_2L_87_delta.json','PB15_attach_4L_87_delta.json','PB15_4L_short_L2_comparison_95.json','PB15_4L_L2_reference_95.json','PB10_south_2L_92_candidate.json','PB10_original_header_2L_94.json','PB10_original_header_4L_94.json']]+[N]
D={'status':'READ_ONLY_CANDIDATES_NOT_NATIVE_COMPLETE','actualBaseline':'padentry_2L/4L_b019_DRC_PENDING; both7remaining','files':[{'path':str(q),'sha256':hashlib.sha256(q.read_bytes()).hexdigest()}for q in files]};(P/'manual_portals_record_manifest_20261022.json').write_text(json.dumps(D,indent=2),encoding='utf8');print('Saved',len(files),'artifacts. Note SHA',D['files'][-1]['sha256'])
