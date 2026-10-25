from pathlib import Path
R=Path(r'D:\001DIY\005lib\01AIEDA\learning\examples\lessonHI_38_50_20261021')
s=(R/'scripts/scoped_rule_builderHI.py').read_text();s=s.replace('def __init__(self,variant):','def __init__(self,variant,baseline_path=None,prefix="HI_JS"):').replace("self.variant=variant;self.base=json.loads((R/f'inventory/base_net_rules_{variant}.json').read_text())", "self.variant=variant;self.prefix=prefix;self.base=json.loads((Path(baseline_path) if baseline_path else R/f'inventory/base_net_rules_{variant}.json').read_text())").replace("return f'HI_JS_{kind}{self.serial:03d}_{self.variant}'", "return f'{self.prefix}_{kind}{self.serial:03d}_{self.variant}'");(R/'scripts/scoped_rule_builderHI_v2.py').write_text(s,encoding='utf8')
s=(R/'scripts/compile_batchHI_v28.py').read_text().replace("R/'scripts/extraReadHI.il',R/'scripts/batchHI_intermediate_drc_pending.il'", "R/'scripts/extraReadHI.il',R/'scripts/batchHI_b016_scoped_reference.il',R/'scripts/batchHI_intermediate_drc_pending.il'")
s=s.replace("statements=['hiRegistry=nil'", "statements=['hiDeferredReferences=nil','hiReferenceParamsBefore=nil','hiRegistry=nil'")
s=s.replace(" elif typ=='removeConstructionShape':", " elif typ=='deferReference':statements.append(f'hiDeferReference(f {q(ident)} {q(op[\"layer\"])} {points(op[\"polygon\"])})')\n elif typ=='restoreReference':statements.append(f'hiRestoreReference(f {q(ident)})')\n elif typ=='verifyReferences':statements.append('hiVerifyReferences(f)')\n elif typ=='removeConstructionShape':")
s=s.replace(" elif check['type']=='finiteViaLineChallenge':", " elif check['type']=='spacingFieldChallenge':statements.append(f'hiScopedSpacingFieldChallenge({q(out.as_posix())} {q(check[\"cset\"])} {q(check[\"layer\"])} \\'{check[\"field\"]} {q(check[\"net\"])} {num(check[\"normal\"])} {num(check[\"strict\"])})')\n elif check['type']=='changedNetworks':statements.append('hiScopedChangedNetworks('+q(out.as_posix())+' list('+' '.join(q(n) for n in check['nets'])+'))')\n elif check['type']=='finiteViaLineChallenge':")
(R/'scripts/compile_batchHI_v29.py').write_text(s,encoding='utf8')
import py_compile
# Syntax checking avoids filesystem bytecode outside task; explicit cfile stays in HI runtime.
(R/'runtime').mkdir(exist_ok=True)
py_compile.compile(str(R/'scripts/compile_batchHI_v29.py'),cfile=str(R/'runtime/compile_batchHI_v29.pyc'),doraise=True)
print('b016 helpers and compiler prepared')
