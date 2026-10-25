import pathlib,json
h=pathlib.Path(__file__).resolve().parents[1]
for v in ('2L','4L'):
 d=json.loads((h/f'plans/VBUS_entry_{v}_v1.json').read_text(encoding='utf8'))
 if v=='4L':
  op=next(o for o in d['operations'] if o['id']=='VBUS_RIGHT_ESCAPE');op.pop('widths',None);op['width']=.4;op['points']=[[42.4,7.355],[42.4,8.2],[42.7,8.5],[42.7,9.2016]]
 (h/f'plans/VBUS_entry_{v}_v2.json').write_text(json.dumps(d,indent=2),encoding='utf8')
 cc=json.loads((h/f'plans/CC_entry_{v}_v3.json').read_text(encoding='utf8'))
 if v=='4L':
  old=next(o for o in cc['operations'] if o['id']=='CC2_ENTRY');old['points']=[[41.75,7.355],[41.75,8.3]]
  cc['operations'] +=[{'type':'via','id':'CC2_ENTRY_V','net':'USB_CC2','xy':[41.75,8.3],'padstack':'L28_VIA030_C060'},{'type':'route','id':'CC2_BOTTOM_CROSSOVER','net':'USB_CC2','layer':'BOTTOM','points':[[41.75,8.3],[41.95,8.5],[44,8.5],[44.7,9.2],[44.7,10.1016]],'width':.2},{'type':'via','id':'CC2_RECEIVER_V','net':'USB_CC2','xy':[44.7,10.1016],'padstack':'L28_VIA030_C060'},{'type':'route','id':'CC2_RECEIVER_TOP','net':'USB_CC2','layer':'TOP','points':[[44.7,10.1016],[45.5,10.1016]],'width':.2}]
  cc['notes'].append('Four-layer CC2 uses a two-via low-speed crossover backed by actual L3; this gives VBUS a short TOP path and avoids adding a reference cut below the DP entrance. Via1.75,8.3 antipad projection must be checked against actual DP entry/ref plane after update.')
 (h/f'plans/CC_entry_{v}_v4.json').write_text(json.dumps(cc,indent=2),encoding='utf8')