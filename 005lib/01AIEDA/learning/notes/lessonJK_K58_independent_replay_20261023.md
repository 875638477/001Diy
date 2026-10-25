# 第58课：本轮DE ECO原生重放的独立验证

日期：2026-10-23；课目录按2026-10-22启动批次保存。所有文件仍在01AIEDA。独立复核人只读取本轮实际原生结果，未运行Cadence；f29是唯一native执行者。原已封存J51—54记录不修改。

## 结果与范围

本轮官方netrev实际执行并保存、随后独立进程readonly重开baseline/ECO。独立程序完成1,453项检查，0失败：80器件、272逻辑引脚、69有名网络、6显式NC、placed=0；恰R19/R20由2.2k改3.3k、J13.7由GPIO_PB8改GPIO_PB9、J13.8反向交换，其余value/pin-net/package/引脚数/未布局状态均保持。

输出板：`learning/examples/lessonJK_51_59_20261022/eco/DE_REPLAY_ONLY/DE_ECO_REPLAY.brd`。

SHA256：`C1F5DF07547330977BFCE2C7296219F07691EE3793122F7BF99E475DBAB4F984`。

独立报告：[review.json](../examples/lessonJK_51_59_20261022/review/independent_K58/review.json)。报告逐条保存本轮检查、实际delta和每份读取证据SHA，未用历史1578PASS冒充本轮。

## 输入和实际值依据

输入基于未布局的DE演示板，不向HI两层、四层b019或新层叠练习板应用DE旧网表。准备阶段复制119个板/两DSN/两组三PST/库依赖/官方命令与readback文件，逐项SHA一致，重放前后复制品与原源均保持。执行只对JK/eco/DE_REPLAY_ONLY工作副本进行。

`execute_plan.json`及`replay_input_manifest.json`记录原始命令、官方17.2文档和参数含义。netrev使用`-e -i <PST目录> <工作baseline> <独立ECO输出>`；`-e`是缺封装按错误，不能误解成ECO开关；`-n`用于新建板，现有板ECO不加；本轮也未使用禁DRC的`-d`。所有child TEMP/TMP/PCBENV/cwd在01AIEDA内。

器件值由本轮fresh数据库通过官方`axlWriteDeviceFile`导出的每ref设备文件`PACKAGEPROP VALUE`读取，再与同一实际compdef的VALUE属性双核，最后与预期比较；不从deviceType名称后缀猜值。每一个272 pin-net均直接来自本轮component_pins.tsv，不用原理图期望代替PCB读回。

未布局设计中`nets.tsv`的`net->pins=0`不等于零逻辑端点；本轮比较的是所有组件的272个`comp->pins`。这是实际数据库对象语义差异，应保留以免漏验。

## 审查脚本的修正

首稿只识别带引号的`PACKAGEPROP VALUE '2.2k'`，而官方设备文件也允许`VALUE 100nF`等不带引号值，因而产生解析器假失败。已保留`review_failed_parser_quotes_v1.json`，修正为读取行实际内容后按可选引号规范化，再复核native compdef，得到全部通过。这个失败来自独立解析程序，不是native ECO失败；没有为消除错误放宽预期变化。

准备比较程序时，首次文件写入曾因自动审批超时未执行；按工具说明重试一次成功。未改目的目录，也未产生外部Temp文件。

## 仍未证明的事项

这是受控、未布局DE演示的本轮ECO复现证据；不代表实际布线、制造、SI/PI/EMI或上电测试验收。没有应用本轮反向SWP到Capture GUI，也不把生成文件等同GUI应用。HI七个未接GPIO、四个USB/全板DRC、用户新四层层功能及性能待办继续由各自真实板版本跟踪。
