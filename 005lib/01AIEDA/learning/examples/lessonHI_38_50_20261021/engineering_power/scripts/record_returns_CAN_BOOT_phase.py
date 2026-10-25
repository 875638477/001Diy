from pathlib import Path
import json,shutil,hashlib
R=Path(r'D:\001DIY\005lib\01AIEDA\learning\examples\lessonHI_38_50_20261021');P=R/'engineering_power';note=R.parent.parent/'notes/lessonHI_power_20261021.md';dest=P/'source/official_BOOT_diagnostic';dest.mkdir(exist_ok=True)
base=Path(r'C:\Program0\Cadence\SPB172\share\pcb\examples\skill\DOC\FUNCS');apis=['axlDBCreatePath.txt','axlDBControl.txt','axlDBDynamicShapes.txt','axlShapeDynamicUpdate.txt']
items=[]
for name in apis:
 src=base/name;out=dest/name;shutil.copyfile(src,out);items.append(dict(source=str(src),path=str(out),sha256=hashlib.sha256(out.read_bytes()).hexdigest().upper()))
(dest/'source_manifest.json').write_text(json.dumps(dict(status='INSTALLED_CADENCE17_2_OFFICIAL_API_REFERENCE_COPY',files=items,webCrossCheck='https://community.cadence.com/cadence_technology_forums/pcb-design/f/allegro-x-pcb-editor/11321/axldbcreatepath/13798',webScope='OriginalCadencecommunitythread discussesfirst-touchednet; not an authoritativeError9code mapping andnotusedasrootcauseproof.'),indent=2)+'\n',encoding='utf-8')
text='''

## 20. 原生 BOOT0 创建失败、真实间距遗漏与动态地铜施工顺序

冻结 RIGHT11 的 BOOT_DIRECT_TOP 曾沿 y27.3 经过 R28.2 GND 焊盘下方，净距仅0.1935mm，低于该处实际 GND smdpin_line=0.3mm。原粗组合报告中已经保留该警告，但未在交付冻结候选前修掉，这是本次专项审查的遗漏；不能用“所有源短颈都允许0.16mm”或“警告已保存”替代修正该非局部规则的真实间距。修正路径为 (46.8,27.65)→(47.27,27.18)→(52.8984,27.18)→R28.1(52.8984,28)，正常0.20mm，对R28地焊盘净距增至0.3135mm，其余规则不变。冻版原文件不覆写，由执行者显式记录单操作适配。

原生 axlDBCreatePath 仍在该水平段返回nil/SPMHSY-49 Error9。分段实验先证明 R28.1 到 y27.18 的竖段可创建，BOOT0网络身份正确；因此不能把“去掉焊盘内折回”当作已证明的根因。执行者导出 try07 实际失败时刻的80件、611段、112过孔及8个真实多边形。独立对真实铜重查发现：水平段没有碰其他网的焊盘/走线/过孔，但与 TOP 已生成的 GND 碎片交叠0.061683mm²；该片bbox约(46.7602,26.8502)至(47.5,28.128)，面积0.5714232mm²，母dynamic boundary为(39.2,24.6)至(47.5,28.4)。该片不是静态晶振quiet岛。

工程诊断证据为 readouts/actual_BOOT_failure07_geometry.json，原始失败快照由native执行者保留在HI/review/PROVISIONAL_FAILED_BOOT_2L_GEOMETRY.json，明确是未保存、未通过DRC的诊断态。try08采用“精删需要重裁的旧dynamic boundary→创建源/服务真实铜→用新polygon恢复dynamic并更新”的施工顺序，随后相同BOOT段原生成功且actualNet=BOOT0，272引脚身份及新quiet唯一anchor负测通过；截至本次记录，全板fullDRC和正式新进程验收仍由native执行者继续，不能把这些中间成功冒充b015已正式发布。

这项对照支持旧generated GND铜在该操作顺序中是触发因素，不泛化为所有 axlDBCreatePath nil 都由铜皮导致。官方17.2安装API已完整复制到 source/official_BOOT_diagnostic：CreatePath说明etch取首次接触网络且nil不能当成功；DBControl的dynamicFillMode与drcEnable是不同控制；ShapeDynamicUpdate支持强制voiding、smoothing和thermal生成。实际try08没有依靠关闭DRC、修改全局规则或永久改变dynamic模式来通过。后续仍需检查实际网络、最终dynamic fill、完整DRC与重开，不能绕过失败后只记连接成功。

## 21. remaining19 普通信号换层的共地返回组02

两层 remaining_returns_2L_v19_02.json 提供三个普通共地过孔：NRST(39.55,42.8)、UART_TX(54.75,19.75)、VBUS_PRESENT_N(50.95,12.5)，距各信号过孔分别0.8602/0.8062/0.8246mm。四层同名文件提供 NRST(39.85,42.5)、UART_TX(54.75,19.85)、CAN源(61.85,11.4)、CAN目的端(37.65,15.8)、VBUS检测(51.25,13.65)，距离0.8944/0.9055/0.8944/0.9000/0.8944mm。

全部使用正常L28通孔、没有新规则例外。对实际规则全部相关字段、未来SOURCE21、UART03及remaining19一起筛选，排除了钻进SMD、孔间距冲突、晶振application void/guard shadow及非共地来源。历史实际BOTTOM或L2/L3 common面覆盖各0.6mm铜环，但此覆盖仍需最终刷新新反焊盘后的实际铜复核，不能写成新板完成。全组预审无交叠，新返回操作没有间距警告；其他源组59/61条简化字段警告继续保留，不能整体标成最终通过。

父任务最初的候选点也逐一检查：NRST(40.1,42.2)到信号线仅0.25mm小于0.3mm，UART地(54.45,17.8)到CAN_TX仅0.1mm，两板VBUS地候选均碰实际V3铜，因此全部被拒而重新选点。不能凭“距信号via小于1.5mm”认为地过孔可用。静态晶振电容孔即使最终同GND网，也不能拿来当普通共地返回点；必须排除局部quiet域。

## 22. 两层 CAN_RXD 07：完整信号路径与有限参考跨槽返回

当前候选 CAN_RXD_2L_engineered_07.json 含10操作，CAN_RXD从U5.4到R13.2的中心线总长52.3953mm，仅两个真实信号换层过孔。它是数字接收逻辑网，并非CAN_H/L差分对；不强行等长，不凭500kbps假设宣称器件输出边沿慢。SOURCE/USB关键铜/主供电/HSE不变。

BOTTOM从PHY (61.45,12.2)绕到USB壳下，中央y2.2，只有绕SH3/SH4时使用短y1.4段，避免TOP壳内走线；西端过孔(34.45,1.95)后TOP沿x34.05至y16.05，再斜接R13.2(36.3236,18.3)。TOP西线距实际V3总干铜边0.35mm，不能沿原x33.3短接V3。原04的SH3斜边对矩形壳脚拐角净距只有0.1263mm，小于两层thrupin_line=0.16mm；07把该斜边向右0.12mm，净距0.2111mm，水平壳脚段净距0.20mm。按真实矩形焊盘而非圆形或名义中心距离核查。

西端换层返回采用已有实际common GND组中的J2.SH3 plated壳脚，距信号孔1.391mm；不再把新地孔塞进板边V3供电。PHY新增地孔(61.7,11.2)距信号孔1.0308mm。壳下短y1.4段到名义BOTTOM地边0.5mm之间仅约0.5mm返回条带，中央y2.2扩大至约1.3mm，必须在最终实际填铜中测宽颈/连通及壳脚共地，不称整条是无限连续参考平面。

原低速VBUS检测BOTTOM x34.55纵段贴近TOP CAN西线。07只替换尚未执行的 HI_2L_VBUS_PRESENT_N_1_R1：检测网在y9.3..17.25移到x35.3，在y18.15..22.8移到x34.4。原pending操作必须明确排除一次，绝不能新旧并画成环；若集成时旧线已经实际写入，就必须另做唯一实际段精删delta。改后CAN右边到检测网参考让位区左边的名义地带增加约0.75mm，末端仍有一处有限交叉，不能称为整段完整微带。

该交叉配0.6mm TOP共地桥 (34.25,17.25)→(35.2,18.2)→(35.2,18.5)，两端各正常GND过孔，跨过BOTTOM检测网槽并与真实common面连接。桥与CAN平行段铜间距0.3071mm；它提供有限局部返回，不替代实际平面刷新/铜颈与时域边沿验证。早期05把检测线移x36.05撞R3共地孔(36.1,11.6764)，06仍有0.25<0.3mm，均留失败历史；07不以降低规则消除这些错误。

完整预审纳入 J2_GND_entry_2L_01.json 的四个新入口操作。原J2.A1_B12/B1_A12在b014终端图曾孤立，不能因SH1..4已共地便假称信号侧GND焊盘本来已通。当前243操作/504铜片组合无交叠，新CAN及检测网替换没有任何基线间距警告，其余源组59条继续保留。实际回流、GND图、入口端点、动态铜、HSE负测试及新进程完整DRC仍是原生验收要求。候选SHA D331E853C55FCB367530EE560DFA56D1DC12CEC90FAB33759812FAB970E040C5。

## 23. 普通GPIO可用的局部电源区域通道研究

应MCU组请求，只读评估粗SWITCHING_BLOCK矩形是否过度封锁。保留TOP热区、实际输入热环、L1本体投影与SW/BOOT/FB≥1mm避让，只研究BOTTOM有限窗口x28.3..30.9/y23.2..26.5。7条0.2mm/0.2mm直列中心x28.4、28.8、29.2、29.6、30.0、30.4、30.8，在两层y23.3..26.4局部均满足实际几何字段，距SW/BOOT/FB铜最少1.2316mm；TOP其他异网铜+0.3mm投影前6列为0，最右列约0.3765mm，仍需实际TOP地。

四层不能直接照搬同一端点：真实SPI_MOSI在BOTTOM y26.25横穿，初版研究因此失败。把四层窗口端点止于25.8后局部列才均清，若要继续向北必须在该SPI线之前真实换到TOP。readouts/PB_local_switch_corridor_02.json 明确区分两板，初版01保留。

这些结果只证明有限局部列，不证明七条GPIO源端能进入、过孔阵列能放下或北端能全部穿越SPI。V3过孔(33.3,22.5)与BOOT1孔(32.5,23.7)还夹住下侧入口，需联合源/桥拓扑。没有把这项研究写为可直接执行的全板走线、没有修改主feed或已冻源，也不把贪心搜索失败当成必须大改供电的证据。
'''
s=note.read_text(encoding='utf-8');assert '## 20. 原生 BOOT0 创建失败' not in s;note.write_text(s+text,encoding='utf-8')
readme=(P/'README.md').read_text(encoding='utf-8');readme+='''

新增阶段候选：remaining_returns_{2L,4L}_v19_02.json（普通网共地返回）与 CAN_RXD_2L_engineered_07.json（完整2LCAN接收支路、有限共地桥、pending低速VBUS网替换）。必须排除原检测网pending操作、纳入J2_GND_entry四操作，实际原生填铜/共地/负测/DRC尚待。BOOT y27.3对R28地焊盘.1935<.3的遗漏已修到.3135；原生创建失败独立actual诊断找出旧generated GND碎片，施工顺序修复对照详见笔记§20，未以关DRC/改全局规则通过。§23/PB_local_switch_corridor_02仅局部通道研究，不是七路全通释放。
''';(P/'README.md').write_text(readme,encoding='utf-8');print(json.dumps(dict(note=str(note),officialCopies=len(items),CAN07='Frozen candidate not nativeacceptance')))