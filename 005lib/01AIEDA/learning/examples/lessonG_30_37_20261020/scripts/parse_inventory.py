from pathlib import Path
import re,json,csv,hashlib
R=Path(r'D:\001DIY\005lib\01AIEDA\learning\examples\lessonG_30_37_20261020')
def sx(s):
 t=re.findall(r'"(?:\\.|[^"\\])*"|\(|\)|[^\s()]+',s);i=0
 def take():
  nonlocal i
  v=t[i];i+=1
  if v=='(':
   a=[]
   while t[i]!=')':a.append(take())
   i+=1;return a
  if v.startswith('"'):return json.loads(v)
  if v=='nil':return None
  if v=='t':return True
  try:return float(v)
  except ValueError:return v
 return take()
def rows(p):return list(csv.DictReader(p.open(encoding='utf8'),delimiter='\t',quotechar='\0'))
def sh(p):return hashlib.sha256(p.read_bytes()).hexdigest().upper()
de=json.loads((R/'source/integrated_circuit.json').read_text());metadata={x['ref']:x for x in de['components']}
for kind in ['4L','2L']:
 B=R/f'logs/inventory_{kind}'
 launch=json.loads((B/'launch.json').read_text())
 assert launch['exitCode']==0 and launch['beforeSHA256']==launch['afterSHA256']
 assert 'G_INVENTORY_COMPLETE' in (B/'g_inventory_summary.txt').read_text()
 assert '*Error*' not in (B/'stdout.txt').read_text()
 defs={}
 for x in rows(B/'g_package_definitions.tsv'):
  name=sx(x['package']);defs[name]={'package':name,'bodyExtent':sx(x['bodyExtent']),'bbox':sx(x['bbox']),'localPins':[],'geometry':[]}
 for x in rows(B/'g_package_pins.tsv'):
  defs[sx(x['package'])]['localPins'].append({k:sx(v) for k,v in x.items() if k!='package'})
 for x in rows(B/'g_package_geometry.tsv'):
  defs[sx(x['package'])]['geometry'].append({k:sx(v) for k,v in x.items() if k!='package'})
 actual={sx(x['refdes']):{k:sx(v) for k,v in x.items() if k!='refdes'} for x in rows(B/'g_actual_symbols.tsv')}
 pinrows=rows(B/'component_pins.tsv')
 components=[]
 for x in rows(B/'components.tsv'):
  ref=x['refdes'];meta=metadata[ref];pack=x['package']
  pins=[]
  for p in pinrows:
   if p['refdes']!=ref:continue
   number=p['pin'];local=next((z for z in defs[pack]['localPins'] if str(z['pin'])==number and z['layer']=='ETCH/TOP'),None)
   assert local is not None,(ref,number,pack)
   pins.append({'number':number,'net':p['net'] or None,'pinName':next((z['name'] for z in de['models'][meta['model']]['pins'] if z['number']==number),None),'localXY':local['xy'],'localRotation':local['rotation'],'padstack':local['padstack'],'copperFigure':local['figure'],'regularPadBBox':local['padbbox']})
  components.append({'ref':ref,'package':pack,'model':meta['model'],'value':meta.get('value'),'sourceMetadata':meta,'placed':x['placed']=='t','placement':actual.get(ref),'bodyExtent':defs[pack]['bodyExtent'],'logicalPins':pins})
 assert len(components)==80 and sum(len(x['logicalPins']) for x in components)==272
 result={'status':'PASS_NATIVE_READONLY_INVENTORY','sourceBoard':str(R/f'backups/G_{kind}_INPUT.brd'),'sourceSHA256':launch['afterSHA256'],'components':components,'packages':defs,'actualSymbols':actual,'scope':'Native package origin geometry from official axlLoadSymbol in memory only; unplaced parts have null absolute placement. Pin net assignments from native component pins; metadata from DE source. Library load rounded-value warning retained in stdout; values below are actual native results.'}
 (R/f'inventory/inventory_{kind}.json').write_text(json.dumps(result,indent=2),encoding='utf8')
 out=R/f'inventory/all_component_local_pins_{kind}.tsv'
 with out.open('w',newline='',encoding='utf8') as f:
  wr=csv.writer(f,delimiter='\t');wr.writerow(['ref','model','value','package','pin','pinName','net','localX','localY','localRotation','padstack','regularPadBBox'])
  for c in components:
   for p in c['logicalPins']:wr.writerow([c['ref'],c['model'],c['value'],c['package'],p['number'],p['pinName'],p['net'],*p['localXY'],p['localRotation'],p['padstack'],json.dumps(p['regularPadBBox'])])
 print(kind,len(components),len(defs),len(pinrows),out)
print('G_NATIVE_INVENTORY_JSON_COMPLETE')
