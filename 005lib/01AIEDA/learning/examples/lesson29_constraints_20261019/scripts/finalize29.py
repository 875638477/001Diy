from pathlib import Path
import json,hashlib,html,sys,re
R=Path(r'D:\001DIY\005lib\01AIEDA\learning\examples\lesson29_constraints_20261019')
s=json.loads((R/'constraint_spec.json').read_text())
s.update(status='APPLIED_SAVED_REOPENED_DRC_CHALLENGE_PROVEN',finalBoard='native/F29_CONSTRAINTS_v3.brd',finalReadback='logs/read_final02',validation='validation.json',finalBoardSHA256=hashlib.sha256((R/'native/F29_CONSTRAINTS_v3.brd').read_bytes()).hexdigest().upper())
s['profile_applicability']='Four-layer lesson28 JLC04161H-7628 target only; not fabrication released. Not the OSH Park2layer profile:0.15mm neck is below that process0.1524mm published minimum.2layer requires separate constraints.'
s['native_classes']={g:{'physical_class':'NC_'+g+'_P','spacing_class':'NC_'+g+'_S','electrical_class':'NC_'+g+'_E','physical_cset':v.get('physical',v.get('physical_cset')),'spacing_cset':v.get('spacing',v.get('spacing_cset')),'members':s['groups'][g]} for g,v in s['native_classes'].items()}
s['exceptions']={'VDDA':{'physical_cset':'P_VDDA_030','reason':'0.30mm analog branch instead of0.60mm power trunk'},'GND':{'physical_cset':'P_GND_PLANE','reason':'Only GND may form copper or connect on L2/L3; other power and signal CSets prohibit interior etch. L2/L3 actual ground copper not yet created.'}}
s['actual_electrical_rules']={'cset':'E_USB_FS_BUDGET','attached_to':['DP_USB_CONNECTOR','DP_USB_MCU_SIDE'],'Maximum_Via_Count':2,'Differential_Pair_Phase_Tolerance':'1 MM','Differential_Pair_Max_Uncoupled_Length':'6 MM','basis':'Explicit teaching/project allocations, not mandatory F103 timing limits. No generic matching or maximum delay on unrelated nets.'}
s['copper_stackup_rule']='TOP-L2-L3-BOTTOM; TOP signal reference L2 GND. L3 is planned GND; bottom traces require actual L3 coverage. At present no ground plane is poured.'
s['formal_exports']={'technology':'exports/F29_RULES.tcf','compare':'exports/techfile_run/compare_techfile.log','full_DCF':'GUI File-Export-Constraints not performed; no fullDCF claimed. Native TSV includes actual class/net/pair mappings.'}
s['validation_counts']={'own':543,'independent_review':'See sibling lesson29_constraints_20261019_review/review_final.json; counters may differ because scopes differ, do not sum.'}
(R/'constraint_spec.json').write_text(json.dumps(s,indent=2),encoding='utf8')
failures=[
{'stage':'build01/reopen01','finding':"NetClassCreate 'all and multi-domain list return groups with all domain flags nil in17.2S045; AddProp returned(nil nil), which is truthy inSKILL, so initialguard was insufficient.",'resolution':'Explicit single domain classes P/S/E per9functional categories; assertNetClassGet+actualproperties, save/reopen69nets3domains. V1 retained rejected.'},
{'stage':'challenge01','finding':'API prose suggested make_axlPadStackPad fordrill data; fieldusage rejected.','resolution':'Installed dbcreate/pad.il correctly usesmake_axlPadStackDrill; corrected source retained.'},
{'stage':'challenge02','finding':'axlNetEcsetValueGet docs name variant rejected stringUSB_DP on this build; transaction auto cancelled.','resolution':'Use actual net dbid; completechallenge04 normalexit0+rollback0/t.'},
{'stage':'challenge03','finding':'Native challenge completion took61s afterlauncher55stimeout; launchreport completedfalse/exitnull is not upgraded tosuccess.','resolution':'No broad processkill. Finalchallenge04 uses120stimeout, actual111s exit0, hashesstable; originaltimeout retained.'},
{'stage':'coupon_package01','finding':'RECTANGLE figure with equal0.2x0.2 dimensions rejectedillegalfigure.','resolution':'UseSQUARE for exactlyequal sides; nativePAD/DRA/PSM savedandcompiled. SPMHUT-48 rounding warning retained.'},
{'stage':'coupon_board02','finding':'Native electricalDRC automaticallyinvokedbem2d; fieldsolution failuresretained, noSI/impedance result accepted.','resolution':'PurelengthDRCactual7.6MM exactlymatchesgeometric20/27.6difference; matched20/20newprocesshash/readbackpassed. Safe stopattempt found processalreadyexited andstoppednothing; no controlledtermination claimed.'},
{'stage':'validator_v1','finding':'CSV reader removedSKILLstringquotes beforeMKS parse; trailingcolon invialist falselytreatedaswrongvalue. net->pins returned0evenwithactual4assignedphysicalpins.','resolution':'Preservequotes, splitcolonlistandfilteremptydelimiter; officialaxlPinsOfNet reports2pins/net withunconnected0, actualpinxy matchesrouteends. Failedvalidator snapshot retained.'}]
(R/'failure_history.json').write_text(json.dumps(failures,indent=2),encoding='utf8')
# Vector preview is generated from verified rules/geometry, not a screen capture.
svg=['<svg xmlns="http://www.w3.org/2000/svg" width="1400" height="1020" viewBox="0 0 1400 1020">','<rect width="1400" height="1020" fill="#f2f5f9"/>','<style>text{font-family:Arial,sans-serif;fill:#1c2b3d} .h{font-size:30px;font-weight:bold}.s{font-size:17px}.c{font-size:19px;font-weight:bold}</style>']
def tx(x,y,t,cl='s',fill=None):
 size={'h':30,'s':17,'c':19}[cl]
 svg.append(f'<text x="{x}" y="{y}" font-family="Arial" font-size="{size}"'+(' font-weight="bold"' if cl in ['h','c'] else '')+(f' fill="{fill}"' if fill else ' fill="#1c2b3d"')+'>'+html.escape(t)+'</text>')
tx(40,50,'Lesson 29 | Persisted PCB constraints','h')
tx(40,82,'F29_CONSTRAINTS_v3 | 80 components / 69 nets / 27 domain classes / 3 differential pairs')
tx(40,110,'543 independent checks PASS. Rule values below are draft allocations for the 4-layer JLC target.')
svg.append('<rect x="30" y="135" width="1340" height="405" rx="12" fill="white"/>')
tx(50,170,'Category / CSet','c');tx(460,170,'Nominal width / neck / max neck','c');tx(940,170,'Applied scope','c')
rs=[('General / P_SIGNAL_020','0.20 / 0.15 / 1.0 mm','TOP + BOTTOM'),
('Power / P_POWER_060','0.60 / 0.25 / 1.0 mm','TOP + BOTTOM'),
('VDDA direct exception','0.30 / 0.20 / 1.0 mm','TOP + BOTTOM'),
('GND / P_GND_PLANE','0.60 / 0.25 / 1.0 mm','L2 + L3 permitted for GND'),
('USB / P_USB_PROVISIONAL','0.20 / 0.15 / 1.0 mm','TOP only; gap 0.15 mm'),
('CAN / P_CAN_025','0.25 / 0.20 / 1.0 mm','TOP + BOTTOM'),
('Class-class spacing','Switch to analog / crystal / USB: 1 mm','Reference continuity still required'),
('Approved via','Drill 0.30 / copper 0.60 mm','One unique GND test via inherited')]
for i,(a,b,c) in enumerate(rs):
 y=209+i*39;tx(50,y,a);tx(460,y,b);tx(940,y,c)
svg.append('<rect x="30" y="565" width="1340" height="190" rx="12" fill="white"/>')
tx(50,602,'Controlled native DRC proofs (all reverted)','c')
tx(50,638,'Neck width: 0.10 < 0.15 mm | Power neck: 10 > 1 mm | Net MIN_LINE_WIDTH override removes violation')
tx(50,670,'Spacing: 0.10 < 0.20 mm | Class-class: 0.50 < 1 mm | USB via count: 3 > 2')
tx(50,702,'Unapproved via rejected on all 4 layers | L2 power cline blocked | L2 GND fill allowed')
tx(50,734,'Rollback: current DRC = 0, state = t. DRC zero is not SI / PI / EMI acceptance.')
svg.append('<rect x="30" y="780" width="1340" height="175" rx="12" fill="white"/>')
tx(50,818,'Separate fully connected length-rule coupon','c')
tx(50,853,'Unbalanced: 20.0 / 27.6 mm -> native phase tolerance error: expected 1, actual 7.6 mm')
tx(50,886,'Balanced: two actual 20.0 mm segments, 4 pin endpoints verified -> current DRC 0 / t')
tx(50,919,'90 ohm target geometry is unconfirmed. No ground plane has been poured. No manufacturing release.')
tx(40,993,'Native data preview, not a Cadence UI screenshot. Full sources, failures, readback and hashes are archived.')
svg.append('</svg>')
out='\n'.join(svg)
(R/'constraint_overview.svg').write_text(out,encoding='utf8')
sys.path.insert(0,r'D:\001DIY\005lib\01AIEDA\learning\tools\pymupdf_1_28_2')
import fitz
doc=fitz.open(stream=out.encode(),filetype='svg')
doc[0].get_pixmap(matrix=fitz.Matrix(1,1)).save(R/'constraint_overview.png')
print('FINAL_SPEC_AND_PREVIEW_READY')
