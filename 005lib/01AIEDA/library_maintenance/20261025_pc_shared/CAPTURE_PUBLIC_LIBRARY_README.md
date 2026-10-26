# COMMON_PC公共原理图库维护记录

日期：2026-10-25（Asia/Shanghai）。本记录只说明Capture公库新增、来源迁移和复用验证；写入本阶段记录时13版PCB仍在处理中，不是整工程最终发布回执。

本机库：D:\001DIY\005lib\01captureLib\COMMON_PC.OLB  
新增文件SHA256：F9C8A06886E7B556D2D7F2F5D35B260B26E815240723BC611C20D7B52069EAF2  
原生GetName实际身份：D:\001DIY\005LIB\01CAPTURELIB\COMMON_PC.OLB

## 新增依据和保护范围

对本机原有36个OLB原生导出，完整扫描1865个Package／网络符号；与实际源设计55个共享Package和4个网络符号逐项比较全部有序内容及库级默认值。55包均没有完整可替换公库对象。OFFPAGELEFT-L在既有Capsym／Dream1有相同对象内容，但两库级Defaults不同；GND_SIGNAL与Capsym/GND_A去名后有相同内容，库级Defaults也不同。因此没有据相似外观或同名覆盖旧库，新COMMON_PC包含完整55包和4符号。

原有36个公共OLB未修改，也未覆盖安装目录CAPSYM。原始公库路径／大小／SHA见工程 tools/PUBLIC_OLB_INPUT_MANIFEST.json；38源导出任务的保护回执在工程 w/capture_export_job/。新增COMMON_PC之外的公库保护以这些逐文件SHA及实际作业回执为准，不以文件时间或“程序退出成功”代替。

公共PSM／PAD另有本目录其它维护记录；本Capture记录不代表PCB完成。历史设计、原件和压缩包按用户决定保留。本阶段未删除这些历史原件。

## 已完成的Capture验证

- 新OLB已原生构建并保存，在新进程重开；55个完整Package＋4个网络符号及库级Defaults对照候选全部相同。每个对象内部顺序、针脚、电气标记、图形、字体及属性均保留。
- 24种默认字体的全部14字段和primitive设置已从源设计克隆，并在最终公库真实路径的新进程读取核验。详见 capture_build_report/、capture_public_reopened/DEFAULTS_REOPEN.tsv。
- 工程隔离候选已原生修改941个实例PCB Footprint、231个Cache对象来源及3118个页面实例来源；55个共享包名称／图形保持。独立完整XML和实际PST比较均通过。
- 从最终公库真实路径分别试放R、C和ADL_S_PCH_EXT_4，3／3通过：Package保持55，全Cache保持231，新增缓存数为0；每个试放pin的实际世界起点／热点与原生图形变换精确一致。试放结束丢弃设计，save_calls=0，保护的设计及公库SHA不变。

工程证据根：D:\001DIY\004computer\lga1700\13shared_libraries_pc_20261025。

| 范围 | 工程内相对位置 |
| --- | --- |
| 36公库完整匹配、候选OLB XML及来源母计划 | w/capture_reuse_final/ |
| 新库完整59对象与全部Defaults比较，含6反测 | verification/common_pc_reopened/COMMON_PC_FULL_LIBRARY_REVIEW.json |
| 最小变更冻结计划与Tcl | w/capture_native_frozen/ |
| 原生应用与输入保护 | w/capture_apply_job/job_result.json、w/cn1_report/ |
| 保存后完整XML比较 | verification/xn1/PUBLIC_LIBRARY_XML_REVIEW.json |
| 实际PST比较 | verification/pstn1/PUBLIC_LIBRARY_PST_REVIEW.json |
| 公库不保存试放 | w/place_R/、w/place_C/、w/place_ADL_S_PCH_EXT_4/ |
| 默认封装及1131实例显式覆盖审计 | w/template_default_audit/TEMPLATE_DEFAULT_FOOTPRINT_AUDIT.json |

以上路径记录本阶段证据，不表示后续PCB候选或最终正式设计已发布。

## 模板默认封装的准确范围

1131个已放置实例全部恰有1条显式PCB Footprint，当前工程封装以这些显式属性及冻结映射为准。共享模板保留37个Package级非空默认封装及1个SymbolUserProp级默认PCB Footprint；本轮没有修改任何模板默认，R、C、C_ELEC、L、FB的Package封装默认均为空。

新放置R/C等共享符号时，要填写实际Value和PCB Footprint。试放R/C时原生有效User_Value读取可为未定义状态（例如failed=1/code=1021）；这与现有器件的值丢失不同，不能自动填0或空串代替物料参数。

专用模板也必须明确选实际器件封装：

- HF1004E模板仍默认FAN4P；本工程实例显式使用经核验的 fan4p_pc。二者不能仅凭名字替代。
- DS14185_0模板仍默认TSSOP20；本工程实例显式使用经核验的 tssop20_pc。
- W25Q128JVSIQ是继承的符号模板名称，模板默认WSON8-8X6MM-9P；U18的实际型号及封装沿用电气修正后的显式实例信息，不能从模板名反推型号。
- FootprintName等原AD追溯属性没有随PCB Footprint一起重写，它们不是本轮有效选封装的依据。
- CN1／CN2／CN3原来没有User_Value；迁移时保留原生缺失状态和独立XML中的缺失，不新增空属性。

如果今后要让模板默认也统一到新公库封装，另建逐Package／Cell变更计划，并同步设计Cache和共享OLB，重新验证继承、完整库内容、PST和放置复用。不要直接改已经核验的COMMON_PC来假装本次证明仍适用。

## 方法和脚本

[通用迁移与唯一_pc方法](../../learning/notes/public_shared_library_migration_pc_naming.md)区分符号、实例封装、命名和真实定义替换。通用函数副本和脚本SHA索引见 capture_methods/；它们不自动打开或保存设计。

本次实际工程脚本继续保存在工程 tools/，不将工程参数和大XML复制进学习侧方法目录：analyze_capture_public_reuse.py、build_common_pc_olb.tcl、reopen_common_pc_olb.tcl、review_common_pc_olb.py、compile_capture13_native_plan.py、apply_capture13_public_sources.tcl、canary_common_pc_public_only.tcl。重新运行前应建立新输出目录，并重新固定最新设计／公库SHA；原生保存仅由拥有独立任务会话的调用方执行。