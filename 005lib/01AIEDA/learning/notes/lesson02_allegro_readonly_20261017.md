# 第 2 课：Allegro 17.2 只读数据库查询与退出
日期：2026-10-17（Asia/Shanghai）
状态：Allegro 内部 SKILL 查询和正常退出已实测；桌面控制、Capture 内部 Tcl、IPC 桥接尚未验证成功。

## 目的与前提
先确认能准确读取设计对象、单位、层叠及检查状态，后续再练习符号/封装、布局和走线。读取到器件数或网络数，不代表已掌握布线或已验证 SI/PI/EMI。

实际软件：C:/Program0/Cadence/SPB172/tools/bin/allegro.exe。
命令 `allegro.exe -version` 返回 `Tool: allegro 17.2-S045`；运行日志进一步显示 Windows SPB 64-bit Edition。
本次使用 `-product Allegro_performance` 启动成功。这证明本次只读会话可启动和执行 SKILL，不推断其他产品/选件也可用。

## 已验证的启动与退出流程
1. 将安装自带示例板复制到学习目录。显式指定板副本，不依赖“上次打开的板”。
2. 为运行创建独立目录，并仅在启动子进程的环境中设置 ALLEGRO_PCBENV 到该目录下 pcbenv。未主动修改全局 HOME 或用户启动文件。
3. 使用官方参数：`-product Allegro_performance -safe -readonly -nographic -s <scr路径> -p <运行目录> <板副本.brd>`。
4. 成功脚本是 learning/scripts/lesson02_readonly_quit.scr，其主要内容如下：

```text
set NOCONFIRM
skill errset(load("D:/001DIY/005lib/01AIEDA/learning/scripts/lesson02_probe_quit.il") t)
quit
fillin "yes"
```

5. 同时核对：报告包含 COMPLETE、进程自行退出、journal 正常结束、板文件哈希未变。不要只看脚本调用或进程退出码。
6. 本次 journal 在 quit 后正常结束，fillin 行未执行到；退出组合依据 Cadence 安装自带 mgx 脚本。NOCONFIRM 仅用于本次隔离只读诊断会话，不作为正常交互编辑的默认设置。

本次使用 -safe 是为了排除用户/site 启动配置，不是日常生产配置。-readonly 禁止保存板，但运行仍会产生日志、journal 和锁文件。-nographic 是官方所称 pseudo non-graphic mode，不保证所有命令都能无人值守执行。

## 只读查询方法与实际结果
来源：安装自带 BRDExtractor/demo_ver_17p2.brd，686180 字节。SHA256：
F2AC54090DEE0E67E2A734752C66AA6CFEFE9C604456324B889C79D9BFA77CB0。

| 查询 | 方法 | 本次结果 |
| --- | --- | --- |
| 活动设计名 | axlCurrentDesign() | demo_ver_17p2 |
| 根设计对象 | axlDBGetDesign() | 返回有效设计对象 |
| 单位与精度 | axlDBGetDesignUnits() | ("mils" 0) |
| 器件、网络 | length(design->components/nets) | 57 个器件、95 个网络 |
| symbol 实例 | length(design->symbols) | 59 个；不能直接视作器件数 |
| 设计图形包围框 | design->bBox | ((-4000 -3000) (7000 5500))，单位 mil |
| DRC 存量和状态 | design->drcs、design->drcState | 0 条、nil（不是最新检查状态） |
| stackup 名称 | axlXSectionGet(nil 'stackups) | PRIMARY |
| 完整层叠条目 | axlXSectionGet(nil 'all) | 13 个，含空气、介质与铜层 |
| 铜层 | 逐项读取 ->conductor 并计数 | 6 个 |

铜层从上到下：TOP / GND / IS3 / IS4 / VCC / BOTTOM。
示例中铜厚字段为 1.2 mil，相邻介质厚度字段为 8 mil，材料字段为 COPPER / FR-4；这是示例数据库内容，不是为用户板选择的板厂层叠。

本课的几个关键区分：
- 单位必须先读。("mils" 0) 中的 0 是坐标精度，不是层数；后续位置、线宽、间距均须按实际设计单位解释。
- 完整层叠条目数不等于铜层数。'count 包含其他条目；当前通过 conductor 属性计数。
- design->bBox 是设计图形范围，不是制造板框。原始报告字段写作 board_bbox，名称不够准确；保存脚本已改为 design_bbox，原始报告保持不动。要取得实际板框应另查 designOutline 及相应几何，不能拿这里的 11000×8500 mil 作为板子尺寸。
- 0 条存储 DRC 且 drcState=nil，不能宣称 DRC 通过。此课未重新运行 DRC，也未审查电气质量。
- GND/VCC 是层名；层名与 PLANE 类型不能证明实际铜区连续、网络正确或没有缝隙。后续检查回流路径必须读取/查看实际铜与走线。
- 不把本次 6 层示例当作两层/四层布局方案；两层与四层练习后续单独建立。

## 失败尝试与纠正
第一次：lesson02_readonly.scr，报告 COMPLETE，但末尾 core SKILL `exit(0)` 没有使进程自行退出。已核对 PID 1612 与启动时间后，仅结束该测试进程。原因未确定，不能当作可靠退出入口。
第二次：lesson02_readonly_quit.scr，PID 22116，报告 COMPLETE，约 5 秒正常退出，journal 有 Journal end，没有残留运行进程或该次板锁。PowerShell Start-Process 的 ExitCode 读取为空，未记录为 exit code 0；验收依据报告、进程状态、journal 和哈希。
两次同时改变了退出组合和换行；官方自带 mgx 脚本也使用 LF，因此不能把首次失败归因于 LF。
本机旧用户指南将 -nographic 写作 UNIX only，而安装自带 batchhelp/Commands 说明为 pseudo non-graphic mode。本次 Windows 实测成功，结论限定为上述参数及只读探针。

## 产物与可复核证据
- learning/scripts/lesson02_probe_quit.il、lesson02_readonly_quit.scr：成功入口。脚本中的报告路径是本课固定路径，复现前应建立新运行目录并调整输出路径，保留既有证据。
- learning/logs/lesson02_readonly_20261017/：第一次启动参数、原始查询报告及锁文件存档。
- learning/logs/lesson02_readonly_quit_20261017/：成功运行的 launch.json、probe.txt、allegro.jrl、stdout/stderr 及板副本。
- learning/logs/lesson02_result_20261017.json：汇总状态、来源和哈希。
- backups/lesson02_20261017/：本课更新前的主记录、环境记录和脚本备份及变更清单。

## 官方出处
均为本机 Cadence 17.2 安装自带资料：
- [启动参数](C:/Program0/Cadence/SPB172/share/pcb/batchhelp/allegro.txt)：-s、-p、-product、-readonly、-nographic。
- [诊断安全模式](C:/Program0/Cadence/SPB172/share/pcb/batchhelp/safe.txt)：禁用启动定制及仅用于诊断的限制。
- [安装自带退出脚本](C:/Program0/Cadence/SPB172/share/pcb/text/script/mgx_restore.scr)：set NOCONFIRM、quit、fillin "yes"。
- [数据库读取](C:/Program0/Cadence/SPB172/doc/algroskill/07dbaccs.html)：axlDBGetDesign、axlDBGetDesignUnits。
- [设计名](C:/Program0/Cadence/SPB172/doc/algroskill/14dsnctl.html)：axlCurrentDesign。
- [设计和图形属性](C:/Program0/Cadence/SPB172/doc/algroskill/02dbdesc.html)：components、nets、symbols、drcState、bBox。
- [完整层叠](C:/Program0/Cadence/SPB172/doc/algroskill/04parmgt.html)：axlXSectionGet；旧 paramLayerGroup:ETCH 方法的限制。
- [quit 命令](C:/Program0/Cadence/SPB172/doc/qcoms/qchap.html)：结束会话及确认。
- [exit 命令](C:/Program0/Cadence/SPB172/doc/ecoms/echap.html)：裸 Allegro exit 会保存板，不能与 core SKILL exit(0) 混用。

下一课：继续 P1 的器件—封装—引脚—网络与几何读取，接入 P2 的焊盘/封装核对。先建立可审查的器件与引脚对应关系，再进入位置修改；Capture 内部 Tcl 和桌面通道继续分别验证。
