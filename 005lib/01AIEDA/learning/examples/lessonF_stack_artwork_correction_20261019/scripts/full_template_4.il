procedure(fcorTemplate4(f)
 let((r)
r=axlFilmCreate( "TOP" ?negative nil ?undefineLineWidth 0.0025 ?sequence 1 
	?rotation 0 ?xOffset 0.0000 ?yOffset 0.0000 ?shapeBoundingBox 2.5400 ?mirrored nil ?fullContact nil 
	?suppressUnconnectPads nil ?drawMissingPadApertures nil ?useApertureRotation nil 
	?suppressShapeFill nil ?vectorBasedPad t ?drawHolesOnly nil 
	?domains '(ipc2581 pdf artwork visibility ) ?ipc2581 '() 
	?layers '("ETCH/TOP" "PIN/TOP" "VIA CLASS/TOP" "BOARD GEOMETRY/OUTLINE"  ))
fprintf(f "FILM_RESULT\t%L\t%L\n" "TOP" r)
r=axlFilmCreate( "L2" ?negative nil ?undefineLineWidth 0.0025 ?sequence 25 
	?rotation 0 ?xOffset 0.0000 ?yOffset 0.0000 ?shapeBoundingBox 2.5400 ?mirrored nil ?fullContact nil 
	?suppressUnconnectPads nil ?drawMissingPadApertures nil ?useApertureRotation nil 
	?suppressShapeFill nil ?vectorBasedPad t ?drawHolesOnly nil 
	?domains '(ipc2581 pdf artwork visibility ) ?ipc2581 '() 
	?layers '("ETCH/L2" "PIN/L2" "VIA CLASS/L2" "BOARD GEOMETRY/OUTLINE" ))
fprintf(f "FILM_RESULT\t%L\t%L\n" "L2" r)
r=axlFilmCreate( "L3" ?negative nil ?undefineLineWidth 0.0025 ?sequence 20 
	?rotation 0 ?xOffset 0.0000 ?yOffset 0.0000 ?shapeBoundingBox 2.5400 ?mirrored nil ?fullContact nil 
	?suppressUnconnectPads nil ?drawMissingPadApertures nil ?useApertureRotation nil 
	?suppressShapeFill nil ?vectorBasedPad t ?drawHolesOnly nil 
	?domains '(ipc2581 pdf artwork visibility ) ?ipc2581 '() 
	?layers '("ETCH/L3" "PIN/L3" "VIA CLASS/L3" "BOARD GEOMETRY/OUTLINE" ))
fprintf(f "FILM_RESULT\t%L\t%L\n" "L3" r)
r=axlFilmCreate( "BOTTOM" ?negative nil ?undefineLineWidth 0.0025 ?sequence 27 
	?rotation 0 ?xOffset 0.0000 ?yOffset 0.0000 ?shapeBoundingBox 2.5400 ?mirrored nil ?fullContact nil 
	?suppressUnconnectPads nil ?drawMissingPadApertures nil ?useApertureRotation nil 
	?suppressShapeFill nil ?vectorBasedPad t ?drawHolesOnly nil 
	?domains '(ipc2581 pdf artwork visibility ) ?ipc2581 '() 
	?layers '("ETCH/BOTTOM" "PIN/BOTTOM" "VIA CLASS/BOTTOM" "BOARD GEOMETRY/OUTLINE" ))
fprintf(f "FILM_RESULT\t%L\t%L\n" "BOTTOM" r)
r=axlFilmCreate( "PASTTOP" ?negative nil ?undefineLineWidth 0.0025 ?sequence 23 
	?rotation 0 ?xOffset 0.0000 ?yOffset 0.0000 ?shapeBoundingBox 2.5400 ?mirrored nil ?fullContact nil 
	?suppressUnconnectPads nil ?drawMissingPadApertures nil ?useApertureRotation nil 
	?suppressShapeFill nil ?vectorBasedPad t ?drawHolesOnly nil 
	?domains '(ipc2581 pdf artwork visibility ) ?ipc2581 '() 
	?layers '("PIN/PASTEMASK_TOP" "PACKAGE GEOMETRY/PASTEMASK_TOP"  ))
fprintf(f "FILM_RESULT\t%L\t%L\n" "PASTTOP" r)
r=axlFilmCreate( "PASTBOTTOM" ?negative nil ?undefineLineWidth 0.0025 ?sequence 24 
	?rotation 0 ?xOffset 0.0000 ?yOffset 0.0000 ?shapeBoundingBox 2.5400 ?mirrored nil ?fullContact nil 
	?suppressUnconnectPads nil ?drawMissingPadApertures nil ?useApertureRotation nil 
	?suppressShapeFill nil ?vectorBasedPad t ?drawHolesOnly nil 
	?domains '(ipc2581 pdf artwork visibility ) ?ipc2581 '() 
	?layers '("PIN/PASTEMASK_BOTTOM" "PACKAGE GEOMETRY/PASTEMASK_BOTTOM"  ))
fprintf(f "FILM_RESULT\t%L\t%L\n" "PASTBOTTOM" r)
r=axlFilmCreate( "SKILTOP" ?negative nil ?undefineLineWidth 0.0025 ?sequence 1 
	?rotation 0 ?xOffset 0.0000 ?yOffset 0.0000 ?shapeBoundingBox 2.5400 ?mirrored nil ?fullContact nil 
	?suppressUnconnectPads nil ?drawMissingPadApertures nil ?useApertureRotation nil 
	?suppressShapeFill nil ?vectorBasedPad t ?drawHolesOnly nil 
	?domains '(ipc2581 pdf artwork visibility ) ?ipc2581 '() 
	?layers '( "PACKAGE GEOMETRY/SILKSCREEN_TOP" "BOARD GEMETRY/SILKSCREEN_TOP" ))
fprintf(f "FILM_RESULT\t%L\t%L\n" "SKILTOP" r)
r=axlFilmCreate( "SKILBOTTOM" ?negative nil ?undefineLineWidth 0.0025 ?sequence 2 
	?rotation 0 ?xOffset 0.0000 ?yOffset 0.0000 ?shapeBoundingBox 2.5400 ?mirrored nil ?fullContact t 
	?suppressUnconnectPads nil ?drawMissingPadApertures nil ?useApertureRotation nil 
	?suppressShapeFill nil ?vectorBasedPad t ?drawHolesOnly nil 
	?domains '(ipc2581 pdf artwork visibility ) ?ipc2581 '() 
	?layers '("PACKAGE GEOMETRY/SILKSCREEN_BOTTOM" "BOARD GEMETRY/SILKSCREEN_BOTTOM" ))
fprintf(f "FILM_RESULT\t%L\t%L\n" "SKILBOTTOM" r)
r=axlFilmCreate( "SOLDTOP" ?negative nil ?undefineLineWidth 0.0025 ?sequence 2 
	?rotation 0 ?xOffset 0.0000 ?yOffset 0.0000 ?shapeBoundingBox 2.5400 ?mirrored nil ?fullContact t 
	?suppressUnconnectPads nil ?drawMissingPadApertures nil ?useApertureRotation nil 
	?suppressShapeFill nil ?vectorBasedPad t ?drawHolesOnly nil 
	?domains '(ipc2581 pdf artwork visibility ) ?ipc2581 '() 
	?layers '("VIA CLASS/SOLDERMASK_TOP" "PIN/SOLDERMASK_TOP" "PACKAGE GEOMETRY/SOLDERMASK_TOP" "BOARD GEOMETRY/SOLDERMASK_TOP"))
fprintf(f "FILM_RESULT\t%L\t%L\n" "SOLDTOP" r)
r=axlFilmCreate( "SOLDBOTTOM" ?negative nil ?undefineLineWidth 0.0025 ?sequence 2 
	?rotation 0 ?xOffset 0.0000 ?yOffset 0.0000 ?shapeBoundingBox 2.5400 ?mirrored nil ?fullContact t 
	?suppressUnconnectPads nil ?drawMissingPadApertures nil ?useApertureRotation nil 
	?suppressShapeFill nil ?vectorBasedPad t ?drawHolesOnly nil 
	?domains '(ipc2581 pdf artwork visibility ) ?ipc2581 '() 
	?layers '("VIA CLASS/SOLDERMASK_BOTTOM" "PIN/SOLDERMASK_BOTTOM" "PACKAGE GEOMETRY/SOLDERMASK_BOTTOM" "BOARD GEOMETRY/SOLDERMASK_BOTTOM"))
fprintf(f "FILM_RESULT\t%L\t%L\n" "SOLDBOTTOM" r)
r=axlFilmCreate( "DRILL" ?negative nil ?undefineLineWidth 0.0025 ?sequence 26 
	?rotation 0 ?xOffset 0.0000 ?yOffset 0.0000 ?shapeBoundingBox 2.5400 ?mirrored nil ?fullContact nil 
	?suppressUnconnectPads nil ?drawMissingPadApertures nil ?useApertureRotation nil 
	?suppressShapeFill nil ?vectorBasedPad t ?drawHolesOnly nil 
	?domains '(ipc2581 pdf artwork visibility ) ?ipc2581 '() 
	?layers '( "BOARD GEOMETRY/ASSEMBLY_NOTES" "MANUFACTURING/NCDRILL_LEGEND" "MANUFACTURING/NCDRILL_FIGURE" "MANUFACTURING/NCLEGEND-1-4" "BOARD GEOMETRY/DIMENSION"))
fprintf(f "FILM_RESULT\t%L\t%L\n" "DRILL" r)
r=axlFilmCreate( "OUTlie" ?negative nil ?undefineLineWidth 0.0025 ?sequence 1 
	?rotation 0 ?xOffset 0.0000 ?yOffset 0.0000 ?shapeBoundingBox 2.5400 ?mirrored nil ?fullContact nil 
	?suppressUnconnectPads nil ?drawMissingPadApertures nil ?useApertureRotation nil 
	?suppressShapeFill nil ?vectorBasedPad t ?drawHolesOnly nil 
	?domains '(ipc2581 pdf artwork visibility ) ?ipc2581 '() 
	?layers '( "BOARD GEOMETRY/OUTLINE" "BOARD GEOMETRY/FILM_FORMAT" ))
fprintf(f "FILM_RESULT\t%L\t%L\n" "OUTlie" r)
r=axlFilmCreate( "PDFTOP" ?negative nil ?undefineLineWidth 0.0025 ?sequence 1 
	?rotation 0 ?xOffset 0.0000 ?yOffset 0.0000 ?shapeBoundingBox 2.5400 ?mirrored nil ?fullContact nil 
	?suppressUnconnectPads nil ?drawMissingPadApertures nil ?useApertureRotation nil 
	?suppressShapeFill nil ?vectorBasedPad t ?drawHolesOnly nil 
	?domains '(ipc2581 pdf artwork visibility ) ?ipc2581 '() 
	?layers '("REF DES/ASSEMBLY_TOP" "PACKAGE GEOMETRY/SILKSCREEN_TOP" "BOARD GEMETRY/SILKSCREEN_TOP" "BOARD GEOMETRY/OUTLINE" ))
fprintf(f "FILM_RESULT\t%L\t%L\n" "PDFTOP" r)
r=axlFilmCreate( "PDFBOTTOM" ?negative nil ?undefineLineWidth 0.0025 ?sequence 2 
	?rotation 0 ?xOffset 0.0000 ?yOffset 0.0000 ?shapeBoundingBox 2.5400 ?mirrored t ?fullContact t 
	?suppressUnconnectPads nil ?drawMissingPadApertures nil ?useApertureRotation nil 
	?suppressShapeFill nil ?vectorBasedPad t ?drawHolesOnly nil 
	?domains '(ipc2581 pdf artwork visibility ) ?ipc2581 '() 
	?layers '("REF DES/ASSEMBLY_BOTTOM" "PACKAGE GEOMETRY/SILKSCREEN_BOTTOM" "BOARD GEMETRY/SILKSCREEN_BOTTOM" "BOARD GEOMETRY/OUTLINE" ))
fprintf(f "FILM_RESULT\t%L\t%L\n" "PDFBOTTOM" r)
r=axlFilmCreate( "DisTOP" ?negative nil ?undefineLineWidth 0.0025 ?sequence 1 
	?rotation 0 ?xOffset 0.0000 ?yOffset 0.0000 ?shapeBoundingBox 2.5400 ?mirrored nil ?fullContact nil 
	?suppressUnconnectPads nil ?drawMissingPadApertures nil ?useApertureRotation nil 
	?suppressShapeFill nil ?vectorBasedPad t ?drawHolesOnly nil 
	?domains '(ipc2581 pdf artwork visibility ) ?ipc2581 '() 
	?layers '("ROUTE KEEPOUT/ALL" "ROUTE KEEPOUT/TOP" "DRAWING FORMAT/DRAWING_ORIGIN" "MANUFACTURING/PHOTOPLOT_OUTLINE" "PACKAGE KEEPIN/ALL" "ROUTE KEEPIN/ALL" "BOARD GEOMETRY/OUTLINE" "BOARD GEOMETRY/DXFTOP" "PACKAGE GEOMETRY/SILKSCREEN_TOP" "BOARD GEOMETRY/DXF_TOP" "PIN/TOP" "MANUFACTURING/PHOTOPLOT_OUTLINE"  ))
fprintf(f "FILM_RESULT\t%L\t%L\n" "DisTOP" r)
r=axlFilmCreate( "DisBOTTOM" ?negative nil ?undefineLineWidth 0.0025 ?sequence 1 
	?rotation 0 ?xOffset 0.0000 ?yOffset 0.0000 ?shapeBoundingBox 2.5400 ?mirrored nil ?fullContact nil 
	?suppressUnconnectPads nil ?drawMissingPadApertures nil ?useApertureRotation nil 
	?suppressShapeFill nil ?vectorBasedPad t ?drawHolesOnly nil 
	?domains '(ipc2581 pdf artwork visibility ) ?ipc2581 '() 
	?layers '("ROUTE KEEPOUT/ALL" "ROUTE KEEPOUT/BOTTOM" "DRAWING FORMAT/DRAWING_ORIGIN" "MANUFACTURING/PHOTOPLOT_OUTLINE" "PACKAGE KEEPIN/ALL" "ROUTE KEEPIN/ALL" "BOARD GEOMETRY/OUTLINE" "BOARD GEOMETRY/DXFBOTTOM" "PACKAGE GEOMETRY/SILKSCREEN_BOTTOM" "BOARD GEOMETRY/DXF_BOTTOM" "PIN/BOTTOM" "MANUFACTURING/PHOTOPLOT_OUTLINE" ))
fprintf(f "FILM_RESULT\t%L\t%L\n" "DisBOTTOM" r)
r=axlFilmCreate( "DisAll" ?negative nil ?undefineLineWidth 0.0025 ?sequence 1 
	?rotation 0 ?xOffset 0.0000 ?yOffset 0.0000 ?shapeBoundingBox 2.5400 ?mirrored nil ?fullContact nil 
	?suppressUnconnectPads nil ?drawMissingPadApertures nil ?useApertureRotation nil 
	?suppressShapeFill nil ?vectorBasedPad t ?drawHolesOnly nil 
	?domains '(ipc2581 pdf artwork visibility ) ?ipc2581 '() 
	?layers '( "CONSTRAINT REGION/TOP" "CONSTRAINT REGION/L2" "CONSTRAINT REGION/L3" "CONSTRAINT REGION/BOTTOM" "CONSTRAINT REGION/ALL" "BOARD GEOMETRY/FILM_FORMAT" "ROUTE KEEPOUT/TOP" "ROUTE KEEPOUT/BOTTOM" "ROUTE KEEPOUT/ALL" "ETCH/TOP" "ETCH/BOTTOM" "DRAWING FORMAT/DRAWING_ORIGIN"  "BOARD GEOMETRY/ASSEMBLY_NOTES" "BOARD GEOMETRY/DXF" "BOARD GEOMETRY/DXFTOP" "BOARD GEOMETRY/DXFBOTTOM" "BOARD GEOMETRY/SILKSCREEN_TOP" "BOARD GEOMETRY/SILKSCREEN_BOTTOM" "BOARD GEOMETRY/FILM_FORMAT" "BOARD GEOMETRY/DIMENSION" "PACKAGE GEOMETRY/SILKSCREEN_TOP" "PACKAGE GEOMETRY/SILKSCREEN_BOTTOM" "BOARD GEOMETRY/OUTLINE" "BOARD GEOMETRY/DXF" "VIA CLASS/TOP" "VIA CLASS/BOTTOM" "PIN/TOP" "PACKAGE KEEPIN/ALL" "ROUTE KEEPIN/ALL" "ROUTE KEEPOUT/ALL" "PIN/BOTTOM" "BOARD GEOMETRY/DXF" "DRAWING FORMAT/DRAWING_ORIGIN" "MANUFACTURING/PHOTOPLOT_OUTLINE" "MANUFACTURING/NCLEGEND-1-4" ))
fprintf(f "FILM_RESULT\t%L\t%L\n" "DisAll" r)

 t))
