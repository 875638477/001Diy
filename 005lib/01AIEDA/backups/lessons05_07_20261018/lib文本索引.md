我的计算机安装了多个版本 目前使用17.2比较合适
cadence 17.2版本的安装目录
C:\Program0\cadence\SPB172
C:\Program0\cadence\LicenseManager172
C:\Program0\cadence\SPBData172\pcbenv
D:\001DIY\005lib\01AIEDA 是 ai接管cadence 路径文件
D:\001DIY\005lib\01brdlib  pcb库路径文件
D:\001DIY\005lib\01captureLib 原理图库路径
D:\001DIY\005lib\01env  环境变量 快捷方式路径
D:\001DIY\005lib\01Pad_lib 焊盘库路径
D:\001DIY\005lib\01Psm_lib 封装库路径
D:\001DIY\005lib\01script_file 用脚本的路径
C:\Program0\SumatraPDF\SumatraPDF.exe  是pdf阅读器的路径
D:\005study 是学习的视频和软件的书籍的 
CADENCE 17.2电路设计与仿真 从入门到精通 云课版 (李鹏) (z-library.sk, 1lib.sk, z-lib.saak).pdf

## QMI8610 PCB 库（2026-10-18）

- 数据手册：D:\004Document\016Sensor\06IMU\矽睿\QMI8610 Datasheet Rev. A.pdf，Document 13-52-14 Rev A，第8/9/79页。
- PCB Footprint 名称：qmi8610_lga16_3d3_p0d5（不带扩展名）。
- 可编辑封装：D:\001DIY\005lib\01Psm_lib\qmi8610_lga16_3d3_p0d5.dra
- 编译封装：D:\001DIY\005lib\01Psm_lib\qmi8610_lga16_3d3_p0d5.psm
- 焊盘：D:\001DIY\005lib\01Pad_lib\qmi8610_smd061x032_m05_p100.pad
- 本次只做 PCB，不创建 Capture OLB。
- 已保存、编译、独立重开；公共PSM载入练习PCB并核对顶层0°/90°、底层镜像48个引脚。
- 工程取值：阻焊每边外扩0.05mm、钢网1:1；最小阻焊桥0.08mm，生产时配合板厂/贴片工艺确认。
- 规格、预览、脚本和验收记录：learning/examples/qmi8610/README.md、qmi8610_spec.json、final_validation.json；笔记learning/notes/qmi8610_package_20261018.md。
