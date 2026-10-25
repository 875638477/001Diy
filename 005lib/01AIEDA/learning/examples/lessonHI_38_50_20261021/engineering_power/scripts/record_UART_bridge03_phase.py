from pathlib import Path
import json,hashlib,math
R=Path(r'D:\001DIY\005lib\01AIEDA\learning\examples\lessonHI_38_50_20261021\engineering_power'); H=R.parent
note=H.parent.parent/'notes/lessonHI_power_20261021.md'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest().upper()
def length(op):return sum(math.dist(a,b) for a,b in zip(op['points'],op['points'][1:]))
rows=[]
for v in ['2L','4L']:
 p=R/f'UART_RX_receiver_bridge_{v}_03.json'; q=json.loads(p.read_text(encoding='utf-8')); pre=R/f'readouts/UART_RX_bridge03_full_{v}.json'; x=json.loads(pre.read_text(encoding='utf-8'))
 ids={z['id'] for z in q['operations']}; warnings=[z for z in x['issues'] if any(i in json.dumps(z) for i in ids)]
 assert not warnings and x['definiteOverlapPieces']==0
 routes=[z for z in q['operations'] if z['type']=='route' and z['net']=='UART_RX']; assert len(routes)==3
 assert math.dist(routes[0]['points'][0],[50.12,25.0374])<1e-9 and math.dist(routes[-1]['points'][-1],[68.1016,25])<1e-9
 assert routes[0]['points'][-1]==routes[1]['points'][0] and routes[1]['points'][-1]==routes[2]['points'][0]
 rows.append(dict(variant=v,plan=str(p),sha256=sha(p),precheck=str(pre),precheckSHA256=sha(pre),operations=len(q['operations']),wholeGroupDefiniteOverlapPieces=x['definiteOverlapPieces'],otherGroupBaseRuleWarningPieces=x['spacingWarningPieces'],newUARTBaseRuleWarnings=len(warnings),receiverCenterlineLengthMM=sum(length(o) for o in routes),bottomBridgeCenterlineLengthMM=length(routes[1]),routeEndpointContinuity=True,newSignalVias=2,removedGroundVias=1,noOtherGroundMove=True))
review=dict(status='PASS_SCOPED_CANDIDATE_GEOMETRY_NATIVE_REBASE_AND_REFERENCE_PENDING',date='2026-10-22',variants=rows,sourceStage='Virtual integrated review on USB_aux_b014 plus frozen joint sources; not an actual b015 native result',requiredNativeActions=['Confirm actual b015 input SHA and whether service18 or19 supplied R17; unique-match old source copper, pose and removed GNDvia before applying delta','If service19 already saved, explicitly omit already-applied R17 and PA10 edits without rebuilding sources','Full DRC, exact U1.31-R17.1 and R17.2-R18.1 connectivity proofs, no orphan branch; verify PB4via returns through retained GND62.6,25.65','Refresh actual ground and examine 2L TOP projection over short BOTTOM bridge; for 4L verify actual L2/L3 around both new through-vias; stored/fresh reopen evidence required'],returnAssignments=dict(newSignalViaToRetainedGND_MM=[1.0578341079772335,1.043845295050947],retainedPB4SignalViaToAlternativeGND_MM=.8246211251235369,retainedPB5MidGroundXY=[56.757,25.092],removedRedundantPB4GroundXY=[61.8,24.95],retainedAlternativeGroundXY=[62.6,25.65]),rejectedHistory=['Parent proposed GND55.4,27.25 intersects actual future SCL TOP diagonal and SDA BOTTOM y27.15','Bridge02 second BOTTOM bridge intersects root_remaining18 NRST BOTTOM x60.25; preserved failure readout','No global width/spacing/via list changed; all new receiver copper .20mm and stock L28_VIA030_C060'])
(R/'readouts/UART_RX_receiver_bridge_03_review.json').write_text(json.dumps(review,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
append='''

## 17. 右侧完整 v11 与 SWCLK/SWDIO 联合修正

RIGHT10_FULL_2L_v11.json 与 RIGHT10_FULL_4L_v11.json 各95操作，替代第16节 v10 候选。v10 的 SWCLK 全TOP东段与根任务后加入的 SWDIO 服务线相交，不能继续称为当前可执行版本。v11 改 SWCLK 为实际需要的短 BOTTOM 桥，新增两信号过孔及三个配对共地过孔，同时修改 PC14 的底层绕路；五个密集源端小通孔仍用于真正换层。它不是为保留旧锚点而添加的闲置过孔。

SWCLK 桥两端为 (47.95,22.4)/(57.4,20.8)，中段通过 BOTTOM y23.1→y21.2 绕开 SWDIO TOP 服务段。新回流点 (46.8,22.5)/(52.8,22.8)/(57.35,19.31) 与完整源/长路一起预审。源组仍要求原生实际替换 quiet 岛、各层永久 void 与唯一 anchor，执行删除新 anchor 的负测试，再刷新铜与完整DRC。文件 SHA：2L 3F616508C7D06A8B8E86FC01D4C718E1FC20B35DA4FF6206715692FE53FF469A；4L B3E053D45D702C34571EBD608F05EDE7928D63DA82F21CB23EFE4C297D981EF2。

第16节的 v10 资料、8个新共地过孔与“SWCLK全TOP”均为该历史版本的事实，不代表 v11 当前操作数/回流过孔数。本次 v11 新增回流点须与全组服务线一起核对；不能把 v10 manifest 当成 v11 证据。根任务已冻结 v11、South9、services18、NSS04，后续只能新建 delta，不能原名覆写。

## 18. UART_RX 接收端出口与短换层桥候选 03

原 R17 接收端电阻 pin2 被 PA15 TOP 横线、SWCLK BOTTOM 桥及 SWO/地返回封住，逐网几何搜索只有1063个可达单元。这是实际出口拥塞，不能简单让自动布线多跑。根任务提出 R17 旋90°移到 (50.12,23.361)，pin1 PA10=(50.12,23.4626)、pin2 UART_RX=(50.12,25.0374)，PA15 y24.25 可从两焊盘间通过，名义铜间距0.2175mm；移动焊盘及 PlaceBound 已由根任务预审。

完整新 delta 为 UART_RX_receiver_bridge_2L_03.json 与四层同名变体，各9操作加 R17 姿态。包含精确删除原 PA10 两段TOP铜、连接新 pin1，以及 R17.2 到 R18.1 的完整接收支路。为绕过 (56.757,25.092) 的既有 PB5 回流地过孔，使用两个正常 L28 过孔 (55.7,25.05)/(57.8,25.05) 和 BOTTOM 短桥，经 (56.45,24.3)/(57.05,24.3)；其余接收线TOP为0.20mm。桥两端距保留地孔分别1.0578/1.0438mm，需最终实际地铜与转换回流审查。

仅删除冗余 PB4 远端地孔 (61.8,24.95)。PB4信号过孔 (61.8,25.85) 仍有更近的保留共地孔 (62.6,25.65)，距离0.8246mm，因此没有以移除唯一回流来换通路。接收线东段改 y24.93，到该保留地孔铜间距0.32mm，到 PA15 信号过孔铜间距0.28mm。所有其他回流地孔及其位置保持。

两板对实际 USBaux b014 加冻结各组及 root_remaining18 进行完整组合预审，均无 definite overlap，新增 UART 操作没有基线间距警告；其他组60/62项规则域简化警告保留，不能因此把全板标成PASS。报告 readouts/UART_RX_receiver_bridge_03_review.json 与 UART_RX_bridge03_full_*.json。03本身仍是待原生重基/端点/真实参考验证的候选，不能称最终完成。

记录两项被否决方案：拟将 PB5地孔移到 (55.4,27.25) 会撞 TOP SCL 斜段与 BOTTOM SDA 横线；桥02的第二段底层绕路会碰 NRST BOTTOM x60.25。均未执行，原方案及失败读回保留。03取消第二座桥，保留 PB5 地孔，仅删已有更近替代地的冗余 PB4 地孔。

原生集成必须先确认 b015 输入 SHA 与 R17 实际姿态。若执行的仍是 services18，仅应用精确两段旧铜删除、R17移动及新线路，不重做整个 SOURCE；若 services19 已应用，显式省略已完成的姿态/PA10替换并记录原因。最终还需新进程读回、完整DRC、两条真实端点证明、无新孤枝，以及2L桥上方TOP实际地缺口/4L真实L2和L3反焊盘及共地宽颈复查。UART默认初次115200bps不代表外部边沿已受限或信号完整性已经认证。

## 19. 主供电返工暂停与搜索归因勘误

NSS源端返工期间曾推测 MCU BOTTOM STAR 大对角是剩余13条GPIO无法合理引出的必然原因，提出把 C9→MCU 主供电改走 TOP。初稿 NSS_pullup_local_relayout_03.json 真实穿 C9.2 GND 焊盘并撞 buck反馈/地，已被实际铜审查否决，绝不执行。

随后完整顺序对照在保留原 STAR 的条件下也找到了 PB12；此前约10秒没有工具输出被误判为搜索失败。逐网贪心失败或暂时无输出，不能证明必须大改关键供电。当前暂停为GPIO单独重构主feed，NSS_pullup_local_relayout_04_SOURCE_ONLY.json 保持原供电与 SPI guard，改做联合出口、预留和回溯。未执行 C9旋转、U3下移或 R29改位等推演，不能写成已优化完成。原07c主供电、外设低阻分发及既有去耦返回继续保留；后续只有在真实几何证明必要时才重新评估供电返工。
'''
text=note.read_text(encoding='utf-8');assert '## 17. 右侧完整 v11' not in text
note.write_text(text+append,encoding='utf-8')
readme='''# HI 电源、接口、SPI 与右侧 MCU 专项入口

全部文件与运行资料均位于01AIEDA。本目录主笔记是 ../../../notes/lessonHI_power_20261021.md；原生 current/ 与整板验收由根任务维护。

当前冻结右侧源与完整长路是 RIGHT10_FULL_2L_v11.json、RIGHT10_FULL_4L_v11.json，各95操作。它们包含与 SWDIO 联合修正的 SWCLK 底层桥；v10全TOP说法只属历史。右侧完整新 quiet 岛、永久void、唯一anchor(46.35,29.4)、C15/16供地与真实端点必须作为整组执行和原生负测试，不能只执行旧partial候选。密集源五个换层距共地2.006–2.585mm，低边沿/初始I2C100k/SWO关闭为使用条件，固件尚未设置或验证。

新的 UART_RX_receiver_bridge_{2L,4L}_03.json 是冻结源之后的完整接收端 delta：R17重定位、两段PA10旧铜精确删除、两正常信号过孔短BOTTOM桥、仅删一颗已有更近替代回流的冗余地孔。原生前必须核输入SHA及R17是否已重定位。readouts/UART_RX_receiver_bridge_03_review.json 只证明候选组合几何范围，尚不代表新原生板/实际返回验收。

电源07c、外围06b、CAN04/05与ESD04c已经历史原生批次实施；SPI两层v10/四层v6已经b012原生指定端点、DRC0和HSE负测试。后续移动源端和新增其他铜后必须重新核查，不能用历史PASS覆盖新板。

暂停为GPIO单独大改主feed。NSS03的TOP供电方案真撞C9地焊盘/反馈铜而被否决；保留原STAR也可通过合适搜索顺序找到PB12。NSS04_SOURCE_ONLY保持原供电和SPI guard，不能把工具暂未输出/贪心失败当成必须返工供电的证据。

所有失败候选、脚本及只读报告保留。私有HI_VIA026_C052_TENT为.26钻/.52铜/.13环的机械通孔，许可需全实际导体层局部批准；外层neck/spacing局部例外不得开启内层信号etch。真实几何弧解析 helper 为 scripts/cadence_poly.py。

持续开放：USB4105脚长与1.6mm板工艺、OSH阻焊桥、ESD邻开窗零余量、真实MPN高度/电容/温升与装配、USB阻抗/22Ω/ESD/EMI实测。artifact_manifest.json 为阶段记录完整性清单，不是整板布线验收证明。
'''
(R/'README.md').write_text(readme,encoding='utf-8')
print(json.dumps(dict(review=str(R/'readouts/UART_RX_receiver_bridge_03_review.json'),note=str(note),variants=rows),ensure_ascii=False))