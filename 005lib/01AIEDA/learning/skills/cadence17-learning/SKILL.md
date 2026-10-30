---
name: cadence17-learning
description: Resume recorded Cadence 17.2 training, migrate the 01AIEDA learning library, and verify isolated replay. Use for tutorial-to-operation records and environment recovery; production PCB signoff requires its own engineering review.
---

# Cadence 17.2 学习与迁移

先读用户本次指定的学习根目录中的 EDA.md 开头计划和课程索引；未给新位置时从本技能所在路径向上查找同时含 EDA.md 和课程索引.md 的目录。不要假定盘符/用户名/安装路径永远不变。独立复制本技能时，根目录由用户或明确配置提供。

- 2026-10-23最新目录政策：01AIEDA保留通用步骤、方法、参数化工具及既有课程练习。实际工程的输入/副本、专用脚本、配置、中间物、日志、备份、案例记录和交付都放对应工程根，不写入学习库的staging/examples/logs。通用工具的项目参数与输出同样放工程内。原公共库、01env、实际工程的修改须属于当前授权任务。
- 开始先区分课程练习与真实工程，为当前任务指定绝对工作根；子任务遵守同一目录边界。本规则覆盖此前“所有产物统一放01AIEDA”的历史表述。LGA1700项目历史已迁至其工程根的conversion_archive/01AIEDA_20261023；学习侧只保留[通用转换方法](../../notes/ad_to_cadence_conversion_workflow.md)。
- 新环境先运行本技能的只读脚本 `scripts/preflight.py --root <学习根> --cadence-root <实际安装根>`；它只核文件与身份，不验证许可、GUI或原生执行。使用第60课 portable package 的 plan/run/verify 按其README复现，不能批量执行旧课程脚本。
- 先固定副本、来源SHA和成功判据，再执行最小操作，保存、独立重开并读回。任务进程按PID+创建时间+程序+父进程/任务路径识别；未知窗口/进程属于用户现场，不发送命令或结束它。
- 记录教程版本、PDF物理页/书页或视频实际观看区间，再核对图、单位、实际软件版本和输入。未提供/未看过的视频不填完成。扫描页视觉/OCR和文本提取分别记录。
- 跟随已有证据读相应笔记，不将“有教程”“脚本存在”“运行退出”“几何已核”“GUI已验”“整板通过”混为一项。迁移后重新验证每种接口。
- 课程当前进度和未接网/USB/整板DRC/制造/实物开放项以最新记录为准；本技能和第60课小操作都不授予整板放行。
- R/C显示统一按[Value与画布格式约定](../../notes/rc_value_display_conventions.md)执行：C为电容量/封装/额定电压/精度，R为阻值/封装/精度；单位用ASCII，区分mR与M。参数必须来自明确输入或用户明示策略，通用工具不内置示例电压/精度；显示策略与源规格分别保留。修改时Value与实际User_Value画布一致，并复核保存重开后的有效值、逐脚网络及有界器件定义变化。

用户的固定封装/层规范及已遇到的接口陷阱见 [操作边界与验收](references/operating-boundaries.md)。更换路径后以本机实查配置替代历史绝对路径，不修改历史封存证据来伪装新机成功。课程练习在对应课程目录保存机器可读结果、中文步骤、错误/恢复方法与SHA清单；真实工程的同类内容全部存该工程。学习侧只提炼通用方法并更新EDA开头和课程索引。

技能文件是下一次可读取的操作说明；保存它不等于训练模型权重，也不保证新会话自动加载或获得桌面/许可证连接。

可选--out只新建JSON报告并拒绝覆盖已有文件；不得把报告输出指向EDA、索引、源设计或历史证据。预检退出0只代表学习文件和固定fixture身份，不代表Cadence程序/许可/GUI就绪。

- 阻容排版按[水平方向及位号/Value左右规范](../../notes/capture_rc_horizontal_ref_value_layout_spec.md)：普通阻容尽量1脚左、2脚右，位号左侧、Value右侧；文字避让网络、引脚和导线，必要时协调局部导线调整并原生重开逐脚验收，不固定上方两格。
