from pathlib import Path
import json,hashlib,xml.etree.ElementTree as ET
R=Path(r'D:\001DIY\005lib\01AIEDA\learning\examples\lessonHI_38_50_20261021')
S=Path(r'D:\001DIY\005lib\01AIEDA\learning\examples\lesson28_stackup_20261019\native\l28_via030_c060.pxml')
B=R/'native/private_padstacks';B.mkdir(exist_ok=True)
text=S.read_text();text=text.replace('l28_via030_c060','hi_via026_c052_tented').replace('0.300','0.260').replace('0.600','0.520')
p=B/'hi_via026_c052_tented.pxml';p.write_text(text,encoding='utf8')
e=ET.fromstring(text);assert e.findtext('padstackusage')=='VIA';assert e.findtext('drillinfo/slothole/width')=='0.260'
assert [(x.findtext('layer'),x.findtext('width')) for x in e.findall('pad')]==[('BEGIN_LAYER','0.520'),('DEFAULT_INTERNAL','0.520'),('END_LAYER','0.520')]
spec={'status':'PREPARED_NOT_NATIVE_IMPORTED_NOT_APPROVED_IN_ANY_BOARD','name':'hi_via026_c052_tented','purpose':'Small mechanically drilled plated through-via for individually scoped ordinary-digital source escape only; not laser microvia.','source':str(S),'sourceSHA256':hashlib.sha256(S.read_bytes()).hexdigest().upper(),'pxml':str(p),'pxmlSHA256':hashlib.sha256(p.read_bytes()).hexdigest().upper(),'drillMM':0.26,'regularCopperDiameterMM':0.52,'nominalAnnularRingMM':0.13,'padTypes':{'BEGIN_LAYER':{'REGULAR':'CIRCLE .52','ANTIPAD':None,'THERMAL':None},'DEFAULT_INTERNAL':{'REGULAR':'CIRCLE .52','ANTIPAD':None,'THERMAL':None},'END_LAYER':{'REGULAR':'CIRCLE .52','ANTIPAD':None,'THERMAL':None}},'topMask':None,'bottomMask':None,'scope':['Intended for the existing positive-copper dynamic-plane designs. No legacy negative-film antipad/thermal geometry is introduced. Read back actual per-layer REGULAR/ANTIPAD/THERMAL/mask, including actual used via object after import.','NULL mask geometry and current Film missing-aperture setting alone are not fabrication tent reliability or assembly insulation certification.','Both fabrication profiles and exact southern source geometry require engineering confirmation before a local approved-via rule is created. Public libraries/global rules unchanged.','Native import and binary .pad creation deliberately wait for sole Cadence slot to be released.']}
(B/'spec.json').write_text(json.dumps(spec,indent=2),encoding='utf8')
print(json.dumps({'status':spec['status'],'pxml':str(p),'sha256':spec['pxmlSHA256']}))
