from pathlib import Path
R=Path(r'D:\001DIY\005lib\01AIEDA\learning\examples\lessonHI_38_50_20261021');s=(R/'scripts/prepare_nonUSB65_scoped_b018_2LHI_v2.py').read_text(encoding='utf-8-sig').replace('PRE_NON_USB_65_DRC_PENDING','PRE_ALL69_DRC_PENDING');(R/'scripts/prepare_nonUSB65_scoped_b018_2LHI_v3.py').write_text(s,encoding='utf8')
