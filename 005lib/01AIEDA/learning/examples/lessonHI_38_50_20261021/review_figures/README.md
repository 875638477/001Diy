# Native copper diagrams, source b015

The two SVG files are generated from the actual fresh readonly checkpoints. They are engineering diagrams, not Allegro screenshots or CAM manufacturing artwork. Both boards are DRC_PENDING.

Plane arcs and holes use the audited Cadence converter; all nine native filled polygons retained their holes and differed from native area by at most 0.00312975 mm². See ../engineering_power/readouts/arc_source_b015_area_audit.json. Pad shapes are native bounding-box approximations; body rectangles are PlaceBound extents. Via radii use their actual selected-layer pads (.26 or .30 mm), not a universal .30 mm symbol.

Total exported route segments include generated thermals: 2L 714 = 651 manual + 63 thermal; 4L 771 = 643 manual + 128 thermal. Colors identify nets/layers; a drawing does not establish clearance, connectivity, reference continuity or assembly acceptance.

The optional System.Drawing raster script was prepared but execution of the .ps1 file was blocked by the machine PowerShell execution policy. No policy was changed, no PNG was produced, and this is not a visual QA pass. The in-app browser was unavailable when trying to preview the local SVG. The SVG files remain available for manual viewing; their XML geometry is derived from the actual checkpoint, not a fabricated PCB image.
