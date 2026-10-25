# 新四层装配身份副本（仅训练）

**TRAINING_NOT_FOR_ASSEMBLY / NOT_RELEASED。** 本目录绑定实际新栈板：`TOP-L2-L3-BOTTOM`，L2共地、L3实际V3V3。它与旧J55装配包分别保存。

80件、66组、80坐标、65贴装候选、15非SMT或DNP项；所有元件值由原生VALUE属性及官方设备文件双核。5份CSV除3个坐标类文件的源板SHA外，其余字段与旧J55_4L一致。具体板身份及独立结构报告见[source_identity.json](source_identity.json)。

坐标为mm、数据库X0/Y0下的封装symbol原点；原生旋转不是工厂旋转。工厂旋转列刻意留空，未核准吸取中心或MPN；68件仍需采购选型。13个THT项和2个DNP项不进入SMT候选，J2混合结构需单独工艺确认。6个NPTH机械孔不属于BOM器件。

72个1mm是用户默认CAD高度，8个既有显式高度保留；均不自动等于实物高度认证。阻焊桥、钢网厚度、DNP开口抑制、插装脚长、字体及装配余量等旧开放项继续适用。新SHA绑定和实际内层更改不等于工厂批准、USB90Ω、SI/PI或完整DRC通过；仍有7个GPIO连接待完成。
