import pathlib,json
H=pathlib.Path(r"D:\001DIY\005lib\01AIEDA\learning\examples\lessonHI_38_50_20261021")
n=json.loads((H/"inventory/normalized_actual_4L.json").read_text(encoding="utf-8"));print(json.dumps([{k:c[k] for k in("ref","xy","rotation","pins")} for c in n["placements"] if c["ref"] in("R21","R22","R24")],ensure_ascii=True))
