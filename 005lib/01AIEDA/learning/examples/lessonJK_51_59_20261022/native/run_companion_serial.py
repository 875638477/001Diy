import pathlib,shutil,json,subprocess,sys
R=pathlib.Path(r'D:\001DIY\005lib\01AIEDA\learning\examples\lessonJK_51_59_20261022')
s=(R/'native/run_native56_v7.py').read_text();s=s.replace("'ncroute'],required=True)","'ncroute','skill'],required=True)").replace("P.add_argument('--outdir');a=P.parse_args()","P.add_argument('--outdir');P.add_argument('--script');a=P.parse_args()")
s=s.replace("elif a.action=='list':", "elif a.action=='skill':\n assert a.script and pathlib.Path(a.script).resolve().is_relative_to(R.resolve())\n args=[str(C/'allegro.exe'),'-product','Allegro_performance','-safe','-nographic','-s',a.script,'-p',str(log),str(board)]\nelif a.action=='list':")
(R/'native/run_native56_v8.py').write_text(s,encoding='utf8')
for v in ['2L','4L']:
 out=R/'exports'/f'supplement_{v}_THREE_TEXTS_TRAINING';out.mkdir(exist_ok=False)
 shutil.copy2(R/'exports'/f'native_{v}_TRAINING_NOT_FOR_FAB'/'art_param.txt',out/'art_param.txt')
 (out/'TRAINING_NOT_FOR_FAB.txt').write_text('Three companion review Films only; not replacement for original 15/17 templates. Not a fabrication release.\n',encoding='ascii')
 base=R/'native'/v/f'JK_{v}_J55_text_height_review_NOT_RELEASED.brd';work=R/'native'/v/f'supplement_{v}_WORKING_COPY.brd';shutil.copy2(base,work)
 gen=R/'native'/v/f'JK_{v}_THREE_TEXT_FILM_GENERATOR_ONLY.brd';assert not gen.exists()
 il='procedure(jkSupp()\n foreach(n axlGetParam("artwork")->groupMembers unless(axlDeleteObject(axlGetParam(strcat("artwork:" n))) error("Cannot retire generator Film\\n")))\n'
 for name,layer in [('REFDES_SILK_TOP','REF DES/SILKSCREEN_TOP'),('REFDES_ASSEMBLY_TOP','REF DES/ASSEMBLY_TOP'),('VALUE_ASSEMBLY_TOP','COMPONENT VALUE/ASSEMBLY_TOP')]:
  il+=' unless(axlFilmCreate("'+name+'" ?undefineLineWidth 0.1 ?suppressUnconnectPads nil ?drawMissingPadApertures nil ?layers list("'+layer+'")) error("Cannot create companion film\\n"))\n'
 il+=' unless(length(axlGetParam("artwork")->groupMembers)==3 error("Generator must have3Films\\n"))\n jk56Probe("'+(out/'generator_inventory.tsv').as_posix()+'")\n unless(axlSaveDesign(?design "'+gen.as_posix()+'" ?noMru t ?noConfirm t) error("Generator SaveAs failed\\n")) t)\n'
 (R/'native'/f'supplement_{v}.il').write_text(il,encoding='ascii')
 scr='set NOCONFIRM\nskill errset(load("'+(R/'native/native56_probe.il').as_posix()+'") t)\nskill errset(load("'+(R/'native'/f'supplement_{v}.il').as_posix()+'") t)\nskill errset(jkSupp() t)\nskill axlKillDesign()\nquit\n'
 (R/'native'/f'supplement_{v}.scr').write_text(scr,encoding='ascii')
 args=[sys.executable,str(R/'native/run_native56_v8.py'),'--variant',v,'--outdir',str(out)]
 subprocess.run(args+['--action','skill','--tag',f'supplement_{v}_generator_01','--board',str(work),'--script',str(R/'native'/f'supplement_{v}.scr')],check=True)
 assert gen.exists()
 subprocess.run(args+['--action','artwork','--tag',f'supplement_{v}_artwork_01','--board',str(gen)],check=True)
