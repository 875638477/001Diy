# 封装文字与高度默认规范
记录日期：2026-10-17（Asia/Shanghai）
来源：用户本轮明确要求。后续封装创建/修改至少按本规范检查。

| 内容 | Class | Subclass | 文字锚点坐标 |
| --- | --- | --- | --- |
| 位号 | REF DES | SILKSCREEN_TOP | (0,0) |
| 位号 | REF DES | ASSEMBLY_TOP | (0,0) |
| VALUE | COMPONENT VALUE | ASSEMBLY_TOP | (0,0) |

- 坐标为封装局部原点，三个文字对象的锚点均置于器件原点中心；器件放入 PCB 后按其原点和变换定位。
- 这是最少要求，允许按具体工程增加其他必要层和内容。
- 默认 package height 为 **1 mm**。Cadence 实现：在填充的 PACKAGE GEOMETRY/PLACE_BOUND_TOP 上写 PACKAGE_HEIGHT_MAX="1 MM"。本次没有设置 MIN，官方定义其下界默认 0，表示占用 0～1 mm。
- 高度输入显式带单位；不能仅写无单位数值并假定按 drawing mm 解释。
- 用户未指定文字字高、线宽或字体；本次沿用已有文字样式，新增文字使用相同样式并水平居中。Package height 是器件高度。
- 当前练习封装使用 U* / U* / VALUE 占位文本；实际器件的位号和值应随工程填写。
- 默认高度用于初始化；真实器件仍需核对数据手册中的高度。

## 本次应用与核验
已更新 learning/examples/lesson04_package/library/eda_l04_two_pin_training.dra，并重新编译同名 .psm。
新进程只读重开，三项文字均读到 x=0、y=0、rotation=0，PACKAGE_HEIGHT_MAX 读回 "1 MM"。
孔、焊盘、轮廓和放置边界的几何保留原练习定义；原始 .dra/.psm、规格、预览和记录备份在 backups/package_defaults_20261017。

- 脚本：learning/scripts/package_defaults.il、package_defaults_apply.scr、package_defaults_read.scr。
- 日志：learning/logs/package_defaults_20261017/apply 与 reopen。
- 三层文字实值：reopen/required_texts.tsv；高度实值：reopen/defaults.txt。
- 当前规格：learning/examples/lesson04_package/training_spec.json。
- 当前预览：同目录 preview.png；顶视图仅显示 REF DES/SILKSCREEN_TOP，装配位号和值分别在其装配层也以 (0,0) 为锚点。
- 汇总：learning/logs/package_defaults_result_20261017.json。

第 4 课原始笔记/日志保存了修改前的 U* 在 (0,1.6) 等事实；当前库以本次修订为准。历史 SHA 对应修改前快照，可从本次备份复核。
今后复现原始 lesson04_create 脚本后，必须按本默认规范补齐文字与高度并读回；不要将历史脚本当作最新封装规范。

## 本机官方实现依据
- algrolibdev/chap3.html：Place-bound 只设 MAX 时 MIN 默认 0；package height 属性适用对象。
- algroskill/03dbcre8.html：axlDBCreateText、axlDBAddProp；不显式带单位时属性按 units.dat 解释。
- algroskill/06intedt.html：axlTransformObject 的移动接口。
- algroskill/07dbaccs.html：axlDBGetProperties 返回含单位的属性值。

## 第7—10课实操补充

2026-10-18：1mm继续作为初始化默认。真实器件最大高度必须据图纸覆盖：QMI8610/QFN为1MM，LQFP48为1.6MM；USB4105侧视3.31及一般公差±0.15得到MAX3.46MM，壳脚S按器件安装基准面单列，不直接当PCB底面突出量。不要用连接器开口高度替代板上高度。

三项文字锚点仍为(0,0)。QFN中心REF DES丝印会与EP阻焊开窗重叠；库遵守锚点规范，实际PCB应将实例位号移动到可读且不覆盖焊接的位置，检查最终丝印输出。对应实操与其他规则见[B阶段总结](lessonB_07_10_20261018.md)。

## 壳脚S基准补充（2026-10-19）

器件高度和壳脚长度的基准分别记录。USB4105的S是自安装基准面到脚尖，板底突出需另扣实际板厚/座高并计公差，不能沿用早前不清楚的“板下侵入”理解。见[复核勘误](lessonF_source_corrections_20261019.md)。
