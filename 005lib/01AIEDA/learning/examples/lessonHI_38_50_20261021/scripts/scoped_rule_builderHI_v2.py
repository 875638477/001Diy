from pathlib import Path
import json,csv,re,itertools
R=Path(r'D:\001DIY\005lib\01AIEDA\learning\examples\lessonHI_38_50_20261021')
class ScopedRuleBuilder:
 """Build explicit finite rules from actual native baseline tables; no Cadence execution."""
 def __init__(self,variant,baseline_path=None,prefix="HI_JS"):
  self.variant=variant;self.prefix=prefix;self.base=json.loads((Path(baseline_path) if baseline_path else R/f'inventory/base_net_rules_{variant}.json').read_text());self.readback=Path(self.base['sourceDirectory']);self.rules={(x['net'],x['layer']):x for x in self.base['rules']};self.operations=[];self.audit=[];self.serial=0
  src=(R/'scripts/normalize_HI_actual_v4.py').read_text();ns={'re':re,'json':json};exec(src[src.index('def sx('):src.index('symbols=')],ns);self.sx=ns['sx'];self.spacing={};self.physical={};self.tables=[];self.regions=[]
  for typ,target in [('spacing',self.spacing),('physical',self.physical)]:
   for row in csv.DictReader((self.readback/f'{typ}_csets.tsv').open(),delimiter='\t',quotechar='\0'):target[row['cset'],row['layer']]=dict(self.sx(row['values']))
  for row in csv.DictReader((self.readback/'hi_rules_context.tsv').open(),delimiter='\t',quotechar='\0'):
   item={k:(self.sx(v) if v is not None else None) for k,v in row.items()}
   if item['kind']=='TABLE':self.tables.append(item)
   if item['kind']=='REGION':self.regions.append(item)
 def newname(self,kind):
  self.serial+=1;return f'{self.prefix}_{kind}{self.serial:03d}_{self.variant}'
 def members(self,domain,klass):return sorted({r['net'] for r in self.rules.values() if r[domain+'Class']==klass})
 def copy(self,domain,parent,changes,reason):
  name=self.newname('P' if domain=='physical' else 'S');self.operations.append({'type':'csetCopy','domain':domain,'name':name,'copyFrom':parent,'values':changes,'rationale':reason});return name
 def region(self,name,layer,polygon,assignments,requested):
  scope=[]
  for a in assignments:
   scope.append({'class1':a['netClass'],'allClass1NetMembers':self.members(a['domain'],a['netClass']),'class2':a.get('otherNetClass'),'allClass2NetMembers':self.members(a['domain'],a['otherNetClass']) if a.get('otherNetClass') else None,'domain':a['domain'],'cset':a['cset']})
  self.operations.append({'type':'region','id':name,'layer':layer,'polygon':polygon,'assignments':assignments})
  self.audit.append({'region':name,'layer':layer,'polygon':polygon,'engineeringRequestedNets':requested,'actualNativeClassScope':scope,'warning':'Existing class membership is deliberately retained. Every listed class member is subject to this region if its actual copper enters; this is not a per-pin or per-net-only override.'})
 def physical_region(self,name,layer,polygon,nets,changes):
  groups={}
  for net in nets:
   r=self.rules[net,'TOP' if layer not in ['TOP','BOTTOM'] else layer];groups.setdefault((r['physicalClass'],r['physicalCSet']),[]).append(net)
  assignments=[];seen={}
  for (cl,parent),members in groups.items():
   assert cl not in seen or seen[cl]==parent,'Ambiguous direct physical overrides require explicit handling';seen[cl]=parent
   values=dict(changes)
   if 'viasAdd' in values:
    additions=values.pop('viasAdd');old=self.physical[parent,'TOP']['vias'];values['vias']=list(dict.fromkeys([p for p in old.split(':') if p]+additions))
   c=self.copy('physical',parent,values,{'sourceClass':cl,'requestedNets':members,'onlyDelta':list(values),'sourceReadback':str(self.readback)})
   assignments.append({'domain':'physical','netClass':cl,'cset':c})
  self.region(name,layer,polygon,assignments,nets)
 def pair_spacing_copy(self,ca,cb,layer,changes):
  exact=[t for t in self.tables if t['name'] is None and t['data2'] is not None and {t['data1'],t['data2']}=={ca,cb} and t['data3'][1]]
  assert len(exact)<=1,'Duplicate global class-pair source'
  def parent_of(cl):
   rows=[r for r in self.rules.values() if r['spacingClass']==cl and r['layer']==('TOP' if layer not in ['TOP','BOTTOM'] else layer)];sources={r['spacingCSet'] for r in rows};assert len(sources)==1,'Mixed direct-net spacing sources need manual handling';return sources.pop()
  if exact:
   parent=exact[0]['data3'][1];reason={'baseline':'existing global native Class-Class CSet','classes':[ca,cb],'source':parent,'onlyDelta':list(changes)};values=dict(changes)
  else:
   pa,pb=parent_of(ca),parent_of(cb);av,bv=self.spacing[pa,layer],self.spacing[pb,layer];parent=pa;values={}
   # Explicit conservative full-pair baseline; never lower an unrequested spacing field.
   for k,a in av.items():
    b=bv[k]
    if a==b:continue
    assert isinstance(a,(int,float)) and isinstance(b,(int,float)),(k,a,b)
    value=max(a,b)
    if value!=a:values[k]=value
   reason={'baseline':'per-field conservative maximum of two native class CSet values when no explicit global pair exists','classes':[ca,cb],'sourceCSets':[pa,pb],'conservativeBaselineDeltas':dict(values),'onlyEngineeringRelaxedFields':list(changes),'nativeDRCAndScopeReviewRequired':True};values.update(changes)
  return self.copy('spacing',parent,values,reason)
 def spacing_pairs(self,name,layer,polygon,netsA,netsB,changes):
  aa=sorted({self.rules[n,'TOP']['spacingClass'] for n in netsA});bb=sorted({self.rules[n,'TOP']['spacingClass'] for n in netsB});pairs=sorted({tuple(sorted((a,b))) for a in aa for b in bb});assignments=[]
  for ca,cb in pairs:
   c=self.pair_spacing_copy(ca,cb,layer,changes);assignments.append({'domain':'spacing','netClass':ca,'otherNetClass':cb,'cset':c})
  self.region(name,layer,polygon,assignments,sorted(set(netsA+netsB)))
 def via_point_permission(self,name,net,xy,layer,parent):
  r=self.rules[net,'TOP'];old=self.physical[parent,'TOP']['vias'];approved=list(dict.fromkeys([p for p in old.split(':') if p]+['HI_VIA026_C052_TENT']));c=self.copy('physical',parent,{'vias':approved},{'onlyDelta':'approvedVias','net':net,'actualExistingRegionalTemplate':parent,'layer':layer,'xy':xy,'preserve':'All other physical keys and layer permissions are copied unchanged; external neck/spacing scope handled separately.'})
  x,y=xy;polygon=[[round(x-.01,4),round(y-.01,4)],[round(x+.01,4),round(y-.01,4)],[round(x+.01,4),round(y+.01,4)],[round(x-.01,4),round(y+.01,4)]];self.region(name,layer,polygon,[{'domain':'physical','netClass':r['physicalClass'],'cset':c}],[net])
 # This resolver only chooses an existing physical-copy template where the native region source is unambiguous.
 # It never claims to replace native coordinate-dependent DRC evaluation.
 def existing_physical_template_at(self,net,layer,xy):
  import sys
  sys.dont_write_bytecode=True
  sys.path.insert(0,str(R/'tooling/packages'))
  from shapely.geometry import Polygon,Point
  klass=self.rules[net,'TOP']['physicalClass'];candidates=[]
  for reg in self.regions:
   if reg['data1']!='CONSTRAINT REGION/'+layer:continue
   verts=reg['data3'];assert all(abs(v[1])<1e-8 for v in verts),'Curved constraint region requires explicit handling'
   poly=Polygon([v[0] for v in verts])
   if not poly.covers(Point(xy)):continue
   for tbl in self.tables:
    if tbl['name']==reg['name'] and tbl['data1']==klass and tbl['data2'] is None and tbl['data3'][0]:candidates.append((tbl['data3'][0],poly,reg['name']))
  if not candidates:return self.rules[net,'TOP']['physicalCSet'],{'source':'baseNetCSet','net':net,'layer':layer,'xy':xy}
  names={c[0] for c in candidates}
  if len(names)==1:return candidates[0][0],{'source':'existingRegionClass','regions':[c[2] for c in candidates],'net':net,'layer':layer,'xy':xy}
  # Nested regions: an unambiguous geometrically innermost applicable source may be copied.
  inner=[c for c in candidates if all(d[1].covers(c[1]) for d in candidates)]
  if len({c[0] for c in inner})==1:return inner[0][0],{'source':'existingInnermostRegionClass','regions':[c[2] for c in inner],'net':net,'layer':layer,'xy':xy}
  raise ValueError(('Ambiguous overlapping physical templates; do not guess',net,layer,xy,[c[0] for c in candidates]))
