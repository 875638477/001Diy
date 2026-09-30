# Allegro 坐标导出（reports.txt）

`reports.txt` 是 Tools > Reports 用的 Extract 命令文件。  
快捷键 R，或 **Tools > Reports** 里选 `reports.txt`，再点 **Report**。

只保留一个 `COMPONENT` 视图。同一个文件里再加 `GEOMETRY` 会导致 Allegro 崩溃。

## 列说明

| 列 | 含义 |
|----|------|
| `COMP_VALUE` | 器件 Value |
| `SYM_X` `SYM_Y` | symbol origin（封装原点） |
| `SYM_CENTER_X` `SYM_CENTER_Y` | **body center**（贴片用这个） |
| `SYM_ROTATE` | 旋转角 |
| `SYM_MIRROR` | 是否镜像（YES=底面） |

`SYM_CENTER` 与 **File > Export > Placement** 勾选 **Body center** 是同一套算法：

1. 有 `BODY_CENTER` 文字，用该点
2. 否则用 `PLACE_BOUND_TOP` 矩形中心

File > Export > Placement 能出 body center，但没有 Value。  
用这份 Reports 可以一次同时得到 **body center + Value**。
