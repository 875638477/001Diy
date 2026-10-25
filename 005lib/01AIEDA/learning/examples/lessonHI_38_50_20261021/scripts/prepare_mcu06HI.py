from pathlib import Path
R=Path(r'D:\001DIY\005lib\01AIEDA\learning\examples\lessonHI_38_50_20261021')
s=(R/'scripts/adapt_mcu05HI.py').read_text().replace('mcu_critical_routes_v5.json','mcu_critical_routes_v6.json').replace('b005.json','b006.json')
(R/'scripts/adapt_mcu06HI.py').write_text(s,encoding='ascii')
