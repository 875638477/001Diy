# 第56课：实际制造文件的独立复核

日期：2026-10-22—23。范围：原b019训练板及J55文字/高度修正派生板；不作生产放行。

## 实际完成的方法

先只读核对01env/env中的o/O→gerber.scr及其参数/Film链，再在JK独立副本调用本机Cadence17.2的正式artwork、nctape、ncroute。不是在原工程重放整个env，也没有修改快捷键。原生操作与来源、命令、退出码见[原生记录](lessonJK_native56_20261022.md)。

使用本地独立Gerbonara 1.6.3读取实际RS274X、Excellon和槽孔文件，另写原始NC指令解析器与Cadence实际孔账本比对；SVG/PNG来自实际输出，不是示意板图。工具与源文件SHA留在本课目录。未上传工程到在线CAM。

| 输入 | 原模板Film | 独立机器检查 | PTH圆孔 | NPTH | 电镀槽 |
| --- | --- | --- | --- | --- | --- |
| b019两层 | 15 | 77/77通过 | 217 | 6 | 4 |
| b019四层旧栈 | 17 | 85/85通过 | 207 | 6 | 4 |

核对内容包括原Film全部名称与层映射、MM单位、Gerber3.6、NC绝对MM3.4、8段80×60 C2板框、每个圆孔的位置和孔径、4个USB固定槽的中心和外形、278个顶层阻焊开窗、211个顶层钢网开窗。原模板OUTlie/SKILTOP等拼写保留。PDFBOTTOM的镜像是原装配视图设置；BOTTOM铜不镜像。

两张最终CAM总览已逐张查看：各层图框独立显示，内层、阻焊、钢网、钻孔和槽孔均可辨，空的底面钢网/丝印与DRILL.art保留为空的真实结果。该视觉检查只覆盖输出的可见性和明显错层/尺寸问题，不能替代电气、DFM和实物检查。

## 发现的问题与修正边界

1. 原SKILTOP只含PACKAGE GEOMETRY/SILKSCREEN_TOP，不含REF DES/SILKSCREEN_TOP；PDFTOP含装配位号，不含COMPONENT VALUE/ASSEMBLY_TOP。三文字实例合规与三文字已出光绘必须分开验。另用独立generator导出三种文字Film；没有改变主板15/17 Film或01env。
2. 实际Gerber圆角开窗边界距离：C8.2—U3.2约0.0635 mm，C9.2—U3.4约0.08543 mm。两处均进入JK55-010制造开放项，尚未修阻焊或批准工艺。弧线离散误差上限0.00005 mm；不是仅用矩形包围盒估计。
3. R12/R13默认DNP的4个钢网开口仍在实际输出中，不能认为BOM设DNP就自动取消开口。装配profile/钢网决策待定。
4. 原生artwork退出码1伴随DRC_OUT_OF_DATE和无photoplot rectangle、采用drawing extents的警告。文件已生成并独立解析，但不记成DRC通过。
5. 四层b019/J55修正板仍为旧L3地层；不能冒充用户新增L2完整地、L3电源的默认方案。新栈使用另存板和单独证据。
6. 每板7个GPIO未接、4个USB数据/共享网及整板DRC待验继续保留。输出目录均标TRAINING_NOT_FOR_FAB。

## 本次解析错误与防止重犯

原始输出从未因此修改。最初自写NC解析器漏识别Rnn重复孔指令，少算39孔；修正后与第二解析器及原生孔账本一致。Gerbonara对NPTH全局T05/T06与局部Holesize1/2注释的组合不兼容，派生解析副本只去掉注释，原始机器指令与原文件保留。最初总览嵌套SVG坐标/ID重复导致图层挤在左上，改成各层独立渲染PNG再排版，最终两张总览已重新查看。详细失败证据见[解析修正记录](../examples/lessonJK_51_59_20261022/review/cam56_parser_corrections.md)。

## 证据入口

- [b019独立CAM结果](../examples/lessonJK_51_59_20261022/review/independent_CAM/summary.json)
- [两层实际CAM总览](../examples/lessonJK_51_59_20261022/review/independent_CAM/2L/ACTUAL_CAM_CONTACT_SHEET.png)
- [四层旧栈实际CAM总览](../examples/lessonJK_51_59_20261022/review/independent_CAM/4L/ACTUAL_CAM_CONTACT_SHEET.png)
- [视觉复核记录](../examples/lessonJK_51_59_20261022/review/cam56_visual_qa.json)
- [J55与装配记录](lessonJK_55_57_20261022.md)

来源：[Gerbonara文件模型](https://gerbolyze.gitlab.io/gerbonara/api-concepts.html)、[命令与单位说明](https://gerbolyze.gitlab.io/gerbonara/cli.html)、[Ucamco Gerber规范入口](https://www.ucamco.com/en/gerber)；Cadence本机正式文档和模板SHA另存source与原生记录。

## 2026-10-23：J55修正板和独立三文字输出复核

J55两块新板已保存、独立重开，每板822项、合计1644项实例规范检查通过。修正板重新导出的15/17个模板Film、圆孔、NPTH和槽孔各77/85项独立解析检查通过。另把J55与b019逐个Film的实际图元进行比较：两层22/22、四层24/24项通过，只有目标装配位号所在PDFTOP几何发生改变，其余原Film几何完全相同；这是防止改文字时误动铜/孔/阻焊的复核，不是电气DRC。

三文字伴随输出实际存在且已独立渲染查看，各包括REFDES_SILK_TOP、REFDES_ASSEMBLY_TOP、VALUE_ASSEMBLY_TOP三个MM3.6文件。前两类各2339个矢量图元，VALUE类4130个矢量图元；每类80项文字的数量来自独立fresh原生实例审查，不能把Gerber笔画数当文字数。位号/值按用户要求保持器件原点；同一装配原点的位号与值使用独立视图查看，不通过擅自移动文字避免重叠。

- [J55输出独立解析](../examples/lessonJK_51_59_20261022/review/independent_CAM_J55/summary.json)
- [几何差异与三文字复核](../examples/lessonJK_51_59_20261022/review/companion_and_J55_CAM/summary.json)
- [两层三文字实际光绘](../examples/lessonJK_51_59_20261022/review/companion_and_J55_CAM/2L/THREE_TEXT_FILMS.png)
- [四层三文字实际光绘](../examples/lessonJK_51_59_20261022/review/companion_and_J55_CAM/4L/THREE_TEXT_FILMS.png)

所有上述J55四层输出仍为历史L3地层，不能当新L3电源层输出使用。


## 2026-10-23：新四层实际CAM复核

新板文件为JK_4L_L2_GND_L3_V3V3_STACK_TRAINING_NOT_RELEASED.brd，SHA256为471176A9B25BA8DEF9F117AEFB1E9220CBCBEBBAC5191BCBC6E228F52831F3F9。正式Cadence重新导出17Film及PTH/NPTH/槽孔，独立解析85/85项通过；207个PTH、6个NPTH、4个槽孔仍与原始实际位置/孔径账本一致。全部17Film头部Layout Name指向新板。

相对J55旧栈逐个实际Gerber图元比较34/34项通过：只有L2和L3的几何改变，其余15个Film相同；L2对象404→403，L3对象403→383。原生网络身份由独立数据库审查核实，不能单凭普通RS274X中的层名推断GND/V3V3。最终L2、L3单层图及新CAM总览均已查看，旧HSE分隔大开口消失，保留正常焊盘/过孔/机械避让。

- [新栈实际CAM解析](../examples/lessonJK_51_59_20261022/review/independent_CAM_NEWSTACK/summary.json)
- [新旧栈实际CAM差异](../examples/lessonJK_51_59_20261022/review/independent_CAM_NEWSTACK/geometry_delta.json)
- [新栈实际CAM总览](../examples/lessonJK_51_59_20261022/review/independent_CAM_NEWSTACK/4L/ACTUAL_CAM_CONTACT_SHEET.png)

该结果不关闭参考换层、未接网、USB/整板DRC、阻焊/字体、工厂装配和实物验证开放项。新栈BOM/坐标必须绑定新板身份，不得把旧栈输出直接改目录名冒充新版本。
