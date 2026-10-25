from pathlib import Path
import json,math
R=Path(r'D:\001DIY\005lib\01AIEDA\learning\examples\lessonHI_38_50_20261021\engineering_power')
ops=[]
for i,pts in enumerate([[[30.7,32],[30.7,24]],[[30.7,24],[37,24]]],1):
 ops.append(dict(type='deleteSegment',id='RIPUP_STAR_OLD_'+str(i),net='V3V3',layer='BOTTOM',points=pts,width=.6,purpose='Delete uniqueactualsegment bynet/layer/exactstartEnd(orreverse)/width only; neverdeleteentiremergedpath. Preserveallothercopper.'))
ops.append(dict(type='route',id='STAR_BOTTOM_FEED_DIAGONAL',net='V3V3',layer='BOTTOM',points=[[30.7,32],[37,25.7],[37,24]],widths=[.6,.6],**{'from':'V_HI_V3_SOURCE','to':'V_HI_V3_STAR','purpose':'H45realreroute: oldverticalx30.7 blockedSPIwestheaderescape; diagonal opensx31.65/y27.9 corridor without longMOSI detour.'}))
ops.append(dict(type='route',id='STAR_PERIPH_TAP_TOP',net='V3V3',layer='TOP',points=[[37,24],[33.3,24],[33.3,22.5]],widths=[.6,.6],**{'from':'V_HI_V3_STAR','to':'V3_PERIPH_SOURCE_TOP','purpose':'Peripheralmain .6C9takeofffromstarvia, notMCUpadneck. SameTOP eliminatesproposedsecondvia33.3,22.5 andBOTTOMhorizontalbranch. ActualGND23padgap.30/oldGNDlinegap.325.'}))
ops.append(dict(type='route',id='STAR_DIAG_GROUND_RETURN',net='GND',layer='TOP',points=[[35.75,24.75],[36.45,24.75],[36.65,24.95],[38,24.95]],widths=[.25,.25,.6],**{'from':'U1.23','to':'V_HI_STAR_GND_EAST','purpose':'VSS23 mustescape.25(total .982843)before.6 to avoidadjacentVDD24pad. TOPreturncrossesnewBOTTOMstarverticalx37, linksoldC13groundbridge toactualeast-sidecommonGND.'}))
ops.append(dict(type='via',id='V_HI_STAR_GND_EAST',net='GND',xy=[38,24.95],padstack='L28_VIA030_C060',purpose='EastofnewBOTTOMverticalstar: GNDreturn acrosspowerreferencecut, gap.40 toBOTTOMV3 and.35 toTOPV3bus.'))
o=dict(status='REROUTE_CANDIDATE_NEEDS_FULL_GROUP_SCREEN_NATIVE',operations=ops,rules=[],placementChanges=[],
 prerequisites=['StartfromstableMCU6checkpoint, preserveUSB/ESDintendedroutes andallG31localdecaps.',
 'Exactoldsegmentmatchmustbeunique; logdeleteddbid/net/layer/startEnd/width andparentremainingsegments; ifnotuniquestopbatch.',
 'UseV3_peripheral_distribution_06b, not06 oldBOTTOMtap/via.',
 'Noadditionalneckbudget: GNDnewneck.982843<=1.0. Ifnative mergeswitholdGND.25neck, reportactualandscopedDRC; do notsilentlyrelax.'],
 returnedGroundIntent='2Lnewdiagonalreferencevoid differsfromoldverticalslot. RetainedC13-C9TOPgroundbridge remainsdirectlocalground; addedVSS23->eastviaTOPbridge physicallycrossesnewverticalx37slot. Actualplaneconnectedcomponents/width/detour andGNDnode proofsneedrecheckafterfill.',
 affectedHistoricalClaims=['Old03creview remainsvalidforitsfrozencheckpoint only; not proofnewreroute.',
 'Deleteoldverticalandhorizontalratherthanaddingparallelpowerloop. Allirrelevantcopperandnetlistunchanged.'],
 criticalLengths_mm=dict(newDiagonal=math.dist([30.7,32],[37,25.7]),newVertical=1.7,newGNDNeck=.7+math.sqrt(.2**2+.2**2)))
(R/'STAR_reroute_07.json').write_text(json.dumps(o,indent=2)+'\n',encoding='utf-8')
s=json.loads((R/'V3_peripheral_distribution_06.json').read_text())
s['revision']='06b consumes07TOPtakeoffat33.3,22.5; original06BOTTOMtapandproposedvia removedbeforeexecution'
s['operations']=[x for x in s['operations'] if x['id']not in ['V3_PERIPH_SOURCE','V_HI_PERIPH_SOURCE']]
for op in s['operations']:
 if op.get('from')=='V_HI_PERIPH_SOURCE':op['from']='V3_PERIPH_SOURCE_TOP'
s['constraints'][0]='Allroutesnormal.6, noaddedpowerneck. 07alreadybuildsTOPtakeoff37,24->33.3,24->33.3,22.5; nosecondvia orBOTTOMhorizontalbranch.'
s['prerequisites']=['STAR_reroute_07 actualvalidated andsourceTOPendpoint33.3,22.5 available.']
(R/'V3_peripheral_distribution_06b.json').write_text(json.dumps(s,indent=2)+'\n',encoding='utf-8')
print('STAR07ops',len(ops),'periph06bops',len(s['operations']))
