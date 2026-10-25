---
name: cadence17-learning
description: Resume recorded Cadence 17.2 training, migrate the 01AIEDA learning library, and verify isolated replay. Use for tutorial-to-operation records and environment recovery; production PCB signoff requires its own engineering review.
---

# Cadence 17.2 学习与迁移

先读用户本次指定的学习根目录中的 EDA.md 开头计划和课程索引；未给新位置时从本技能所在路径向上查找同时含 EDA.md 和课程索引.md 的目录。不要假定盘符/用户名/安装路径永远不变。独立复制本技能时，根目录由用户或明确配置提供。

- 学习产物、临时中转、脚本、日志、备份均存用户指定01AIEDA内部。原公共库、01env、实际工程的修改须属于当前授权任务。
- 新环境先运行本技能的只读脚本 `scripts/preflight.py --root <学习根> --cadence-root <实际安装根>`；它只核文件与身份，不验证许可、GUI或原生执行。使用第60课 portable package 的 plan/run/verify 按其README复现，不能批量执行旧课程脚本。
- 先固定副本、来源SHA和成功判据，再执行最小操作，保存、独立重开并读回。任务进程按PID+创建时间+程序+父进程/任务路径识别；未知窗口/进程属于用户现场，不发送命令或结束它。
- 记录教程版本、PDF物理页/书页或视频实际观看区间，再核对图、单位、实际软件版本和输入。未提供/未看过的视频不填完成。扫描页视觉/OCR和文本提取分别记录。
- 跟随已有证据读相应笔记，不将“有教程”“脚本存在”“运行退出”“几何已核”“GUI已验”“整板通过”混为一项。迁移后重新验证每种接口。
- 课程当前进度和未接网/USB/整板DRC/制造/实物开放项以最新记录为准；本技能和第60课小操作都不授予整板放行。

用户的固定封装/层规范及已遇到的接口陷阱见 [操作边界与验收](references/operating-boundaries.md)。更换路径后以本机实查配置替代历史绝对路径，不修改历史封存证据来伪装新机成功。完成后在新课目录保存机器可读结果、中文步骤、错误/恢复方法与SHA清单，并更新EDA开头和课程索引。

技能文件是下一次可读取的操作说明；保存它不等于训练模型权重，也不保证新会话自动加载或获得桌面/许可证连接。

可选--out只新建JSON报告并拒绝覆盖已有文件；不得把报告输出指向EDA、索引、源设计或历史证据。预检退出0只代表学习文件和固定fixture身份，不代表Cadence程序/许可/GUI就绪。
