import pathlib,json
H=pathlib.Path(r"D:\001DIY\005lib\01AIEDA\learning\examples\lessonHI_38_50_20261021")
n=json.loads((H/"inventory/checkpoints/mcu_4L_b006/normalized.json").read_text(encoding="utf-8"))
print(list(n))
for key in("routes","vias","shapes"):print(key,len(n.get(key,[])),n.get(key,[])[:1])
