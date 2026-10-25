from pathlib import Path
import json,math
R=Path(r'D:\001DIY\005lib\01AIEDA\learning\examples\lessonHI_38_50_20261021\engineering_power')
ops=[]
old=[[[29.8,30.95],[28.4,32.35]],[[28.4,32.35],[22,32.35]],[[22,32.35],[22,37]]]
for i,p in enumerate(old,1):ops.append(dict(type='deleteSegment',id='RIPUP_PRE_FILTER_OLD_'+str(i),net='V3V3',layer='TOP',points=p,width=.6,purpose='Uniqueactualoldprefiltersegmentdelete, preserveoriginalTOP22,37->R26.1row. No danglingx22stubunderSCK.'))
def rt(i,n,p,w,layer,f,t,purpose):
 ops.append(dict(type='route',id=i,net=n,layer=layer,points=p,widths=[w]*(len(p)-1),**{'from':f,'to':t,'purpose':purpose}))
rt('V3_PREFILTER_SOURCE_TOP','V3V3',[[29.8,30.95],[28.8,31.95]],.6,'TOP','C9.1','V_HI_PREF_A','ShortdirectC9branch beforeanalogRC, avoidsC8V5pad TOPgap.142 ofrejectedallTOPy31.95row.')
ops.append(dict(type='via',id='V_HI_PREF_A',net='V3V3',xy=[28.8,31.95],padstack='L28_VIA030_C060',purpose='Offpad transition lowcurrentprefilterbranch; actualcommonreference below/nearbyGNDstitch.'))
rt('V3_PREFILTER_BOTTOM_ROW','V3V3',[[28.8,31.95],[9,31.95]],.6,'BOTTOM','V_HI_PREF_A','V_HI_PREF_B','Movebranchparallelrow offTOP underSPI SCKy33.05, bottomsame-layer edgegap.70. LowcurrentDCpowerbeforeR26, notMCUmaintrunk.')
ops.append(dict(type='via',id='V_HI_PREF_B',net='V3V3',xy=[9,31.95],padstack='L28_VIA030_C060',purpose='WestofSPIclockcorridorx>=11, avoidsnewTOP x22verticalreferencecut underSCK.'))
rt('V3_PREFILTER_WEST_TOP','V3V3',[[9,31.95],[9,37],[22,37]],.6,'TOP','V_HI_PREF_B','EXISTING_V3_22_37','GooutsideSPIcorridor, joinexisting22,37->R26.1. TOPy37 toJ6NSSy36.16 reference/tracegapfiniteactualreview required.')
ops.append(dict(type='via',id='V_HI_PREF_GND_A',net='GND',xy=[27.5,31.05],padstack='L28_VIA030_C060',purpose='CommonGNDstitch nearC9side transition, offset1.581mm. Coppergap.3708toC9V3outputdiagonal/.30toBOTTOMprefilterrow; finalnativevalidate.'))
ops.append(dict(type='via',id='V_HI_PREF_GND_B',net='GND',xy=[10.2,31.05],padstack='L28_VIA030_C060',purpose='CommonGNDstitchlefttransition offset1.50mm. ConnectfutureTOPreferenceunderSCK toBOTTOMcommonGND, notquietisland.'))
o=dict(status='PREFERRED_PREFILTER_REROUTE_CANDIDATE_AWAIT_COMPLETE_SPI_GROUP_NATIVE',
 operations=ops,rules=[],placementChanges=[],
 prerequisites=['STAR07b andperipheral06b havebeenreconciled; rootmustscreenfinalSPI/MCU/GPIO/USBallfuturecopper.',
 'FreezeSCKBOTTOMpreferredy33.05x11..31 orshortcrossovers. Do notexecuteindependentlybeforeactualSPIplan.',
 'DeleteoldTOPverticalx22inadditiontorow/diagonal sooldstubdoesnotleaveTOPreferencegapunderSCK. Exactunique3segmentmatches required.',
 'RetainTOProw22,37->29.5,37 toR26.1; VDDApostR26/caps/MCU/VSSA unchanged.'],
 engineering=[
 'RejectedallTOPy31.95 wouldhaveonly.142mmtoC8V5padupper31.508, violates.3 eventhoughtrace-tracegap.35.',
 'ShortBOTTOMbridgeleftvia22 wouldstillleavefiniteTOPreferencecrossingx22underSCK. Preferredleftvia9movesTOPverticaloutsideclockcorridor.',
 'BOTTOMpowerrow31.95 andSCK33.05 edgegap=.70; usingSCK32.75 yields.40 but33.05preferredreferencebandbelowADC_INPUTy34.',
 'TOPreferenceunderSCK mustbeactualfilledcommonGND, not justreservedwhitearea. Verifygeneratedshape/OOD/components/minwidthandstripcoverage afterallrouting.',
 'Additional~26mm lowcurrentprefilterwire hasnominalR~.021ohm(Cu20C35um/.6), before10ohmR26/localcaps; notampacityoranalogaccuracycertification.',
 'TOPy37 rowtoSPIheaderNSSy36.16 linegap .44 for.2clocktrace/width.6supply, x9verticaltoJ6padgap>=.93. Nativeallpad/keepinchecks stillrequired.',
 '2LTOP V5/C8pad projections maylocallyinterruptreturnunderBOTTOMprefilterDCrow; giveexplicitcommonGNDstitches, do not callituniformplane. Main concernreleasedTOPreferenceunderfastSPI.',
 'GroundstitchAoffset1.581mm isslightlyabovegeneric1.5reviewtarget, explicitgeometry/currentrole given; notblindclaimwithin1.5.'
 ],
 alternatives=[dict(id='LEFT22_SHORTER',viaB=[22,31.95],disposition='Notpreferred: leavesoneTOPV3verticalreferencecutunderSCKy33.05. Requiresboundedgapengineeringreviewratherthanclaimcontinuousreference.')])
(R/'VDDA_prefilter_reroute_08.json').write_text(json.dumps(o,indent=2)+'\n',encoding='utf-8')
print('ops',len(ops))
