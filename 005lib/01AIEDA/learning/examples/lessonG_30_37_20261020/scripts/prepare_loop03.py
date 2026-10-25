from pathlib import Path
R=Path(r'D:\001DIY\005lib\01AIEDA\learning\examples\lessonG_30_37_20261020')
il=(R/'scripts/local_copperG.il').read_text().replace('neighbors=append(car(neighbors) cadr(neighbors))','when(listp(car(neighbors)) neighbors=append(car(neighbors) cadr(neighbors)))')
(R/'scripts/local_copperG_v2.il').write_text(il,encoding='ascii')
il=(R/'scripts/local_loops02.il').read_text().replace('35.75:24.25','35.20:24.25').replace('35.75:24.75','35.20:24.75').replace('42.75:22.75','42.75:22.20').replace('42.25:22.75','42.25:22.20').replace('44.25:29.75','44.80:29.75').replace('44.25:29.25','44.80:29.25')
(R/'scripts/local_loops03.il').write_text(il,encoding='ascii')
s=(R/'scripts/loops_4L_02.scr').read_text().replace('local_copperG.il','local_copperG_v2.il').replace('local_loops02.il','local_loops03.il').replace('loops_4L_02','loops_4L_03').replace('G_4L_LOOPS_v2','G_4L_LOOPS_v3')
(R/'scripts/loops_4L_03.scr').write_text(s,encoding='ascii')
# 2L has .20 spacing power and default .16, no region required, keep all inherited rules.
il=il.replace('gEscapeRegion(f)','fprintf(f "TWO_LAYER_NO_SPACING_EXCEPTION_NEEDED\\n")',1) if False else il
# Remove only invocation, keep unused definition.
il=il.replace('  gEscapeRegion(f)','  fprintf(f "TWO_LAYER_NO_SPACING_EXCEPTION_NEEDED\\n")')
(R/'scripts/local_loops_2L03.il').write_text(il,encoding='ascii')
s=(R/'scripts/loops_2L_01.scr').read_text().replace('local_copperG.il','local_copperG_v2.il').replace('local_loops01.il','local_loops_2L03.il').replace('loops_2L_01','loops_2L_03').replace('G_2L_LOOPS_v1','G_2L_LOOPS_v3')
(R/'scripts/loops_2L_03.scr').write_text(s,encoding='ascii')
