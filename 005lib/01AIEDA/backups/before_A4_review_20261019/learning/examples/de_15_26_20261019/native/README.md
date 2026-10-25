# D和E课程原生练习入口

权威基线：DE_CONTROL.opj → de_integrated_single.dsn，原生库为../library/de_training_single.olb。权威ECO：DE_CONTROL_ECO.opj → de_integrated_eco_final.dsn。OPJ资源路径存在，GUI打开尚未验；两个DSN均由独立官方数据库会话保存重开及pstswp真实导出验证。

两版80件/272物理pin/69net/266连接/6明确NC。单页是六模块整合的接口与连接练习：原始教学模块名存于SOURCE_MODULE_PAGE属性，课程笔记与BOM按模块分类。矩形符号体是显式引脚的教学模型，不把符号外观当成最终制图规范；器件电气脚名/物理编号/连接独立核对。

DE_INTEGRATED_V1、BASELINE、SEQUENTIAL六页版本及de_integrated_eco.dsn为试错历史，不作继续设计入口。多页Expand/PST包装失败未解决，没有用部分网表生成的板代替完整通过的工程。正式板与反向比较以课程总记录指向的native_flow_final为准。

未放置/布线，未完成GUI ERC、生产电路审查及器件采购/制造释放。裸板文件用于第26课网络/ECO学习。后续优先从基线2.2k I2C上拉方案继续；3.3k ECO为明确变更实验，100pF下400kHz RC预算余量更小。
