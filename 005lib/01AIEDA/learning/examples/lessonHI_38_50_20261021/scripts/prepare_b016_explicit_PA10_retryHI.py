from pathlib import Path
import subprocess,sys
R=Path(r'D:\001DIY\005lib\01AIEDA\learning\examples\lessonHI_38_50_20261021')
head='''hiRipupNormalizationActive=nil
hiRipupAllowedObjects=nil
procedure(hiPrepareExplicitPA10TransientWhitelist(f)
 let((o original other desc)
  hiRipupAllowedObjects=nil
  foreach(pp list(list(list(40.0 20.3) list(40.0 20.5)) list(list(40.0 20.3) list(48.4 20.3)) list(list(48.4 20.3) list(50.1 22.0)) list(list(50.1 22.0) list(50.1 22.4)))
   o=car(hiFindExactManualLine("PA10_UART_RX" "BOTTOM" pp 0.2))
   unless(o error("Explicit PA10 transitional whitelist baseline line absent\\n"))
   original=hiManualLineSignature(o) other=sprintf(nil "%L" list("GND" "ETCH/BOTTOM" pp 0.2)) desc=list("line" pp 0.2)
   hiRipupAllowedObjects=cons(list(o original other desc) hiRipupAllowedObjects))
  foreach(x list(list(list(40.0 20.5) "HI_VIA026_C052_TENT") list(list(50.1 22.4) "L28_VIA030_C060"))
   o=hiUniqueVia("PA10_UART_RX" car(x) cadr(x)) original=sprintf(nil "%L" hiViaIdentity(o)) other=sprintf(nil "%L" list(car(x) cadr(x) "GND")) desc=list("via" car(x) cadr(x))
   hiRipupAllowedObjects=cons(list(o original other desc) hiRipupAllowedObjects))
  fprintf(f "HI_EXPLICIT_TRANSIENT_WHITELIST_PREBOUND_ONLY_SIX=%L\\n" hiRipupAllowedObjects) drain(f) t))
procedure(hiNormalizeExactRipupSignature(o sig)
 let((row)
  row=assoc(o hiRipupAllowedObjects)
  if(hiRipupNormalizationActive && row && equal(sig caddr(row)) then
   fprintf(hiRipupAuditF "HI_EXPLICIT_TRANSIENT_RELABEL_SAME_ORIGINAL_DBID object=%L before=%s after=%s geometryLayerWidthIdentityExact=t\\n" o cadr(row) sig)
   cadr(row)
  else sig)))
procedure(hiVerifyExplicitPA10Restored(f)
 let((d now)
  foreach(row hiRipupAllowedObjects
   d=nth(3 row)
   now=if(equal(car(d) "line") then car(hiFindExactManualLine("PA10_UART_RX" "BOTTOM" cadr(d) caddr(d))) else hiUniqueVia("PA10_UART_RX" cadr(d) caddr(d)))
   unless(now error("Original PA10 bridge object not restored to exact original net+geometry\\n"))
   fprintf(f "HI_EXPLICIT_TRANSIENT_FINAL_RESTORED originalObject=%L actualObject=%L originalDescriptor=%L originalNetPA10=t\\n" car(row) now d))
  fprintf(f "HI_EXPLICIT_TRANSIENT_SIX_OBJECTS_RESTORED_COUNT=%d\\n" length(hiRipupAllowedObjects)) t))
'''
s=(R/'scripts/batchHI_exact_ripup_v3_diagnostic.il').read_text();s=s.replace('sprintf(nil "%L" list(if(o->net then o->net->name else nil) o->layer pp o->width))','hiNormalizeExactRipupSignature(o sprintf(nil "%L" list(if(o->net then o->net->name else nil) o->layer pp o->width)))');s=s.replace('vias=cons(sprintf(nil "%L" hiViaIdentity(o)) vias)','vias=cons(hiNormalizeExactRipupSignature(o sprintf(nil "%L" hiViaIdentity(o))) vias)');s=s.replace('  before=hiExactRipupInventory(nil)','  hiPrepareExplicitPA10TransientWhitelist(f) hiRipupAuditF=f\n  before=hiExactRipupInventory(nil)');s=s.replace('    after=hiExactRipupInventory(nil)','    hiRipupNormalizationActive=t\n    after=hiExactRipupInventory(nil)\n    hiRipupNormalizationActive=nil');s=s.replace('   unless(complete','   progn(hiRipupNormalizationActive=nil\n   unless(complete').replace('equal(before hiExactRipupInventory(nil)))))','equal(before hiExactRipupInventory(nil))))))');(R/'scripts/batchHI_exact_ripup_v4_explicit_PA10.il').write_text(head+s,encoding='ascii')
s=(R/'scripts/compile_batchHI_v30.py').read_text().replace('batchHI_exact_ripup_v3_diagnostic.il','batchHI_exact_ripup_v4_explicit_PA10.il').replace("for check in data.get('postChecks',[]):","statements.append('hiVerifyExplicitPA10Restored(f)')\nstatements.append(\"axlDBControl('drcEnable t)\")\nstatements.append('fprintf(f \"HI_SCOPED_CHECK_MASTER_DRC_ENABLED=%L\\\\n\" axlDBControl(\\\'drcEnable))')\nfor check in data.get('postChecks',[]):");(R/'scripts/compile_batchHI_v31.py').write_text(s,encoding='utf8')
subprocess.run([sys.executable,str(R/'scripts/prepare_b016_retryHI.py'),'--variant','2L','--try-number','03','--compiler','31'],check=True)