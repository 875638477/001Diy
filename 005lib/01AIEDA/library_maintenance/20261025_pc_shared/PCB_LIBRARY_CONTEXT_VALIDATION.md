# 用实际工程上下文校验公共PCB封装

PCB内缓存与公共PSM比较时，要使用同一设计单位、精度、实际铜层顺序，以及工程拥有的字体参数表。不同环境里的 textBlock 编号对应不同字符宽度、间距与线宽；即使同一个PSM，文字边界也可能不同。不能因此忽略全部字体字段，也不能修改工程的字体表来迎合空模板。

先在新进程只读导出实际工程完整缓存、全部字体槽参数与文件SHA。对原有定义，比较实际源缓存的完整物理图、属性和字体；对新名字，在独立空板从公共psmpath/padpath冷加载一次，再比较完整原生图。公共PAD的制造字段可复用此前完整原生XML，但必须重新绑定当前PAD文件和XML原件的SHA，名字或外形相同都不能代替制造字段校验。

本案工程使用mils、精度2、TOP/L2/L3/BOTTOM四铜层。原49AF板与最终迁移候选的完整64槽字体参数表字节相同，SHA为 `D28EEA764D760E1801DE7961A2DA275A1E4D38EE45DA6E84D9A3B5C6552B05C8`。将这份原表复制到每个独立空fixture后，只读加载新公共封装；原工程与公共库本体均不修改。使用官方 `axlDBTextBlockCreate` 分配相同槽号，`axlSetParam` 设置字符几何，`axlDBTextBlockSetName` 还原用户名字，逐槽比较完整 `p->??`。保留首次默认空模板的字体差异报告，不能把失败覆盖成通过。

SPB17.2 的 `axlGetParam("paramTextBlock:17")` 在槽不存在时可能返回只有 `objType` 的真值占位对象。必须再检查 `p->name` 是否为请求的槽号，不能仅凭返回值非nil判断槽已存在。新槽创建后仍应严格检查其完整参数，不跳过实际字体字段。

脚本：`prepare_project8_mils2_cold.py` 准备8个新目标的同单位/铜层冷审计；`prepare_project6_mainfont_cold.py`、`prepare_project6_mainfont_v2.py` 准备6个依赖工程字体环境的补充冷审计；`review_all59_final_cache_v2.py` 合并51个保留源缓存、2个已匹配的精确clone和6个完整上下文匹配的定义。执行结果只以各次新输出中的原生COMPLETE、源文件SHA保护和独立比较报告为准；脚本准备完成不等于校验通过。

本机官方依据：`SPB172/doc/algroskill/04parmgt.html#1120504`、`#1109729`、`#1148454`；字体字段见 `02dbdesc.html#606032`。缓存校验不替代全引脚、实际连接分区、走线铜、规则或制造DRC检查。
