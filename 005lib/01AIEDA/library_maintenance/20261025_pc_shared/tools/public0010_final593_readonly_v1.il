; Definitions only. Query an owned read-only final candidate; no806 re-probe.
pub403Bundle="D:/001DIY/005lib/01AIEDA/library_maintenance/20261025_pc_shared/public0010_native403_bundle13_v6_restore"
load(strcat(pub403Bundle "/public0010_native403_v1.il"))
procedure(pub0010Final593Readonly(dir)
 let((f)
  sstatus(fullPrecision t) pub403ReadUnits()
  pub403FullTypedGate(strcat(pub403Bundle "/TARGET_FULL2698_WITH_NONLOGICAL_IDENTITIES.ilist"))
  pub403StateGate(strcat(pub403Bundle "/SOURCE_CONTROL_EXPECTED_ALL593_TEXT_PROPS.ilist"))
  pub403AllNameGate(nil)
  pub403SnapshotAll(strcat(dir "/FINAL_FRESH_ALL593_TEXT_PROPS.ilist"))
  f=outfile(strcat(dir "/FINAL_FULL2698_593_READONLY_COMPLETE.txt"))
  fprintf(f "FINAL_FRESH_ALL2698_TYPED_PINS_ALL593_POSE_OWNED_TEXT_SYMBOL_COMPONENT_COMPDEF_PROPERTIES_AND_USED_FONTS_EXACT_SOURCE_ONLY403_DEFINITION_NAMES\nNO_CREATE_NO_SAVE_NO806_REPROBE\n") close(f) t))
