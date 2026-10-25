# 保存快照的255字符PST导出与受控发布

这两个PowerShell工具没有工程名或安装位置默认值。源DSN、CFG、运行输出和发布目录来自调用者；项目参数与结果放工程根。

```powershell
& $Exporter -SourceDsn $SavedDsn -ConfigFile $Cfg -OutputRoot $ExportRuns -CadenceRoot $CadenceInstallation
& $Publisher -SourceDsn $SavedDsn -ConfigFile $Cfg -OutputRoot $ExportRuns -PublishDirectory $ActiveNetlist -ExporterFile $Exporter -CadenceRoot $CadenceInstallation
```

`export_pst255.ps1`创建新运行目录，复制并校验已保存DSN，然后调用该安装根的`tools/bin/pstswp.exe`，固定`-l 255`及PCB Footprint属性。要求正常退出、日志存在、三个非空PST、无ERROR／器件名截断，且源DSN前后SHA一致。报告也记录实际writer路径及SHA。报告不包含未保存Capture编辑，也不代表连接／器件／PCB／DRC／制造验收。

`publish_pst255.ps1`锁定OutputRoot，使用本次导出返回的报告；验证成功后保留旧目录并切换活动PST。失败不修改成功发布指针。发布目录必须与运行输出分离，不能包含源件、CFG或工具；旧目录移动失败会尝试恢复。只在当前授权的项目中操作，不用于整盘清理。

`-PstswpExecutable`是显式后端路径覆盖，供特定安装或合成测试使用；调用者须确认真实执行文件身份。配套`selftest.ps1`使用`.ps1`模拟writer和纯文本假DSN，不加载任何Cadence程序；它验证文件安全和发布控制，不证明原生Cadence导出能力。实际使用应完成一次隔离真实DSN导出及独立PST连接／器件比较。

```powershell
& $SelfTest -OutputDirectory $FreshSyntheticFixtureDirectory
```

不要为运行工具永久修改全局执行策略；按当前环境允许的脚本启动方式运行。模拟测试曾只为测试子进程指定运行策略，不修改用户的持久策略。

完整方法与边界见[工具保留与无损证据归档](../../notes/eda_tool_retention_and_evidence_archives.md)和[Capture到Allegro网表排错](../../notes/capture_allegro_netlist_troubleshooting.md)。
