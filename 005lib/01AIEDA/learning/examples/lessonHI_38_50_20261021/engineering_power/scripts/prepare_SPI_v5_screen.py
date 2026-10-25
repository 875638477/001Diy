from pathlib import Path
import shutil
R=Path(r'D:\001DIY\005lib\01AIEDA\learning\examples\lessonHI_38_50_20261021\engineering_power')
shutil.copyfile(R.parent/'plans/SPI_source_explicit_v5.json',R/'source/root_SPI_source_explicit_v5.json')
s=(R/'scripts/precheck_prefilter08_NSSpatched.py').read_text().replace("'source/root_SPI_NSS_westvia_patch_proposal.json'","'source/root_SPI_source_explicit_v5.json'").replace("'readouts/Prefilter08_NSS_westvia_patch_power_group_precheck.json'","'readouts/SPI_source_v5_power_prefilter08_precheck.json'")
(R/'scripts/precheck_SPI_source_v5.py').write_text(s)
print('preparedSPIv5')
