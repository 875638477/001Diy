load {C:/Program0/Cadence/spb172/tools/bin/orDb_Dll_Tcl64.dll} DboTclWriteBasic
set ::DboSession_s_pDboSession [DboTclHelper_sCreateSession]
DboSession -this $::DboSession_s_pDboSession
source {D:/001DIY/005lib/01AIEDA/learning/scripts/de_capture_helpers.tcl}
set root {D:/001DIY/005lib/01AIEDA/learning/staging/lga1700_pcb_repair_20261023/stub_xml_roundtrip_probe}
puts [list export_command [info commands XMATIC_DSN2XML] import_command [info commands XMATIC_XML2DSN]]
if {[info commands XMATIC_DSN2XML] eq {} || [info commands XMATIC_XML2DSN] eq {}} {exit 2}
set code [catch {
 if {[file exists "$root/design.xml"] || [file exists "$root/roundtrip.DSN"]} {error {Refuse existing XML/output DSN}}
 set st [XMATIC_DSN2XML "$root/input.DSN" "$root/design.xml" {C:/Program0/Cadence/SPB172/tools/capture/tclscripts/capDB/dsn.xsd} "$root/export.log" 0]
 ::DE::state $st ExportDesignXML
 if {![file exists "$root/design.xml"]} {error {Export returned but XML file absent}}
 puts [list exported_xml_bytes [file size "$root/design.xml"]]
 set st [XMATIC_XML2DSN "$root/design.xml" "$root/roundtrip.DSN" 0 0 "$root/import.log" "$root/import_extra.tcl"]
 ::DE::state $st ImportDesignXML
 if {![file exists "$root/roundtrip.DSN"]} {error {Import returned but output DSN absent}}
 dict create status roundtrip_complete dsn_bytes [file size "$root/roundtrip.DSN"]
} result opts]
::DE::write "$root/roundtrip_result.tcldict" [dict create code $code result $result opts $opts]
puts [dict create code $code result $result]
if {$code} {puts [dict get $opts -errorinfo]}
exit $code
