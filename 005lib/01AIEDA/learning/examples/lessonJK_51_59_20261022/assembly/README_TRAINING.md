# 装配训练资料的使用约定

全部文件标识 TRAINING_NOT_FOR_ASSEMBLY，以真实HI b019两板为输入；PCB尚有7个GPIO连接/板与USB和整板DRC待验。4L当前为LEGACY_4L_L3_GND，不代表用户新TOP/L2 GND/L3 power/BOTTOM规范已实现。

- BOM_80：80件均保留，包括2件DNP。BOM_grouped数量总和80。
- coordinates_all80：实际CAD符号原点，单位mm、X0/Y0不平移，TOP视图原生CCW角度；不是经工厂核准的吸取中心或机台角度。工厂角度列有意留空。
- SMT_candidates：65件工艺候选（含J2混装），不代表工厂已批准机器贴装。non_SMT_and_DNP：13件THT与2件DNP单列；不能从主BOM删除排针。
- mechanical_NPTH：6个机械孔独立，不计入80件BOM或贴装数量。stencil_apertures记录真实211开口，含4个DNP开口，钢网厚度及屏蔽策略待定。
- assembly_review：依据实际坐标的独立审核标注图，非Cadence原生字体/制造Artwork，也非已认证器件实体外形。

详细依据/问题/修正状态见01AIEDA/learning/notes/lessonJK_55_57_20261022.md。原生JK实例修正及其新进程验证完成后，应以新板SHA出具新身份文件，保留本b019训练基线。
