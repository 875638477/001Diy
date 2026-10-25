# 新四层默认实际应用：独立结构与参考审查

日期：2026-10-23。新记录位于01AIEDA/JK，旧已封存J51—54与K58组不修改。本代理仅仅读取正式原生读回；Cadence由f29唯一执行。

## 结构结论和文件身份

新板结构应用通过，主独审73项0失败；另8项规则/真实段补证0失败。真实新板为`JK_4L_L2_GND_L3_V3V3_STACK_TRAINING_NOT_RELEASED.brd`，SHA256 `471176A9B25BA8DEF9F117AEFB1E9220CBCBEBBAC5191BCBC6E228F52831F3F9`。

源是已做三文字/高度修订的J55四层副本，SHA256 `9DEC773FE106E09C9844FEF5F160E1A1B3348BFC693926579F0CAF0A6A18DCF0`，不是直接覆盖HI b019。完整报告：[review.json](../examples/lessonJK_51_59_20261022/review/independent_newstack/review.json)。状态明确为`PASS_INDEPENDENT_NEWSTACK_PHYSICAL_LAYER_APPLICATION_WITH_OPEN_SI_PI`，不是整板release。

实际层名/物理层序保持TOP-L2-L3-BOTTOM，原物理材料/厚度/Dk、无物理MASK、全部17Film/Options、板框/孔保持。实际L2有单一公共GND母形和已填充面，旧HSE静态参考岛/永久moat退休；L3有单一实际V3V3母形和电源面，不再有L3 GND母面。GND过孔盘/反焊盘仍是合法真实对象，不能因L3电源就将它们误当残留GND平面删掉。

全部56真实GNDpin及76GNDvia共L2公共面，32个V3V3pin及3个V3V3via共实际L3电源面。独立以actual vias.tsv和native图成员逐个核对，未靠中间cache摘要。80器件及272pin的网/anchor/rotation/焊盘、源文字和封装几何、机械及完整Film保持。装配专项另以官方device VALUE核全部80值；本结构脚本没有靠deviceType后缀猜值。

## 真正的保线证据和检查修正

原生接口GetConnect曾只取path父对象，未递归segments，导致旧新增采样表写manualSegments=0/samples=0；这不是“参考通过”，其manual子守卫也不能证明保线。旧空表原样保留NOT_EVIDENCE。

本独审直接用官方fgeo的route_geometry和hi_route_roles判别line/父path thermal，逐(net,layer,width,startEnd)多重集合比较：source750段manual→新750段manual，完全相同，无增删，非GND内层信号为0。新生成thermal有意随平面改变，不能和manual混计。f29另做只读补证真实932段=750manual+182thermal，与独立fgeo集合再核相同。

补证新参考采样收齐658段非GND外层manual/18854点。TOP→L2为11405点，其中928点无公共参考覆盖；BOTTOM→L3 V3为7449点，其中660点无覆盖。这些含端部/反焊盘及实际缺口，不能把非空采样当全通过，也不能把每个样点缺口自动当失败。

本独审另有两项初稿假失败：物理pad表3424行与via表600行只是枚举顺序改变；已以重数和全部字段Counter核完全相同，未放宽几何或丢行，失败稿保留。脚本分段写入缺换行、TSV末尾COMPLETE标记误作数据的错误也已修正；附加检查确认跳过的仅为显式完成标记，不丢实际数据行。均不属于native板错误。

## 新HSE与规则边界

旧“删唯一anchor后C22/C23必须断开”的预期只属于旧隔离架构，已退休。新架构临时删除旧anchor后，C22/C23仍通过完整L2公共地相通；原生反测实际结果为仍共地，rollback恢复。TOP guard仍可保留，其高频效果/晶振启动裕量仍非本次硬件实测。

原全部PSet字段保持，仅V3V3增加专用`JK_P_V3V3_L3_PLANE`直赋；对照源PSet全层全字段，只有L3 allow_etch由nil变t用于电源面，L2仍nil，普通内层信号没有开放。其余68网assign、group、Spacing/Electrical源表保持；新GND/V3V3逐网DRC各0。不能把旧65非USB或这两个0扩成新全板DRC。

## 实际SI/PI返回仍开放

新参考必须按真实网络理解：TOP看L2 GND，BOTTOM看L3 V3V3。103个net/layer完整线宽足迹已用真实native多边形和全部holes独立重算，signed-arc与mm4量化边界保留，最大面积转换误差.003629mm²（逐形<.01）。文件：[actual_reference_footprints.json](../examples/lessonJK_51_59_20261022/review/independent_newstack/actual_reference_footprints.json)。这不是阻抗或HF电流仿真。

实际PA11_SHARED/PA12_SHARED中心线L2覆盖，但全宽仍分别缺.020452/.038544mm²，不能用中心线代全宽。USB_DP TOP仍有1.2002mm中心参考开口；其1mm BOTTOM入口桥整段位于反焊盘区域。SPI和North局部也有端部/反焊盘等开口，需要按具体路径、同层地边与实际返回解释；没有宣称新栈自动修完USB参考问题。

8颗现有V3-GND电容C9/C11/12/C13/14/15/C16/C17两端已分别native到L3电源/L2地，建立了DC/图连接依据。但66个signalvia的GND→V3参考转换仍逐项工程OPEN：地stitchvia只连地，不直接耦合电源参考；电容共网且距离近也不自动证明局部低感回路/有效C/ESR。PA2远端via(17.5,52.6)到最近既有C9两脚的最大直线距离约26.686mm，另一PA2远端约24.154mm；SPI_MOSI一处约17.304mm。它们是具体需后续分布去耦/改走层/实际回流审查的线索，不是批准新的通用距离阈值。

文件：[reference_conversion_caps_and_vias.json](../examples/lessonJK_51_59_20261022/review/independent_newstack/reference_conversion_caps_and_vias.json)。L2-L3 core保持原1.065mm，不能凭电源/地层名假定足够的高频平面对耦合。

仍有7个SouthGPIO未接；4个USB检查与全板DRC、负载/边沿/线缆/MPN有效电容/温度/ESD/EMI/实物待办均保留。本次学习验收只关闭“新默认实际层功能应用”，HI原板仍是其历史L3GND输入，旧封存记录不覆盖。

## 跨组输出与归档

root的实际CAM独审为85/85、逐Film新旧几何34/34，只L2/L3变化，其余15Film同，见本课review/independent_CAM_NEWSTACK。该结果与本独审的750manual全保互相支持，仍不是制造放行。f27提供新板SHA身份的BOM/坐标/装配副本；不得把旧板身份文件改名当新输出。

本组新审查、规则/采样补证、失败修正、脚本和此笔记另封artifact_manifest；可变进度policy与长期pcb_layer_naming不作为sealed依赖，只引用不可变合同与正式native源。原HI/01env及已封存J51—54/K58源均保持。
