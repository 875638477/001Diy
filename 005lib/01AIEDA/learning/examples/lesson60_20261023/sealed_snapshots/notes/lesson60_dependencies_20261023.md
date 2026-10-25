# 第60课：依赖盘点、资料迁移与能力边界

日期：2026-10-23，Asia/Shanghai。异常关机后先做只读盘点；本代理未改旧课/公共库/01env，未启动Cadence、GUI、bridge或watcher。小操作复现及课程主验收由主记录汇总。

## 本轮实际结果

明确解释器为 `D:\001DIY\005lib\01AIEDA\learning\tools\python_3_14_0\python.exe`，实测Python **3.14.0 Windows x64**。PyMuPDF **1.28.2**、numpy **2.5.4**、shapely **2.2.0**、Gerbonara **1.6.3**、rtree **1.4.1**、click **8.5.0**均实际import成功；未全局安装。已知tools/HI/JK路径没有yaml，import失败；主任务之后若新增局部PyYAML，按其新记录。

PATH的python指向WindowsApps候选入口，不凭名字当可用解释器。ffmpeg/ffprobe/Tesseract/pdftotext/pdftoppm/git在PATH均未发现；未全盘搜索，不断言全机未装。文本PDF可用PyMuPDF，扫描页可渲染后视觉复核，可选OCR/视频工具按任务安装。

九个官方程序文件及七个手册/API入口存在；Capture数据库DLL存在，未加载。Allegro/Capture文件元数据为17.2-2016，不能据此推导S045；S045是既有原生日志历史证据，新机需新日志重核。见[原始快照](../examples/lesson60_20261023/inventory/environment_snapshot.json)。本代理GUI未测，历史native pipe失败不是本轮新失败或永久结论；主任务本轮探测应另列证据。

## 迁移分类

| 类型 | 方式 | 新机验收 |
| --- | --- | --- |
| 规范/索引/工程理由/失败记录 | 保持01AIEDA相对树复制 | 新会话先读入口，区分历史/当前/待验，UTF-8可读 |
| 自有BRD、DSN/OPJ、PAD/DRA/PSM、OLB、PST、规格 | 精确源版本与完整依赖一起复制 | 身份、库关联、保存重开对象 |
| 外部01env/公共库 | 留定位，新机核版本路径 | 不覆盖新环境，核层序、光绘、o/O快捷键 |
| 源码/日志/备份/manifest | 保留成功和失败证据 | 查绝对根、queue、输出路径和进程归属 |
| 软件/ABI依赖 | 新机合法安装兼容版本 | 位数/补丁/import和真实小操作 |
| 教程/PDF/视频 | 留合法来源、版本、页码/时间点、SHA | OCR/字幕回看原图；未读不记已学 |

不打包Cadence安装程序、许可文件或教程全本；本次未复制修改外部库/01env。旧wheel清单仅锁版本与来源，ABI/平台需目标机重新验证。完整[迁移清单与故障排查](../examples/lesson60_20261023/inventory/migration_checklist.json)。

## 旧脚本与配置

抽查十个代表入口，见[历史脚本可迁移性](../examples/lesson60_20261023/inventory/historical_script_portability.json)。launch_cadence17、c11 SDK/runtime、de_native_cli、J/K CAM脚本及bridge含固定根；capture_request虽用__file__找根，仍绑定旧capture_C_20261019队列。旧ready不能证明新会话；旧J/K审核脚本重跑可能覆盖已封报告字段。仅十个入口抽查，不是所有历史代码审计。

保留旧源码，另写配置副本，解析记录根/安装根/库根并约束路径，用新日志与输出。自己的进程关联本次PID+创建时间+exe+命令/目标；旧PID、SKILL DBID、Capture Dbo对象、ready或旧请求ID不可当新会话。用户已开CAD不作为实验入口。

[环境示例](../examples/lesson60_20261023/inventory/environment_config.example.json)默认executionEnabled=false，是待配置数据；[schema](../examples/lesson60_20261023/inventory/environment_config.schema.json)只检字段形状，不证明路径/许可/实际启动。私有pcbenv按已验方法source官方TELENV并显式本机PSM/PAD，不改全局。

## 知识与执行能力

普通Tcl成功不代表Capture Dbo存在。官方SDK正确初始化后可以处理隔离DSN/OLB，但活动文档、选中对象、菜单、ERC/打印预览需实际GUI另测。旧SDK通过是历史证据，不填成本轮GUI通过。SKILL也需真实软件/数据库/会话，数据库句柄跨重开要重查。返回0仍需完成标记、真实文件、保存重开及对象几何。一个小操作通过不等于交互布线全部掌握或整板可发布。

迁移文件让下一次协作读回方法、工程前提、失败与限制。**可携带载体是本地文件**，不表示模型永久被训练，不证明自动云同步，也不保证新机执行能力自动继承；目标机依赖与现场复现仍要做。

## 资料索引与异常恢复

[来源定位索引](../examples/lesson60_20261023/inventory/source_reference_index.json)保留本机官方API及QMI/DE/J/K入口。QMI历史Rev.A SHA/页码只是引用，本轮未访问/复制外部原PDF。learning/sources七份制造商资料不等于教程全本；本代理没核验《Cadence 17.2电路设计与仿真从入门到精通》的本轮副本，也没收到视频，不宣称已下载/读完或学视频。新索引需标题/作者/版本/合法定位/SHA、实际PDF页与印刷页/视频起止、目的参数、实际观察执行、读回与状态；OCR回看单位、脚号、层名和版本。

异常关机后先核输入身份/开放项，再新建隔离目录、重建路径和小操作，保存后新进程重开核目标及目标外不变，失败留证回退。旧完成标记不证明当前会话有效；不删归属不明锁/临时文件，不结束用户进程。同机改目录标**同机路径迁移**，真实另一台机未执行前保持未测。PCB/DFM/实测开放项不因迁移变通过。

可重跑[probe_dependencies.py](../examples/lesson60_20261023/inventory/probe_dependencies.py)，用明确Python，--cadence-root为本机安装根，--output为本课inventory内全新JSON；拒绝覆盖旧观察。仅import、路径/命令定位，不启动EDA、不导出环境/许可、不全盘搜或重哈希旧大组。

```powershell
& 'D:\001DIY\005lib\01AIEDA\learning\tools\python_3_14_0\python.exe' -B -X utf8 'D:\001DIY\005lib\01AIEDA\learning\examples\lesson60_20261023\inventory\probe_dependencies.py' --cadence-root 'C:\Program0\Cadence\SPB172' --output 'D:\001DIY\005lib\01AIEDA\learning\examples\lesson60_20261023\inventory\environment_snapshot_NEW.json'
```

本代理产物：环境快照、只读盘点脚本、配置schema/示例、迁移清单、脚本抽查、来源索引及本笔记。未宣称全套新机能力或完整PCB验收。
