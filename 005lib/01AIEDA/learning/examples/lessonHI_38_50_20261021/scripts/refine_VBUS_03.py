import pathlib,json
h=pathlib.Path(__file__).resolve().parents[1]
for v in ('2L','4L'):
 d=json.loads((h/f'plans/VBUS_entry_{v}_v2.json').read_text(encoding='utf8'))
 if v=='2L':
  for o in d['operations']:
   if o['id']=='VBUS_RIGHT_UNDER_HOUSING':o['points']=[[42.4,7.355],[42.4,6.84],[41.86,6.3],[41.86,3.7]]
   if o['id']=='VBUS_RIGHT_V':o['xy']=[41.86,3.7]
   if o['id']=='VBUS_LEFT_LOW_ROUTE':o['points'][-1]=[41.86,3.7]
   if o['id']=='VBUS_RIGHT_TO_CLAMP':o['points']=[[41.86,3.7],[41.86,8.4],[42.6616,9.2016],[43.8,9.2016]]
 else:
  d['operations']=[o for o in d['operations'] if o['id'] not in ('VBUS_SENSE_V','VBUS_SENSE_TOP','VBUS_SENSE_BOTTOM')]
  d['operations'].append({'type':'route','id':'VBUS_SENSE_DIRECT_TOP','net':'USB_VBUS','layer':'TOP','points':[[42.7,9.2016],[43.3,8.6016],[46,8.6016],[47.6016,7],[49.1016,7]],'width':.4})
  o=next(o for o in d['operations'] if o['id']=='VBUS_RIGHT_ESCAPE');o.pop('width',None);o['points']=[[42.4,7.355],[42.4,7.97],[42.4,8.2],[42.7,8.5],[42.7,9.2016]];o['widths']=[.4,.2,.2,.4]
 (h/f'plans/VBUS_entry_{v}_v3.json').write_text(json.dumps(d,indent=2),encoding='utf8')