import pathlib,json
R=pathlib.Path(r"D:\001DIY\005lib\01AIEDA\learning\examples\lessonHI_38_50_20261021\engineering_mcu");note=R.parents[2]/"notes/lessonHI_mcu_20261021.md"
s=note.read_text(encoding="utf-8").replace('[USB v6](../examples/lessonHI_38_50_20261021/engineering_mcu/plans/usb_critical_routes_v6.json)','[USB v7](../examples/lessonHI_38_50_20261021/engineering_mcu/plans/usb_critical_routes_v7.json)')
s=s.replace('v6只做对应最小修正，正式结果仍需新进程读回。USB/GPIO当下为已做实际铜几何预审、待原生验证方案。','v6只做对应最小修正，其原生新进程读回和独立82项专项检查已通过，详见第11节。USB/GPIO当下为已做实际铜几何预审、待原生验证方案。')
s+="""

## 11. MCU6正式检查点：两板独立82项通过

本节是MCU局部检查点，尚余112处最少连接，不是完整HI布线入口。原生读取后导出保存到immutable checkpoint，本专项另存关键输入副本与hash，详见[独立报告](../examples/lessonHI_38_50_20261021/engineering_mcu/review/mcu6_independent_native_review.json)和[复核脚本](../examples/lessonHI_38_50_20261021/engineering_mcu/review_mcu6_native.py)。

| 项目 | 四层 | 两层 |
| --- | --- | --- |
| 检查点 | inventory/checkpoints/mcu_4L_b006 | inventory/checkpoints/mcu_2L_b006 |
| 独立检查 | 41/41 | 41/41 |
| 原生状态 | 80件/69网、DRC0且current | 80件/69网、DRC0且current |
| MCU6计划铜 | 67段全部几何覆盖、12via准确 | 同左 |
| quiet实际层/面积 | L2、62.31 mm² | BOTTOM、62.31 mm² |
| 单via负测试 | 6组正/负端点、3guard成功，恢复0DRC | 同左 |

HSE_CASE4地线被native在Y1.2汇入的y38.9处分割为36→38.9→40.8；独立检查按同宽同网同层线段并集核整个计划区间覆盖，不把正常CAD分段错判缺线。并检查三处器件移动、quiet真实polygon、应用地真实void/无重叠及quiet via实际每层铜。

实际铜polygon包含圆弧，采用本机Cadence 17.2官方algroskill/20plyopr.html中vertices说明：半径属于前一点到本点的段，正负表示圆心竖轴左右侧；不把半径丢掉当直边。独立展开每弧最大弦高误差0.00002 mm，实际global面积与native打印面积差约0.004—0.006 mm²，归于几何量化/打印与离散口径，采用0.01 mm²面积核对容限；island无圆弧，面积误差为数值舍入。详见[圆弧展开核验](../examples/lessonHI_38_50_20261021/engineering_mcu/review/mcu6_native_polygon_flattening_check.json)。这不把弦高精度说成板厂制造公差。

还发现两层旧normalized.vias[].pads显示L2/L3，但原始physical_pad_layers.tsv仅TOP/BOTTOM。实际crosssection没有内层，本专项按真实逐层pad文件核验，不把normalizer盲点解释为两层板额外铜层。已通知原生执行者修后续normalizer，保留旧immutable checkpoint身份，不静默改历史证据。

USB首次原生执行使用v6中的“L28_VIA030_C060_OR_VERIFIED_TENTED_PRIVATE_VARIANT”占位选择文字，axlDBCreateVia返回nil，执行停止、源稳态未保存为错误板。该字符串不是软件里真实存在的封装，是本专项交可执行方案时的失误；现[USB7](../examples/lessonHI_38_50_20261021/engineering_mcu/plans/usb_critical_routes_v7.json)四枚via均用准确名字L28_VIA030_C060，几何没有改变，且保留[映射/身份](../examples/lessonHI_38_50_20261021/engineering_mcu/review/usb_v6_native_adapter_mapping.json)。以后“待选A或B”只放purpose/prerequisites，执行字段必须是已盘点真实对象。tented实际mask/artwork验证仍独立保留。
"""
note.write_text(s,encoding="utf-8");print("note updated",note.stat().st_size)
