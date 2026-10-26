; Definitions only, all placed logical/nonlogical cached definitions, no mutations.
load("D:/001DIY/004computer/lga1700/13shared_libraries_pc_20261025/w/pcb_migration/pc13_export_board_definitions.il")
procedure(pub13AllCachedOnly(dir)
 let((d f b s def seen count symbols missing file)
  sstatus(fullPrecision t) d=axlDBGetDesign() unless(d error("No active design\n"))
  seen=makeTable('pubAllCached nil) count=0 symbols=0 missing=0
  f=outfile(strcat(dir "/manifest.tsv")) b=outfile(strcat(dir "/all_symbol_definition_bindings.tsv"))
  fprintf(f "name\tfile\tunits\n") fprintf(b "index\tsymbol_name\trefdes\tcomponent\tdefinition\n")
  foreach(s d->symbols
   symbols=symbols+1 def=s->definition
   fprintf(b "%d\t%L\t%L\t%L\t%L\n" symbols s->name s->refdes if(s->component then s->component->name else nil) if(def then def->name else nil))
   if(def then unless(seen[def->name]
    seen[def->name]=t file=sprintf(nil "%s/def_%04d.sexp" dir count)
    pc13ExportOneDefinition(def file)
    fprintf(f "%L\t%L\t%L\n" def->name file axlDBGetDesignUnits()) drain(f) count=count+1)
   else missing=missing+1))
  close(f) close(b)
  f=outfile(strcat(dir "/PUBLIC_ALL_CACHE_COMPLETE.txt"))
  fprintf(f "COMPLETE_READ_ONLY_ALL_PLACED_SYMBOLS\nALL_SYMBOLS=%d\nACTUAL_CACHED_DEFINITIONS=%d\nSYMBOLS_WITHOUT_DEFINITION=%d\nSAVE_CALLS=0\n" symbols count missing) close(f) t))
