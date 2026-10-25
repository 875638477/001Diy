import pathlib,json
h=pathlib.Path(__file__).resolve().parents[1]
for v in ('2L','4L'):
 ops=[];proofs=[]
 def r(id,points,w=.4,layer='TOP',widths=None):
  d={'type':'route','id':id,'net':'USB_VBUS','layer':layer,'points':points,'purpose':'Low-current USB VBUS clamp/bypass/sense connection, not a source of board V5; explicit source geometry and actual USB reference review required.'}
  d.update({'widths':widths} if widths else {'width':w});ops.append(d)
 def via(id,xy,net='USB_VBUS'):ops.append({'type':'via','id':id,'net':net,'xy':xy,'padstack':'L28_VIA030_C060'})
 # Common connector-left escape avoids the neighboring SMD ground pad.
 r('VBUS_LEFT_ESCAPE',[[37.6,7.355],[37.6,8.2],[36.9,8.9],[36.9,9.2]])
 via('VBUS_LEFT_V',[36.9,9.2])
 if v=='2L':
  for tag,old,new in [('LEFT',[38.15,5.8],[38.3,5.6]),('RIGHT',[41.7,5.8],[41,4.7])]:
   ops.append({'type':'deleteVia','id':'USB_RETURN_'+tag+'_RIP','net':'GND','xy':old,'padstack':'L28_VIA030_C060','purpose':'Controlled return-stitch relocation for VBUS path clear of both actual alignment drills; old source retained and final USB return corridors must be remeasured.'});via('USB_RETURN_'+tag+'_NEW',new,'GND')
  r('VBUS_LEFT_LOW_ROUTE',[[36.9,9.2],[39,7.1],[39,6.05],[39,5.15],[39,3.7],[41.95,3.7]],layer='BOTTOM',widths=[.4,.4,.2,.4,.4])
  r('VBUS_RIGHT_UNDER_HOUSING',[[42.4,7.355],[42.4,6.75],[41.95,6.3],[41.95,3.7]],widths=[.4,.2,.4])
  via('VBUS_RIGHT_V',[41.95,3.7])
  r('VBUS_RIGHT_TO_CLAMP',[[41.95,3.7],[41.95,8.4],[42.7516,9.2016],[43.8,9.2016]],layer='BOTTOM')
 else:
  r('VBUS_LEFT_LAYER3_REFERENCED_BRIDGE',[[36.9,9.2],[40.15,9.2],[40.25,9.3]],layer='BOTTOM')
  # Four-layer L3 is actual GND; the short lower-copper bridge does not split TOP L2 reference.
  r('VBUS_RIGHT_ESCAPE',[[42.4,7.355],[42.4,8.08],[42.4,8.65],[42.7,8.95],[42.7,9.2016]],widths=[.4,.2,.2,.4])
 # Sense gate divider connection remains a separate low-current branch from C10/ESD.
 via('VBUS_SENSE_V',[47.8,7]);r('VBUS_SENSE_TOP',[[47.8,7],[49.1016,7]])
 r('VBUS_SENSE_BOTTOM',[[43.8,9.2016],[45.5984,9.2016],[47.8,7]],layer='BOTTOM')
 proofs=[{'from':'J2.A4_B9','to':'C10.1','connected':True},{'from':'J2.B4_A9','to':'C10.1','connected':True},{'from':'R7.1','to':'C10.1','connected':True}]
 d={'status':'CANDIDATE_ACTUAL_HOLE_CLEARANCE_AND_NATIVE_PENDING','variant':v,'operations':ops,'proofs':proofs,'scope':'2L consciously uses a longer low-current VBUS path below the connector to preserve DM entrance reference; 4L uses short bridges backed by actual L3 GND. Narrow .2mm necks are finite and must obey inherited1mm max; no net-tie/PIN_SHORT. All housing/tenting/drill/assembly manufacturing checks remain open.'}
 (h/f'plans/VBUS_entry_{v}_v1.json').write_text(json.dumps(d,indent=2),encoding='utf8')