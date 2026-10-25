from pathlib import Path
import json,hashlib,subprocess,sys,shutil
R=Path(r'D:\001DIY\005lib\01AIEDA\learning\examples\lessonHI_38_50_20261021');sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest().upper()
s=(R/'scripts/prepare_b016_phased_retryHI.py').read_text();s=s[s.index('for v,t in '):].replace("[('2L','06'),('4L','03')]","[('4L','03')]").replace('prepare_b016_retryHI_v2.py','prepare_b016_retryHI_v3.py');exec(s)