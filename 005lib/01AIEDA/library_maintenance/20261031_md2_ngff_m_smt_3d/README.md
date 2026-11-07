# md2_NGFF_M_SMT：添加立贴 M.2 M Key 的 STEP 模型

> **2026-10-31 用户现场补充：** 3D Canvas 只有边界方块的问题，已由用户按“数字键 4 → STEP Mapping 界面左下角 Save → 数字键 3”恢复正常。原生验证历史保留；新增 GUI 成功依据为用户说明和截图。完整操作见[添加与显示流程](../../learning/notes/allegro_step_model_mapping_and_3d_canvas.md)。

日期：2026-10-31。软件：Cadence Allegro 17.2 S045。

## 最终文件

- 修改的源封装：`D:\001DIY\005lib\01Psm_lib\md2_NGFF_M_SMT.dra`
- 重新编译的封装：`D:\001DIY\005lib\01Psm_lib\md2_NGFF_M_SMT.psm`
- 新增模型：`D:\001DIY\005lib\01_3d_step_lib\md2_NGFF_M_SMT.step`

STEP 关联名称为 `md2_NGFF_M_SMT.step`，PRIMARY，XYZ 偏移和旋转全部为零。模型自身已与封装坐标对齐。已只读确认当前 Cadence 用户环境及 `01env/env` 的 `steppath` 指向用户提供的 3D 库目录；此次没有修改这些配置。

若 PCB 中已经放置旧版本封装，需要在当前工程执行 Update Symbols / Refresh Symbols 并更新 STEP 映射，或重新放置，才能使用新增关联。此任务只修改用户指定的公共库，没有改动任何现有 PCB 工程。

## 模型来源与准确范围

库中已有的 `md2_a_h2d7.stp`、`MD2_B_H4D2.stp` 与这款 5.30 mm 高的立贴 M Key 不匹配，未用它们替代。现有立创下载包没有对应 3D 模型。

本次模型由原厂 HOAUC 图纸 HYC-1804101726 第 1、2 页建立，是**简化工程外形模型，不是原厂提供的精细 STEP**。原厂 PDF 随本记录归档。模型用 OpenCascade 7.9.3 实体布尔运算生成，输出带颜色、单位为毫米的 AP214 STEP，并重新导入检查。

| 几何 | 模型名义值 |
| --- | --- |
| 本体 | 21.85 × 5.70 × 5.30 mm |
| 安装面 | Z=0，与 PCB 顶面对应 |
| 定位柱 | X=-10/+10 mm，直径 0.95/1.45 mm，向下伸出 0.70 mm |
| 引脚外缘跨度 | Y=-3.23～+3.23 mm，共 6.46 mm |
| 插槽 | 宽 0.90 mm，槽底 Z=2.60 mm |
| M Key 挡块 | 中心 X=6.125 mm，宽 1.10 mm |
| 接点 | 67 个；保留 1～75 物理编号，缺 59～66 |

未标注的弹簧曲率、端子内部结构、塑料倒扣、圆角和模塑细节进行了简化。模型不包含插入的 M.2 模块、模块支撑或公差极限。封装原有 `PACKAGE_HEIGHT_MAX=5.55 MM` 保留；STEP 表示 5.30 mm 名义高度。

## 验证

- 修改前备份用户改名后的 DRA 和 PSM，记录 SHA-256；原文件与前轮原厂推荐封装一致。
- 通过官方 `axlStepSet` 添加关联，保存 DRA，重新编译 PSM，独立进程只读重开。
- 修改前后的原生 `pins.tsv`、`geometry.tsv`、`summary.txt`、`symbols.tsv` 逐字节一致。原 67 个电气焊盘、2 个 NPTH、阻焊、锡膏、丝印、装配线、原点文字、边界及高度均保留；封装 DRC 为 0 且状态有效。
- 在隔离检查板加载三个实际 PSM：顶层 0°、顶层 90°、底层镜像。三个实例均保留模型关联。
- 从 Allegro 官方批处理接口实际导出带模型的 STEP。重新导入该导出文件，得到 405 个有效实体，即三个实例各 135 个实体；检查三套本体坐标、Z 范围、旋转和镜像方向。67 个焊尾逐一位于原铜焊盘内。
- 独立验证 93 项通过。预览基于 CAD 几何三角化和深度遮挡绘制，不冒充 Allegro 窗口截图。

软件验证不代表实物插合、完整外壳干涉或模塑细节验证。

## 过程记录与恢复

`backups/` 保存原 DRA/PSM；`library/`、`models/` 是最终候选；`logs/` 保存原生运行和进程身份；`verification/validation.json` 为最终核验；`model_preview.png` 为模型预览；`manifest.json` 记录最终文件及 SHA-256。

独立 `step_out.exe` 初次调用因其资源路径初始化失败，改用官方 `axlRunBatchDBProgram`。首次导出返回成功但日志显示找不到模型，仅导出封装定义，因此未作为验收依据。最终使用隔离运行目录中的同名 STEP，导出不再有“找不到映射模型”警告，并独立读回 405 个实际实体。隔离检查板缺 `DESIGN_OUTLINE` 的提示已单列记录，与连接器实体加载无关；没有改动用户板框。

一次启动因脚本尚未写成而等待，随后按记录核对 PID、启动时间和可执行路径，只终止了该任务自建实例并重试；清理记录保留。没有批量停止进程，也没有修改系统网络或代理。

若恢复旧版本，先核对当前文件与本次 manifest 的新 SHA，再用 `backups/` 中的两份原件恢复 DRA/PSM。STEP 是新增文件；只有确认不再被其他封装引用时才移除。本次没有执行自动删除、Git 提交或远程同步。

归档不包含约百 MB 的临时建模依赖。复现建模可在独立工作目录用 `python -m pip install --target deps --no-deps cadquery-ocp-novtk==7.9.3.1.1` 准备局部依赖，再运行 `build_model.py`。不要原地重跑历史原生操作日志；原生复现需使用新目录。
