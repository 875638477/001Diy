# PCB 层叠命名与光绘模板规范

来源：用户于2026-10-18明确指定，作为后续建板和设计的固定要求。目的是沿用01env的光绘模板与现有快捷方式。

| 导电层数 | 从顶到底的层名顺序 |
| --- | --- |
| 2 | TOP-BOTTOM |
| 4 | TOP-L2-L3-BOTTOM |
| 6 | TOP-L2-L3-L4-L5-BOTTOM |
| 8 | TOP-L2-L3-L4-L5-L6-L7-BOTTOM |
| 更多层 | TOP，随后L2至L(N−1)，最后BOTTOM |

使用大写、连续编号和准确顺序。L2/L3等是固定层名；地/电源/信号用途记录为层功能和网络属性，不用GND、POWER、IN1、INNER1等替代这些层名。新练习板、正式PCB、走线/过孔层、导入导出及光绘映射都按此核对。实际物理顺序读取设计Cross Section，不能仅凭名称排序推断。

D:\001DIY\005lib\01env\drill*.txt 是用户已有的对应光绘层信息/脚本。已只读盘点13份：drill2、2noet、2REF、2VAL、4、4noet、6、6nodll、8、8noet、10、12、18。它们含axlFilmCreate及ETCH/PIN/VIA等层映射，读取时不执行这些命令。

重要区分：模板 ?sequence 是光绘Film参数，不能拿它替代PCB物理层叠顺序。例如drill4中L2/L3的sequence数值并非物理层号。实际建板先按用户规定的Cross Section顺序，再核对模板中对应层映射。

只读盘点的每份原始SHA256、铜Film名称、ETCH引用与规则一致性见 [模板清单](../logs/layer_template_inventory_20261018.json)。本轮没有修改01env模板或快捷方式；第7课四层练习已按此规则调整为 TOP-L2-L3-BOTTOM，最终应由原生层叠读回验收。

后续执行：先读取本文件与匹配层数模板，建板后读回导电层名称和顺序；输出光绘前核对模板所有引用实际存在，并按实际铜/阻焊/丝印/钻孔产物验收。模板中任何疑点单独记录，不能为了迁就新层名擅改用户快捷方式。

## 本次已发现的模板差异

13份模板中，drill12.txt的铜Film定义为TOP,L2,L3,L4,L5,L6,L7,L8,L9,L10,L11,L12,BOTTOM，共13项。L12定义在第67—72行；按12层固定规范应为TOP,L2至L11,BOTTOM。已通知用户并记录差异，未修改模板。其余12份的铜Film名称/次序与对应层数规则一致；13份铜Film的ETCH引用均对应自身层名。本次只核模板映射，未执行光绘生产输出。

## 2026-10-19补充：物理层表与完整Artwork（用户截图纠错）

1. 两/四/六层固定铜名与顺序按上表，逐项读取原生名称；TOP/BOTTOM不得凭界面显示的Top/Bottom样式擅自改名。
2. 用户板的Cross Section不另加Soldermask_Top/Bottom物理MASK行。阻焊厚度/材料放制造说明；保留PIN、VIA CLASS、PACKAGE/BOARD GEOMETRY的阻焊开窗与输出子类。Through All是默认通孔跨度，不是额外铜层。
3. Artwork完整执行匹配的01env/drill*.txt，包含铜、锡膏、丝印、阻焊、钻孔、外形、PDF和显示Film；drill2有15项，drill4有17项。严禁只挑铜Film，严禁自行加F28_DESIGN_OUTLINE等替代项目。
4. 验收全部Film集合、每项class/subclass及所有Options，不以铜Film通过替代完整模板通过。sequence仍不是物理层号。
5. 模板的OUTLINE必须具有与真实DESIGN_OUTLINE一致的有效板框；不改原模板，不靠新建Film绕过。模板历史无效引用和软件数值量化差异逐项记录，不能静默修文件或凭空增铜层。
6. 修改后另进程重开，核MASK=0、原生铜序/大小写、15/17全部Film及Options、真实板框、网络/焊盘/机械/约束保持；最后确认DRC及来源SHA。旧“只验铜”报告不能作为当前合规证据。

本次失误、纠正版文件及证据见[完整纠错记录](lessonF_stack_artwork_correction_20261019.md)。
