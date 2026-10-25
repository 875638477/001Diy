# 第26课 Capture 网络导出与 PCB ECO 原生后端

2026-10-19，Asia/Shanghai。**原生网表、BRD导入、ECO、逆向VIEW/SWP比较已通过，1578项独立检查通过。** 权威DSN采用一页容纳六个电路模块：baseline为 [de_integrated_single.dsn](../examples/de_15_26_20261019/native/de_integrated_single.dsn)，ECO为 [de_integrated_eco_final.dsn](../examples/de_15_26_20261019/native/de_integrated_eco_final.dsn)。初次六页设计的包装失败，诊断产物不作为有效工程。Capture GUI完整ERC与SWP应用仍待验。

正式后端以 `native_flow_final` 为准。R19/R20的source_description已同步为3.3k 1%，原生DSN属性见 [properties_eco.tsv](../logs/de_15_26_20261019/properties_eco.tsv)；本次使用修正后的DSN重新执行全部8个原生步骤与1578项检查。旧 `native_flow` 保留作属性说明修正前的历史，不作为当前DSN的最新验收。

## 正式工程结果

| 项目 | Baseline | ECO |
| --- | --- | --- |
| 原生PST导出、netrev导入、独立只读重开 | 全部exit0 | 全部exit0 |
| 元件与物理针 | 80件，272针 | 80件，272针 |
| 已连接针与网络 | 266针，69网 | 266针，69网 |
| 显式NC | 6针 | 6针 |
| 原生BRD | [DE_BASELINE.brd](../examples/de_15_26_20261019/native_flow_final/DE_BASELINE.brd) | [DE_ECO.brd](../examples/de_15_26_20261019/native_flow_final/DE_ECO.brd) |
| 实际放置symbol | 0 | 0 |

两版均以原需求JSON→原生PST→全新进程BRD查询逐一核对refdes、每个物理针、网络、封装和值。JSON中的null代表显式NC，统一与BRD“无网络”比较。全部1578项通过，见[独立比较](../examples/de_15_26_20261019/native_flow_final/independent_compare.json)；完整8个原生进程的PID、时间、命令与exit0见[流程结果](../examples/de_15_26_20261019/native_flow_final/flow_result.json)。DSN交付原件哈希在运行前后相同。

ECO只产生这四处逻辑变化：R19与R20各从2.2k改为3.3k；J13.7从GPIO_PB8改到GPIO_PB9，J13.8从GPIO_PB9改到GPIO_PB8。MCU物理45/46脚网络保持不变，没有增删元件或其他pin/net变化。原生 [eco.txt](../examples/de_15_26_20261019/native_flow_final/logs/import_eco/eco.txt)报告2个net变化、1个新component definition、2个component变化、2个slot属性新增，共7条内部数据库变更；新增definition与slot属性随电阻VALUE引起的primitive换型产生，不等于新增元件。

从ECO BRD真实导出的四VIEW文件及 [DE_ECO.swp](../examples/de_15_26_20261019/native_flow_final/feedback/DE_ECO.swp)已保存。SWP只有Flags/DesignName，没有CHANGEREF、PINSWAP、GATESWAP或属性差异节，证明导入后的实际BRD与ECO DSN/PST同步。两个BRD目前是含全部逻辑元件的导入基线；未放置/布线，DRC=0不能解释为布局或制造验收完成。

## 实际层名与后续层叠边界

原生只读 `axlXSectionGet(nil 'all)`分别导出baseline和ECO的物理层序，两者完全一致：position1为TOP、position2为未命名DIELECTRIC、position3为BOTTOM，外侧导体对应 `ETCH/TOP` 与 `ETCH/BOTTOM`，没有INNER_LAYER旧名。原始证据为 [baseline cross_section.tsv](../examples/de_15_26_20261019/native_flow_final/baseline_readback/cross_section.tsv)与 [ECO cross_section.tsv](../examples/de_15_26_20261019/native_flow_final/eco_readback/cross_section.tsv)，汇总见 [native_layer_evidence.json](../examples/de_15_26_20261019/native_flow_final/native_layer_evidence.json)。

这是netrev新板的默认逻辑承载层结构，只确认TOP→BOTTOM命名和ECO未意外改变层序。实际板厚、介质、铜厚、材料、阻抗及生产层数尚未定义或验收，后续第28课另行建立制造层叠；不据此宣称已完成两层或四层板设计。

## 已验证的原生通道

`pstswp.exe`直接读取磁盘 DSN，产生 `pstchip.dat`、`pstxprt.dat`、`pstxnet.dat`；`netrev.exe`直接把这些文件导入新的 BRD 或既有 BRD 的副本。两者是安装的 Cadence 原生程序，Python 承担启动、日志保存和独立比较，不生成或补写 CAD 网表内容。

```text
pstswp.exe -pst -d DE_CONTROL.dsn -n netlist -c allegro.cfg -v 3 -l 255 -j "PCB Footprint"
netrev.exe -n -e -i netlist DE_BASELINE.brd
netrev.exe -e -i netlist_v2 DE_BASELINE.brd DE_ECO.brd
genfeedformat.exe -x -b DE_ECO.brd -o feedback
pstswp.exe -swp -d DE_CONTROL.dsn -n feedback -s DE_ECO.swp -c allegro.cfg -hpath HPathForCollision -backwd
```

`-e`把缺失 footprint 当作错误；不使用关闭 DRC 或忽略固定对象的参数。隔离 PCB 环境仍须先 `source $TELENV`，再设置本学习目录中的 psmpath、padpath。只写两行路径而省略全局默认环境，会使 netrev 无法找到 `allegro_smi_modules.txt`；失败和修复均保留在 staging。

基线与 ECO DSN 各复制到独立目录并采用同一个文件基名 `DE_CONTROL.dsn`，以免仅改文件名就引入 ROOT_DRAWING/C_PATH 差异。用户交付的 DSN 在原处不被网表器修改。所有新文件、进程工作目录、TMP/TEMP 和 PCB 环境均在 01AIEDA 内。

## 库依赖验收

独立学习库位于 [library](../examples/de_15_26_20261019/library)。[准备库封装清单](../examples/de_15_26_20261019/selected_footprints.json)包含19种通过原生装载的封装；当前电路实际使用18种，见[实际使用清单](../examples/de_15_26_20261019/used_footprints.json)，SMB只是未采用TVS的候选。原生 Allegro 仅使用此目录中的 PSM/PAD 装载19种封装并保存 [dependencies_verified.brd](../examples/de_15_26_20261019/dependencies_verified.brd)，全新只读进程重开后的 516 行 pin/layer 查询与保存后输出相同。[独立验收](../examples/de_15_26_20261019/dependency_validation.json)共 717 项通过。

| 类型 | 使用的原生封装 | 已核对内容 |
| --- | --- | --- |
| MCU | l09_stm32f103c8_lqfp48 | B9原厂依据；1至48脚、0.5mm pitch、native铜尺寸与位置 |
| USB Type C | l10_gct_usb4105_gf_a_12land | B10原厂依据；12信号/供电land、4个SH电气脚、2个无编号NPTH，编号含合并land名 |
| 小型器件 | sot23-3、sot23-5、sot23-6、so8 | 原库学习副本；针数/编号/实际铜尺寸和库依赖 |
| 无源及二极管 | 0603、0805、1206、do-214ac_sma、do-214aa_smb | 1/2脚、铜尺寸、SMD层、原生装载 |
| 教学接口 | pin02/03/04/06/08_2d54MM_1xN | 逐脚编号、2.54mm pitch、PTH，2/3/4/8孔1.0mm、6孔0.762mm |
| 晶体 | de_abm3b_5032 | ABM3B原厂Rev U页3 TOP VIEW；1左下、2右下、3右上、4左上；1/3谐振、2/4接地；land1.8×1.2mm，中心x±2.0/y±1.2 |
| 电感 | de_xal6060_2land | Coilcraft文档887-4 2026-02-25页4；land1.43×5.50mm、中心距4.04mm；本地pin1右侧短引线连接BUCK_SW、pin2左侧连接V5；height6.1mm |
| 极性储能电容 | de_capradial_6d3_p2d5 | 采购教学包络；1为正极、2为负极、pitch2.5mm、body最大6.3mm、height11mm；实际MPN与引线/孔匹配待确定 |

通用 SOT/SO8/无源公库副本的“原生几何通过”不等于已经对每个最终 MPN 的厂家推荐 land pattern 完成制造认证。掩膜每边0.05mm和1:1锡膏属于教学定义，需要装配工艺审查。电容采购包络不能直接作为已选实料制造释放。其余未选候选和额外header别名保留作学习历史，不进入19种最终选用清单。

## 连接与 ECO 的判定方法

原生导出先验实际退出码和 netlist.log，不只检查 DAT 文件是否出现。随后在全新 Allegro 只读进程中查询所有 component、component pin、net，包括尚未放置的逻辑元件。按 refdes/pin 比较 PST→BRD 的完整集合与每个网络，再比较 baseline→ECO 的确切属性/引脚变化；禁止把不相干的改动默认为正常。

逆向 `genfeedformat` 从实际 BRD 提取四个 VIEW 文件，再由 pstswp 对照真实 PST 生成 SWP。无差异时应只有 Flags/DesignName，不应出现 CHANGEREF、PINSWAP 或属性差异节。逆向 SWP 输出证明比较流程已运行；它与在 Capture GUI 内执行 Apply/Update Schematic 是不同的验收步骤。

## ERC 范围

本机 `Ercdx.exe`为 DE-HDL ERC-DX，不能把它的存在当作 Capture DSN 独立 ERC。Capture 官方 17.2 命令行参考没有独立 ERC 参数；公开数据库 Tcl 文档包含 ERC 标记读写以及 customDRC 框架，后者遍历对象并调用自定义规则。`batch_drc.exe`是 PCB 端。当前证据支持自定义引脚/连接/供电规则、pstswp 原生物理包装和 netrev 检查；**Capture GUI 完整 ERC 仍待验**。

## 原生失败与修正

1. C11历史空设计输入 pstswp，真实返回 ORCAP-36029“无可包装组件”；随后用 C14最终设计副本验证 PST→BRD 正常通道，netrev 无错误/疏漏/警告。
2. 初次 dependency SKILL 生成器少闭合 foreach。Allegro reader补括号后继续执行，最后 exit3 并写出 MiniDump/SAV；该源文件和产物已隔离在 [失败记录](../staging/de_15_26_20261019/dependency_load01_failed_artifacts/incident.md)。未把异常批次保存的板当作成功。当前生成入口增加括号/字符串预检，修正后的独立批次均正常退出。
3. integrated v1及两次六页变体的PST包装报告SPCODD-228/53/391。各页wire几何实际已保存，但原生flatten/packaging只得到最后页相关连通；单页80件设计在独立重开与PST包装中全部266个连接通过，故采用单页作为权威，六模块结构保留在原理图分组与课程说明。六页原生SDK原因未解决，不写成已完成多页发布。下游netrev仍可能读入部分DAT并exit0，因此[初次预检板](../staging/de_15_26_20261019/native_preflight/README_FAILED.md)被排除。
4. 权威单页的ECO打开时曾遇到NextPage对象非NULL但DboState3969；先取得GetRootOccurrence再创建页面迭代器后状态为0，随后编辑与独立重开验证通过。没有对NULL对象做强制转换。
5. 正式逆向SWP正常生成，但stderr尝试解压缺失的feedbackview.cdsz后回退四DAT；全部四VIEW加载与完整比较正常结束、exit0，此信息保留，不称全程无告警。

## 主要资料

- 本机官方 `doc/ncoms/nchap.html#netrev`：批处理参数与传统 Capture 三文件流。
- 本机官方 `doc/gcoms/gchap.html#genfeedformat`：BRD→VIEW文件与输出目录。
- 本机官方 `doc/cap_ug/Back_Annotation_from_PCB_Editor.html`：VIEW→PST比较→SWP→Capture更新的四步，以及 pxlBA.txt 属性配置。
- 本机官方 `doc/algroskill/02dbdesc.html`：component、pin、net对象，包括未放置逻辑pin。
- 本机官方 `tools/capture/tclscripts/capDRCFramework/tcl/capProcessDRC.tcl`：customDRC遍历与回调范围。
- [Cadence社区批量网表命令](https://community.cadence.com/cadence_technology_forums/pcb-design/f/pcb-design/14232/batch-netlisting-from-orcad-capture)：命令格式线索；可用性以本机原生实际执行为准。
- [Cadence社区反标脚本讨论](https://community.cadence.com/cadence_technology_forums/pcb-design/f/allegro-x-capture-cis/65127/back-annotation-via-a-tcl-script)：VIEW/SWP命令线索及生成与应用SWP的区别；本地版本结果单独记录。
