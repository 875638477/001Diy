# QMI8610 PCB 封装制作与验收

日期：2026-10-18（Asia/Shanghai）。本次按用户最新决定，只制作 PCB 焊盘和封装，不制作 Capture 原理图符号。

## 最终公共库文件

| 类型 | 文件 |
| --- | --- |
| 可编辑封装 DRA | D:\001DIY\005lib\01Psm_lib\qmi8610_lga16_3d3_p0d5.dra |
| 编译封装 PSM | D:\001DIY\005lib\01Psm_lib\qmi8610_lga16_3d3_p0d5.psm |
| 焊盘 PAD | D:\001DIY\005lib\01Pad_lib\qmi8610_smd061x032_m05_p100.pad |

PCB Footprint 属性填写 **qmi8610_lga16_3d3_p0d5**，不带扩展名。本次未创建 OLB；该属性名称只说明将来关联时的封装名。

本次验证进程显式设置：
- PSMPATH：D:/001DIY/005lib/01Psm_lib
- PADPATH：D:/001DIY/005lib/01Pad_lib 在前、D:/001DIY/005lib/01Psm_lib 在后。

未更改用户全局环境或启动文件。公共库原本存在一些同名而哈希不同的 .pad，几何是否相同未核实；本次使用新专名，不覆盖、不清理旧文件。

## 数据来源与工程选择

精确源文件：D:\004Document\016Sensor\06IMU\矽睿\QMI8610 Datasheet Rev. A.pdf  
Document 13-52-14，Rev A，PDF 共 82 页。源 SHA256：
A4B2F50DBFAB21EBA0BEEACD500F214A7B9301AF733F8B3D5B28939E06D0E265。

同目录有 Rev.A.pdf、Rev.A_8.pdf 等近似名字，本次没有混用。关键页面：
- PDF 第 8 页 Figure 4/5：顶视、底视编号，以及中心不可焊接；第 8—9 页 Table 2：引脚定义。
- PDF 第 79 页 §11.1 Package Drawing：本体尺寸、最大高度、器件端子底视图及推荐 PCB land pattern。
- 推荐 land 注 D：基于 FSC design；不能据此宣称已完成独立装配/制造验证。

| 项目 | 本次值（mm） | 依据 |
| --- | --- | --- |
| 本体 | 3.30 × 3.30 | 第 79 页 TOP VIEW |
| 最大高度 | 1.00 | 第 79 页 SIDE VIEW；与用户默认 1 mm 一致 |
| 外围焊盘数 | 16 | 第 8、79 页 |
| 引脚间距 | 0.50 | 第 79 页推荐 land |
| 铜焊盘 | 径向 0.61 × 切向 0.32 | 第 79 页推荐 land；不是器件端子尺寸 |
| 铜焊盘最外缘总跨度 | 3.40 × 3.40 | 第 79 页推荐 land 的 3.40 及四向对称定义 |
| 相对两侧铜内缘间距 | 2.18 | 第 79 页参考尺寸 (2.18) |
| 径向焊盘中心 | ±1.395 | (3.40 − 0.61) / 2；3.40 − 2×0.61 = 2.18 |
| 阻焊开窗 | 0.71 × 0.42（随引脚旋转） | 工程选择：铜每边外扩 0.05 |
| 钢网开口 | 0.61 × 0.32（随引脚旋转） | 工程选择：铜 1:1；手册图未规定 |
| Place Bound | 4.00 × 4.00，填充 | 工程选择：器件/焊盘外围放置边界 |
| 丝印线宽 / 装配线宽 | 0.10 / 0.05 | 工程选择；轮廓和 pin1 标记见 spec |

铜同侧最小间隙 0.18 mm，阻焊桥 0.08 mm。阻焊/钢网参数需要与实际板厂及贴片工艺匹配；本次没有指定板厂和钢网厚度，未做实物焊接验证。

中心区域不建编号 17，不建中心铜焊盘、阻焊或钢网开口；遵照 “Do Not Solder Center Tab/Pin (NC)”。这不是允许将中心区域改作散热焊盘的 QFN 模板。PCB 设计时应保持中心不可焊接，避免未盖油的过孔或裸铜造成意外焊接；手册未在此给出中心布线禁区尺寸，因此本封装没有凭空添加禁布区。

## 顶视编号与坐标

原点为器件中心，X 向右、Y 向上；pin1 在左侧最上方。左侧 1→4 向下，底边 5→8 向右，右侧 9→12 向上，顶边 13→16 向左。不要把 BOTTOM VIEW 直接复制成 PCB 顶视编号。

| 引脚 | 手册功能名（核对用） | X / mm | Y / mm | Pad 旋转 |
| --- | --- | --- | --- | --- |
| 1 | RESV3 | -1.395 | 0.750 | 0° |
| 2 | VDDa | -1.395 | 0.250 | 0° |
| 3 | GNDa | -1.395 | -0.250 | 0° |
| 4 | RESV2 | -1.395 | -0.750 | 0° |
| 5 | RESV1 | -0.750 | -1.395 | 90° |
| 6 | SDA2 | -0.250 | -1.395 | 90° |
| 7 | SCL2 | 0.250 | -1.395 | 90° |
| 8 | VDDd | 0.750 | -1.395 | 90° |
| 9 | SA0/SDO | 1.395 | -0.750 | 0° |
| 10 | CS | 1.395 | -0.250 | 0° |
| 11 | INT2/DRDY | 1.395 | 0.250 | 0° |
| 12 | INT1/CLKout | 1.395 | 0.750 | 0° |
| 13 | SDA/SDI/SDO | 0.750 | 1.395 | 90° |
| 14 | SCL/SPC | 0.250 | 1.395 | 90° |
| 15 | GNDd | -0.250 | 1.395 | 90° |
| 16 | RST | -0.750 | 1.395 | 90° |

第 9 页 pin13 的表格 alternate name 重复印成 SDI；其说明和第 8 页图明确包括三线 SPI SDO。本次仅记录功能，不创建逻辑符号或电气类型。pin1 RESV3 在表中要求接板地，pin4/5 是 NC；PCB 封装仍保留这三个实际外围焊盘。

## 用户规定的文字与高度

| Class / Subclass | 文本 | 局部锚点 |
| --- | --- | --- |
| REF DES / SILKSCREEN_TOP | U* | (0,0) |
| REF DES / ASSEMBLY_TOP | U* | (0,0) |
| COMPONENT VALUE / ASSEMBLY_TOP | VALUE | (0,0) |

文字采用新建 text block：width 0.45、height 0.60、lineSpace 0.30、charSpace 0.08、photoWidth 0.10 mm；引脚编号用更小的单独 block。水平居中，rotation 0。锚点是原点，不等同字形边界中心；native U* bbox 为 (-0.54,-0.25)～(0.54,0.65) mm。

填充 PACKAGE GEOMETRY/PLACE_BOUND_TOP 为 (-2,-2)～(2,2)，PACKAGE_HEIGHT_MAX 显式写 “1 MM”。未设 MIN 时沿用默认 0。装配外形为准确本体方框，并加内部 pin1 标识；丝印采用外围四角及左上 pin1 标记，避开焊盘开窗。

## 实际完成的验证

1. Cadence Padstack Editor 17.2-S045 使用官方 -x PXML 导入生成 PAD。
2. Allegro 17.2-S045 新建隔离 PACKAGE，按毫米精度 3 创建 16 pins、轮廓、三文字层及高度，保存 DRA 并编译 PSM；create02 报 COMPLETE，编译日志成功。
3. 新的 Allegro 只读进程从磁盘重开 DRA：16 pins，stored DRC=0，drcState=t；96 项铜/阻焊/锡膏层查询核对通过，48 项底层查询为 NULL，无孔。
4. 18 条轮廓线段的实际端点/线宽/层别与规格一致；3 项文本锚点及高度正确。几何精算丝印线到阻焊约 0.226 mm；独立保守 AABB 计算约 0.205 mm；native 丝印文字 bbox 到阻焊最小 0.39 mm。
5. 复制到公共库时目标均不存在；DRA/PSM/PAD 的 SHA256 与隔离验收版本逐项相同，发布清单保存于 publication.json。
6. 新进程只读重开公共 DRA，四份 pins/pads/segments/texts TSV 与隔离读回逐字节相同，DRA 哈希不变。
7. 在新练习 PCB 中只通过公共 PSMPATH/PADPATH 加载编译 PSM，验证 TOP 0°、TOP 90°、BOTTOM 0° 三种实例，共 48 个引脚的绝对坐标/局部坐标/方向及 TOP/BOTTOM 映射全部通过。底层 0° 镜像实测为相对原点 X 反向、Y 不变。
8. preview.png 根据原生读回的坐标、焊盘尺寸与轮廓绘制，已目视检查；它不是 Cadence 截图，文字字体与引脚标签为示意。

这是数据手册尺寸与原生 CAD 文件的验收，不等于电路设计、板级 SI/PI/EMI 或制造认证。实际电源去耦、回流、IMU 机械振动位置等在后续 PCB 布局中落实。

## 本轮学习与问题记录

- 第一次 create 在保存前查询 root design->pins 未反映逐 pin 创建结果，保护条件报 “Expected 16 peripheral pins”；没有生成 DRA/PSM。改为保存后及独立重开核对，实读 16。具体列表刷新机制尚未确认，不能简单认定保存前查询总可靠或总不可靠。首次原始脚本与日志保留在 logs/create。
- axlDBGetPad(pin)->bBox 在本机实测以 pin 中心为局部零点，但宽高已包含 pin 的 90° 旋转：左侧 .61×.32，上下侧 .32×.61；mask 同样交换。不能把它当成未旋转 pad definition 再转一次。校验脚本首次据未交换宽高而失败，随后按真实读回修正，通过；未修改已正确的原生封装。旧课“局部 bbox”说明应结合此精化。
- 新空绘图区毫米单位设置仍有 SPMHUT-48 “Scaled value has been rounded off”；具体触发字段未定位。所有本次要求的尺寸、端点和属性均逐项核对相符，警告未隐藏。
- 本机无可用 PDF 命令行工具/Python PDF 库。Autodesk 自带 Python 3.14 缺少 python3.dll，ABI3 PyMuPDF 无法导入；已把官方便携 Python 3.14.0 与 PyMuPDF 1.28.2 放在 learning/tools 下隔离使用。下载来源/哈希见各工具 install_source.json，不改系统安装。
- Capture 符号创建实操仍未完成。只读调研确认官方文档 doc/orctclsample/TCL_Programmimg_with_OrCAD_Capture_GUI_Interface.html Sample-19 给出 capture -product="OrCAD Capture" Sample-19.tcl，以及 Menu "File::Exit"；本次未实际执行，不记为已学会创建/保存 OLB。用户之后明确只做 PCB，本任务不继续 Capture。
- 本轮使用原生 CLI/SKILL 成功，不代表桌面 native pipe 已恢复。

## 文件与复现

- qmi8610_spec.json：审过的唯一规格与编号表。
- source/：源 SHA/元数据、提取文本及原始 PDF 页面渲染；源 PDF 不改动。
- library/：本次隔离生成的原生文件和 PXML；与公共文件的哈希见 final_validation.json。
- scripts/：read_datasheet.py、qmi8610_create.il、qmi8610_verify.il、qmi8610_placement.il，以及 create02/read/public_read/placement.scr。
- scripts/validate_preview.py、finalize_validation.py：读回数据验收及 PNG 绘制；脚本要求真实 native 导出存在。
- logs/pad、create（失败保留）、create02、reopen、public_reopen、placement：原始输入哈希、启动参数、PID/启动时间、进程结束状态、stdout/stderr/journal、原生报告及测试板。
- validation.json：隔离几何验证；publication.json：发布清单；final_validation.json：公共文件及 48 pins 的最终验证。
- preview.png：可查看的顶视预览。

官方创建入口沿用已验证课程：
- padstack_editor.exe -x 输入.pxml（隔离 library 为工作目录）。
- allegro.exe -product Allegro_performance -safe -nographic -symbol package -s create02.scr -p 日志目录 新文件.dra。
- 重开时使用 -readonly；PSM 实例测试使用新 .brd，无 -symbol。
- .scr 用 errset(load(...))、本任务函数、quit/fillin "yes"。进程级 ALLEGRO_PCBENV 指向相应日志目录，不写全局 pcbenv。

复现创建前必须另建空目录、更新参数路径并检查同名 DRA/PSM/PAD 不存在；axlSaveDesign 的 noConfirm 不能代替外层重名保护。不要直接在已发布公共文件上重放创建脚本。回退时只处理 publication.json 里本次新增且哈希仍匹配的三份文件；不清理其他泛用 LGA16/PAD。

本次笔记及输入、脚本、日志全部保留在 01AIEDA；公共库只新增指定原生文件，未修改真实用户 PCB 工程或全局设置。
