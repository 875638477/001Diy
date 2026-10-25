"""Package an owned working copy, recording pre-export identity and source integrity."""
from pathlib import Path
import hashlib, json, shutil, subprocess, sys

ROOT = Path(__file__).resolve().parents[1]
STAGE = ROOT/'staging/a4_review_20261019'
SOURCE = ROOT/'examples/de_15_26_20261019/a4_review/native/DE_INTEGRATED_A4.DSN'
PACK = STAGE/'packaging'
def sha(path): return hashlib.sha256(path.read_bytes()).hexdigest()
copy = PACK/'DE_A4.dsn'
before = sha(SOURCE)
shutil.copy2(SOURCE, copy)
record = {'source':str(SOURCE),'source_sha256_before':before,
          'working_copy':str(copy),'working_copy_sha256_before':sha(copy),
          'log':str(STAGE/'packaging_verified_process')}
(STAGE/'pst_input_identity.json').write_text(json.dumps(record,indent=2),encoding='utf-8')
run = subprocess.run([sys.executable,str(ROOT/'scripts/de_native_cli.py'),
 '--log',record['log'],'--timeout','40','pstswp.exe','-pst','-d',str(copy),
 '-n',str(PACK/'netlist'),'-c',str(PACK/'allegro.cfg'),'-v','3','-l','255','-j','PCB Footprint'])
launch = json.loads((Path(record['log'])/'launch.json').read_text(encoding='utf-8'))
record.update(source_sha256_after=sha(SOURCE),working_copy_sha256_after=sha(copy),
              native_exit_code=launch['exitCode'],native_completed=launch['completed'])
record['source_unchanged'] = record['source_sha256_before']==record['source_sha256_after']
record['working_copy_changed_during_packaging'] = record['working_copy_sha256_before']!=record['working_copy_sha256_after']
(STAGE/'pst_input_identity.json').write_text(json.dumps(record,indent=2),encoding='utf-8')
assert run.returncode==0 and launch['completed'] and launch['exitCode']==0
assert record['source_unchanged']
print(json.dumps(record,indent=2))
