# 第 4 课：创建焊盘和两脚封装，保存后重新打开核对

本课原始记录之后，用户追加了封装默认规范：三文字层锚点均为 (0,0)，package height 默认 1 mm。当前 .dra/.psm 已更新；下文 (0,1.6) 等为修改前历史。最新规范和验证见 [package_defaults.md](package_defaults.md)。

日期：2026-10-17（Asia/Shanghai）
状态：在独立练习库完成 .pad / .dra / .psm 创建、保存和新进程读回核对。当前是教学尺寸，未对应某真实器件。

## 练习规格与产物
目录：learning/examples/lesson04_package。
规格文件 training_spec.json 是本课尺寸依据；单位毫米、精度 3 位小数。

| 项目 | 本课定义与重开实值 |
| --- | --- |
| 1、2 号引脚中心 | (-1,0)、(1,0)，中心距 2 mm |
| TOP 铜焊盘 | 矩形 1.0 × 1.5 mm |
| TOP 阻焊开窗 | 1.1 × 1.6 mm |
| TOP 锡膏/钢网开口 | 0.9 × 1.4 mm |
| 焊盘偏移 | (0,0)，无钻孔 |
| BOTTOM 铜、阻焊、锡膏 | 均为 NULL；两个引脚共 6 个查询 |
| 丝印轮廓 | 中心线 bbox (-1.7,-1.0)～(1.7,1.0)，4 段闭合，线宽 0.10 mm |
| 装配轮廓 | 中心线 bbox (-0.8,-0.5)～(0.8,0.5)，4 段闭合，线宽 0.05 mm |
| Place Bound | bbox (-1.8,-1.1)～(1.8,1.1)，填充矩形 |
| 位号占位文字 | U*，REF DES/SILKSCREEN_TOP，(0,1.6)，0° |
| 绘图区 | (-10,-10)～(10,10) mm，允许原点两侧放置 |

库文件：
- library/eda_l04_smd_1000x1500.pad：3648 字节，独立焊盘。
- library/eda_l04_two_pin_training.dra：65556 字节，可编辑封装。
- library/eda_l04_two_pin_training.psm：6644 字节，编译封装。
- library/eda_l04_smd_1000x1500.pxml：焊盘定义输入。
- preview.png：由保存后的数据库查询结果绘制的预览；不代表 Cadence 窗口截图，字体为预览标注，精确核对以 TSV 为准。

这些开窗和外形尺寸是练习定义，不是板厂规则或某型号器件推荐 land pattern。

## 第一步：从 XML 真正生成 .pad
官方批处理入口：

```text
C:/Program0/Cadence/SPB172/tools/bin/padstack_editor.exe -x <练习.pxml>
```

工作目录设为独立 library，后台隐藏启动；仅对子进程设 ALLEGRO_PCBENV。
PXML 使用 padstackusage=SMD_PIN、units=Mm、accuracy=3、holetype=NONE；三项 pad 的层为 BEGIN_LAYER、TOP_SOLDER_MASK_PAD、TOP_PASTE_MASK_PAD，类型 REGULAR_PAD、图形 RECTANGLE。
实际 .pad、同名 .log 和 padstack_editor.jrl 生成在本课 library。log 只有处理信息，journal 还含一条舍入警告，不能只读 log 就宣称无警告。
padstack_editor.jrl 确认程序版本为 17.2 S045 Windows SPB 64-bit Edition。
现有同名文件可能被覆盖，因此本课先检查新目录/文件不存在；复现应换新运行目录和库名。

## 第二步：新建 PACKAGE 并保存
Allegro 官方启动参数：
```text
allegro.exe -product Allegro_performance -safe -nographic
  -symbol package -s <创建.scr> -p <运行目录> <新的.dra路径>
```

实际操作在 lesson04_create.il 中：
1. 检查 axlDesignType(t) 为 PACKAGE 且 drawing 无 pin。
2. axlDBChangeDesignUnits("millimeters" 3)，再读回确认。
3. axlDBChangeDesignExtents(list(-10:-10 10:10)) 显式设置绘图区。
4. axlSetVariable("padpath" list(libDir)) 设置本会话的库路径，再 axlLoadPadstack。没有使用会写用户 env 的 axlSetVariableFile。
5. make_axlPinText 的 number 用字符串 "1"/"2"，带 axlTextOrientation，随后 axlDBCreatePin。第三参不能用 nil 隐藏编号，nil 会创建机械 pin。
6. axlDBCreateLine 创建丝印、装配闭合轮廓；axlDBCreateRectangle(... t ...) 创建填充放置边界。
7. axlDBCreateText 创建 U* 位号占位文字。
8. axlSaveDesign 显式保存到练习 library；保存后旧 dbid 失效，重新查询。
9. axlCompileSymbol 显式编译，并检查实际 .psm 和编译日志。

默认 Symbol Editor 保存 .dra 已会生成编译符号；本课另显式编译用于验证，不把两步说成所有配置强制流程。
所请求产品参数是 Allegro_performance；创建进程 banner 显示 Allegro Venture PCB Designer Suite，重开进程显示 Allegro PCB Designer。记录实际日志，不由此推断全部产品/选件可用。
未关闭 padstack 定义检查，未设置 nocheck 保存选项。

## 第三步：用新进程重开，核对磁盘结果
新进程带 -readonly 重开 .dra，不依赖创建进程内存或旧 dbid。
- design->pins 读到两 pin，坐标、编号、无孔属性一致。
- 每 pin 查询 TOP/BOTTOM 铜、阻焊、锡膏，读到预期矩形/NULL。
- axlExtractMap 使用安装自带 fgeo_bv.txt 的 FULL_GEOMETRY view，按实际图层筛选。
- 本例返回独立 line，按 startEnd / width 核对 8 段及闭合性；脚本也兼容 path->segments。
- 填充 Place Bound 的 objType 实际为 shape、filled=t、isRect=t。
- 对照独立 training_spec.json，18 项规格/持久性检查通过。
- 保存后 native DRC 日志为 0，重开读取 stored_drcs=0、drc_state=t；编译日志完成。它只说明本训练对象的相应检查状态，不是数据手册、制造或 SI/PI/EMI 验收。
- .pad/.dra/.psm 的重开前后 SHA256 一致，无残留测试进程或板锁。

## 实际故障与修正
1. run02_create：默认新绘图区不包含负坐标，pin1 报 outside of extents。该次未保存 .dra；补设对称绘图区后解决。
2. run03_create：REF** 被 axlDBCreateText 拒绝，报 Illegal character(s)。改为安装自带 axltdesign2.il 的 U* 占位例后成功；不推断所有命令均禁止相同字符串。
3. run05_reopen：初版只按 path 导出轮廓，outline_segments=0；实际 FULL_GEOMETRY 已返回 8 条独立 line，不是轮廓缺失。补充 line/arc 分支后 run06 读出完整 8 段。
4. 进程审计中 PID 19604 后续被 msedge 复用；改为结合程序名、启动时间和原 WaitForExit 结果，不能仅据同一 PID 仍存在判断测试进程未退出。
失败脚本、前版规格和原始日志均保留在对应 run 目录。

## 警告与尚未验证
- Padstack XML 导入 journal 和新 drawing 的单位设置过程均有 SPMHUT-48：Scaled value has been rounded off。日志未指出具体字段；当前逐项读取的练习规格均匹配，不宣称所有字段没有舍入。
- 上课 C1 polygon bbox/vertices 的 0.5 mil 差异仍未解释；本课毫米练习成功不等于该问题已解决。
- 尚未将 .psm 放置到 PCB，尚未创建配套 Capture 符号及核对原理图网络映射。
- 尚未依据真实器件数据手册认证这个封装；不能作为量产库交付。
- 本课未重试桌面控制，也未运行 ai_bridge；通过官方原生 CLI/SKILL 完成操作。
- 没有打开修改用户真实硬件工程；变更仅为本课新建的练习文件。

## 日志与复现
learning/logs/lesson04_package_20261017：
- run01_padxml：Padstack Editor 启动参数和 stdout/stderr；原生 log/journal 在 library。
- run02_create、run03_create：两次失败及执行脚本快照。
- run04_create：成功创建报告、journal、compile/DRC 日志。
- run05_reopen：首次重开及脚本快照。
- run06_reopen：最终引脚、焊盘、几何、线段、文字 TSV 与重开前文件哈希。
汇总：learning/logs/lesson04_result_20261017.json。
成功脚本：learning/scripts/lesson04_create.il/.scr、lesson04_verify.il/.scr。
复现时先换输出目录/库名并保留已有文件；创建脚本会保存文件，verify 脚本只读。

## 本机官方来源
- [Padstack Editor 命令](C:/Program0/Cadence/SPB172/doc/pcoms/pchap.html#pad_designer)：-x 导入、检查、保存并退出。
- [XML 示例](C:/Program0/Cadence/SPB172/share/pcb/examples/padstack_xml/smd_pin.pxml)、[锡膏层示例](C:/Program0/Cadence/SPB172/share/pcb/examples/padstack_xml/via1.pxml)、同目录 padstack_xml.docx、xml-formats/cdn_padstack.dtd。
- [创建 API](C:/Program0/Cadence/SPB172/doc/algroskill/03dbcre8.html)：Pin、Line、Rectangle、Text。
- [官方编号构造测试](C:/Program0/Cadence/SPB172/share/pcb/examples/skill/dbcreate/axldbctpin.il)。
- [U* 官方示例](C:/Program0/Cadence/SPB172/share/pcb/examples/skill/file/axltdesign2.il)。
- [设计单位、绘图区、保存、编译](C:/Program0/Cadence/SPB172/doc/algroskill/14dsnctl.html)。
- [变量设置作用域](C:/Program0/Cadence/SPB172/doc/algroskill/09cmdshl.html)：axlSetVariable 仅本会话。
- [几何遍历](C:/Program0/Cadence/SPB172/doc/algroskill/22extrct.html)：axlExtractMap。
- [封装保存和 Place Bound](C:/Program0/Cadence/SPB172/doc/algrolibdev/chap3.html)。

下一课：把编译封装载入独立练习 PCB，练习放置、旋转、镜像并核对实例引脚位置和层别，再衔接原理图符号/封装映射。

预览绘图源码已归档到 learning/scripts/lesson04_preview_source.txt（PowerShell + System.Drawing）。它是成功 inline 命令的文本记录，本课没有以 .ps1 文件运行，也未更改执行策略；重新渲染会覆盖所配置的 preview.png。

做好记录  字符丝印至少包含 
位号层 REF DES   的 SILKSCREEN_TOP 和 ASSEMBLY_TOP 
value层  COMPONENT VALUE 下的  ASSEMBLY_TOP 
坐标都在器件的原点中心
器件的高度默认 package height  1mm
