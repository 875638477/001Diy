;;; Examples of Cross Section in Allegro 
;;;     File is: <cdsroot>/share/pcb/examples/skill/dbcreate/xsection.il

; examples of manipulating the Allegro cross section via Skill
;	see end of file for createing entire cross sections

allDetail = t
addDetail = t

; Get all stackups
procedure( GetAll()
    let( (all stackups)

    ; get  all layers in design
    printf("@----------------------------------------------------\n")
    printf("S %s with thickness %f\n" "\"All stackups\"" axlXSectionGet(nil 'thickness))
    all = axlXSectionGet(nil 'all )
    ; get list of all stacks
    stacks = axlXSectionGet(nil 'stackups )

    ; print all
    when( allDetail axlPrintDbid(all))
    when( (length(stacks) > 1)
	foreach(item stacks
	    printf("@----------------------------------------------------\n")
	    printf("@----------------------------------------------------\n")
	    printf("S %s with thickness %f\n" item axlXSectionGet(item 'thickness))
	    printf("@----------------------------------------------------\n")
    	    all = axlXSectionGet(item 'all )
    	    when( allDetail axlPrintDbid(all))
	)
    )
))

; Get TOP layer xsection info
procedure( GetTop()
    let( (xs)

    xs = axlXSectionGet(nil 'top)
    ; print
    axlPrintDbid(xs)
))

; Get dielectric layer after top
procedure( GetAfterTop()
    let( (xs dielectric)

    xs = axlXSectionGet(nil 'top)
    dielectric = axlXSectionGet(nil xs->position +1)
    ; print
    axlPrintDbid(dielectric)
))


; Create layer pair above bottom. Good pratice to always create a dielectric
; when creating a etch layer
procedure( XSPair(@optional (name "FOO"))
    XSPairStack(nil name)
)

; Create layer pair above bottom. Assign it to a stackup
; when creating a etch layer
procedure( XSPairStack(@optional (stack nil) (name "FOO"))
       let( (xs exs  lxc dxc position )

       ; first make etch layer
       position = 'bottom

        ; modify some layer characturistics
	;  complicated -- this is disabled by default
        lxc = axlXSectionModify(
		?name name
		?layerType "CONDUCTOR"
		?mfg "foobar"
		?thickness 10.0
		?tolPlus 0.1
		?tolMinus 0.2
		?layerId "Ed"
		?material "1OZ_COPPER"
		;?negativeArtwork t
		;?unusedPin t
		?unusedVia t
		;?embedded "BODY_UP"
		;?embeddedAttach "INDIRECT_ATTACH"
		?conductivity "20000"
		;?dielectricConst "2.1"
		?width 4.4
		?lossTangent "0.123"
		?shield t
		?freqDepFile "freqFile"
		?etchFactor 88
		?diffCouplingType "EDGE"
		?diffSpacing 2
		)

       ; simple
       lxc = make_axlXSection(?name name ?layerType "CONDUCTOR" )
       xs = axlXSectionCreate( stack position lxc)
       when( addDetail axlPrintDbid(xs))
       exs = xs

       ; now make dielectric
       dxc = make_axlXSection()
       xs = axlXSectionCreate( stack position dxc)
       when( addDetail axlPrintDbid(xs))
       ; return etch and dielectic layers
       list(exs xs)
))

;
procedure( CreateMask()
       let( (lxc dxc position name)
       position = 'top
       name = "SOLDERMASK_TOP"
       lxc = make_axlXSection(?name name ?layerType "MASK"  )
       xs = axlXSectionCreate( nil position lxc)

       position = 'afterBottom
       name = "SOLDERMASK_BOTTOM"
       lxc = make_axlXSection(?name name ?layerType "MASK" ?layerFunction "SOLDER_PASTE"  )
       xs = axlXSectionCreate( nil position lxc)

       lxc->name = "FOOBAR"
       lxc->layerFunction = nil
       xs = axlXSectionCreate( nil position lxc)
))

procedure( CreateSpecialMask(@optional (layer "CARBON_TOP") (position 'top) (stackup nil))
       let( (lxc xs )
       unless(position position = 'top)
       lxc = make_axlXSection(?name layer ?layerType "MASK"  )
       xs = axlXSectionCreate( stackup position lxc)
))

; modify a layer, assume design has an layer named GND
procedure( ModLayer()
    let( (xs name ds ret)

    name = "GND"
    name = "GND1"
    xs = axlXSectionGet(nil name)

    axlPrintDbid(xs)

    ; modify some layer characturistics
    ds = axlXSectionModify(
		?layerType "CONDUCTOR"
		?mfg "foobar"
		?thickness 10.0
		?tolPlus 0.1
		?tolMinus 0.2
		?layerId "Ed"
		?material "1OZ_COPPER"
		;?negativeArtwork t
		?unusedPin t
		;?unusedVia t
		?embedded "BODY_UP"
		?embeddedAttach "INDIRECT_ATTACH"
		?conductivity "20000"
		;?dielectricConst "2.1"
		?width 4.4
		?lossTangent "0.123"
		?shield t
		?freqDepFile "freqFile"
		?etchFactor 88
		?diffCouplingType "EDGE"
		?diffSpacing 2
		)

    ret = axlXSectionSet(xs ds)
    if( ret then
	axlPrintDbid(xs)
    else
	printf("FAILED\n")
    )
    xs
))

; modify a layer, assume design has an layer named GND
procedure( RenameLayer()
    let( (xs name ds ret)

    name = "GND"
    name = "GND1"

    xs = axlXSectionGet(nil name)
    when( xs
    	printf("Old name: %s\n" xs->name)

        ds = axlXSectionModify(
		?name "rename"
		)

        ret = axlXSectionSet(xs ds)
    	printf("new name: %s\n" xs->name)
    )
    xs
))

procedure( DeleteLayer()
    let( (name xs ret)

    name = "FOO"
    XSPair()
    xs = axlXSectionGet(nil name)

    ; by name
    ; ret = axlXSectionDelete(name)
    ; by dbid
    ret = axlXSectionDelete(xs)
    printf("\n\nRESULT %s  - %L\n" name ret)
))

;---------------------------------------------------------------------------------
;---------------------------------------------------------------------------------
;---------------------------------------------------------------------------------
; create complete cross sections

; create a traditional xsection of 5 layers with soldermask assigned
procedure( SimpleCreate()
    let( (xs )

    CreateSpecialMask("SOLDERMASK_TOP")

    XSPairStack(nil "l1")
    XSPairStack(nil "GND")
    XSPairStack(nil "PWR")
    XSPairStack(nil "l2")

    CreateSpecialMask("SOLDERMASK_BOTTOM" 'afterBottom)
))

; create 2 additional stackups in a new design and populate them
;	This uses the recommended "assign" model
procedure( RigidFlexCreate()
    let( (xs p s1 s2)

    p = "rigid"
    s1 = "flex1"
    s2 = "flex2"
    axlXSectionCreateStackup(s1)
    axlXSectionCreateStackup(s2)
    axlXSectionRename(nil p)	; rename primary stackup

    xs = CreateSpecialMask("CARBON_TOP")
    axlXSectionRemove(nil xs)
    axlXSectionAssign(s1 xs)
    axlXSectionAssign(s2 xs)

    ; create the solder mask only in the primary
    CreateSpecialMask("SOLDERMASK_TOP")

    ; Create layers l1 and l2 and assign to flex1
    xs = XSPairStack(nil "l1")
    axlXSectionAssign(s1 xs)
    xs = XSPairStack(nil "l2")
    axlXSectionAssign(s1 xs)

    ; Create layers l3 and l4 and assign to flex2
    xs = XSPairStack(nil "l3")
    axlXSectionAssign(s2 xs)
    xs = XSPairStack(nil "l4")
    axlXSectionAssign(s2 xs)


    ;; reversed since it inserts it after bottom layer
    xs = CreateSpecialMask("CARBON_BOTTOM" 'afterBottom)
    ; only want masks on flex
    axlXSectionRemove(nil xs)
    axlXSectionAssign(s1 xs)
    axlXSectionAssign(s2 xs)

    ; more mask layers on bottom
    CreateSpecialMask("SOLDERMASK_BOTTOM" 'afterBottom)
))

; create 2 additional stackups in a new design and populate them
;   This uses the alternative create directly model
procedure( RigidFlexCreateAlt()
    let( (s1 s2 layers)

    s1 = "flex1"
    s2 = "flex2"
    axlXSectionCreateStackup(s1)
    axlXSectionCreateStackup(s2)

    xs = CreateSpecialMask("CARBON_TOP" nil s1)
    ; need to assign it to the other flex layer
    axlXSectionAssign(s2 xs)

    CreateSpecialMask("SOLDERMASK_TOP")

    layers = XSPairStack(s1 "l1")
    ; must assign dielectric to primary
    axlXSectionAssign(nil cadr(layers))
    layers = XSPairStack(s1 "l2")
    axlXSectionAssign(nil cadr(layers))
    layers = XSPairStack(s2 "l3")
    axlXSectionAssign(nil cadr(layers))
    layers = XSPairStack(s2 "l4")
    axlXSectionAssign(nil cadr(layers))

    ;; reversed since it inserts it after bottom layer
    xs = CreateSpecialMask("CARBON_BOTTOM" 'afterBottom s1)
    axlXSectionAssign(s2 xs)

    CreateSpecialMask("SOLDERMASK_BOTTOM" 'afterBottom)
))
