from pathlib import Path
import argparse,json,hashlib,shutil
R=Path(r'D:\001DIY\005lib\01AIEDA\learning\examples\lessonG_30_37_20261020')
P=argparse.ArgumentParser();P.add_argument('--plan',default=str(R/'plans/placement_plan.json'));P.add_argument('--variant',choices=['4L','2L'],required=True);P.add_argument('--tag',required=True)
a=P.parse_args();planpath=Path(a.plan);assert planpath.resolve().is_relative_to(R.resolve());data=json.loads(planpath.read_text())
placements=data['placements'];assert len(placements)==80 and len({x['ref'] for x in placements})==80
assert all(x.get('side','TOP')=='TOP' for x in placements),'Bottom placement requires explicit mirroring implementation review'
assert next(x for x in placements if x['ref']=='J2')['x']==40 and next(x for x in placements if x['ref']=='J2')['y']==3.675
def q(s):return json.dumps(s)
def num(x):return str(float(x))
rows=' '.join('list('+q(x['ref'])+' '+' '.join(num(x[k]) for k in ['x','y','rotation'])+')' for x in placements)
il=R/f'scripts/plan_{a.tag}.il'
il.write_text('gPlan=list('+rows+')\n',encoding='ascii')
p=R.as_posix()
loads=[*(R/'source'/x for x in ['de_board_read.il','build29_v2.il','read29.il','extra_read29.il','specific_proof.il','more28.il','mechanical28.il','correction.il']),R/'scripts/inventoryG.il',R/'scripts/placementG.il',il]
prefix='set NOCONFIRM\n'+''.join('skill errset(load("'+x.as_posix()+'") t)\n' for x in loads)
board=R/f'native/G_{a.variant}_PLACEMENT_{a.tag}.brd'
layers='list("TOP" "BOTTOM")' if a.variant=='2L' else 'list("TOP" "L2" "L3" "BOTTOM")'
script=R/f'scripts/place_{a.tag}.scr'
script.write_text(prefix+f'skill errset(gPlace(gPlan "{board.as_posix()}" "{p}/logs/place_{a.tag}" "{p}/library" {layers}) t)\nquit\nfillin "yes"\n',encoding='ascii')
reopen=R/f'scripts/reopen_{a.tag}.scr'
reopen.write_text(prefix+f'skill errset(gSnapshot("{p}/logs/reopen_{a.tag}" "{p}/library") t)\nquit\nfillin "yes"\n',encoding='ascii')
record={'status':'PREPARED_NATIVE_PLACEMENT_NOT_EXECUTED','plan':str(planpath),'planSHA256':hashlib.sha256(planpath.read_bytes()).hexdigest().upper(),'planStatus':data['status'],'variant':a.variant,'tag':a.tag,'board':str(board),'script':str(script),'reopenScript':str(reopen)}
(R/f'scripts/compiled_{a.tag}.json').write_text(json.dumps(record,indent=2),encoding='utf8')
print(json.dumps(record,indent=2))
