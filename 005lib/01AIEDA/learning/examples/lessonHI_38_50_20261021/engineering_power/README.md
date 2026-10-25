# HI 电源、接口、SPI、右侧与北6专项入口

全部产物与中转保存在01AIEDA。本目录只做工程规划、只读审查和图像；唯一Cadence执行、实际板及整板验收由root/native代理负责。完整笔记：[lessonHI_power_20261021.md](../../../notes/lessonHI_power_20261021.md)。

## 当前实际阶段

正式只读输入为 `../inventory/checkpoints/padentry_{2L,4L}_b019_DRC_PENDING`。2L SHA `AA3BFC0E01B06CB1058462439C71E56BC316F1F2929859B6A224320BE1013420`；4L `B7A32330992F49609339E33C00BE92D989D0EA0C4AF64ED2763D0678DE14B501`。North51与TOP common已实际；两板65非USB逐网scoped0、465累计端点/GND/HSE证明通过，仍有South7与USB四网/wholeDRC待完成。不能称整板完成/制造通过。

b019规范化仅四网pad内部normal锚点/细颈对象，实际铜并集0变化；原对象2.141421→1.741421，真实外露细颈始终1.541421，预算2.0未增。独立40checks见 [B019审查](readouts/B019_padentry_independent_actual_review.json)，原生严格挑战与65项结果见 `../review/b019_native_report.json`。

## 实际铜与人工规划图

- [整板上下层PNG](readouts/B018_2L_wholeboard_South7_manual_map.png)：5mm格、真实pad/via/drill、器件/源点/J12/J13，J12南位仅ghost。
- [MCU源端actual放大PNG](readouts/B019_2L_sourcebank_actual_zoom.png)：0.5mm格、真实U1 pad、7源与19个GND/V3孔坐标；对应SVG及各单面PNG均保留。
- [两层USB/North实铜](readouts/TOP_b018_2L_USB_NORTH_actual.png)、[四层实铜](readouts/TOP_b018_4L_USB_NORTH_actual.png)，对应 `*_actual_reference_audit.json`保全部holes/弧、common归属、线宽/中心线缺口与局部诊断。

两面均同TOP-view XY，BOTTOM未镜像；非圆regular pad以native变换bbox近似。图中actual与工程保护overlay/ghost明确分开，不是mask/装配审核。

## USB参考与返回：仍未确认整路合格

2L shared TOP下BOTTOM缺口3.8235/4.6208mm，真实TOP地不能补回对面平面。4L shared中心线全L2覆盖，但PA10/SWDIO反焊盘咬部分线宽。入口DP换层1mm桥位于反焊盘区；不得用bulk几何或共地证明认证90Ω/SI/EMI。

[逐段实际障碍/桥冲突](readouts/USB_shared_b019_obstacles_and_actual_ground_corridors.json)及[多目标实际返地/候选对比](readouts/USB_b019_return_multiterminal_actual_vs_derived_03.json)给出可回放证据。网格是几何诊断，不是HF电流解。`USB_RETURN_SOURCE_COMPARE_*_03.json`是有限普通UART源微调比较，未native，预估仍残较长shared缺口。额外四op地孔/桥比较未改善最近MCUGND指标，建议拒采，所有失败/未采候选保留，勿从文件名误当已布板。

## 已实施历史与必须保留的纠错

电源07c、外设06b、CAN04/05/CAN07、ESD04c、SPI2L v10/4L v6、RIGHT21、UART03、North51均有历史native证据，但后续铜变需重审。North51旧alias按真实pin/新via透明退役，不对旧XY假通过。PC13/14/15输出≤2MHz、负载≤30pF、backup开关3mA且不得作LED电流源，外部负载仍未验证。

曾把TOP V3 `(31.11,55)→(31.11,47)→(38.1016,47)`误判旧R25死枝，实际沿x38.1016供R27.NRST上拉，原y58.2→55也LIVE。两板三段现全保，不得重播N35/N37/N41错误派生删除。原J12北位实际未动；任何南位比较必须保R27供电。b015无端1其实GND generated岛，不是该V3支路。

`cadence_poly.py`保原始解析器备份、端点重合及短切线弧审计；每实际形面积误差<0.01mm²，不能删整个hole制造虚假连续地。旧manifest/north51-stage只代表当时记录完整性；后续阶段使用另立清单，不覆盖冻结件。

持续开放：USB4105脚长/1.6mm装配、OSH阻焊桥、ESD相邻开窗余量、真实MPN高度/电容有效值/温升、USB历史22Ω/阻抗/外线缆及硬件EMI/ESD测试。记录完整不等于制造或整板验收。
