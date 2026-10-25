import pathlib,json
R=pathlib.Path(r'D:\001DIY\005lib\01AIEDA\learning\examples\lesson29_constraints_20261019')
p=R/'constraint_plan_preparation.json';d=json.loads(p.read_text())
d['basis']={
'default':'Teaching conservative minimum0.20mm width and0.20mm spacing; comfortably above the documented selected-board process limits. Not a current-density/thermal certification.',
'POWER_INPUT':'9-16V regulated bench input;500mA fuse.0.60mm trunk and0.30mm clearance are routing allocations, not mains creepage or unlimited fault-current proof.',
'POWER_LV':'150mA total normal V3V3 load and bounded external10mA;0.60mm distribution trunk, short necks independently checked. Copper pours/return and thermal/voltage-drop review remain layout work.',
'SWITCHING':'TPS54202 SW and BOOT must be compact; keep the BUCK_SW area small.1mm class-to-class separation from ADC/FB/oscillator is a project isolation allocation, not an EMI pass threshold.',
'ANALOG_SENSITIVE':'ADC_IN,ADC0 and BUCK_FB are physically sensitive. Additional separation from high-dV/dt nodes; do not split GND underneath them.',
'OSCILLATOR':'OSC_IN,OSC_OUT,XTAL_OUT kept compact with no gratuitous vias or matched-length meanders. Load capacitance budget depends on actual placement/parasitics.',
'USB_FS':'USB4105 and USBLC6 flow-through; actual DP/DM net identity kept through duplicated connector pads and ESD same-channel equivalent pins. Create USB connector side and MCU short-side diffpairs separately because22R splits nets; DNP CAN branches remain physical stubs to assess.',
'CAN_BUS':'TCAN332 short bench CAN500kbps max1m; CAN_H/L can be paired for routing symmetry but do not inherit USB90ohm or USB phase automatically.',
'USB_AUX':'VBUS sense only, separate from V5/V3V3. CC Rd and VBUS do not become members of the USB data pair.',
'DIGITAL_GENERAL':'3V3 UART/I2C100k/SPI<=1MHz and SWD; classify by source/edge/topology where needed. No unsupported global equal-length/max-delay constraint.',
'local_exceptions':'VDDA separate physical CSet0.30mm due analog branch; V3V3 and power escape necks have explicit reduced width and maximum neck length. Temporary net-width override and optional region escape demonstrated only in controlled challenge then rolled back.',
'USB_limits':'90ohm target follows general USB design intent; actual W/S requires manufacturer stackup and calculation/confirmation. Do not copy TI SoC-specific AppendixA numeric timing limits to STM32F103.',
}
d['online_primary_sources']=[
{'url':'https://www.st.com/resource/en/application_note/an4879-introduction-to-usb-hardware-and-pcb-guidelines-using-stm32-mcus-stmicroelectronics.pdf','version':'Rev12 June2026','used_pages':[4,10,13,14,21,24],'status':'Read through web PDF; shell download HTTP567 retained. Current document no longer includes old PCB-length chapter. No old layout number treated as current hard requirement.'},
{'url':'https://www.ti.com/video/6087491555001','title':'Layout basics for USB designs','used':'General90ohm target and PCB/return/short symmetric routing concepts; video HS examples not F103-specific compliance constraints.'},
{'url':'https://www.ti.com/lit/an/spraar7j/spraar7j.pdf','version':'RevJ Feb2023','used_pages':[6,8,9,10,14],'used':'Reference continuity, local matching and symmetric route/connector/ESD concepts. SoC-specific tables not copied.'}
]
p.write_text(json.dumps(d,indent=2),encoding='utf8')
print('basis recorded')
