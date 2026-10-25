from pathlib import Path
R=Path(r'D:\001DIY\005lib\01AIEDA\learning\examples\lessonG_30_37_20261020')
il=(R/'scripts/finalG.il').read_text().replace("axlCnsClassTableFind('all)","axlCnsClassTableFind('netclass)").replace("axlCNSList(","axlCnsList(")
(R/'scripts/finalG_v2.il').write_text(il,encoding='ascii')
s=(R/'scripts/bulk_2L_01.scr').read_text().replace('finalG.il','finalG_v2.il').replace('bulk_2L_01','bulk_2L_02')
(R/'scripts/bulk_2L_02.scr').write_text(s,encoding='ascii')
