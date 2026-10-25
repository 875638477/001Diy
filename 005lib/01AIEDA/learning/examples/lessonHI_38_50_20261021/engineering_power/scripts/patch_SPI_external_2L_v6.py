from pathlib import Path
import json
R=Path(r'D:\001DIY\005lib\01AIEDA\learning\examples\lessonHI_38_50_20261021\engineering_power');p=json.loads((R/'SPI_external_2L_engineered_v6.json').read_text())
updates={
'SPI_SCK_EAST':dict(xy=[31.25,30.45]),'SPI_SCK_WEST':dict(xy=[21.4,30.05]),
'SPI_SCK_EAST_TOP':dict(points=[[32.0252,31],[31.8,31],[31.25,30.45]]),
'SPI_SCK_BOTTOM_BRIDGE':dict(points=[[31.25,30.45],[30.85,30.05],[21.4,30.05]]),
'SPI_SCK_WEST_TOP':dict(points=[[21.4,30.05],[16.1,30.05],[14.59,28.54],[7,28.54]]),
'SPI_MOSI_EAST':dict(xy=[31.7,26.2]),'SPI_MOSI_WEST':dict(xy=[14,28.8]),
'SPI_MOSI_BOTTOM_BRIDGE':dict(points=[[31.7,26.2],[30.4,27.5],[15.3,27.5],[14,28.8]]),
'SPI_MOSI_WEST_TOP':dict(points=[[14,28.8],[14,29.5],[12.42,31.08],[7,31.08]]),
'SPI_MISO_EAST':dict(xy=[31.5,29.15]),'SPI_MISO_WEST':dict(xy=[19.5,29.2]),
'SPI_MISO_EAST_TOP':dict(points=[[32.0252,29],[31.65,29],[31.5,29.15]]),
'SPI_MISO_BOTTOM_BRIDGE':dict(points=[[31.5,29.15],[31.45,29.2],[19.5,29.2]]),
'SPI_MISO_WEST_TOP':dict(points=[[19.5,29.2],[19.5,31.6],[17.48,33.62],[7,33.62]]),
'SPI_NSS_EAST':dict(xy=[29.7,32.65]),'SPI_NSS_WEST':dict(xy=[19,31.5]),
'SPI_NSS_EAST_TOP':dict(points=[[31.2236,33.02],[30.07,33.02],[29.7,32.65]]),
'SPI_NSS_BOTTOM_BRIDGE':dict(points=[[29.7,32.65],[28.55,31.5],[19,31.5]]),
'SPI_NSS_WEST_TOP':dict(points=[[19,31.5],[19,32.9],[15.74,36.16],[7,36.16]]),
'SPI_RETURN_G1A':dict(xy=[30.9,28.9]),'SPI_RETURN_G1B':dict(xy=[20.3,28]),
'SPI_RETURN_GMOSI_W':dict(xy=[14,30.8]),'SPI_RETURN_GMISO_E':dict(xy=[32.85,28.1]),
'SPI_RETURN_G2A':dict(xy=[26.6,30.9]),'SPI_RETURN_G2B':dict(xy=[20.3,30.85]),
'SPI_RETURN_G3A':dict(xy=[28.8,33.45]),'SPI_RETURN_G3B':dict(xy=[20.4,32.3]),
'SPI_RETURN_GNSS_E':dict(xy=[29.3,34.7]),
'SPI_GUARD_LOWER':dict(points=[[30.9,28.9],[30.4,28.4],[21,28.4],[20.3,28]],width=.6),
'SPI_GUARD_MID':dict(points=[[26.6,30.9],[26.5,30.8],[20.35,30.8],[20.3,30.85]],width=.6),
}
p['operations']=[o for o in p['operations'] if o['id']!='SPI_GUARD_UPPER']
for o in p['operations']:
 if o['id'] in updates:o.update(updates[o['id']])
(R/'SPI_external_2L_engineered_v6.json').write_text(json.dumps(p,indent=2),encoding='utf-8')