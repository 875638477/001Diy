from pathlib import Path
import json,hashlib,shutil
R=Path(r'D:\001DIY\005lib\01AIEDA\learning\examples\lessonG_30_37_20261020')
D=Path(r'C:\Program0\Cadence\SPB172\share\pcb\examples\skill\DOC\FUNCS')
A=R/'source/official_api';A.mkdir(exist_ok=True)
names=['axlDBCreateSymbol','axlLoadSymbol','axlDBGetSymbolBodyExtent','axlDBRefreshId','axlTransformObject','axlDBCreateGroup','axlDBTransactionStart','axlDBTransactionRollback','axlPathStart','axlPathLine','axlDBCreatePath','axlDBCreateVia','axlDBCreateShape','axlShapeChangeDynamicType','axlShapeDynamicUpdate','axlDBDynamicShapes','axlDBGetShapes','axlPolyFromDB','axlDBGetConnect','axlRegionCreate','axlRegionAdd','axlDBCreateRectangle','axlCnsClassTableCreate','axlCnsClassTableFind','axlCnsList','axlCNSCreate','axlCNSSetPhysical','axlCNSGetPhysical','axlCNSSetSpacing','axlCNSGetSpacing','axlNetClassCreate','axlNetClassAdd','axlNetClassRemove','axlNetClassGet','axlDBAddProp']
manifest=[]
for n in names:
 p=D/(n+'.txt');assert p.is_file(),p;q=A/p.name;shutil.copyfile(p,q);manifest.append({'officialSource':str(p),'copy':str(q),'sha256':hashlib.sha256(q.read_bytes()).hexdigest().upper()})
(A/'api_manifest.json').write_text(json.dumps(manifest,indent=2),encoding='utf8')
shutil.copyfile(R/'plans/placement_plan.json',R/'source/approved_placement_plan.json')
# Add explicit scoped profiles to the permanent report generator.
s=(R/'scripts/validate_nativeG_v2.py').read_text()
needle="inputs=json.loads((R/'source/input_manifest.json').read_text())[:2]"
addition="""boards['2L']['independentRuleProfile']={'defaultWidthMM':.2032,'defaultNeckWidthMM':.2032,'defaultCopperSpacingMM':.16,'localPowerGroundSpacingMM':.2,'powerGroundWidthMM':.6,'powerGroundNeckWidthMM':.25,'powerGroundNeckMaxOutsideRegionMM':1.0,'localEscapeNeckMaxMM':1.4,'approvedVia':'L28_VIA030_C060','scope':'Explicit V3V3/GND demo net rules and 2 new physical classes; source4L class scheme, inner-layer exceptions and USB rules were not copied.'}
boards['4L']['classChanges']={'before':27,'after':28,'newPhysicalClass':'G31_GND_P','member':['GND'],'removedFromPhysicalClass':'NC_POWER_LV_P','unchangedSpacingClass':'NC_POWER_LV_S','unchangedElectricalClass':'NC_POWER_LV_E','retainedNetOverride':'P_GND_PLANE','domainMembershipTotal':207}
"""
assert needle in s;s=s.replace(needle,addition+needle)
(R/'scripts/validate_nativeG_v3.py').write_text(s,encoding='ascii')
print('OFFICIAL_API_SNAPSHOT',len(manifest))
