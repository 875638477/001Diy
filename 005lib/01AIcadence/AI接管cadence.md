# AI 接管 Cadence Allegro —— 完整记录与使用手册

> 本文件夹 `D:\001DIY\005lib\01AIcadence` 是 AI 接管 Cadence 的**永久工程目录**。
> 以后用 Cursor 直接打开本文件夹继续工作,所有信息都记录在本文档中。
> 创建日期:2026-06-10

---

## 一、目标与可行性结论

目标:让 AI 接管 Cadence Allegro PCB Editor 17.2,完成元件摆放、走线布线等操作。

结论:**可行**。不靠模拟鼠标键盘,而是通过 Cadence 官方支持的 **SKILL 编程接口**直接读写 PCB 数据库(EDA365 工具箱本身就是 SKILL 插件,证明本机 SKILL 通道可用)。

## 二、总体架构(文件桥方案)

```
AI 写入 exchange/command.il(SKILL 指令)
AI 创建 exchange/command.flag(触发标志)
        ↓
Allegro 启动时 ipcBeginProcess 拉起外部监视进程 flag_watch.bat
监视进程每 1 秒检查 command.flag,存在则向 Allegro 输出 "RUN"
        ↓
SKILL 回调 AIB_ipcData 被异步唤醒 → 执行 command.il
全部输出捕获到 exchange/result.txt
        ↓
生成 exchange/result.flag 表示完毕 → AI 读取 result.txt → 决定下一步
```

> v2(2026-06-10):17.2 无定时器 API,放弃轮询,改用 IPC 事件驱动,
> 全自动、不抢焦点、约 1~2 秒响应。用户无需手输任何命令。

三层能力规划:

1. **查询层**:`axlDBGetDesign`、`axlGetSelSet` 等读取板框、元件、网络、飞线 → AI 不需截图即可"看懂"PCB 状态
2. **操作层**:摆放(`axlPlaceComponent`)、走线(`axlDBCreateLine` / `axlDBCreateConnection`)、过孔、约束规则
3. **自动布线层**(可选):SKILL 导出 SPECCTRA DSN → 开源 FreeRouting 自动布线 → 导回 .ses

## 三、目录结构

```
D:\001DIY\005lib\01AIcadence\
├── AI接管cadence.md          ← 本文档(总记录)
└── ai_bridge\
    ├── ai_bridge.il          ← 驻留 Allegro 的桥接脚本(核心,v2 IPC 事件驱动)
    ├── flag_watch.bat        ← Allegro 通过 ipcBeginProcess 拉起的监视进程
    ├── auto_run.ps1          ← (废弃)按键注入方案,被系统拦截,留作记录
    ├── watch_result.ps1      ← AI 用的结果监视脚本(等待 result.flag 出现)
    └── exchange\             ← AI ? Allegro 文件交换目录
        ├── command.il        ← AI 下发的 SKILL 指令
        ├── command.flag      ← 存在 = 有新指令待执行(执行前会被删除)
        ├── result.txt        ← 执行结果(打印输出 + OK/ERROR 状态)
        └── result.flag       ← 存在 = 执行完毕
```

## 四、已完成的安装配置

### 1. allegro.ilinit 自动加载(已配置)

文件:`C:\Program0\cadence\SPBData172\pcbenv\allegro.ilinit`,内容:

```
errset(loadi(strcat(axlOSSlash(getShellEnvVar("FP_SKILL")),"FP_Load.il"),"fastprint"))
errset(loadi("D:/001DIY/005lib/01AIcadence/ai_bridge/ai_bridge.il","ai_bridge"))
```

第一行是 EDA365 Skill 的(原有),第二行是 AI 桥接(新增),两者共存互不影响。
Allegro 每次启动会自动加载桥接并开始轮询。

### 2. Cadence 17.2 环境(背景信息)

- 安装目录:`C:\Program0\cadence\SPB172`
- HOME:`C:\Program0\cadence\SPBData172`(pcbenv 在此目录下)
- License:`C:\Program0\cadence\LicenseManager172\license.dat`
- 本机装有多版本 Cadence,17.2/17.4 环境变量切换用 bat 脚本(在旧目录 eda365 文件夹中)

## 五、如何运行 / 调用(操作步骤)

### 日常启动流程

1. 启动 Allegro PCB Editor 17.2(桥接随 ilinit 自动加载)
2. 确认命令行窗口出现:
   ```
   AI_BRIDGE: loaded. Commands: ai_start / ai_stop / ai_run / ai_status
   AI_BRIDGE: polling started, every 2 s.
   ```
3. 打开要操作的 .brd 板子
4. 在 Cursor 中打开本文件夹,告诉 AI 要做什么,AI 自动通过交换目录下发指令并读取结果

### Allegro 内可用命令(底部命令行输入)

| 命令 | 作用 |
|---|---|
| `ai_status` | 查看桥接状态(是否运行、已执行次数、是否有待处理指令) |
| `ai_start`  | 启动轮询(加载时已自动启动,一般不用手输) |
| `ai_stop`   | 停止轮询(不想让 AI 操作时输入) |
| `ai_run`    | 手动执行一次待处理指令(定时器不可用时的兜底方式) |

### AI 侧的调用方法(给 AI 自己看的备忘)

1. 把 SKILL 代码写入 `ai_bridge/exchange/command.il`(**纯 ASCII**,禁止中文)
2. 写入 `ai_bridge/exchange/command.flag`(内容随意,存在即触发)
3. 运行 `watch_result.ps1`(后台)等待 `result.flag` 出现,或直接轮询检查
4. 读取 `result.txt` 获取输出与 OK/ERROR 状态
5. 桥接脚本会自动删除 command.flag、重建 result.flag,无需 AI 清理

## 六、当前进度与状态

- [x] 方案设计(文件桥 + SKILL)
- [x] ai_bridge.il 编写完成
- [x] allegro.ilinit 配置完成(指向本目录)
- [x] 第一条测试指令已就位(报告板名/元件数/网络数)
- [x] **链路已验证通**(2026-06-10 23:06):打开 `01AI3576allV1_00_00.brd` 后执行查询成功,读到 760 元件 / 621 网络
- [x] ~~手动模式~~ → **已升级 v2 全自动**:IPC 事件驱动(`ipcBeginProcess` + `flag_watch.bat`),AI 下发指令约 1~2 秒自动执行,无需任何手动操作(实测通过)
- [x] 真实未布线清单已取得:125 网络 / 736 飞线(GND 348 + GND-A 55 靠铺铜;DDR 全部已布通)
- [ ] 查询层封装(读取板框/元件坐标/飞线)
- [ ] 操作层封装(摆放、走线、过孔)
- [ ] FreeRouting 自动布线链路(DSN 导出 → 布线 → SES 导回)

## 七、已知风险与注意事项

- SKILL 指令**直接修改 .brd 数据库**,重要操作前必须备份(AI 操作前应自动另存副本)
- 所有 `.il` 文件保持**纯 ASCII**:本机是中文 Windows(GBK),UTF-8 中文会乱码甚至破坏解析(参考旧目录"乱码问题记录.md")
- 17.2 SKILL 文档较老,定时器 API 名称不确定:桥接已做三级兜底
  `axlScheduleTimer` → `axlDelayedRunSkill` → 手动 `ai_run`
  若启动后提示 `no timer API found`,改用手动模式,链路同样能通
- 高速差分、等长、阻抗控制类走线:AI 可以做,但需人工给规则并复查结果

## 八、历史记录 / 变更日志

| 日期 | 事项 |
|---|---|
| 2026-06-10 | 方案确定:SKILL 文件桥;在旧目录 `D:\003Software\001AD_CAD_Cadence_creo\eda365\ai_bridge` 首次搭建 |
| 2026-06-10 | 因 eda365 软件安装目录易丢失,整体迁移到 `D:\001DIY\005lib\01AIcadence`(本目录),allegro.ilinit 已同步改指新路径,旧目录桥接文件已删除 |
| 2026-06-10 | 链路验证通过:打开 .brd 后查询成功(760 元件/621 网络)。确认 17.2 无定时器 API,固定使用手动模式:AI 下发指令后用户在 Allegro 输 `ai_run` |
| 2026-06-10 | 桥接升级 v2:按键注入方案被 Windows 拦截弃用;探测发现 ipc 进程族可用,改为 `ipcBeginProcess` 事件驱动,全自动免手输,实测 1.5 秒响应。备份已建:`backup_by_AI\01AI3576allV1_00_00_20260610_231257.brd` |

## 九、下一步计划

1. ~~重启 Allegro 验证链路~~(已完成,手动模式)
2. 封装常用查询指令:列出全部元件及坐标、列出未布线网络(飞线)
3. 实现单网络两点走线 demo(指定线宽、层)
4. 接入 FreeRouting 做整板自动布线

## 十、当前工作会话

- 正在操作的板子:`D:\011job\018Hengbot\000Sparky\05HW\01AiHead\02PCB\01AI3576allV1_00_00.brd`
- 板况:760 个元件、621 个网络
- 工作节奏(手动模式):AI 写好 `command.il` 并放置 `command.flag` → 用户在 Allegro 命令行输 `ai_run` → AI 读取 `result.txt` 汇报


## 十一(补)、2026-06-11 下午会话记录

### 链路修复
- `allegro.ilinit` 丢失导致桥接未自动加载,已重建于 `C:\Program0\cadence\spbdata172\pcbenv\`(HOME 已核实)
- 链路恢复全自动,本日往返 50+ 次

### 重大教训(必读)
- **框选/DRC 查询只对"当前可见"对象生效**:BOTTOM 层显示关闭时,框选查不到底层走线,DRC 标记也选不到,导致出现假"零违规"
- 正确做法:任何勘察/DRC 前先 `axlVisibleLayer("ETCH/XX" t)` + `axlVisibleUpdate(t)` 打开相关层(含 PIN/VIA CLASS)
- `axlAddSelectBox` 只选**完全包含**在框内的对象,框要开大,跨框长线会漏
- `axlPathLine` 是函数式:必须 `pp = axlPathLine(pp w pt)` 接收返回值
- `axlDBCreatePath` 返回 `((dbids) t)`;贴着同网络过孔端点创建会自动挂网
- 事务 API 为 `axlDBTransactionStart/Commit/Oops`;`axlShell("drc update")` 勿夹在事务中间
- 板上原有 14 个旧 DRC 标记(板框处 10 + 中部 4),为用户遗留基线

### 当前板况(01AI3576allV1_00_01.brd,与昨日 _00_00 不同!)
- 未布:6 网络 / 22 飞线 = 信号 5 条(UART2_TX/RX、UART4_TX/RX、WIFI_BT_RSTN)+ GND 17 条
- 电源飞线已全部由用户自行解决
- 备份:`backup_by_AI\01AI3576allV1_00_01_20260611_144608.brd`
- AI 试布的 3 条线(曾出现假 DRC 通过)已全部删除,板子恢复原状

### 5 条信号线自动布线结论:**不可布(无改动前提下)**
- 已建闭环布线器 `routing\autoroute3d.py`:Python A* 三层(TOP/L3/BOTTOM)+ 加过孔跳层 + Allegro DRC 裁决、违规自动回退
- U5(BGA)西南/东南逃逸区:过孔阵列间距 23.6mil、既有逃逸线已占满全部空隙;间距压至 2mil 仍无连续通道,口袋内也无任何可放新过孔的净空
- 这 5 条正是用户剩下没布的"死局"网络;需挪动既有走线(推挤)或改规则才可能布通

## 十一、布线任务记录(2026-06-10 晚)

### 用户需求

- 把板上未连接的飞线处理连接
- 已有部分尽量不动,尤其 DDR:不穿插,绕开 DDR 的走线/器件/铜皮
- 名称带 VCC/VDD 的都是电源,用铺铜方式连接
- 信号线布线方式:用户已选定 **AI 用 SKILL 逐条计算路径**(不用 FreeRouting)

### 勘察结论(全部只读查询,板子未动)

- 未布通:125 网络 / 736 飞线
  - 电源约 300 条(VCC5V0_SYS_S5 40、VCC_3V3_S3 33、VCC_3V3_S0 26、VCC_1V8_S3 19 等)
  - GND 348 + GND-A 55(靠平面,先核实真实性再补)
  - 信号约 120 条;**DDR 网络 0 条(已全部布通,只需避让)**
- 平面结构:L2/L7/L9=GND 平面;L3~L6/L8=电源分块平面;TOP/BOTTOM 局部小铜皮
- DDR 走线集中区:(-1321,-491) 到 (1030,753) mils
- 单位 mils;板框 bBox 含图框,实际器件区约 ±1500 mils

### 实施方案(已定,待用户发令开始)

1. 电源:逐网络处理,过孔下到对应平面或短线连邻近焊盘;每步事务保护+DRC 复查;从最简单网络试点
2. 信号:AI 用 SKILL 逐条计算路径布线,避开 DDR 区域
3. GND:先核实 348 条飞线真实性,再决定补缝合孔

### 状态:布线暂停中(用户要求先确认命令接管;接管已于 00:01 实测完成,全自动)

## 十二、两个问题的解答(2026-06-11 17:08)

### 1. 实时性优化(已完成)

旧链路延迟约 1.5~2.5 秒/次,瓶颈与改法:

| 环节 | 旧 | 新 |
|---|---|---|
| flag_watch.bat 轮询间隔 | `ping -n 2`(约1秒) | `ping -n 1 -w 250`(约0.25秒) |
| AI 侧等待 result.flag | 1 秒/次 | 50 毫秒/次 |

改完实测 5 次往返:393/185/186/185/186 ms,**平均约 0.2 秒**,提速约 10 倍。
(注意:大命令本身的执行时间不变,比如 drc update 要几百毫秒;感觉慢的另一原因是 AI 每步之间要分析思考,这部分不是链路延迟。)

### 2. Allegro 窗口无需置前,后台即可操作

- 原理:指令是在 Allegro **进程内部**由 SKILL 的 IPC 回调执行的,不是模拟鼠标键盘,所以**不需要窗口焦点**,后台、被遮挡、最小化都能跑
- 证据:今天全部 72 次执行都是你在 Cursor 界面、Allegro 在后台时完成的
- 两个例外情况:
  - Allegro 弹了**模态对话框**(等你点确定的那种)时,回调会被卡住,点掉即恢复
  - 你正在 Allegro 里**拖动/执行交互命令**的瞬间,AI 写数据库可能与你互相干扰——AI 动板子时你别同时操作板子即可,只看不动没关系

问题
1.你操作走线的时候 是否可以 一点一点走线 而不是一次性走线整条  
这样可以一点一点查看drc而且可以迅速做出改进走线 
我有没有吧这个条件说明白?
2.你布线的时候我刚刚也要求了在第八层是可以走通的 但是你依然在其他层叠走  且全部是错误
为什么会出现这样的情况?


1.重新检查飞线和布线
2.是否有一种可能先一点一点预判走线然后再走线 这样是不是可以避免走线drc错误