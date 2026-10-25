load {C:/Program0/Cadence/spb172/tools/bin/orDb_Dll_Tcl64.dll} DboTclWriteBasic
set ::DboSession_s_pDboSession [DboTclHelper_sCreateSession]
DboSession -this $::DboSession_s_pDboSession
set ::C11ExecutionMode standalone_Capture_native_database_SDK
source {D:/001DIY/005lib/01AIEDA/learning/scripts/c11_capture_runtime.tcl}
vwait ::C11Shutdown
