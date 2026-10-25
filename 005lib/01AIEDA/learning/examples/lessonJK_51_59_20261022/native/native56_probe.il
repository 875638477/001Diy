procedure(jk56Probe(outname)
 let((p d a count tb)
 p=outfile(outname)
 d=axlDBGetDesign()
 fprintf(p "DESIGN\t%L\n" d->??)
 a=axlGetParam("paramDesign") fprintf(p "PARAM_DESIGN\t%L\n" a->??)
 a=axlGetParam("paramLayerGroup:ETCH") fprintf(p "ETCH\t%L\n" a->??)
 a=axlGetParam("artwork") fprintf(p "ARTWORK\t%L\n" a->??)
 foreach(name a->groupMembers
  a=axlGetParam(strcat("artwork:" name)) fprintf(p "FILM\t%s\t%L\n" name a->??)
 )
 count=axlDBGetTextBlockCount()
 for(i 1 count
  tb=axlGetParam(sprintf(nil "paramTextBlock:%d" i))
  fprintf(p "TEXTBLOCK\t%d\t%L\n" i tb->??)
 )
 fprintf(p "COMPLETE\tt\n") close(p) t
 ))
