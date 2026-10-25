AD18 native connectivity research (2026-10-23)

Status: prepared, not executed. AD has not been started; source files have not been modified.

Installed executable: C:\Program0\AD18\X2.exe (registry AD18 18.0.7.293).
The draft opens only source_copy\lga1700.PrjPCB under this research directory.
Copy the source project and its relative-path source documents there before an isolated trial.
The script calls DM_Compile, then reads DM_DocumentFlattened and exports each native net and its pins.
Use net_index / pin membership to compare connectivity, and compare flattened_net_name separately.
Inspect native compile diagnostics before treating the exported graph as an accepted baseline.
The draft does not change project options, source document contents, annotations, or library objects.
SaveToFile writes only research TSV/status files; no design-document save or AD exit is performed.
The minimal PrjScr container and DelphiScript bindings need an isolated AD18 runtime trial.

Documented UI route: File > Run Script, browse NativeConnectivity.PrjScr, run DumpCompiledConnectivity.
A form-free .pas can also use ScriptingSystem:RunScriptFile with FileName and ProcName parameters.
The official Altium CI article demonstrates external X2 -RScriptingSystem:RunScript in AD19.
For this draft the process parameters would be:
ProjectName=<this directory>\NativeConnectivity.PrjScr|ProcName=DumpCompiledConnectivity.pas>DumpCompiledConnectivity
This is a candidate for AD18, not runtime-verified. Keep the process string as one shell argument.
The official article's caret before the pipe is cmd.exe escaping, not an Altium parameter.
This is a GUI process entry; no separate headless Altium compiler has been established.
Do not use CloseObject All or TerminateWithExitCode in a user session.

Official sources:
https://resources.altium.com/p/continuous-integration-implementation-using-altium-designer
https://www.altium.com/documentation/altium-dxp-developer/workspace-manager-api
https://www.altium.com/documentation/altium-dxp-developer/delphi-sdk-how-to-faq
https://www.altium.com/documentation/altium-designer/scripting/running-scripts

GNDA decision:
https://www.altium.com/documentation/altium-designer/schematic/creating-circuit-connectivity
A net label and power port with the same name do not automatically join.
PowerPortNamesTakePriority=0 changes name precedence, not connectivity.
Keep the separate 5-pin GNDA/SIO_GNDA label branch and 3-pin GNDA power branch distinct pending native compile.
Separate schematic nets with equal final names may merge during PCB transfer, so retain net partitions independently of names.
