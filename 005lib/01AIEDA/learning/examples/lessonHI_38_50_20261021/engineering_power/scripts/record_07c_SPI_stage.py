from pathlib import Path
R=Path(r'D:\001DIY\005lib\01AIEDA\learning\examples\lessonHI_38_50_20261021\engineering_power');n=R.parents[2]/'notes/lessonHI_power_20261021.md'
s=n.read_text(encoding='utf-8')
s=s.replace('当前返工候选为 **STAR_reroute_07b.json**','当时返工候选为 **STAR_reroute_07b.json**（现为失败历史，最终07c见第12节）')
append='''

## 12. 2026-10-22：07c真实验收及两层SPI协同设计

07b的独立几何比较没有发现间距问题，但原生postcritical b009报出唯一MaxNeck：新返回细颈1.4654mm在旧G31_GND_ESCAPE的1.4mm区域内，新小区1.5mm不能覆盖旧区更严限制。不能据此扩大旧G31或全局预算。07c把正常0.6mm起点提前到(36.952,25.222)，保留(36.48,24.75)前一拐点；完整0.25mm新颈长1.397508801mm，处于原1.4mm内，新小区也改1.4。与b009真实全部铜只读预审966项通过；b010从USB8稳定源重新执行而非叠加失败候选。

原生两板postcritical b010均0DRC且新进程只读重开/hash稳定：

- 4L native/HI_4L_postcritical_4L_b010.brd，SHA256 A9215927856EF4D3AD6D6CBAE3F227365EE09640821C8403336863C0A35F9437，473段/58via/63remaining。
- 2L native/HI_2L_postcritical_2L_b010.brd，SHA256 76ED85DA3999A7DAFBDF9EB99EEC425B480A5EAEB49843BF970F8664707DE0AF，58via/62remaining；actual410 ETCH segments含生成热焊盘，不把总段数当手工走线数。
- 04/05 CAN、06b外设取电、07c返工及根source5等已实际执行。上述是固定历史检查点，后续b011增加地stitch及其他数字线时仍以最新native/current为主。

两层外部SPI起初按根v5电气候选评估：SCK BOTTOM y29.95下方有U3 VIN/EN/VOUT铜，MISO y30.8下方有C8/C9正端；即使后面铺TOP GND，也无法在真实电源焊盘上变出参考地。把四层SCK via单独搬到(31,29.95)又会与两层MISO via(31.5,29.85)相交，这个跨变体单点照搬建议没有执行。后续必须把四线和返回一起设计。

本专项产出 SPI_external_2L_engineered_v9.json（35操作：3条精确删铜、15route、8signalvia+9GNDvia）。按b010真实铜/过孔/保守焊盘AABB比较28656次0问题；MCU专项另作27441次独立比较，无小于0.2mm异网铜间距，无钻孔进入SMD pad，离HSE moat最近6.489mm。两份预审均不是原生全板验收。

- 源端source5不改，串阻顺序保留。SCK局部BOTTOM桥8.95mm在y29.95，之后回TOP并在西侧早降至J6.2；源via(30.8,29.95)与MISO via(31.65,29.77)联合定位。
- MOSI局部BOTTOM先y28.3再28.5，避开L1 SW copper land投影和C8/C9既有GND via；之后回TOP到J6.3。仍有TOP V5投影，不声称对面全地。
- MISO BOTTOM y30.8→TOP到J6.4；NSS BOTTOM y32.3，避J10接地stub(23.73,33.052..34)，再TOP到J6.5。MISO的外部接收端0Ω不等于源阻尼。
- 第一根0.6mm BOTTOM guard y29.25从既有C9共地via(28.6,29)引出，为clock/MOSI局部提供同层返回；第二根y31.55、0.6mm guard直连(27.1,31.55)/(21,31.55)两个GNDvia，位于MISO/NSS之间。
- 仅把低电流、10Ω前的TOP V3预滤波横排y32.35上移0.20至32.55、拐点28.4改28.2，给第二guard地via提供真实间距。精确删原3段，不留电源铜桩；R26后VDDA/ADC/本地滤波不变。原08长BOTTOM电源桥没有采用。

返回专项 readouts/SPI_external_2L_v9_return_plan.json 的8个signalvia最近GNDvia中心距0.856—1.490mm。冻结真实BOTTOM地面减去新信号线0.3mm保守halo和signalvia半径0.6mm切口，再合入合法GND guard/via，全部新GNDvia和两根guard在同一预测common GND连通块中。这仍是几何规划，需原生动态铜刷新后以实际铜重做。

为避免把“地网连通”当成返回合格，另将预测common GND腐蚀0.299mm，寻找至少0.598mm宽的地通道核心，沿桥每0.1mm采样（端部0.7mm过孔转换区单列）。SCK/MOSI/NSS中心至最近宽地核心最坏0.699/0.714/0.699mm；MISO源侧拥挤拐角局部为1.642mm，坐标约(30.893,30.757)，需最终真实填铜审查并明确条件。此数值不是板厂阻抗/高速认证，也不隐藏成“全程等距参考”。SPI初始<=1MHz并采用最低足够GPIO输出边沿，仍须看实际边沿/负载，低时钟频率不能消除快速边沿反射。

TOP异网铜加0.3mm预计GND让位区，与上述BOTTOM桥中心线重合长度分别5.70/12.53/6.80/7.84mm（SCK/MOSI/MISO/NSS）。这组数值明确记录其同层返回意图，不把这些区域宣称为连续TOP参考。J6仅pin6为地，外部排线/负载回流、引脚次序和边沿仍有限制；未改变原理图或伪造相邻地脚。

四层原根外SPI v5另审：对b010原生已生成L2/L3地铜投影，全部0.2mm信号铜足迹除自身J6 THT正常反焊盘外均被真实参考覆盖。只排除实际自身pad AABB+0.301mm，原始缺口面积仍保留。新signalvia antipad尚未生成，最终刷新、返回stitch及近SW MOSI耦合仍需核，不能靠层名宣称完整性。报告 readouts/SPI_external_4L_v5_actual_L3_projection.json。

局部via均没有钻入实际SMD铜，但bodyExtent/PlaceBound并非已核MPN实体外形。特别C9附近via钻边与库包围范围有约0.039mm投影重叠，真实物料实体/tenting/贴装吸锡及容差需保留；不能将数据库包围框直接称实物合格或判定必然撞本体。

## 13. 原生地铜小圆弧舍入与审查工具勘误

cadence_poly.py继续按官方axlPolyFromDB半径属于前点→当前点、正负表示圆心局部Y轴左右以及象限切分语义处理。b010有两条极短水平弦在舍入后使两个圆心的左右判别均满足浮点符号，旧断言因此拒绝读取；没有据此忽略整个孔洞。保留原解析器cadence_poly_v1_before_rounded_arcs.py，仅在模糊弧的最大弓高<=1e-5mm（10nm）时用弦，并在ROUNDED_ARC_FLATTENED逐项记录。正常弧保持原方法，其他歧义仍报错。

arc_b010_area_audit.json涵盖两板10个真实平面，实际被折弦的最大弓高5.43nm，小于保守外缩/孔扩0.0001mm（100nm）；最大原生面积与转换面积差0.003342mm²。孔列表nil也必须显式转为空列表，不能将nil误当有孔或漏掉全平面。SPI预审脚本中一次PowerShell多行替换误加首尾引号产生SyntaxError，已修复并重跑；没有因此修改设计或放宽原生规则。

本节新增全部方案仍属于独立工程准备/预审。最终完成必须有当前原生板、全量DRC、实际地面/护线/参考缺口验证、连接证明和新进程重开；不可用此目录候选或旧manifest的PASS替代最终状态。
'''
if '## 12. 2026-10-22' not in s:s+=append
n.write_text(s,encoding='utf-8')
readme='''# HI 电源、接口和两层SPI专项入口

本目录为2026-10-21开始、跨2026-10-22继续的学习专项。笔记：../../../notes/lessonHI_power_20261021.md；主整板入口由根任务维护。

当前已执行的电源/接口组合是 STAR_reroute_07c.json + V3_peripheral_distribution_06b.json + interface_CAN_routes_04.json + CAN_local_supply_05.json，ESD_ground_routes_04c.json随USB8一起实施。两板postcritical b010原生0DRC且只读重开通过；具体SHA与范围见笔记第12节。07/07b及旧06/04b为失败或废弃历史，禁止当当前执行入口。07c实际细颈1.397508801mm，在旧1.4规则内；未扩大原G31/全局。

当前待合并的两层SPI候选：SPI_external_2L_engineered_v9.json，35ops，source5固定。独立实际铜预审readouts/SPI_external_2L_v9_precheck.json，28656比较0问题；返回方案readouts/SPI_external_2L_v9_return_plan.json，明确同层0.6mm GND护线、预滤波TOP横排+0.20mm微调、全部signalvia最近GND<=1.5mm及MISO局部1.642mm宽地核心距离。不得把“候选”或“预测commonGND”写成实际动态铺铜验收。

四层SPI候选的真实参考面投影：readouts/SPI_external_4L_v5_actual_L3_projection.json，除自身THT正常反焊盘外L2/L3覆盖；新via反焊盘/最终返回仍待原生刷新。原VDDA_prefilter_reroute_08.json仅历史预案，当前两层候选不采用其长BOTTOM电源桥。

固定历史02d/03c独立审查分别1798/1880项通过，不代表后续全板完成。各v6/v7/v8失败SPI候选和报告保留，记录斜线实际最小间距、via相撞、库焊盘与工程回流的联动修正。scripts/build_*属于当时生成过程，旧版不要重跑覆盖新版。

scripts/cadence_poly.py提供官方弧线语义的只读几何转换；极短舍入弧有弓高<=10nm的可审计折弦，旧解析器留存。readouts/arc_b010_area_audit.json覆盖两板10平面，最大原生/转换面积差0.003342mm²。导入者配置根tooling/packages；不运行Cadence。全新资料/脚本/缓存/临时记录仍只能放01AIEDA。

artifact_manifest.json是阶段清单而非最终布线验收。原生current/最终manifest和主任务记录优先；DRC0/零飞线不证明SI/PI/EMI/制造装配合格。具体制造开放项及ESD阻焊名义零余量见笔记第8/11节。
'''
(R/'README.md').write_text(readme,encoding='utf-8')
print(str(n))