import pathlib,json,hashlib
G=pathlib.Path(__file__).resolve().parents[1]
R=G.parents[2]
report=G/'review/native_final_report.json'
assert report.exists(), 'Require final native report before updating completion claims'
for variant in ('4L','2L'):
    assert (G/f'current/G_{variant}_LAYOUT_v1.brd').exists()
def put(p,s):p.write_text(s,encoding='utf-8',newline='\n')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest().upper()
note=R/'learning/notes/lessonG_30_37_20261020.md'
s=note.read_text(encoding='utf-8-sig')
start=s.index('状态：')
end=s.index('\n',start)
s=s[:start]+'2026-10-20启动，2026-10-21整理完成。状态：**第30—37课已完成本文声明的资料、工程布局、原生CAD实操与保存重开验收；整板布线和制造/实物验证仍待后续。**'+s[end:]
s=s.replace('三组MCU去耦计划增加真实局部铜和地参考演示','三组MCU去耦已增加真实局部铜、C16储能支路和地参考演示')
s=s.replace('四层继承F29的power/GND常规宽0.60mm、颈宽≥0.25mm、颈长≤1mm，不能为演示偷偷放宽。焊盘0.30宽、脚距0.50时，先从焊盘**外缘**短颈直出，再错开相邻引脚后扩宽；从焊盘中心直接斜出或0.6线压向相邻脚都会出问题。两层规则单独设定并核板厂下限，不照搬四层内层允许规则。',
'''四层继承F29的power/GND常规宽0.60mm、颈宽≥0.25mm、全局颈长≤1mm。原生连接要求线到焊盘中心；实测每条.25mm颈段总长1.365685mm，其中首.600000mm位于焊盘内，焊盘外约.765685mm。不能把外部长度冒充软件计算长度，也不能把端点停在焊盘边缘却称原生连通。因此显式建立局部例外：一个G31_U1_ESCAPE区域组包含三个TOP矩形，G31_POWER_ESCAPE/G31_GND_ESCAPE从对应常规CSet复制，仅改maxneck为1.4mm；它们是复制模板，后续不会自动跟随源CSet改变。四层局部spacing另从S_POWER_030复制，仅smdpin_line和line_line由.30改.20mm。全局原规则保持；允许层、via、宽度等逐项比对。区域与类的组合不是逐pin绑定，修改布局/分组后必须复核覆盖范围。

焊盘0.30宽、脚距0.50时，先沿引脚长轴直出，错开相邻引脚后扩至.60；不能从中心直接斜出或用宽线压向相邻脚。两层使用独立规则配置，默认宽/颈宽.2032mm、间距.16mm，本轮仅V3V3/GND演示网络以.60/.25mm、间距.20mm、普通颈长1mm覆盖，三个局部扇出区同样显式1.4mm例外；其余67网仍属DEFAULT，未完成全部两层网络分类/专用约束，进入整板布线前须补齐。四层内层限制未照搬。''')
s=s.replace('本地输入/输出电容分别连到正确脚和GND。','本地输入/输出电容的逐pin网络和位置已核对，LDO实际铜尚未闭环。')
s=s.replace('ESD GND与外壳泄放返回不借道MCU长地线。','后续走线要求ESD GND与外壳泄放返回不借道MCU长地线；本轮尚未完成这些泄放铜路径。')
s=s.replace('本课计划在L2实际生成GND参考','本课已在L2实际生成GND参考')
s=s.replace('L3是否实际铺铜以原生结果为准，未生成则明确保留后续任务。','L3本轮未铺铜，明确保留后续任务。')
s=s.replace('失败日志保留，修正原因以最终原生报告为准。','失败日志保留；补axlDBRefreshId(nil)后重新读组件关联及位置，保存后新进程确认。')
pos=s.index('\n文件迁移规则、物理MASK')
s=s[:pos]+'''
4. C8与U3实际铜间距.1773mm小于.20，移动C8 .20mm修正；C9调整朝向后又对U3的NC脚产生.1374mm间距，向右移动.20mm修正。NC仍是物理焊盘，不能在几何检查中忽略。
5. 独立脚本起初把原生NC空字符串和源数据null判为不一致，核对真实6个NC后统一为None，旧误报报告保留；不是改电气网络来通过检查。
6. group transform返回dbid后，缓存可能仍显示旧成员位置；不刷新又重做会移动两次。现已验证generic group单次+.5mm、旋转/移动/对齐及事务回退，刷新后80件姿态完全恢复。
7. 首轮三回路实际出现30项间距错误；焊盘边缘端点又出现“DRC为0但原生getconnect未接上”。按焊盘中心连接、保留全局规则并明示局部例外后，故意收紧间距/颈长仍能触发错误，回退后恢复0。创建、post-read脚本拼写和原生数据库结果分开判断，失败过程全部保留。
''' + s[pos:]
s=s.split('## 保存重开结果')[0]
s+='''## 保存重开结果与当前入口

两种板均完成独立原生进程重新打开、实际规则/网络/层/完整Film/连通图和DRC复核。正式入口与placement检查点分开保存；失败版本、规则挑战及回退日志保留，不作为当前板。

| 项目 | 四层 | 两层 |
| --- | --- | --- |
| 当前工程 | [G_4L_LAYOUT_v1.brd](../examples/lessonG_30_37_20261020/current/G_4L_LAYOUT_v1.brd) | [G_2L_LAYOUT_v1.brd](../examples/lessonG_30_37_20261020/current/G_2L_LAYOUT_v1.brd) |
| 真实导电层 | TOP-L2-L3-BOTTOM | TOP-BOTTOM |
| 完整Artwork | drill4的17 Film | drill2的15 Film |
| 已放逻辑器件/逻辑pin/net | 80/272/69，另4机械符号；6个NC保留 | 同左 |
| 本轮实际地参考 | ETCH/L2生成GND，L3未铺 | ETCH/BOTTOM生成GND |
| 局部实铜 | U1三组VDD/VSS与C13/14/15、C16两支路 | 同左 |
| GND过孔 | 3颗新建+1颗原有，共4颗 | 同左 |
| 最终有效DRC | 0 | 0 |

三组主局部回路是U1 VDD→本地电容→本层GND→U1 VSS；电容GND侧的过孔把这个GND子图接到实际参考铜。不能描述为高频返回必经地平面。C16接到C15所在V3V3/GND子图，但LDO到全部V3V3的主供电仍未布通。原生导电图逐组核六个MCU脚与指定cap pad，并核GND经via到生成ETCH shape；不是按坐标接近推断连接。

动态地铜实际填充、更新且无OOD；底层地的当前连续性只针对本版本已有局部线，后续增加所有信号后需重审。四层S/G/G/S是层功能意图，本轮L3不能算已有参考铜。

[原生最终报告](../examples/lessonG_30_37_20261020/review/native_final_report.json)记录规则/类/区域、受控正反挑战、操作回退、实际铜、独立重开、源文件不变、SHA及限制。[根独立几何审查](../examples/lessonG_30_37_20261020/review/root_geometry_review.json)对每板做597项、272pin映射/实际边界检查，均通过；不同审查有重叠，不加总充数。[MCU专项](lessonG_mcu_20261020.md)及[电源/接口专项](lessonG_power_20261020.md)保留分工与具体证据范围，电源独审绑定placement checkpoint，并不冒充后加实铜的复核。

[工程导读](../examples/lessonG_30_37_20261020/README.md)列目录和复现路径；[总验收清单](../logs/g_lessons_30_37_20261020.json)及[产物哈希](../examples/lessonG_30_37_20261020/review/deliverable_manifest.json)用于迁移后核身份。预览图依据原生几何与最终读回绘制，审查标签不是实际丝印，绿色板底也不代表铜；真实地铜证据以原生读取为准。

下一主线是H第38课逐段交互走线与精确几何操作。全板布线、buck/反馈/USB/晶振/ADC实际走线、最终参考连续性、制造输出及实物验证保留后续；GUI待验状态不变。

当前文件SHA256：

'''
for v in ('4L','2L'):
    p=G/f'current/G_{v}_LAYOUT_v1.brd';s+=f'- `{p.name}`：`{sha(p)}`\n'
put(note,s)
p=G/'learning_plan.md';t=p.read_text(encoding='utf-8-sig').replace('实际 L2/L3 作为 GND 参考的教学方案','L2/L3 功能意图为 GND；本轮实际生成 L2，L3 未铺铜留后续')
t+='\n## 本阶段结果\n\n第30—37课已完成声明范围的布局学习及原生实操，80件在两种板保存重开，三组去耦/C16局部实铜与实际地参考通过；整板布线及制造/硬件仍未完成。见[工程导读](README.md)与[完整笔记](../../notes/lessonG_30_37_20261020.md)。\n'
put(p,t)
print('G notes and learning plan finalized')