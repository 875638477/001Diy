

--- BEGIN 20261025_GITHUB_UPLOAD_SNAPSHOT ---
GitHub 005lib 上传快照记录（2026-10-25）

源根目录：D:\001DIY\005lib
目标仓库：https://github.com/875638477/005lib
仓库根目录对应上述本机源根目录；9 个 01 开头目录直接放在仓库根目录，内部路径保持原样：
01aeLib、01AIEDA、01brdlib、01captureLib、01env、01Pad_lib、01Psm_lib、01script_file、01_3d_step_lib。
包含隐藏文件、原有忽略文件、工具文件和 __pycache__ 文件；不自行清理源文件。
按用户最新指令，以今天本机这 9 个 01 目录为 GitHub 内容基准；删除远端不在该范围内的旧文件，保持目录层级一致。本次经核验原远端仅有根 README.md，因此删除该旧文件，最终仓库根仅保留这 9 个目录。快照脚本只复制和验证，不执行 Git add、commit 或 push。

Git 兼容归档特例：13 个历史测试样本 .git 目录不直接进入 Git 工作树。
它们的原相对路径、所有文件内容和包括空目录在内的目录项无损保存在本目录 git_test_fixtures.zip。
git_test_fixtures_manifest.csv 记录逐项映射，git_test_fixtures_verification.json 记录 CRC32/SHA256 读回核验。
这些源测试目录保持原样。解压到本机源根目录可恢复原路径；请勿将其直接添加至版本库。

upload_manifest.csv 逐项记录源绝对路径、仓库相对路径、字节数、SHA256 和原始 Git blob SHA1。
每项均对源文件与工作树副本进行 SHA256 比对；复制使用 copy2 保留通常文件时间和属性。
Git blob SHA1 是文件原始字节的哈希；后续 Git 应关闭换行转换并核对索引 blob。
源目录中已有的 .gitignore 不构成快照排除规则；后续应将清单中所有文件纳入提交。
普通空目录会在工作树复制阶段保留，并在 empty_directories.json 中记录；Git 本身不记录普通空目录。

覆盖边界：upload_manifest.csv 和 snapshot_verification.json 为枚举结束后生成的两份自引用输出，
不列入 upload_manifest.csv 自身；生成后另行复制到源记录目录及仓库记录目录并逐份核验 SHA256。
13 个 .git 测试目录的原文件不逐项复制到工作树，而在上述 ZIP 及 ZIP 成员清单中验证保存。
其他全部源文件均应列入上传清单。快照后的修改、后续 Git 压缩包及认证数据不在快照范围内。
本次不将便携 Git/gh/LFS 可执行文件写入源库，仅保留官方下载校验证据。

upload_inventory.json/csv 是准备开始时的原始盘点，可能包含后来按用户指示删除的重复备份 ZIP，
当前快照以 upload_manifest.csv 和 snapshot_verification.json 为准。
备份 ZIP 核验及删除记录见 README_backup_removal.txt、backup_zip_removal.json。
敏感内容扫描报告及复核记录保留在本目录；执行前必须完成上层人工复核。
--- END 20261025_GITHUB_UPLOAD_SNAPSHOT ---
