; Read-only learning probe. No edits, no save, no selection changes.
let((edaDesign)
  edaDesign = axlDBGetDesign()
  if(edaDesign then
    printf("EDA_READONLY design=%L\n" axlCurrentDesign())
    printf("EDA_READONLY components=%d nets=%d\n"
      length(edaDesign->components) length(edaDesign->nets))
  else
    printf("EDA_READONLY no design loaded\n")
  )
)
