from pathlib import Path
P=Path(r'D:\001DIY\005lib\01AIEDA\learning\notes\lessonHI_38_50_20261021.md')
s=P.read_text(encoding='utf8')
insert='''
### 电源批次02d与03c：已保存重开

两板02d完成输入保护到输入电容、buck输出/反馈、LDO及相应地连接，24个端点证明通过，未连接163→142。反馈取样从输出电容低阻节点分支，FB高阻节点保持TOP短路径；为避免TOP与VIN交叉，5V取样前低阻支路采用BOTTOM短跨接。两层额外TOP GND桥连接跨接两侧实际地，最终仍查真实铺铜；四层增加真实L3 GND，不能只把L3层功能写成地。独立读回1792项核对通过，输入电容至U2地之间真实参考铜的0.6mm返回带完整；实际多边形弧线采用原生方向/圆心规则展开，面积与原生结果差<0.01mm²，不用AABB把L形void误算成整片缺铜。

03c把主3V3从C9独立主干送入MCU内部星形分配，原有外侧去耦连接保留。VDD各脚的内向0.25mm细颈1.25mm，VBAT内向细颈1.453553mm；后续外设主电流不得经这些颈。低电流模拟滤波前支路绕开ADC路径，保持ADC TOP短线及BOTTOM参考。03c两板10个端点证明通过、原生DRC=0，未连接142→137。只有两个新局部maxneck从1.3改1.4以容纳既有外侧1.3657mm细颈；VBAT局部1.5保留，全局1.0未放宽。原生临时收紧1.3确实报出两条1.3657错误，恢复1.4回0，源SHA不变。

有效检查点：inventory/checkpoints/power_2L_b003c和power_4L_b003c；原生native/HI_2L_power_2L_b003c.brd SHA256 A86488E37C98A7135BECF48DC7130D2461F0DCA12E5E6A53CD52EBA77CBE6082；四层HI_4L_power_4L_b003c.brd SHA256 F673C67C06BF169626A5D08E05FE4D541CAC9241020152C1A76AAA65B10A5392。它们仍是部分连接板，不是45/50整板验收结果。

'''
s=s.replace('## 41—50：后续验收点（进行中）',insert+'## 41—50：后续验收点（进行中）')
s=s.replace('## 最终保存重开与验收（待完成）','''5. 电源02b的TOP VIN支路经过旧地via产生实际短路；02c虽避短，却与BOTTOM取样支路平行形成不必要的两层地槽，最终02d改VIN TOP通道并加实际地跨接。保留各候选及拒绝原因。
6. 原03b模拟前级电源线与ADC输入相交，改低电流滤波前支路绕行，不靠把ADC换到底层压在分割参考上解决。
7. 原生MCU05查出R23与原3V3铜间距0.2959<0.3、ADC出局部区域后与U1.12间距0.25<0.3。MCU06仅移R23 y+0.02及局部改变ADC外段，保留全局0.3；等待新批实际验收。两板失败候选、32端点证明及单anchor删点隔离负测试结果完整保留，不能因端点证明通过就接受DRC失败板。
8. USB+ESD独立分组遗漏了VBUS via与DM合并横段的相交，完整组合复核后改via坐标，旧ESD04b不执行。root预检工具也补齐commonOperations与variantOperations变体展开，避免漏检两层/四层特有铜。
9. Cadence禁止布线字段nil读为JSON null，必须按FALSE处理；不能因它不等于Python False对象就允许该层。几何搜索器已修正，原生规则未放松。

## 最终保存重开与验收（待完成）''')
P.write_text(s,encoding='utf8');print('Main HI progress and failure notes updated')