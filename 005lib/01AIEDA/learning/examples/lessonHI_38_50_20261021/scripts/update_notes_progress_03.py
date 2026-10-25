from pathlib import Path
import json
B=Path(r'D:\001DIY\005lib\01AIEDA');R=B/'learning/examples/lessonHI_38_50_20261021';P=B/'learning/notes/lessonHI_38_50_20261021.md';s=P.read_text(encoding='utf8')
parts=['## 2026-10-22续作：已冻结MCU6与USB8，整板仍在进行','', '|板|当前有效原生板|SHA256|剩余最少连接/原生DRC|','|---|---|---|---|']
for v in ['2L','4L']:
 d=json.loads((R/'inventory'/('current_'+v+'.json')).read_text(encoding='utf8'));name=Path(d['board']).name;parts.append(f'|{v}|[{name}](../examples/lessonHI_38_50_20261021/native/{name})|`{d["sha256"]}`|{int(d["summary"]["nativeRemainingConnections"])}/0|')
parts+=['','以上均保存后在新进程只读重开、源SHA稳定，net69/带网terminal266/NC6保真；完整原始目录以inventory/current_*.json和对应不可变checkpoint为准。开始日期和目录20261021保留，实际续作日期2026-10-22，不移动学习目录。','',
'''MCU6两板32端点与HSE隔离反测通过，137→112；独立82项复核通过。晶振quiet地岛真实面积62.31mm²，下方2L BOTTOM/4L L2，application铜物理moat和L3永久void均读回。删除唯一anchor via(45.45,28.85)，两颗负载电容、地岛和三段guard仍互通，不能到VSS47/application/case；case/VSS仍通，恢复后DRC0。该反测需终板全部普通线/地铜/新via后再重复，不能只在局部阶段通过一次。三处器件微调、ADC/VDDA及复位具体步骤见[MCU专项笔记](lessonHI_mcu_20261021.md)。

USB8两板physical/spacing和实际电气DRC全部0，112→96。connector-only完整复制ECSet后仅改phase4mm和uncoupled13.5mm；其余字段/最大via2保留。shared MCU pair仍原phase1mm/uncoupled6mm，靠真实缩小并正确错位45°的短主干达到耦合，未把全局预算放大。原生connector平面phase实际3.2757mm；临时收紧到3mm确实报错。shared临时uncoupled1mm确实报4.9931/4.9204mm，恢复原值回0。Z Axis Delay默认未启用，平面phase不含via barrel，不能把mm阈值当USB时延合规证明。

USB2L bulk1.15mm/.16mm、4L .26mm/.15mm只对应各自层叠和假设Dk下的近90Ω估算。细引脚、ESD流通列、MCU共享与支路仍有.2mm端口段，逐段长度和范围另列；不是整条均匀90Ω。真实PCB铜将ESD1↔6、3↔4贯通，不用PIN_SHORT虚构PCB连接。连接器两插向、offpair上拉短stub及CAN DNP残桩必须按各路径核，不用全部net铜长替代主路径。

实际参考审查发现1mm BOTTOM镜像桥在两via反焊盘间没有直接TOP投影铜，不能称全程微带。原生实际铜上存在0.4mm宽南侧走廊，signalvia附近到左右GNDvia返回上界路径2.0215/1.5349mm，左右地返回相连走廊4.5564mm。两层ESD的VBUS底桥导致入口约1.34262mm直接参考投影缺口，底地绕左端存在0.3mm宽、4.8mm长可用路径。这些是实际存在的几何上界路径，不是电流必经或场求解最短路径，直接缺口仍要保留。最终两板地铜更新后再核，不能以同net或附近via替代真实返回。

via本身双面mask为NULL、光绘不补缺失开窗已经实查，但U4.5焊盘mask下边9.45与VBUS via孔上边9.45名义相切，孔到铜land仅.10mm。可靠盖油、钻位/阻焊注册、吸锡及装配工艺仍未匹配，不能说无via独立开窗就保证孔已盖油，更不能等同填孔。

Cadence内部自动field-solution连续失败与纯几何/长度结果分开记录。只对受控子进程PATH加tools/bin后裸名bem2d可解析，但内部失败仍存在，未宣布解决，也未宣称阻抗/SI仿真通过。官方支持的批量性能方法已经受控实测：创建几何期间drcEnable=nil，unwindProtect保证恢复t，末尾axlDRCUpdate(t)完整检查；故意.10mm错误会实际报MinNeck，rollback再检查回0/source稳定。两层USB构建由逐段重复派生约10分钟降到13.77秒，终检和新进程差分收紧挑战仍通过，未关闭最终检查。操作/角色导出也根据parent->thermal识别原生动态热连接，避免把可更新spoke当固定手工铜；两层via pad归一化按真实Cross Section过滤，仅TOP/BOTTOM，不让解析器凭默认层补L2/L3。

SPI源端本轮拒绝了三类候选：绕SW到y13的约80mm长路；上拉R25支路BOTTOM x29.95堵住整个西侧通道；粗网格在真实窄通道多加信号via。明确源端方案SPI_source_explicit_v5使用SCK x34.385，对R24实pad边和NSS竖线各.215mm，MISO用受控直角避开SCK，NSS先接R23并将上拉支路安排在MCU内侧。两个信号via避R29 BOOT1间距错误均留失败版本；新候选仍待原生。电源STAR旧两段需要唯一精确匹配删除再重布，不能仅加新线形成并行回路；新地桥实际返回与HSE单anchor隔离是两种问题，前者删掉未必使全局地断网，不能伪设必须断网来证明有用。

电源几何、实际plane弧线、CIN返回带、局部规则及制造前提见[电源专项笔记](lessonHI_power_20261021.md)。H45电源重布、GPIO新出口、外围供电和普通接口长路径仍在推进，45/50完整板尚未验收；第6/11/14/26 GUI及51编程状态继续保留。
''']
insert='\n'.join(parts)+'\n\n';s=s.replace('## 最终保存重开与验收（待完成）',insert+'## 最终保存重开与验收（待完成）');P.write_text(s,encoding='utf8')
P=B/'EDA.md';s=P.read_text(encoding='utf8');s=s.replace('当前状态为进行中，计划与验收范围见','当前状态为进行中（2026-10-22续作），计划与验收范围见',1)
s=s.replace('G实现三组MCU去耦/C16局部实铜，2L BOTTOM与4L L2实际GND；4L L3未铺，主供电/关键接口/整板走线及最终回流审查待H/I','H/I进行中：两板MCU6/USB8原生保存重开0DRC，171→96剩余连接；4L L2/L3真实GND与HSE单anchor隔离反测通过。电源重布/普通接口/终板实际返回待继续，详见[H/I笔记](learning/notes/lessonHI_38_50_20261021.md)')
P.write_text(s,encoding='utf8');print('Updated unified main note and root EDA current progress; no full-board pass claim')