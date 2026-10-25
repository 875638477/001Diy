import pathlib,json,shutil
R=pathlib.Path(r'D:\001DIY\005lib\01AIEDA');J=R/'learning/examples/lessonJK_51_59_20261022'
d={"51":["审查实操已做；未接网/USB/整板DRC开放","lessonJK_51_54_20261022.md"],"52":["实际路径/参考审查已做；USB/返回待闭环","lessonJK_51_54_20261022.md"],"53":["供电域/回路审查已做；负载/热条件开放","lessonJK_51_54_20261022.md"],"54":["实际风险定位已做；整改/实测开放","lessonJK_51_54_20261022.md"],"55":["两板实例整改fresh1644项通过；DFM未释放","lessonJK_55_57_20261022.md"],"56":["原生实际输出+独立CAM/视觉已做；不可投产","lessonJK_independent56_20261022.md"],"57":["BOM/坐标训练输出通过；料号/工厂映射待定","lessonJK_55_57_20261022.md"],"58":["本轮隔离ECO1453项通过；完整两板未结课","lessonJK_K58_independent_replay_20261023.md"],"59":["测试方案/测点/空白表已备；实物NOT_RUN","lessonJK_59_bench_20261022.md"]}
b=J/'backups/index_progress_before_consolidation_20261023';b.mkdir(exist_ok=True)
for name in ['EDA.md','课程索引.md']:
 if not (b/name).exists():shutil.copy2(R/name,b/name)
p=R/'课程索引.md';s=p.read_text(encoding='utf-8-sig');ls=s.splitlines();count=0
for i,line in enumerate(ls):
 parts=[x.strip()for x in line.split('|')]
 if len(parts)==8 and parts[1]in d:
  parts[5]=d[parts[1]][0];parts[6]='[实操记录](learning/notes/'+d[parts[1]][1]+')';ls[i]='| '+' | '.join(parts[1:-1])+' |';count+=1
assert count==9,count
p.write_text('\n'.join(ls)+'\n',encoding='utf8')
p=R/'EDA.md';s=p.read_text(encoding='utf-8-sig')
s=s.replace('## 当前学习计划（2026-10-22，J/K第51—59课）','## 当前学习计划（2026-10-23，J/K第51—59课）',1)
ls=s.splitlines()
for i,line in enumerate(ls):
 if line.startswith('| P6 '):
  ls[i]='| P6 审查与生产输出 | SI/PI/EMI、制造装配、实际CAM、BOM/坐标、ECO与实测方案 | 问题闭环，输出与最终板身份一致 | J/K本轮审查/整改/输出已做：J55 fresh1644项；CAM77/85项及逐Film22/24项通过；隔离ECO1453项通过。完整两板/DFM/整板DRC开放，59仅方案NOT_RUN。见[J/K记录](learning/notes/lessonJK_51_59_20261022.md)。 |'
 if line.startswith('1. 正在合并学习H/I第38—50课'):
  ls[i]='1. 当前J/K第51—59课：审查、实例整改、实际CAM/BOM/坐标及隔离ECO已有真实结果；新四层按用户L2完整地/L3电源另存并复核。其后继续H/I每板7个未接网、USB/整板DRC及制造条件，45/50/58完整板验收保持待办。见[J/K主笔记](learning/notes/lessonJK_51_59_20261022.md)。'
s='\n'.join(ls)+'\n';marker='**2026-10-22四层默认层功能';pos=s.index(marker)
s=s[:pos]+'**本轮可核验进展（2026-10-23）：** J55两板独立fresh共1644项通过；实际CAM各77/85项、目标外几何22/24项通过，三文字光绘已查看；隔离ECO1453项通过；上电表与测点已备但NOT_RUN。完整PCB、DFM及实物未放行。\n\n'+s[pos:]
p.write_text(s,encoding='utf8')
p=J/'learning_plan.md';s=p.read_text(encoding='utf-8-sig')
assert '## 2026-10-23本轮执行状态'not in s
s+='\n## 2026-10-23本轮执行状态\n\n| 课号 | 实际状态 |\n| --- | --- |\n'+''.join('| '+k+' | '+v[0]+' |\n'for k,v in d.items())+'\n完整事实、源板身份及开放项见[主笔记](../../notes/lessonJK_51_59_20261022.md)。审查已做不等于问题全部关闭。\n'
p.write_text(s,encoding='utf8')
print(json.dumps({'indexRowsUpdated':count,'EDAOpeningPlanUpdated':True,'oldRecordsBackedUp':True}))
