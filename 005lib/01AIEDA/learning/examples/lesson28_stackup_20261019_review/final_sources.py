from pathlib import Path
O=Path(r'D:/001DIY/005lib/01AIEDA/learning/examples/lesson28_stackup_20261019_review')
p=O/'review28.py';s=p.read_text()
s=s.replace("webInputs=[", """for src in spec['sources']:
 fp=B/src['file']
 ck('Archived primary source SHA '+fp.name,sha(fp)==src['SHA256'])
 reviewed.append(fp)
gct=B/'source/GCT_USB4105_RevB4_inherited.pdf'
ck('Inherited official GCT drawing SHA preserved',sha(gct)=='FB331FBABEE8392ED2937ED757C1610CB0F174B84625147C0B580A18EEA8C0E5')
reviewed.append(gct)
webInputs=[{'url':'https://gct.co/connector/usb4105','reviewDate':'2026-10-19','role':'Shell Stake Length options; drawing dimension datum independently inspected'}, """)
p.write_text(s)
