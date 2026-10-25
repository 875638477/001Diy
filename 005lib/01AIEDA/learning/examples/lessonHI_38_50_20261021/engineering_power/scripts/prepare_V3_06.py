from pathlib import Path
R=Path(r'D:\001DIY\005lib\01AIEDA\learning\examples\lessonHI_38_50_20261021\engineering_power')
s=(R/'scripts/precheck_CAN04_05.py').read_text()
s=s.replace("files=['interface_CAN_routes_04.json','CAN_local_supply_05.json']","files=['interface_CAN_routes_04.json','CAN_local_supply_05.json','V3_peripheral_distribution_06.json']")
s=s.replace("'readouts/CAN_04_05_geometry_precheck.json'","'readouts/V3_06_CAN_04_05_geometry_precheck.json'")
(R/'scripts/precheck_V3_06.py').write_text(s)
print('prepared')
