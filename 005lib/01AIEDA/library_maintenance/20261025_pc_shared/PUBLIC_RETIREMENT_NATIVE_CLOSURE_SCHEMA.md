# 旧别名退役前的八类实际引用闭环

此文件仅定义最终输入和输出约定，当前公共模块与工程 PCB 仍在独立校验，不能据此宣称零引用或执行删除。

最终 closure 必须绑定 `public_retirement_all_confirmed_plan13/PUBLIC_RETIREMENT_EXACT_PLAN.json` 的真实完整 SHA 及全部 1067 个旧 stem，每个 stem 都要明确列出下列八个整数计数，不能用缺字段代表零：

```json
{
  "status": "PASS_NATIVE_REFERENCE_CLOSURE",
  "retirement_plan_sha256": "<实际冻结计划SHA>",
  "covered_source_stems": ["<计划中全部1067个旧stem>"],
  "active_reference_counts": {
    "<每个旧stem>": {
      "project_capture": 0,
      "project_brd_declared": 0,
      "project_brd_placed": 0,
      "public_olb": 0,
      "public_dsn": 0,
      "public_brd_declared": 0,
      "public_brd_placed": 0,
      "active_device_map": 0
    }
  },
  "native_evidence": [{"path": "<实际证据绝对路径>", "sha256": "<完整SHA>"}],
  "canonical_target_proofs": [{"path": "<cold-native及完整PAD证明路径>", "sha256": "<完整SHA>"}]
}
```

以上示例的零只是输出格式说明，不是本工程的检查结果。`native_evidence` 至少应包含完整的最终来源覆盖清单、独立校验通过报告及原生实际引用提取记录，且各记录自身绑定实际设计／公共文件的完整 SHA。

|类别|必须覆盖的实际对象|可直接提取的原生字段|
|---|---|---|
|project_capture|最终保存重开 DSN，含全部 Cache 默认、Cell 默认、实例覆盖|完整 XML 的 `pcbFootprint`，及 `UserProp/Defn[@name='PCB Footprint']/@val`；不能只扫 1131 个实例|
|project_brd_declared|最终保存重开的全部组件声明，含未放置器件|原生 `components_full.ilist` 的 component package，或完整设备导出／PST 与实际板绑定的声明表|
|project_brd_placed|最终物理 symbol 和其真实缓存定义|原生 `symbols.tsv` 的 symbol 名／definition；另核完整 symdefs，避免导库再出现旧 unused 定义|
|public_olb|本机全部 37 个 OLB，含本次已精确发布的 13 个|同 Capture 属性提取；完整库对象／默认均覆盖，历史追溯 `FootprintName` 单列，不当 PCB Footprint 更新|
|public_dsn|本机两个 DSN|全部 Cache／实例 PCB Footprint；原生快照必须与当前实际源 SHA 绑定|
|public_brd_declared|本机全部七个 BRD，含未放置组件|逐板全 component package／真实设备声明，不能只统计 placed symbols|
|public_brd_placed|同七个 BRD 的全部物理对象|逐板原生 symbol／definition 及完整缓存集合；无修改的板也要有当前 SHA 对应证据|
|active_device_map|实际启用的 device／映射／环境和脚本入口|实际 PACKAGE／映射引用；本次将一起退役的精确 self-device TXT 单列并绑定删除清单，不能把备份文件误当启用映射|

来源覆盖应为工程 DSN／BRD 各一份、公共 OLB 37 份、公共 DSN 两份、公共 BRD 七份。最终公共文件集合以已批准 guard 为准，13 OLB 发布后 guard 从原 13433 文件清单显式替换 13 条 SHA／大小产生；后续公共 BRD 发布同样显式更新，不能用新扫描结果直接重置期望。

对于已发布文件，允许复用“候选库原生导出＋完整字节相同”的证明，但必须同时绑定实际公共文件的 SHA 与候选 SHA，并记录实际路径身份；这不是忽略根名称、跳过重开或接受任意同名 XML 的理由。COMMON 的真实公共路径已另有最终完整 59 对象门。

原生退出码零、同一份逻辑网表、相同铜并集或几何覆盖都不能代替公共 BRD 与工程 BRD 的完整物理、属性、约束、实际连接验收。候选板仍有独立校验回归时，不生成 `PASS_NATIVE_REFERENCE_CLOSURE`。所有旧别名零引用且目标 cold-native／完整 PAD 证明齐全后，才把最终 closure 交给精确退役器。
