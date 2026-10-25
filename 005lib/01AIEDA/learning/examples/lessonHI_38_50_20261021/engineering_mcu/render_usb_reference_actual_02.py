import pathlib,json,sys,math
R=pathlib.Path(r"D:\001DIY\005lib\01AIEDA\learning\examples\lessonHI_38_50_20261021\engineering_mcu");H=R.parent
sys.path.insert(0,str(H/"tooling/packages"));sys.path.insert(0,str(R));sys.path.insert(0,str(R.parents[2]/"tools/pymupdf_1_28_2"))
from shapely.geometry import box,LineString,Point
from shapely import affinity
from review_usb_native_paths import copper_ground
import pymupdf as fitz
n=json.loads((H/"inventory/checkpoints/usb_esd_2L_b008_bulk/normalized.json").read_text(encoding="utf-8"));logs=pathlib.Path(n["readbackDirectory"]);parts=['<svg xmlns="http://www.w3.org/2000/svg" width="1100" height="560" viewBox="0 0 1100 560"><rect width="1100" height="560" fill="white"/><text x="25" y="28" font-family="Arial" font-size="19">USB 2L: actual reference copper and available return corridors</text><text x="25" y="50" font-family="Arial" font-size="13">Formal USB8 checkpoint; final whole board must be rechecked. Not an SI/impedance result.</text>']
def drawpanel(xmin,ymin,xmax,ymax,left,top,label,layer,corridors):
 scale=68;ground,_=copper_ground(n,logs,layer);clip=box(xmin,ymin,xmax,ymax);xf=[scale,0,0,-scale,left-scale*xmin,top+scale*ymax]
 def screen(sh):return affinity.affine_transform(sh,xf)
 parts.append(f'<text x="{left}" y="{top-12}" font-family="Arial" font-size="15">{label}</text>')
 parts.append(f'<rect x="{left}" y="{top}" width="{(xmax-xmin)*scale}" height="{(ymax-ymin)*scale}" fill="#f8f8f8" stroke="#888"/>')
 parts.append(screen(ground.intersection(clip)).svg(fill_color="#b8d9bc").replace('stroke="#555555"','stroke="#53985b"').replace('stroke-width="2.0"','stroke-width="0.4"'))
 for c in corridors:
  sh=screen(LineString(c).buffer(.2 if layer=="TOP" else.15,quad_segs=32))
  parts.append(sh.svg(fill_color="#f7bd45").replace('stroke-width="2.0"','stroke-width="0.5"'))
 for z in n["routes"]:
  if z["net"] not in("USB_DP","USB_DM","USB_VBUS") or not z["layer"].endswith("BOTTOM" if layer=="TOP" else"TOP"):continue
  sh=LineString(z["startEnd"]).buffer(z["width"]/2,quad_segs=32).intersection(clip)
  if not sh.is_empty:
   color={"USB_DP":"#7039ad","USB_DM":"#2583b0","USB_VBUS":"#c44a30"}[z["net"]]
   parts.append(screen(sh).svg(fill_color=color).replace('stroke-width="2.0"','stroke-width="0.5"'))
 for via in n["vias"]:
  if not clip.covers(Point(via["xy"])):continue
  color="#39743f" if via["net"]=="GND" else"#7039ad" if via["net"]=="USB_DP" else"#c44a30"
  parts.append(screen(Point(via["xy"]).buffer(.15,quad_segs=48)).svg(fill_color="white").replace('stroke="#555555"',f'stroke="{color}"').replace('stroke-width="2.0"','stroke-width="1.2"'))
drawpanel(37.6,4.2,42.3,7.2,35,95,"TOP GND reference / BOTTOM DP mirror","TOP",[[[39.75,4.9],[38.9,4.9],[38.15,5.8]],[[40.75,4.9],[41.3,4.9],[41.7,5.8]]])
drawpanel(38.8,8.0,44.0,11.5,520,95,"BOTTOM GND reference / TOP DP entry","BOTTOM",[[[40.7,8.4],[39.4,8.4],[39.4,10.1],[41.2,10.1]]])
parts.append('<text x="35" y="375" font-family="Arial" font-size="14">Green: actual GND copper. Gold: verified available GND corridor.</text><text x="35" y="398" font-family="Arial" font-size="14">Purple/blue: projected DP/DM from opposite signal layer. White: holes / reference voids. Orange: VBUS via pads.</text><text x="35" y="425" font-family="Arial" font-size="14">Mirror: 1.0 mm planar bridge has no direct vertical plane cover at the via antipads.</text><text x="35" y="448" font-family="Arial" font-size="14">ESD VBUS bottom crossing: DP reference gap 1.34262 mm; a 0.30 mm copper corridor goes around it.</text><text x="35" y="486" font-family="Arial" font-size="13">Corridors demonstrate available copper only; HF current is not constrained to these drawn polylines.</text></svg>')
svg=''.join(parts);sp=R/"review/usb_reference_return_actual_02.svg";sp.write_text(svg,encoding="utf-8")
doc=fitz.open(stream=svg.encode(),filetype="svg");pix=doc.get_page_pixmap(0,alpha=False);pix.save(R/"review/usb_reference_return_actual_02.png")
print("rendered",sp)
