"""Write final project records only after actual publish/retirement/path checks pass."""
from pathlib import Path
import argparse,hashlib,json,os,datetime
M=Path(__file__).resolve().parent
P=Path('D:/001DIY/004computer/lga1700');R=P/'13shared_libraries_pc_20261025'
sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest().upper()
jr=lambda p:json.loads(Path(p).read_text('utf-8-sig'))
def need(v,m):
    if not v:raise ValueError(m)
def write_atomic(p,b):
    t=p.with_name(p.name+'.final28.tmp');need(not t.exists(),'Temporary target exists')
    with t.open('xb') as f:f.write(b);f.flush();os.fsync(f.fileno())
    os.replace(t,p)
def main():
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--active-audit',type=Path,required=True);a=ap.parse_args()
    documents={
      'main_publication':R/'verification/final13_five_publication27/PUBLICATION_RECEIPT.json',
      'main_final_active_paths':a.active_audit,
      'public_olbs':M/'public_olb_final13_published13/PUBLIC_OLB_PUBLISH_RECEIPT.json',
      'public_boards':M/'public_four_final_native_published28/PUBLISH_RECEIPT.json',
      'native_zero_reference_closure':M/'final_native_reference_closure28/NATIVE_REFERENCE_CLOSURE.json',
      'exact_alias_retirement':M/'public_retirement_all_confirmed_stage13_v2/APPLY_RECEIPT.json',
      'public0010_all_native_proofs':M/'public0010_final_private_gates_index13_v1/PUBLIC0010_FINAL_PRIVATE_EXECUTED_PROOFS_INDEX.json',
      'canonical127_complete_graph_and_pad':M/'canonical_retirement_target127_v127/REQUIRED_CANONICAL_NATIVE_TARGET_INDEX.json',
      'main59_official_export':M/'final59_official_name_export_review27/PACKAGE_EXPORT_NAME_VERIFICATION.json'}
    q={k:jr(v) for k,v in documents.items()}
    for k,v in q.items():need(v['status'].startswith('PASS'),k+' not actual PASS')
    retire=q['exact_alias_retirement'];need(retire['public_files_removed']==3069 and retire['remaining_public_files']==10364,'Actual retirement counts differ')
    need(retire['closure']['sha256']==sha(documents['native_zero_reference_closure']),'Closure changed after retirement')
    need(q['public_boards']['public_files_replaced']==4,'Four public boards not published')
    designs=[(R/'sch/LGA1700.DSN','E421141B8B9DF969E8C654E86FEF6D2B2E06E5C5B8CF82C1DC03C7AC1767D374'),(R/'pcb/LGA1700_RULES.brd','49B874ED98BD3F66EC23D115848C88E2F744195DEE9B35DC98F143674E055308')]
    for p,h in designs:need(sha(p)==h,'Formal main design changed')
    frozen=jr(R/'verification/SOURCE_FREEZE.json')
    for p,h in [('schematic_source','schematic_sha256'),('pcb_source','pcb_sha256'),('formal12_board','formal12_board_sha256'),('source_common_olb','source_common_sha256')]:need(sha(frozen[p])==frozen[h],'Protected original changed')
    readme=R/'README.md';need(sha(readme)=='653275F37BB3F010764119BFCD5E1AF8E794DDA7FB59969887E4210D6D2D2260','README edited; preserve before deliberate merge')
    text=readme.read_text('utf-8-sig').replace('13版主工程已发布；本机公共模块迁移和旧别名清理仍在进行，以本目录正式文件为主。','13版主工程及本机公共库归并已完成，以本目录正式文件为主。')
    text=text.replace('本机库清理进度以该目录的最终清理回执为准；未完成公共模块连接校验前不删除旧别名。','本机4个公共PCB模块及13份OLB已完成对应迁移；1067个旧别名在48个原生来源、8类引用中逐项为零后，删除3069个精确旧文件。127个公共目标、备份归档及关键验证资料保留。详见[最终发布与清理记录](verification/FINAL13_SHARED_LIBRARY_RESULT.json)。')
    write_atomic(readme,text.encode('utf-8'))
    record=R/'工程更改记录.md';need(sha(record)=='FD4B0A1A1156B065AAA7976D0FE11CC4C4651DFA879301E0A1D06AFCAD80C128','Engineering record edited; preserve before deliberate merge')
    text=record.read_text('utf-8-sig').replace('主工程已于2026-10-26发布。公共库4个模块迁移、最终零引用复核及旧别名删除仍待最后回执，本记录下方将补充实际结果。','主工程、本机公共库迁移及旧别名清理已于2026-10-26完成。最终实际结果及回执见文末。').replace('外国模块源来已有','其他模块原来已有')
    text+='''

## 最终公共发布与精确清理（2026-10-26）

4个公共模块00012/0010/006/008已按完整原生证明发布到01brdlib；13份OLB已发布到01captureLib。0010最终SHA为07A0F9340CBC89718BD586DEFCC270E299E24242C6AA7A6FA78973C220E82A42，独立重开全部2698焊盘/915连接分区、593对象、1739过孔、101完整器件定义、完整网表和规则通过。

0010的21条源热连接小路径按原DB2Path精确重建，实际返回24个静态路径对象。完整三电源网铜满足after=before∪source21，源外新增铜/旧铜损失/异网交叠为零；不把它们声称为动态thermal。裁切铜片在数据库量化后的精确FAIL保留，未设通用容差。全部79缓存（70在用PACKAGE/MECHANICAL/FORMAT及9个SHAPE）/20080对象、554973值经过完整未知字段/属性/图形及显式运行期ID双射核验，0字段忽略、0数值容差；4种实际PAD全制造XML与公共文件精确一致。

正式文件发布后，重新读取公共7板的全部声明、放置符号及完整symdefs（含unused），结合37 OLB、2公共DSN及主工程两文件，共48个原生来源。1067个旧名在8类引用中全部为整数0；127个公共目标与退休名单无交集，154种PAD制造对象和当前文件SHA重新核验。

按冻结清单实际删除3069个旧PSM/DRA/同名self-device TXT目录项，逻辑文件大小87,476,185字节。未声称等量物理磁盘空间已释放（存在硬链接及保留归档）。其余10364个公共文件逐SHA未变，不删除共享PAD。两份已逐成员SHA/CRC回读的原别名备份归档及原4模块备份保留；需要恢复时先按BACKUP_STAGE.json定位指定文件及归档成员，解压到暂存目录核对SHA，再决定是否重新启用旧名，不要整包覆盖当前公共库。

全部实际回执及当前正式身份汇总见[FINAL13_SHARED_LIBRARY_RESULT.json](verification/FINAL13_SHARED_LIBRARY_RESULT.json)。方法与脚本在D:/001DIY/005lib/01AIEDA/library_maintenance/20261025_pc_shared；历史失败/旧计划仅作留证，当前状态以本记录和README为准。旧工程、原件和既有压缩包保留。
'''
    write_atomic(record,text.encode('utf-8'))
    log=P/'转换记录.md';b=log.read_bytes();need('## 四十一　13版公共库统一'.encode('utf-8') not in b,'Final section already exists')
    addition='''

## 四十一　13版公共库统一与全库旧别名清理（2026-10-26）

已完成[13shared_libraries_pc_20261025](./13shared_libraries_pc_20261025/README.md)。正式原理图sch/LGA1700.DSN SHA E421141B8B9DF969E8C654E86FEF6D2B2E06E5C5B8CF82C1DC03C7AC1767D374；正式PCB pcb/LGA1700_RULES.brd SHA49B874ED98BD3F66EC23D115848C88E2F744195DEE9B35DC98F143674E055308。主板81种归并59种，994个物理器件封装更换，1066实体/6494编号脚网表、35页原理图及原Value/NC_保持。公共路径全面指向D:/001DIY/005lib；134差分/42匹配/212PinPair原规则内容保持。VDD10_1 U5.3原已同网且源铜接触的附着恢复有限接受，实际连接分组2020→2019，其余逐组不变。

本机不只处理AO3414/AO4468示例，13份公共OLB及4个PCB模块完成迁移。1067旧名在48个原生来源×8类引用实际全0后，精确删除3069个旧PSM/DRA/self-device TXT文件（87,476,185逻辑字节）；其余10364个公共文件SHA保持，公共127目标及154PAD制造对象通过。原别名ZIP、4模块原件ZIP、脚本、方法和关键校验记录保留。真实焊盘/功能/制造差异变体保留独立名称。

完整过程、0010原热连接精确恢复及静态路径事实、全部79缓存ID双射、实际文件回执见[工程更改记录](./13shared_libraries_pc_20261025/工程更改记录.md)和[最终核验](./13shared_libraries_pc_20261025/verification/FINAL13_SHARED_LIBRARY_RESULT.json)。通用学习方法已更新D:/001DIY/005lib/01AIEDA及其learning/notes/public_shared_library_migration_pc_naming.md。旧11/12、01sch/02pcb、AD原件及既有归档保留；A16待布线及硬件/固件/MRC/VRM/VREF/DRC制造开放项未因本轮库归并关闭。
'''
    write_atomic(log,b+addition.encode('utf-8'));need(log.read_bytes().startswith(b),'Conversion history prefix changed')
    result=dict(status='PASS_PROJECT13_AND_MACHINE_SHARED_LIBRARY_CONSOLIDATION_COMPLETE',created_local=datetime.datetime.now().astimezone().isoformat(),formal_designs=[dict(path=str(p),sha256=h) for p,h in designs],main_footprints_before=81,main_footprints_after=59,main_physical_refs=1066,main_numbered_pins=6494,main_physical_FP_changes=994,public_olbs_replaced=13,public_boards_replaced=4,retired_stems=1067,retired_file_entries=3069,retired_logical_bytes=87476185,remaining_public_files=10364,canonical_targets=127,canonical_PAD_manufacturing_objects=154,protected_four_original_inputs_unchanged=True,proofs={k:dict(path=str(p),sha256=sha(p),status=q[k]['status']) for k,p in documents.items()},records=[dict(path=str(p),sha256=sha(p)) for p in [readme,record,log]],scope='Library consolidation and original connectivity preservation; existing hardware/routing/manufacturing open items remain documented.')
    output=R/'verification/FINAL13_SHARED_LIBRARY_RESULT.json';need(not output.exists(),'Final result already exists');write_atomic(output,json.dumps(result,ensure_ascii=False,indent=2).encode('utf-8'));print(json.dumps(dict(status=result['status'],report=str(output),sha256=sha(output))))
if __name__=='__main__':main()
