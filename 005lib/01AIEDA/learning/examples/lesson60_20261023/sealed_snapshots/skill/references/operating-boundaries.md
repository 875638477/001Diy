# 固定规范与证据边界

## 用户固定规范

- 两层TOP-BOTTOM；四层TOP-L2-L3-BOTTOM；六层TOP-L2-L3-L4-L5-BOTTOM，继续按连续L编号扩展。层功能另记，不把L2/L3重命名为GND/POWER，不在本项目物理层叠加入额外MASK行。
- 四层默认TOP器件/信号、L2完整公共GND、L3电源、BOTTOM信号。完整公共地保留正常反焊盘与机械避让；BOTTOM电源参考及跨参考返回须核真实去耦路径，不能只添GND via判通过。
- 封装至少REF DES/SILKSCREEN_TOP、REF DES/ASSEMBLY_TOP、COMPONENT VALUE/ASSEMBLY_TOP，局部锚点(0,0)。缺省PACKAGE_HEIGHT_MAX=1 MM；明确器件高度以器件证据为准，已有明确高度不覆盖。
- 01env/drill*.txt是对应光绘模板来源；先核实际层序再核所有Film映射。env o/O指向mm Gerber脚本，~o/~O为mil，不能在原工程盲目重放带save等副作用的整套env。

## 已知操作陷阱

1. Allegro数据库ID仅在所属进程/数据库有效；跨进程通过稳定身份/坐标/层/网络重新解析。GetConnect可能返回path父对象，须遍历segments；空集合/0检查数不能算几何通过。
2. 动态铜看实际更新状态、网络、孤岛、孔和端点，不仅看母形或颜色。热连接段与manual段分开计数。顺序不稳定的导出表用保重复的多重集合比较。
3. 读取.comp/device definition的真实VALUE，不从deviceType命名后缀猜值。实例文字合规不保证原Film含这些文字class；核实际输出层。
4. scoped DRC、存量marker数与最新全板DRC不同。生成文件不等于命令无警告，更不等于SI/PI/EMI或制造通过。警告应记录原文、条件与结论。
5. 本地启动器、SDK、桥接和queue常含本机绝对路径；旧ready/result可能是旧会话残留。新目录/唯一请求token、进程身份和新鲜结果共同证明本次执行。
6. Windows中所有文件名/JSON用明确UTF-8；跨PowerShell传中文源码宜ASCII JSON转义。路径引用不以JSON字符串当shell转义。SHA比较统一大小写，字节差异与JSON语义差异分开。
7. 活动EDA/current进度入口会继续变化。封存课内快照与源件身份，不把活动入口期望为永远不变的历史依赖。保留失败和恢复日志，勿改旧封存使其看似通过。

## 迁移与能力声明

携带整个01AIEDA可保留文本、脚本、工程和日志；外部公共库/原教程/安装路径依赖另清点。软件、合法许可、桌面工具和硬件需目标机现场配置，不在本技能打包凭据或承诺恢复连接。

本机换目录重跑属于“重定位复现”，不是“另一台物理电脑验证”。文本可提取、扫描页视觉可读、OCR识别、视频已看、原生CLI、Capture SDK/Tcl、GUI每项单列状态；一个接口可用不能推断其他接口已通过。

官方技能机制说明（核对日期2026-10-23）：[Build skills](https://learn.chatgpt.com/docs/build-skills)。这里只提供本地技能源包，没有自动修改全局技能安装目录或账户设置。完整学习根内的第60课README提供迁移步骤和现场验收表。
