from pathlib import Path
import csv,json,hashlib,collections,shutil
B=Path(r'D:\001DIY\005lib\01AIEDA\learning\examples\lesson29_constraints_20261019_review')
B.mkdir(exist_ok=True)
(B/'source').mkdir(exist_ok=True);(B/'scripts').mkdir(exist_ok=True)
S=Path(r'D:\001DIY\005lib\01AIEDA\learning\examples\lesson28_stackup_20261019\logs\baseline01')
r=list(csv.DictReader((S/'pads.tsv').open(),delimiter='\t',quoting=csv.QUOTE_NONE))
nets=collections.defaultdict(set);pins={}
q=lambda s:s.strip('"')
for x in r:
 key=(q(x['refdes']),q(x['number']));net=q(x['net'])
 assert key not in pins or pins[key]==net
 pins[key]=net;nets[net].add(key)
data={'source':str(S),'pinCount':len(pins),'nets':{k:sorted(v) for k,v in nets.items()},'sourceHashes':{p:hashlib.sha256((S/p).read_bytes()).hexdigest().upper() for p in ['components.tsv','nets.tsv','pads.tsv']}}
(B/'baseline_connectivity.json').write_text(json.dumps(data,indent=2),encoding='utf-8')
for net,p in nets.items():
 if any(z in net for z in ['USB','PA11','PA12','CAN']):print(net,sorted(p))
for key,net in pins.items():
 if key[0] in ['R5','R6','R11']:print('USB control/series',key,net)
D=Path(r'C:\Program0\Cadence\SPB172\share\pcb\examples\skill\DOC\FUNCS')
for name in ['axlCNSGetPhysical.txt','axlCNSSetPhysical.txt','axlCNSGetSpacing.txt','axlCnsClassTableSeek.txt','axlCnsClassTableFind.txt','axlCNSEcsetValueGet.txt','axlNetEcsetValueGet.txt','axlCnsNetFlattened.txt']:
 shutil.copy2(D/name,B/'source'/name)
print('Independent baseline prepared',len(pins),'logical pins')
