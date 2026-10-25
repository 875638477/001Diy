# Capture 网格工具：参数、边界和验收

本页只记录可复用操作。真实工程的输入、原生导出、坐标计划、日志、候选 XML 和验收记录都放工程自己的工作目录；学习库不保存这些工程数据。完整整理流程见 [缓存、网格与文字整理](capture_cache_grid_text_cleanup.md)。

## 通用工具

- [capture_grid_plan.py](../scripts/capture_grid_plan.py)：纯 Python 标准库的离线几何计划器，不启动 Capture，不读写 DSN。必须明确给输入 XML、同一设计的原生审计目录、全新输出目录和 document-unit 网格。`--pin-spacing-raw` 仅校验原 PinToPin 值，不改变页面比例；`--self-test` 运行四个负向连接检查，不产生工程输出。
- [capture_grid_readonly.tcl](../scripts/capture_grid_readonly.tcl)：只读原生导出，覆盖页面单位、器件、实例引脚的局部／实际 start 与 hotspot、网线顶点、显式 Junction、Port／Global／OffPage 热点及 Alias。`source` 只定义函数；显式调用审计函数后才加载 SDK、打开设计并读取，不调用 Connect、Save、SetLocation 或 MarkModified。
- [capture_dbo_readonly_common.tcl](../scripts/capture_dbo_readonly_common.tcl)：参数化只读助手。SDK 根目录由调用者给出，不包含安装位置、用户名或工程默认路径。

## 使用参数

先冻结原 DSN／库与配置 SHA，在工程内创建独立工作目录。用本机官方 SDK 导出完整 XML，并为同一设计生成原生坐标表。SDK 安装根、公共 helper 位置、DSN、输出目录、网格和显示分母全部由调用者传入。

```tcl
source $GridAuditScript
::CAPGRID::audit $InputDsn $FreshAuditDirectory $CommonHelper $CadenceRoot $GridDoc $GridDenominator
```

若进程已由调用者加载并打开了设计，可先显式初始化助手，再调用：

```tcl
source $CommonHelper
::CAPDB::init $CadenceRoot
source $GridAuditScript
::CAPGRID::auditLoaded $Design $TopSchematic $FreshAuditDirectory $GridDoc $GridDenominator
```

上述函数不自动导出 XML。外部启动器应记录 SDK 版本、输入前后 SHA、进程身份和退出码。不要把其他进程中的数据库对象指针传进来。

```powershell
python capture_grid_plan.py --input-xml $SourceXml --native-audit $NativeAuditDirectory --output-dir $FreshPlanDirectory --grid $GridDoc --pin-spacing-raw $ExpectedPinSpacing
python capture_grid_plan.py --self-test
```

输出目录必须不存在。通用计划器位于学习库时，默认拒绝把输出写回学习目录；只有明确的课程练习才使用 `--allow-learning-exercise-output`。原生审计对应的课程例外是函数最后一个布尔参数，真实工程保持默认值。

## 网格与几何约束

先逐页读 PinToPin、GetDocUnitsPerInch、GetPhysicalGranularity、GetPinToPinScaleFactor 和 IsMetric，结合用户选定的网格分母确定 document-unit 步长。不能把物理 PinToPin 值直接当数据库坐标，也不能用偏好设置代替已有对象的实际坐标检查。Master 在 Pointer snap to grid 勾选时采用 Coarse；未勾选时采用 Fine。不要修改用户全局 Capture.ini 来冒充已经修复已有原理图。

计划器先判断一页是否可以整体平移；其余页面对连接坐标量化，但整件器件以实际 pin hotspot 的共同余数求刚性平移。局部余数不兼容、引脚 start 无法保持上网格或原生坐标与 XML 不符时拒绝生成候选。器件原点与引脚网格有冲突时单列例外，不能再次直接四舍五入原点。库原点重基是另一个需要逐实例证明实际图形不变的步骤。

比较对象包括全部线段的端点接触、无 Junction 交叉、重合、引脚／网络符号对线的附着、端点彼此重合以及显式结点。自由短线只有确认自由端没有 pin、网络符号、Alias、Junction 或其他线段附件，而且延长后没有碰到其他线／引脚／可见器件包络时，才保持方向扩为一个网格；不静默删线。

源 XML 的 SHA 从同一组读取字节计算，结束前再次校验。未知电气对象、未解析可见图元、非直角网线或原生审计不匹配都会拒绝；几何门禁失败只输出审查资料，不写 `grid_candidate.xml`。当前支持标量网线、PlacedInst 的实际标量引脚及 Port／Global／OffPage；总线、BusEntry、DrawnInst、层次块、活动 ConvertView 和其他未实现图元须另扩展后再用，不能默默跳过。已识别的装饰线和文字不由本电气网格阶段重排。

## 原生返回值与显示边界

每个带 DboState 的调用独立检查。NULL 迭代结束、未接 Net／Wire、可选字段未实现与真实读取失败分别写入 ledger。Capture 17.2 的消息包括：1002 为 Function not implemented，1021 为 Object Not Found，1022 为正常迭代结束，1043 为未接任何 Net。PointIsJunction 返回 false／1021 必须与显式 Junction 迭代数据独立核对；不能把其他 API 的同一错误码一律当成功。

默认实例迭代器可能不返回共享或未实例化脚。保留完整 cache／设备的有序脚映射与实例覆盖，以实际实例、原生编译和 PST 分别验收；不要把“cache 比实例多的脚”直接称为隐藏脚或 NC。引脚显示由 UI 管理，不能用零／dirty 包围框或近似文字位置宣称没有重叠。

离线 PASS 只证明计划器声明范围内的几何关系。还要原生导入独立副本、保存、关闭、独立重开、重新导出完整 XML／坐标表，并比较全部物理 `refdes.pin` 网络分区、名称、NC、器件有效属性及有序脚映射。文字和 GUI／PDF 视觉核查独立完成；本方法不授予 ERC、PCB DRC 或生产放行。

## 已做的工具检查

通用计划器有四个独立负向控制：新增端点接触、无结点交叉变成连接、丢失 pin-wire 附件、不同引脚新增同点。`--self-test` 只报告这四项，不能替代具体工程验收。通用 Tcl 的 source-only 检查确认没有加载 DboState／SDK；通用离线工具做过同机参数化重放，具体输入与结果保存在对应工程目录。重命名后的原生 wrapper 是否适用于另一安装或另一设计，仍需现场最小只读验证。
