from pathlib import Path
import json,math
R=Path(r'D:\001DIY\005lib\01AIEDA\learning\examples\lessonHI_38_50_20261021\engineering_power')
ops=[]
def rt(i,p,f,t,purpose,layer='TOP'):
 ops.append(dict(type='route',id=i,net='V3V3',layer=layer,points=p,widths=[.6]*(len(p)-1),**{'from':f,'to':t,'purpose':purpose,'length_mm':sum(math.dist(a,b) for a,b in zip(p,p[1:]))}))
rt('V3_PERIPH_SOURCE',[[33.3,24],[33.3,22.5]],'STAR_BOTTOM_FEED','V_HI_PERIPH_SOURCE','Take off .6 main C9 distribution before allMCUpadescapes. ThisbranchcarriesCANandheaderloads independently.','BOTTOM')
ops.append(dict(type='via',id='V_HI_PERIPH_SOURCE',net='V3V3',xy=[33.3,22.5],padstack='L28_VIA030_C060',purpose='Offpad .3/.6 via, linksmainBOTTOM.6supply toTOPperimeter.'))
rt('V3_PERIPH_SOUTH',[[33.3,22.5],[33.3,1],[76.8,1],[78.2,2.4]],'V_HI_PERIPH_SOURCE','V3_PERIM_EAST_LOW','TOPperimeter supply leavesSPIx7..35/y27..36 entirelyfree. y1 belowUSBshell copper; actualedge/keepinverify.')
rt('V3_PERIPH_EAST',[[78.2,2.4],[78.2,58.2]],'V3_PERIM_EAST_LOW','V3_PERIM_EAST_HIGH','Outsideallrightheadercontacts butinside board/mountingkeepouts; digitaltracesenterfromleft.')
rt('V3_PERIPH_NORTH',[[78.2,58.2],[1.8,58.2]],'V3_PERIM_EAST_HIGH','V3_PERIM_WEST_HIGH','Outsidey55GPIOheaderrow, noTOP3VrailthroughHSE/MCUfanout.')
rt('V3_PERIPH_WEST_J6',[[1.8,58.2],[1.8,26],[7,26]],'V3_PERIM_WEST_HIGH','J6.1','J6supplyapproachesfromy26; SPI source/headercorridorx7..35/y27..36 reserved forsignals.')
rt('V3_J4',[[78.2,28.81],[74,28.81]],'V3_PERIPH_EAST','J4.1','ShortbranchtoUARTconnectorV3pin, no fine neck.')
rt('V3_J5',[[78.2,42.81],[74,42.81]],'V3_PERIPH_EAST','J5.1','ShortbranchtoI2CconnectorV3pin.')
for ref,x in [('J11',9.11),('J12',31.11),('J13',53.11)]:
 rt('V3_'+ref,[[x,58.2],[x,55]],'V3_PERIPH_NORTH',ref+'.1','GPIOheaderV3 shortnorthbranch; no routebetween.6line/.3space andadjacent2.54mmordinarypads.')
rt('V3_CAN_MAIN',[[60.5,1],[60.5,12.76],[59.8,13.46]],'V3_PERIPH_SOUTH','C12.1','DedicatedCAN60mAbranchtodecouplingbank C12/C11/U5; no currentthroughMCUdecapneck.')
rt('V3_SPI_NSS_PULLUP',[[33.3,22.5],[33.5748,22.2252],[33.5748,21]],'V_HI_PERIPH_SOURCE','R25.1','NSSpullup only, noSPIclocksource orderchange.')
rt('V3_USB_AUX_R9',[[59.8,13.46],[56.2,13.46],[56.2,13.1016]],'C12.1','R9.1','VBUSdetectoroutputpullup fedV3, notUSBVBUS.')
rt('V3_USB_AUX_Q2',[[56.2,13.46],[53.8,13.46],[53.8,10.73],[49.9,10.73],[49.9,12.2282],[48.9525,12.2282]],'V3_USB_AUX_R9','Q2.2','.6V3corridorbetweenQ1source/gateanddrain, tightestnominalcoppergap.3018 tolowerrow. AvoidshortingVBUSdrain/gate.')
rt('V3_USB_ATTACH_PULLUP',[[49.9,12.2282],[49.9,16],[48.6016,16],[48.6016,17.2]],'V3_USB_AUX_Q2','R10.1','Q2defaultoffgatepulluptosource; do not tieR10.2attachcontroltoV3.')
rt('V3_SWD_VTREF',[[48.6016,17.2],[48.6016,18],[50,19.3984],[51,20]],'R10.1','J9.1','SenseonlyVTREF. Probe mustnotpowerrail, TLV755noreverseblocking. Signalroutingmusthonorthissupplycorridor.')
rt('V3_UART_IDLE',[[74,28.81],[72,28.81],[71,27.81],[69.6764,27.81],[69.6764,25]],'J4.1','R18.2','UART_RXidle10kpullup independentofdata source; keepsupplyawayfromadjacentconnectorTX/RXpads.')
rt('V3_BOOT_SERVICE',[[74,28.81],[72.5,30.31],[59,30.31],[57.4916,31.1016],[56.7,31.1016]],'J4.1','R30.1','ApproachR30V3fromsouth/right, neverfromnorththroughBOOT_SERVICEpad2.')
rt('V3_I2C_PULLUPS',[[78.2,47],[56.9252,47],[56.9252,37],[56.9252,35]],'V3_PERIPH_EAST','R19.1','FeedsR20.1andR19.1. Doesnotcrossy55GPIOpads/75,55mountingkeepout. I2Cdata approachfromy<34 beforebranching.')
rt('V3_RESET_PULLUP',[[31.11,55],[31.11,47],[38.1016,47],[38.1016,41.3]],'J12.1','R27.1','OutsideHSEvoidtopedge39.75; .6resetpullupsupplyfromGPIOheaderV3branch, not throughquietisland.')
o=dict(status='CANDIDATE_FULL_V3_PERIPHERAL_DISTRIBUTION_NEEDS_GROUP_SCREEN_NATIVE',
 operations=ops,rules=[],placementChanges=[],
 constraints=['Allroutesnormal.6, noaddedpowerneck exception. Singlemainoffpadvia.3/.6 at33.3,22.5.',
 'Preserveuppercasephysicalnames/fullFilm. 4LnonGNDinnerneverallowed. MostnewpowerTOPaboveactualL2or2Lbottomground.',
 'CANsourceC12positive joinsCAN_local_supply_05; CANH/LR15 useinterface_CAN_routes_04, lattertwofilesmustmerge.',
 'ExternalGPIO+headerscombined10mA. CAN60mA worstallocation, totalnormalboard150mA/Ta0..40C untestedthermal.',
 'R9/Q2/R10/J9 supplynearUSBcontrol, stillnotUSBVBUSpowerrail. Reject anyshort/crossing withUSBcriticalorGNDslot.',
 'NoSPIroutingthroughSW/ADC, noTOPpowerinsideSPIcorridorx7..35/y27..36; J6entersaty26.',
 'Powercorridorscanforceordinarysignals toshortBOTTOMcrossovers; maintainactualGNDreturnandnearGNDstitch, do notsolvebylongthinV3.',
 'ExampleDCresistance usesrhoCu20C1.724e-8ohm-m andnominal35um: .6mm routeR=0.000821ohm/mm; actualCu/temp/via/contact/loadmustconfirm. Notampacitycertification.',
 'Actualminimumline-pad .3018 nearQ1 reliesnativepositions/precision. IfactualDRCflag, reroute .6 orlocalplacementreview; do notgloballyreducepower.3spacing.'
 ],
 expectedNewV3Endpoints=['J4.1','J5.1','J6.1','J9.1','J11.1','J12.1','J13.1','R25.1','R19.1','R20.1','R27.1','R30.1','R9.1','R10.1','R18.2','Q2.2','C12.1'],
 reservedAreas=[dict(polygon=[[.9,.7],[79,.7],[79,2.8],[.9,2.8]],allowedNets=['V3V3','GND'],purpose='Candidateperimeterpowercorridor, mustyieldtoactualUSBconnectorcopper/boardedgechecks, notoverridekeepout.')])
(R/'V3_peripheral_distribution_06.json').write_text(json.dumps(o,indent=2)+'\n',encoding='utf-8')
print('ops',len(ops),'maxroute',max(x.get('length_mm',0) for x in ops))
