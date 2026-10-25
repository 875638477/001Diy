# Cadence 17.2 焊盘堆叠与过孔学习

本轮完成教材第 9.7 节至第 9 章章末的 37 页视觉阅读。与元件库工作直接相关的理解是：`.pad` 保存焊盘堆叠定义；孔、铜盘、热连接、隔离区、阻焊开窗、锡膏开窗及钻孔图例需要分别检查。教材包含多处文字与截图不一致，后续实践要按字段和实际数值复核。

## 来源和阅读范围

| 项目 | 记录 |
| --- | --- |
| 日期 | 2026-10-17，Asia/Shanghai |
| 来源 | `D:\005study\CADENCE 17.2电路设计与仿真 从入门到精通 云课版 (李鹏) (z-library.sk, 1lib.sk, z-lib.saak).pdf` |
| 范围 | 纸页 228 至 264，对应 PDF 第 247 至 283 页，共 37 页，均已逐页查看 |
| 章节 | 9.7 焊盘的概述；9.8 Pad Designer 图形编辑器；9.9 焊盘设计；9.10 过孔设计；9.11 报表文件；9.12 操作实例 |
| 章末 | 纸页 264 有图 9-194 与图 9-195，不是空白页 |
| 证据 | [37 页阅读清单](../evidence/batch2_padstack_reading.json)，[逐页渲染图](../evidence/padstack_batch2/) |
| 实践状态 | 仅阅读和整理；未打开 EDA 软件操作，未创建或修改 PAD、DRA、FSM 或现有工程 |

正文定位沿用 `PDF 页 = 纸页 + 19`。下文的尺寸是教材示例值，尚未用于实际器件或生产设计；术语疑问和数值冲突集中列在待核对表。

## 焊盘堆叠与层的分工

教材纸页 228 / PDF 247 / 图 9-86 将焊盘视为涉及孔和多个物理层的结构，称 PADSTACK 为一组 PAD 的总称。纸页 237 / PDF 256 / 第 9.9 节明确焊盘文件扩展名为 `.pad`，并说明封装的管脚要引用对应焊盘；放入设计时会复制相关封装及焊盘数据。由此，后续检查应同时覆盖库文件和设计中实际使用的数据。

| 对象或字段 | 本轮理解 | 精确位置 |
| --- | --- | --- |
| Drill、Finished diameter | 孔的几何和孔径信息；与图面显示的钻孔符号分开记录 | 纸 231 至 232 / PDF 250 至 251 / 图 9-101；纸 240 / PDF 259 / 图 9-119 |
| Regular Pad | 每层的常规焊盘几何，记录外形、尺寸和偏移 | 纸 234 至 235 / PDF 253 至 254 / 图 9-111 |
| Thermal Pad、Thermal Relief | 热连接相关的几何或 Flash 符号；教材使用“热焊盘”“热风焊盘”等称呼 | 纸 234 至 235 / PDF 253 至 254 / 图 9-111；纸 244 至 245 / PDF 263 至 264 / 图 9-131 至 9-135 |
| Anti Pad | 隔离区相关几何；教材称“负片焊盘”或“隔离焊盘” | 纸 234 至 235 / PDF 253 至 254 / 图 9-111；纸 238 / PDF 257 / 第 9.9 节 |
| Keep Out | Design Layers 中独立的一列，不能与 Anti Pad 或阻焊层合并记录 | 纸 235 / PDF 254 / 图 9-111 |
| BEGIN LAYER、END LAYER | 焊盘定义的起始层和结束层字段；本章通孔示例对应两端层 | 纸 234 / PDF 253 / 第 9.8.2 节；纸 249 至 250 / PDF 268 至 269 / 图 9-146、9-148 |
| DEFAULT INTERNAL | 默认内层焊盘定义 | 纸 235 / PDF 254 / 图 9-111；纸 249 / PDF 268 / 图 9-147 |
| SOLDERMASK_TOP、SOLDERMASK_BOTTOM | 顶、底阻焊开窗定义，与铜盘几何分别设置 | 纸 235 至 236 / PDF 254 至 255 / 图 9-113 |
| PASTEMASK_TOP、PASTEMASK_BOTTOM | 顶、底锡膏钢网开窗定义；不等于 SOLDERMASK | 纸 235 至 236 / PDF 254 至 255 / 图 9-113 |
| Shape symbol、Flash symbol | 编辑器可引用的外形符号与 Flash 符号字段 | 纸 235 / PDF 254 / 第 9.8.2 节；纸 263 / PDF 282 / 图 9-190 至 9-191 |

教材纸页 229 / PDF 248 / 第 9.7.2 节给出对称性、焊盘大小和与大面积导体连接时热隔离等原则。纸页 238 的尺寸公式有单位冲突，因此本轮保留概念，不将其公式或固定尺寸作为当前元件库的默认规则。

## 17.2 Pad Editor 界面和文件

纸页 229 / PDF 248 / 图 9-87 的实际窗口标题为 Pad Editor，启动入口是 `Product Utilities → PCB Editor Utilities → Padstack Editor`。教材章节名使用 Pad Designer；记录具体操作时以截图中可见的 17.2 页签和字段为准。用户现有 16.6 视频仍可辅助理解共同流程，具体选项要对应到 17.2 环境。

| 页签或操作 | 本轮读到的内容 | 精确位置 |
| --- | --- | --- |
| File → New、Open、Save、Save As | 建立、打开和保存 Padstack；新建时填写名称、位置和 usage | 纸 230 / PDF 249 / 图 9-88 至 9-93 |
| File → Check | 编辑器的焊盘检查入口；本轮没有执行 | 纸 230 / PDF 249 / 图 9-88 |
| File → Script | 录制和重放脚本的入口 | 纸 230 至 231 / PDF 249 至 250 / 图 9-94 |
| Start | 选择用途和默认几何；截图包含 Thru Pin、SMD Pin、Via、BBVia、Microvia、Slot、Mechanical Hole 等 | 纸 232 / PDF 251 / 图 9-100 |
| Drill | 孔形、Finished diameter、公差、Drill tool size、非标准钻孔、孔壁处理和孔阵列 | 纸 232 至 233 / PDF 251 至 252 / 图 9-101 至 9-104 |
| Secondary Drill | 截图包含 Backdrill 以及 Counter bore/sink，具体术语见待核对项 PAD02 | 纸 233 / PDF 252 / 图 9-105 |
| Drill Symbol | 设置图例形状、字符、宽高或直径；这一页签中的尺寸不能代替 Drill 中的实际孔径 | 纸 234 / PDF 253 / 图 9-109；纸 240 / PDF 259 / 图 9-121 |
| Drill Offset | 孔中心相对 Padstack 原点的 X、Y 偏移；多数教材示例填 0 | 纸 234 / PDF 253 / 图 9-110 |
| Design Layers | 逐层设置 Regular Pad、Thermal Pad、Anti Pad、Keep Out | 纸 235 / PDF 254 / 图 9-111 至 9-112 |
| Mask Layers | 分别设置 SOLDERMASK、PASTEMASK 等开窗几何 | 纸 236 / PDF 255 / 图 9-113 |
| Options | 可见 `Suppress unconnected internal pads; legacy artwork`、`Lock layer span`；准确输出和层跨度行为待实际环境核对 | 纸 236 / PDF 255 / 图 9-114 |
| Summary | 查看汇总信息，提供 Save 和 Print；教材展示保存为 HTML | 纸 237 / PDF 256 / 图 9-115；纸 254 至 255 / PDF 273 至 274 / 图 9-163 至 9-165 |
| Units、Decimal places | 单位和显示精度；截图有 Mils、Inch、Millimeter、Centimeter、Micron；正文给出小数位 0 至 4 | 纸 237 / PDF 256 / 图 9-116 |

复核时先确认单位，再分别读取孔、层和符号信息。纸页 240 的图 9-119 显示实际孔径 40 mil；同页图 9-121 的 45 × 25 mil 是矩形钻孔图例尺寸，两者不矛盾，也不能互相替代。

## 钻孔孔形和铣槽示例

圆形孔示例通过 Drill 页的 `Hole type = Circle` 和 Finished diameter 设置；镀孔字段为 `Hole/slot plating`。纸页 232 / PDF 251 / 图 9-101 同时可见 Drill tool size，因此不能把成品孔径、钻刀尺寸和钻孔图例直径合并成一个字段。

纸页 261 至 264 / PDF 280 至 283 / 第 9.12.3 节展示了实际 Slot 用途的操作，并非仅画椭圆铜盘。教材先在 Start 选择 Slot 与默认几何 Oblong，再在 Drill 选择 Oval slot，分别设置槽孔与各层铜盘及开窗。

| 槽孔示例字段 | 截图或文字中的数值 | 精确位置 |
| --- | --- | --- |
| Padstack usage | Slot | 纸 261 至 262 / PDF 280 至 281 / 图 9-187 至 9-188 |
| Drill → Slot type | Oval slot | 纸 262 / PDF 281 / 图 9-189 |
| Slot X size、Y size | 60、140 mil；正文另写成 30 × 140 mil，见 PAD08 | 纸 261 至 262 / PDF 280 至 281 / 图 9-189 |
| X tolerance、Y tolerance | 图中正、负公差输入框均显示幅值 3；需要按各自 `+`、`-` 标志解读 | 纸 262 / PDF 281 / 图 9-189 |
| Hole/slot plating | Plated | 纸 262 / PDF 281 / 图 9-189 |
| Regular Pad | Oblong，100 × 180 mil | 纸 262 至 263 / PDF 281 至 282 / 图 9-191 |
| Thermal | Flash，引用 `tr30_20` | 纸 262 至 263 / PDF 281 至 282 / 图 9-190 至 9-191 |
| Anti Pad | Oblong，90 × 170 mil；其小于 Regular Pad 的尺寸关系需要另行核对 | 纸 263 / PDF 282 / 图 9-191 至 9-192 |
| Mask | 图中 SOLDERMASK 顶、底为 Oblong 106 × 186 mil；文字写 PASTEMASK，见 PAD09 | 纸 263 / PDF 282 / 图 9-193 |
| 汇总 | 类型为 Slot，孔几何为 Oval slot，孔尺寸 60 × 140 mil | 纸 264 / PDF 283 / 图 9-195 |

这组例子明确表明：孔可以是槽形，铜盘也可以是 Oblong，但二者是不同设置。以上仍为教材阅读记录，未生成钻孔、铣槽或制板输出。

## 热连接和 Flash 符号

第 9.9.2 节在纸页 244 至 245 / PDF 263 至 264 / 图 9-131 至 9-135 演示热连接 Flash 符号的建立：新建 Drawing Type 为 Flash symbol 的 DRA，设置图纸单位，再通过 `Add → Flash` 打开 Thermal Pad Symbol。界面包含 Inner diameter、Outer diameter、Spoke width、Number of spokes、Spoke angle 及 Center Dot 等字段，最后通过 Create Symbol 生成 `.fsm`。

该节示例名为 `tr50x64x15-45`，而图 9-134 显示内径 90、外径 110、spoke width 20、spokes 4、angle 45。名称、表 9-3 和截图没有给出一致的参数组合，故本轮只确认字段及文件关系，未按名称推定一个可用的热连接符号。第 9.12.3 节另展示在焊盘 Thermal 中引用 Flash `tr30_20`，位置为纸页 263 / PDF 282 / 图 9-190 至 9-191。

## 通孔 盲孔和埋孔

纸页 248 / PDF 267 / 图 9-142 从层间连接关系区分三类：Through via 穿过整个板；Blind via 连接一个表面与内部层；Buried via 连接内层且不到表面。这是本轮保留的概念区分。后面的示例使用字段和数值存在问题，不能以画出侧视图作为已完成实际盲埋孔工艺设置的证据。

| 示例 | 教材读到的定义 | 精确位置与限制 |
| --- | --- | --- |
| 通孔 `pad_c_1` | 单位 mm；Finished diameter 1.00；BEGIN、END 的 Regular 1.60、Thermal 2.40、Anti 2.40；默认内层 1.40、1.40、2.10；两端阻焊 2.00 | 纸 248 至 250 / PDF 267 至 269 / 图 9-143 至 9-150；均为教材例值 |
| 盲孔 `b_v40_20` | 单位 Mils；Drill 截图孔径 15；BEGIN 的 Regular 40、Thermal 46、Anti 46；默认内层 25、44、44；END 为 None；顶面阻焊 40 | 纸 250 至 252 / PDF 269 至 271 / 图 9-151 至 9-156；开头写“20 mm、40 mm”与后续不一致，且新建截图 usage 为 Thru Pin |
| 埋孔 `bu_v_40_20` | 单位 Mils；Drill 截图孔径 15；BEGIN、END 无铜盘；增加 HOLELAYER，Regular 21、Thermal 38、Anti 38；默认内层 24、44、44 | 纸 252 至 254 / PDF 271 至 273 / 图 9-157 至 9-163；步骤勾选 Backdrill，术语及实际盲埋孔做法需要官方帮助核对 |

本章截图能说明如何编辑局部层定义，但没有构成本轮对 PCB 实际叠层、钻孔层对及制造工艺的验证。`Lock layer span` 的行为也应在独立练习工程中检查，不能仅凭本章文字判断。

## 贴片焊盘和章末实例

| 示例 | 本轮记录的参数与操作 | 精确位置 |
| --- | --- | --- |
| 贴片焊盘 | SMD Pin，Drill 的 Hole type 为 None；BEGIN Regular 为 Rectangle 60 × 30 mil；SOLDERMASK_TOP 为 Rectangle 66 × 36 mil；图中 PASTEMASK 为 None | 纸 245 至 247 / PDF 264 至 266 / 表 9-4，图 9-136 至 9-141 |
| 方形有孔 `Pad50sq30d` | 孔为 Circle 30 mil；两端铜盘 Square 50 mil；文字两端 Thermal、Anti 为 Square 68 mil；两端阻焊 Square 60 mil；默认内层文字为 Regular Circle 40、Thermal Circle 30、Anti Circle 60 mil | 纸 255 至 258 / PDF 274 至 277 / 图 9-166 至 9-176；END 的部分截图数值与“同 BEGIN”描述冲突，见 PAD10 |
| 圆形有孔 `Pad50cir30d` | Circle 孔径 30 mil；BEGIN、END、DEFAULT INTERNAL 的 Regular 为 Circle 50、Thermal 和 Anti 均为 Circle 68 mil；顶、底 SOLDERMASK 均为 Circle 60 mil；最后保存并查看 Summary | 纸 258 至 261 / PDF 277 至 280 / 图 9-177 至 9-186 |
| 槽形有孔 | 单独选择 Slot、设置 Oval slot，并引用 Thermal Flash；详见前面的槽孔字段表 | 纸 261 至 264 / PDF 280 至 283 / 图 9-187 至 9-195 |

贴片示例只展示了顶层铜盘和阻焊开窗，没有定义锡膏开窗。后续用于需要钢网印刷的实际器件时，应另核对锡膏层，不能直接把示例中的 None 作为所有贴片焊盘的默认值。教材的参数表及图例用于理解字段，实际器件尺寸仍需与规格书和当前工程要求对应。

## 教材差异与待核对项

下表中的“内部冲突”可由已读文字、图表直接对照；“术语或工艺疑问”需要本地官方帮助或后续独立实践确认。本轮未将这些疑问宣称为已全部纠正。

补充核对本机 `C:\Program0\Cadence\spb172\doc\algrolibdev\chap2.html`：锚点 `1032184` 明确盲孔和埋孔用途选择 BBvia；`1036681` 将孔或槽尺寸、镀孔、沉孔、钻孔图例和偏移分列；`1038008` 与 `1038037` 分别说明热连接和 Anti Pad 的用途。PAD12 中的 usage 差异因此已有官方依据，实际层对和工艺仍待实践。

主任务另外核对了 [Cadence 17.2 Padstack Editor 官方介绍](https://resources.academic.cadence.com/pcb-design-and-analysis-resources/why-move-up-to-orcad-17-2-2016-new-padstack-editor-more-than-just-a-new-gui-3)，确认 Finished drill、Drill Tool 和 Backdrill 是独立设置，并支持 counterbore、countersink；[Cadence 17.2 焊盘教学资料](https://community.cadence.com/cfs-file/__key/communityserver-discussions-components-files/137/MakePadstackInAllegroSkill.pdf) 第 10 页也指定盲埋孔使用 BBVia，第 13 页的 SMD 例分别设置 TOP 与 SOLDERMASK_TOP。这些支持区分字段和层，不能据此确认教材全部例值正确。

| 编号 | 现象和定位 | 类型与后续处理 |
| --- | --- | --- |
| PAD01 | 纸 232 / PDF 251 / 图 9-101 至 9-104 的字段为 Hole Plating、Plated、Non-plated，正文译为“孔壁上锡 / 不上锡” | 术语疑问；应核对镀孔定义，避免与焊锡混同 |
| PAD02 | 纸 233 / PDF 252 / 图 9-105 实际为 Backdrill 和 Counter bore/sink，正文分别写“埋孔”和“盲孔”；纸 252 至 253 / PDF 271 至 272 / 图 9-159 的“埋孔”示例又勾选 Backdrill | 官方资料已确认这些是独立的钻孔设置，不能把 Backdrill、Counter bore/sink 与盲埋孔直接等同；实际盲埋孔步骤尚待核对 |
| PAD03 | 纸 238 / PDF 257 / 第 9.9 节给出“钻孔直径 + 0.5 mm（6 mil 或 8 mil）”；按单位换算，0.5 mm 约为 19.685 mil，6、8 mil 分别为 0.1524、0.2032 mm | 数值内部冲突；不能直接套用该尺寸公式 |
| PAD04 | 纸 239 / PDF 258 / 表 9-2 与名称 Pad60sq30d 写孔径 30 mil，步骤填 40；纸 240 / PDF 259 / 图 9-119 也显示 40 | 数值内部冲突；示例名不代表实际孔径，须查 Drill 与 Summary |
| PAD05 | 纸 239 / PDF 258 / 步骤 (2) 将 Start 的默认 Square 解释为钻孔 Square；纸 240 / PDF 259 / 图 9-119 的实际 Hole type 为 Circle，外层 Regular 为 Square，见图 9-122 | 字段内部冲突；区分默认焊盘几何与孔形 |
| PAD06 | 纸 240 / PDF 259 / 图 9-121 图注为“设置钻孔尺寸”，界面实际是 Drill Symbol，宽高 45 × 25；实际 Drill 图 9-119 孔径为 40 | 图注易混；分别保存孔径和钻孔图例尺寸 |
| PAD07 | 纸 244 至 245 / PDF 263 至 264 / 表 9-3、图 9-134 中，名称 tr50x64x15-45、表中内径 50 / 开口 15 / 角度 45，与截图内径 90 / 外径 110 / spoke width 20 不一致 | 数值内部冲突；重新确认目标参数后再建 FSM |
| PAD08 | 纸 261 / PDF 280 / 第 9.12.3 节步骤 (4) 先写 X=60、Y=140，随后称槽孔尺寸为 30 × 140；纸 262 / PDF 281 / 图 9-189 和纸 264 / PDF 283 / 图 9-195 均显示 60 × 140 | 数值内部冲突；槽孔大小按实际字段及汇总复核 |
| PAD09 | 纸 263 / PDF 282 / 图 9-193 的文字与图注称 PASTEMASK_TOP/BOTTOM，实际表格显示 SOLDERMASK_TOP/BOTTOM 为 106 × 186，PASTEMASK 为 None | 层名内部冲突；阻焊与锡膏层分别核查，不能按图注替换层名 |
| PAD10 | 纸 256 / PDF 275 文字称 END 与 BEGIN 设置相同，BEGIN Anti 为 68；纸 257 / PDF 276 / 图 9-170、9-171 中 END Anti 可见为 60 | 数值内部冲突；完成后逐行比较两端层，不用“同上”代替复核 |
| PAD11 | 纸 250 / PDF 269 / 第 9.10.2 节开头称盲孔内外径 20 mm、40 mm；同页立即切换 Mils，Drill 图 9-152 为 15；纸 252 / PDF 271 的埋孔例开头为 20 mil、40 mil，图 9-158 仍为 15 | 单位和数值内部冲突；盲埋孔例不作为可靠的尺寸样本 |
| PAD12 | 纸 250 至 254 / PDF 269 至 273 / 图 9-151、9-157、9-163 中盲埋孔例 usage 为 Thru Pin / Through Pin，并使用局部层定义和 Backdrill；纸 232 / PDF 251 / 图 9-100 另有 BBVia 用途 | 本机官方帮助及官方教学第 10 页均要求盲埋孔选择 BBVia，教材 usage 不一致；层跨度和设计层对仍待实践 |
| PAD13 | 纸 245 / PDF 264 的示例名为 smd60_30，纸 246 / PDF 265 / 表 9-4 写宽 60、高 30；纸 246 至 247 / PDF 265 至 266 / 图 9-136、9-138 标为 smd30_60，实际铜盘仍为 60 × 30 | 命名内部冲突；文件名和宽高字段分开记录 |
| PAD14 | 纸 263 / PDF 282 / 图 9-191 至 9-192 的槽形 Regular 为 100 × 180，而 Anti 为 90 × 170 | 尺寸关系疑问；需结合使用层类型与隔离规则确认，不能据此默认采用更小 Anti Pad |

其他阅读提醒：纸页 228 的“顶层焊接锡膏”解释混入过孔铜盘用途，应与纸页 235 至 236 的独立铜层和 Mask 字段交叉核对；纸页 255 图 9-165 图注写 PAD60SQ40D，前文实际例名为 bu_v_40_20，查看报表时应以报表内容为准。上述均未用于修改现有库。

## 理解检查与后续实践

本轮可以回答以下问题：PADSTACK 涉及多个层和孔定义；SMD Pin 示例的孔形为 None；槽孔必须在 Drill 中定义槽几何；Drill Symbol 只记录图例；热连接可引用独立 FSM；阻焊和锡膏开窗属于不同字段；通孔、盲孔和埋孔的概念区别取决于连接的层范围。

下一步与前半章封装学习合并后，在独立副本中核对一个实际器件的 PAD 引用和各层定义。实践记录至少应保存单位、铜盘外形、孔或槽尺寸、公差、镀孔属性、钻孔图例、热连接与隔离、阻焊和锡膏开窗、层跨度及 Summary。盲埋孔和教材存在冲突的示例先核对本地官方帮助，再决定复现方式。本轮完整阅读已完成，软件操作、制造输出和实际库验收仍未完成。
