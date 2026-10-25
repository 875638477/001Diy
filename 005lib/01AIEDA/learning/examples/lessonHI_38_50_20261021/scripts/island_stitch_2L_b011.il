procedure(hiBatchProgram()
 let((f)
  f=outfile("D:/001DIY/005lib/01AIEDA/learning/examples/lessonHI_38_50_20261021/logs/island_stitch_2L_b011/hi_batch_execution.txt")
  fprintf(f "HI_BATCH_DRC_BEFORE=%L\n" axlDBControl('drcEnable))
  unwindProtect(
   progn(
    axlDBControl('drcEnable nil)
    fprintf(f "HI_ASSEMBLY_ONLINE_DRC_TEMPORARILY_DISABLED=%L\n" axlDBControl('drcEnable))
    hiRegistry=nil
    hiNodeDefinitions=list(list("V_HI_GPIO_ISLAND_STITCH" "GND" "TOP" list(37.4 27.4) "via"))
    hiGroundPointCheck(f "ISLAND_BEFORE" list(37.4 27.4) nil t)
    hiVia(f "V_HI_GPIO_ISLAND_STITCH" "GND" list(37.4 27.4) "L28_VIA030_C060")
    hiGroundPointCheck(f "ISLAND_AFTER" list(37.4 27.4) t t)
    hiHSEIsolationChallengeGraph("D:/001DIY/005lib/01AIEDA/learning/examples/lessonHI_38_50_20261021/logs/island_stitch_2L_b011" list(45.45 28.85) "BOTTOM" list(list(42.2 39.8) list(44.2 39.8) list(47.8 33.5)))
    t)
   progn(
    axlDBControl('drcEnable t)
    fprintf(f "HI_UNWIND_DRC_RESTORED=%L\n" axlDBControl('drcEnable))))
  unless(axlDBControl('drcEnable) error("Final DRC must be enabled\n"))
  hiFinalize(f "D:/001DIY/005lib/01AIEDA/learning/examples/lessonHI_38_50_20261021/logs/island_stitch_2L_b011" "D:/001DIY/005lib/01AIEDA/learning/examples/lessonHI_38_50_20261021/native/HI_2L_island_stitch_2L_b011.brd" "D:/001DIY/005lib/01AIEDA/learning/examples/lessonHI_38_50_20261021/library" list(list("V_HI_GPIO_ISLAND_STITCH" "U1.23" t)))
  t))
