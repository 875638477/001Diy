# 清理 BAT 双击启动与结果显示修复

日期：2026-10-19。用户反馈：“这个脚本只能powershell里面运行，双击无效一闪而过。”本轮只调整BAT启动层，删除和保留规则继续以 [清理规范](cleanup_user_rules_20261019.md) 为准。

## 查到的原因

只读检查发现，Windows `.bat` 关联为 `batfile`，打开命令为 `"%1" %*`，没有用户级覆盖或Command Processor AutoRun异常。没有发现BAT只能从PowerShell终端启动的关联问题。

核对时Capture、Allegro及两个UV4进程仍在运行。现有清理逻辑会拒绝在这些软件运行时实际删除，并报出 `Close the design/build tools before cleanup`。旧BAT随即 `exit /b`，没有停留步骤，双击时错误随窗口关闭而不可见。命令行终端保留了输出，因此看起来只有终端能运行。

`/preview`允许这些软件运行，所以此前预览成功只能证明预览路径可用，不能证明实际清理已执行。本轮未关闭或终止用户软件，也未修改Windows文件关联。

## 启动层修改

- 用 `%SystemRoot%\System32\WindowsPowerShell\v1.0\powershell.exe` 调用系统PowerShell，减少不同启动环境的PATH影响；用户无需先手动打开PowerShell。
- 命令结束后立即保存退出码。成功显示 `[Cleanup] OK - command completed.`；失败显示 `[Cleanup] FAILED` 和退出码，保留上方原始错误。
- **无参数运行，包括双击，等待按键后关闭窗口。** 从终端无参数调用也会等待按键。
- 带 `/preview`、`/help` 等参数时完成后直接返回，继续支持命令行调用；预览不会删除文件。
- 暂停和提示不覆盖原退出码。系统PowerShell路径不存在时显示原因并返回9009。

检测到设计软件运行时仍停止实际清理。看到失败提示后，应先正常保存并退出提示中的软件，再执行清理。启动层不会绕过这一检查。

维护源：[modernize_cleanup_scripts.py](../scripts/modernize_cleanup_scripts.py)。25份BAT继续自包含、UTF-8无BOM、CRLF。嵌入的 [eda_cleanup_payload.ps1](../scripts/eda_cleanup_payload.ps1) 本轮未修改，清理规则、XML/CSV/DAT全局保留和01AIEDA/env/01env中TXT保护保持原样。

## 验证与备份

验证分为真实BAT启动段的隔离样例和实际入口预览。启动样例只在 `01AIEDA/learning/staging/cleanup_review_20261019/double_click` 内创建，验证正常/失败退出、无参暂停、有参自动返回和特殊路径；不对用户工程双击触发实际删除，也不将CMD启动测试描述成已经操作Explorer界面。

**启动层30项检查全部通过。** [测试脚本](../scripts/test_cleanup_bat_launcher.py)验证无参数成功/失败均显示暂停提示且保留原码，带参数自动返回，缺少PowerShell返回9009，以及中文、空格、`! & ()`路径和父CMD延迟展开场景。另在仅含自建sentinel.log的隔离目录运行完整生产载荷：检测到真实软件进程时，无参显示原错误和FAILED、等待输入后返回1；预览返回0且不等待。两个场景的sentinel内容哈希均未变。

报告见 [launcher_verification.json](../staging/cleanup_review_20261019/double_click/launcher_verification.json)，25个入口的编码、预览、启动段一致性、清理载荷哈希及记录链接见 [final_verification.json](../staging/cleanup_review_20261019/user_rules/final_verification.json)。生产载荷SHA256仍为 `1aa5b501dc89a136ec1f34f46960dea519d5f2939dcadc896d54e85777f07fef`，此前538项清理语义检查继续对应当前载荷；本轮启动层30项单独记录。

修复前25份BAT、生成器及验证资料已备份到 [cleanup_double_click_20261019](../../backups/cleanup_double_click_20261019/)。全部新记录、测试和中转文件仍存01AIEDA。
