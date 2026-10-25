# 第60课迁移与恢复操作手册

这是交接说明。实际证据入口：[第60课完整笔记](../../notes/lesson60_20261023.md)。本机两个目录复现已验；另一台物理电脑仍需按以下步骤执行，不预填成功。

## 搬运资料

完整知识备份复制整个01AIEDA，保留learning、skills、logs、backups、源工程和清单。按[inventory清单](inventory/migration_checklist.json)携带所用外部PAD/PSM/OLB库、原教材/视频并重新绑定来源SHA。01env/drill*.txt和快捷键是有版本的环境依赖；不可在新板上盲目重放旧脚本。

小包eda60-portable-kit.zip仅用于最小操作练习：最终原生代码+自有板fixture+示例配置、本地技能源和记录模板。它不是完整知识备份，不含Cadence/许可、Python安装、第三方原教材或视频。

## 目标机准备与执行

1. 在目标机确认Windows、可用Python（本轮实测3.14）、合法Cadence17.2安装和可用产品/许可。不要把源机许可文件、账户凭据或环境秘密装入压缩包。Python的完整exe路径优先，WindowsApps占位入口不能当已安装解释器。
2. 用较短ASCII目录解包到目标机01AIEDA内，例如01AIEDA/L60。当前原生包只验证ASCII路径（支持空格），中文路径未验而早拒绝；经验命令长度500门槛不是Cadence官方极限。
3. 复制replay/config.example.json为replay/config.local.json，填写本机cadence_root、合法product和超时。此配置只供原生包使用；inventory环境schema是完整迁移清单，二者用途不同。
4. 使用目标机Python完整路径和-I执行，先probe、plan，再run、verify。替换下面尖括号中的实际路径，不要运行旧课程初始化脚本。

```powershell
& "<Python完整路径>/python.exe" -I "<包目录>/replay/replay.py" probe
& "<Python完整路径>/python.exe" -I "<包目录>/replay/replay.py" plan --tag m01
& "<Python完整路径>/python.exe" -I "<包目录>/replay/replay.py" run --tag m01
& "<Python完整路径>/python.exe" -I "<包目录>/replay/replay.py" verify --tag m01
```

plan不启动Cadence；probe只核静态输入和进程身份。run在新副本实际操作两次原生进程；已有tag拒绝覆盖。超时仅可处理具有完整创建时间/父进程/程序/任务路径证据的本任务子进程，用户窗口保持由用户控制。系统和合法许可环境仍继承，不声称整个Windows环境完全隔离，也不输出其值。

## 成功判据

实际查看新logs和verification：新输出BRD存在；fresh唯一L60_REPLAY位于指定class、(4,4)mm、0°；80件/272逻辑pin/69net/四层/mm；实际932段=750手工+182thermal；非空铜、via、pins/poses/层/网络几何三阶段相同；源fixture/input SHA未变；build与fresh退出和进程身份正确。42项报告是辅助，须核原始行数，不把0项或陈旧ready/result当通过。

新电脑执行成功后，才新增REPRODUCED_NEW_PC记录，附本机版本、配置（不含秘密）、source manifest、命令、日志和fresh证据；不要修改旧机封存清单或把旧PASS文件改日期。GUI连接、Capture Tcl/SDK、原理图ERC、整板DRC/SI/PI/EMI及实物分别验证。

## 关机或失败后恢复

先确认进程身份与输入SHA；保留stdout/stderr/journal、failure.json和工作副本。不得仅见lck或旧PID就删除锁/结束进程；PID可能复用。没保存的界面操作不能由文件存在推断已恢复。本课异常关机时L60尚未落盘，恢复记录没有伪造其执行进度。

修正配置/脚本后用新tag、新结果文件，不覆盖失败。较长路径启动前AV只作观察，先plan检查并改短路径；持续失败明确记目标机未通过，不用软件退出0或最后一张视频帧冒充验收。

活动EDA/索引会继续更新；历史依赖使用课内快照和SHA。PyYAML只用于本课技能源校验，最小原生包和只读preflight均不依赖它。本地技能加载方式见[官方文档](https://learn.chatgpt.com/docs/build-skills)，本轮未改全局技能/账户配置。
