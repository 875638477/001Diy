from pathlib import Path
R=Path(r'D:\001DIY\005lib\01AIEDA\learning\examples\lessonG_30_37_20261020')
s=(R/'scripts/validate_nativeG_final.py').read_text()
needle="check(f'{key}.reference_fill_exact_after_coupon_rollback',(before/'g_copper_shapes.tsv').read_bytes()==(after/'g_copper_shapes.tsv').read_bytes())"
s=s.replace(needle,needle+"\n check(f'{key}.actual_pin_copper_mask_exact_after_coupon_rollback',(before/'g_actual_pins.tsv').read_bytes()==(after/'g_actual_pins.tsv').read_bytes())")
(R/'scripts/validate_nativeG_final.py').write_text(s,encoding='ascii')
