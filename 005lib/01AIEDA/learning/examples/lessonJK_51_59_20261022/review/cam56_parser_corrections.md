# Independent CAM reader correction record

Initial raw NC reader missed39 holes per variant. The first diagnosis as omitted modal axes was incorrect; inspecting actual unsupported lines found eight Excellon Rnn incremental repeat-hole commands (5+5+7+7+2+3+3+7=39). Original Gerbonara independently decoded all217/207 PTH circles. The corrected raw reader expands Rnn repeats, also supports G90 modal single-axis fields, and is compared again to native physical hole inventory. No machine output changed. This is a reader defect, not missing native drill data.

The original mirror assertion assumed all Films unmirrored. Original PDFBOTTOM is intentionally mirrored in the native template for an assembly view. The check now compares each actual Film option, preserving unmirrored physical copper and the original PDFBOTTOM option. Initial reports are retained in backups/cam56_initial_parser_review.

Gerbonara1.6.3 separately rejects global NC tool IDs T05/T06 with local Holesize ordinal1/2 in NPTH comments. Original NC output stays untouched; a derived parser-input copy removes only those metadata comment lines. Raw explicit tool/coordinate commands and independent parser results must agree.

Initial contact-sheet composition nested SVG viewports and reused per-layer SVG IDs; the rasterizer placed/combined them at the first panel. Individual layer SVG/PNG outputs were correct. Contact sheets now embed independently rendered PNG tiles at explicit image coordinates; all final panels require fresh visual inspection. Native CAM files remain unchanged.
