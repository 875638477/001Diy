from pathlib import Path
R=Path(r'D:\001DIY\005lib\01AIEDA\learning\examples\lessonHI_38_50_20261021')
p=R/'scripts/adapt_postcritical09HI.py';s=p.read_text().replace("val=val[0]+'.'+str(val[1]);op[field]=val","assert len(val) in (1,2), 'Endpoint list must be a single named alias or [ref,pin]'\n    val=val[0] if len(val)==1 else val[0]+'.'+str(val[1]);op[field]=val")
p.write_text(s,encoding='ascii')
