from pathlib import Path
import sys,json,math
H=Path(r'D:/001DIY/005lib/01AIEDA/learning/examples/lessonHI_38_50_20261021');sys.path.insert(0,str(H/'scripts'));from routing_geometry import *
O=H/'engineering_power';n=load(O/'N37_2L_snapshot.json');w=load(O/'N37_2L_networks.json');r=load(O/'N37_2L_rules.json');p=load(O/'N37_2L_policy.json');n['routes']=[a for a in n['routes'] if a['net']!='GPIO_PA3'];n['vias']=[a for a in n['vias'] if a['net']!='GPIO_PA3'];s=CopperScene(n,w,r,p)
for pts in [[[35.75,29.75],[34.75,29.75]],[[35.75,29.75],[34.5,29.75]],[[35.75,29.75],[34.75,29.75],[34.0,30.5]]]:
 line=LineString(pts).buffer(.1);print('TEST',pts,s.path_clear('GPIO_PA3','TOP',pts,.2));print([(a['net'],a['source'],round(line.distance(a['geometry']),4),a['geometry'].bounds) for a in s.obstacles if a['layer']=='TOP' and a['net']!='GPIO_PA3' and line.distance(a['geometry'])<.2])