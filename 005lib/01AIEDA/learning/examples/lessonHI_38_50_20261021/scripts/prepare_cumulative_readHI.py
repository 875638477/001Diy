from pathlib import Path
import json,hashlib,shutil,argparse
R=Path(r'D:\001DIY\005lib\01AIEDA\learning\examples\lessonHI_38_50_20261021');p=argparse.ArgumentParser();p.add_argument('--variant',required=True,choices=['2L','4L']);a=p.parse_args();v=a.variant;tag=f'cumulative_pin_contract_{v}_b014';D=json.loads((R/f'review/cumulative_physical_proofs_{v}_b014.json').read_text());q=json.dumps;out=(R/'logs'/tag).as_posix();contract='list('+' '.join('list('+q(x['ref'])+' '+q(x['pin'])+' '+(q(x['net']) if x['net'] else 'nil')+' '+q(x['padstack'])+')' for x in D['terminalContract'])+')'
s='procedure(hiCumulativePhysicalRead(out)\n let((f)\n f=outfile(strcat(out "/hi_cumulative_physical_pin_proofs.txt"))\n hiRegistry=nil hiNodeDefinitions=nil\n hiPhysicalTerminalContract(f '+contract+')\n'
for x in D['baselineComponentPreservationProofs']:s+=' hiProof(f '+q(x['from'])+' '+q(x['to'])+' t)\n'
s+=' fprintf(f "HI_CUMULATIVE_BASELINE_PHYSICAL_PIN_PROOFS_COMPLETE positiveEdges='+str(len(D['baselineComponentPreservationProofs']))+' readOnly=t storedDRC=%d fullDRCRecompute=NOT_REQUESTED final197AllNetProofs=NOT_REQUESTED online=%L\\n" length(axlDBGetDesign()->drcs) axlDBControl(\'drcEnable)) close(f) t))\n'
p=R/f'scripts/{tag}.il';p.write_text(s,encoding='ascii');loads=[R/'source'/x for x in ['placementG.il','local_copperG_v2.il']]+[R/'scripts/batchHI.il',R/'scripts/batchHI_extended.il',R/'scripts/batchHI_shapes_v3.il',p]
snap=R/'source/readback_snapshots'/tag;snap.mkdir();h='set NOCONFIRM\n';man=[]
for i,src in enumerate(loads):
 dst=snap/f'{i:02d}_{src.name}';shutil.copyfile(src,dst);h+='skill errset(load('+q(dst.as_posix())+') t)\n';man.append({'source':str(src),'snapshot':str(dst),'sha256':hashlib.sha256(dst.read_bytes()).hexdigest().upper()})
h+='skill errset(hiCumulativePhysicalRead('+q(out)+') t)\nquit\nfillin "yes"\n';(R/f'scripts/{tag}.scr').write_text(h,encoding='ascii');(snap/'manifest.json').write_text(json.dumps(man,indent=2));print(tag)
