procedure(jkEcoRead()
 let((f)
 deBoardRead("D:/001DIY/005lib/01AIEDA/learning/examples/lessonJK_51_59_20261022/eco/DE_REPLAY_ONLY/logs/eco_readonly")
 f=outfile("D:/001DIY/005lib/01AIEDA/learning/examples/lessonJK_51_59_20261022/eco/DE_REPLAY_ONLY/logs/eco_readonly/component_values_source.tsv")
 fprintf(f "refdes\tinstanceProps\tdefinitionProps\tdefinitionAttrs\n")
 foreach(c axlDBGetDesign()->components
 fprintf(f "%L\t%L\t%L\t%L\n" c->name axlDBGetProperties(c) axlDBGetProperties(c->compdef) c->compdef->??)
 unless(axlWriteDeviceFile(c->compdef strcat("D:/001DIY/005lib/01AIEDA/learning/examples/lessonJK_51_59_20261022/eco/DE_REPLAY_ONLY/logs/eco_readonly/devices/" c->name)) error("Native device definition export failed\n")))
 fprintf(f "JK_ECO_NATIVE_DEVICE_READ_COMPLETE\n") close(f) t))
