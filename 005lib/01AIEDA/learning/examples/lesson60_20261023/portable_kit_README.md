# EDA第60课最小复现包

用于在目标机验证一个小操作：复制自有四层训练板，只加L60_REPLAY标识、保存、用第二原生进程重开。它不提供已完成产品板，也不是完整01AIEDA备份。

## 依赖与配置

Windows、可用Python（本轮3.14）和目标机合法Cadence17.2安装/产品许可由目标机准备。压缩包不含软件、许可凭据、整本教材或视频。请用Python完整exe路径，WindowsApps入口可能只是占位。

解包到较短ASCII路径，建议在目标机01AIEDA内。复制replay/config.example.json为config.local.json，填写本机Cadence安装根。原生包当前只验证ASCII路径（可含空格）；中文路径未测并早拒绝。命令长度500是本包经验性保守限制，非官方Cadence上限。

用Python -I运行replay/replay.py，依次probe、plan --tag m01、run --tag m01、verify --tag m01。每次新tag，不覆盖旧run。详细命令、错误与期望42项在[原生README](replay/README.md)。

## 结果判定与记录

目标机需得到本机新build/fresh原始日志、新BRD及verification。核80件/272逻辑pin/69net、TOP-L2-L3-BOTTOM、mm、实际932段=750manual+182thermal、唯一标识(4,4)mm，源fixture身份及三阶段几何保持。文件PASS字样本身不足。

随附skill为本地操作说明，不保证新会话自动发现。可明确要求读取[SKILL.md](skill/cadence17-learning/SKILL.md)。preflight需要完整学习根的EDA/课程索引/原始fixture；仅有这个小包不能替代完整学习根，它也不验证Cadence许可或GUI。完整迁移仍须复制整个01AIEDA及核外部源/公共库。

records中是教程/视频/来源重绑定模板，未填时间点不是已观看。config中的环境schema供清点，原生程序只读replay的config.local.json。目标机成功后另记实际版本、命令、源/输出SHA、日志和fresh证据，不修改原机历史记录。

本机曾在两个目录完成验证，不能替目标机预填成功。GUI、第二物理电脑、OCR和视频播放均未由此小包证实。fixture和内容SHA见kit_manifest.json；原生源码另由replay/package_manifest.json保护。
