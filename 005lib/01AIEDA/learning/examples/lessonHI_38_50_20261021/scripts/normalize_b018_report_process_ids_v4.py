from pathlib import Path
import json,re,csv
R=Path(r'D:\001DIY\005lib\01AIEDA\learning\examples\lessonHI_38_50_20261021');p=R/'scripts/report_TOP_trial_b017_b018HI_v3.py';s=p.read_text(encoding='utf-8-sig').replace("r'dbid:[0-9A-Fa-f]+','dbid:PROCESS_LOCAL'", "r'(dbid|pad|propList):[0-9A-Fa-f]+',r'\1:PROCESS_LOCAL'").replace("Only process-local dbid hexadecimal addresses replaced", "Only process-local dbid, pad and propList hexadecimal addresses replaced");(R/'scripts/report_TOP_trial_b017_b018HI_v4.py').write_text(s,encoding='utf8')
