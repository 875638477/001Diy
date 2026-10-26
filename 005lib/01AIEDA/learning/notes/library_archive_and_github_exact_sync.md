# 工程库散件归档与 GitHub 精确同步

这套方法处理已完成公共库迁移后的工程历史库与验证副本。当前设计、原始 AD、必要源库、封存报告和可复用工具分别保护；目录名和封装后缀不能证明库内容相同。

## 工程库清理

1. 固定工程根、正式 DSN/BRD/PST 的 SHA，以及现用公共库清单。递归盘点外置 OLB、PSM、DRA、PAD、其他实际 CAD 符号及数字备份，拒绝跟随 junction/reparse；`.lib` 必须结合目录与内容区分 CAD 库和软件编译库。
2. 对每个文件记录相对路径、字节数、SHA256、mtime；独立复核全量清单。读取 SourceFreeze、当前引用和历史验证依赖。原始输入、当前仍需实际路径的源库、受保护转储和原 ZIP 不随散件清理删除。
3. 按当前导出副本、旧工程私库、验证输入分类，生成精确候选表。将候选的真实字节存入内容去重归档：相同 SHA 只保存一份，恢复表仍逐原路径保存大小、SHA 与时间。历史库即使名字相似，也不能拿当前 `_pc` 库替代。
4. 逐对象核 CRC/SHA，检查恢复表覆盖所有候选；在全新目录实际还原后逐路径核大小与 SHA。只有归档和保护项复核完成，才由当前明确授权的任务按冻结清单再次核 SHA 并逐文件删除，记录可续查的删除账本；不做跨 shell 的递归删除。
5. 清理后重扫候选全部缺席，保护文件和现用公共库全部未变。保留清单、归档、恢复工具、日志、最终报告。不要修改旧 FAIL/PASS 报告来伪装路径还存在。

历史 DSN/BRD 内部缓存必须保留。打开历史设计和按历史库执行 Place/Update 是不同操作；重放旧任务前应按恢复表还原原始库字节到隔离目录，必要时在明确授权下恢复原路径。不要在 `.olb/.psm` 路径写占位文本。

## GitHub 完整子目录镜像

[github_exact_subtree_sync.py](../scripts/github_exact_subtree_sync.py) 显式接受本地根、选定一级目录、工程工作目录、bare 仓库、Git/gh 路径、远端仓库及一级目标子目录。它不会修改源库。没有忽略文件规则；空目录另列，因为 Git 不存储空目录。单文件达到 100MiB、reparse、`.git` 或大小写冲突时停止，不能悄悄漏传。

使用既有认证配置；认证令牌只交给官方 gh credential helper，不写脚本、配置、输出或归档。读取最新远端 `main`，在工程内建立 `--depth=1 --filter=blob:none` 的隔离 bare 仓库，避免为核树下载全部旧库内容。记录和日志全部留工程，不进入库源快照。

```powershell
# 参数均由当前任务给出；四步使用相同参数。
python github_exact_subtree_sync.py snapshot <显式参数>
python github_exact_subtree_sync.py prepare  <显式参数>
# 审查 SYNC_PLAN.json 的 added/changed/deleted 和外部根保持证明。
python github_exact_subtree_sync.py publish  <显式参数>
python github_exact_subtree_sync.py verify   <显式参数>
```

`snapshot` 冻结所有选定目录中的文件字节，计算 SHA256 与 Git blob SHA1。`prepare` 再核源文件，导入远端尚无的新 blob，构建完整目标子树，并以远端当前提交为唯一父提交；其他一级目录的 mode/type/SHA 保持一致。增删只发生在明确目标子树。

`publish` 再核全部本地字节、远端 HEAD 仍是冻结父提交，然后正常推送新子提交；禁止 force。若远端推进或本地变化，保留失败证据，在新工作目录重做差异和提交，不覆盖并发修改。

`verify` 通过 GitHub API 独立读回提交、父提交、根树和完整子树，逐文件核路径、mode、blob SHA1、大小，并再次计算本地 SHA256。GitHub 的递归树有条目数和响应大小限制；遇到 `truncated` 时丢弃部分结果，按实际下一层子树分支读取、缓存并合并，直到每一分支都完整，不以截断结果报通过。限制说明见 [GitHub Git trees API](https://docs.github.com/en/rest/git/trees)。删除项必须确实在远端消失，目标子树之外仍保持原值。最终服务器证明保存在工程工作目录，避免将“包含自身最终提交号的报告”反复写回源库形成无限变更。

本地合成验证覆盖二进制、空文件、Unicode/空格路径、增改删、保留目标外文件和源字节变化拒绝。合成验证不代表真实远端已同步；真实任务必须另有服务器读回报告。
