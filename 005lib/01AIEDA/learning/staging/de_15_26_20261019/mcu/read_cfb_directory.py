from pathlib import Path
import struct, json, hashlib
ROOT=Path(__file__).resolve().parents[3]
p=ROOT/'examples'/'de_15_26_20261019'/'native'/'DE_INTEGRATED_BASELINE.DSN'
b=p.read_bytes()
assert b[:8]==bytes.fromhex('d0cf11e0a1b11ae1')
ssize=1<<struct.unpack_from('<H',b,30)[0]
difat=struct.unpack_from('<109I',b,76)
assert struct.unpack_from('<I',b,72)[0]==0,'unsupportedextendedDIFAT'
fat=[]
for sector in difat:
    if sector<0xfffffffa:
        fat.extend(struct.unpack('<%dI'%(ssize//4),b[(sector+1)*ssize:(sector+2)*ssize]))
def chain(start):
    seen=set(); data=b''
    while start<0xfffffffa:
        assert start not in seen
        seen.add(start)
        data+=b[(start+1)*ssize:(start+2)*ssize]
        start=fat[start]
    return data
dirs=chain(struct.unpack_from('<I',b,48)[0])
records={}
for idx in range(0,len(dirs),128):
    e=dirs[idx:idx+128]
    n=struct.unpack_from('<H',e,64)[0]
    if n>2 and e[66] in (1,2,5):
        records[idx//128]=dict(index=idx//128,name=e[:n-2].decode('utf-16le'),type=e[66],left=struct.unpack_from('<I',e,68)[0],right=struct.unpack_from('<I',e,72)[0],child=struct.unpack_from('<I',e,76)[0],sector=struct.unpack_from('<I',e,116)[0],size=struct.unpack_from('<Q',e,120)[0])
paths=[]
def walk(idx,parent):
    if idx==0xffffffff:return
    e=records[idx]
    walk(e['left'],parent)
    path=parent+[e['name']]
    out={**e,'path':'/'.join(path)}
    if e['type']==2 and e['size']>=4096:
        data=chain(e['sector'])[:e['size']]
        out['stream_sha256']=hashlib.sha256(data).hexdigest()
        out['first64hex']=data[:64].hex()
    paths.append(out)
    if e['child']!=0xffffffff:walk(e['child'],path)
    walk(e['right'],parent)
walk(records[0]['child'],[])
result={'read_only':True,'path':str(p),'sha256':hashlib.sha256(b).hexdigest(),'directory_entries':paths}
(Path(__file__).parent/'dsn_cfb_directory.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
for e in paths:print(e['index'],e['type'],e['size'],e['path'])
