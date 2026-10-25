# 第27—29课复核中的来源与机械基准勘误

日期：2026-10-19（Asia/Shanghai）。本记录更正历史笔记的依据与措辞。原PDF、已验收封装的铜/孔坐标、真实板上高度及原生文件均未因本勘误改变；当前学习工程仍沿DE_BASELINE谱系，未暗改原理图或网表。

## 1. USB4105壳脚长度S的基准

依据GCT USB4105 Rev B4第1页侧视及订货表：[原厂图](https://gct.co/files/drawings/usb4105.pdf)，本地[已归档PDF](../examples/lesson10_connector_20261018/source/usb4105.pdf)，SHA256 FB331FBABEE8392ED2937ED757C1610CB0F174B84625147C0B580A18EEA8C0E5。

Shell Stake Length的S=0.95±0.15mm表示从器件安装基准面向下的壳脚长度，不是壳脚穿过任意厚PCB之后在板底额外突出的长度。早前中文“板下侵入0.80～1.10mm”未说明基准，容易造成错误理解，现统一改成“由器件安装基准面向下的长度”。

若仅作几何算例，假定器件安装基准面与PCB上表面重合、无额外离板间隙，尖端相对板底的有符号突出量为S−PCB成品厚度；实际还需代入座高、焊料、材料和制造公差。不能从S单独推导板底突出量。

- 0.8mm名义教学板、0.95mm名义S，零座高差的算术突出量为0.15mm；壳脚最短0.80mm时与名义板底齐平，不能保证所有公差下穿出。
- 1.6mm名义教学目标与0.95mm名义壳脚组合没有证明穿透到板底。不得写成“板下还伸出0.95mm”，也不据此判定工艺必然失败：是否允许短插脚、从顶面焊接、穿孔回流或其他工艺，需要厂家和装配工艺确认。
- 订货表中的0.60/0.95/1.20mm是不同壳脚选项，不能把某一选项的后缀与另一长度混用。
- 原生MAX高度3.46MM是板上高度包络，仍按第10课的3.31尺寸及一般公差记录，与此处壳脚S分开。

B10原[spec.json](../examples/lesson10_connector_20261018/spec.json)的字段stake_below_seating_plane_mm已经采用正确安装平面基准；本次主要纠正中文解释和跨课程继承措辞。B10软件孔/land尺寸验收不等于任何板厚下装配工艺已通过。

## 2. USB串阻22Ω的依据不能冒称器件强制要求

原厂核读：[DS5319 Rev20](https://www.st.com/resource/en/datasheet/stm32f103c8.pdf)的USB电气参数页（实际PDF第72—73页）规定USB工作与外部D+上拉等条件，未查到“必须串22Ω”的推荐。相同PDF已在[本地来源](../sources/de_15_26_20261019/DS5319.pdf)归档。

当前[AN4879 FAQ](https://www.st.com/content/st_com/en/technical-documents/an4879-introduction-to-usb-hardware-and-pcb-guidelines-using-stm32-mcus-stmicroelectronics_asset/chunk-005-topic-an4879-faqs-frequently-asked-questions.html)及[VBUS章节](https://www.st.com/content/st_com/en/technical-documents/an4879-introduction-to-usb-hardware-and-pcb-guidelines-using-stm32-mcus-stmicroelectronics_asset/chunk-003-topic-an4879-vbus-sensing-detection.html)说明内部PHY已经具备相应输出匹配阻抗，不能将外部串阻当作所有STM32 USB的必要匹配。

因此，D/E先前采用的R5/R6=22Ω应视为**未经本板波形验证的历史工程选值**，不能称为F103数据手册硬性要求或USB认证条件。后续布局/装配定版前应复核默认0Ω/跳接或实测调试值，并通过受控原理图/BOM/ECO更新保持一致；不能只改PCB上的VALUE造成前后端不一致。本轮F教学板保留既有22Ω实际值和逻辑连接以追踪输入身份，未据此声称USB电气合格。

串阻两侧USB_DP/DM与PA12_SHARED/PA11_SHARED、D+上拉支节、ESD和Type-C双面接点分叉应作为完整路径审查。单个差分pair的几何匹配不能代表串联器件两侧全路径已经匹配；CAN互斥装配的未装焊盘仍可能形成物理支节。

## 3. 约束依据和生产释放的区别

当前AN4879 Rev12不再包含早期独立PCB layout/阻抗计算指导（修订历史记载在Rev3移除），不得把网上旧版长度数字冒称现行F103强制门槛。第29课的phase、uncoupled length、via数量等教学预算要逐条标来源类别。

第28课已建立公开制造层叠目标，但90Ω对应的最终线宽/间距仍需按所选实际叠层和板厂阻抗流程核定；第29课暂定几何只证明软件规则创建和DRC生效，不能写成90Ω已实现。L2/L3连续GND是层功能意图，尚未生成的平面不能当已验证的回流铜。

独立审核还核出两层OSH教学目标的继承USB阻焊桥为0.100mm，而该厂公开最小为0.1016mm，相差0.0016mm；两层整板不能据层叠CAD通过就称已满足该厂释放要求。原生逐层tolPlus/tolMinus=0表示未输入制造公差，不表示实际无公差。详见[第28课独立审查](lesson28_independent_review_20261019.md)。

这些纠正保留“学习方法已验证”和“具体硬件/制造条件仍需定版”的界线。历史清单是各自记录时刻的SHA快照；本次更正后的笔记身份由F阶段新清单记录，原始CAD几何身份保留。

## 用户层叠与Artwork规范勘误（2026-10-19）

后续发现原建板自行增加物理MASK、只加载铜Film并加自定义板框Film，不符合用户规范。已撤销这些做法并补验完整15/17Film及板框映射；当前文件与证据见[纠错记录](lessonF_stack_artwork_correction_20261019.md)。阻焊制造资料与开窗仍保留，先前材料讨论不能解释为允许在用户板物理层表新增MASK。
