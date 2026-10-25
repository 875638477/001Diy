# 第29课独立只读审查

日期：2026-10-19，Asia/Shanghai。范围：父任务要求独立复核第29课正式约束板，不启动Cadence、不修改第29课文件或用户工程。审查源码、来源摘录和记录全部位于01AIEDA。

**结论：正式v3原生约束证据通过937项独立检查，0失败。** 先前class-class导出仅有dbid无法独立解析名字的问题已补齐；以read_final02为正式重开来源。这里证明规则定义、映射、继承、实际DRC检出和回退，不代表全板布局布线或生产释放完成。

- [最终独立检查](../examples/lesson29_constraints_20261019_review/review_final.json)
- [独立审查源码](../examples/lesson29_constraints_20261019_review/scripts/review29.py)
- [审查输入证据SHA](../examples/lesson29_constraints_20261019_review/evidence_manifest.json)
- [独立基准连接关系](../examples/lesson29_constraints_20261019_review/baseline_connectivity.json)
- [正式原生板](../examples/lesson29_constraints_20261019/native/F29_CONSTRAINTS_v3.brd)
- [实际规则读回](../examples/lesson29_constraints_20261019/logs/read_final02/net_rules.tsv)
- [class-class名字／域／唯一via补证](../examples/lesson29_constraints_20261019/logs/read_final02/specific_proof.tsv)
- [挑战原始DRC](../examples/lesson29_constraints_20261019/logs/challenge04/challenges.txt)
- [独立coupon原始DRC](../examples/lesson29_constraints_20261019/logs/coupon_build.txt)

正式板SHA256：6276201EF1750D3A318D901CCF1ADFBB1CA41A4301329CD21E32A0E22B3FA607。新进程readonly重开及挑战副本均真实exitCode=0，磁盘SHA未变；未把早先v1/v2或超时未取到exitCode的尝试当最终证据。

## 1. 基准与继承关系

以第28课不可变基准独立形成逐pin连接表，再与第29课component_pins.tsv核对：80件、69个命名网络、272逻辑pin，包括6个NC完全保持；package、deviceType及器件pin数量一致。不同导出对无命名网络分别用空字符串或nil，审查只对这两种无连接表示做规范化，保留逐pin身份。

9组网络每组在physical／spacing／electrical三个域分别建立类，共27个真实NETCLASS；每个域完整覆盖69网，逐网反向指向及实际group成员互相一致。没有只凭类名判断域。另有3个真实DIFF_PAIR，成员分别为USB_DP／USB_DM、PA12_SHARED／PA11_SHARED、CAN_H／CAN_L。

物理CSet实际是10套（9个命名集加DEFAULT），并非早期准备稿的8套。GetPhysical／GetSpacing数值按当前mm单位解释；ECSet读回保留“1 MM”“6 MM”单位字符串。独立复核使用安装目录官方CNS接口说明，副本在审查目录source内。

| 物理集 | 最小线宽／最小颈宽 | 最大颈长 | 允许布铜层 |
| --- | --- | --- | --- |
| DEFAULT、P_SIGNAL_020、P_ANALOG_020、P_OSC_020 | 0.20／0.15 mm | 1 mm | TOP、BOTTOM |
| P_POWER_060、P_SWITCH_060 | 0.60／0.25 mm | 1 mm | TOP、BOTTOM |
| P_CAN_025 | 0.25／0.20 mm | 1 mm | TOP、BOTTOM |
| P_USB_PROVISIONAL | 0.20／0.15 mm | 1 mm | 仅TOP |
| P_VDDA_030 | 0.30／0.20 mm | 1 mm | TOP、BOTTOM |
| P_GND_PLANE | 0.60／0.25 mm | 1 mm | TOP、L2、L3、BOTTOM |

GND和VDDA仍属于POWER_LV分类，但直接指定P_GND_PLANE及P_VDDA_030例外。最终所有net属性仅保留原LOGICAL_PATH及这两项指定例外；没有残留挑战中MIN_LINE_WIDTH或临时MAX_VIA_COUNT覆盖。P_GND_PLANE是给后续地铜的许可条件，尚未完成整板地铜。

所有物理集的允许via只有L28_VIA030_C060。原生唯一via补证显示实际仅1个GND教学via@(52,35)，没有把视图返回的多个关联别名误算为多个via。

## 2. 间距、class-class和实际层叠

7套spacing CSet的line_line分别为DEFAULT0.20、POWER／ANALOG0.30、USB0.15、CAN0.25、USB_OTHER0.50、ISOLATE1.00 mm，四铜层均有实际值。

| class-class规则 | 实际CSet／间距 |
| --- | --- |
| USB_FS_S ↔ DIGITAL_GENERAL_S | S_USB_OTHER_050，0.50 mm |
| SWITCHING_S ↔ USB_FS_S | S_ISOLATE_100，1.00 mm |
| SWITCHING_S ↔ OSCILLATOR_S | S_ISOLATE_100，1.00 mm |
| SWITCHING_S ↔ ANALOG_SENSITIVE_S | S_ISOLATE_100，1.00 mm |

原始class_table.tsv仅列两端dbid，不能独立证明四张表分别连接哪些类。经反馈后read_final02/specific_proof.tsv补出两端真实名字与spacing=t、physical/electrical=nil，四条表均闭合。官方API允许构造跨错域表，但DRC可能忽略，所以这项实际域核对必要。

完整stackup_full.tsv与第28课材料、厚度、Dk、mask、导体标志、正负片及来源标签逐项一致；物理铜序TOP-L2-L3-BOTTOM不变。真正DESIGN_OUTLINE／KEEPIN／KEEPOUT的bbox和顶点也与第28课显式层查询逐条一致。已保存板没有遗留挑战ETCH走线。

## 3. USB两侧、分支与装配前提

两个USB差分对通过实际net继承得到MAX_VIA_COUNT=2、Phase Tolerance=1 MM、Max Uncoupled Length=6 MM；不是只给ECSet填数字后假设已分配。实际生效模式包含Maximum_Via_Count及Differential_Pair_Primary_Gap。Phase在本例单位为长度，不是相位角或延时认证。

独立从原始逐pin连接确认：

- USB_DP：J2.A6/B6、U4.1/6、R5.2、R11.2；USB_DM：J2.A7/B7、U4.3/4、R6.2。
- 22Ω电阻另一侧：PA12_SHARED=U1.33/R5.1/R12.1，PA11_SHARED=U1.32/R6.1/R13.1。
- USB_PULLUP_SRC=R11.1/Q2.3，形成D+上拉支路；共享CAN侧装配互斥由R12/R13等DNP条件控制。

因此不能把真实连接器重复pad、ESD同通道双脚、上拉及共享接口分支写成无分支点对点网络。后续布局应缩短汇接与支路、按ESD路径穿过保护器件，并控制未装支路的物理stub。配对／长度规则和DNP备注不自动消除PCB铜支路。

USB的0.20 mm线宽及0.15 mm间隙明确属于暂定几何；没有板厂90Ω确认。L2/L3只允许GND铜的规则与第28课S/G/G/S意图一致，但还要在后续真实布局、铺铜和换层中验证回流。

## 4. 受控挑战实际证明了什么

| 挑战 | 原生DRC实际名称与读数 |
| --- | --- |
| DEFAULT_WIDTH | Minimum Neck Width，要求0.15、实际0.10 mm，source=P_SIGNAL_020 |
| CLASS_POWER_WIDTH | Maximum Neck Length，要求1、实际10 mm，source=P_POWER_060 |
| NET_OVERRIDE | 临时MIN_LINE_WIDTH=0.20 MM解除该长颈违规，随后回退 |
| DEFAULT_SPACING | Line to Line Spacing，要求0.20、实际0.10 mm |
| CLASS_CLASS_ISOLATION | Line to Line Spacing，要求1.00、实际0.50 mm，source=S_ISOLATE_100 |
| UNAPPROVED_VIA | Via List，实际非许可via，在TOP/L2/L3/BOTTOM检出 |
| USB_MAX_VIA | Maximum Via Count，ECSet要求2、实际3，source=E_USB_FS_BUDGET |
| L2_POWER_BLOCKED | Allow on ETCH Subclass，实际V3V3在L2被禁止 |
| L2_GND_SHAPE_ALLOWED | 实际GND填充shape在L2允许，0错误 |

前两例验证宽度／颈宽／颈长的联合作用，**不能改写成已独立触发Minimum Line Width 0.20／0.60 mm报错**。逐个挑战回退后都为DRC0且状态current，最终也为0/t，临时属性没有进入正式板。

## 5. 长度coupon和自动场求解失败的边界

独立coupon原始DRC记录：Phase Tolerance要求1 MM、实际7.6 MM；两网未耦合长度要求6 MM、实际10及17.6 MM。修正后两条实际线段分别从x=5到25，独立按端点计算各20 mm，宽0.2 mm；新进程重开为0/t。官方axlPinsOfNet另行读回每网2个pin、unconnected=0、unplaced=0；四个实际pin坐标与两条线的端点完全吻合。原始net->pins属性显示0是查询口径差异，不能据此判断连接断开。

coupon过程中软件自动调用bem2d并报failed，原stdout保留。这里只采信实际长度／未耦合长度DRC及修正后几何；没有把自动求解尝试、DRC0或ECSet里的数字当成90Ω、传播延时、完整SI／PI／EMI认证。

官方techfile.exe导出F29_RULES.tcf后再比较，实际exitCode=0、No objects were updated、板SHA不变；技术文件SHA也独立核对。但TCF不是全net/object DCF，实际网络及group映射仍由原生读回来证明。

## 6. 结论范围与学习记录

独立审查通过的是正式约束板、许可规则、域映射、局部例外、几何保持、原生检出与回退。79个逻辑器件仍未布局、参考铜面尚未整板铺设；不能将当前0 DRC解释为完成全板布局布线。

第28课已记录的阻焊桥、1.6 mm板厚与USB固定脚长度、制造公差和90Ω几何确认条件仍保留。第29课的约束学习完成不解除这些实际制造／装配要求。

本审查没有修改第29课源文件、启动Cadence或改用户工程；所有新增审查材料在learning/examples/lesson29_constraints_20261019_review及本笔记中，方便换机继续追溯。
