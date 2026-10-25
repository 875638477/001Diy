# Allegro 视频第二批软件组件与焊盘案例画面记录

记录时间：2026-10-17T11:09:51+08:00，Asia/Shanghai。此次优先使用带“完整版”名称的源目录。用户说明本地工程与教材为 17.2；本轮画面核对到视频中的 Capture 和 Allegro 启动页均为 16.6。

本批已刷新文件状态、检查 72 个 AVI 的 RIFF 顶层长度和尾部索引样本，并完成第 01 讲的逐秒画面阅读及第 02 讲的关键画面预读。两讲音频理解和本地 EDA 实操均未完成，完整学习完成仍为 0 讲。

## 新目录快照与结构检查

统计时间：2026-10-17T11:00:09+08:00 至 2026-10-17T11:00:09+08:00。

源目录：`D:\005study\72讲速成视频【Cadence Allegro16.6视频教程】完整版`。

| 检查 | 结果 |
| --- | --- |
| 主目录 | 72 个 AVI，01–72 均存在，共 4,640,900,608 字节 |
| 旧截短名目录 | 69 个 AVI，缺 15、17、18 |
| 与 09:35:59 视频快照比较 | 72 个文件大小一致 |
| 与 2026-10-17T10:58:07.331047+08:00 清单比较 | 72 个文件大小与 mtime_ns 均一致 |
| 逐文件检查前后 | 72 个文件的大小与修改时间未变化 |
| RIFF 检查 | 72 个文件声明长度均在文件范围内，顶层块边界可闭合，movi 与 idx1 均存在 |
| 尾部索引抽检 | 每个文件最后 32 个 idx1 项，合计 2304 项，引用的块头名称及长度均匹配 |
| RIFF 外尾部数据 | 每个文件另有 4–496 字节，长度与哈希已记入证据 |

这些是长度、结构和索引引用抽检；没有逐个完整解码 72 讲，也没有校验全部媒体载荷或下载来源清单，因此未确认全部文件播放完整或下载完成。附带目录样章 PDF 与二维码 JPG 仅登记存在，本批未阅读。

## 第 01 讲阅读方法与状态

原文件：`D:\005study\72讲速成视频【Cadence Allegro16.6视频教程】完整版\第01讲 Allegro常用组件介绍.avi`。

在 2026-10-17T11:03:36+08:00 至 2026-10-17T11:04:03+08:00 期间，顺序调用 Windows VfW 解码全部 1014 个声明视频帧，调用未返回解码错误。声明帧率 5 帧／秒，时长 202.8 秒，最后一帧时间 202.6 秒。每秒保存一帧，另补较大画面变化帧和末帧，共 234 张，组成 10 张接触表。

**实际查看范围：全部 10 张接触表中的 234 个缩略画面，并放大阅读 12 张代表帧。** 放大帧时间为 87.0、118.0、125.0、126.0、131.6、140.0、159.0、162.0、170.0、175.0、185.0、188.0 秒。全帧解码不等于逐帧人工观看；本轮完成的是逐秒抽样画面阅读与关键界面核对，音频仍未理解。

较大画面变化使用相邻帧缩小至 256×144 灰度图后的平均亮度差识别，阈值为 6.5／255，仅用来补选代表画面。

| 抽样时间段 | 实际画面 | 学习所得 |
| --- | --- | --- |
| 00:00–00:19 | 桌面三个快捷方式 | 区分 OrCAD Capture CIS、PCB Editor、Pad Designer 三个入口 |
| 00:19.2–01:18 | Word 教程说明页 | 这段主要为课程介绍，未提取联系信息用于学习 |
| 01:18.4–01:48 | 桌面及开始菜单 Cadence 项目 | 看见 Capture、PCB Editor 等软件入口；列表还包含其他工具 |
| 01:49–02:04 | Capture 的 Cadence Product Choices | 看到选择产品套件的对话框，列表含 OrCAD Capture CIS |
| 02:05–02:08 | Capture CIS 16.6 启动页及空白主窗口 | 确认 Capture 的实际启动界面；此处未演示原理图或符号创建 |
| 02:11.6–02:46 | Allegro 16.6 启动页、已有 PCB、File 菜单及 Product Choices | 区分 PCB 编辑窗口与产品选择窗口；已有板可见 Find、Visibility、层列表、走线和器件 |
| 02:49.4–03:08 | Pad Designer 的 unnamed.pad 参数页 | 看见 Parameters／Layers 标签，Mils、Drill/Slot hole、Hole type、Plating、Drill diameter、Offset 与 Top view |
| 03:08.4–03:22.6 | 回到桌面 | 课程画面结束前未见本地练习或封装成果验证 |

时间段按保存画面定位，边界不代表精确的讲解或操作起止点。

Pad Designer 空白页中的孔径 0.0 是当时参数状态，未形成可复用焊盘规格。本讲的价值是识别工具入口和对象界面；已有 PCB 文件、空白 Capture 窗口与 unnamed.pad 应分别记录，避免把它们视为同一种库文件操作。

代表证据：[Capture 启动页 125 秒](../evidence/video_batch2/lesson01_f0625.png)、[Allegro 启动页 131.6 秒](../evidence/video_batch2/lesson01_f0658.png)、[PCB 界面 140 秒](../evidence/video_batch2/lesson01_f0700.png)、[Pad Designer 170 秒](../evidence/video_batch2/lesson01_f0850.png)。

## 第 02 讲电源 IC 案例画面预读

原文件：`D:\005study\72讲速成视频【Cadence Allegro16.6视频教程】完整版\第02讲 以电源IC为例建立封装：一.avi`。

在 2026-10-17T11:05:11+08:00 至 2026-10-17T11:05:49+08:00 期间，顺序解码 1670 个声明视频帧，调用未返回解码错误。时长 334.0 秒。每 5 秒保存一帧，另补画面变化与末帧，共 153 张，组成 7 张接触表。

**实际查看范围：全部 7 张接触表中的 153 个缩略画面，并放大阅读 20、30、80、130、210、295、330 秒共 7 张代表帧。** 状态为关键画面预读，音频与实操未完成。

| 时间 | 画面观察 | 可衔接第 9 章的内容 |
| --- | --- | --- |
| 20 秒 | 打开 Richtek RT8059.pdf 首页 | 明确教程器件案例，后续尺寸记录应关联具体数据手册 |
| 30 秒 | PDF 第 10／10 页，封装外形及毫米／英寸尺寸表 | 先辨认机械尺寸、符号和单位，再进入焊盘编辑 |
| 80 秒 | Pad Designer 的 New Padstack 对话框 | Directory 与 Padstack Name 分别表示目录和焊盘名称 |
| 130 秒 | s1x0_6.pad 的 Layers，Single layer mode 已勾选 | 看见 BEGIN LAYER、SOLDERMASK_TOP、PASTEMASK_TOP 等层行及 Regular Pad、Thermal Relief、Anti Pad 列 |
| 210 秒 | Parameters 为 Millimeter，Single Mode 为 On | 记录案例改用了毫米，不能仅沿用第 01 讲的 Mils 画面状态 |
| 295 秒 | BEGIN LAYER 的矩形 Regular Pad，Width 1.0000、Height 0.6000 | 确认选中层与下方几何参数之间的对应关系 |
| 330 秒 | 层表已填入铜、阻焊和钢网相关矩形 | 不同层行可有不同外形尺寸；数值应逐层记录 |

330 秒可读的案例值如下，单位为毫米。这些值只记录该教程示范，尚未应用到当前元件库，也未验证工艺适用性。

| 层行 | 矩形宽 | 矩形高 |
| --- | --- | --- |
| BEGIN LAYER | 1.0000 | 0.6000 |
| SOLDERMASK_TOP | 1.1000 | 0.7000 |
| PASTEMASK_TOP | 1.0000 | 0.6000 |

代表证据：[封装外形 30 秒](../evidence/video_batch2/lesson02_f0150.png)、[New Padstack 80 秒](../evidence/video_batch2/lesson02_f0400.png)、[毫米参数页 210 秒](../evidence/video_batch2/lesson02_f1050.png)、[矩形焊盘 295 秒](../evidence/video_batch2/lesson02_f1475.png)、[层表 330 秒](../evidence/video_batch2/lesson02_f1650.png)。

## 音频状态与本机 ASR 检查

音频理解单独标为未完成。系统登记了 zh-CN 的 MS-2052-80-DESK 识别器，但现成 x64／x86 System.Speech 初始化均失败，听写语法未能加载；WinRT 枚举未返回可用语言。检查到的两个 Python 环境没有常见 ASR 包；仅在约定资料根目录按模型文件名规则检查，未找到候选模型。

注册信息未能转化为本次可用的离线转录能力，因此没有提取 WAV 或生成转录文本，也未调用麦克风、安装、下载或外传音频。错误链无法完全区分引擎缺失和当前会话的访问限制。详见 [ASR 检查证据](../evidence/video_batch2/asr_availability.json) 与 [简短说明](../evidence/video_batch2/asr_availability.txt)。

## 接续任务

与教材第 9 章对照，下一步核对焊盘类型、单位、单层模式以及铜、阻焊、钢网三个层行的设置，再继续第 03–05 讲案例。第 01、02 讲音频理解保持独立待办；第 02 讲还需补清文件保存、命名规则和参数依据，再在 17.2 的练习副本中验证。当前没有创建或修改任何元件库文件。

## 可追溯证据

- [本批目录和 RIFF 检查](../evidence/video_batch2/directory_snapshot.json)：保留精确统计时间、文件大小、mtime、结构与索引抽检。
- [第 01 讲逐帧记录](../evidence/video_batch2/lesson01_frames.json) 与 [第 02 讲逐帧记录](../evidence/video_batch2/lesson02_frames.json)：每帧时间、像素哈希、代表图和接触表路径。
- [实际阅读清单](../evidence/video_batch2/visual_review.json)：逐张接触表及放大帧列表、音频和实操状态。
- [本批核验结果](../evidence/video_batch2/batch2_validation.json)：909 处 JSON 路径引用、笔记证据链接、解码与阅读数量核对通过。
- [只读检查与解码脚本](../evidence/video_batch2/inspect_video_batch2.py) 与 [本记录生成脚本](../evidence/video_batch2/write_batch2_review.py)。

本批保存在 `01AIEDA/study_records`。旧 inventory 快照与第一批抽帧保留；迁移中断的暂存 PNG 已在新路径重新生成并核对，本批未重建旧记录目录。
