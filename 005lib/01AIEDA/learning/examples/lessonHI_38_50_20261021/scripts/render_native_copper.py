"""Reference-copper diagrams from native normalized snapshots, not manufacturing artwork."""
from pathlib import Path
import sys,json,argparse,html,hashlib,math
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'tooling/packages'));sys.path.insert(0,str(R/'engineering_power/scripts'))
from cadence_poly import plane_from_native
A=argparse.ArgumentParser();A.add_argument('--checkpoint',required=True);A.add_argument('--out',required=True);A.add_argument('--layers',default='TOP,BOTTOM');A.add_argument('--bounds',default='0,0,80,60');A.add_argument('--nets',default='');a=A.parse_args()
c=Path(a.checkpoint);s=json.loads((c/'normalized.json').read_text(encoding='utf8'));n=json.loads((c/'networks.json').read_text(encoding='utf8'));layers=a.layers.split(',');picked=set(a.nets.split(',')) if a.nets else None;x0,y0,x1,y1=map(float,a.bounds.split(','));out=Path(a.out).resolve();assert out.is_relative_to(R.resolve())
colors={'GND':'#418d6a','V3V3':'#c32d92','V5':'#dc7926','VIN_RAW':'#ca6b20','VIN_FUSED':'#ca6b20','VIN_PROT':'#bd5321','VDDA':'#b8309c','BUCK_SW':'#db270c','BUCK_BOOT':'#dc691b','BUCK_FB':'#ad592d','USB_DP':'#d024d0','USB_DM':'#256ed8','PA12_SHARED':'#c62a95','PA11_SHARED':'#2992c0','OSC_IN':'#cc3129','OSC_OUT':'#df721d','XTAL_OUT':'#b155a0','ADC0':'#04a3ae','ADC_IN':'#0095a2','NRST':'#a555c4'}
def color(net,layer):return colors.get(net,'#b04034' if layer=='TOP' else '#3777b2')
def title(text):return '<title>'+html.escape(text)+'</title>'
def path(g):
 polys=[g] if g.geom_type=='Polygon' else list(g.geoms);z=[]
 for p in polys:
  for ring in [p.exterior]+list(p.interiors):z.append('M'+' L'.join(f'{x:.5f},{y:.5f}' for x,y in ring.coords)+' Z')
 return ' '.join(z)
w=(x1-x0)*15;h=(y1-y0)*15;parts=[f'<svg xmlns="http://www.w3.org/2000/svg" width="{w:.0f}" height="{h+85:.0f}" viewBox="{x0} {-y1-5.6} {x1-x0} {y1-y0+5.6}">','<rect x="-10" y="-90" width="110" height="110" fill="#f5f5ee"/>',f'<text x="{x0+1}" y="{-y1-3.7}" font-family="sans-serif" font-size="1.1">{html.escape(s["variant"]+" native copper: "+a.layers+" | "+c.name)}</text>',f'<text x="{x0+1}" y="{-y1-2}" font-family="sans-serif" font-size=".7">{html.escape(n.get("sha256",n.get("sourceSHA256","")))}</text>','<g transform="scale(1,-1)">','<path d="M2 0 L78 0 L80 2 L80 58 L78 60 L2 60 L0 58 L0 2 Z" fill="#e5dfcf" stroke="#454b56" stroke-width=".15"/>']
for layer in layers:
 for p in s['planes']:
  if p['layer']!='ETCH/'+layer or (picked and p['net'] not in picked):continue
  q=plane_from_native(dict(p,holes=p.get('holes') or []));parts.append(f'<path d="{path(q)}" fill="{color(p["net"],layer)}" fill-rule="evenodd" opacity=".19" stroke="none">'+title(f'{layer} {p["net"]} filled copper native area {p["area"]} mm²')+'</path>')
for p in s['placements']:
 if p.get('bodyExtent'):
  b=p['bodyExtent']
  if isinstance(b,list) and len(b)==2 and isinstance(b[0],list):parts.append(f'<rect x="{b[0][0]}" y="{b[0][1]}" width="{b[1][0]-b[0][0]}" height="{b[1][1]-b[0][1]}" fill="none" stroke="#777" stroke-width=".05" stroke-dasharray=".3 .15">'+title(p['ref']+' PlaceBound only; not certified component body')+'</rect>')
 for pin in p['pins']:
  if not pin.get('number'):continue
  if picked and pin['net'] not in picked:continue
  b=pin['padBBox'];parts.append(f'<rect x="{b[0][0]}" y="{b[0][1]}" width="{b[1][0]-b[0][0]}" height="{b[1][1]-b[0][1]}" fill="#c3ad49" stroke="#74652a" stroke-width=".025">'+title(p['ref']+'.'+str(pin['number'])+' '+str(pin['net'])+' native pad BBOX approximation')+'</rect>')
 cx,cy=p['xy']
 if x0<=cx<=x1 and y0<=cy<=y1:parts.append(f'<text transform="translate({cx},{cy}) scale(1,-1)" x="0" y="-.2" text-anchor="middle" font-size=".65" font-family="sans-serif" fill="#333">{html.escape(p["ref"])}</text>')
for line in s['routes']:
 layer=line['layer'].removeprefix('ETCH/');net=line['net']
 if layer not in layers or(picked and net not in picked):continue
 pts=line['startEnd'];w=line['width']
 if not w or len(pts)<2:continue
 parts.append(f'<polyline points="'+ ' '.join(f'{x},{y}' for x,y in pts)+f'" fill="none" stroke="{color(net,layer)}" stroke-width="{w}" stroke-linecap="round" stroke-linejoin="round" opacity=".9">'+title(f'{net} {layer} width {w} mm {pts}')+'</polyline>')
for v in s['vias']:
 if picked and v['net'] not in picked:continue
 x,y=v['xy'];pads=[p for p in v.get('pads',[]) if p.get('layer','').removeprefix('ETCH/') in layers];radius=max((max(abs(t) for b in p['bbox'] for t in b) for p in pads),default=.3);parts.append(f'<circle cx="{x}" cy="{y}" r="{radius}" fill="#af9649" stroke="#534520" stroke-width=".03">'+title(f'{v["net"]} via {v["padstack"]} {v["xy"]}')+'</circle>');parts.append(f'<circle cx="{x}" cy="{y}" r="{v["drill"]/2}" fill="#f5f5ee"/>')
for x,y in [(5,5),(75,5),(75,55),(5,55)]:parts.append(f'<circle cx="{x}" cy="{y}" r="1" fill="#f5f5ee" stroke="#777" stroke-width=".05"/><circle cx="{x}" cy="{y}" r="2.5" fill="none" stroke="#777" stroke-width=".05" stroke-dasharray=".4 .2"/>')
parts+=['</g></svg>'];out.parent.mkdir(parents=True,exist_ok=True);out.write_text('\n'.join(parts),encoding='utf8');print(json.dumps({'output':str(out),'checkpoint':str(c),'status':'NATIVE_COPPER_DIAGRAM_NOT_MANUFACTURING_ARTWORK','sha256':hashlib.sha256(out.read_bytes()).hexdigest()}))