from pathlib import Path
import json,sys,runpy,hashlib,shutil
R=Path(r'D:\001DIY\005lib\01AIEDA');L=R/'learning/examples/lesson60_20261023';S=R/'learning/skills/cadence17-learning'
sys.path.insert(0,str(L/'tooling/pyyaml_6_0_3'));validator=Path(r'C:\Users\Administrator\.codex\skills\.system\skill-creator\scripts\quick_validate.py');module=runpy.run_path(str(validator));ok,msg=module['validate_skill'](S);assert ok,msg
d={'status':'PASS_FINAL_SKILL_SOURCE_VALIDATION','validator':str(validator),'message':msg,'files':[{'path':str(p.relative_to(S)),'sha256':hashlib.sha256(p.read_bytes()).hexdigest().upper()}for p in sorted(S.rglob('*'))if p.is_file()and '__pycache__'not in p.parts],'preflightBehaviorReport':'preflight_forward_fix_validation.json','autoInstalled':False}
(L/'review/skill_final_validation.json').write_text(json.dumps(d,indent=2),encoding='utf8')
p=R/'learning/notes/lesson60_20261023.md';s=p.read_text(encoding='utf8');s=s.replace('独立审查另从raw summary、geometry、journal、process和probe复核，不只读PASS标签。','独立审查另从raw summary、geometry、journal、process和probe做313项语义/身份检查，0失败，不只读PASS标签。',1);p.write_text(s,encoding='utf8')
p=R/'EDA.md';s=p.read_text(encoding='utf8');start=s.index('## 当前学习计划（2026-10-23，第60课）');end=s.index('## 上一轮J/K学习进度',start)
current='## 当前学习计划（2026-10-23，第60课）\n\n第60课本轮资料/依赖/操作库学习与同机重定位已完成：文字PDF第1页与扫描教材PDF281/纸页262实际读取、来源模板与迁移依赖齐全；最终原生包在两个不同目录（含空格）各42项通过，真实932段（750manual/182thermal）保存重开保持，独立原始证据313项通过。已有[最小迁移ZIP](learning/examples/lesson60_20261023/eda60-portable-kit.zip)、[操作手册](learning/examples/lesson60_20261023/MIGRATION.md)、[本地技能源](learning/skills/cadence17-learning/SKILL.md)与[第60课完整笔记](learning/notes/lesson60_20261023.md)。另一台物理电脑、GUI、OCR及本轮视频播放仍未验；H/I45/50、JK58整板和59实物待办保持。异常关机恢复、空枚举不足、长路径启动失败、预检防覆盖修复均已如实记录。\n\n'
s=s[:start]+current+s[end:];p.write_text(s,encoding='utf8')
p=R/'\u8bfe\u7a0b\u7d22\u5f15.md';ls=p.read_text(encoding='utf8').splitlines();count=0
for i,line in enumerate(ls):
 if line.startswith('| 60 |'):
  row=[a.strip()for a in line.split('|')];row[5]='本轮资料/技能及同机双路径复现完成；异机/GUI待验';row[6]='[完整笔记](learning/notes/lesson60_20261023.md) / [迁移手册](learning/examples/lesson60_20261023/MIGRATION.md)';ls[i]='| '+' | '.join(row[1:-1])+' |';count+=1
assert count==1;p.write_text('\n'.join(ls)+'\n',encoding='utf8')
snapshot=L/'sealed_snapshots';mapping=[]
for src,rel in [(R/'EDA.md','EDA.md'),(R/'\u8bfe\u7a0b\u7d22\u5f15.md','\u8bfe\u7a0b\u7d22\u5f15.md')]+[(p,'notes/'+p.name)for p in (R/'learning/notes').glob('lesson60*.md')]+[(p,'skill/'+p.relative_to(S).as_posix())for p in S.rglob('*')if p.is_file()and '__pycache__'not in p.parts]:
 dst=snapshot/rel;dst.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(src,dst);mapping.append({'liveSourceAtSeal':str(src),'frozenSnapshot':str(dst.relative_to(L)),'sha256':hashlib.sha256(dst.read_bytes()).hexdigest().upper()})
(L/'review/live_to_frozen_snapshot_mapping.json').write_text(json.dumps({'reason':'Seal byte snapshots, not mutable EDA/index/skill pointers; future course updates need not invalidate this lesson','mapping':mapping},ensure_ascii=False,indent=2),encoding='utf8')
print(json.dumps({'skillValid':ok,'courseIndexRowsUpdated':count,'frozenSnapshots':len(mapping)}))
