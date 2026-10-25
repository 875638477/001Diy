import pathlib,json,math,sys,html
ROOT=pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT.parents[1]/'tools/pymupdf_1_28_2'))
import fitz
source=pathlib.Path(sys.argv[1]) if len(sys.argv)>1 else ROOT/'plans/placement_plan.json'
d=json.loads(source.read_text(encoding='utf-8-sig'))
items=d.get('placements',d.get('components',[]))
inv=json.loads((ROOT/'inventory/inventory_4L.json').read_text(encoding='utf-8-sig'))
components={c['ref']:c for c in inv['components']}
for item in items:
    if 'x' not in item:item['x'],item['y']=item['xy']
    ref=item['ref'];c=components[ref];rad=math.radians(item.get('rotation',0));ca,sa=math.cos(rad),math.sin(rad)
    def xf(p):return [item['x']+p[0]*ca-p[1]*sa,item['y']+p[0]*sa+p[1]*ca]
    b=c['bodyExtent'];corners=[xf([x,y]) for x in (b[0][0],b[1][0]) for y in (b[0][1],b[1][1])]
    item.setdefault('extent',[[min(p[0] for p in corners),min(p[1] for p in corners)],[max(p[0] for p in corners),max(p[1] for p in corners)]])
    pads=[]
    for p in c['logicalPins']:
        xy=xf(p['localXY']);b=p['regularPadBBox'];pr=0;pc,ps=1,0 # native regularPadBBox already contains local pin rotation
        q=[]
        for xx in (b[0][0],b[1][0]):
            for yy in (b[0][1],b[1][1]):
                q.append(xf([p['localXY'][0]+xx*pc-yy*ps,p['localXY'][1]+xx*ps+yy*pc]))
        pads.append({'number':p['number'],'net':p['net'],'xy':xy,'bbox':[[min(v[0] for v in q),min(v[1] for v in q)],[max(v[0] for v in q),max(v[1] for v in q)]]})
    item['renderPads']=pads
out=ROOT/'review_figures';out.mkdir(exist_ok=True)
status=d.get('status','UNSPECIFIED')

def render(name,region,scale=15):
    x0,y0,x1,y1=region;pad=30;w=(x1-x0)*scale+2*pad;h=(y1-y0)*scale+2*pad+34
    def X(x):return pad+(x-x0)*scale
    def Y(y):return pad+34+(y1-y)*scale
    chunks=[f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">',f'<rect width="100%" height="100%" fill="#101d29"/>',f'<text x="{pad}" y="20" fill="white" font-family="Arial" font-size="13">{html.escape(name)} / {html.escape(status)}</text>',f'<text x="{pad}" y="36" fill="#aac3d0" font-family="Arial" font-size="10">Native geometry + saved poses / TOP copper if present; review labels and board fill are not CAM. mm.</text>']
    chunks.append(f'<defs><clipPath id="view"><rect x="{pad}" y="{pad+34}" width="{(x1-x0)*scale}" height="{(y1-y0)*scale}"/></clipPath></defs><g clip-path="url(#view)">')
    def rect(b,fill,stroke,sw=.1):
        chunks.append(f'<rect x="{X(b[0][0]):.3f}" y="{Y(b[1][1]):.3f}" width="{(b[1][0]-b[0][0])*scale:.3f}" height="{(b[1][1]-b[0][1])*scale:.3f}" fill="{fill}" stroke="{stroke}" stroke-width="{sw*scale:.3f}"/>')
    rect([[0,0],[80,60]],'#173b35','#cad6d0',.12)
    for x in range(0,81,5):chunks.append(f'<path d="M {X(x)} {Y(0)} L {X(x)} {Y(60)}" stroke="#315049" stroke-width=".5"/>')
    for y in range(0,61,5):chunks.append(f'<path d="M {X(0)} {Y(y)} L {X(80)} {Y(y)}" stroke="#315049" stroke-width=".5"/>')
    pts=[(2,0),(78,0),(80,2),(80,58),(78,60),(2,60),(0,58),(0,2)]
    chunks.append('<polygon points="'+' '.join(f'{X(x)},{Y(y)}' for x,y in pts)+'" fill="none" stroke="#e3efee" stroke-width="1.6"/>')
    rect([[10,42],[30,52]],'none','#ee9957',.1)
    chunks.append(f'<text x="{X(10.5)}" y="{Y(50.5)}" fill="#ffbd86" font-size="10" font-family="Arial">height restriction / no parts</text>')
    for x,y in [(5,5),(75,5),(75,55),(5,55)]:
        chunks.append(f'<circle cx="{X(x)}" cy="{Y(y)}" r="{2.5*scale}" fill="none" stroke="#ef7777" stroke-width="1"/>')
        chunks.append(f'<circle cx="{X(x)}" cy="{Y(y)}" r="{scale}" fill="#101d29" stroke="#ddd" stroke-width="1"/>')
    for item in items:
        ref=item['ref'];b=item['extent']
        rect(b,'#244357','#7ecbd4',.065)
        for p in item['renderPads']:
            rect(p['bbox'],'#d7b75b' if p['net'] else '#a99d77','#d7b75b',.02)
            if scale>=40:
                chunks.append(f'<text x="{X(p["xy"][0])}" y="{Y(p["xy"][1])+.1*scale}" fill="#081d29" font-family="Arial" font-size="{max(7,scale*.21):.1f}" text-anchor="middle">{html.escape(p["number"])}</text>')
        xx=(b[0][0]+b[1][0])/2;yy=b[1][1]+.22
        chunks.append(f'<text x="{X(xx)}" y="{Y(yy)}" fill="#f2f8ff" font-family="Arial" font-size="{max(10,min(14,scale*.35)):.1f}" text-anchor="middle">{html.escape(ref)}</text>')
    # Actual top copper and vias, if present in the normalized native snapshot.
    for rt in d.get('routes',[]):
        ends=rt.get('startEnd');width=rt.get('width')
        if rt.get('layer')!='ETCH/TOP' or not ends or len(ends)!=2 or not isinstance(width,(int,float)):continue
        if any(not isinstance(z,(list,tuple)) or len(z)!=2 for z in ends):continue
        color='#6febba' if rt.get('net')=='GND' else '#ff7570'
        chunks.append(f'<path d="M {X(ends[0][0])} {Y(ends[0][1])} L {X(ends[1][0])} {Y(ends[1][1])}" stroke="{color}" stroke-width="{width*scale}" stroke-linecap="round" fill="none"/>')
    for via in d.get('vias',[]):
        x,y=via['xy'];drill=via.get('drill',.3)
        chunks.append(f'<circle cx="{X(x)}" cy="{Y(y)}" r="{.3*scale}" fill="#74e8bc" stroke="#a7f3d2" stroke-width=".8"/>')
        chunks.append(f'<circle cx="{X(x)}" cy="{Y(y)}" r="{drill*.5*scale}" fill="#101d29"/>')
    chunks.append('</g></svg>')
    target=out/(name+'.svg');target.write_text(''.join(chunks),encoding='utf-8')
    doc=fitz.open(stream=target.read_bytes(),filetype='svg');doc[0].get_pixmap(matrix=fitz.Matrix(1.25,1.25)).save(out/(name+'.png'));doc.close()
    print(str(out/(name+'.png')))
render('layout_overview',(0,-1,80,60),15)
render('mcu_decoupling_clock',(28,17,53,43),44)
render('power_lc_input',(3,8,36,32),36)
render('usb_protection',(32,0,51,24),46)