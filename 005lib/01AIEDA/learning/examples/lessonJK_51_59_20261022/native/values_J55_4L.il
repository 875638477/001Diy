procedure(jkValues()
 let((f)
 f=outfile("D:/001DIY/005lib/01AIEDA/learning/examples/lessonJK_51_59_20261022/exports/devicevalues_J55_4L_TRAINING/component_values_source.tsv")
 fprintf(f "refdes\tinstanceProperties\tdefinitionProperties\tdefinitionAttributes\n")
 foreach(c axlDBGetDesign()->components
 fprintf(f "%L\t%L\t%L\t%L\n" c->name axlDBGetProperties(c) axlDBGetProperties(c->compdef) c->compdef->??)
 unless(axlWriteDeviceFile(c->compdef strcat("D:/001DIY/005lib/01AIEDA/learning/examples/lessonJK_51_59_20261022/exports/devicevalues_J55_4L_TRAINING/" c->name)) error("Native definition VALUE export failed\n")))
 fprintf(f "JK_NATIVE_80_DEVICE_VALUES_COMPLETE\n") close(f) t))
