2026-11-02 原理图排版方法沉淀与九个01目录同步

用户要求：总结位号/Value同行略偏上、文字互不覆盖、网络简洁无冗余绕线的方式，形成可复用方案；更新本地AI学习库，并将全部01目录同步至已有对应GitHub库。

通用方案：learning/notes/capture_compact_schematic_layout_method.md
复用技能：learning/skills/cadence-schematic-layout/SKILL.md
入口更新：EDA.md、课程索引.md、cadence17-learning技能、既有阻容/网络标签笔记、library_maintenance/INDEX.txt。

方案包含真实本地符号优先、位号左/Value右、实际字体避让、端口显示与电气热点分离、局部短连线、原图分页、原生保存重开、逐RefDes.Pin网表比较及分项证据。A3作为任务参数，不强制所有未来工程使用。

GitHub对应位置：875638477/001Diy 的 main 分支 005lib 子目录。
本次范围：01aeLib、01AIEDA、01brdlib、01captureLib、01env、01Pad_lib、01Psm_lib、01script_file、01_3d_step_lib。
使用 learning/scripts/github_exact_subtree_sync.py 冻结完整文件清单、逐字节哈希、审查差异、正常提交推送，并用服务器树逐文件核验。无force覆盖，不改范围外的仓库内容。

本文件在源快照冻结前写入，不自称推送完成。实际执行计划、完整清单、最终提交与服务器核验结果保存工程工作区：D:\001DIY\004computer\lga1700\library_sync_20261102。
最终提交回执放同步源之外，避免把最终提交号写回被同步目录导致新的未同步更改。当前状态以工程工作区实际回执为准。

本次仅归纳方法并同步库，不重新修改或重新宣称验证已有Cadence工程。课程学习完成状态保持原记录。
