"""Pure synthetic unit, missing-evidence and conflict checks; no CAD execution."""
import argparse
import copy
import json
from pathlib import Path
import subprocess
import sys
sys.path.insert(0, str(Path(__file__).resolve().parent))
import normalize_rc_values as formatter


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    args.output.mkdir(parents=True, exist_ok=False)
    checks = []
    def row(family, raw, **extra):
        return dict(ref='TEST1', family=family, raw_value=raw, package='0402', tolerance='1%', **extra)
    examples = [
        ({'ref':'C1','family':'C','raw_value':'100nF','package':'0402','rated_voltage':'25V','tolerance':'10%'}, '100nF/0402/25V/10%'),
        ({'ref':'C2','family':'C','raw_value':'10uF','package':'0805','rated_voltage':'25V','tolerance':'10%'}, '10uF/0805/25V/10%'),
        ({'ref':'C3','family':'C','raw_value':'4.7uF','package':'0603','rated_voltage':'25V','tolerance':'10%'}, '4.7uF/0603/25V/10%'),
        (row('R','100R'), '100R/0402/1%'),
        (dict(row('R','100K'),package='0603'), '100K/0603/1%'),
        (dict(row('R','100M'),package='0805'), '100M/0805/1%')]
    for record, expected in examples:
        assert formatter.normalize_record(record)['candidate_value'] == expected
    checks.append('All six requested display-format examples exact')
    for raw, expected in [('100mR','100mR'),('100M','100M'),('100m\u03a9','100mR'),('100M\u03a9','100M'),('0\u03a9','0R'),('4K7','4.7K'),('4R7','4.7R'),('100kohm','100K')]:
        assert formatter.resistance(raw) == expected
    checks.append('Milli versus mega, zero ohm, embedded decimal and Ohm spelling kept distinct')
    for raw, expected in [('0.1\u00b5F','100nF'),('0.1\u03bcF','100nF'),('1000pF','1nF'),('4n7','4.7nF'),('1mF','1000uF')]:
        assert formatter.capacitance(raw) == expected
    checks.append('Micro variants and exact pF/nF/uF engineering conversion')
    incomplete={'ref':'C4','family':'C','raw_value':'100nF','package':'0402','MPN':'KEEP','population':'NI','source':{'evidence':'unchanged'}}
    preserved=copy.deepcopy(incomplete);result=formatter.normalize_record(incomplete)
    assert result['candidate_value'] is None and result['status']=='REVIEW_NEEDED'
    assert set(result['missing_fields'])=={'rated_voltage','tolerance'} and incomplete==preserved and result['metadata']==preserved
    checks.append('No25V/10% fallback; full source metadata and input object preserved')
    conflicts=[
        dict(row('R','100R/0603/1%'),package='0402'),
        dict(examples[0][0],raw_value='100nF/0402/16V/10%'),
        dict(row('R','100m')),
        dict(row('R','10uF')),
        dict(examples[0][0],raw_value='4.7uH'),
        dict(examples[0][0],raw_value='1MF'),
        dict(examples[0][0],package='R0402'),
        dict(row('R','100R'),family='L'),
        dict(row('R','100R'),tolerance='J'),
        dict(row('R','100'))]
    for record in conflicts:
        value=formatter.normalize_record(record)
        assert value['status']=='REVIEW_NEEDED' and value['candidate_value'] is None, record
    checks.append('Conflicts, ambiguous m/MF, wrong dimension, family/package mismatch and letter codes block candidates')
    dnp_examples = [
        (dict(row('R', '100R'), population='NI', BOM_IGNORE=False, ConvertToPCB=True, PSpiceOnly=False,
              source={'assembly': 'NI', 'pin_no_connect': False}), 'NC_100R/0402/1%'),
        ({'ref':'DNP_C','family':'C','raw_value':'NC_100nF/0402/25V/10%'}, 'NC_100nF/0402/25V/10%'),
        (dict(examples[0][0], raw_value='100nF/NI'), 'NC_100nF/0402/25V/10%'),
        (dict(examples[0][0], raw_value='nc_0.1\u00b5F/0402/25V/10%'), 'NC_100nF/0402/25V/10%'),
        (dict(row('R', '100mR/0402/1%/DNP'), dnp=True), 'NC_100mR/0402/1%'),
        (dict(row('R', '100M'), assembly_state='not fitted'), 'NC_100M/0402/1%')]
    for record, expected in dnp_examples:
        preserved=copy.deepcopy(record);value=formatter.normalize_record(record)
        assert value['candidate_value']==expected and value['status']=='READY', value
        assert value['normalized_fields']['assembly_state']=='DNP' and value['assembly_evidence']
        assert record==preserved and value['metadata']==preserved
    checks.append('Explicit NI/DNP states and exact NC_ or trailing assembly markers preserve units and full source/assembly metadata')
    populated=formatter.normalize_record(dict(row('R','100R'),dnp=False))
    assert populated['candidate_value']=='100R/0402/1%' and populated['normalized_fields']['assembly_state']=='POPULATED'
    no_inference=dict(row('R','100R'),package='MINI_0402',MPN='NI_EXAMPLE',source_raw_value='NI',
                      exclude_from_bom=True,pin_no_connect=True)
    value=formatter.normalize_record(no_inference)
    assert value['candidate_value']=='100R/MINI_0402/1%' and value['normalized_fields']['assembly_state']=='UNSPECIFIED'
    assert value['assembly_evidence']==[] and value['metadata']==no_inference
    checks.append('NI in package/MPN/history and BOM/Convert/Pin-NoConnect metadata never infer population')
    pure_ni=dict(row('R','NI'),population='NI')
    value=formatter.normalize_record(pure_ni)
    assert value['candidate_value'] is None and value['status']=='REVIEW_NEEDED'
    assert value['normalized_fields']['assembly_state']=='DNP' and 'raw_value' in value['missing_fields']
    checks.append('Pure NI has no electrical value and requires review; never fabricated as zero ohm')
    for record in [dict(row('R','NC_100R'),assembly_state='INSTALLED'),
                   dict(row('R','100R'),population='NI',dnp=False),
                   dict(row('R','100R'),population='OPTIONAL'),
                   dict(row('R','100R'),dnp='NI'),
                   row('R','100R/NI/0402'),row('R','NC_NC_100R')]:
        value=formatter.normalize_record(record)
        assert value['status']=='REVIEW_NEEDED' and value['candidate_value'] is None, value
    checks.append('Conflicting/unknown assembly states and malformed marker positions are not silently discarded')
    explicit=dict(examples[0][0],rated_voltage=6.3,tolerance=0.1)
    assert formatter.normalize_record(explicit)['candidate_value']=='100nF/0402/6.3V/0.1%'
    assert formatter.normalize_record(dict(examples[0][0],rated_voltage='25'))['candidate_value'] is None
    checks.append('Numeric voltage meansV and numeric tolerance means percentage points, never ratio')
    policy=dict(row('R','100R'),tolerance='1%',source_tolerance='0.1%',
                display_policy={'basis':'Explicit user selection','tolerance':'1%'})
    policy_before=copy.deepcopy(policy)
    policy_result=formatter.normalize_record(policy)
    assert policy_result['candidate_value']=='100R/0402/1%' and policy_result['metadata']==policy_before and policy==policy_before
    unknown=dict(row('R','100R'),tolerance='TBD')
    assert formatter.normalize_record(unknown)['candidate_value'] is None
    assert formatter.normalize_record(dict(row('R','100R'),tolerance=None))['candidate_value'] is None
    checks.append('Explicit display policy may differ from preserved source tolerance; no implicit1% or TBD approval')
    doc=formatter.normalize_document([row('R','100R'),dict(row('R','1K'),ref='test1')])
    assert doc['summary']=={'records':2,'ready':0,'review_needed':2}
    checks.append('Duplicate references rejected instead of choosing one candidate')
    source=args.output/'source.json';candidate=args.output/'candidate.json'
    source.write_text(json.dumps({'metadata':{'keep':True},'records':[examples[0][0],incomplete]}),encoding='utf-8')
    before=source.read_bytes()
    command=[sys.executable,str(Path(formatter.__file__)),'--input',str(source),'--output',str(candidate),'--fail-on-review']
    completed=subprocess.run(command,capture_output=True,text=True)
    assert completed.returncode==2 and source.read_bytes()==before
    result=json.loads(candidate.read_text(encoding='utf-8'));assert result['input_metadata']=={'metadata':{'keep':True}}
    old=candidate.read_bytes();again=subprocess.run(command,capture_output=True,text=True)
    assert again.returncode==1 and candidate.read_bytes()==old
    checks.append('Real CLI writes review report, keeps source bytes and rejects output overwrite')
    assert all(r['candidate_value'] is None or r['candidate_value'].isascii() for r in result['records'])
    checks.append('Every non-null candidate is ASCII')
    report={'status':'PASS_SYNTHETIC_RC_FORMATTER_FIXTURES','checks':checks,'CAD_started':False,'user_library_accessed':False}
    (args.output/'report.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(report))


if __name__=='__main__':
    main()
