我的计算机安装了多个版本 目前使用17.2比较合适
cadence 17.2版本的安装目录
C:\Program0\cadence\SPB172
C:\Program0\cadence\LicenseManager172
C:\Program0\cadence\SPBData172\pcbenv
D:\001DIY\005lib\01AIcadence 是 ai接管cadence 路径文件
D:\001DIY\005lib\01brdlib  pcb库路径文件
D:\001DIY\005lib\01captureLib 原理图库路径
D:\001DIY\005lib\01env  环境变量 快捷方式路径
D:\001DIY\005lib\01Pad_lib 焊盘库路径
D:\001DIY\005lib\01Psm_lib 封装库路径
D:\001DIY\005lib\01script_file 用脚本的路径
C:\Program0\SumatraPDF\SumatraPDF.exe  是pdf阅读器的路径


D:\001DIY\061PcieDis\AST2400\AST2400芯片的官方参考设计.pdf
吧AST2400的芯片的原理图库做一下
方案B试试

D:\001DIY\005lib\AUTOlib\ul_AST2400\AllegroV17_2\2026-07-15_11-37-06.bat
allegro打开后一闪而过没有出来封装
bat里面的allegro软件地址我已经指定

打断一下  建议你生成的焊盘和封装 
 封装的封装源  焊盘的焊盘源  都放到01Pad_lib 01Psm_lib 里面  并且bat目录留有备份
 另外bat的名字尽量换成封装的名字 不要用日期

## Allegro 封装交付约定（已按此整理）
- bat 名 = 封装名（无日期）:
  `D:\001DIY\005lib\AUTOlib\ul_AST2400\AllegroV17_2\LFBGA408_19X19.bat`
- bat 工作目录自留备份: `AllegroV17_2\` 与 `AllegroV17_2\backup\`
  （xml / bat / builder.ile / dra / pad / psm）
- 焊盘源 → `D:\001DIY\005lib\01Pad_lib\`  （例: `c16.pad`）
- 封装源 → `D:\001DIY\005lib\01Psm_lib\`  （例: `LFBGA408_19X19.xml` / `.dra` / `.psm`）
- 脚本再生成: `python D:\001DIY\005lib\01AIcadence\ast2400_lib\build_allegro_fp.py`
- 然后双击 `LFBGA408_19X19.bat` 跑 Allegro，自动拷贝到两个库目录

## AST2400 原理图库（方案B 已生成 2026-07-14）
- 源 datasheet: D:\001DIY\061PcieDis\AST2400\ast2400v13.pdf （408-ball LFBGA）
- 工作目录: D:\001DIY\005lib\01AIcadence\ast2400_lib\
- Capture 导入用: D:\001DIY\005lib\01captureLib\AST2400\
  - AST2400_pins.csv （全引脚）
  - sections\AST2400_A_POWER.csv ... H_GPIO_SD_PWM.csv （8分符）
  - AST2400_pin_checklist.txt
- 脚本备份: D:\001DIY\005lib\01script_file\AST2400\
D:\001DIY\005lib\AUTOlib\ul_TPS65217CRSLR
这是我刚刚从 ultra librarian 网站下载的TPS65217CRSLR的原理图库
里面有详细的生成的步骤 你帮我审视一遍  看看能否直接用

 
D:\001DIY\061PcieDis\AST2400\AST2400芯片的官方参考设计.pdf
我需要你按照我提供的原理图生成 的原理图库
按照参考原理图吧U2做相同封装
引脚排布必须一模一样
我是说的是U2 是一个
## 修复 v3.2.2（2026-07-15 15:40）— 按官方参考原理图重生
- 源: `AST2400芯片的官方参考设计.pdf`（EVB DDR3，P05~P08 = U1A~U1D）
- 说明: 参考图里 AST2400 位号是 **U1**（四分符 U1A~D）；你板子上可放成 **U2**，封装脚序与参考一致即可
- 脚本: `ast2400_lib\gen_ul_ast2400_evb.py`（推荐）
- 最新 XML（请用这个 Import）:
  `D:\001DIY\005lib\01captureLib\AST2400\OrcadCaptureXML\2026-07-15_15-40-52.xml`
  （同内容: `AUTOlib\ul_AST2400\OrcadCaptureXML\`）
- 覆盖: U1A/B/C/D = 108/120/88/92，missing=0 / extra=0 / dups=0
- 已含: EVB 左右脚序 + 分区线/说明字 + 10 网格对齐
- 核对清单: `01captureLib\AST2400\AST2400_pin_checklist.txt`（含 L|R 对照）
- 注意: 参考图上的 **U2=DDR3X16 颗粒**，不是 AST2400；若要做 DDR3 库请另说

---

# 本次对话总总结（2026-07-14 ~ 2026-07-15）

## 一、目标
1. 用截图/PDF 资料，让 AI 协助做 Cadence 17.2 原理图库（方案 B：半自动 CSV/脚本/XML）。
2. 以 AST2400（408-ball LFBGA）为主器件建库。
3. 参照 Ultra Librarian 下载包格式（TPS65217CRSLR）生成可 Import 的 Capture XML + Allegro 封装源。
4. 最终要求与官方 EVB 参考原理图一致：仅 U1A / U1B / U1C / U1D 四个分符。

## 二、关键路径
| 用途 | 路径 |
|------|------|
| Cadence 17.2 | C:\Program0\cadence\SPB172 |
| 原理图库 | D:\001DIY\005lib\01captureLib |
| 封装/焊盘 | D:\001DIY\005lib\01Psm_lib 、01Pad_lib |
| AI 工程目录 | D:\001DIY\005lib\01AIcadence |
| AST2400 工作目录 | D:\001DIY\005lib\01AIcadence\ast2400_lib\ |
| UL 同款输出 | D:\001DIY\005lib\AUTOlib\ul_AST2400\ |
| UL 参考样例 | D:\001DIY\005lib\AUTOlib\ul_TPS65217CRSLR\ |
| Datasheet | D:\001DIY\061PcieDis\AST2400\ast2400v13.pdf |
| 官方参考原理图 | D:\001DIY\061PcieDis\AST2400\AST2400芯片的官方参考设计.pdf（EVB DDR3，P05~P08=U1A~U1D） |
| PDF 工具 | C:\Program0\SumatraPDF\sumatrapdf-tool.exe |

## 三、演进过程（版本）
1. 方案 B：从 datasheet 抽 408 脚 → CSV + 8 分符清单（早期 A_POWER…H_GPIO）。
2. UL 同款包：生成 OrcadCaptureXML + AllegroV17_2（复用 TPS 的 builder.ile）。
3. v2：OrCAD 禁止重名 → GND1/GND2…；曾改为 8 功能分符（后弃用）。
4. v3：严格按 EVB 参考 U1A/B/C/D 四页建库，408 脚刚好分完。
5. v3.1：修右侧引脚名与编号重叠（startX 对齐右边框；指向标志=0；框宽 280）。
6. v3.2：按 EVB 逐球指定左右脚序 + 框内分区线/说明字（PCI-Express 等）。
7. 误删恢复：最新 XML 重生并复制到 01captureLib\AST2400。

## 四、当前推荐交付物（请用最新）
- Capture 导入 XML（优先）：
  D:\001DIY\005lib\01captureLib\AST2400\OrcadCaptureXML\2026-07-15_15-40-52.xml
  （同内容也在 AUTOlib\ul_AST2400\OrcadCaptureXML\）
- 引脚表 / 清单：
  ...\AST2400\AST2400_pins.csv
  ...\AST2400\AST2400_pin_checklist.txt（含 L|R 对照）
- Allegro 封装源：
  ...\AST2400\AllegroV17_2\LFBGA408_19X19.xml + builder.ile + *.bat
- 生成脚本（推荐）：
  D:\001DIY\005lib\01AIcadence\ast2400_lib\gen_ul_ast2400_evb.py

### 四分解一览（与 EVB 一致）
| 分符 | 脚数 | 内容 |
|------|------|------|
| U1A | 108 | PCIE + DDR + LPC + I2C + SD |
| U1B | 120 | Flash + UART + MAC + SPI |
| U1C | 88 | VGA / USB / ADC / PWM / Misc |
| U1D | 92 | 电源/地（GND1…） |

## 五、操作步骤（必做）
### Capture 原理图库
1. 删除/覆盖旧的 AST2400.OLB（避免混入旧 8 分符版本）。
2. Capture 17.2 → File → Import → Library XML。
3. 选最新 `2026-07-15_15-40-52.xml`（或时间戳更新的文件）。
4. 另存到 D:\001DIY\005lib\01captureLib\AST2400.OLB。
5. 放置后应只有 U?A / U?B / U?C / U?D 四个分符（位号可改成 U2A~D）。

### Allegro 封装
1. 先加载 Cadence 17.2 环境（allegro.exe 在 PATH）。
2. 双击 AllegroV17_2\*.bat 生成 footprint。
3. 将 pad/psm 拷到 01Pad_lib / 01Psm_lib。
4. 封装名：LFBGA408_19X19（19×19 mm，0.8 mm pitch；焊盘为估算值，量产前对照 ASPEED 封装图复核）。

## 六、Ultra Librarian（TPS65217CRSLR）审视结论
- 可用，但是生成源包，不是现成 .OLB/.dra。
- 已含 AllegroV17_2，版本匹配本机 17.2。
- Capture：Import Library XML；Allegro：跑 bat + builder.ile。
- 注意：EPAD 常标成 NC，原理图应接到 GND；Value 可能写成 B 版而器件是 C 版，脚位一般相同需核对。

## 七、注意事项（重要）
1. OrCAD 引脚名不可重复：同名电源/地必须 GND1、GND2… / IV12D1…（参考图里可同名，库内必须唯一）。
2. 分符数量以 EVB 为准：最终只要 4 个（U1A~D），不要再用早期 8 分符版本。
3. 导入永远选时间戳最新的 XML；旧 OLB/旧 XML 会带回右侧重叠或错误分符。
4. 右侧引脚规则（再改库时务必保持）：
   - 左边：startX=0，hotptX=-30
   - 右边：startX=边框宽，hotptX=边框宽+30
   - IsLeftPointing=0 且 IsRightPointing=0（方向由 start/hotpt 决定，不要设反）
5. 多功能脚：库名尽量跟 EVB 写法（如 GPIOD0/SD2CLK）；板级用哪一功能由网络名体现。
6. U1D / 模拟地 / EPAD：按参考接 AGND/PGND，勿悬空。
7. 封装焊盘尺寸：当前 0.40 mm land / 0.50 mm mask 为工程估算，非官方最终值。
8. 无 STEP 3D：自建 UL 同款包未带 3D；需要可另补。
9. 路径注意：本机 Cadence/Sumatra 在 C:\Program0\...，不要写成 C:\Program Files\...。
10. 误删：关键交付在 AUTOlib\ul_AST2400 与 01captureLib\AST2400；可用 gen_ul_ast2400_ref_fix.py 一键重生。

## 八、尚未完成 / 待办
1. ~~框内分区线 + 说明文字~~ → **v3.2 已合入**（Line + CommentText）。
2. ~~左右脚序与 EVB 一致~~ → **v3.2 已按球号显式指定**；请 Import 后对照 P05~P08 再人工看一眼。
3. Allegro 封装 bat 需在 17.2 环境下实机跑通，并把生成物归档进 01Pad_lib / 01Psm_lib。
4. U1C VGA/ADC 等单侧脚较多时中间空白略大，若要更紧凑可再微调间距。

## 九、相关工具/文件速查
- PDF 转文字/出图：sumatrapdf-tool convert / draw
- 引脚解析：ast2400_lib\parse_ast2400_pins.py 、parse_ref_u1.py
- 库生成：gen_ul_ast2400_evb.py（当前推荐，含分区线+EVB L/R）
- 参考页图：ast2400_lib\ref_pages\p5.png ~ p8.png（U1A~U1D）
- 参考文本：ast2400_lib\ref_design.txt

## 十、一句话结论
AST2400 库 v3.2.2：按官方参考原理图重生；U1A~D 四符 + EVB 左右脚序 + 分区线/说明字 + 10 网格；请用 `2026-07-15_15-40-52.xml` 重新 Import。
