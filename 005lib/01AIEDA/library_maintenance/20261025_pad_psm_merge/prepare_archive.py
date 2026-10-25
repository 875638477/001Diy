"""Prepare a reviewable, hash-bound archive publication without external writes."""
import csv,hashlib,json,shutil
from pathlib import Path

B=Path(__file__).resolve().parent
WORK=B.parent
AI=Path(r'D:\001DIY\005lib\01AIEDA')
DEST=AI/'library_maintenance/20261025_pad_psm_merge'
SOURCES=[
 (WORK/'cadence_library_cleanup_20261025','cadence_library_cleanup_20261025'),
 (WORK/'cadence_geometry_merge_20261025','cadence_geometry_merge_20261025'),
 (Path(r'D:\001DIY\005lib\_library_suffix_backup_20261025'),'backups/_library_suffix_backup_20261025'),
 (Path(r'D:\001DIY\005lib\_library_merge_backup_20261025'),'backups/_library_merge_backup_20261025'),
 (Path(r'D:\001DIY\005lib\_library_geometry_backup_20261025'),'backups/_library_geometry_backup_20261025'),
]

def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()

def prepare_doc(relative,encoding,transform):
    source=AI/relative;before=source.read_bytes();text=before.decode(encoding)
    newline='\r\n' if b'\r\n' in before else '\n'
    normalized=text.replace('\r\n','\n')
    after_text=transform(normalized)
    insertion_codec='utf-8' if encoding=='utf-8-sig' else encoding
    if relative!='study_records/README.md':
        title,tail=normalized.split('\n',1)
        assert after_text.startswith(title+'\n') and after_text.endswith(tail)
        added=after_text[len(title)+1:len(after_text)-len(tail)]
        split=before.index(b'\n')+1
        updated=before[:split]+added.replace('\n',newline).encode(insertion_codec)+before[split:]
    else:
        needle='| --- | --- |';row=after_text.split(needle+'\n',1)[1].split('\n',1)[0]
        assert after_text==normalized.replace(needle,needle+'\n'+row,1)
        updated=before.replace(needle.encode(insertion_codec),(needle+newline+row).encode(insertion_codec),1)
    before_path=B/'docs_before'/relative;after_path=B/'docs_after'/relative
    before_path.parent.mkdir(parents=True,exist_ok=True);after_path.parent.mkdir(parents=True,exist_ok=True)
    before_path.write_bytes(before);after_path.write_bytes(updated)
    return dict(target=str(source),relative=relative,encoding=encoding,before_sha256=hashlib.sha256(before).hexdigest(),
                after_sha256=hashlib.sha256(updated).hexdigest(),before=str(before_path),after=str(after_path))

def after_title(text,block):
    first,rest=text.split('\n',1);return first+'\n\n'+block.strip()+'\n'+rest

def main():
    (B/'readable').mkdir(exist_ok=True)
    docs=[]
    entry='library_maintenance/20261025_pad_psm_merge/README.txt'
    block=f'''## 公共库维护记录（2026-10-25用户指定）

`D:/001DIY/005lib/01AIEDA` 是全部公共库维护的统一工作与记录入口。公共库的创建、修改、尺寸/几何合并、删除、检查及恢复记录，统一放在 `library_maintenance/`，按日期和任务分目录；维护过程中产生的脚本、中间物、清单、日志、验证证据和备份同步归档，并更新本入口。

本次两轮焊盘/封装库整理已统一归档，见[2026-10-25焊盘与封装维护记录]({entry})及[库维护总索引](library_maintenance/INDEX.txt)。按实际尺寸和完整几何合并，C/R/L开头封装保持；数字0402/0603/0805带后缀封装的删除清单、兼容旧名映射、原生验证与恢复备份均在归档中。

本条适用于公共库维护；具体PCB/原理图工程继续按其工程根保存。公共库文件继续使用用户指定的 `01Pad_lib`、`01Psm_lib`、`01captureLib` 等路径。
'''
    docs.append(prepare_doc('EDA.md','utf-8-sig',lambda t:after_title(t,block)))
    bridge=f'''## 公共库维护更改记录入口（2026-10-25）

用户指定：所有库维护的工作记录统一保存在 `D:/001DIY/005lib/01AIEDA/library_maintenance/`，创建、修改、合并、删除和验证均按日期/任务记录；后续维护同步更新 `EDA.md` 与库维护总索引。

本次记录：[焊盘与封装整理归档]({entry})；总索引：[library_maintenance/INDEX.txt](library_maintenance/INDEX.txt)。原生库文件仍使用既定公共库路径。
'''
    docs.append(prepare_doc('AI接管cadence.md','gb18030',lambda t:after_title(t,bridge)))
    rule='''## 2026-10-25公共库维护目录规则

用户最新指定：`D:/001DIY/005lib/01AIEDA` 是全部公共库维护的统一工作与记录根。公共焊盘、封装、原理图库及其它公共库的创建/修改/合并/删除/验证，工作材料和更改记录统一保存在 `library_maintenance/<日期_任务>/`，包含来源与用户范围、软件版本、前后SHA、变更清单、主文件/兼容旧名映射、脚本与中间物、日志、验证结果、备份及恢复方式；每次更新总索引与EDA.md。

此条优先于下列将库维护记录随具体工程保存的旧表述；普通实际PCB/原理图工程继续在自己的工程根。公共库实体按用户既定的01Pad_lib、01Psm_lib等路径使用。

本次入口：[2026-10-25公共焊盘/封装维护归档](../../library_maintenance/20261025_pad_psm_merge/README.txt)；[全部库维护索引](../../library_maintenance/INDEX.txt)。旧记录中的绝对路径保留取证，归档清单保存新旧位置和校验值。
'''
    docs.append(prepare_doc('learning/notes/record_location_rules.md','utf-8-sig',lambda t:after_title(t,rule)))
    def update_study(t):
        needle='| --- | --- |'
        assert needle in t
        return t.replace(needle,needle+'\n| [公共焊盘/封装库维护记录](../library_maintenance/20261025_pad_psm_merge/README.txt) | 两轮合并/删除清单、原生验证、完整证据与恢复备份 |',1)
    docs.append(prepare_doc('study_records/README.md','utf-8-sig',update_study))
    # Directly readable records; full original trees are included in the ZIP.
    selected={
      '第一轮_执行记录.txt':(SOURCES[0][0]/'执行记录.txt'),
      '第二轮_按实际尺寸合并_执行记录.txt':(SOURCES[1][0]/'按实际尺寸合并_执行记录.txt'),
      '第一轮_合并清单.csv':SOURCES[0][0]/'merge_plan.csv',
      '删除后缀封装清单.csv':SOURCES[0][0]/'suffix_delete_plan.csv',
      '第二轮_实际几何合并清单.csv':SOURCES[1][0]/'physical_merge_plan.csv',
      '第二轮_唯一主文件索引.csv':SOURCES[1][0]/'canonical_physical_index.csv',
      '第一轮_完成校验.json':SOURCES[0][0]/'completion.json',
      '第二轮_完成校验.json':SOURCES[1][0]/'completion.json',
      '第二轮_全库校验.json':SOURCES[1][0]/'final_library_verification.json',
      '第二轮_原生焊盘验证.json':SOURCES[1][0]/'live_physical_pad_verification.json',
      '第二轮_原生符号验证.json':SOURCES[1][0]/'live_physical_symbol_verification.json',
      '第二轮_独立复审.json':SOURCES[1][0]/'final_physical_plan_independent_review.json',
    }
    for name,source in selected.items():shutil.copyfile(source,B/'readable'/name)
    inventory=[]
    for root,archive_root in SOURCES:
        for p in sorted(root.rglob('*')):
            if not p.is_file() or '__pycache__' in p.parts or p.suffix.lower()=='.pyc':continue
            inventory.append(dict(source=str(p),archive_path=archive_root+'/'+p.relative_to(root).as_posix(),
                                  bytes=p.stat().st_size,sha256=sha(p)))
        print(json.dumps(dict(source=str(root),inventoried_files=len(inventory))),flush=True)
    (B/'archive_manifest.json').write_text(json.dumps(inventory,ensure_ascii=False,indent=2),encoding='utf-8')
    with (B/'archive_manifest.csv').open('w',encoding='utf-8-sig',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(inventory[0]));w.writeheader();w.writerows(inventory)
    readme=f'''公共库维护记录统一归档
日期：2026-10-25（Asia/Shanghai）

用户指定的统一入口：D:\\001DIY\\005lib\\01AIEDA\\library_maintenance
本次目录：{DEST}

本次同时收录两轮公共库工作：
1. 首轮内容/原生定义去重，以及9种数字0402/0603/0805带后缀封装共18个文件的删除。
2. 按实际尺寸和完整几何继续合并：50个PAD、38个PSM、44个DRA、5个SSM、1个FSM；共138条路径。
两轮计数属于顺序操作，部分路径可能重叠，不可直接相加作为唯一文件数。
C/R/L开头封装保持不动；旧名称保留为共享实体的兼容硬链接。

直接查看：readable/ 内的中文执行记录、合并/删除清单、唯一主文件索引、原生验证和完成校验。
完整原始记录与恢复原件：cadence_library_maintenance_20261025_full.zip。
完整源文件清单：archive_manifest.csv / archive_manifest.json（含历史原位置、归档内位置、大小、SHA256）。
归档共{len(inventory)}个原始文件、{sum(r['bytes'] for r in inventory)}字节；ZIP中的5个目录分别保留两轮完整记录树和三套恢复备份。
ZIP及逐条原始文件的验证结果见 archive_verification.json；不是只检查压缩文件是否能打开。

原始记录中的绝对路径按历史原文保留；原工程目录中的记录暂留供既有引用读取。统一查阅和今后新增更改记录以本目录和library_maintenance/INDEX.txt为准。
归档的脚本是历史证据，不自动执行。恢复前先核对应备份清单与库当前状态。
现有恢复目录也继续保留：
D:\\001DIY\\005lib\\_library_suffix_backup_20261025
D:\\001DIY\\005lib\\_library_merge_backup_20261025
D:\\001DIY\\005lib\\_library_geometry_backup_20261025
ZIP中backups/同时包含上述恢复原件及脚本的逐文件副本。

实际公共库仍使用既定01Pad_lib、01Psm_lib、01captureLib等目录，本次仅归档记录与更新入口，不改动CAD库内容、PCB、DSN或网表。
后续所有公共库维护：直接在01AIEDA/library_maintenance下按日期/任务记录工作过程、变更清单、验证与备份，并同步更新EDA.md和总索引。
'''
    (B/'README.txt').write_text(readme,encoding='utf-8-sig')
    (B/'INDEX.txt').write_text('公共库维护记录总索引\n\n统一目录：D:\\001DIY\\005lib\\01AIEDA\\library_maintenance\n\n2026-10-25  焊盘/封装两轮整理、实际尺寸与几何合并、后缀封装删除。\n入口：20261025_pad_psm_merge\\README.txt\n\n后续每次库创建、修改、合并、删除和检查均增加日期/任务条目，并更新EDA.md。\n',encoding='utf-8-sig')
    (B/'publish_plan.json').write_text(json.dumps(dict(destination=str(DEST),docs=docs,
        sources=[dict(source=str(r),archive_root=a) for r,a in SOURCES],file_count=len(inventory),
        original_bytes=sum(r['bytes'] for r in inventory),manifest_sha256=sha(B/'archive_manifest.json')),
        ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps(dict(status='PREPARED',file_count=len(inventory),bytes=sum(r['bytes'] for r in inventory),destination=str(DEST)),ensure_ascii=False),flush=True)

if __name__=='__main__':main()
