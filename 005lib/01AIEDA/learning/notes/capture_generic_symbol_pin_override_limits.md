# Capture 17.2 generic symbols and instance pin override limits

A shared graphic template is safe only when its physical pin schema, electrical types, shared/global/no-connect flags and downstream netlist behavior have been checked. A matching land pattern alone does not establish this equivalence. Keep the physical pad mapping by actual number; do not substitute the XML pin position index for the pad number.

## Official model and the required canary

The installed `doc/capinfomodel/dboimnew.html#1006979` documents an exception to the usual immutable placed-pin model: `PortInst` UserProps with IDs `IDS_PROP_PIN_NAME` and `IDS_PROP_PIN_NUMBER` can override instance pin names/numbers, and EffectiveProps should be used to read the effective values. The installed `OrCAD_Capture_TclTk_Extensions.pdf`, pages 542?550, lists the associated getters and setters. These signatures establish API availability; downstream netlist behavior still needs validation.

Use a disposable copy of a design and an unmodified source library. Place two instances from the same package, mutate one pin of only the first, and compare direct getters, EffectiveProps, UserProps, the defining cache pin, the second instance and a freshly placed third instance. Save only the copy. In a new process, reopen it, repeat the reads, place a fresh fourth instance without saving, and export the actual PCB netlist. Protect the original DSN and source OLB with before/after hashes. Keep setter return codes and failed reads; a failed read is not an empty value.

## Observed 17.2 behavior

| Operation on a placed pin | Native instance/readback | PCB PST consequence |
|---|---|---|
| `SetPinName` | Creates the instance `Name` UserProp; direct and effective name survive save/reopen without changing the other instances or cache definition. | The tested PST chip pin names still come from the shared cache definition. A changed effective instance name is not proof that chip `PINNAME` changed. |
| `SetPinType` | Returned success in the controlled test, but direct/effective/XML type remained the original Passive type. No Type UserProp was created. | Treat this observed call as a no-op. Require the canonical template to have the actual electrical type instead of relying on this setter. |
| `SetPinNumber` | Creates the instance `Number` UserProp and survives save/reopen. | The tested xnet used the new number while the chip primitive retained the cache physical number. Packaging failed with SPCODD-395/SPCODD-384 and ORCAP-36026. Do not use this override to renumber production PCB pins. |

## A bounded shared-template policy

For a generic body with a fixed physical pin map, preserve the original physical reference-and-pin net partitions, Value, footprint, BOM metadata and pin electrical flags. Preserve each source function name as an explicit instance Name override when useful for display or traceability. If the canonical cache deliberately uses numeric pin names, record that as an intentional PINNAME normalization and allowlist only those exact pin-name changes in the comparison; do not call the effective parts exact-equivalent. Physical numbers and all other electrical fields still require strict equality.

For a template whose contact coordinates differ, any added lead wires are real topology changes. Plan them on the design grid, retain the original wires, avoid all foreign nets and pins, and independently compare complete physical-pin connectivity before and after native import/netlist export. Retain separate templates where pin schema or electrical flags differ. Do not encode unrelated MOS, transistor and regulator models as fake gates of one multiunit physical package.

## Raw library defaults are not proof of effective instance values

A property visible in a Package or Symbol XML scope must not be promoted to an instance merely because the raw value is unique. First query that property on the original instance with the native effective-property API and retain both the returned state and value. A controlled test found raw package audit properties whose original instance effective query failed with code 1021. Promoting those raw values created new effective properties even though all connectivity checks passed.

When replacing the cache, remove a differing canonical default that the old instance did not inherit. Preserve original explicit instance values. Materialize an inherited default only after a successful baseline native effective read; preserve a successful empty string as a defined empty string. For an original failed query, record the exact failed state and do not create an empty override. After save/reopen, compare the full query matrix, including success/failure codes, rather than comparing only text values. Unexpected failure codes or missing baseline queries require review before the transform can proceed.

## Empty iterators, explicit PinDP and visible function names

An empty native display-property iterator is not proof that a placed pin has no explicit display record. A controlled interface probe returned empty while the official saved/reopened DSN-to-XML contained placed `PortInstDisplayProp` records. A probe that requires a known result must report failure when it receives none; retain its object type, return code and empty result rather than inventing SDK anchor coordinates. Explicit location/font/rotation/display records in the official XML are a separate, hash-bound structural source, not a successful direct SDK measurement.

Give a pin's explicit placed display record precedence over the default preview offset. A preview path that ignores explicit PinDP can flag a caption/pin-number collision that does not follow the saved layout. If AUTO anchor semantics have not been GUI calibrated, test a stated range of horizontal/vertical anchor and rotation interpretations. A zero intersection result over that envelope closes the bounded model question; it does not establish Capture GUI pixels. Do not move a caption or change the electrical template merely to satisfy an uncalibrated default-offset heuristic.

Keeping an original function name as an instance pin `Name` property does not mean it remains visible on the canvas. Read the actual Name and Number display modes separately. A template may intentionally hide Name and display only the physical Number while retaining the source function as a property or tooltip. Describe those two states explicitly in delivery notes. A preserved effective Name value alone proves neither visible text nor a changed PCB `PINNAME`.

For a narrowly authorized visual adaptation, see [shared-template outer-frame handling](capture_user_library_first_templates.md#显式引脚显示与外围框的最小适配). Removing only redundant non-electrical frame strokes still requires save/reopen checks of the unchanged SymbolBBox, per-instance native affine frames, real pin hot/start and every retained display anchor; then regenerate the derived OLB and repeat placement reuse from its actual new contents. Original user libraries remain read-only.
