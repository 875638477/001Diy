---
name: cadence-schematic-layout
description: Arrange Cadence Capture reference designators, values, net names and off-page connectors without text overlap or unnecessary wire detours. Use for schematic reconstruction or cleanup with existing local symbols, native save/reopen and connectivity verification.
---

# Capture 清晰排版与简洁连线

先读[完整方案](../../notes/capture_compact_schematic_layout_method.md)，再按当前工程范围实施。用户当前约束优先。

1. 确定工程源、原图、纸张、库路径和可移动范围；保存来源身份及副本。实际工程记录、计划和输出放工程根，学习库保存通用方法。
2. 优先用本地真实基本器件符号。普通二端阻容尽量水平，实际 1 脚左、2 脚右；位号在左、Value 在右，与器件同行稍偏上。依据实际字形避让，不固定上方两格，不改变规格或极性。
3. 先调整显示文字的偏移与对齐，再考虑必要的局部导线。网名、翻页符文字和引脚名/号保持独立可读，位号/Value 靠近所属器件。
4. 保持短直连线和原图分组；独立信号就近接器件、测试点及端口。不要为了文字位置制造长 U 形折返或把无关信号汇成很长的线束。
5. 区分显示属性、网络别名、翻页符、层次端口与电源符号；移动文字不等于移动电气热点。同名文字不能代替跨页和层次连接校验。
6. 用原生引脚热点、旋转/镜像变换、实际字体范围及网格生成局部计划。候选位置限制在器件附近；未解决项显式记录，不遮盖、截短或无限缩小文字。
7. 在副本应用后原生保存、重开、重新导出。对实际交付源逐页检查显示，逐 RefDes.Pin 比较网络分区、名称、NC、属性和封装。有 PCB 交接要求时验证真实主工程网表及严格 Allegro 导入。
8. 分别报告原生重开、几何检查、GUI 阅读、网表与 PCB 导入的证据和未验项。不能用临时测试设计、旧日志或器件排除项冒充主工程通过。

阻容细则见[既有规范](../../notes/capture_rc_horizontal_ref_value_layout_spec.md)；原生变换、GDI 文字边界及现有参数化工具见[几何与可读性](../../notes/capture_text_geometry_and_readability.md)。A3 等纸张要求由本次任务决定，不硬编码为所有工程的默认值。

此技能保存在用户 AI 学习库，供后续读取复用；保存文档不等于模型权重训练或新会话自动加载。
