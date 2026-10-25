from pathlib import Path
R=Path(r'D:\001DIY\005lib\01AIEDA\learning\examples\lessonHI_38_50_20261021\engineering_power')
s=(R/'scripts/review_power02d.py').read_text().replace('import json,math,csv,hashlib,sys,shutil','import json,math,csv,hashlib,sys,shutil,re')
s=s.replace("'power_paths_02d.json']]","'power_paths_02d.json','power_star_03c.json']]")
s=s.replace("b002d","b003c").replace("native_power02d_","native_power03c_").replace("review_power02d","review_power03c").replace("evidence_power02d","evidence_power03c")
s=s.replace("POWER02D","POWER03C").replace("24freshEndpointProofs","10freshEndpointProofs").replace("==24 and'actual=nil'","==10 and'actual=nil'").replace(".142remaining",".137remaining").replace("NATIVE_REMAINING_CONNECTIONS=142","NATIVE_REMAINING_CONNECTIONS=137")
insert=""" # Compare actual region copies against their actual base source, not proposed class names.
 def params(row):
  d={}
  for k,v in re.findall(r'\\((\\w+) ([^()]*)\\)',row):
   v=v.strip()
   if v=='nil':d[k]=None
   elif v=='t':d[k]=True
   elif v.startswith('"'):d[k]=json.loads(v)
   else:
    try:d[k]=float(v)
    except ValueError:d[k]=v
  return d
 pv={(q['cset'],q['layer']):params(q['values']) for q in csv.DictReader((rb/'physical_csets.tsv').read_text().splitlines(),delimiter='\\t')}
 sv={(q['cset'],q['layer']):params(q['values']) for q in csv.DictReader((rb/'spacing_csets.tsv').read_text().splitlines(),delimiter='\\t')}
 for n in ['physical_csets.tsv','spacing_csets.tsv','hi_rules_context.tsv']:record(rb/n)
 bm=json.loads((cp/'base_net_rules.json').read_text())['rules'];by={(x['net'],x['layer']):x for x in bm}
 for reg,limit in [('HI_U1_INNER_LEFT',1.4),('HI_U1_INNER_SOUTH',1.4),('HI_U1_INNER_NE',1.5)]:
  actual=pv[(reg+'_P_'+variant,'TOP')];source=pv[(by[('V3V3','TOP')]['physicalCSet'],'TOP')].copy()
  source['necklength_max']=limit
  check(variant+'.regionExactPhysical.'+reg,actual==source,dict(actual=actual,expected=source))
  for role,net in [('POWER','V3V3')]+([('GROUND','GND')] if variant=='2L' else[]):
   actual=sv[(reg+'_S_'+role+'_'+variant,'TOP')];source=sv[(by[(net,'TOP')]['spacingCSet'],'TOP')].copy()
   source['smdpin_line']=.2;source['line_line']=.2
   check(variant+'.regionExactSpacing.'+reg+'.'+role,actual==source,dict(actual=actual,expected=source))
  raw=(rb/'hi_rules_context.tsv').read_text()
  check(variant+'.regionBinding.'+reg,reg+'_P_'+variant in raw and reg+'_S_POWER_'+variant in raw)
 # 4LGND/V3 share spacingclass and localPOWERcopy covers both;2L actualseparatesGROUNDcopy.
 if variant=='4L':check('4L.GNDandV3spacingShareDomain',by[('GND','TOP')]['spacingClass']==by[('V3V3','TOP')]['spacingClass'])
"""
pos=s.index("out=dict(")
s=s[:pos]+insert+s[pos:]
s=s.replace("Fixed02d checkpoints only, before03star/MCU/USB/ordinarysignals.","Fixed03c checkpoints only, aftermainstar beforeMCU/USB/ordinarysignals.")
s=s.replace("INPUT_BUCK_LDO_FEEDBACK_ONLY_NOT_FINAL_ROUTED_BOARD","INPUT_BUCK_LDO_FEEDBACK_STAR_ONLY_NOT_FINAL_ROUTED_BOARD")
s=s.replace("necks_mm={'VIN_U2':.95,'U2_GND':.6,'SW_U2':1.15,'BOOT_U2':.6}","necks_mm={'VIN_U2':.95,'U2_GND':.6,'SW_U2':1.15,'BOOT_U2':.6,'newInner24_36_48':1.25,'newVBAT':1.453553,'existingG31outward':1.365685}")
(R/'scripts/review_power03c.py').write_text(s)
print('prepared03creview')
