from pathlib import Path
import json, math
root=Path(__file__).resolve().parents[1]
out=root/'examples'/'de_15_26_20261019'; out.mkdir(parents=True,exist_ok=True)
parts={
'TPS54202DDCR':{'package':'SOT23-6 DDC','pins':{'1':['GND','POWER'],'2':['SW','OUTPUT'],'3':['VIN','POWER'],'4':['FB','INPUT'],'5':['EN','INPUT'],'6':['BOOT','PASSIVE']},'source':'https://www.ti.com/lit/ds/symlink/tps54202.pdf','source_page':3},
'TLV75533PDBVR':{'package':'SOT23-5 DBV','pins':{'1':['IN','POWER'],'2':['GND','POWER'],'3':['EN','INPUT'],'4':['NC','NC'],'5':['OUT','POWER']},'source':'https://www.ti.com/lit/ds/symlink/tlv755p.pdf','source_page':3},
'TCAN332DR':{'package':'SOIC-8 D','pins':{'1':['TXD','INPUT'],'2':['GND','POWER'],'3':['VCC','POWER'],'4':['RXD','OUTPUT'],'5':['NC5','NC'],'6':['CANL','BIDIR'],'7':['CANH','BIDIR'],'8':['NC8','NC']},'source':'https://www.ti.com/lit/ds/symlink/tcan332.pdf','source_page':4},
'USBLC6-2SC6':{'package':'SOT23-6L','pins':{'1':['IO1A','PASSIVE'],'2':['GND','POWER'],'3':['IO2A','PASSIVE'],'4':['IO2B','PASSIVE'],'5':['VBUS','POWER'],'6':['IO1B','PASSIVE']},'source':'https://www.st.com/resource/en/datasheet/usblc6-2.pdf','source_page':1,'internal_pin_equivalence':[['1','6'],['3','4']]},
'2N7002':{'package':'SOT23','pins':{'1':['G','INPUT'],'2':['S','PASSIVE'],'3':['D','PASSIVE']},'source':'https://assets.nexperia.com/documents/data-sheet/2N7002.pdf','source_page':1},
'DMP2035U-7':{'package':'SOT23','pins':{'1':['G','INPUT'],'2':['S','PASSIVE'],'3':['D','PASSIVE']},'source':'https://www.diodes.com/datasheet/download/DMP2035U.pdf','source_page':1},
'SS14-E3/61T':{'package':'SMA DO-214AC','pins':{'1':['K','PASSIVE'],'2':['A','PASSIVE']},'source':'https://www.vishay.com/docs/88746/ss12.pdf','source_page':1,'pin_numbering':'local schematic/footprint convention 1=banded cathode, 2=anode; manufacturer uses A/K'},
'XAL6060-153MEC':{'package':'de_xal6060_2land','pins':{'1':['SW_END','PASSIVE'],'2':['OUT_END','PASSIVE']},'source':'https://www.coilcraft.com/getmedia/ea51f14b-7f32-4dc6-8dfe-d4b70549040f/xal60xx.pdf','source_page':[1,4],'pin_numbering':'local convention 1=manufacturer marked right short-lead high-dv/dt end (+2.02mm), 2=other end (-2.02mm)','body_mm':[6.36,6.56],'body_tolerance_mm':0.2,'height_max_mm':6.1,'land_mm':[1.43,5.50],'land_center_distance_mm':4.04,'DCR_max_25C_ohm':0.04375,'Isat_25C_typ_30pct_L_drop_A':5.8,'Irms_20C_rise_A':4.5,'Irms_40C_rise_A':6.0},
'USB4105-GF-A':{'package':'l10_gct_usb4105_gf_a_12land','pins':{'A1_B12':['GND1','PASSIVE'],'A4_B9':['VBUS1','PASSIVE'],'B8':['SBU2','NC'],'A5':['CC1','PASSIVE'],'B7':['DM2','BIDIR'],'A6':['DP1','BIDIR'],'A7':['DM1','BIDIR'],'B6':['DP2','BIDIR'],'A8':['SBU1','NC'],'B5':['CC2','PASSIVE'],'B4_A9':['VBUS2','PASSIVE'],'B1_A12':['GND2','PASSIVE'],'SH1':['SHELL1','PASSIVE'],'SH2':['SHELL2','PASSIVE'],'SH3':['SHELL3','PASSIVE'],'SH4':['SHELL4','PASSIVE']},'source':'https://gct.co/files/drawings/usb4105.pdf','source_page':1,'pin_numbering':'B10 validated 12 copper land model combining four VBUS/GND contact pairs plus four tool-defined shell pins; not generic 16-contact numbering'},
}
components=[]
def add(ref,kind,value,pins,**kw):
 components.append(dict(ref=ref,kind=kind,value=value,pins={str(k):v for k,v in pins.items()},populate='yes',**kw))
def two(ref,kind,value,a,b,**kw): add(ref,kind,value,{'1':a,'2':b},**kw)
add('J_PWR','HEADER2','9-16V DC IN',{'1':'VIN_RAW','2':'GND'},page='POWER',rating='>=24V >=0.5A connector, exact MPN before mechanical release')
two('F_IN','FUSE','500mA fast 32VDC','VIN_RAW','VIN_FUSED',page='POWER',mpn='0467.500NR',footprint_family='0603',source='https://www.littelfuse.com/assetdocs/fuse-467-datasheet?assetguid=4a59f034-1cca-460e-a5ba-e1e66247c76d',release_note='secondary protection only; inrush and I2t coordination not measured')
add('D_REV','SS14-E3/61T','SS14',{'1':'VIN_PROT','2':'VIN_FUSED'},page='POWER',rating='40V VRRM 1A; local pin1=K pin2=A')
two('C_IN_BULK','CAP_POL','47uF 35V','VIN_PROT','GND',page='POWER',rating='electrolytic ESR provides source-cable resonance damping; polarity pin1+')
two('C_IN','CAP','22uF 35V X7R','VIN_PROT','GND',page='POWER',rating='effective >=10uF at16V including tolerance/temp/DC bias')
two('C_IN_HF','CAP','100nF 50V X7R','VIN_PROT','GND',page='POWER')
add('U_BUCK','TPS54202DDCR','TPS54202',{'1':'GND','2':'BUCK_SW','3':'VIN_PROT','4':'BUCK_FB','5':None,'6':'BUCK_BOOT'},page='POWER',nc_reason={'5':'datasheet permits float EN for enabled; never connect directly to VIN_PROT'})
two('C_BOOT','CAP','100nF 16V X7R','BUCK_BOOT','BUCK_SW',page='POWER')
two('L_BUCK','XAL6060-153MEC','15uH +/-20%','BUCK_SW','V5',page='POWER',mpn='XAL6060-153MEC',rating='DCRmax43.75mohm@25C, Isat5.8A typ (30% L drop), Irms4.5A at20C rise; covers nominal120mA and is above TPS54202 current-limit maximum3.9/4.3A at25C; temperature/current curves and actual PCB heat remain validation')
two('C5_A','CAP','22uF 10V X7R','V5','GND',page='POWER',rating='pair effective >=30uF total at5V; verify selected MPN bias data; Cff75pF starting value requires stability test')
two('C5_B','CAP','22uF 10V X7R','V5','GND',page='POWER',rating='same as C5_A')
two('R_FB_HI','RES','100k 0.1%','V5','BUCK_FB',page='POWER')
two('R_FB_LO','RES','13.5k 0.1%','BUCK_FB','GND',page='POWER')
two('C_FF','CAP','75pF C0G','V5','BUCK_FB',page='POWER',rating='feedforward across upper FB resistor; official 5V low-ESR starting point, verify loop after actual C/L selected')
add('U_LDO','TLV75533PDBVR','TLV75533P',{'1':'V5','2':'GND','3':'V5','4':None,'5':'V3V3'},page='POWER',nc_reason={'4':'NC, no internal connection'})
two('C_LDO_IN','CAP','2.2uF 10V X7R','V5','GND',page='POWER',rating='effective >=0.47uF worst case; pin-local')
two('C_LDO_OUT','CAP','4.7uF 10V X7R','V3V3','GND',page='POWER',rating='effective >=0.47uF worst case; pin-local')
add('J_USB','USB4105-GF-A','USB-C USB2 DEVICE',{'A1_B12':'GND','A4_B9':'USB_VBUS','B8':None,'A5':'USB_CC1','B7':'USB_DM','A6':'USB_DP','A7':'USB_DM','B6':'USB_DP','A8':None,'B5':'USB_CC2','B4_A9':'USB_VBUS','B1_A12':'GND','SH1':'GND','SH2':'GND','SH3':'GND','SH4':'GND'},page='USB_CAN',nc_reason={'B8':'SBU2 unused','A8':'SBU1 unused'},layout='signal ground and shell stakes bonded at connector; enclosure chassis absent in bench design')
two('R_CC1','RES','5.1k 1%','USB_CC1','GND',page='USB_CAN')
two('R_CC2','RES','5.1k 1%','USB_CC2','GND',page='USB_CAN')
add('U_USB_ESD','USBLC6-2SC6','USBLC6-2SC6',{'1':'USB_DP','2':'GND','3':'USB_DM','4':'USB_DM','5':'USB_VBUS','6':'USB_DP'},page='USB_CAN',layout='connector -> ESD flow-through pads -> matched short route -> MCU series resistors; shortest wide local ESD GND return')
two('C_USB_VBUS','CAP','100nF 10V X7R','USB_VBUS','GND',page='USB_CAN',rating='no board power from USB VBUS; cap supplies ESD rail HF return')
two('R_USB_DP','RES','22R 1%','PA12_SHARED','USB_DP',page='USB_CAN',assembly_group='USB_ONLY')
two('R_USB_DM','RES','22R 1%','PA11_SHARED','USB_DM',page='USB_CAN',assembly_group='USB_ONLY')
two('R_VBUS_GATE','RES','10k 1%','USB_VBUS','VBUS_GATE',page='USB_CAN')
two('R_VBUS_GPD','RES','1M 1%','VBUS_GATE','GND',page='USB_CAN')
add('Q_VBUS','2N7002','2N7002',{'1':'VBUS_GATE','2':'GND','3':'VBUS_PRESENT_N'},page='USB_CAN')
two('R_VBUS_READ','RES','10k 1%','V3V3','VBUS_PRESENT_N',page='USB_CAN')
add('Q_ATTACH','DMP2035U-7','DMP2035U',{'1':'USB_ATTACH_N','2':'V3V3','3':'USB_PULLUP_SRC'},page='USB_CAN')
two('R_ATTACH_OFF','RES','100k 1%','V3V3','USB_ATTACH_N',page='USB_CAN')
two('R_DP_PULLUP','RES','1.5k 1%','USB_PULLUP_SRC','USB_DP',page='USB_CAN')
add('U_CAN','TCAN332DR','TCAN332',{'1':'CAN_TXD','2':'GND','3':'V3V3','4':'CAN_RXD','5':None,'6':'CAN_L','7':'CAN_H','8':None},page='USB_CAN',nc_reason={'5':'TCAN332 NC, not SHDN','8':'TCAN332 NC, not STB'})
two('C_CAN','CAP','100nF 10V X7R','V3V3','GND',page='USB_CAN')
two('C_CAN_BULK','CAP','1uF 10V X7R','V3V3','GND',page='USB_CAN')
two('R_CAN_TX','RES','0R','PA12_SHARED','CAN_TXD',page='USB_CAN',assembly_group='CAN_ONLY')
two('R_CAN_RX','RES','0R','PA11_SHARED','CAN_RXD',page='USB_CAN',assembly_group='CAN_ONLY')
two('R_CAN_TX_IDLE','RES','10k','V3V3','CAN_TXD',page='USB_CAN',rating='explicit recessive default complements internal pull-up; no output contention at3.3V')
two('R_CAN_TERM','RES','120R 1% >=0.25W','CAN_H','CAN_L',page='USB_CAN',assembly_group='END_NODE_ONLY',rating='fit at physical two bus ends only; DNP for intermediate node')
add('J_CAN','HEADER3','CAN 500kbps <=1m BENCH',{'1':'CAN_H','2':'CAN_L','3':'GND'},page='USB_CAN')
add('J_UART','HEADER4','3V3 UART',{'1':'V3V3','2':'UART_TX','3':'UART_RX','4':'GND'},page='INTERFACES',rating='V3V3 is OUT/reference <=10mA combined connector load; no external power injection')
two('R_UART_TX','RES','33R','PA9_UART_TX','UART_TX',page='INTERFACES',layout='source damping footprint near MCU; final value requires edge/receiver/cable check')
two('R_UART_RX','RES','0R','PA10_UART_RX','UART_RX',page='INTERFACES')
two('R_UART_IDLE','RES','10k','UART_RX','V3V3',page='INTERFACES')
add('J_I2C','HEADER4','3V3 I2C <=400kHz <=100pF',{'1':'V3V3','2':'I2C_SCL','3':'I2C_SDA','4':'GND'},page='INTERFACES',rating='short bench interconnect; no hot plug; <=10mA total header load')
two('R_I2C_SCL','RES','2.2k 1%','V3V3','I2C_SCL',page='INTERFACES')
two('R_I2C_SDA','RES','2.2k 1%','V3V3','I2C_SDA',page='INTERFACES')
add('J_SPI','HEADER6','3V3 SPI <=1MHz <=10cm',{'1':'V3V3','2':'SPI_SCK','3':'SPI_MOSI','4':'SPI_MISO','5':'SPI_NSS','6':'GND'},page='INTERFACES',rating='exact receiver setup/hold and edge spec needed before faster/longer interface')
two('R_SPI_SCK','RES','33R','PA5_SPI_SCK','SPI_SCK',page='INTERFACES')
two('R_SPI_MOSI','RES','33R','PA7_SPI_MOSI','SPI_MOSI',page='INTERFACES')
two('R_SPI_NSS','RES','33R','PA4_SPI_NSS','SPI_NSS',page='INTERFACES')
two('R_SPI_MISO','RES','0R','PA6_SPI_MISO','SPI_MISO',page='INTERFACES')
two('R_SPI_NSS_PU','RES','10k','V3V3','PA4_SPI_NSS',page='INTERFACES')
for c in components:
 if c.get('assembly_group')=='CAN_ONLY': c['populate']='DNP default USB mode'
spec={
 'date':'2026-10-19','scope':'D/E integrated isolated learning design; not fabrication release; root MCU net naming must explicitly map aliases',
 'parts':parts,'components':components,
 'mcu_aliases':{'PA12_SHARED':'MCU PA12 / USB_DP / CAN_TX','PA11_SHARED':'MCU PA11 / USB_DM / CAN_RX','PA9_UART_TX':'MCU PA9 USART1_TX','PA10_UART_RX':'MCU PA10 USART1_RX','I2C_SCL':'MCU PB6 I2C1_SCL','I2C_SDA':'MCU PB7 I2C1_SDA','PA4_SPI_NSS':'MCU PA4 SPI1_NSS','PA5_SPI_SCK':'MCU PA5 SPI1_SCK','PA6_SPI_MISO':'MCU PA6 SPI1_MISO','PA7_SPI_MOSI':'MCU PA7 SPI1_MOSI','VBUS_PRESENT_N':'MCU PB0 INPUT active low','USB_ATTACH_N':'MCU PA8 OUTPUT active low; reset pull-up -> detach'},
 'assembly_profiles':{'USB':{'fit':['R_USB_DP','R_USB_DM'],'DNP':['R_CAN_TX','R_CAN_RX'],'firmware':'enable USB only, PB0=0 and V3V3 valid then PA8=0; PB0=1 => PA8=1. At reset Q_ATTACH off.'},'CAN':{'fit':['R_CAN_TX','R_CAN_RX'],'DNP':['R_USB_DP','R_USB_DM'],'firmware':'enable CAN only, PA8 always high; USB and CAN share MCU SRAM and cannot operate simultaneously even with remapping'}},
 'supply_limits':{'input_V':[9,16],'V3V3_load_max_A':0.150,'ambient_C':[0,40],'header_combined_load_max_A':0.010,'external_GPIO_plus_header_load_max_A':0.010,'USB_VBUS':'sense+ESD only; must never connect to V5 or V3V3','no_external_backfeed':'SWD and headers are reference outputs only; probe Vtarget must sense, not power; TLV755 has no reverse blocking','current_budget_revision':'Final normal150mA/Ta0-40C supersedes initial120mA/Ta0-50C after MCU50mA+CAN60mA+external10mA leaves no pullup margin. Fault180mA not normal guarantee.','native_historical_L1_requirement':'L1 saved REQUIREMENTS still says covers nominal120mA as original design context; not inductor current rating. Actual Isat5.8A/Irms4.5A unchanged and final150mA load/thermal review controls. No native rerun needed.'},
 'normal_current_budget_mA':{'MCU_72MHz_all_peripherals_DS5319_Table13_max_85C':50.0,'TCAN332_dominant_RL50_max':60.0,'external_GPIO_plus_header_combined_ceiling':10.0,'two_I2C_pullups_2k2_minR_conservative':3.2,'other_bias_resistors_reserve':3.0,'analog_current_conservative_reserve':5.0,'internal_switching_unmodelled_reserve':5.0,'allocated_subtotal':136.2,'remaining_margin_to150':13.8,'USB_profile_total_including2V4mA_attach_reserve':82.1,'note':'Reserve rows are design allocations, not quoted IC specifications; CAN term load already included in transceiver ICC, not double-added.'},
 'I2C_operating_note':'Default100kHz. <=400kHz means RC design envelope only; DS5319Rev20 Table41 footnote2 and Table42 disagree on PCLK1 condition. Fast-mode hardware/firmware timing remains unverified.',
 'calculations':{'buck_V_nom':0.596*(1+100/13.5),'buck_V_min':0.581*(1+(100*.999)/(13.5*1.001)),'buck_V_max':0.611*(1+(100*1.001)/(13.5*.999)),'buck_deltaIL_at16V_15uH_500kHz_A':5*(1-5/16)/(15e-6*500e3),'ldo_P_at5V_150mA_W':(5-3.3)*.150,'ldo_rise_JEDEC_C_at5V_150mA':(5-3.3)*.150*231.1,'ldo_P_worst_150mA_W':(0.611*(1+(100*1.001)/(13.5*.999))-3.2505)*.150,'ldo_Tj_first_order_at40C_worst_150mA_C':40+(0.611*(1+(100*1.001)/(13.5*.999))-3.2505)*.150*231.1,'i2c_tr_2k2_100pF_ns':.8473*2200*100e-12*1e9,'i2c_Rmax_300ns_100pF_ohm':300e-9/(.8473*100e-12),'i2c_Rmin_3mA_3V465_0V4_ohm':(3.465-.4)/.003,'vbus_gate_at4V75_V':4.75*1e6/1.01e6,'vbus_sense_low_current_A':3.3/10000},
 'unpopulated_or_rejected':{'input_TVS':'No populated TVS: ST SMBJ16A VRWM16V but Vcl26V at10/1000us and34.4V at8/20us; latter exceeds TPS54202 abs30V. Not a surge-certified input. Optional review pads only if root explicitly adds DNP.','CAN_TVS':'No arbitrary SM712/24V TVS: TCAN332 bus abs +/-14V. Short nonautomotive bench, internal device IEC12kV ESD rating does not prove system compliance.','ferrite':'No default series ferrite/LC on whole V3V3; MCU analog RC supply review delegated to MCU lesson; verify DC drop/damping and supply ramp if added.','BSS84':'Replaced by DMP2035U with Rds guarantee at-2.5V; BSS84 current catalog Not for Design In and no low-Vgs Rds guarantee used here.'},
 'release_gates':['exact passive/connector/inductor MPN and DC-bias curves','buck loop response, load step, DCM ripple under minimum/maximum loads','fuse inrush/I2t and source limit coordination','LDO actual PCB temperature and input/output power-off slew/reverse-current test','USB attach/detach firmware behavior and compliance/ESD test','CAN bit timing, termination and bus-fault envelope','Capture ERC and native network output vs this spec; PCB import/ECO verified separately by root']}
(out/'power_interface_spec.json').write_text(json.dumps(spec,ensure_ascii=False,indent=2),encoding='utf-8')
print(f'{len(parts)} part definitions; {len(components)} components; '+str(out/'power_interface_spec.json'))
