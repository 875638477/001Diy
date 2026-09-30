
:: 删除 JLINK 垃圾
del *.bak /s
del *.ddk /s
del *.edk /s
del *.lst /s
del *.lnp /s
del *.mpf /s
del *.mpj /s
del *.obj /s
del *.omf /s
::del *.opt /s  ::不允许删除JLINK的设置
del *.plg /s
del *.rpt /s
del *.tmp /s
del *.__i /s
del *.crf /s
del *.o /s
del *.d /s
del *.axf /s
del *.tra /s
del *.dep /s           
del JLinkLog.txt /s
del *.pbi /s
del *.xcl /s
del *.pbd /s
del *.browse /s
del *.linf /s
del *.pbw /s

::del *.IntLib /s
::del *.PCBDOC /s  ::
::del *.PcbDoc /s
::del *.PcbLib /s  ::
::del *.PRJPCB /s  ::
::del *.SchDoc /s  ::

:: 删除 allegro orcad 垃圾
del *.iex /s
del *.sct /s
del *.map /s
del *.BOM /s
del *.htm /s
del *.log /s
del *.log","1 /s
del *.log","2 /s
del *.log","3 /s
del *.edf /s
del *.opj /s
del *.dbk /s
del *.cfg /s
del *.cfg","1 /s
del *.jrl /s
del *.jrl","1 /s
del *.jrl","2 /s
del *.jrl","3 /s
del *.dmp /s
del *.baf /s
del *.ctl /s
del *.sav /s
del *.DRC /s
del *.dml /s
del *.tag /s
del *.csv /s
del *.cnv /s
del *.cnv","1 /s
del *.xml /s
del *.iml /s
del *.iml","1 /s
del *.txt /s
del *.txt","1 /s
del *.dat /s
del *.dat","1 /s
del *.dat","2 /s
del *.dat","3 /s
del *.dml"," /s
del *.dml","1 /s
del *.dml","1 /s
del *.dcf /s
del *.pro /s
del *.OBK /s
::del *.DBC /s
::del *.DBCBAK /s
::del *.psm /s
::del *.dra /s
::del *.pad /s

:: 删除 AD 垃圾
del *.pcbdoc_viewstate /s
del *.PCBDOCPreview /s
del *.PrjGrp /s
del *.SchDocPreview /s
del *.PcbLib.Zip /s
del *.PrjPCBStructure /s
del *.PcbDoc.Zip /s
del *.OutJob /s
del *.PrjPCB.Zip /s
del *.PCBDOCPreview /s
del *.SchDocPreview /s
del *.SchDocPreview /s
del *.$$$Preview /s
del *.PCBPreview /s
del *.SchPreview /s
del *.pcbdoc_viewstate /s

del *.db /s
@echo off
::假定winrar软件安装于c盘默认目录下，如自定义目录安装，请修改该行
::set "rar=C:\Program0\WinRAR1\WinRAR.exe"
::默认对当前批处理文件所在文件夹及子文件夹操作，也可以自定义文件夹根目录
::set srcdir="D:\001DIY\005lib\01env"
::set srcdir="E:\批量解压"
::winrar命令行只支持对.rar操作
::GZ代表压缩包的后缀名
::for /r %srcdir% %%i in (*.GZ) do "%rar%" x -y "%%i" "%%~dpi" && del "%%i">nul

::解压程序WinRAR.exe所在目录 32位%ProgramFiles(x86)% 或64位 %ProgramFiles%
::set WinRarDir=%Program0%\WinRAR1

:: x即解压。-y是说如果遇到提示说是否覆盖，选择yes
start  /wait  ""  "C:\Program0\WinRAR1\WinRAR.exe"  x  -l -y  D:\001DIY\005lib\01env\01env.rar  D:\001DIY\005lib\01env\

exit
