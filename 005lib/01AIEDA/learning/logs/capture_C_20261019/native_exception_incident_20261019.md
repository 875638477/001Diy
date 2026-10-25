# Native SDK exception and desktop interruption

2026-10-19, Asia/Shanghai. The user supplied a screenshot showing a tclsh.exe native access violation and the Windows just-in-time debugger chooser (PID 31400). This was associated with the ongoing Capture database SDK experiments; Visual Studio was not intentionally launched. The precise PID was not recorded by the failed child launch, so attribution to the C13 FlatNet.NewWiresIter crash is probable, not proven.

C13 had two unsafe native paths during exploratory work: casting NULL to a DboDesign, and invoking FlatNet.NewWiresIter. C14 also reported a native cache failure followed by a NULL access in an earlier exploratory batch. The screenshot cannot be strictly assigned to one of these failed batches from recorded PIDs. These paths are stopped. The successful read path uses NetOccurrences, validates non-NULL objects, and accesses schematic-net wires only through an actual occurrence. Separate batch processes isolate lessons.

After the screenshot, Get-Process found no tclsh, vsjitdebugger, or WerFault process. No PID31400 remained to terminate. The owned unready Capture lite startup probe (PID24164, start10:03:48) was stopped after matching its recorded process name and start time. No debugger was started, no system exception or registry setting was changed, and no unrelated application was terminated.

No success claim may be derived from a native process that crashes or from an API that returns success without changing the saved database. The error and attempted alternatives remain in lesson records.
