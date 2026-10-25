# 通用工具保留、工程证据归档与迁移

学习库保留方法、参数化工具及合成小样；真实设计、材料分类、逐位号计划、坐标、运行日志和验收结果留在 `<工程根>`。脚本仅有参数还不等于通用：固定安装路径、环境变量、位号、预期数量、图形索引或旧运行目录也要检查。来源脚本SHA和目标工具映射见[本次小体积保留清单](../reports/reusable_tool_retention_20261024.json)；它是工具保留记录，不是工程验收。

## 已有工具继续复用

| 功能 | 通用入口与边界 |
| --- | --- |
| Cache盘点、严格／有条件合并、来源重绑、配套库比较 | [缓存与来源方法](capture_cache_reuse_and_origin_rebase_xml.md)及`capture_xml_tools`。有条件默认值物化仍需原生effective查询；raw Package属性不证明实例有效值。 |
| 电气半网格及完整连接关系 | [网格工具](capture_grid_tools_portable.md)。同版本原生表、明确单位、独立原生重开与PST都是单独门禁。 |
| 原生实例仿射及文字几何 | [文字方法](capture_text_geometry_and_readability.md)。旋转／镜像优先使用实际native frames；旧原点重基工具明确拒绝未支持的非零姿态。 |
| 用户库优先、双端模板与晶振schema | [模板共享方法](capture_user_library_first_templates.md)。原库只读；材料／脚号分类及例外配置属工程；保实际脚数、类型、Global和Name显示状态。 |
| PST脚声明计划与完整物理连接／器件比较 | [预置计划生成器](../scripts/generate_pst_pin_declaration_plan.py)、[连接比较](../scripts/compare_pst_connectivity.py)、[器件比较](../scripts/compare_pst_parts.py)、[有界声明比较](../scripts/compare_pst_parts_bounded.py)。先由源／目标XML预测，不能从失败PST反推白名单。 |
| 实际铜、via接触与保铜导入 | [铜皮与电源避让方法](allegro_shape_contact_and_power_voiding.md)。源作用域、区域坐标、弧解释校准、私有库环境和规则审计回调属工程，不能把旧case启动器直接当通用工具。 |

## 255字符网表快照与成功后发布

新通用入口为[netlist255说明](../scripts/netlist255/README.md)、[导出](../scripts/netlist255/export_pst255.ps1)和[发布](../scripts/netlist255/publish_pst255.ps1)。SourceDsn、ConfigFile、OutputRoot、发布目录、ExporterFile及CadenceRoot均明确给出，没有工程或安装根默认值。

导出器只把已保存DSN复制到新运行目录，核复制前后SHA后调用writer；原生包装可改变快照元数据，不能直接包装唯一源件。要求writer退出、日志、三份非空PST和源SHA保持。发布器使用独占锁，接受本次返回的报告；先验证再切换活动输出，保留旧目录，发布失败保留旧网表。源目录、配置、导出程序和运行输出不能被包含在发布目录中。

工具不设置Capture菜单默认值，也不包含未保存界面编辑；GUI中仍须检查PCB页签→Setup→Device/Net/Pin name char limit=255。OPJ、CFG和工程私有库不是可随意删除的垃圾。生成、连接比较、PCB导入、铜分区、DRC与制造分别验收，见[网表排错](capture_allegro_netlist_troubleshooting.md)。

## 显式文件清单的无损归档

[evidence_archive.py](../scripts/evidence_archive.py)只支持create、verify、restore，不删除原文件、不递归选择工程。选择JSON只含POSIX相对文件名数组，或`{"files":[...]}`；不接受目录、通配符、父目录跳转、符号链接／reparse、大小写冲突或含糊Windows名称。

```powershell
python evidence_archive.py create --root $ProjectRun --selection $SelectionJson --archive $NewZip
python evidence_archive.py verify --archive $NewZip
python evidence_archive.py restore --archive $NewZip --destination $NewRestoreDirectory
```

归档内嵌每成员SHA256、大小、相对路径与mtime_ns；打包前后复核源件，ZIP逐成员CRC/SHA验证。恢复目录必须全新，不覆盖任何已有文件，恢复后再比较字节和时间戳。保证范围是文件内容、相对路径和记录的时间戳，不承诺NTFS ACL或替代数据流。

先明确保护原设计、唯一原厂PDF／异常日志、AD编译pin-net证据、特殊映射计划、原始FAIL、最终有界结论与重建源码。可重生的大XML、字体轮廓及原生几何转储可先做无损归档，再由当前用户授权的工程清理流程逐文件核SHA移除散件。本通用工具没有compact或删除入口；不把归档成功当作删除许可。

工程专用清理器的删除计划、进程／读者退出门禁、最终发布SHA、保留文件前后比较和精确删除账本仍留工程。归档脚本的来源根可能已清理；来源SHA证明当时读到的代码，不承诺所有旧case能直接重放。要重跑需按保留配置恢复目录、依赖与输入，不修改旧FAIL伪装通过。

## 打包、路径与验证范围

先完成文档及元数据再生成最终manifest和ZIP，避免打包期间文件变化。文件移到不同目录时按新文档位置重算相对链接；根转换记录中的链接不能原样用于更深层的随包副本。原生readback若在长工作路径异常，可用短ASCII独立目录对照同输入／参数的完整流程，保留失败证据；短路径成功不是官方固定限长的证明。

显式PinDP在官方保存重开XML中应优先于默认预览偏移；SDK迭代器空不能当作不存在，也不能伪造直接SDK锚点读数。只删除冗余外框图元仍要核真实frames、pin hot/start、显示与派生OLB，再做试放。此类方法已收在[模板方法](capture_user_library_first_templates.md)与[引脚覆盖限制](capture_generic_symbol_pin_override_limits.md)，本轮没有为清理重构整个scene或迁入工程渲染结果。

## 本地小样验证

本轮归档测试覆盖Unicode／空文件、源件保留、CRC与SHA、精确恢复、拒绝覆盖、路径穿越和CRC有效但内容被篡改的反测。网表测试采用明确的模拟writer，覆盖成功发布、失败保留活动输出、外部源件变化、并发锁、危险目录重叠及PowerShell语法。没有启动Cadence；不把模拟后端通过称为新环境原生／许可验证。

自测入口：[归档小样](../scripts/selftest_evidence_archive.py)、[模拟网表小样](../scripts/netlist255/selftest.ps1)。输出参数必须是全新的合成测试目录。真实工程运行结果始终输出到工程根。
