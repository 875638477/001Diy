procedure(hiReadbackProofs()
 let((f)
  f=outfile("D:/001DIY/005lib/01AIEDA/learning/examples/lessonHI_38_50_20261021/logs/reopen_island_stitch_2L_b011/hi_reopen_endpoint_proofs.txt")
  hiRegistry=nil
  unwindProtect(progn(
   axlDBControl('drcEnable nil)
  hiNodeDefinitions=list(list("V_HI_GPIO_ISLAND_STITCH" "GND" "TOP" list(37.4 27.4) "via"))
  hiBindExistingVia(f "V_HI_GPIO_ISLAND_STITCH" "GND" list(37.4 27.4) "L28_VIA030_C060")
  hiGroundPointCheck(f "ISLAND_AFTER" list(37.4 27.4) t t)
  hiProof(f "V_HI_GPIO_ISLAND_STITCH" "U1.23" t)
  hiHSEIsolationChallengeGraph("D:/001DIY/005lib/01AIEDA/learning/examples/lessonHI_38_50_20261021/logs/reopen_island_stitch_2L_b011" list(45.45 28.85) "BOTTOM" list(list(42.2 39.8) list(44.2 39.8) list(47.8 33.5)))
  t) progn(axlDBControl('drcEnable t) fprintf(f "HI_READBACK_UNWIND_DRC_RESTORED=%L\n" axlDBControl('drcEnable))))
  fprintf(f "HI_REOPEN_ALL_ENDPOINTS_COMPLETE\n") close(f) t))
