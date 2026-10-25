# 合并原理图Expand不完整的只读诊断

日期2026-10-19。范围仅为源脚本、已生成TSV、原生DSN的CFB文件索引和本地Cadence官方文档；本诊断没有运行Cadence API，没有修改DSN/OLB，也没有调用NULL cast或FlatNet.NewWiresIter。

## 已确定的事实

- `de_capture_helpers.tcl`的verify原版直接调用`$top Expand`却未检查其返回的DboState。后续GetRootOccurrence使用的状态变量不是Expand返回对象，不能证明Expand成功。
- root追加诊断已记录`failed1 code1021 severity2 message ERROR(ORDBDLL-1021): Object Not Found`。所以32个FlatNet/60个pin memberships是计算失败后的部分结果，不能作为完整连通验收。
- 60个membership恰好来自前两页ADC_GPIO与CLOCK_RESET，各30个。页与实例盘点则有六页、80个器件、272个物理pin。
- baseline DSN是标准OLE/CFB文件。只读解析目录，`Views/TOP/Pages`下六个页面流都存在且可按FAT完整读取。其大小分别为ADC_GPIO12415、CLOCK_RESET11159、INTERFACES12631、MCU_SUPPLY24823、POWER12756、USB_CAN20243字节。源码在本目录`read_cfb_directory.py`，结果`dsn_cfb_directory.json`含文件和页面流SHA256。
- DSN与源OLB字节文本中均有23个DE包名以及对应.Normal名字，包括DE_HEADER4.Normal。这仅证明字符串存在，不证明数据库内部对象引用链闭合。
- 实例TSV的80个位号唯一；每个实例的pin热点无重复。GetHotSpot结果是实例局部坐标，不能直接把跨实例相同局部坐标认定为几何短接，须加实例位置/变换。

## 原厂接口依据

`tools/capture/tclscripts/OrCAD_Capture_TclTk_Extensions.pdf`第147页DboState提供Failed、Severity、Code、Message(CString&)；DboSchematic的ReadAllPages在第343页、Expand在354页、NewPage(status,name,pageNumber=-1)在362页。具体Tcl wrapper是否可调用由root安全范围确认，不凭文档签名盲试。

`doc/capinfomodel/dboimnew.html`的Schematic段说明，Schematic网表由页面图形计算，计算不会持续维护，应先Expand，并用IsExpanded检查。FlatNet段说明FlatNet不是持久化实体，计算及Occurrence有效性影响查询结果。因此页面/实例存在与完整FlatNet存在是不同验收条件。

## 下一步定位建议

1. root已获得Expand自己的错误信息，后续检查必须以该状态成功为前提。不要继续把部分net counts写成通过。
2. 第三页INTERFACES首次使用DE_HEADER4.Normal模型，前两页只使用HEADER2/6/8、RES/CAP、XTAL。优先与已成功HEADER6比对设计Cache里的Package、Device、Cell、Normal Part引用，定位Object Not Found；也可由官方PST导出日志给出更直接的缺失对象名。不要先修改有效电路连接。
3. 只读导出六页实际ID/PageNumber，检查NewPage默认-1后的结果及Schematic页面目录索引是否一致。CFB文件结构不是Cadence对象ID文档，本诊断没有把头部hex误解为页ID。
4. 若引用链完整，再检查保存顺序与NewPagesIter遍历期间保存页面是否影响索引；任何修复先在新副本中进行，保存/关闭后用新进程复核Expand成功和272脚覆盖。

目前确定了“Expand失败导致前两页部分网表”，尚未确定底层缺失对象是什么。未把假设写成已修复结论。
