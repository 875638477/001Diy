# L60 portable native replay

This is a self-contained training copy, not a released PCB. It performs one operation: create L60_REPLAY at (4,4) mm on BOARD GEOMETRY/ASSEMBLY_NOTES, save a new board, and reopen it in a second native process to verify the exact result.

Requirements: Windows, Python 3.10 or later (this run tested 3.14), an independently installed and licensed Cadence17.2 Allegro PCB Designer. The board contains its existing embedded padstacks/symbols; this operation does not refresh the public library or load the user env.

1. Copy the package directory to the destination. Do not copy generated runs for a clean replay.
2. Copy config.example.json to config.local.json; set cadence_root to the destination installation and keep a legitimately available product. No license file or credentials belong in the package.
3. Run the following commands with your Python executable from any working directory. Use an absolute path to replay.py; quote paths containing spaces.

```powershell
python -I "PATH TO PACKAGE/replay.py" probe
python -I "PATH TO PACKAGE/replay.py" plan --tag migration01
python -I "PATH TO PACKAGE/replay.py" run --tag migration01
python -I "PATH TO PACKAGE/replay.py" verify --tag migration01
```

probe checks only static files, checksums and process identity; it does not prove a license is available. run actually opens the training copy twice through Cadence. plan launches nothing. Existing run tags refuse overwrite. A failure preserves its inputs, generated script, stdout, stderr, journal and process identity. Choose a new tag after correcting a failure.

Expected successful verification: 42 checks PASS, 80 components, 272 logical pins, 69 nets, physical route layers TOP-L2-L3-BOTTOM, millimeter units, 932 actual path segments (750 manual, 182 generated thermal) in every phase, zero source markers, exactly one saved/fresh marker, and identical nonempty native geometry fingerprints before creation, in memory and after fresh reopen. Source fixture SHA must stay 471176A9B25BA8DEF9F117AEFB1E9220CBCBEBBAC5191BCBC6E228F52831F3F9.

Each run has private pcbenv/TEMP and sources only the installed TELENV defaults; no user hotkeys, 01env, autosave or global HOME changes. Unrelated GUI processes are recorded and excluded from automation. Only a launched direct child with the same PID, creation time, executable, parent and exact task command paths may be terminated after timeout. No blanket kill or UI input is used.

The manifest protects portable source files and the board fixture. config.local.json is intentionally machine-specific and excluded. After an intentional source change, create a new reviewed manifest/version; do not just accept a mismatch.

A second directory with spaces on this computer is a relocation experiment. It is not evidence of successful execution on a second physical computer. The texts and scripts are portable records; legal software installation, licensing, native process access and GUI interaction must be established again on a new machine. Routing, DRC, SI/PI/EMI and fabrication signoff are outside this tiny operation.

Native script and package paths are explicitly limited to ASCII characters, including spaces. A non-ASCII/Chinese package or Cadence path is rejected before native launch; it has not been tested. Python -I is mandatory so user site and PYTHONPATH cannot silently change the launcher imports. The Cadence child additionally removes PYTHONPATH/PYTHONHOME and sets PYTHONNOUSERSITE=1. These are Python-specific variables; the user HOME is never changed. Other operating-system and legitimate license environment is inherited, not claimed isolated, and its values are not logged.

The launcher also conservatively refuses native command lines longer than 500 characters before any run/native launch. In this environment a 526-character fresh-reopen command failed twice at startup with Windows exit 0xC0000005, while a prior 508-character command succeeded. This correlation does not prove a universal 512-character Cadence limit or that spaces are the cause. Keep the destination root and run tag short; plan validates both build and fresh argv lengths. All failed long-path evidence remains in the lesson native history/output directories.
