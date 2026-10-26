# 更换公共封装时区分旧焊盘与板级热连接铜

适用情形：替换标准封装后，引脚和原有铜之间的实际连接分区已保持，但逐条源走线的完整铜覆盖检查仍发现差异。

不能仅根据“原线对象找不到”恢复全部旧铜，也不能仅凭连接数量相同就判定制造铜完整相同。应先取实际原生对象和铜形状。

1. 保护源板和候选板的 SHA。在源板读取实际线段 `objType`、完整属性、父链，以及它是否出现在元件图形的 children graph。区分手工走线、`thermal=t` 的热连接路径、`symbolEtch` 和普通焊盘。
2. 用 `axlPolyFromDB` 获取源实际线段的完整圆端铜；用实际源 pin 的 `REGULAR` 铜获取旧焊盘。层、旋转、镜像由原生 API 处理，不用 bbox 或估计矩形替代。
3. 将原生多边形精确复制为 detached poly，再在脚本顶层打开候选副本。不要在 SKILL 回调内反复调用 `axlOpenDesignForBatch` 切板。
4. 对每条原线计算 `missing = 源线实际铜 ANDNOT 候选同网全部实际铜`。再计算 `external = missing ANDNOT 旧实际焊盘铜`。
5. 旧焊盘内部的 missing 需要绑定已批准的封装几何变更及当前公共 PSM/PAD 的完整原生证据。不要通过补回旧 land 抵消标准封装的变更。
6. 旧焊盘外的源铜缺片应单独处理。若需要恢复，只恢复 `external`，保证它仍是源实际铜的子集且与旧焊盘没有正面积交集。创建前和创建后都检查实际异网铜交集；不能用 bbox 或统一数值阈值放行。
7. 允许在工程中创建同网、板级静态铜形状以保留这些源铜，不更改公共封装。每个创建形状与请求的原生源片须进行双向 ANDNOT，两个方向均为空。
8. 保存候选前，检查全部缓存封装/焊盘/自定义图形/字体属性不变，全部 typed pin、via、元件位置、文本和属性不变，DRC 和动态填充模式不变。保存后必须用新进程重新核对完整实际连接分区与规则；数量相等不能代替成员相等。

本轮 0010 的证据：25 条源线均为板级 `thermal=t`、`symbolEtch=nil`、无用户属性的热连接路径，涉及 11 个 0603 器件。原生计算发现总缺铜 1.06347277538932802 mm²，其中 0.882277921363270238 mm² 在旧 land 内；另有 21 片、0.181194854026057782 mm² 在旧 land 外。旧 land 全包含检查的真实 FAIL 保存在 `public0010_source25_owner_probe_run13_v2`，不能改称 PASS。

裁切薄片直接建 shape 的实际试验未通过：`public0010_external_thermal_restore_run13_v3` 中，第一片创建成功，但数据库重建的曲线/顶点与请求薄片的双向 ANDNOT 不为空。失败保留，不能通过全局数值容差将其改称一致。

针对本用例的有限决定在 `FINITE_SOURCE_THERMAL_PATH_RESTORE_DECISION27.json`：仅对同一 21 个 key，改为用 `axlDB2Path` 复制源板实际单段热连接路径，再用 `axlDBCreatePath` 重建可由数据库精确表达的源路径。允许这 21 条真实板级线路恢复部分原先位于旧焊盘内的线路铜；不复制旧焊盘图形，不处理另外 4 个纯旧 land 差异项。重新创建的路径可能是静态 board-owned path，必须记录实际 `thermal` 标志，不能称它仍是原生动态热连接。

原生可能把新线和现有同网线合并，不能将合并后的长路径全部当成新增铜。应对完整受影响网的实际铜验证 `after = before UNION source21`，同时要求无旧铜丢失、无源路径和既有铜以外的新增铜，并保持实际异网铜交集为零。此次 `public0010_original_thermal_restore_bundle13_v4` 实现此有限方案；v5 保存待独立复核的私有候选 `07A0F9340CBC89718BD586DEFCC270E299E24242C6AA7A6FA78973C220E82A42`。实际 21 次恢复返回 24 个 native path 对象，`thermal` 均为 nil，因此如实记作板级静态路径。

v5 的实际完整三网铜并集门通过；`FINITE_ORIGINAL21_THERMAL_CU_REVIEW_V5.json` 含 14 个破坏反控。保存后的独立重开 `w/module0010_final_full28` 又通过全 79 缓存定义的严格 typed ID 双射门，保留所有 20080 个对象、554973 个递归值及完整未知字段、属性、图形和字体字段。10 个缓存破坏反控全部拒绝。完整 2698 脚、593 个符号、915 个实际连接分区、全部规则和 70 个在用模板/4 个新焊盘制造 XML 由独立门验证；正式发布仍需绑定其发布收据，不能仅凭本方法文件认定已发布。

缓存比较有两类运行期陷阱。`pad:` 用户类型不能直接作为 assoc table 的 key，可用原生完整 ID 字符串；刷新或重开后 `pad:`、`propList:`、原生图形 handle 的地址可能变化，不能按 raw 地址变化断言制造几何改变，也不能忽略全部地址字段。应建立显式一一对应，逐字段核对全部原生数据。跨进程的图外 `instances` 和唯一 design parent 也只能按明确类型映射，并分别由全部实际符号/引脚身份门和完整规则门约束。此次实际缓存为 79 个定义，其中 70 个在用、9 个未使用；退休别名检查必须枚举 `design()->symdefs` 全部定义，不能只导出放置器件的 70 个。

`axlDBCloak` 会捕获内部 SKILL 错误并返回 nil。出现批量计数不符时，不能直接修改计数条件。先使用持久逐 key 日志和 `errset(... t)` 暴露首个真实 native 错误；必要时按官方建议在受保护副本直接调用调试，失败不保存。

可复用脚本为 `prepare_public0010_source25_probe_v1.py`、`prepare_public0010_source25_probe_v2.py`、`review_public0010_source25_thermal_failure_v2.py`、`prepare_public0010_original_thermal_restore_v4.py`、`prepare_public0010_original_thermal_restore_v5_pending.py`、`review_public0010_original_thermal_restore_v5.py`、`review_native_cache_id_bijection_fresh_v3.py` 和 `test_native_cache_fresh_bijection_v3.py`。具体板级硬计数、有限范围决定和输入 SHA 属于该工程用例，复用于其他工程时必须重新冻结，不能沿用。
