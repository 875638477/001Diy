from pathlib import Path
R=Path(r'D:\001DIY\005lib\01AIEDA\learning\examples\lessonHI_38_50_20261021');s=(R/'scripts/extract_checkpointHI_v9.py').read_text();s=s.replace("B=Path(a.log);assert B.resolve().is_relative_to(R.resolve())", "B=Path(a.log);assert B.resolve().is_relative_to(R.resolve())\nNO_ALIAS_UPDATE=a.no_alias_update")
s=s.replace('if not a.no_alias_update:', 'if not NO_ALIAS_UPDATE:');(R/'scripts/extract_checkpointHI_v10.py').write_text(s,encoding='utf8')
