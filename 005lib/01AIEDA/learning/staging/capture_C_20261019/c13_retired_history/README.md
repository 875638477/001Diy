# C13 已停用实验快照

此目录只作历史证据，文件以`.tcl.txt`保存，不作为执行入口。

`c13_run06_NULL_cast_retired.tcl.txt`有未判空即cast的旧探针；`c13_helpers_before_retiring_unsafe_reader.tcl.txt`包含本机17.2曾发生native crash的FlatNet.NewWiresIter路径。不得重新提交它们。

正式入口与安全读回路径见`learning/notes/lesson13_completion_20261019.md`；最终验收只针对c13_scope_v8.dsn。
