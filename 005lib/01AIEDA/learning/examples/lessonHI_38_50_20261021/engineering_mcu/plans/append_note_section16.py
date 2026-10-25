import pathlib
B=pathlib.Path(r'D:\001DIY\005lib\01AIEDA');p=B/'learning/notes/lessonHI_mcu_20261021.md'
addition=r'''

## 16. 普通 GPIO 之前先联合扇出与源端可接续性（2026-10-22，进行中）

本节是工程候选与纠错记录。第 11—15 节的 MCU6、USB8 是各自不可变原生检查点的历史证据；后续器件移动、供电改线、地形变化必须重新验证。不能把历史 0 DRC 或 USB 参考走廊覆盖到尚未执行的新源端/普通网络。

本轮按原生 b014 真实焊盘、272 个逻辑引脚、实际过孔、全部手工/固定铜线及机械孔建几何障碍。GND 同网不代表安静振荡地与应用地可以直接相连；HSE 原有真实 guard 的铜宽加工程余量也在 TOP/BOTTOM 普通信号禁穿区内。机械 J2 空位号的两颗 Ø0.65 对位孔必须单独读实际钻孔，不能因 regular pad 为 NULL 而漏掉。

### 16.1 源端要给后续网络留出口

- 北侧拟定 [north02](../examples/lessonHI_38_50_20261021/engineering_mcu/plans/GPIO_north_joint_fanout_02.json)：PA1/PA2/PA3 分别给明确出层点，PC15 的原底层折线也联合调整。PA2 先接续再处理 PA1，可以避免先走 PA1 把 PA2 夹在 PC13 partial 与自身新线之间。顺序只是候选求解策略，最终仍逐段复核，不称自动布线即可完成工程设计。
- 左侧 [left07](../examples/lessonHI_38_50_20261021/engineering_mcu/plans/GPIO_left_joint_fanout_07.json) 联合 PB1/PB10/PB11/BOOT1 与 pin18 VBUS_PRESENT_N。PB11 出层点改为 (33.7,25.3)，PB1 改从内侧到 (38.3,27.35)，给 pin18 外侧 (34.6,26.85) 留真实可接续出口。PB1 的短窄线全长约 2.7542 mm，其中一段按两颗实际过孔间隙采用非 45° 斜段，必须记录其几何原因，不能隐瞒为全板 45° 标准走线。
- 为达“地孔距离 ≤1.5 mm”而先放地孔，会把普通信号出层点封成口袋。原 left04/05 拟加 GNDvia(33.28,26) 因此取消。PB11 仍靠继承 C13 应用地孔，PB1 的实际返回则须在全长路和填铜后核，不机械地追求一个距离数字。
- 南侧 PB15 原下行底层短颈与根组后来挪至 (38.8,19.7) 的 GNDvia 实铜重叠，不能只审查新服务线。已记录 [PB15 上行替换 delta](../examples/lessonHI_38_50_20261021/engineering_mcu/plans/GPIO_PB15_bottom_exit_delta_01.json)，用 BOTTOM (38.5,20.7)→(38.5,22.3)、宽 .16、长 1.6 mm、局部 maxneck2.4；只在 PB14/USB_ATTACH_N 两个邻过孔的有限 via_line 字段用 .16。没有保留原下行死端。

这些小孔使用原生已核的私有 `HI_VIA026_C052_TENT`，Ø.26 钻孔、Ø.52 铜、单边环 .13、mask NULL。最初 `hi_via026_c052_tented` 为 21 字符，超过本机官方 PADLIB 20 字符限制，已缩为 19 字符并保留映射/失败准备源。不是通过改公共库解决。两层 OSH 已公开孔最小 .254、环最小 .127，当前仅 .006/.003 的名义裕量；实际刀具、成品孔口径、公差、帐篷阻焊仍是制造待确认。四层 JLC 公开多层孔/铜环能力分别核，不沿用两层认证。

原生许可预审进一步证明：through via 的 approved list 要在每个实际铜层有正确作用域，只放 TOP 小区域会在四层 L2/L3/BOTTOM 继续报 ViaList。只增加小孔许可的区域逐层复制真实父 Physical CSet，其它线宽、颈长、层许可不改。实际区域交叠会采用更严格预算，不能把 JSON 中写了 2.8 就当原生已生效。

### 16.2 长 NSS 上拉支路应先改布局，不能靠绕全板挤 GPIO

NSS 上拉支路虽然直流电流小，其铜线仍是 NSS 信号残桩。原内侧 TOP 加 BOTTOM 约 19 mm 的支路，与 TOP MCU 电源横干共同围住普通信号；找到 83—119 mm 绕 USB/板边的候选不能作为合理设计交付。

冻结的 [NSS04_SOURCE_ONLY](../examples/lessonHI_38_50_20261021/engineering_mcu/plans/NSS_pullup_local_relayout_04_SOURCE_ONLY.json) 将 R25 置于主 NSS 节点附近，残桩中心线约 1.89906 mm。必要布局为 R21(33.7016,30.7)180°、R23(33.5,32.1)180°、R25(31,33.7)0°、R32(31,35.5)0°。保持 R21/R23/R25/R32 的原理逻辑/值，精确删除原 SPI 源侧和接口侧相关旧段并重接，不能只拖器件留旧铜。

MCU U1.10→C24.1 的 ADC 主路径原样保留。移动 R32 后，只重做输入端与 R32→C24 的 RC 前级铜；新 ADC0 竖向段 x33.65 是为避让 C24 真实 .6 GND 返回及 R25 焊盘，不是凭器件中心拉一条直线。新的输入/串阻路径与相应参考保护区须一并更新，不能拿旧路径的参考审查替代。

[四层原类别/真实焊盘检查04](../examples/lessonHI_38_50_20261021/engineering_mcu/plans/NSS_pullup_relayout_class_review_4L_04.json) 29,042 对、[两层检查04](../examples/lessonHI_38_50_20261021/engineering_mcu/plans/NSS_pullup_relayout_class_review_2L_04.json) 29,380 对，无名义类别间距违规；此结果包括移动后的元件焊盘，并非只检查新增线。原生连接图、真实 CSet、填铜、重开和 HSE 单 anchor 负测仍待完成，不能将此称作原生 DRC 通过。

Source04 特意保持原 C9via(30.7,32)、原 C9 TOP feed、原 BOTTOM STAR 对角和 37,24 via、原 SPI guard。它仅从原 C9via 加 R25 的短电源支路。后续若更换主供电入口，独立 delta 应按实际原生对象删除原 STAR 两段/末端 via，不能重复套用此前被否决版本的移孔操作。

### 16.3 已发现并保留的失误

1. left04 的 PB11 出层原拟 (33.5,25.3)，基于较早 b010 场景看似可用；SPI b012 新增 GNDvia(32.8,25.3) 后，.52 信号孔对 .6 地孔铜间距只 .14，低于两层公开工艺 .1524。改 (33.7,25.3) 后铜距 .34。每次新原生检查点都必须重纳所有旧/新过孔，不能只比本组旧板。
2. left03 曾出现“输出 anchor 改了，但实际 via op 未同步”的脚本替换问题。交执行前增加 source op 与 partialEndpoint 坐标一致断言，旧候选保留，不冒充已经创建的原生孔。
3. NSS01 的 R21 y30.6 新输出焊盘与两层真实 MISOvia(31.65,29.77) 只有 .1235，检查制造最小距离或只看新线均不足。按原类别+移动焊盘补查后，改 R21y30.7 恢复 .2235，邻 R23 也联合挪位。
4. [NSS03](../examples/lessonHI_38_50_20261021/engineering_mcu/plans/NSS_pullup_local_relayout_03.json) 曾手拟主电源沿 x29.8 直下，在未先逐一核 C9.2 与 buck 反馈/地焊盘时猜了路径。真实铜审查发现跨 C9 GND 焊盘/地线及 R2 反馈区，明确否决，未交原生执行。以后先由实际焊盘/线/孔建完整障碍，再规划电源路径；不能依靠封装原点或记忆猜净空。主 feed 改道交电源组按实际铜设计。
5. 原型搜索把整块 SPI bank 或 ADC 任意 buffer 当硬禁布，会把合理局部跨层判为“无解”。它们不等同用户/制造硬约束。HSE 主 quiet/moat/真实 guard 的禁入继续严格；其它投影交叉要按实际有限开口、同层地、近返回与线路优先级审查，也不能反过来称所有投影交叉都没有影响。

### 16.4 当前未完成项与验收边界

13 路普通 GPIO 全长路仍在联合规划。旧搜索的“找到/失败”只是候选，不是实际通断；曾发现 source 颈线 .16 合法而强制按 .20 倒走同路径扩大铜宽造成假封口，也发现栅格过保守膨胀误挡有限间隙。候选改为精细名义掩模后，仍对每段做连续几何验证；不能用降低栅格安全余量替代原生 DRC。

为与电源组协作，另有明确标为 `CONTINGENT_GPIO_CORRIDOR_STUDY_MAIN_POWER_NOT_COMPLETE` 的抽象场景，暂移除原 STAR 大对角观察普通 GPIO 走廊。该场景电源尚未接回，绝不是可用 PCB 或电气完整设计；必须有合法新主 feed、实际地返回及全组几何后才可转成原生批次。

最终还要逐板验证：全部逻辑引脚/80 件/69 网保持；13 GPIO 每个 U1→header 真图；新小孔全实际层许可；每条短颈/区域内外挑战；GND 无孤岛/孤枝；HSE 唯一 anchor 断开后局部岛保持互连但不达应用地/壳地，恢复后重新通；USB 两插向主铜和 DNP 残桩/参考；新 ADC、晶振护地及电源/接口有限返回。不会从“全部连通”或“0 DRC”推出制造、90Ω、USB、ADC、SI/PI、EMI 辐射或硬件性能已通过。
'''
p.write_text(p.read_text(encoding='utf-8')+addition,encoding='utf-8')
print('appended',len(addition),'characters')
