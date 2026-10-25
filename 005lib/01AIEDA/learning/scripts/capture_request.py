"""Submit one owned lesson Tcl file to the isolated native Capture SDK session."""
from pathlib import Path
import argparse, time, json

root = Path(__file__).resolve().parents[1]
parser = argparse.ArgumentParser()
parser.add_argument('id')
parser.add_argument('script')
parser.add_argument('--timeout', type=int, default=25)
args = parser.parse_args()
if not args.id.replace('_','').isalnum(): raise ValueError('Use an alphanumeric request id')
script = Path(args.script).resolve()
if not script.is_relative_to(root) or not script.is_file(): raise ValueError('Script must exist under learning')
queue = root/'staging/capture_C_20261019/queue'
queue.mkdir(parents=True, exist_ok=True)
request = queue/(args.id+'.tcl')
result = root/'logs/capture_C_20261019/runtime'/(args.id+'.result.tcldict')
if request.exists() or result.exists(): raise ValueError('Request id already used')
partial=request.with_suffix('.part')
partial.write_text('source {'+script.as_posix()+'}\n',encoding='utf-8')
partial.rename(request)
for _ in range(args.timeout*5):
    if result.exists():
        print(result.read_text(encoding='utf-8-sig'))
        break
    time.sleep(.2)
else:
    print(json.dumps({'request_id':args.id,'status':'pending','result':str(result)}))
    raise SystemExit(2)
