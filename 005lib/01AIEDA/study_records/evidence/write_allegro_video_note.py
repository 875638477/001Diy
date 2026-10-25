"""Create the local lesson index, including manually reviewed frame observations."""
from pathlib import Path
import json
import re

root = Path(r"D:\001DIY\005lib\01AIEDA\study_records")
data = json.loads((root / "evidence" / "video_inventory.json").read_text(encoding="utf-8"))
sources = {source["source_key"]: source for source in data["source_directories"]}
old = sources["short_named"]
new = sources["complete_named"]


def clock(seconds):
    seconds = round(seconds, 1)
    hours, seconds = divmod(seconds, 3600)
    minutes, seconds = divmod(seconds, 60)
    if hours:
        return f"{int(hours)}:{int(minutes):02d}:{seconds:04.1f}"
    return f"{int(minutes)}:{seconds:04.1f}"


def group(number):
    for numbers, label in [
        ({1}, "软件组件"), (set(range(2, 9)), "封装制作"),
        (set(range(9, 14)), "基础操作"), ({14, 18}, "原理图网络表"),
        ({15}, "原理图交互"), ({16, 17, 19}, "工程设置与板框层叠"), (set(range(20, 37)), "放置与配置"),
        ({37, 38, 39}, "封装复用与过孔"), ({40}, "帮助文档"),
        (set(range(41, 46)), "约束管理"), (set(range(46, 56)), "布线与过孔"),
        ({56}, "偏好设置"), (set(range(57, 65)), "铜皮"),
        ({65}, "丝印"), (set(range(66, 71)), "制造输出"),
        ({71}, "文件保护"), ({72}, "课程说明")]:
        if number in numbers:
            return label
    return "待归类"


text = f"""# Allegro 16.6 视频清点与元件库学习索引

统计时间：{data['snapshot_started_at_local']} 至 {data['snapshot_finished_at_local']}，Asia/Shanghai。学习方向：优先 Cadence／Allegro，与当前元件库工作衔接；单片机暂缓。用户已说明 PDF 与本地工程采用 17.2，视频为 16.6，主流程通用；具体菜单与字段仍以本地 17.2 验证为准。

旧副本已被用户改为截短目录名，仍有 69 讲，缺第 15、17、18 讲。用户正在带“完整版”名称的新目录下载资料；本次最新快照中存在 {new['avi_count']} 个 AVI，讲号 01–72 均已出现。**这只说明统计时文件存在及头部可读，未确认下载完成或全片完整。**

按讲号建立了 72 讲主题索引，未复制或合并视频文件。**完整学习完成 0 讲；旧副本第一讲为五个时间点的画面抽样，其余 71 个讲号仅建立索引。**

## 资料范围与读取结果

旧副本：`{old['path']}`。

新下载目录：`{new['path']}`。

新下载目录还附有 16.6 目录样章 PDF 和二维码 JPG。样章待读；二维码仅登记文件存在，内容未读。附带资料不计入本次视频学习进度。

| 目录 | 此次存在文件 | 统计时未出现的讲号 | 头部可读 | 字节数 |
| --- | --- | --- | --- | --- |
| 旧副本 | {old['avi_count']} | 15、17、18 | {old['header_readable_count']} | {old['total_bytes']:,} |
| 新下载目录 | {new['avi_count']} | 无 | {new['header_readable_count']} | {new['total_bytes']:,} |

本轮较早时，新目录曾统计到 47 个 AVI，随后增长为 72 个；47 个时暂未出现第 42、49–72 讲。较早的这两次清点未独立采集具体时分，作为本轮历史快照保留，不把下载过程中的暂未出现视为固定缺失。

| 项目 | 结果 |
| --- | --- |
| 两目录文件数 | {data['avi_count']} 个 AVI，按讲号唯一 {data['unique_lesson_count']} 讲 |
| 总大小 | {data['total_bytes']:,} 字节，约 {data['total_bytes'] / 1024**3:.2f} GiB |
| 按讲号选择一个文件的声明总时长 | {clock(data['declared_total_duration_seconds'])}，约 5 小时 12 分钟 |
| 旧副本声明总时长 | {clock(old['declared_total_duration_seconds'])} |
| 选用规则 | 索引优先指向旧副本，旧副本缺的 15、17、18 讲指向新目录的当前文件 |
| 字幕 | 两目录及子目录未发现 SRT、VTT、ASS、SSA |
| AVI 头部 | {data['header_readable_count']} 个均可读取；视频压缩字段均为 CRAM |
| 第一讲解码 | Windows 自带 avifil32／VfW 成功读取 5 个画面 |

时长由 AVI 视频流的 `length × scale ÷ rate` 计算，未逐个完整播放校验。全部头部可读只说明元数据可读取，不能代替完整视频和音频的完整性验证。第一讲画面为 1364×768，视频流声明 5 帧／秒，时长 {clock(data['preferred_files'][0]['avi_header']['duration_seconds'])}。两目录同号文件的名称、大小和声明时长比较保存在 JSON 中，未做全文件哈希或内容一致性认证。

## 元件库学习顺序

按当前元件库目标，先建立软件和对象的对应关系，再学习封装制作与复用。下面是根据课程文件名安排的学习路线，操作细节需在后续阅读视频和本地文档后核实。

1. **入口与基础：01、09、10、11。** 先识别 Capture、PCB Editor、Pad Designer，并理解操作界面以及 Class／Subclass。
2. **封装制作：02–05，再 06–08。** 电源 IC 封装案例在前，LQFP 向导及毫米／mil 相关主题在后。结合现有库选取一个实际器件记录尺寸来源、焊盘、图形与输出文件。
3. **与原理图和板级连接：14、20。** 对照元件名称、封装调用和网络表错误，确认库文件能被设计调用。
4. **已有封装的维护：37、38。** 重点学习导出、更新封装的流程和影响；后续在副本中验证。
5. **焊盘和过孔：39，必要时回看 02–08。** 分别记录元件焊盘和过孔的用途及设置，避免只凭文件名混用。
6. **查错与日常效率：23、31、34、40、56。** 快捷键、对象查找、自动保存、帮助文档与偏好设置。

约束、差分、等长、铜皮与制造输出属于后续 PCB 流程，可在核心元件库路线完成后展开。第 65 讲丝印调整与第 66–70 讲制造输出，也可在检查库中丝印和装配信息时回查。

## 第一讲实际画面记录

抽帧源：`{data['lesson01_sample_source']['path']}`。确认用户重命名信息后，已从这个旧副本精确路径重新解码保存以下画面，并逐张检查；未读取音频或连续观看完整课程。

| 时间 | 实际可见内容 | 证据 |
| --- | --- | --- |
| 00:00 | 桌面及两个 Word 说明文件快捷方式，尚未进入操作界面。 | [画面](../evidence/allegro_lesson01_000s.png) |
| 00:30 | Word 中显示教程说明和联系信息，未见封装操作。 | [画面](../evidence/allegro_lesson01_030s.png) |
| 01:00 | 仍显示课程说明页。 | [画面](../evidence/allegro_lesson01_060s.png) |
| 02:00 | Cadence Product Choices 产品选择窗口，列表包括 OrCAD Capture CIS 等项目；背景桌面可见 OrCAD Capture CIS、PCB Editor、Pad Designer 快捷方式。 | [画面](../evidence/allegro_lesson01_120s.png) |
| 03:00 | Pad Designer 窗口，标题含 `unnamed.pad`；可见 Parameters、Layers 标签，Units 为 Mils，以及 Drill/Slot hole、Hole type、Plating、Drill diameter、Offset 等字段。 | [画面](../evidence/allegro_lesson01_180s.png) |

本次可确认：本讲画面展示了这三个软件入口，并包含 Pad Designer 的参数界面。接续学习时应记录各工具与原理图符号、焊盘、封装对象的准确对应关系，以及当前安装版本和教程界面的差异。画面抽样不能证明这部分讲解的全部内容。

## 逐讲主题索引

标题来自文件名。时长来自 AVI 头部。“旧”代表旧副本，“新”代表新下载目录的瞬时存在文件。状态“画面抽样”只用于旧副本第一讲；“仅索引”表示未进行内容学习。

| 讲号 | 主题 | 分类 | 时长 | 来源 | 状态 |
| --- | --- | --- | --- | --- | --- |
"""
for entry in data["preferred_files"]:
    number = entry["lesson_number"]
    title = re.sub(r"^第\d+讲\s*", "", Path(entry["name"]).stem)
    duration = clock(entry["avi_header"]["duration_seconds"]) if entry["header_readable"] else "不可读"
    status = "画面抽样" if number == 1 and data.get("lesson01_sample_frames") else "仅索引"
    source_label = "旧" if entry["source_key"] == "short_named" else "新"
    text += f"| {number:02d} | {title} | {group(number)} | {duration} | {source_label} | {status} |\n"

text += """
## 接续任务与交互节点

接续主线为教材第 9 章与视频第 01 讲补齐。先补第 01 讲的连续画面学习，并单独记录音频是否实际听取、听取时间段和理解内容，再进入第 02–05 讲电源 IC 封装案例，结合已有元件库选择练习对象。每讲记录原文件、实际检查时间段、观察到的菜单／字段、可复用步骤、待验证问题、对应库文件和实操验证结果；画面学习、音频理解与实操验证分别记录，达到相应条件后才更新状态。

建议在三个节点向用户汇报：完成第一讲软件对象关系梳理；完成第 02–05 讲并形成一个封装案例；完成第 37–38 讲并验证封装导出／更新。新目录下载过程中只记录瞬时文件状态；用户确认下载完成后，才安排一次完整性复查。

## 证据与复现

- [机器可读清单](../evidence/video_inventory.json)：每个文件的路径、字节数、AVI 头部、时长与读取状态。
- [读取脚本](../evidence/inspect_allegro_videos.py)：Python 标准库读取 AVI 头部，Windows avifil32 读取第一讲抽样帧，Pillow 保存 PNG。
- [索引生成脚本](../evidence/write_allegro_video_note.py)：生成本记录中的逐讲表格，含本次逐张检查后的画面观察。

环境中 PATH 及检查过的常见 Program Files、WinGet 目录未找到 ffmpeg／ffprobe；当前 Python 未提供 cv2、av、imageio。已用 Windows 自带视频接口完成本次读帧，未安装软件、未启动视频或 EDA 图形界面，未修改源资料。
"""
output = root / "notes" / "allegro_video_inventory.md"
output.write_text(text, encoding="utf-8")
print(f"Wrote {output}, {len(data['preferred_files'])} unique lessons indexed")
