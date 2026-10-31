公共库维护：M.2 Key M 金手指修正
日期：2026-10-31；Cadence 17.2 S045。
用户授权：核对 CON1 金手指与 J26 插座，对原理图库和 PCB 封装可直接修改。

范围
- 01captureLib/019Connector.OLB：M_2 KEY M 删除未连接占位 PAD1/PAD2/H1/H2/H3（76～80），保留 67 个接点。
- 同库 M_2-05NGFF-KEY-M 的 PCB Footprint 同步 md2_NGFF_M_SMT。
- 01Psm_lib/md2_key_m_Finger.dra/.psm：铜、脚号、位置与参考图形不变；奇数 Top 阻焊，偶数 Bottom 阻焊，两面均无锡膏。
- 01Pad_lib 新增 md2_finger_top035x150.pad、md2_finger_bottom035x200.pad；未覆盖旧通用焊盘。
- 金手指铜宽 0.35 mm，Top 长 1.50、Bottom 长 2.00 mm；保留 Bottom 原 0.25 mm 局部偏心。
- Native PAD 的 NON_PLATED 为无钻孔焊盘的钻孔电镀属性，不代表金手指表面无需镀金；表面工艺由制造文件规定。

验证
重新打开 OLB 后两种符号均为 67 脚；原生 DRA 4020 项检查通过。
编译 PSM 后正面 0 度、90 度及背面镜像，两种封装合计 6 实例独立重开，通过逐脚、层和开窗检查。
两者脚号一对一，59～66 缺口，同面节距 0.5 mm，双面错位 0.25 mm。
金手指 Top 面朝插座奇数脚 / +Y 一侧；卡 Y 轴对应座 X 轴，M Key 名义中心 +6.125 mm。
旧金手指最大横向量化误差 0.0003 mm 保留。原厂配插板厚名义 0.8 mm。
未进行实物插接或 GUI 显示确认。板边/缺口为 DXF/丝印参考，制造外形仍需在实际布局中落实。

工程实际运行记录单独保存在：
D:/001DIY/000driver/18Brushless/_cad_audit/20261031_m2_pair/检查与修正记录.txt
工程 DSN/BRD/PST、实际电路、完整运行日志及工程备份不存入本学习库。

恢复
关闭 Capture/Allegro 后，将 before/ 的原件复制回上述公共库路径。
新增两个 PAD 可保留以免破坏新引用。library_publish_manifest.json 记录前后 SHA-256；
archive_manifest.json 校验本归档，after/ 保存已发布库实体及 XML 焊盘源。
scripts/ 为本次库操作与读回定义；evidence/ 为实际执行证据及六实例测试板，不直接重放旧 SCR 内历史路径。

外部核对：Kyocera 官方 M.2 键位表将 M Key 位置列为 59～66：
https://ele.kyocera.com/en/technical/358426/
源厂家图纸保存在 evidence/HYCW19M-05NGFF-530B.pdf。
