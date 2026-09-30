# Allegro env 快捷键说明

`01env/env` 是 Allegro 的快捷键和环境配置。切层**只保留 Ctrl 组合**。

| 按键 | 作用 |
|---|---|
| `Ctrl+T` | 只开 **TOP** |
| `Ctrl+B` | 只开 **BOTTOM** |
| `Ctrl+2` … `Ctrl+9` | 只开 **L2** … **L9** |
| `Ctrl+0` | 恢复全部层 |
| `Tab` | spin（旋转） |
| `O` | 生成 Gerber（毫米板，`gerber.scr`） |
| `Ctrl+O` | 生成 Gerber（英寸 mil 板，`gerber_mil.scr`） |

从 L2 切到 L3 时：L3 的 ETCH / PIN / VIA / 电气 DRC 打开，L2 的对应项关掉。右侧 **Through All** 黄点（等长报错）保持关。

`Ctrl+O` 与 `O` 流程相同：钻孔定制、钻孔图、NC Drill、NC Route、光绘外形、Artwork。坐标按 **1 mm = 39.3700787 mil** 换算，例如钻孔图 `-300 mm` → `-11811.0236 mil`，光绘窗口 `±1000 mm` → `±39370.0787 mil`。mm 的整数位 5 对应 mil 的整数位 7（99999 mm = 3936968.5 mil）。`Ctrl+O` 不再是 Open。

https://github.com/875638477/001Diy 
这个是我的github仓库的diy链接
帮我吧本文件夹所有库文件备份到github上文件夹和路径要完全   一致
PCB_pads_LIB
History
AUTOlib
这三个不用备份
压缩包也不同备份