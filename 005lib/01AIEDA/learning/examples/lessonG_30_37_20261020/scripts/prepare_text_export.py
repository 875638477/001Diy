from pathlib import Path
p=Path(r'D:\001DIY\005lib\01AIEDA\learning\examples\lessonG_30_37_20261020\scripts\placementG.il')
s=p.read_text()
s=s.replace('let((pf gf df obj pin pad poly d)','let((pf gf df tf obj pin pad poly d)')
s=s.replace('df=outfile(strcat(out "/g_drc_details.txt"))','df=outfile(strcat(out "/g_drc_details.txt"))\n  tf=outfile(strcat(out "/board_instance_texts.tsv"))\n  fprintf(tf "refdes\\tpackage\\tlayer\\ttext\\txy\\trotation\\tmirrored\\tjustify\\ttextBlock\\tbbox\\tattrs\\n")')
s=s.replace('foreach(shape obj->children\n    when(','''foreach(shape obj->children
    when(equal(shape->objType "text")
     fprintf(tf "%L\\t%L\\t%L\\t%L\\t%L\\t%L\\t%L\\t%L\\t%L\\t%L\\t%L\\n" obj->refdes obj->name shape->layer shape->text shape->xy shape->rotation shape->isMirrored shape->justify shape->textBlock shape->bBox shape->??))
    when(''')
s=s.replace('foreach(f list(pf gf df) close(f))','foreach(f list(pf gf df tf) close(f))')
p.write_text(s,encoding='ascii')
print('INSTANCE_TEXT_EXPORT_READY')
