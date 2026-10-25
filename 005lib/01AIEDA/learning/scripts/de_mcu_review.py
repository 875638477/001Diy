from pathlib import Path
import json, hashlib, math
ROOT=Path(__file__).resolve().parents[1]
EX=ROOT/'examples'/'de_15_26_20261019'
data=json.loads((EX/'mcu_spec.json').read_text(encoding='utf-8'))
pins={p['number']:p for p in data['pins']}
checks=[]
def check(name,ok,detail): checks.append({'check':name,'pass':bool(ok),'detail':detail})
check('48 unique physical pins',len(data['pins'])==48 and set(pins)==set(range(1,49)),'unique integers1..48, noEP49')
check('power numbers match visually inspected DS5319 Figure8',all(pins[n]['name']==name for n,name in {1:'VBAT',8:'VSSA',9:'VDDA',23:'VSS_1',24:'VDD_1',35:'VSS_2',36:'VDD_2',47:'VSS_3',48:'VDD_3'}.items()),'sourceDS5319 PDF26/36')
check('no invented external regulator or reference pins',not any(x in p['name'] for p in data['pins'] for x in ['VCAP','VREF','EP']),'LQFP48 VREFinternallyVDDA/VSSA; noexposedVCAP')
check('digital decoupling one per VDD pair',[(x['pin'],x['return_pin']) for x in data['supply']['digital_decoupling']]==[(24,23),(36,35),(48,47)],'actual3pairs notgeneric5pairs')
check('bulk explicitly on VDD3',data['supply']['bulk']['at_pin']==48,'DS5319 Figure14 caution')
check('USB and CAN selection exclusive',not data['interfaces']['USB_CAN_simultaneous'] and data['interfaces']['CAN_selected_pins']=={'RX':32,'TX':33} and all(pins[n]['proposed_net']==net for n,net in {32:'PA11_SHARED',33:'PA12_SHARED'}.items()),'physicalpinconflict+shared512BSRAM; noPB8/PB9remapselection')
check('SWD separate from normal interfaces',pins[34]['proposed_net']=='SWDIO' and pins[37]['proposed_net']=='SWCLK' and pins[7]['proposed_net']=='NRST','DS5319 PDF26/table5')
clk=data['clock']
loaded=clk['C1_C2_initial_pF']/2+clk['Cstray_assumed_pF']
gmcrit=4*clk['ESR_max_ohm']*(2*math.pi*clk['HSE_Hz'])**2*((clk['C0_max_pF']+clk['CL_pF'])*1e-12)**2
check('crystal load and small-signal startup calculation',abs(loaded-clk['CL_pF'])<1e-9 and abs(gmcrit-clk['gmcrit_S'])<1e-12 and clk['gm_min_S']/gmcrit>=5,{'load_pF':loaded,'gmcrit_mA_per_V':gmcrit*1000,'gain_margin':clk['gm_min_S']/gmcrit,'scope':'calculationonly; drive/startup/frequencytestopen'})
check('crystal top-view terminals and dimensions',[(p['number'],p['x_mm'],p['y_mm'],p['net']) for p in clk['crystal_pins_top_view']]==[(1,-2.0,-1.2,'OSC_IN'),(2,2.0,-1.2,'GND'),(3,2.0,1.2,'OSC_OUT'),(4,-2.0,1.2,'GND')],'AbraconABM3B PDF3 TOPVIEW visuallychecked; bottomviewnotcopied')
adc=data['ADC']; dt=(adc['source_output_max_ohm']+adc['series_R_ohm']+adc['Rsample_max_ohm'])*adc['Csample_max_F']*math.log(2**14)
check('ADC acquisition and slow external RC separately checked',adc['sample_time_s']>dt and 1/adc['sample_rate_teaching_Hz']>adc['input_RC_step_settling_to_quarterLSB_s'],{'internal_model_required_us':dt*1e6,'selected_sample_us':adc['sample_time_s']*1e6,'external_RC_step_ms':adc['input_RC_step_settling_to_quarterLSB_s']*1000,'period_ms':1000/adc['sample_rate_teaching_Hz'],'anti_alias_claim':False})
old=ROOT/'examples'/'lesson09_qfn_qfp_20261018'/'source'/'stm32f103c8_official.pdf'; new=ROOT/'sources'/'de_15_26_20261019'/'DS5319.pdf'
h=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
check('datasheet copy identical to B9 official archive',h(old)==h(new),{'original':str(old.relative_to(ROOT)),'copy':str(new.relative_to(ROOT)),'sha256':h(new)})
result={'date_client':'2026-10-19 Asia/Shanghai','scope':'MCUsource/specconsistencyreview; notnativeERC orhardwareacceptance','pass':all(c['pass'] for c in checks),'count':len(checks),'checks':checks,'data_sha256':h(EX/'mcu_spec.json'),'native_CAD':'recordedbyrootseparately','hardware_tests':'notperformed'}
(EX/'mcu_spec_review.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({'pass':result['pass'],'count':len(checks),'failures':[x for x in checks if not x['pass']]},ensure_ascii=True))
if not result['pass']:raise SystemExit(1)
