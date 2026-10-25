from pathlib import Path
import json
R=Path(r'D:\001DIY\005lib\01AIEDA\learning\examples\lessonHI_38_50_20261021')
body=r'''procedure(hiMechanicalPinRead(out)
 let((f pf sf ps pad)
  f=outfile(strcat(out "/hi_mechanical_pins.tsv"))
  pf=outfile(strcat(out "/hi_mechanical_pad_layers.tsv"))
  sf=outfile(strcat(out "/hi_hole_spacing_defaults.tsv"))
  fprintf(f "symbol\trefdes\tpin\tpadstack\txy\tthrough\tmechanical\tholeType\tplating\tdrillDiameter\tdrillX\tdrillY\tdefinitionAttributes\tinstanceAttributes\n")
  fprintf(pf "refdes\tpin\tpadstack\txy\tlayer\tkind\tfigure\tpadBBoxRelativeXY\tpadAttributes\n")
  foreach(s axlDBGetDesign()->symbols
   foreach(p s->pins
    when(p->isMech || !p->number || equal(p->number "")
     ps=p->definition
     fprintf(f "%L\t%L\t%L\t%L\t%L\t%L\t%L\t%L\t%L\t%L\t%L\t%L\t%L\t%L\n" s->name s->refdes p->number p->name p->xy p->isThrough p->isMech ps->holeType ps->plating ps->drillDiameter ps->drillSizeWidth ps->drillSizeHeight ps->?? p->??)
     foreach(layer mapcar(lambda((l) strcat("ETCH/" l)) axlSubclassRoute())
      foreach(kind list("REGULAR" "ANTI" "THERMAL" "KEEPOUT")
       pad=axlDBGetPad(p layer kind)
       fprintf(pf "%L\t%L\t%L\t%L\t%L\t%L\t%L\t%L\t%L\n" s->refdes p->number p->name p->xy layer kind if(pad then pad->figureName else nil) if(pad then pad->bBox else nil) if(pad then pad->?? else nil)))))))
  fprintf(sf "cset\tlayer\tfield\tvalue\n")
  foreach(layer axlSubclassRoute()
   foreach(key list('hole_line 'hole_shape 'hole_via 'hole_hole 'hole_thrupin)
    fprintf(sf "DEFAULT\t%L\t%L\t%L\n" layer key axlCNSGetSpacing("DEFAULT" layer key))))
  foreach(port list(f pf sf) close(port))
  f=outfile(strcat(out "/hi_mechanical_pin_scope.txt"))
  fprintf(f "HI_ALL_MECHANICAL_PINS_READ_COMPLETE\nAll actual symbol pins with isMech or empty/nil number included, including connector locating holes. Hole geometry taken from embedded native padstack definition, not inferred from name. Only actual routing layers probed. DEFAULT spacing is raw reference data, not a coordinate-specific resolved rule for a hole against another net/class.\n") close(f) t))
'''
(R/'scripts/mechanical_pin_readHI.il').write_text(body,encoding='ascii');p=R/'scripts/batchHI_shapes_v3.il';p.write_text(p.read_text()+'\n'+body,encoding='ascii')
for v,tag in [('4L','private_pad_inspect_4L_01'),('2L','private_pad_inspect_2L_02')]:
 h='set NOCONFIRM\nskill errset(load('+json.dumps((R/'scripts/private_pad_inspectHI.il').as_posix())+') t)\nskill errset(load('+json.dumps((R/'scripts/mechanical_pin_readHI.il').as_posix())+') t)\nskill errset(hiInspectPrivatePad('+json.dumps((R/'logs'/tag).as_posix())+' '+json.dumps((R/'library').as_posix())+') t)\nskill errset(hiMechanicalPinRead('+json.dumps((R/'logs'/tag).as_posix())+') t)\nquit\nfillin "yes"\n';(R/f'scripts/{tag}.scr').write_text(h,encoding='ascii')
