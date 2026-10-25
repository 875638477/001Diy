# 第 60 课资料学习：页码、图形、证据与可迁移来源

日期：2026-10-23，Asia/Shanghai。本分组完成两页真实 PDF 的读取、渲染与视觉核对、一个本机 Cadence 帮助段落核对、三条已索引视频路径检查。没有启动 Cadence，没有播放视频，没有执行 OCR；本记录不新增整本教材或整讲视频完成进度。

## 本轮实际读了什么

| 实填记录 | 来源与定位 | 实际证据 | 状态 |
| --- | --- | --- | --- |
| L60-PDF-TEXT-001 | USB4105，Rev B4，18/12/23；PDF 物理第 1 页，页内 Sheet No. 1/2 | 2529 个可提取字符；整页渲染已查看，图纸方向、单位与尺寸已交叉核对 | 选定页已读，未做封装操作 |
| L60-PDF-SCAN-001 | Cadence 17.2 教材；PDF 物理第 281 页，纸页 262；图 9-188、图 9-189 | 提取文本 0 字符，存在 1 个页图；整页渲染已查看，纸页 262 可见 | 真实扫描页已视觉读，不是派生伪扫描；OCR 未做 |
| 本机官方帮助 | SPB172/doc/algrolibdev/chap5.html，anchor 1033539，原文件第 785 行附近 | END 语句与 netin warning 段落已读取；来源 SHA 已记录 | 文档核对，未实际触发 warning |

PDF 输入均只读，读取前后 SHA-256 相同。仅访问上述两页正文，没有重新解析、复读整本 492 页教材。既有学习笔记用于定位页码，本次仍以新渲染的当前源页为依据。[页读取与渲染清单](../examples/lesson60_20261023/sources/pdf_read_probe.json)保留文字数量、页图数量、像素尺寸、源哈希及渲染器版本。

文字页来源：`learning/examples/lesson10_connector_20261018/source/usb4105.pdf`，SHA-256 `FB331FBABEE8392ED2937ED757C1610CB0F174B84625147C0B580A18EEA8C0E5`。扫描教材沿用既有源文件，位于 `D:\005study`，SHA-256 `FB16EE05893C976F8E71706B4A2EFC29AB6179C0F4BD66336B90FB90C1AD44B3`。完整文件名、字节数和页数见 JSON，不根据书名相同认定版本相同。

## 两页中学到并核对的内容

USB4105 页内明确单位 Metric (mm)、Not to Scale。推荐 PCB 图注明从元件面观察，局部公差 ±0.05 mm；不能用截图像素比例量尺寸，也不能拿标题栏一般公差覆盖局部公差。图上 0.50 mm 间距、PCB 推荐图的 2×Ø0.65 mm 与另一视图的 2×Ø0.50 mm 属于不同图形/对象，应带视图和标注上下文分别登记，不能因为数字接近就替换。推荐焊盘、孔、器件端子、本体轮廓与板边分别核查。这次核对的是来源解释，没有修改 USB4105 公共库或已有封装。

扫描教材纸页 262 的图 9-188 显示 Start 页签、Slot 用途、Oblong 默认几何、Mils 单位；图 9-189 显示 Drill 页签、Oval slot、X size 60、Y size 140、Plated。X/Y tolerance 的 + 与 - 两个框都显示数值 3，应理解为各方向公差幅值，不能把负公差框的 3 识别成 +3 的偏移。旁边正文将 Drill Offset 的 X/Y 写为 0，并给出 BEGIN LAYER Regular Pad 的 Oblong 100×180；后者是正文设定值，本页尚不能证明软件已经保存了这些铜盘。60×140 mil 换算为 1.524×3.556 mm，±3 mil 为 ±0.0762 mm，100×180 mil 为 2.540×4.572 mm，均为教材示例，不是当前 PCB 的工艺默认值。

本机官方帮助指出 device file 的 END 可选但强烈建议保留，缺少时 netin 会给 warning。本次仅阅读该文档语义，未执行 netin，也没有生成或消除这个 warning。[本机帮助定位](../examples/lesson60_20261023/sources/selected_local_help.json)同时区分“手册描述的警告”和“本次日志中实际出现的警告”。Padstack 实际警告应逐字保存软件消息、层和源 PAD，不能用别处的文档警告冒充处理结论。

## 页码和 OCR 的操作顺序

先记录源 SHA、版本和总页数，再分别填写 PDF 物理页号（从 1 开始）、API 索引（从 0 开始）、纸页/Sheet 和章节/图号。本页已经验证 281 对应 262；既有记录的“PDF 页 = 纸页 + 19”仅适用于这个已识别版本的正文，不默认套到前言、目录、附录或另一版书。

文字页先提取便于检索，再查看整页图、标题、脚注和相关视图。扫描页提取为空时仍继续渲染并视觉阅读；0 字符不表示空白页。本轮扫描页实际有图文，没有运行 OCR。后续若用 OCR，应保存引擎/版本/语言、原图哈希、原始识别结果和人工修正稿，并逐项核对 0/O、1/I、正负号、µ、Ø、小数点、mm/mil、TOP/BOTTOM、引脚号及界面字段。OCR 结果可帮助检索，不能替代几何和字段复核。

环境 PATH 未找到 pdftoppm/pdfinfo/tesseract，因此采用 01AIEDA 内已有 Python 3.14.0 + PyMuPDF 1.28.2 渲染。没有临时联网安装依赖，也未把未安装 OCR 记作 OCR 完成。两张最终整页图已分别查看，页边、纸页号、图号和主要界面均可见：

- [文字页完整图](../examples/lesson60_20261023/sources/usb4105_pdf001.png)
- [真实扫描页完整图](../examples/lesson60_20261023/sources/cadence_book_pdf281.png)
- [实际视觉核对记录](../examples/lesson60_20261023/sources/visual_review.json)

## 视频来源与时间点记录

既有源索引确实包含视频；本次不是“未给视频”。旧第 01 讲原路径不存在，依据既有 progress.json 的“完整版”路径核对，第 01、02 讲 AVI 都存在，分别约 49 MB、78 MB，文件 SHA 和 RIFF/AVI 头已记录。[本次路径检查](../examples/lesson60_20261023/sources/video_presence_and_scope.json)只检查这三条显式索引路径，没有扫描整个 D 盘，也没有重新下载视频。

本轮播放 0 讲、听音频 0 讲、查看新帧 0 张；没有核实时长或填写任何新学习时间点。既有记录仍为全讲学习完成 0 讲、曾有两讲代表画面预读、音频待完成；历史状态不自动变成本轮执行证据。AVI 头和文件 SHA 不能证明整片可解码、讲解已听完或操作已掌握。

[视频分段模板](../examples/lesson60_20261023/sources/video_segment_template.json)的 start_ms/end_ms 保持 null。以后学习时，以源文件 SHA 固定时间轴，记录 16.6/17.2 版本差异、起止毫秒、是否实际播放连续片段、是否听到音频、讲解内容/画面内容/推断的区别及对应小操作。抽取某个时间点的帧，只能证明这张画面被查看；不能把最后一帧或密集缩略图当作完整播放。若时间轴经过剪辑或变速，另存原时间→当前时间映射。

## 记录模板与真实执行能力

[教程记录模板](../examples/lesson60_20261023/sources/tutorial_record_template.json)可直接复制填入，两个实填例子见[实际来源记录](../examples/lesson60_20261023/sources/tutorial_records.json)。每条记录分开存放原文事实、图形判断、单位换算、未解决问题、拟操作步骤、输入/输出与验证证据。

证据阶段依次使用 INDEXED、READ_SCOPED、PROCEDURE_PREPARED、EXECUTED_LOCAL、FRESH_VERIFIED_LOCAL、REPRODUCED_NEW_PC；TEMPLATE 只供填写，不算完成。本组两条实填均停在 READ_SCOPED；native_execution.executed=false、迁移复现实验=false。学会描述 Padstack 字段，不等于在当前机器创建 PAD，更不等于跨电脑后已能执行。实际建库或走线仍要核对软件版本/许可证、源输入、操作日志、原生输出、保存后重开和读回几何；已有脚本也要先核输出路径与依赖，不能凭脚本存在认定可复现。

## 迁移依赖和本轮边界

本组记录及页图已位于 01AIEDA，可随目录迁移；相对路径优先。Python 和 PyMuPDF 也已在该根下，重建时按根路径定位，不写死原机器盘符。文字 PDF 已在 01AIEDA；扫描书和两个视频仍在既有 D:\005study，本轮没有复制整本/整片，它们是明确的外部来源依赖。迁移时需把这些自备材料放到新机授权位置，再用源 SHA 绑定新路径；页图与学习笔记可以继续查看，但不等于原始资料已随包完整迁移。

本机 Cadence 官方 HTML 属安装依赖，需在新机相应版本的安装目录重新定位并核对。此分组没有运行 Cadence、没有访问许可证、没有检查 GUI 连接，也未证明跨电脑可执行。这些由第 60 课环境/原生小操作复现分组单独记录。[依赖清单](../examples/lesson60_20261023/sources/source_dependencies.json)将 01AIEDA 内资料、外部资料与安装文档分开登记。

[验证脚本](../examples/lesson60_20261023/sources/validate_sources.py)和[验证结果](../examples/lesson60_20261023/sources/source_validation.json)检查记录、页图、源哈希、实际页码身份与“未播放/未 OCR/未原生执行”的状态一致性；这属于资料证据验收，不能用于宣称封装或 PCB 设计验收。资料原件、旧学习记录及已封存 JK 文件均未修改。

首次资料验收出现 1 项报告链接检查失败：source_validation.json 在链接检查之后才生成。已调整为先预留结果文件再检查链接，失败报告保存在 [source_validation_first_pass_link_pending.json](../examples/lesson60_20261023/sources/source_validation_first_pass_link_pending.json)；资料源文件和页图均未改动。最终 74 项检查通过，0 失败，18 个本组产物的清单哈希全部一致。
