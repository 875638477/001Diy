# Allegro 17.2：封装添加 STEP 模型与 3D Canvas 显示

更新：2026-10-31；本机 Allegro 17.2 S045。关键闭环：**核对/添加关联 → STEP Mapping 窗口左下角 Save → 保存封装 → 3D Canvas 检查真实模型 → 重开复核**。

## 本机入口与文件

| 项目 | 本机配置 |
| --- | --- |
| 封装源与编译库 | D:/001DIY/005lib/01Psm_lib，.dra 与 .psm |
| 模型库 | D:/001DIY/005lib/01_3d_step_lib，.step / .stp |
| 数字键 4 | funckey 4 replay D:/001DIY/005lib/01script_file/setup_step_package_mapping.scr |
| 脚本实际命令 | step pkg map，打开 Device/Package STEP Mapping |
| 数字键 3 | funckey 3 3D，打开 3D Canvas |

键位已核对本机 01env/env，不是所有安装的默认快捷键。换电脑核实际 env；没有绑定时使用对应命令/界面入口，不直接覆盖共享环境。

## 完整添加流程

1. 打开目标封装源 .dra，确认文件名和路径，先备份 .dra/.psm。保留 STEP 的厂家来源、型号和尺寸图；自建简化模型标明范围。不要只改检查板实例就以为公共库已更新。
2. STEP 放入模型库，通过 Setup → User Preferences → Paths → Library 核对 steppath。本机指向上表模型库；step_mapping_path / step_facet_path 是映射与 facet 导出位置，不能代替模型搜索路径，本机这两项也指向模型库。
3. 按数字键 **4** 打开 **Device/Package STEP Mapping**。封装编辑器使用 Package 模式，确认映射目标是当前 .dra；选择正确的 Available STEP Models，并使用 **Primary Model** 作为主体模型。
4. 核对右侧“封装名 => STEP 文件名”和实际预览。找不到文件时检查 steppath、筛选与真实文件，不用近似型号替代。不要只凭映射行存在判定模型已经正常。
5. 调整 Rotation XYZ（度）和 Offset XYZ（毫米）。用 Display origin of STEP model、观察方向及透明显示核对安装面、1 脚、定位柱、外壳高度、端子与焊盘和插接方向。全零仅适用于模型原点本来就正确的情况。
6. **在 STEP Mapping 窗口左下角点 Save。即使映射和六个数值没变，也要完成一次界面保存。** 本机用户正是这一步之后，3D Canvas 才显示正常。Close 或只保存 .dra 不能代替这个 Save。
7. 关闭映射窗口，保存封装源并确认同名 .psm 已重新生成，核对文件名、输出路径和时间。源 .dra 和供 PCB 调用的 .psm 都要保留。
8. 按数字键 **3** 打开 3D Canvas。确认看到插槽、定位柱等真实模型特征，而非仅 PLACE_BOUND 拉出的方块；旋转看顶部、底部和侧面，检查方向、偏移及穿板。
9. 关闭后重新打开封装，再看 Mapping 和 3D，确认保存后仍有效。已有 PCB 缓存旧封装时，更新该符号/映射并保存板，再重开检查；必要时在隔离副本重新放置验证 .psm。
10. 记录模型来源、映射文件名、六个变换值、Save 与重开显示结果和前后 SHA。公共封装还需比较二维铜、孔、脚号及阻焊/锡膏，避免加模型时误动封装。

## 已有关联但 3D 只有方块

本机先做最短恢复步骤：

**关闭 3D Canvas → 数字键 4 → 确认映射与右侧模型 → 左下角 Save → 关闭并保存封装 → 数字键 3 → 检查真实模型。**

仍无效时依次核查：

- 模型文件存在、可读且非空，steppath 正确，映射目标/文件名正确。
- **3D Canvas 窗口内**的 Setup → Preferences → Symbol Representation 是否允许 STEP，选择 Only STEP 或优先 STEP 的表示方式；不是主 PCB 窗口的 User Preferences。
- 单位、六个变换值及视图是否导致模型离开视野，模型本身是否为空或只是方块。
- PCB 是否仍使用旧 .psm / 旧映射，是否更新并保存了当前板。
- 必要时在隔离副本检查模型几何；不先删私有附件、改注册表或重置环境。

Symbol Representation 是备选排查项，**不是本次已证明的故障原因**。

## 2026-10-31 用户确认的 md2_NGFF_M_SMT

用户说明并附图：数字键 4 打开添加 3D 的界面后点了一次 Save，随后数字键 3 打开 3D 显示，模型正常。截图中 Primary Model 为 md2_NGFF_M_SMT => md2_NGFF_M_SMT.step，Rotation 与 Offset 的 XYZ 都为 0。

此模型按封装原点建立，所以本例全零；不能机械套用到其它模型。模型和二维验证见[此前公共库维护记录](../../library_maintenance/20261031_md2_ngff_m_smt_3d/README.md)。

证据边界：

- 本机 GUI 成功来自用户现场操作说明和截图，本次没有冒称由助手重新操作 GUI。
- 之前 axlStepSet 写入关联、DRA 保存、PSM 编译和实际 STEP 导出通过，只证明相应层面，不能代替 3D Canvas 实显检查。
- 官方帮助说明 facet 数据参与 3D Canvas 显示。没有 Save 前后数据库差分，不能断言本次 Save 具体写了哪个私有附件，也不能把问题归因于 STEP 多根实体。
- 不需要发布此前试验的“单一装配根”候选来解决此问题；用户用现有模型界面保存后已恢复显示。
- 真实模型可见不等于实物插接、整机干涉和制造公差已验证。

## 迁移和交付

至少带走 .dra、重新编译的 .psm、实际映射的 STEP 和 .pad 依赖；换机器核实际 steppath / psmpath / padpath。用 Mapping 导出/导入时同时保存 .map 和配套 facet 文件包，按目标版本界面导入后再 Save、重开 3D 检查，不能只复制 .map。

## 核对来源

- 用户 2026-10-31 的实际操作和 Device/Package STEP Mapping 截图，箭头指向左下角 Save。
- 本机 01env/env 的数字键 3/4 绑定，以及 01script_file/setup_step_package_mapping.scr 的 step pkg map 命令。
- 本机 Cadence 17.2 官方帮助 doc/algrolibdev/chap11.html：模型路径、映射、导入导出与 facet；doc/algro3Dcanvas/working_with_3D_canvas.html：Symbol Representation。
