; =====================================================================
; ai_bridge.il -- AI <-> Allegro PCB Editor command bridge  (v2, IPC)
;
; Location: D:/001DIY/005lib/01AIcadence/ai_bridge/ai_bridge.il
;
; How it works (event driven, no polling timer needed):
;   - AI writes SKILL code into  exchange/command.il
;   - AI creates the trigger file exchange/command.flag
;   - An external watcher process (flag_watch.bat, started via
;     ipcBeginProcess) prints "RUN" whenever command.flag exists.
;   - The ipc data handler fires asynchronously inside Allegro,
;     executes command.il, captures output into exchange/result.txt,
;     then creates exchange/result.flag.
;
; Allegro commands registered by this file:
;   ai_start   : start the watcher (auto-started on load)
;   ai_stop    : stop the watcher
;   ai_run     : execute the pending command once (manual fallback)
;   ai_status  : show bridge status
;
; NOTE: keep this file pure ASCII to avoid codepage issues.
; =====================================================================

AIB_exchDir  = "D:/001DIY/005lib/01AIcadence/ai_bridge/exchange"
AIB_cmdFile  = strcat(AIB_exchDir "/command.il")
AIB_cmdFlag  = strcat(AIB_exchDir "/command.flag")
AIB_resFile  = strcat(AIB_exchDir "/result.txt")
AIB_resFlag  = strcat(AIB_exchDir "/result.flag")
AIB_watchCmd = "cmd /c D:\\001DIY\\005lib\\01AIcadence\\ai_bridge\\flag_watch.bat"
AIB_runCount = 0
AIB_running  = nil

when( !boundp('AIB_ipc) AIB_ipc = nil )

procedure( AIB_writeFlag(path text)
    let( (p)
        p = outfile(path)
        when( p
            fprintf(p "%s\n" text)
            close(p)
        )
    )
)

; Execute pending command.il once (if command.flag exists)
procedure( AIB_run()
    let( (p oldPort res)
        if( !isFile(AIB_cmdFlag) then
            nil
        else
            deleteFile(AIB_cmdFlag)
            when( isFile(AIB_resFlag) deleteFile(AIB_resFlag) )
            AIB_runCount = AIB_runCount + 1
            p = outfile(AIB_resFile)
            if( !p then
                printf("AI_BRIDGE: cannot open result file %s\n" AIB_resFile)
            else
                fprintf(p "[AI_BRIDGE] run #%d at %s\n" AIB_runCount getCurrentTime())
                fprintf(p "----------------------------------------\n")
                oldPort = poport
                poport = p
                res = errset(load(AIB_cmdFile) t)
                poport = oldPort
                fprintf(p "----------------------------------------\n")
                if( res then
                    fprintf(p "[AI_BRIDGE] STATUS: OK\n")
                else
                    fprintf(p "[AI_BRIDGE] STATUS: ERROR\n")
                    fprintf(p "[AI_BRIDGE] ERRSET: %L\n" errset.errset)
                )
                close(p)
                AIB_writeFlag(AIB_resFlag "done")
                printf("AI_BRIDGE: command #%d executed, result written.\n" AIB_runCount)
            )
            t
        )
    )
)

; Async data handler: watcher prints RUN when command.flag exists
procedure( AIB_ipcData(cid data)
    when( AIB_running && nindex(data "RUN")
        errset(AIB_run() t)
    )
    t
)

procedure( AIB_ipcAlive()
    AIB_ipc && car(errset(ipcIsAliveProcess(AIB_ipc) t))
)

procedure( AIB_start()
    if( AIB_ipcAlive() then
        printf("AI_BRIDGE: watcher already running.\n")
    else
        let( (r)
            AIB_running = t
            r = errset(ipcBeginProcess(AIB_watchCmd "" "AIB_ipcData") t)
            if( r && car(r) then
                AIB_ipc = car(r)
                printf("AI_BRIDGE: ipc watcher started (event driven).\n")
                printf("AI_BRIDGE: exchange dir = %s\n" AIB_exchDir)
            else
                AIB_ipc = nil
                AIB_running = nil
                printf("AI_BRIDGE: ipc watcher FAILED to start, use manual ai_run.\n")
            )
        )
    )
)

procedure( AIB_stop()
    AIB_running = nil
    when( AIB_ipc
        errset(ipcKillProcess(AIB_ipc) t)
        AIB_ipc = nil
    )
    printf("AI_BRIDGE: watcher stopped.\n")
)

procedure( AIB_status()
    printf("AI_BRIDGE: running=%L watcherAlive=%L runs=%d pendingCmd=%L\n"
        AIB_running AIB_ipcAlive() AIB_runCount isFile(AIB_cmdFlag))
    printf("AI_BRIDGE: exchange dir = %s\n" AIB_exchDir)
)

axlCmdRegister("ai_run"    'AIB_run    ?cmdType "general")
axlCmdRegister("ai_start"  'AIB_start  ?cmdType "general")
axlCmdRegister("ai_stop"   'AIB_stop   ?cmdType "general")
axlCmdRegister("ai_status" 'AIB_status ?cmdType "general")

printf("AI_BRIDGE v2: loaded. Commands: ai_start / ai_stop / ai_run / ai_status\n")
AIB_start()
