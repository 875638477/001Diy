from pathlib import Path
import json,hashlib
R=Path(r'D:\001DIY\005lib\01AIEDA');H=R/'learning/examples/lessonHI_38_50_20261021';P=H/'engineering_mcu/plans';N=R/'learning/notes/lessonHI_mcu_20261021.md'
text='''

## 17. 2026-10-22 后半程：手动门户、布局比较与尚未通过的条件

本节是工程探索记录，不是完成验收。当前真实板仍是 `padentry_*_b019_DRC_PENDING`：两板各有 7 个 South GPIO 待接，65 个非 USB 网络逐网 scoped DRC 为 0；完整 USB/整板检查未通过验收。2L SHA256=`AA3BFC0E01B06CB1058462439C71E56BC316F1F2929859B6A224320BE1013420`，4L=`B7A32330992F49609339E33C00BE92D989D0EA0C4AF64ED2763D0678DE14B501`。下面所有 80—92 派生几何均没有写入这些原生板；派生 snapshot 中继承的字段名不能作为原生执行证据。

### 17.1 改用人工短门户，并纠正坐标和人工墙

原位/南置比较中，[独立与联合状态](../examples/lessonHI_38_50_20261021/engineering_mcu/plans/GPIO7_comparison_state_20261022.json) 保留了每次路线、失败与条件。独立七网各自能找到路径，并不表示组合后能共存；12 轮拥塞搜索仍有交叉，不能通过增加搜索次数把它称为 PCB 已设计完成。之后停止广域 negotiated 搜索，改成源、短换层窗口、主走廊、目的端分别手动核。

必须从实际过孔读坐标：PA9_UART_TX 是 `(39.7,21.7)`，USB_ATTACH_N 是 `(39,21.2)`，PB14 是 `(38,21.25)`；此前口头分析误用 UART_TX `(39.55,20.7)` 的设想已废弃。4L PB13/PB15 源孔分别为 y20.725/y20.675；2L 则为 y20.75/y20.7。不能用虚拟尾线端点替代真实源孔，不能由封装中心推测焊盘位置。

[PB1 80 候选](../examples/lessonHI_38_50_20261021/engineering_mcu/plans/GPIO_PB1_inward_4L_80_delta.json) 保留原电源/ADC/HSE，只研究 TOP 源弧与普通返回孔的小修改。它仍改变了通用 V3 入口：PTH `(37,24)` 移到 `(37.2,24.3)`，TOP 新 .6 mm stub 长 .38284 mm；BOTTOM 末段从 1.7 mm 改成 1.48284 mm。不得把它写成供电/去耦路径完全没有变化。原直接去耦铜虽保留，完整供电图、入口电感、过孔 alias 和实际回流仍须原生核验。2L 普通 GND 37.4,27.4 的迁移也必须逐一解释其原 PB10 返回角色及替代共地路径，不能只凭同 GND 网络删除。

80 的 BOTTOM L 又会把 PB10/其它源封在里面，不能把新候选冻结成物理墙。最小左绕替代为 `(41.9,26.79)→(40.8,25.69)→(40.8,23.55)→(36.7,23.55)`；TOP 和原 PB1 孔不变。它仍只是候选，PB14 的北向门若需要穿过该横段，还必须联合调整。普通源需一组设计，不能完成一脚便把其余脚的通道封死。

North51 的 PA3 不是整路 x+y=67.25：它先有横段，再长 NW 时实际 x+y=65.9。仅按一个源段的斜线常数设计 PB1/PB10 会撞真实长尾。原 R25 新 V3 支路 BOTTOM x31,y32.3..33.7 也是实际障碍，不能只因与主 STAR 平行就声称 NW 门户已全通。

### 17.2 单移 ATTACH .14 mm 的真实局部门户

[87 两层检查](../examples/lessonHI_38_50_20261021/engineering_mcu/plans/PB15_attach_2L_87_check.json) 与 [四层检查](../examples/lessonHI_38_50_20261021/engineering_mcu/plans/PB15_attach_4L_87_check.json) 在加入全部新铜后同时检查，避免先查 via 再加相邻新线的顺序盲点。

- USB_ATTACH_N 源孔从 `(39,21.2)` 移到 `(39.14,21.2)`；TOP .16 源为 `(39.25,22.75)→(39.25,22.1)→(39.14,21.99)→(39.14,21.2)`；BOTTOM .2 接 `(39.14,20.44)→(39.7,19.88)→(39.7,18.6)`，接回原远端。
- PB14/PB15 原孔及 MID/EAST 普通地孔均保留。PB15 正常 .2 BOTTOM 能沿 x38.57 穿过原 PB14 与新 ATTACH 孔之间，正常名义铜距约 .21/.212 mm，再北绕东达 `(47.1,23.3)`。4L 全部新外层铜几何检查通过；这不等于完整 PB15 长路，更不等于原生 DRC。
- 2L 没有真实异网铜碰撞，但新 PB15 穿过 TOP USB pad 对面参考保护区；ATTACH 的新腿也与原 USB DM/DNP 附近参考范围相交。这些是实际参考与局部回流待审，不能通过删除保护区域就称通过。
- 更大的 ATTACH 迁移到 `(39,18.6)` 曾直接落入 R6 的 PA11_SHARED 真 SMD 焊盘，已否决；迁至 `(39.38,21.07)` 的方案又遇 UART_TX/RX 源与返回，均未执行。小移动避免了这些实际对象，不能把大移动的一部分名义间距作为完整通过。

USB pad 的实际北端为 y23.35。BOTTOM 线 y23.8、宽 .2、按 .3002 地间距产生的参考 void 下缘为23.3998，只有约 .0498 mm 名义余量；需 native actual fill 验证。其自身又可能长期在 TOP V3 条/地避让投影下，必须单列电源耦合/同层共地返回，不能说通过 USB 投影就有完整 GPIO 参考。

### 17.3 四层 PB15 完整短内层桥比较，不擅改变层功能

[89 完整路径比较](../examples/lessonHI_38_50_20261021/engineering_mcu/plans/PB15_4L_short_L2_comparison_89.json) 只作为 root 选择的工程备选：接87源门后，BOTTOM 到新孔 `(48.9,23.68)`，L2 .2 沿 `(49.1,23.88)→(49.1,28.9)→(51.6,31.4)`，再 BOTTOM 北行；在 NRST 的 BOTTOM y41.55 附近用 TOP 1.7 mm 短桥，最后 BOTTOM 至 J13.3。

完整 U1.28→J13.3 中心线为50.61514 mm；其中 L2 8.83838 mm，新增4个 signal PTH、3个 stock GND return PTH。源换层至原应用地孔 `(48.2,25)` 为1.4948 mm，其余返回为 .9/.8/1.1 mm。全部新外层铜/保守穿层 pad 检查12项无异网违规；最后一个地孔最初距新斜线只有 .1657<.3，已改到 `(53.4,42.4)`，不能漏查本批新增铜彼此的关系。

此方案没有 native 执行、没有内层许可批准，也未认证 SI。采用时必须显式设有限 L2 allowEtch 及 .2 线宽/原间距，小孔许可覆盖四实际铜层；全局其它信号的内层禁布仍保持。L3 必须是真实连续的应用地参考，L2 新 slot 对 TOP 普通信号和去耦投影的影响需逐点审查；不能把原两块 GND plane 的设计意图当成已实现原样不变。2L 完全不能套用这个内层桥。

### 17.4 PB10 门户和排针布局的真实代价

原生组提供的 [PB10 v46 门户](../examples/lessonHI_38_50_20261021/review/b020_engineering/PB10_NW_North4_repack_v46.json) 使用实际 b019，普通 North4 长尾重新压紧，并将 PC13 接收孔移到 `(29.25,40.05)`。PB10 保留源孔 `(38,26.3)`，到 BOTTOM `(38,27.72)→(30,35.72)`，经 stock 孔转 TOP 至 `(28,36.1)`。这只是源到门户，不是 U1→J12 完整验收；旧 TOP/参考缺口分别按两层/四层记录，不能把两板几何互相替代。

[92 两层南置完整比较](../examples/lessonHI_38_50_20261021/engineering_mcu/plans/PB10_south_2L_92_candidate.json) 接上该门户，保81已成四网和87源修改，在不穿 buck 热区的条件下，经左侧至南置 J12.4，完整 U1.21→J12.4 几何长77.55685 mm；本批远续60.21995 mm、2个新 signal PTH/2个 GND return，7项新外层铜检查无问题。它只是能比较的偏长候选；目标南置需要避 buck、其它目标 bank 和实际排针电源孔，不因已成四网便声称这种布局是优选。4L 同形会碰真实 SPI BOTTOM 线，91失败资料保留，禁止套用两层通过。

J12南置的 V3 .6 新支路32.19 mm仍是额外代价，原 R27 LIVE 全部铜必须保留。原北排针、南置、必要中北空区的小移应按全部7路长度/过孔/实际返回、供电/GND与插拔空间比较；搜索失败不是用户要求搬排针。所有 GPIO 的源边沿/实际负载、串联终端需求仍待接口定义，不能从直流连通或慢时钟数字推断长线不会反射/辐射。
'''
with N.open('a',encoding='utf8') as f:f.write(text)
files=[P/'PB15_attach_2L_87_delta.json',P/'PB15_attach_4L_87_delta.json',P/'PB15_4L_short_L2_comparison_89.json',P/'PB10_south_2L_92_candidate.json',N]
manifest={'status':'ENGINEERING_COMPARISON_CHECKPOINT_NOT_NATIVE_COMPLETE','files':[{'path':str(q),'sha256':hashlib.sha256(q.read_bytes()).hexdigest()}for q in files]};(P/'manual_portals_record_manifest_20261022.json').write_text(json.dumps(manifest,indent=2),encoding='utf8');print('recorded',len(text),len(files))
