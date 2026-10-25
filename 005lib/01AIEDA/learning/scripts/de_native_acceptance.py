"""Compare native readback with the reviewed circuit and run explicit custom rules.

This is not Capture GUI ERC. Input CAD is never modified by this program.
"""
from pathlib import Path
from collections import Counter
import csv,copy,hashlib,json
root=Path(__file__).resolve().parents[1]
base=root/'examples/de_15_26_20261019';logs=root/'logs/de_15_26_20261019'
def rows(name):
    with (logs/name).open(encoding='utf-8-sig',newline='') as f:return list(csv.DictReader(f,delimiter='\t'))
checks=[]
def check(label,passed,detail=None):checks.append(dict(check=label,passed=bool(passed),detail=detail))
def rules(net):
    failures=[]
    def must(test,name):
        if not test:failures.append(name)
    for p in ('1','24','36','48'):must(net.get(('U1',p))=='V3V3','MCU_DIGITAL_SUPPLY')
    for p in ('8','23','35','47'):must(net.get(('U1',p))=='GND','MCU_GROUND')
    must(net.get(('U1','9'))=='VDDA','MCU_ANALOG_SUPPLY')
    must(net.get(('U2','1'))=='GND' and net.get(('U2','3'))=='VIN_PROT','BUCK_INPUT_GROUND')
    must(net.get(('U2','2'))=='BUCK_SW' and net.get(('U2','6'))=='BUCK_BOOT','BUCK_SWITCH_BOOT')
    must(net.get(('U3','1'))=='V5' and net.get(('U3','3'))=='V5' and net.get(('U3','5'))=='V3V3','LDO_RAILS')
    must(net.get(('J2','A4_B9'))=='USB_VBUS' and net.get(('J2','B4_A9'))=='USB_VBUS','USB_VBUS_ISOLATION')
    for p in ('A6','B6'):must(net.get(('J2',p))=='USB_DP','USB_DP_CONTACT_PAIR')
    for p in ('A7','B7'):must(net.get(('J2',p))=='USB_DM','USB_DM_CONTACT_PAIR')
    must(net.get(('R3','1'))=='USB_CC1' and net.get(('R3','2'))=='GND','USB_CC1_RD')
    must(net.get(('R4','1'))=='USB_CC2' and net.get(('R4','2'))=='GND','USB_CC2_RD')
    must(net.get(('Q1','1'))=='VBUS_GATE' and net.get(('Q1','2'))=='GND' and net.get(('Q1','3'))=='VBUS_PRESENT_N','VBUS_MOS_ISOLATION')
    must(net.get(('Q2','1'))=='USB_ATTACH_N' and net.get(('Q2','2'))=='V3V3' and net.get(('Q2','3'))=='USB_PULLUP_SRC','USB_ATTACH_SWITCH')
    must(('U5','5') not in net and ('U5','8') not in net,'TCAN332_NC')
    must(net.get(('Y1','1'))=='OSC_IN' and net.get(('Y1','3'))=='XTAL_OUT' and net.get(('Y1','2'))==net.get(('Y1','4'))=='GND','CRYSTAL_PIN_MAPPING')
    must(net.get(('R32','1'))=='ADC_IN' and net.get(('R32','2'))=='ADC0' and net.get(('C24','1'))=='ADC0' and net.get(('C24','2'))=='GND','ADC_RC')
    must(net.get(('U1','34'))=='SWDIO' and net.get(('U1','37'))=='SWCLK' and net.get(('J9','5'))=='NRST','SWD_RESET')
    return sorted(set(failures))
summaries={}
for tag,filename in [('single','integrated_circuit.json'),('eco','integrated_circuit_eco.json')]:
    spec=json.loads((base/filename).read_text(encoding='utf-8'))
    components={c['ref']:c for c in spec['components']}
    instances=rows('instances_'+tag+'.tsv');pins=rows('pins_'+tag+'.tsv');connections=rows('connectivity_'+tag+'.tsv')
    properties={(r['reference'],r['property']):r['value'] for r in rows('properties_'+tag+'.tsv')}
    actual={(p['reference'],p['number']):p['net'].upper() for p in connections}
    expected={(c['ref'],str(p)):n.upper() for c in spec['components'] for p,n in c['pins'].items() if n}
    check(tag+': exact connected pin map',actual==expected,dict(expected=len(expected),actual=len(actual)))
    check(tag+': no duplicate pin memberships',len(connections)==len(actual))
    check(tag+': complete unique references',len(instances)==len({x['reference'] for x in instances})==80 and {x['reference'] for x in instances}==set(components))
    check(tag+': physical pins complete',len(pins)==272 and len({(p['reference'],p['number']) for p in pins})==272)
    for i in instances:
        c=components[i['reference']];model=spec['models'][c['model']]
        for field,expected_value in [('module_id',c['id']),('value',c['value']),('footprint',model['footprint']),('mpn',c['mpn'])]:
            check(tag+': '+i['reference']+' '+field,i[field]==expected_value)
        for key,expected_value in [('ASSEMBLY',c['populate']),('MPN_STATUS',c['properties']['MPN_STATUS'])]:
            check(tag+': '+i['reference']+' '+key,properties[(i['reference'],key)]==expected_value)
    for p in pins:
        c=components[p['reference']];entry=next(q for q in spec['models'][c['model']]['pins'] if q['number']==p['number'])
        check(tag+': '+p['reference']+'.'+p['number']+' type/name/NC',p['name']==entry['name'] and int(p['type'])==entry['type'] and int(p['nc'])==int(c['pins'][p['number']] is None))
    check(tag+': explicit topology rules',not rules(actual),rules(actual))
    summaries[tag]=dict(components=len(instances),physical_pins=len(pins),connected_pins=len(actual),nets=len(set(actual.values())),explicit_NC=sum(int(p['nc']) for p in pins),custom_rule_failures=rules(actual))
    if tag=='single':baseline=actual
    else:eco=actual
changes={ref+'.'+num:[baseline.get((ref,num)),eco.get((ref,num))] for ref,num in set(baseline)|set(eco) if baseline.get((ref,num))!=eco.get((ref,num))}
check('ECO exact net differences',changes=={'J13.7':['GPIO_PB8','GPIO_PB9'],'J13.8':['GPIO_PB9','GPIO_PB8']},changes)
negative_cases=[]
for name,key,value,expected_rule in [('VDD48_to_GND',('U1','48'),'GND','MCU_DIGITAL_SUPPLY'),('VBUS_to_board_V5',('J2','A4_B9'),'V5','USB_VBUS_ISOLATION'),('CC2_RD_to_V3V3',('R4','2'),'V3V3','USB_CC2_RD'),('TCAN_NC8_connected',('U5','8'),'V3V3','TCAN332_NC')]:
    altered=copy.deepcopy(baseline);altered[key]=value;detected=rules(altered)
    check('custom rule negative example: '+name,expected_rule in detected,detected)
    negative_cases.append(dict(name=name,expected=expected_rule,detected=detected,scope='Fault injected into a readback-table copy, not into native CAD'))
result=dict(date='2026-10-19 Asia/Shanghai',scope='Native readback comparison and explicitly enumerated custom electrical/topology rules; NOT Capture GUI ERC or hardware validation',status='PASS' if all(c['passed'] for c in checks) else 'FAIL',checks=len(checks),passed=sum(c['passed'] for c in checks),summaries=summaries,negative_cases=negative_cases,details=checks)
(logs/'native_acceptance.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({k:result[k] for k in ('status','checks','passed','summaries')},ensure_ascii=True))
if result['status']!='PASS':raise SystemExit(1)
