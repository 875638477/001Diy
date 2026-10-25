from pathlib import Path
R=Path(r'D:\001DIY\005lib\01AIEDA\learning\examples\lessonHI_38_50_20261021')
s=(R/'scripts/network_inventoryHI.il').read_text()
needle='  foreach(net des->nets'
rep='''  fprintf(sf "ALL_PIN_NET_OBJECT_TERMINALS=%d\\n" length(allpins))
  foreach(p allpins
   unless(member(p->net des->nets)
    fprintf(sf "EXCLUDED_PSEUDO_NET_TERMINAL ref=%L pin=%L xy=%L netAttrs=%L\\n" p->parent->refdes p->number p->xy p->net->??)))
  allpins=setof(p allpins member(p->net des->nets))
  foreach(net des->nets'''
assert needle in s;s=s.replace(needle,rep)
(R/'scripts/network_inventoryHI_v2.il').write_text(s,encoding='ascii')
for key in ['4L','2L']:
 s=(R/f'scripts/baseline_{key}_01.scr').read_text().replace('network_inventoryHI.il','network_inventoryHI_v2.il').replace(f'baseline_{key}_01',f'baseline_{key}_02')
 (R/f'scripts/baseline_{key}_02.scr').write_text(s,encoding='ascii')
p=R/'scripts/parse_baseline_HI.py';s=p.read_text().replace('baseline_{key}_01','baseline_{key}_02')
(R/'scripts/parse_baseline_HI_v2.py').write_text(s,encoding='ascii')
