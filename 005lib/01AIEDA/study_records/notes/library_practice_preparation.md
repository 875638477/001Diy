# Cadence／Allegro 现有库案例：只读实践准备

日期：2026-10-17（Asia/Shanghai）  
范围：`D:\001DIY\005lib` 中的 NCP303345 与 HPM6200_BGA116_allegro。  
当前完成项：读取 README、Python 生成器、BAT、SCR、PXML，并独立解析文本核对编号、数量、单位、依赖文件存在性及写入范围。  
未完成项：Cadence 软件生成、现有二进制库内容检查、原理图导入、DRC、实物或制造验证、逐项对照原厂尺寸。**本记录属于静态准备，不计作软件操作练习已通过。**

## 首选案例与比较

首选 **NCP303345 的 Allegro 封装部分**：28 个编号、8 种 PXML 焊盘、Pin 28 异形 Shape Symbol、原始 PDF 和现有二进制成品均能定位，便于衔接教材中的焊盘与封装制作。Capture XML 缺失，原理图部分单独保留为待补输入。

| 项目 | NCP303345 | HPM6200 BGA116 |
| --- | --- | --- |
| 现有放置 SCR | 28 个唯一编号，1～28 | 主版和备选版各 116 个唯一球号 |
| 生成器输入 | 引脚定义直接写在 Python 中；8 个 PXML、2 个 SCR 均在 | 声明的 KiCad 输入路径失效，实际源文件在另一子目录 |
| 原厂 PDF | `AUTOlib\NCP303345\NCP303345-D.PDF` 存在 | 全工作区展开文件中未找到 README 所称 `HPM6200DSV26.pdf` |
| 公共焊盘依赖 | 8 个 `.pad` 和 Pin 28 的 `.ssm` 均存在 | 主版 `BGA025.pad` 存在；备选版 `HPM_BGA025.pad` 未找到 |
| Capture 输入 | README 所称 XML 未找到；已有 OLB 尚未解析 | 本次只准备封装案例，未核查 Capture 引脚 |
| 后续关键事项 | 补 XML、隔离输出路径，再做软件验证 | 修正输入定位、统一焊盘名称与版本，再做软件验证 |

## NCP303345：已核对的输入与编号

主要入口：

- 说明：`01captureLib\NCP303345\README_CN.md`。
- 引脚及生成逻辑：`01AIcadence\ncp303345_lib\gen_ul_ncp303345.py`。
- 路径布局对应的归档生成器：`AUTOlib\NCP303345\02_生成脚本_ncp303345_lib\gen_ul_ncp303345.py`。两个生成器 SHA-256 相同；目录位置影响其输出目标。
- 封装源：`01script_file\NCP303345\PQFN24_4X5_P0D5_483BV.scr`，同目录含 8 个 PXML、Shape SCR 和 BAT。
- 已生成实例：`AUTOlib\ul_NCP303345\AllegroV17_2\` 中有 `.pad/.dra/.psm/.ssm`。本次只确认其存在，没有解析二进制内部内容。
- 原厂资料：`AUTOlib\NCP303345\NCP303345-D.PDF`。README 和生成器引用第 3 页引脚表及第 22 页 CASE 483BV / 98AON13704G；这些属于现有来源声明，本静态准备没有逐项重新核对 PDF 尺寸。

使用 AST 读取生成器的 `PINS` 字面量，没有导入或执行生成器：共 28 项、28 个唯一编号，集合正好是 `1`～`28`。`LEFT + RIGHT` 的符号布局编号同样覆盖这 28 项；封装 SCR 的 28 个放置编号与它们完全一致。这里验证的是文本输入之间一致，尚未验证 OLB 中实际引脚。

| SCR 编号 | 焊盘名 | 实例数量 | PXML 的 BEGIN_LAYER 图形 | PXML 宽×高（mil） |
| --- | --- | ---: | --- | --- |
| 1～7 | `ncp_r54_30` | 7 | RECTANGLE | 21.26 × 11.81 |
| 8～12 | `ncp_r30_54` | 5 | RECTANGLE | 11.81 × 21.26 |
| 13～17 | `ncp_r47_30` | 5 | RECTANGLE | 18.50 × 11.81 |
| 18～24 | `ncp_r30_47` | 7 | RECTANGLE | 11.81 × 18.50 |
| 25 | `ncp_ep25` | 1 | RECTANGLE | 82.68 × 73.23 |
| 26 | `ncp_ep26` | 1 | RECTANGLE | 53.15 × 67.32 |
| 27 | `ncp_ep27` | 1 | RECTANGLE | 19.69 × 7.87 |
| 28 | `ncp_ep28` | 1 | SHAPE_SYMBOL | 138.58 × 55.91（外接尺寸字段） |

8 个 PXML 都声明 `SMD_PIN`、`MILS`、accuracy `2`，并包含 `BEGIN_LAYER`、`SOLDERMASK_TOP`、`PASTEMASK_TOP`。主封装和 Shape SCR 则声明 `Millimeter`、accuracy `4`。尺寸换算采用 `1 mil = 0.0254 mm`；不能把 PXML 数值直接作为 SCR 中的毫米值使用。

Pin 28 的铜层通过 `SHAPE_SYMBOL` 引用 `ncp_ep28_shape`。其 Shape SCR 使用毫米坐标绘制带台阶的多边形；公共依赖 `01Psm_lib\ncp_ep28_shape.ssm` 存在。PXML 的宽高字段不是完整异形轮廓，后续必须连同 Shape Symbol 一起核查。8 个所需 `.pad` 均在 `01Pad_lib` 中存在，主 `.dra/.psm` 也在 `01Psm_lib` 中存在；文件存在不等于内部图形、尺寸或版本已符合规格书。

## NCP303345：待补输入与命令影响

README 指定导入 `OrcadCaptureXML\2026-09-07_16-28-33.xml`。本次以 `rg --files --hidden --no-ignore` 搜索整个工作区展开文件，未找到该文件，也未找到路径中含 NCP303345 的其他 `.xml`；`01captureLib\NCP303345\OrcadCaptureXML` 当前为空。已有 `2026-09-07_16-06-36.OLB`，不能代替缺失 XML 的文本核对证据。本次没有搜索其他 RAR／ZIP 内部，也没有重新生成 XML。

生成器通过脚本所在位置推导 `ARCHIVE → AUTOLIB → LIB_ROOT`：

| 生成器位置 | 静态推导出的 LIB_ROOT | 影响 |
| --- | --- | --- |
| `01AIcadence\ncp303345_lib\gen_ul_ncp303345.py` | `D:\001DIY` | 会把 Capture、脚本、AI 副本等输出写向当前工作区之外；PAD／PSM 路径也据此生成 |
| `AUTOlib\NCP303345\02_生成脚本_ncp303345_lib\gen_ul_ncp303345.py` | `D:\001DIY\005lib` | 对应当前库目录，但仍会覆盖多个现有生成文件、README 与脚本副本 |

因此不能直接在 `01AIcadence` 副本位置运行它。这个结论来自代码路径表达式的静态解释，没有试运行。

现有 BAT 中的生成命令包括 `padstack_editor.exe -x <名称>.pxml`、`allegro.exe -nograph -s ncp_ep28_shape.scr`、`allegro.exe -nograph -s PQFN24_4X5_P0D5_483BV.scr`。这些命令**本次均未执行**。BAT 还会删除当前目录中的旧 Shape／封装输出，并用 `copy /Y` 覆盖 `01Pad_lib`、`01Psm_lib` 和归档副本；当前不能把它作为无副作用的“检查命令”。

## HPM6200：已核对与保留问题

`AUTOlib\HPM6200_BGA116_allegro\gen_hpm6200_bga116.py` 声明的输入是其父目录下的 `HPM_footprints.pretty\BGA116 _13x13_7.0x7.0mm.kicad_mod`，该路径不存在。实际源文件在：

`AUTOlib\HPM_LIB_20251229\HPM_footprints.pretty\BGA116 _13x13_7.0x7.0mm.kicad_mod`

独立解析该源文件，得到 116 个 SMD pad、116 个唯一球号，每个 size 字段为 `0.25 × 0.25`，坐标值范围为 X／Y 各 `-3.0`～`3.0`。主 SCR 同样是 116 个唯一球号，其 `pick` 坐标与该源文件逐项相同；无编号差异或文本坐标差异。两个 SCR 都使用 `Millimeter`、accuracy `4`。这些只是文本核对，尚未验证 Allegro 对 `offsetx/offsety` 与 `pick` 的实际解释、坐标方向、A1 方位或封装引脚电气映射。

存在两套焊盘名称：

- 主版 `BGA116_7x7_P0d5.scr` 使用 `BGA025`，BAT 也检查 `01Pad_lib\BGA025.pad`；实际公共文件 `bga025.pad` 存在，Windows 文件名大小写不影响定位。
- 备选版 `HPM6200_BGA116_7x7_P0d5.scr` 使用 `HPM_BGA025`，公共库中未找到同名 `.pad`。
- 同目录 `BGA025.pxml` 的内部 `<padstackname>` 实际是 `HPM_BGA025`，单位 `MILS`，accuracy `2`，铜层圆宽高 `9.84` mil。不能因文件名叫 BGA025.pxml，就推断它描述的内部名称和公共 BGA025.pad 一致；本次也未解析公共二进制 PAD 来比较图形。

KiCad 源文件还标注 `(attr through_hole)`，而 pad 条目本身是 `smd`；暂保留为源文件属性一致性待复核。README 所称原厂 `HPM6200DSV26.pdf` 在全工作区展开文件中未找到，不能完成原厂图纸尺寸复核。

HPM 的 Python 生成器会改写本目录 SCR、BAT 和 README；现有 BAT 会启动 Allegro，并用 `copy /Y` 覆盖公共 `01Psm_lib` 中的 DRA／PSM。公共与案例目录中的同名 DRA、PSM 的 SHA-256 均不相同，说明有不同二进制副本；尚未判断几何差异或哪一版较新，不能将它们当作同一版本的验证结果。

## 本地 Cadence 路径确认

只读确认以下路径存在，未启动程序：

- `C:\Program0\Cadence\spb172\tools\bin\allegro.exe`
- `C:\Program0\Cadence\spb172\tools\bin\padstack_editor.exe`
- `C:\Program0\Cadence\spb172\doc\algrolibdev\chap1.html`，标题为 `Defining and Developing Libraries -- 1`，正文入口为 Library Development Process。

这给后续本地软件与官方帮助检查提供了入口，未确认许可证可用性、程序可启动性或特定命令成功。

## 下次实践起点与通过条件

1. 从 NCP303345 开始，先对照原厂 PDF 的引脚表与 land pattern，逐项核查 28 个编号及尺寸、方向、Pin 28 台阶轮廓；记录具体页码和结论。
2. 在学习记录内的独立实验目录准备输入副本，明确输出全部留在实验目录，再补齐 Capture XML；不直接运行会写公共库的现有生成器或 BAT。
3. 执行软件生成时分别记录命令、Cadence 版本、日志、实际输出文件与截图；未到这一步前，状态维持“静态准备完成”。
4. 检查软件中的 28 个引脚、焊盘层与 Shape 依赖、原点和方向，确认生成无报错；再验证 Capture 符号到 PCB 封装的脚号映射。最终入公共库应以这些检查结果为依据。

## 可追溯证据

[结构化静态检查结果](../evidence/library_practice_preparation.json) 保存了每个放置编号、坐标、焊盘名、PXML 各层字段、文件路径、大小、SHA-256、BAT 写入相关行号和生成器路径推导。只读检查脚本使用 AST／XML／正则解析，没有导入现有生成器，也没有启动 Cadence。
