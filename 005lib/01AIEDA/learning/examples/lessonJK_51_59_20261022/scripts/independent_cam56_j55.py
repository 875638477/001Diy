import pathlib,sys,json,re,csv,warnings,hashlib,math,collections,base64,xml.etree.ElementTree as ET
R=pathlib.Path(r'D:\001DIY\005lib\01AIEDA');J=R/'learning/examples/lessonJK_51_59_20261022';H=R/'learning/examples/lessonHI_38_50_20261021'
sys.path[:0]=[str(J/'tooling/packages'),str(H/'tooling/packages'),str(R/'learning/tools/pymupdf_1_28_2')]
from gerbonara import GerberFile,ExcellonFile
from gerbonara.cam import FileSettings
from gerbonara.utils import MM
from shapely.geometry import Point,LineString,Polygon,GeometryCollection
from shapely.ops import unary_union
import pymupdf
BASE=J/'review/independent_CAM_J55';BASE.mkdir(exist_ok=True)
def dump(p,d):p.write_text(json.dumps(d,ensure_ascii=False,indent=2),encoding='utf8')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def geom_primitive(p):
 a=p.to_arc_poly().approximate_arcs(max_error=.00005)
 if len(a.outline)<3:return GeometryCollection()
 g=Polygon(a.outline)
 if not g.is_valid:g=g.buffer(0)
 return g
def object_geom(o):
 result=GeometryCollection()
 for p in o.to_primitives(unit=MM):
  g=geom_primitive(p);result=result.union(g) if p.polarity_dark else result.difference(g)
 return result
def gerber_geom(g):
 result=GeometryCollection()
 for o in g.objects:
  a=object_geom(o);result=result.union(a) if o.polarity_dark else result.difference(a)
 return result
def raw_nc(p):
 text=p.read_text(encoding='ascii');tools={int(a):float(b) for a,b in re.findall(r'^T(\d+)C([.\d]+)',text,re.M)};tool=None;out=[];xy=[None,None]
 for line in text.splitlines():
  if m:=re.fullmatch(r'T(\d+)',line):tool=int(m[1])
  elif m:=re.fullmatch(r'R(\d+)((?:X-?\d+)?(?:Y-?\d+)?)',line):
   count=int(m[1]);assert tool in tools and all(a is not None for a in xy)
   deltas=[]
   for axis in ['X','Y']:
    c=re.search(axis+r'(-?\d+)',m[2]);deltas.append(int(c[1])/10000 if c else 0)
   for _ in range(count):
    xy=[a+d for a,d in zip(xy,deltas)];out.append((*xy,tools[tool]))
  elif re.fullmatch(r'(?:X-?\d+)?(?:Y-?\d+)?',line) and line:
   assert tool in tools
   for axis,index in [('X',0),('Y',1)]:
    if m:=re.search(axis+r'(-?\d+)',line):
     assert len(m[1].lstrip('-'))==7,(p.name,line)
     xy[index]=int(m[1])/10000
   assert all(a is not None for a in xy),(p.name,line)
   out.append((*xy,tools[tool]))
 assert 'METRIC'in text and re.search(r'^G90$',text,re.M) and text.rstrip().endswith('M30')
 return out,tools
def holekey(z):return tuple(round(x,4) for x in z)
reports={}
for v in ['2L','4L']:
 source=J/f'exports/J55_corrected_{v}_TRAINING_NOT_FOR_FAB'; inventorySource=J/f'exports/native_{v}_TRAINING_NOT_FOR_FAB'; out=BASE/v;out.mkdir(exist_ok=True)
 n=json.loads((H/f'inventory/checkpoints/padentry_{v}_b019_DRC_PENDING/normalized.json').read_text(encoding='utf8'))
 hol=json.loads((J/f'audits/j55_57_{v}_hole_inventory_b019.json').read_text(encoding='utf8'))
 expectedFilm=[]
 for line in (inventorySource/'inventory_before.tsv').read_text(encoding='utf8').splitlines():
  if line.startswith('FILM\t'):expectedFilm.append(line.split('\t')[1])
 files=sorted(source.glob('*.art'));checks=[];issues=[];layers={};rendered=[]
 def ck(name,ok,detail=None):checks.append({'name':name,'pass':bool(ok),'detail':detail})
 ck('Exact complete original Film filenames',sorted(p.stem for p in files)==sorted(expectedFilm),expectedFilm)
 for p in files:
  raw=p.read_text(encoding='ascii')
  with warnings.catch_warnings(record=True) as ws:
   warnings.simplefilter('always');g=GerberFile.open(p)
  layers[p.stem]=g
  name=re.search(r'^G04 Film Name:\s+(.+?)\*$',raw,re.M)
  ck(p.stem+' header Film identity',name and name[1].strip()==p.stem)
  ck(p.stem+' MM and3.6 Gerber format',g.import_settings.unit==MM and g.import_settings.number_format==(3,6))
  inv=next(s for s in (inventorySource/'inventory_before.tsv').read_text(encoding='utf8').splitlines() if s.startswith('FILM\t'+p.stem+'\t'))
  im=re.search(r'groupMembers \(([^)]*)\)',inv);expectedLayers=re.findall(r'"([^"]+)"',im[1])
  actualLayers=re.findall(r'^G04 Layer:\s+(.+?)\*$',raw,re.M)
  ck(p.stem+' header class/subclass mapping',sorted(expectedLayers)==sorted(actualLayers),actualLayers)
  expectedMirror='Yes' if 'mirrored t ' in inv else 'No'
  ck(p.stem+' native Film offset/rotation/mirroring preserved',bool(re.search(r'G04 Offset:\s+\(0.0000 0.0000\)',raw)) and bool(re.search(r'G04 Mirror:\s+'+expectedMirror+r'\*',raw)) and 'G04 Rotation:  0*'in raw,{'expectedMirror':expectedMirror,'scope':'PDFBOTTOM mirrored assembly view is intentional native template option, not mirrored bottom fabrication copper'})
  stats={'file':str(p),'sha256':sha(p),'objectCount':len(g.objects),'objectTypes':dict(collections.Counter(type(o).__name__ for o in g.objects)),'darkObjects':sum(o.polarity_dark for o in g.objects),'clearObjects':sum(not o.polarity_dark for o in g.objects),'boundsMM':g.bounding_box(unit=MM),'warnings':[str(w.message) for w in ws],'headerLayers':actualLayers}
  svg=str(g.to_svg(margin=1,force_bounds=((-1,-1),(81,61)) if not g.objects else None));svgp=out/(p.stem+'.svg');svgp.write_text(svg,encoding='utf8')
  doc=pymupdf.open('svg',svg.encode());doc[0].get_pixmap(matrix=pymupdf.Matrix(3,3)).save(str(svgp.with_suffix('.png')))
  stats['renderSVG']=str(svgp);stats['renderPNG']=str(svgp.with_suffix('.png'));rendered.append((p.stem,svg,stats['objectCount']))
  dump(out/(p.stem+'_metadata.json'),stats)
  if ws:issues.append({'id':'JK56-PARSER-'+p.stem,'kind':'PARSER_WARNING','warnings':stats['warnings']})
 # Outline is exactly the eight native mechanical edges, with original template spelling OUTlie.
 expectedPts=[(2,0),(78,0),(80,2),(80,58),(78,60),(2,60),(0,58),(0,2)]
 outline=layers['OUTlie'];actualEdges=[((o.x1,o.y1),(o.x2,o.y2)) for o in outline.objects if type(o).__name__=='Line']
 edgekey=lambda e:tuple(sorted(tuple(round(x,5) for x in p) for p in e))
 expectEdges=list(zip(expectedPts,expectedPts[1:]+expectedPts[:1]))
 ck('Mechanical outline8edges actual80x60chamfer',collections.Counter(map(edgekey,actualEdges))==collections.Counter(map(edgekey,expectEdges)),{'nominalWidthMM':80,'nominalHeightMM':60,'nominalAreaMM2':Polygon(expectedPts).area,'lineWidthMM':.0025})
 # Independent raw NC and separate Gerbonara file API decode.
 expectedPTH=[(*a['xy'],a['drill']) for a in n['vias']]+[(*a['xy'],a['drill']) for a in hol['electricalDrilledPins'] if a['holeType']=='circle_drill']
 expectedNPTH=[(*a['xy'],a['drillDiameter']) for a in hol['mechanicalNPTH']]
 for plated,expected in [(True,expectedPTH),(False,expectedNPTH)]:
  candidates=[p for p in source.glob('*.drl') if ('-np.'in p.name)==(not plated)];assert len(candidates)==1
  p=candidates[0];rawpoints,tools=raw_nc(p)
  ck(('PTH'if plated else'NPTH')+' exact native circle centre/diameter multiset',collections.Counter(map(holekey,rawpoints))==collections.Counter(map(holekey,expected)),{'actualCount':len(rawpoints),'expectedCount':len(expected),'toolTable':tools})
  raw=p.read_text(encoding='ascii')
  # Gerbonara assumes both indices in Allegro metadata comments are same; actual NC uses global tool ID with local Holesize ordinal.
  removed=[s for s in raw.splitlines() if re.match(r';T\d+ Holesize ',s)]
  sanitized='\n'.join(s for s in raw.splitlines() if not re.match(r';T\d+ Holesize ',s))+'\n'
  derived=out/(p.stem+'_parser_input_METADATA_COMMENTS_ONLY_REMOVED.drl');derived.write_text(sanitized,encoding='ascii')
  with warnings.catch_warnings(record=True) as ws:
   warnings.simplefilter('always');e=ExcellonFile.open(derived,plated=plated,settings=FileSettings(unit=MM,number_format=(3,4),zeros=None))
  decoded=[(o.x,o.y,o.aperture.diameter) for o in e.objects if type(o).__name__=='Flash']
  ck(('PTH'if plated else'NPTH')+' second independent decoder matches unchanged raw commands',collections.Counter(map(holekey,decoded))==collections.Counter(map(holekey,rawpoints)))
  svg=str(e.to_svg(force_bounds=((-1,-1),(81,61))));(out/('PTH.svg'if plated else'NPTH.svg')).write_text(svg,encoding='utf8');rendered.append(('PTH circles'if plated else'NPTH circles',svg,len(decoded)))
  dump(out/('PTH_metadata.json'if plated else'NPTH_metadata.json'),{'originalFile':str(p),'sha256':sha(p),'format':'METRIC ABSOLUTE3.4 no zero suppression','points':rawpoints,'count':len(rawpoints),'removedMetadataComments':removed,'rawMachineCommandsUnchanged':True,'parserInputDerivedCopy':str(derived),'parserWarnings':[str(w.message) for w in ws]})
 issues.append({'id':'JK56-CAM-NPTH-COMMENT','kind':'INDEPENDENT_PARSER_COMPATIBILITY','detail':'Original Cadence NC tool table is global T05/T06; Holesize comments use local1/2. Gerbonara1.6.3 raises mismatching indices on comments. Raw files untouched; independent raw command parse and second parser with only metadata comments removed agree.'})
 routefiles=list(source.glob('*.rou'));assert len(routefiles)==1;rp=routefiles[0]
 with warnings.catch_warnings(record=True) as ws:
  warnings.simplefilter('always');e=ExcellonFile.open(rp,plated=True,settings=FileSettings(unit=MM,number_format=(3,4),zeros=None))
 slots=[]
 expectedSlots=[a for a in hol['electricalDrilledPins'] if a['holeType']=='oval slot']
 for o in e.objects:
  assert type(o).__name__=='Line'
  center=((o.x1+o.x2)/2,(o.y1+o.y2)/2);w=o.aperture.diameter;bb=(abs(o.x2-o.x1)+w,abs(o.y2-o.y1)+w)
  native=next(a for a in expectedSlots if math.dist(a['xy'],center)<.00011)
  maxerr=max(abs(bb[0]-native['drillX']),abs(bb[1]-native['drillY']))
  slots.append({'center':center,'width':w,'finishedBoundsSizeMM':bb,'nativePin':native['refdes']+'.'+native['pin'],'nativeSlotSizeMM':[native['drillX'],native['drillY']],'maxDimensionDifferenceMM':maxerr})
  ck('Plated slot '+native['pin']+' centre/finished size',maxerr<=.00021 and abs(w-native['drill'])<1e-6,slots[-1])
 ck('Exactly4J2 plated slots routed not round-drilled',len(slots)==4)
 svg=str(e.to_svg(force_bounds=((-1,-1),(81,61))));(out/'PLATED_SLOTS.svg').write_text(svg,encoding='utf8');rendered.append(('PLATED slots',svg,len(slots)))
 dump(out/'slot_metadata.json',{'originalFile':str(rp),'sha256':sha(rp),'slots':slots,'warnings':[str(w.message) for w in ws],'note':'G40 cutter compensation cancelled. F1 and G90 placement parser warnings retained; no feed/speed/manufacturing tolerance approval.'})
 # Real mask/paste shapes, not just pad bounding boxes.
 mask=layers['SOLDTOP'];paste=layers['PASTTOP']
 ck('TOP mask278 actual pad/mechanical openings',len(mask.objects)==278,len(mask.objects));ck('TOP stencil211 openings including DNP',len(paste.objects)==211,len(paste.objects))
 maskShapes=[(o,object_geom(o)) for o in mask.objects]
 def opening(ref,num):
  c=next(c for c in n['placements'] if c['ref']==ref);p=next(p for p in c['pins'] if p['number']==num);xy=p['xy']
  a=[(o,g) for o,g in maskShapes if hasattr(o,'x') and math.dist((o.x,o.y),xy)<1e-6];assert len(a)==1,(ref,num,len(a));return a[0][1]
 gaps=[]
 for a,b in [(('C8','2'),('U3','2')),(('C9','2'),('U3','4')),(('U3','2'),('U3','3')),(('J2','A6'),('J2','A7'))]:
  ga=opening(*a);gb=opening(*b);gaps.append({'a':'.'.join(a),'b':'.'.join(b),'actualGerberMaskEdgeDistanceMM':ga.distance(gb),'arcApproximationErrorMM':.00005,'productionAcceptable':None})
 # Expected DNP stencil apertures are explicitly retained in the training output, not silently deleted.
 dnp=[]
 for ref in ['R12','R13']:
  c=next(c for c in n['placements'] if c['ref']==ref)
  for p in c['pins']:
   if p['number']:
    cnt=sum(hasattr(o,'x')and math.dist((o.x,o.y),p['xy'])<1e-6 for o in paste.objects)
    dnp.append({'pin':ref+'.'+p['number'],'openingCount':cnt});ck('DNP '+ref+'.'+p['number']+' stencil disclosed',cnt==1)
 dump(out/'actual_mask_stencil_review.json',{'actualGaps':gaps,'stencilDNPOpenings':dnp,'maskRepresentation':'Dark Gerber features are mask openings under this template convention, not painted resist.','release':'NOT_APPROVED_FAB_CAPABILITY_AND_ASSEMBLY_PROFILE_PENDING'})
 issues.append({'id':'JK56-TEMPLATE-TEXT','kind':'EXPLICIT_TEMPLATE_OUTPUT_SCOPE','detail':'Original SKILTOP Film includes only PACKAGE GEOMETRY/SILKSCREEN_TOP, omits REF DES/SILKSCREEN_TOP. PDFTOP includes assembly REFDES but not COMPONENT VALUE/ASSEMBLY_TOP. Native three-text compliance does not prove those texts appear in template Gerber. Separate companion exports required; original01env untouched.'})
 # Electrical identity cannot be inferred from ordinary RS274X; native Board SHA/route guards remain required.
 issues.append({'id':'JK56-RELEASE','kind':'DESIGN_REMAINS_UNRELEASED','detail':'Seven GPIO joins pending, USB4/full-board DRC incomplete, original native log says DRC_OUT_OF_DATE. Gerber successful decode is not board signoff.'})
 # Contact sheet made only from actual parsed CAM objects.
 cols=3;rows=math.ceil(len(rendered)/cols);chunks=[]
 for i,(label,svg,count) in enumerate(rendered):
  x=(i%cols)*100;y=14+(i//cols)*81
  tile=pymupdf.open('svg',svg.encode());pix=tile[0].get_pixmap(matrix=pymupdf.Matrix(1.8,1.8),alpha=False);uri='data:image/png;base64,'+base64.b64encode(pix.tobytes('png')).decode()
  chunks.append(f'<rect x="{x}" y="{y}" width="100" height="80" fill="white" stroke="#cad2df" stroke-width=".2"/><text x="{x+2}" y="{y+4}" font-size="2.8">{label} - objects {count}</text><image x="{x+1}" y="{y+5}" width="98" height="74" preserveAspectRatio="xMidYMid meet" href="{uri}"/>')

 sheet=f'<svg xmlns="http://www.w3.org/2000/svg" width="300mm" height="{rows*81+15}mm" viewBox="0 0 300 {rows*81+15}"><rect width="300" height="{rows*81+15}" fill="white"/><text x="2" y="5" font-size="3.3">JK56 {v} ACTUAL CAM - TRAINING NOT FOR FAB</text><text x="2" y="10" font-size="2.4">Gerber MM3.6 / NC MM3.4 / top XY view / J55 corrected board, legacy plane roles / warnings and incomplete DRC retained</text>'+''.join(chunks)+'</svg>'
 sp=out/'ACTUAL_CAM_CONTACT_SHEET.svg';sp.write_text(sheet,encoding='utf8');doc=pymupdf.open('svg',sheet.encode());doc[0].get_pixmap(matrix=pymupdf.Matrix(1.1,1.1)).save(str(sp.with_suffix('.png')))
 report={'status':'INDEPENDENT_CAM_FORMAT_AND_SOURCE_MAPPING_REVIEW_NOT_PRODUCTION_RELEASE','variant':v,'scope':'Actual exported J55 corrected training CAM from official Cadence17.2; unchanged routing/holes compared with b019 audit; file parsing/rendering independent using official Gerbonara1.6.3 package.','checks':checks,'passed':sum(c['pass'] for c in checks),'failed':[c for c in checks if not c['pass']],'issues':issues,'filmCount':len(files),'PTHCircleCount':len(expectedPTH),'NPTHCircleCount':len(expectedNPTH),'slotCount':len(slots),'contactSheet':str(sp.with_suffix('.png')),'visualReviewed':False,'wholeBoardDRC':None,'boardConnectionComplete':False,'fourLayerRole':'LEGACY_L2_GND_L3_GND'if v=='4L'else'TOP_BOTTOM','unitsInput':'MM Gerber3.6 and NC3.4 explicitly, not guessed from filename','originalFilesEdited':False}
 dump(out/'report.json',report);reports[v]=report
 print(v,json.dumps({'films':len(files),'checks':len(checks),'pass':report['passed'],'failures':report['failed'],'PTH':len(expectedPTH),'NPTH':len(expectedNPTH),'slots':len(slots),'maskGaps':gaps}))
dump(BASE/'summary.json',reports)
