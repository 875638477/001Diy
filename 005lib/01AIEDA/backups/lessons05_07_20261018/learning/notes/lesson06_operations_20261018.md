# 第 6 课：原生精确操作、过滤选择、网格和事务回退

日期：2026-10-18（Asia/Shanghai）。状态：**原生接口子项已实操验收，整课部分完成**。桌面接口复测仍为 native pipe 不存在，交互视图、菜单、鼠标和界面撤销仍待实操。证据为 examples/lesson06_operations/desktop_connection.json。

## 目标、环境与产物

Cadence Allegro 17.2-S045，BOARD，millimeters/3，独立练习文件 examples/lesson06_operations/lesson06_operations.brd。操作源码 scripts/lesson06.il，入口 create.scr/read.scr，成功原始日志 logs/create03、logs/reopen。前两次失败原始输入和日志保留于 logs/create、logs/create02。最终 validation.json 是外部读回验收，不能只凭 “COMPLETE” 或进程退出 0 判断学习成功。

本课实操通过了：独立精确几何创建；非交互过滤框选；可见性/过滤器/网格恢复；事务 Start/Mark/Oops/Rollback/Commit；保存后重取 dbid；新进程重开；毫米数据库量化及半个 DBU 边界差异测量。未操作用户真实工程。

## 官方依据

均位于 C:/Program0/Cadence/SPB172/doc/algroskill：
- 04parmgt.html：axlDBGridGet/Set（约193、402、470行）。GridSet 不可撤销；间距读取为 list，输入可用 float。
- 05selfnd.html：axlSingleSelectBox（约599行）、axlSetFindFilter/GetFindFilter。框选必须提供两个角点，否则会等待用户拾取。
- 17dbtran.html：Commit #1076340、Mark #1076368、Oops #1076373、Rollback #1076401、Start #1076430。
- 06intedt.html#821370：axlTransformObject。非法变换可被静默忽略，返回非 nil 仍必须验坐标。
- 07dbaccs.html：axlDBGetShapes 不受可见性/Find Filter 影响；axlDBRefreshId 只刷新自身，不递归刷新子对象。
- 03dbcre8.html#367747 与安装 share/pcb/examples/skill/DOC/FUNCS/axlDBCreateText.txt：文字创建返回结构。
- 14dsnctl.html：保存清除 dbid handles 和 selection；axlDBChangeDesignOrigin 的参数是偏移量，本轮未执行原点移动。
- 20plyopr.html：axlPolyFromDB/polygon 属性。临时 polygon 不是数据库 dbid。

## 已验证的操作流程

1. 在新空板、建几何前设毫米精度3及对称 extents；创建填充矩形 (5,5)～(7,7) 和同层 TARGET 文字。
2. 读取 non-etch 网格，保存普通值（origin和X/Y间距），测试改为0.05mm，再显式恢复原值2.54mm。GridSet 的状态不交给事务回退管理。
3. 新空进程最初 GetFindFilter(nil/t) 均为nil。本轮先建立已知基线（LINES/SHAPES/TEXT，按钮LINES），读取实际返回，再做 SHAPES/TEXT enabled、仅SHAPES buttons 的对照测试。
4. 临时仅显示 PACKAGE GEOMETRY/ASSEMBLY_TOP，双点框选 (4,4)～(8,8)，实际仅选中1个 shape，没有误选文字；清选择后恢复可见性和已知过滤基线。
5. 同一个函数内 Start，移动，Mark，旋转，Oops，Rollback；另开事务移动并Commit。每阶段重新取得目标 shape 并导出 bbox，回退后的旧 dbid 不继续当稳定标识。
6. 提交之后保存，重新取得对象，另起只读进程重开；持久化几何和原始导出逐字节一致。成功创建和重开的实际进程退出码均为0，重开哈希不变。
7. 创建9个小坐标文字测量实际落点，以及0.101mm线宽的线，导出对象bbox、多边形bbox及顶点，保留差异。

| 阶段 | 包围框 minX,minY,maxX,maxY（mm） |
| --- | --- |
| INITIAL | 5,5,7,7 |
| MOVED | 7,4,9,6 |
| ROTATED | 5,4,7,6 |
| OOPS | 7,4,9,6 |
| ROLLBACK | 5,5,7,7 |
| COMMIT / AFTER_SAVE / REOPEN | 4,7,6,9 |

事务 Start 返回 mark 整数；Mark 返回 t/nil，不能用它替换 mark。Oops退到最近Mark，Rollback终止并退到Start，Commit终止并保留变化。事务不跨保存、打开或未结束的 SKILL 命令。视图/过滤/selection/grid等设置分别管理。

## 过滤器的本机实测

官方 GetFindFilter 正文和例子互相矛盾。本机对照实测：
- nil：enabled = ("BONDSMART" "DYNTHEMALS" "SHAPES" "TEXT")
- t：onButtons = ("SHAPES")

BONDSMART、DYNTHEMALS是此处实际自动加入的条目，不能假定返回列表严格等于输入。第一次恢复到初始nil状态时 enabled 不等于nil，未假称恢复成功；最终改用明确初始化后的已知基线，visibility、enabled、buttons、grid四项恢复均读回t。初始状态nil的精确还原行为未查明；隔离进程结束，不写用户全局配置。

## 网格与数据库精度

显示/捕捉网格不是存储精度。以下是本机 millimeters/3 的实际输入/输出，不据此推广通用舍入规则：

| 输入X / mm | 实际X / mm |
| --- | --- |
| -0.0006 | -0.001 |
| -0.0005、-0.0004 | 0 |
| 0.0004、0.0005 | 0 |
| 0.0006 | 0.001 |
| 10.0004、10.0005 | 10.000 |
| 10.0006 | 10.001 |

0.101mm宽、中心线(1,1)～(4,1)：
- 对象 bbox：(0.949,0.949)～(4.051,1.051)
- polygon bbox：(0.9495,0.9495)～(4.0505,1.0505)
- polygon vertices 包围范围：(0.949,0.949)～(4.050,1.050)

本例 polygon bbox 含半个0.001mm单位，顶点落在0.001mm格点，部分边缘相差0.0005mm。保存/重开后仍一致。这与第3课mil/0的半单位现象相似，但本轮没有证明旧样例根因。后续制造/间距审查同时核对几何表示与精度，不能把显示、bbox、顶点自动视为完全相同。

## 失败与修正

- 首次源码少一个右括号，reader自动补括号，导致l6Create未定义；进程仍返回0。现已修正并加入字符串/注释感知的括号静态检查。
- 第二次文字结果的首项不是可直接读取xy的单个dbid，格式化遇到nil；按 dbid/list 类型递归取得第一个dbid后，通过实际文字坐标验收。官方接口示例与返回结构说明也有不一致，应核类型。
- 第二次初始nil过滤器恢复不成立，已如上明确初始化基线后重试，不隐藏该差异。
- 成功run仍有SPMHUT-48舍入警告，未推断具体触发字段；要求的事务bbox及量化记录均实际核对。
- launcher真实退出码0不等于脚本成功；成功必须同时有报告完成、实际文件、独立数值验收和重开哈希证据。

## 复现与下一步

统一启动脚本 learning/scripts/launch_cadence17.py：--mode create/readonly --board 文件 --script SCR --log 全新日志目录，使用 learning/tools/python_3_14_0/python.exe。它限制写入01AIEDA，原生程序隐藏运行，记录参数、PID、UTC时间、退出码、脚本/板哈希；不操作桌面界面。

复现必须新建目录并调整代码中的输出路径，保留旧失败记录；创建模式不覆盖已有板。validation.json由scripts/validate_lessons05_06_and_layers.py核对8个事务状态、四项恢复、过滤语义、量化和持久性生成。当前用户层名规范另见 pcb_layer_naming.md，板的电气层必须使用 TOP/BOTTOM 或 TOP-L2-…-BOTTOM。

下一步：桌面连接恢复后补齐交互视图、菜单、鼠标精细选择、撤销流程；继续追查几何表示与半单位边界原因。已完成原生子项可复用，界面操作不会被本笔记冒记为已掌握。
