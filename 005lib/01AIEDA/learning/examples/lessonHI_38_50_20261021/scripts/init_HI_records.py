import pathlib,datetime,json,hashlib,re,shutil
R=pathlib.Path(r'D:\001DIY\005lib\01AIEDA');G=R/'learning/examples/lessonHI_38_50_20261021'
for q in ('plans','review','review_figures','source','staging'): (G/q).mkdir(parents=True,exist_ok=True)
backup=R/'backups/before_HI_38_50_20261021';backup.mkdir(parents=True,exist_ok=True)
for n in ('EDA.md','课程索引.md'):
 p=backup/n
 if not p.exists():shutil.copy2(R/n,p)
plan='''# H/I 第38—50课合并布线学习计划

开始日期：2026-10-21，Asia/Shanghai。当前状态：进行中。用G阶段已冻结的80件两层/四层板，完成有工程依据的精细走线。所有新资料、脚本、JSON、临时环境、日志、板文件、失败、备份和预览都在01AIEDA内，原G板、公共库、01env及真实硬件工程不修改。

## 执行顺序

1. 基线只读：核两个G源SHA、80件/272逻辑pin/69net/6NC、既有局部铜、实际参考铜、每网未连接分量，保留完整15/17 Film及固定层名。
2. 完整规则：补两层目前67个DEFAULT网的网络分类、物理/间距/接口例外；四层保持非GND禁内层规则。原规则变化及作用范围逐项可追溯。
3. 原生操作：逐段起止/拐角/宽度/捕捉坐标/换层via、拆线重布、事务回退和新进程读回；GUI鼠标操作与数据库API证据分开。
4. 电源/地优先：输入保护、buck输入高di/dt/BOOT/SW/L/输出/FB、LDO/主电源与MCU去耦，实际宽度/瓶颈/返回核对，更新动态地并检查孤岛/颈缩。
5. 敏感信号：HSE/复位/VDDA/ADC，确保局部返回与参考、避开SW和不必要GPIO穿越。
6. USB/CAN：按真实pin和装配方案控制分叉/残桩、源端顺序、实际层叠下的线对几何、参考/过孔/必要匹配；不把历史.20/.15mm默认说成90Ω。
7. 其余数字接口：按边沿/拓扑/连接器、方向/通道及回流安排UART/I2C/SPI/GPIO/调试；辅助路径搜索服从预先规定的禁入区/层/宽度和工程审查，不以自动连通替代设计。
8. 两板综合：69网实际连接分量、unconnected、DRC、真实铜、敏感回路、换层返回、参考开口和形状更新；必要重布。独立新进程保存重开、SHA、版本回退及两层/四层逐项比较。

## 逐课验收

|课号|保留验收点|
|---|---|
|38|逐段实际几何、创建/拆线/重布/via/回退/重开；GUI未执行不能标为通过|
|39|按真实MCU pin功能的扇出/拥塞/换层，不压关键回路|
|40|电源完整连接、宽度/瓶颈、via、电流与热使用前提|
|41|真实动态地铜、网络/孤岛/热焊盘/颈缩/OOD|
|42|HSE/NRST/VDDA/ADC实际铜、参考和耦合路径|
|43|两层USB实际参考/线对几何/分叉/端接/必要匹配|
|44|UART/I2C/SPI/CAN/GPIO边沿、拓扑、通道和返回|
|45|完整两层连接、DRC、实际回路及可回退版本|
|46|四层实际层叠下逐关键网络参考与层选择|
|47|信号换层的参考变化、就近GNDvia及残桩限制|
|48|实际生成平面的开口/分区/颈缩/跨缝|
|49|四层差分/必要匹配/端接，不任意蛇形|
|50|完整四层板及与两层的几何/参考/via/制造比较|

## 范围及开放项

没有整板布通不能宣布45/50完整板通过；没有实际生成铜不能把计划平面记为参考；DRC为0不能单独证明电源/去耦/EMI。USB阻抗几何可作带前提的工程设计，制造厂未确认的stack/公差/阻抗不能宣称认证。MPN有效容量、USB4105板厚装配、两层阻焊桥、热/反灌、HSE起振/ADC/系统ESD-EMI仍保留制造或硬件验证。本任务不以仿真替代基本布线要求。

使用官方Cadence17.2 SKILL/原生数据库接口，原生执行者单一，工程规划和独立审查分开。当前桌面控制list_apps实际返回native pipe unavailable（系统找不到指定的文件，os error2）；GUI待验继续保留，见review/desktop_connection_probe.json。第6/11/14/26课GUI及51编程暂缓状态不改。
'''
(G/'learning_plan.md').write_text(plan,encoding='utf8')
probe={'clientDate':'2026-10-21','method':'computer-use skill; @oai/sky initialize then sky.list_apps','result':'Error: Computer Use native pipe is unavailable: failed to connect native pipe: 系统找不到指定的文件。 (os error 2)','effect':'No desktop target/window was obtained; no UI input performed; native CLI/SKILL work continues with separate GUI pending state.','skill':'C:/Users/Administrator/.codex/plugins/cache/openai-bundled/computer-use/26.1007.71326/skills/computer-use/SKILL.md'}
(G/'review/desktop_connection_probe.json').write_text(json.dumps(probe,ensure_ascii=False,indent=2),encoding='utf8')
raw=(R/'EDA.md').read_bytes();marker='## 当前学习计划'.encode();prefix=raw[:raw.index(marker)]
s=(R/'EDA.md').read_text(encoding='utf-8-sig');a=s.index('## 当前学习计划');z=s.index('**统一学习目录',a)
s=s[:a]+'''## 当前学习计划（2026-10-21，H/I两层与四层精细走线合并学习）

按用户本次要求，将第38—50课合并为一轮实际布线训练，逐课保留验收点。当前状态为进行中，计划与验收范围见[H/I学习计划](learning/examples/lessonHI_38_50_20261021/learning_plan.md)。输入为G阶段冻结的80件两层/四层板，补齐两层完整网络规则后按电源/地、敏感信号、USB/接口及普通数字网推进；最终要求实际连接、DRC和真实回路/参考三方面核验。所有新文件仍在01AIEDA，G源板/公共库/01env及真实工程不改。第6/11/14/26课GUI待验和51编程暂缓保留；本轮桌面连接重试仍为native pipe error2，不能冒称已做GUI交互。

''' +s[z:]
s=s.replace('本轮按用户最新指令完成G第30—37课的布局范围，不将该待验状态抹去。','G第30—37课布局范围已完成，本轮继续H/I第38—50课合并布线学习，不将该待验状态抹去。')
old='1. G第30—37课已完成布局学习及声明范围的原生实操，见第29节和[G阶段笔记](learning/notes/lessonG_30_37_20261020.md)。下一主线第38课逐段交互走线与精确几何操作，从G/current两板继续；局部颈长/间距例外须随布局与规则调整复核。第6/11/14/26课GUI待验、制造条件与[来源勘误](learning/notes/lessonF_source_corrections_20261019.md)保留。'
new='1. 正在合并学习H/I第38—50课，从G/current两板的隔离副本继续。先核每网未连接分量、完整两层规则与关键路径，再分批布线/更新铜/原生重开/独立审查。局部例外随布局和规则变化复核，制造条件与[来源勘误](learning/notes/lessonF_source_corrections_20261019.md)继续保留。'
assert old in s;s=s.replace(old,new)
body=s[s.index('## 当前学习计划'):];(R/'EDA.md').write_bytes(prefix+body.encode())
p=R/'课程索引.md';s=p.read_text(encoding='utf-8-sig');a=s.index('本目录列出完整主线');z=s.index('\n\n## 固定目标',a)
s=s[:a]+'''本目录为60课主线及5个进阶专题。既有G30—37布局范围完成，当前按用户要求合并学习H/I第38—50课；[合并计划](learning/examples/lessonHI_38_50_20261021/learning_plan.md)保留逐课验收，未实际完成项不写通过。输入为G冻结两板80件布局，需补齐两层规则和整板走线。第6/11/14/26课GUI待验、51编程暂缓状态保留。''' +s[z:]
for n in range(38,51):
 m=re.search(rf'^\| {n} \|.*$',s,re.M);assert m,n
 cols=m.group().split('|');cols[-3]=' 合并学习进行中 ';cols[-2]=' [H/I计划](learning/examples/lessonHI_38_50_20261021/learning_plan.md) '
 s=s[:m.start()]+'|'.join(cols)+s[m.end():]
p.write_text(s,encoding='utf8')
print('HI plan, desktop probe, backups, EDA current plan and course38-50 in-progress states recorded')