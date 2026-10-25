import pathlib,re,json
G=pathlib.Path(__file__).resolve().parents[1];R=G.parents[2]
assert (G/'review/native_final_report.json').exists()
def put(p,s):p.write_text(s,encoding='utf-8',newline='\n')
b=R/'backups/before_G_30_37_20261020/EDA.md'
raw=b.read_bytes();marker='## 当前学习计划'.encode();prefix=raw[:raw.index(marker)]
s=b.read_text(encoding='utf-8-sig')
a=s.index('## 当前学习计划');z=s.index('**统一学习目录',a)
s=s[:a]+'''## 当前学习计划（2026-10-21更新，G阶段器件布局）

完整课程目录见根目录[课程索引.md](课程索引.md)。按用户本次指令，G第30—37课已完成声明范围的资料、工程布局、原生CAD实操及保存重开验收；[完整学习笔记](learning/notes/lessonG_30_37_20261020.md)与第29节记录结果。当前四层板为[G_4L_LAYOUT_v1.brd](learning/examples/lessonG_30_37_20261020/current/G_4L_LAYOUT_v1.brd)，两层对比为[G_2L_LAYOUT_v1.brd](learning/examples/lessonG_30_37_20261020/current/G_2L_LAYOUT_v1.brd)。两板80件已布局，三组MCU去耦/C16局部连接和实际地参考已实现；整板布线、制造与实物验证仍待后续。下一主线第38课逐段交互走线与精确几何操作；第6/11/14/26课GUI待验及51编程教程暂缓保持。

''' +s[z:]
s=s.replace('本轮按用户最新指令完成F第27—29课，不将该待验状态抹去。','本轮按用户最新指令完成G第30—37课的布局范围，不将该待验状态抹去。')
s=s.replace('F27—29机械基准/层叠/约束已备；仅J2与安装孔定位，79件待布局，下一主线第30课','G30—37完成80件两层/四层布局，按实际pin审查去耦/电源/时钟/模拟/接口，原生保存重开及局部实铜通过；制造/硬件开放项保留')
s=s.replace('F28两种层叠/F29四层规则已原生验收；正式铺铜、回流与整板走线待后续课程','G实现三组MCU去耦/C16局部实铜，2L BOTTOM与4L L2实际GND；4L L3未铺，主供电/关键接口/整板走线及最终回流审查待H/I')
s=s.replace('| 待开始，具体输出按任务需要 |','| G37完成布局阶段审查、问题分级与可回退冻结；完整走线审查、制造输出/装配及实物释放待J/K |',1)
old='1. F第27—29课已完成建板/层叠/约束原生CAD范围，见第27节及[F阶段总结](learning/notes/lessonF_27_29_20261019.md)。下一主线第30课功能分区、MCU方向与出线规划，使用纠正版F29_v4；第6/11/14/26课GUI待验保持，制造条件与[来源勘误](learning/notes/lessonF_source_corrections_20261019.md)先核。'
new='1. G第30—37课已完成布局学习及声明范围的原生实操，见第29节和[G阶段笔记](learning/notes/lessonG_30_37_20261020.md)。下一主线第38课逐段交互走线与精确几何操作，从G/current两板继续；局部颈长/间距例外须随布局与规则调整复核。第6/11/14/26课GUI待验、制造条件与[来源勘误](learning/notes/lessonF_source_corrections_20261019.md)保留。'
assert old in s;s=s.replace(old,new)
s+='''

## 29. G阶段器件布局第30—37课（2026-10-20）

按用户要求自主评估，把八课放在同一80件真实电路内连续练习，并保留逐课验收。全部来源、草稿、中转JSON、脚本、原生数据库、失败/回退、预览、日志和备份仍集中01AIEDA；未改公共库、01env和真实硬件工程。

入口：[完整学习笔记](learning/notes/lessonG_30_37_20261020.md)、[工程导读](learning/examples/lessonG_30_37_20261020/README.md)、[MCU专项](learning/notes/lessonG_mcu_20261020.md)、[电源/接口专项](learning/notes/lessonG_power_20261020.md)。

| 课号 | 本次完成内容 |
| --- | --- |
| 30 | 核18种真实封装及80件pin，按功能区和出线选择MCU270°；放置/旋转/移动/对齐/组移动及事务回退通过 |
| 31 | U1三组VDD/VSS与C13/14/15本层实铜、cap侧地via到实际平面、C16储能两支路；几何及原生导电图核对 |
| 32 | buck输入热回路、SW/BOOT、电感/输出电容、反馈和LDO按真实pin布局与路径预审，完整电源铜仍待布线 |
| 33 | HSE90°方案、负载电容/复位/BOOT/ADC与VDDA布置，保留安静返回区与GPIO扇出要求，尚待实际走线/实测 |
| 34 | J2固定机械边界、USBLC6正确pin、源端阻尼/互斥CAN、各排针与保护/屏蔽边界布局；ESD泄放等仍待布线 |
| 35 | 独立两层规则、TOP局部线与BOTTOM实际动态GND，预留连续地与有限穿越方案 |
| 36 | TOP-L2-L3-BOTTOM保持，L2实际GND、L3未铺；记录参考变化与换层返回要求 |
| 37 | 两板80件/272逻辑pin/69net、6NC/机械、层/完整Film/规则/DRC及保存重开，问题分级和版本冻结 |

当前板：[四层G_4L_LAYOUT_v1.brd](learning/examples/lessonG_30_37_20261020/current/G_4L_LAYOUT_v1.brd)、[两层G_2L_LAYOUT_v1.brd](learning/examples/lessonG_30_37_20261020/current/G_2L_LAYOUT_v1.brd)。各80逻辑器件加4机械符号；实际3新+1原有共4颗GNDvia，最终有效DRC均0。全部15/17 Film按drill2/4核，物理MASK未重新加入。根独立几何审查每板597项/272pin通过；电源接口独审3916项绑定placement检查点，MCU补充独审对最终局部铜和规则取证，检查范围有重叠不合计。

关键规则例外已显式记录：.25mm扇出颈段原生总长1.365685mm（pad内.6、外部.765685），全局1mm保留；一个G31_U1_ESCAPE组内3个TOP矩形使用复制CSet的1.4mm局部值，四层局部两项spacing .30→.20mm。复制不是动态parent继承，区域/类作用也不是逐pin绑定。两层当前只给V3V3/GND演示网专用physical class/CSet，其余67网仍DEFAULT，整板布线前需补齐两层全网分类/专用规则。收紧规则能实际触发错误，回退后0。主局部返回是本层cap—VSS，cap端via接实际参考铜；不把高频返回描述成必经plane。

失误及修正均入笔记：合并布局的11组冲突、pad bbox重复旋转、原生对象缓存/组移动重复风险、NC焊盘间距、空串/null误报、边缘端点DRC0却未原生连接、初版局部铜30项间距错误及后处理脚本失败。创建成功/进程exit0/DRC0均不独自作为工程通过依据。

[原生最终报告](learning/examples/lessonG_30_37_20261020/review/native_final_report.json)、[根几何审查](learning/examples/lessonG_30_37_20261020/review/root_geometry_review.json)、[总验收](learning/logs/g_lessons_30_37_20261020.json)及[产物哈希](learning/examples/lessonG_30_37_20261020/review/deliverable_manifest.json)保存具体身份和证据。修改前EDA/索引/主笔记备份见backups/before_G_30_37_20261020，本文最前面的用户原文/目录规范原样保留。

仍未完成整板走线：LDO主供电、buck热回路/反馈、USB/ESD、晶振/ADC等在H/I实现；后续所有信号加入后重审参考铜连续性。USB4105装配/板厚、22Ω与90Ω依据、有效电容、两层阻焊桥、热/反灌/起振/ADC及系统ESD/EMI仍为制造或硬件开放项，不据布局学习冻结作生产释放。下一主线第38课；GUI待验不变。
'''
# Preserve all user-authored preamble bytes, including its existing line endings.
body=s[s.index('## 当前学习计划'):]
(R/'EDA.md').write_bytes(prefix+body.encode('utf-8'))
assert (R/'EDA.md').read_bytes().startswith(prefix)
p=R/'课程索引.md';t=p.read_text(encoding='utf-8-sig')
t=t.replace('更新日期：2026-10-19','更新日期：2026-10-21',1)
a=t.index('本目录列出完整主线');z=t.index('\n\n## 固定目标',a)
t=t[:a]+'''本目录列出完整主线 **60课** 及按需进阶专题。第1—5、B7—10、C12—14、D/E15—25、F27—29及G30—37已完成各自声明的资料/原生CAD范围。第26课真实PST→PCB→ECO→逆向比较通过，GUI ERC/应用SWP待验；第6/11/14课界面待续。当前入口为[G布局笔记](learning/notes/lessonG_30_37_20261020.md)及[G工程导读](learning/examples/lessonG_30_37_20261020/README.md)，当前两板G_LAYOUT_v1：80件已布局，三组去耦/C16局部实铜与实际地参考已完成；整板布线及制造/硬件仍待后续。下一主线第38课。51编程教程仍暂缓。''' +t[z:]
statuses={30:'已完成原生布局/操作',31:'已完成三组去耦/C16实铜；余项待布线',32:'已完成布局/路径预审；电源铜待布线',33:'已完成布局/路径预审；走线/硬件待验',34:'已完成布局/边界预审；泄放铜待布线',35:'已完成布局/底层地铜示范',36:'已完成布局/L2地铜；L3待铺',37:'已完成布局冻结；制造/硬件待验'}
for n,status in statuses.items():
    pat=rf'^\| {n} \|.*$';m=re.search(pat,t,re.M);assert m,n
    cols=m.group().split('|');cols[-3]=' '+status+' ';cols[-2]=' [G完整笔记](learning/notes/lessonG_30_37_20261020.md) / [工程](learning/examples/lessonG_30_37_20261020/README.md) '
    t=t[:m.start()]+'|'.join(cols)+t[m.end():]
put(p,t)
print('EDA current plan and G summary; root course rows30-37 updated; original preamble preserved')