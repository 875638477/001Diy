; Official readonly device exporter from actual in-process component definitions.
; Exports only into owned native-job output. No design/library save or setters.
procedure(pub13WriteNativeDeviceBodies(dir)
 let((d c seen count result f before after)
  d=axlDBGetDesign() seen=makeTable('pub13NativeDevices nil) count=0
  f=outfile(strcat(dir "/NATIVE_DEVICE_BODY_MANIFEST.tsv"))
  fprintf(f "device_type\tcomponent_class\tcompdef_class\tpackage\tapi_return\n")
  foreach(c d->components unless(seen[c->deviceType]
   seen[c->deviceType]=t
   result=axlWriteDeviceFile(c->compdef strcat(dir "/after"))
   fprintf(f "%L\t%L\t%L\t%L\t%L\n" c->deviceType c->class c->compdef->class c->package result) drain(f)
   unless(result close(f) error("Official native device file export failed\n"))
   count=count+1))
  close(f) f=outfile(strcat(dir "/NATIVE_DEVICE_BODIES_COMPLETE.txt"))
  fprintf(f "COMPLETE_READONLY_NATIVE_COMPONENT_DEFINITION_DEVICE_BODIES\nDEVICES=%d\nCLASS_SETTERS=0\nSAVE_CALLS=0\n" count) close(f) t))
