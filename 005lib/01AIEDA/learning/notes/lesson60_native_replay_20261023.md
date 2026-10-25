# 第 60 课：可迁移最小原生操作复现（2026-10-23）

本记录对应用户“异常关机后继续学习”的第 60 课。实际完成的是：在本机两个不同目录中，使用同一套最终 Python/SKILL 源码，对一份四层训练板副本添加一条文字、另名保存，再由另一个 Cadence 原生进程只读重开核验。第二个目录包含空格，初始没有任何运行输出。两处正式结果均为 **42/42 PASS**。这是同一台计算机的路径迁移验证；未声称已经在第二台物理计算机重装环境并执行，也未展示 GUI 菜单操作能力。

## 1. 原件、任务副本与动作边界

输入来自已存在的 J/K 新四层训练板，SHA256：

`471176A9B25BA8DEF9F117AEFB1E9220CBCBEBBAC5191BCBC6E228F52831F3F9`

[最小包目录说明](../examples/lesson60_20261023/package/README.md)与[机器可读独审接口](../examples/lesson60_20261023/native/independent_review_interface.json)是复现入口。包内 fixture/training_4L.brd 为复制件；运行时再复制到 runs/<tag>/work/INPUT_COPY.brd。原始 J/K 板与包内 fixture 的 SHA 均保持不变。

唯一新增对象为 `L60_REPLAY`，在 `BOARD GEOMETRY/ASSEMBLY_NOTES`，坐标 **(4,4) mm**，旋转 **0°**，居中。这是板级教学注释，不是器件位号/Value，也不改变用户要求的封装三文字层与器件中心原点规范。输出仅为另名 `L60_replayed.brd`；不调整铜、过孔、器件、层叠、规则或 DRC，也不运行自动布线。

层名仍为 **TOP-L2-L3-BOTTOM**，原有层功能为 TOP 器件与信号、L2 公共 GND、L3 V3V3 电源、BOTTOM 信号。本课的几何保持证据不是对该训练板的 SI/PI/EMI、DRC 或制造放行结论。

## 2. 正式验收的两处运行

仅以下两处计入最终完成，早期记录均保留为历史：

| 正式位置（相对本课目录） | 状态 | 实际子进程 |
| --- | --- | --- |
| package/runs/final03 | 42/42 PASS | build PID 及 fresh PID 见各自 process.json |
| native/R Space/runs/move01 | 42/42 PASS | 全新目标目录、独立输入与两次原生执行 |

证据：[原路径正式报告](../examples/lesson60_20261023/package/runs/final03/verification.json)、[含空格路径正式报告](<../examples/lesson60_20261023/native/R Space/runs/move01/verification.json>)、[最终汇总](../examples/lesson60_20261023/native/native_replay_summary.json)。

每处在 before、memory、fresh 三阶段均检查：

- 80 个逻辑元件、272 个逻辑引脚、69 个网络；实际物理引脚为 278 个，含机械孔。
- 物理导体层顺序 TOP-L2-L3-BOTTOM，单位 millimeters。
- source 不存在同名标记；memory 和 fresh 均只有一个标记，文本、层、(4,4) mm 与 0° 均准确。
- 实际路径子段 **932**，其中 **750 手工段、182 自动生成热连接段**；不是仅看父 path 的数量。
- 非空几何记录还包含 21 条实际铜区记录、150 个过孔、元件姿态及引脚/网络；三个阶段完整排序记录 SHA 一致。
- 两处运行的几何记录 SHA 也相同：

`AE038C95DF6CC1CDDE9A91029DA01B2C37068A28A85365DE78AA644AC57D55DC`

两个输出 BRD 的二进制 SHA 不同是实际观察；另名保存、时间与内部元数据可不同，因此不把跨目录二进制完全一致当成验收条件。验收依靠源文件不变、实际对象与几何读回一致。

## 3. 包结构和迁移方法

包的核心只有 Python 标准库启动器、一个最小 SKILL 文件、训练 BRD、说明、配置样例与 SHA 清单。没有复制 Cadence 可执行程序、许可证、用户全局 env、公共库或账号配置。

- `replay.py`：相对自身目录定位，不依赖当前工作目录，也没有硬编码 01AIEDA 路径。
- `scripts/replay.il`：逻辑元件/引脚、层序与实际铜/路径读回，新增文字、事务回滚与另存。
- `fixture/training_4L.brd`：固定 SHA 的训练源。
- `config.example.json`：安装根目录、product 与超时配置样例。
- `config.local.json`：每台机器自行配置，不纳入可迁移源码清单。
- `package_manifest.json`：保护核心源码、说明、配置样例与 fixture；不接受不明原因的散列差异。

目标计算机需要 Windows、Python 3.10 或更高版本（本次实测 3.14.0）、合法安装并可使用许可证的 Cadence 17.2。安装位置写在 config.local.json 的 cadence_root，不能假定另一台电脑的 C 盘软件路径相同。该小操作使用 BRD 内已嵌入符号和焊盘，不刷新公共库；其他课程如需载入新封装/焊盘，必须另外迁移对应 PAD/PSM/DRA 并明确配置依赖。

从任意工作目录执行以下四个动作，路径含空格时必须加引号。Python 的 **-I 必须保留**：

```powershell
python -I "PATH TO PACKAGE/replay.py" probe
python -I "PATH TO PACKAGE/replay.py" plan --tag migration01
python -I "PATH TO PACKAGE/replay.py" run --tag migration01
python -I "PATH TO PACKAGE/replay.py" verify --tag migration01
```

probe 仅证明静态文件、散列、安装资源和进程身份条件；不能把它当成许可证可用或实际操作成功。plan 不启动 Cadence。run 才会实际创建两个串行原生进程；verify 重新核查已生成的非空证据。相同 tag 拒绝覆盖，已实测反例：[重复 tag 拒绝记录](../examples/lesson60_20261023/native/negative_refuse_existing_run.json)。失败后保留输入、脚本、stdout、stderr、journal、process.json 和 failure.json，再用新 tag 重做。

## 4. 可迁移范围与当前限制

最终源码的 Python 路径、SKILL 路径和 Cadence 安装路径 **仅支持 ASCII 字符**，包含空格已真实验证。中文/其他非 ASCII 路径在原生启动前明确拒绝；没有声称验证过中文路径。

本复现包还保守限制原生命令行 **不超过 500 字符**。较长目标目录的 fresh 命令为 526 字符，连续两次在 stdout/journal 产生任何内容前以 Windows 0xC0000005 退出；先前一条 508 字符命令成功。此对比只支持制定当前包的保守适用范围，**不能证明 Cadence 存在官方 512 字符上限，也不能断言长度或空格就是两次崩溃根因**。最终选择更短且仍含空格的全新目录，完整复现通过。plan/run 会在启动前检查 build 和 fresh 的命令长度；超出时缩短目标根目录或 tag。

本次使用的合法安装为 C:/Program0/Cadence/SPB172，原生版本 17.2 S045。这只是本机环境事实，配置样例应按目标机修改。

## 5. 隔离、进程所有权与异常关机后的恢复

每次运行都有私有 pcbenv、TEMP/TMP；只 source 安装自带 TELENV 默认环境，关闭本任务 autosave，不载入用户 01env 快捷键和工程脚本。Python -I 排除用户 site/PYTHONPATH 对启动器导入的影响；Cadence 子进程另清除 PYTHONPATH/PYTHONHOME，设置 PYTHONNOUSERSITE=1。用户 HOME 不修改。

这是任务相关变量隔离，**其余操作系统与合法许可证环境仍继承**；日志不记录其值，不宣称整个系统或许可证环境完全隔离。

已有用户 Allegro GUI PID 3840 被识别为非本任务进程，不向它发送输入、不关闭、不保存其工程。任务原生进程串行运行，记录 PID、创建时间、可执行文件、父 PID 和包含输入/脚本/日志路径的完整命令。超时只有重新核对全部身份一致的本任务直接子进程可终止，不按进程名批量结束。

异常关机后应先核实：

1. 哪个 task-owned run 已完成，哪个只有 process.json 或半份日志；旧进程 PID 可能已复用，不能仅凭 PID 杀进程。
2. fixture/源码 manifest 是否与已审版本一致；不可把新时间戳当成文件未变的证明。
3. 不完整 run 保留为失败证据，另 tag 重放；fresh 只读检查后才将该 run 标记为成功。
4. 新机环境、许可证、原生进程连接和 GUI 连接分别验证；任一项的历史成功都不代替当前机器实际探测。

## 6. 本次失败与修正，供以后避免

| 记录 | 观察 | 修正与结论 |
| --- | --- | --- |
| 最初 probe | utf8-sig 不是本 Python 的有效编码别名，尚未启动 Cadence | 修正为 utf-8-sig，原错误记录保留 |
| first01 | 创建标记后设计 DBID 缓存未刷新，枚举为 0；事务回滚，没有保存输出 | 读取前 axlDBRefreshId(nil)，再重新获取 design；fresh 单独验证 |
| first02/final01 与旧迁移报告 | 33 项虽然通过，但几何记录没有 ETCH_LINE/ETCH_ARC，只有器件/铜区/过孔；不能证明手工走线保持 | 显式展开 path/cline->segments，三阶段强制 932/750/182，再真实重跑。旧 33 项不计最终完成 |
| 长目录 relocated02/03 | fresh 启动前 0xC0000005，输入 SHA 不变，未产生读取证据 | 保留全部失败文件；不把启动器退出等同读回成功；保守命令长度门槛并以新较短含空格目录重验 |
| 重复正式 tag | run 明确拒绝覆盖 | 反例记录保留，使用新 tag 而不是删除旧运行记录 |

[历史文件目录](../examples/lesson60_20261023/native/history/)保存早期源版本、诊断与失败日志；较长路径的失败 run 也保留。**源码写完、进程退出码为 0、空文件散列相等、报告显示 PASS 都不足以单独证明操作成功**：需要预期对象出现、数据非空、实际数量合理、另进程重开及源不变共同成立。

## 7. 学习结论与后续验收

已执行并能复现：本机安装下的最小 SKILL 操作、Python 串行原生启动、相对路径迁移、含空格路径处理、源完整性校验、实际路径子段读回和 fresh 检查。Tcl 是其他 Capture/网表工作流的一种工具，本课这个 PCB 小操作采用 SKILL；没有把未运行的 Tcl 示例计作已验证。

知识通过本地文本、源码、清单、日志、训练源和失败记录保存；迁移这些文件可以恢复依据与复现步骤。它们不会自动提供另一台电脑的 Cadence 安装、许可证、原生访问权或 GUI 控制连接，也不能把“已经记下教程”写成“所有软件功能已掌握”。真正的第二台电脑验收仍需按包说明重建配置，并保存该机自己的 probe、实际 run 和 fresh 非空证据。
