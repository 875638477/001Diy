from pathlib import Path
R=Path(r'D:\001DIY\005lib\01AIEDA\learning\examples\lessonHI_38_50_20261021')
s=(R/'scripts/adapt_usb_esd06aHI.py').read_text().replace('usb_critical_routes_v6.json','usb_critical_routes_v8.json').replace('b006a.json','b008.json')
needle=" sc='NC_USB_FS_S' if v=='4L' else 'HI2L_USB_FS_S'"
s=s.replace(needle,''' constraints.append({'type':'ecsetCopy','name':'HI_E_USB_CONNECTOR_'+v,'copyFrom':'E_USB_FS_BUDGET' if v=='4L' else 'HI2L_E_USB_BUDGET','pair':'DP_USB_CONNECTOR','values':{'Differential_Pair_Phase_Tolerance':'4 MM','Differential_Pair_Max_Uncoupled_Length':'13.5 MM'}})
 if v=='2L':
  constraints.extend([
   {'type':'csetCopy','domain':'spacing','name':'HI_USB_J2_SOURCE_S_2L','copyFrom':'HI2L_S_CLASSCLASS_10','values':{'smdpin_line':'0.2 MM'}},
   {'type':'region','id':'HI_USB_J2_SOURCE_ESCAPE','layer':'TOP','polygon':[[38.95,7.25],[39.55,7.25],[39.55,8.55],[38.95,8.55]],'assignments':[{'domain':'spacing','netClass':'HI2L_USB_FS_S','otherNetClass':'HI2L_USB_AUX_S','cset':'HI_USB_J2_SOURCE_S_2L'}]}
  ])
 sc='NC_USB_FS_S' if v=='4L' else 'HI2L_USB_FS_S' ''')
s=s.replace('Original phase1mm/uncoupled6mm/maxvia2 retained for first native run. Do not silently relax to force zeroDRC.','Original phase1/uncoupled6 failed natively in b006a. USB8 uses reviewed connector-pair-only static ECSet copy phase4mm/uncoupled13.5mm/maxvia2; shared pair original phase1/uncoupled6 unchanged, new DM geometry intended to improve actual coupling. These are explicit planar teaching budgets, not USB specification or SI acceptance.')
(R/'scripts/adapt_usb_esd08HI.py').write_text(s,encoding='ascii')
print('USB8 adapter')
