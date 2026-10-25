from pathlib import Path
import json
R=Path(r'D:\001DIY\005lib\01AIEDA\learning\examples\lessonHI_38_50_20261021')
tag='reopen_usb_esd_2L_b008_bulk';out=(R/'logs'/tag).as_posix()
code=r'''
procedure(hiUSBLengthChallenge()
 let((f ec base)
  f=outfile("@OUT@/hi_usb_native_length_challenges.txt")
  ec="HI_E_USB_CONNECTOR_2L" base="HI2L_E_USB_BUDGET"
  fprintf(f "BASELINE_CONNECTOR_ALL=%L\nBASELINE_SHARED_ALL=%L\n" axlCNSEcsetValueGet(ec 'all t) axlCNSEcsetValueGet(base 'all t))
  unwindProtect(
   progn(
    unless(axlCNSEcsetValueSet(ec 'Differential_Pair_Phase_Tolerance "3 MM") error("Cannot tighten connector phase\n"))
    axlDRCUpdate(t) axlDBRefreshId(nil) f29DumpDRC(f "CONNECTOR_PHASE_STRICT_3MM")
    unless(setof(d axlDBGetDesign()->drcs equal(d->name "Differential Pair Phase Tolerance")) error("Native connector phase challenge failed to trigger\n"))
    unless(axlCNSEcsetValueSet(ec 'Differential_Pair_Phase_Tolerance "4 MM") error("Cannot restore connector phase\n"))
    unless(axlCNSEcsetValueSet(base 'Differential_Pair_Max_Uncoupled_Length "1 MM") error("Cannot tighten shared uncoupled budget\n"))
    axlDRCUpdate(t) axlDBRefreshId(nil) f29DumpDRC(f "SHARED_UNCOUPLED_STRICT_1MM")
    unless(setof(d axlDBGetDesign()->drcs equal(d->name "Differential Pair Max Uncoupled Length")) error("Native uncoupled challenge failed to trigger\n"))
    t)
   progn(
    axlCNSEcsetValueSet(ec 'Differential_Pair_Phase_Tolerance "4 MM")
    axlCNSEcsetValueSet(base 'Differential_Pair_Max_Uncoupled_Length "6 MM")))
  axlDRCUpdate(t) axlDBRefreshId(nil) f29DumpDRC(f "USB_NATIVE_BUDGETS_RESTORED")
  unless(length(axlDBGetDesign()->drcs)==0 && axlDBControl('drcEnable) error("USB length challenge restoration not clean\n"))
  fprintf(f "RESTORED_CONNECTOR_ALL=%L\nRESTORED_SHARED_ALL=%L\n" axlCNSEcsetValueGet(ec 'all t) axlCNSEcsetValueGet(base 'all t))
  fprintf(f "HI_USB_NATIVE_LENGTH_CHALLENGES_COMPLETE_NO_SAVE\n") close(f) t))
'''.replace('@OUT@',out)
p=R/f'scripts/{tag}_length_challenge.il';p.write_text(code,encoding='ascii')
p=R/f'scripts/{tag}.scr';s=p.read_text();s=s.replace('quit\n','skill errset(load('+json.dumps((R/f'scripts/{tag}_length_challenge.il').as_posix())+') t)\nskill errset(hiUSBLengthChallenge() t)\nquit\n');p.write_text(s,encoding='ascii')
print('prepared native phase/uncoupled strict challenges, restore, noSave')
