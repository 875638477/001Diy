# Not an accepted netlist or board

The first integrated DSN v1 preflight (owned pstswp PID 30768, 2026-10-19 10:53:54–10:53:55 Asia/Shanghai) returned **exitCode 1**. `netlist/netlist.log` records native packaging SPCODD-228/53/391 pin/physical-section mismatches. The generated PST files are partial diagnostic outputs.

The subsequent netrev run returned exitCode 0 and saved `DE_BASELINE.brd`, despite the upstream packaging failure. That proves that successful parsing by a downstream utility does not validate a failed upstream export. This board is excluded from all acceptance results and delivery. The final flow runner checks each stage result before invoking the next stage. No custom Python netlist generation or patching of native PST outputs is used to bypass these errors.
