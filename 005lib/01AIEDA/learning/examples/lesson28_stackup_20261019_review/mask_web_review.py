import pathlib,json
R=pathlib.Path(r'D:/001DIY/005lib/01AIEDA');B=R/'learning/examples/lesson10_connector_20261018';O=R/'learning/examples/lesson28_stackup_20261019_review'
exec((O/'review28.py').read_text().split("cs=[]")[0])
B=R/'learning/examples/lesson10_connector_20261018'
r=table(B/'logs/reopen_package/pins.tsv')
ms=[a for a in r if a['layer']=='PIN/SOLDERMASK_TOP' and a['padstack']=='L10_USB4105_SMD030X115']
widths=sorted(set(a['w'] for a in ms))
xs=sorted(set(a['x'] for a in ms));pitch=min(b-a for a,b in zip(xs,xs[1:]))
from hashlib import sha256
pa=R/'learning/examples/de_15_26_20261019/library/l10_usb4105_smd030x115.pad';pb=B/'library/l10_usb4105_smd030x115.pad'
result={'basis':'Archived native B10 masks + current DE library identical native pad SHA; no new current-board mask rendering','maskWidths_mm':widths,'minimumPitch_mm':pitch,'nominalWeb_mm':round(pitch-widths[0],9),'OSH_minimumWeb_mm':.1016,'shortfall_mm':round(.1016-(pitch-widths[0]),9),'originalPadSHA256':sha(pb),'DE_libraryPadSHA256':sha(pa),'matchingPadBytes':sha(pa)==sha(pb)}
(O/'mask_web_review.json').write_text(json.dumps(result,indent=2),encoding='utf8')
print(json.dumps(result,indent=2))
