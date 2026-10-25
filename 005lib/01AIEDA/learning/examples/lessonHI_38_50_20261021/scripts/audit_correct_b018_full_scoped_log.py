from pathlib import Path
import re,json,hashlib,shutil
R=Path(r'D:\001DIY\005lib\01AIEDA');H=R/'learning/examples/lessonHI_38_50_20261021'
D=json.loads(r'''{"fix":"4L 61/65\u7f51\u4e3a0\uff0c4\u7f51\u67098\u6761\u540c\u6837\u7ec6\u9888\u8d85\u957f\uff0cUSB_DP\u5185\u90e8\u6c42\u89e3\u5668\u963b\u585e\u3001\u53e63\u7f51\u672a\u68c0\u67e5","bannerFix":"4L\u540c\u683761\u7f51\u4e3a0\uff0cBOOT0\u3001GPIO_PA15\u3001GPIO_PB4\u3001I2C_SCL\u54042\u6761\u7ec6\u9888\u8d85\u957f\uff1bUSB_DP\u89e6\u53d1","histFix":"4L\u7684\u5b8c\u6574\u539f\u59cb\u9010\u7f51\u7ed3\u679c\u540c\u6837\u662f61\u7f51\u4e3a0\u3001\u4e0a\u8ff04\u7f51\u54042\u6761\u8d85\u957f\u3002\u5148\u524d\u53ea\u8bfb\u65e5\u5fd7\u5c3e\u90e8\u800c\u8bef\u5199\u621065\u7f51\u51680\uff0c\u73b0\u5df2\u7531\u7236\u7ea7\u811a\u672c\u9010\u9879\u89e3\u6790\u5168\u90e865\u6761\u7ea0\u6b63\uff1b\u539f\u59cb\u65e5\u5fd7\u548c\u6539\u524d\u6587\u6863\u4fdd\u7559\u3002\u5230USB_DP\u65f6","guideFix":"4L61/65\u7f51\u4e3a0\u3001\u540c4\u7f518\u6761\u7ec6\u9888\u8d85\u957f\uff0cUSB_DP\u6c42\u89e3\u963b\u585e/3\u7f51\u672a\u8bd5","note":"\n\n### 2026-10-22 \u9010\u7f51\u6c47\u603b\u62a5\u544a\u5931\u8bef\u53ca\u4fee\u6b63\n\n\u6b64\u524d\u628a\u56db\u5c42\u201865\u4e2a\u7f51\u5747\u8fd4\u56de\u2019\u8bef\u62a5\u4e3a\u201865\u4e2a\u7f51\u5747\u4e3a0\u2019\uff0c\u539f\u56e0\u662f\u4ec5\u67e5\u770b\u65e5\u5fd7\u672b\u5c3eCAN\u4e24\u7f51\uff0c\u6ca1\u6709\u89e3\u6790\u5168\u90e8\u7ed3\u679c\u3002\u7236\u7ea7\u73b0\u72ec\u7acb\u5b8c\u6574\u89e3\u6790\u4e24\u677f\u6240\u6709NET_RESULT\u5e76\u4e0eNET_BEGIN\u96c6\u5408\u6838\u5bf9\uff1a\u4e24\u677f\u574761\u67610\u30014\u67612\uff08BOOT0\u3001GPIO_PA15\u3001GPIO_PB4\u3001I2C_SCL\uff09\uff0c\u5408\u8ba1\u54048\u6761\u771f\u5b9eDRC\u30024L USB_DP\u53ea\u6709BEGIN\u6ca1\u6709RESULT\uff0c\u53e6\u59163\u4e2aUSB\u7f51\u672a\u5f00\u59cb\uff1b2L\u56db\u4e2aUSB\u7f51\u5747\u672a\u6267\u884c\u3002\u673a\u5668\u6838\u5bf9\u89c1[b018\u5b8c\u6574\u9010\u7f51\u5ba1\u8ba1](../examples/lessonHI_38_50_20261021/review/b018_scoped_full_log_independent_audit.json)\u3002\u4fdd\u5b58Pending\u677f\u4e0d\u6539\uff0c\u9519\u8bef\u7684\u521d\u62a5\u672a\u7528\u4f5c\u9a8c\u6536/current\u664b\u7ea7\uff1b\u4ee5\u540e\u901a\u8fc7\u6570\u3001\u5931\u8d25\u6570\u3001\u672a\u8fd4\u56de\u6570\u3001\u672a\u6267\u884c\u6570\u5fc5\u987b\u5206\u522b\u7531\u5168\u65e5\u5fd7\u89e3\u6790\uff0c\u4e0d\u4ece\u5c3e\u90e8\u6216\u8fdb\u7a0b\u9000\u51fa\u7801\u63a8\u65ad\u3002\n"}''')
logs={'2L':H/'logs/nonUSB65_scoped_TOP_trial_2L_b018_01/all69_per_net_scoped.txt','4L':H/'logs/all69_scoped_TOP_trial_4L_b018_01/all69_per_net_scoped.txt'}
result={}
for v,p in logs.items():
 s=p.read_text(encoding='utf8');rows=re.findall(r'(?:ALL69|NON_USB_65)_NET_RESULT name="([^"]+)" result=(\d+)',s);begins=re.findall(r'(?:ALL69|NON_USB_65)_NET_BEGIN name="([^"]+)"',s)
 assert len(rows)==65 and len({x[0] for x in rows})==65
 zero=[n for n,c in rows if int(c)==0];bad={n:int(c) for n,c in rows if int(c)!=0};notreturned=[n for n in begins if n not in dict(rows)]
 assert len(zero)==61 and bad=={'BOOT0':2,'GPIO_PA15':2,'GPIO_PB4':2,'I2C_SCL':2},bad
 assert notreturned==(['USB_DP'] if v=='4L' else [])
 result[v]={'log':str(p),'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'began':len(begins),'completed':65,'zeroCount':len(zero),'zeroNetworks':zero,'nonzeroNetworks':bad,'nonzeroDRCTotal':sum(bad.values()),'beganWithoutResult':notreturned,'notStartedUSB':(['USB_DM','PA11_SHARED','PA12_SHARED'] if v=='4L' else ['USB_DP','USB_DM','PA11_SHARED','PA12_SHARED']),'scope':'per-net normal scoped only, not whole-board or batch-only'}
out=H/'review/b018_scoped_full_log_independent_audit.json';out.write_text(json.dumps(result,indent=2)+'\n',encoding='utf8')
B=H/'backups/b018_report_correction_full_log';B.mkdir(parents=True,exist_ok=True)
for p in [R/'EDA.md',R/'learning/notes/lessonHI_38_50_20261021.md',H/'learning_operation_guide.md',H/'review/progress_record_20261022_0626.json']:
 t=B/p.name
 if not t.exists():shutil.copy2(p,t)
p=R/'EDA.md';s=p.read_text(encoding='utf8');old='4L 65\u7f51\u4e3a0\u3001USB_DP\u5185\u90e8\u6c42\u89e3\u5668\u963b\u585e\u3001\u53e63\u7f51\u672a\u68c0\u67e5';assert old in s;s=s.replace(old,D['fix']);p.write_text(s,encoding='utf8')
p=R/'learning/notes/lessonHI_38_50_20261021.md';s=p.read_text(encoding='utf8')
s=s.replace('4L 65\u7f51\u4e3a0\uff0cUSB_DP\u89e6\u53d1',D['bannerFix'])
s=s.replace('4L\u540c65\u7f51\u5168\u90e80\uff1b\u5230USB_DP\u65f6',D['histFix'])
s+=D['note'];p.write_text(s,encoding='utf8')
p=H/'learning_operation_guide.md';s=p.read_text(encoding='utf8');s=s.replace('4L65\u7f51\u4e3a0\u3001USB_DP\u6c42\u89e3\u963b\u585e/3\u7f51\u672a\u8bd5',D['guideFix']);p.write_text(s,encoding='utf8')
p=H/'review/progress_record_20261022_0626.json';a=json.loads(p.read_text(encoding='utf8'))
a['variants']['4L']['scopedResult']['zeroNetworks']=61;a['variants']['4L']['scopedResult']['failingNetworks']=['BOOT0','GPIO_PA15','GPIO_PB4','I2C_SCL'];a['independentFullLogAudit']=out.name;a['correction']='Previous 4L65zero summary rejected; full65 records prove61zero and4nonzero, source logs unchanged.'
p.write_text(json.dumps(a,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
print(json.dumps({v:{k:a[k] for k in ['began','completed','zeroCount','nonzeroNetworks','beganWithoutResult','notStartedUSB']} for v,a in result.items()}))
