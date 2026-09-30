; Allegro sub-drawing file
; Created by Allegro PCB Designer; version= 17.2-2016 S045

_clp_lay_drw = axlDesignType(nil)
_clp_sym = nil
_clp_pbuf  = nil
_clp_cinfo = make_clp_coord_info()
_clp_cinfo->f_rotation = 0.0
_clp_cinfo->l_origin = '(0.0 0.0)
_clp_text_orient = make_axlTextOrientation()
_clp_pin_text = make_axlPinText()
_clp_cinfo->t_from_units = "millimeters"
_clp_cinfo->t_to_units = car(axlDBGetDesignUnits())
_clp_cinfo->preserve_shape_net = nil
_clp_cinfo->preserve_via_net = nil
_clp_cinfo->snapToObject = nil
_clp_cinfo->createNCLayers = nil
_clp_group_info = make_clp_group_info()
_clp_cinfo->group_info = _clp_group_info
_clp_accuracy =4
_clpCheckAccuracy(_clp_accuracy _clp_cinfo->t_from_units	 	_clp_cinfo->t_to_units)
(putprop _clp_cinfo (list (_clpAdjustPt -5.92:-1.95 _clp_cinfo)	
	(_clpAdjustPt 6.07:4.47 _clp_cinfo)) 'l_extents)
(putprop _clp_cinfo (_clpAdjustPt '(64.65 -51.6) _clp_cinfo) 'l_zeropt)
(unless (_clpSelectRotOrg _clp_cinfo)
	(error "CANCEL"))
_clp_clip_prop_value = _clpGetClipPropValue()

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(0.2949999999999875:0.6338000000000008 _clp_cinfo) _clpAdjustPt(0.664999999999992:0.6338000000000008 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(0.2641999999999882:0.75 _clp_cinfo) _clpAdjustPt(0.2800000000000011:0.75 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-0.05000000000001137:-1.640000000000001 _clp_cinfo) _clpAdjustPt(-0.05000000000001137:-1.949999999999996 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(0.2641999999999882:0.5500000000000043 _clp_cinfo) _clpAdjustPt(0.2457999999999885:0.5500000000000043 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(0.3549999999999898:0.7899999999999992 _clp_cinfo) _clpAdjustPt(0.3549999999999898:1.009999999999998 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(0.2949999999999875:0.6148999999999987 _clp_cinfo) _clpAdjustPt(0.2949999999999875:0.6338000000000008 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-0.1200000000000046:0.75 _clp_cinfo) _clpAdjustPt(-0.1200000000000046:0.8000000000000043 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-0.1700000000000017:1 _clp_cinfo) _clpAdjustPt(-0.1700000000000017:0.8488000000000042 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(0.2599999999999909:1 _clp_cinfo) _clpAdjustPt(0.3299999999999983:1 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-0.1950000000000074:0.7899999999999992 _clp_cinfo) _clpAdjustPt(-0.1350000000000051:0.7899999999999992 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(0.2457999999999885:0.5500000000000043 _clp_cinfo) _clpAdjustPt(0.2304999999999922:0.5500000000000043 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(0.2299999999999898:0.8070000000000022 _clp_cinfo) _clpAdjustPt(0.2299999999999898:0.5502000000000038 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-0.1000000000000085:0.8488000000000042 _clp_cinfo) _clpAdjustPt(0.2599999999999909:0.8488000000000042 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-0.08580000000000609:0.75 _clp_cinfo) _clpAdjustPt(-0.07050000000000978:0.75 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(0.3299999999999983:0.8488000000000042 _clp_cinfo) _clpAdjustPt(0.2599999999999909:0.8488000000000042 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-0.07000000000000739:0.8070000000000022 _clp_cinfo) _clpAdjustPt(-0.07000000000000739:0.8488000000000042 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(0.2800000000000011:0.8000000000000043 _clp_cinfo) _clpAdjustPt(0.2800000000000011:0.75 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(0.2099999999999938:-1.949999999999996 _clp_cinfo) _clpAdjustPt(-0.05000000000001137:-1.949999999999996 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-0.1200000000000046:0.75 _clp_cinfo) _clpAdjustPt(-0.1200000000000046:0.5500000000000043 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-0.07050000000000978:0.5500000000000043 _clp_cinfo) _clpAdjustPt(0.2304999999999922:0.5500000000000043 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(0.2599999999999909:1 _clp_cinfo) _clpAdjustPt(-0.1000000000000085:1 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(0.3299999999999983:1 _clp_cinfo) _clpAdjustPt(0.3299999999999983:0.8488000000000042 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(0.2299999999999898:0.8488000000000042 _clp_cinfo) _clpAdjustPt(0.2299999999999898:0.8070000000000022 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(0.3549999999999898:1.009999999999998 _clp_cinfo) _clpAdjustPt(-0.1950000000000074:1.009999999999998 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-0.1042000000000058:0.75 _clp_cinfo) _clpAdjustPt(-0.08580000000000609:0.75 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(0.2800000000000011:0.5500000000000043 _clp_cinfo) _clpAdjustPt(0.2800000000000011:0.75 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(0.2304999999999922:0.75 _clp_cinfo) _clpAdjustPt(0.2457999999999885:0.75 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-0.07000000000000739:0.5502000000000038 _clp_cinfo) _clpAdjustPt(-0.07000000000000739:0.8070000000000022 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(0.2457999999999885:0.75 _clp_cinfo) _clpAdjustPt(0.2641999999999882:0.75 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-0.1700000000000017:1 _clp_cinfo) _clpAdjustPt(-0.1000000000000085:1 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-0.1350000000000051:0.6338000000000008 _clp_cinfo) _clpAdjustPt(-0.1350000000000051:0.6148999999999987 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(0.2949999999999875:0.6148999999999987 _clp_cinfo) _clpAdjustPt(0.664999999999992:0.6148999999999987 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(0.2099999999999938:-1.640000000000001 _clp_cinfo) _clpAdjustPt(0.2099999999999938:-1.949999999999996 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-0.1200000000000046:0.8000000000000043 _clp_cinfo) _clpAdjustPt(-0.1200000000000046:0.8488000000000042 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-0.1000000000000085:0.8488000000000042 _clp_cinfo) _clpAdjustPt(-0.1700000000000017:0.8488000000000042 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-0.1200000000000046:0.75 _clp_cinfo) _clpAdjustPt(-0.1042000000000058:0.75 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-0.07050000000000978:0.5500000000000043 _clp_cinfo) _clpAdjustPt(-0.08580000000000609:0.5500000000000043 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-0.1350000000000051:0.7220000000000013 _clp_cinfo) _clpAdjustPt(-0.1350000000000051:0.6338000000000008 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-0.1350000000000051:0.7899999999999992 _clp_cinfo) _clpAdjustPt(-0.1350000000000051:0.7220000000000013 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(0.2800000000000011:0.5500000000000043 _clp_cinfo) _clpAdjustPt(0.2641999999999882:0.5500000000000043 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(0.2949999999999875:0.7220000000000013 _clp_cinfo) _clpAdjustPt(0.2949999999999875:0.7899999999999992 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-0.1042000000000058:0.5500000000000043 _clp_cinfo) _clpAdjustPt(-0.1200000000000046:0.5500000000000043 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(0.664999999999992:0.7220000000000013 _clp_cinfo) _clpAdjustPt(0.2949999999999875:0.7220000000000013 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-0.08580000000000609:0.5500000000000043 _clp_cinfo) _clpAdjustPt(-0.1042000000000058:0.5500000000000043 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(0.2800000000000011:0.8488000000000042 _clp_cinfo) _clpAdjustPt(0.2800000000000011:0.8000000000000043 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(0.2949999999999875:0.7899999999999992 _clp_cinfo) _clpAdjustPt(0.3549999999999898:0.7899999999999992 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-0.1950000000000074:1.009999999999998 _clp_cinfo) _clpAdjustPt(-0.1950000000000074:0.7899999999999992 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(0.2949999999999875:0.6338000000000008 _clp_cinfo) _clpAdjustPt(0.2949999999999875:0.7220000000000013 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-1.670500000000004:0.5500000000000043 _clp_cinfo) _clpAdjustPt(-1.685800000000008:0.5500000000000043 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-2.020000000000003:-1.278700000000001 _clp_cinfo) _clpAdjustPt(2.179999999999993:-1.278700000000001 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-1.370000000000005:0.8488000000000042 _clp_cinfo) _clpAdjustPt(-1.370000000000005:0.8070000000000022 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-1.720000000000006:0.8000000000000043 _clp_cinfo) _clpAdjustPt(-1.720000000000006:0.8488000000000042 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-0.5900000000000034:-1.949999999999996 _clp_cinfo) _clpAdjustPt(-0.8500000000000085:-1.949999999999996 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-0.9950000000000046:0.7899999999999992 _clp_cinfo) _clpAdjustPt(-0.9350000000000023:0.7899999999999992 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-1.700000000000003:0.8488000000000042 _clp_cinfo) _clpAdjustPt(-1.770000000000003:0.8488000000000042 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-1.704200000000007:0.75 _clp_cinfo) _clpAdjustPt(-1.685800000000008:0.75 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-0.904200000000003:0.75 _clp_cinfo) _clpAdjustPt(-0.8858000000000033:0.75 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-1.670500000000004:0.5500000000000043 _clp_cinfo) _clpAdjustPt(-1.369500000000002:0.5500000000000043 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-0.5400000000000063:1 _clp_cinfo) _clpAdjustPt(-0.4699999999999989:1 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-1.340000000000003:1 _clp_cinfo) _clpAdjustPt(-1.270000000000003:1 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-0.4450000000000074:1.009999999999998 _clp_cinfo) _clpAdjustPt(-0.9950000000000046:1.009999999999998 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-1.335800000000006:0.5500000000000043 _clp_cinfo) _clpAdjustPt(-1.354200000000006:0.5500000000000043 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-1.795000000000009:1.009999999999998 _clp_cinfo) _clpAdjustPt(-1.795000000000009:0.7899999999999992 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-0.8705000000000069:0.5500000000000043 _clp_cinfo) _clpAdjustPt(-0.569500000000005:0.5500000000000043 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

printf(" 10 percent completed")
newline()

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-0.9200000000000088:0.8000000000000043 _clp_cinfo) _clpAdjustPt(-0.9200000000000088:0.8488000000000042 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-1.245000000000005:0.7899999999999992 _clp_cinfo) _clpAdjustPt(-1.245000000000005:1.009999999999998 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-0.8858000000000033:0.75 _clp_cinfo) _clpAdjustPt(-0.8705000000000069:0.75 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-1.270000000000003:0.8488000000000042 _clp_cinfo) _clpAdjustPt(-1.270000000000003:1 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-0.8700000000000046:0.5502000000000038 _clp_cinfo) _clpAdjustPt(-0.8700000000000046:0.8070000000000022 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-0.970000000000006:1 _clp_cinfo) _clpAdjustPt(-0.9000000000000057:1 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-0.5900000000000034:-1.640000000000001 _clp_cinfo) _clpAdjustPt(-0.5900000000000034:-1.949999999999996 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-0.9200000000000088:0.75 _clp_cinfo) _clpAdjustPt(-0.9200000000000088:0.5500000000000043 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-1.685800000000008:0.75 _clp_cinfo) _clpAdjustPt(-1.670500000000004:0.75 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-0.4699999999999989:0.8488000000000042 _clp_cinfo) _clpAdjustPt(-0.5400000000000063:0.8488000000000042 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-0.8858000000000033:0.5500000000000043 _clp_cinfo) _clpAdjustPt(-0.904200000000003:0.5500000000000043 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-0.5050000000000097:0.6148999999999987 _clp_cinfo) _clpAdjustPt(-0.1350000000000051:0.6148999999999987 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-1.354200000000006:0.75 _clp_cinfo) _clpAdjustPt(-1.335800000000006:0.75 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-0.904200000000003:0.5500000000000043 _clp_cinfo) _clpAdjustPt(-0.9200000000000088:0.5500000000000043 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-0.9350000000000023:0.7220000000000013 _clp_cinfo) _clpAdjustPt(-1.305000000000007:0.7220000000000013 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-0.5358000000000089:0.75 _clp_cinfo) _clpAdjustPt(-0.5200000000000102:0.75 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-1.390000000000008:-1.949999999999996 _clp_cinfo) _clpAdjustPt(-1.650000000000006:-1.949999999999996 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-1.335800000000006:0.75 _clp_cinfo) _clpAdjustPt(-1.320000000000007:0.75 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-1.305000000000007:0.7220000000000013 _clp_cinfo) _clpAdjustPt(-1.305000000000007:0.7899999999999992 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-1.795000000000009:0.7899999999999992 _clp_cinfo) _clpAdjustPt(-1.735000000000007:0.7899999999999992 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-0.5700000000000074:0.8488000000000042 _clp_cinfo) _clpAdjustPt(-0.5700000000000074:0.8070000000000022 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-1.370000000000005:0.8070000000000022 _clp_cinfo) _clpAdjustPt(-1.370000000000005:0.5502000000000038 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-1.305000000000007:0.6148999999999987 _clp_cinfo) _clpAdjustPt(-0.9350000000000023:0.6148999999999987 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-1.670000000000009:0.5502000000000038 _clp_cinfo) _clpAdjustPt(-1.670000000000009:0.8070000000000022 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-1.354200000000006:0.5500000000000043 _clp_cinfo) _clpAdjustPt(-1.369500000000002:0.5500000000000043 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-1.245000000000005:1.009999999999998 _clp_cinfo) _clpAdjustPt(-1.795000000000009:1.009999999999998 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-0.5358000000000089:0.5500000000000043 _clp_cinfo) _clpAdjustPt(-0.5542000000000087:0.5500000000000043 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-0.5050000000000097:0.6338000000000008 _clp_cinfo) _clpAdjustPt(-0.1350000000000051:0.6338000000000008 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-1.305000000000007:0.6338000000000008 _clp_cinfo) _clpAdjustPt(-0.9350000000000023:0.6338000000000008 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-2.020000000000003:-1.640000000000001 _clp_cinfo) _clpAdjustPt(2.179999999999993:-1.640000000000001 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-0.9350000000000023:0.7220000000000013 _clp_cinfo) _clpAdjustPt(-0.9350000000000023:0.6338000000000008 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-0.9950000000000046:1.009999999999998 _clp_cinfo) _clpAdjustPt(-0.9950000000000046:0.7899999999999992 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-0.970000000000006:1 _clp_cinfo) _clpAdjustPt(-0.970000000000006:0.8488000000000042 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-0.4699999999999989:1 _clp_cinfo) _clpAdjustPt(-0.4699999999999989:0.8488000000000042 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-0.5542000000000087:0.75 _clp_cinfo) _clpAdjustPt(-0.5358000000000089:0.75 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-0.8705000000000069:0.5500000000000043 _clp_cinfo) _clpAdjustPt(-0.8858000000000033:0.5500000000000043 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-0.5200000000000102:0.5500000000000043 _clp_cinfo) _clpAdjustPt(-0.5200000000000102:0.75 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-1.720000000000006:0.75 _clp_cinfo) _clpAdjustPt(-1.720000000000006:0.5500000000000043 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-1.320000000000007:0.5500000000000043 _clp_cinfo) _clpAdjustPt(-1.320000000000007:0.75 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-0.9350000000000023:0.7899999999999992 _clp_cinfo) _clpAdjustPt(-0.9350000000000023:0.7220000000000013 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-0.5050000000000097:0.6148999999999987 _clp_cinfo) _clpAdjustPt(-0.5050000000000097:0.6338000000000008 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-1.700000000000003:0.8488000000000042 _clp_cinfo) _clpAdjustPt(-1.340000000000003:0.8488000000000042 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-1.700000000000003:1 _clp_cinfo) _clpAdjustPt(-1.340000000000003:1 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-0.8700000000000046:0.8070000000000022 _clp_cinfo) _clpAdjustPt(-0.8700000000000046:0.8488000000000042 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-1.270000000000003:0.8488000000000042 _clp_cinfo) _clpAdjustPt(-1.340000000000003:0.8488000000000042 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-1.305000000000007:0.7899999999999992 _clp_cinfo) _clpAdjustPt(-1.245000000000005:0.7899999999999992 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-1.390000000000008:-1.640000000000001 _clp_cinfo) _clpAdjustPt(-1.390000000000008:-1.949999999999996 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-0.8500000000000085:-1.640000000000001 _clp_cinfo) _clpAdjustPt(-0.8500000000000085:-1.949999999999996 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-1.720000000000006:0.8000000000000043 _clp_cinfo) _clpAdjustPt(-1.720000000000006:0.75 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-1.735000000000007:0.6338000000000008 _clp_cinfo) _clpAdjustPt(-1.735000000000007:0.6148999999999987 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-1.770000000000003:1 _clp_cinfo) _clpAdjustPt(-1.770000000000003:0.8488000000000042 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-1.735000000000007:0.7220000000000013 _clp_cinfo) _clpAdjustPt(-1.735000000000007:0.6338000000000008 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-1.650000000000006:-1.640000000000001 _clp_cinfo) _clpAdjustPt(-1.650000000000006:-1.949999999999996 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-0.5050000000000097:0.7899999999999992 _clp_cinfo) _clpAdjustPt(-0.4450000000000074:0.7899999999999992 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-1.305000000000007:0.6338000000000008 _clp_cinfo) _clpAdjustPt(-1.305000000000007:0.7220000000000013 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-0.5050000000000097:0.7220000000000013 _clp_cinfo) _clpAdjustPt(-0.5050000000000097:0.7899999999999992 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-1.670000000000009:0.8070000000000022 _clp_cinfo) _clpAdjustPt(-1.670000000000009:0.8488000000000042 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-1.704200000000007:0.5500000000000043 _clp_cinfo) _clpAdjustPt(-1.720000000000006:0.5500000000000043 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-1.770000000000003:1 _clp_cinfo) _clpAdjustPt(-1.700000000000003:1 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-0.5200000000000102:0.8000000000000043 _clp_cinfo) _clpAdjustPt(-0.5200000000000102:0.75 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-0.5050000000000097:0.6338000000000008 _clp_cinfo) _clpAdjustPt(-0.5050000000000097:0.7220000000000013 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-1.305000000000007:0.6148999999999987 _clp_cinfo) _clpAdjustPt(-1.305000000000007:0.6338000000000008 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-1.685800000000008:0.5500000000000043 _clp_cinfo) _clpAdjustPt(-1.704200000000007:0.5500000000000043 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

printf(" 20 percent completed")
newline()

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-1.320000000000007:0.8488000000000042 _clp_cinfo) _clpAdjustPt(-1.320000000000007:0.8000000000000043 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-1.320000000000007:0.8000000000000043 _clp_cinfo) _clpAdjustPt(-1.320000000000007:0.75 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-0.4450000000000074:0.7899999999999992 _clp_cinfo) _clpAdjustPt(-0.4450000000000074:1.009999999999998 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-1.720000000000006:0.75 _clp_cinfo) _clpAdjustPt(-1.704200000000007:0.75 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-0.569500000000005:0.75 _clp_cinfo) _clpAdjustPt(-0.5542000000000087:0.75 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-0.1350000000000051:0.7220000000000013 _clp_cinfo) _clpAdjustPt(-0.5050000000000097:0.7220000000000013 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-0.5700000000000074:0.8070000000000022 _clp_cinfo) _clpAdjustPt(-0.5700000000000074:0.5502000000000038 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-0.9000000000000057:0.8488000000000042 _clp_cinfo) _clpAdjustPt(-0.970000000000006:0.8488000000000042 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-1.735000000000007:0.7899999999999992 _clp_cinfo) _clpAdjustPt(-1.735000000000007:0.7220000000000013 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-0.9200000000000088:0.75 _clp_cinfo) _clpAdjustPt(-0.9200000000000088:0.8000000000000043 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-2.020000000000003:-1.640000000000001 _clp_cinfo) _clpAdjustPt(-2.020000000000003:-1.278700000000001 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-0.5400000000000063:1 _clp_cinfo) _clpAdjustPt(-0.9000000000000057:1 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-0.9000000000000057:0.8488000000000042 _clp_cinfo) _clpAdjustPt(-0.5400000000000063:0.8488000000000042 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-0.5542000000000087:0.5500000000000043 _clp_cinfo) _clpAdjustPt(-0.569500000000005:0.5500000000000043 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-1.369500000000002:0.75 _clp_cinfo) _clpAdjustPt(-1.354200000000006:0.75 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-0.9350000000000023:0.6338000000000008 _clp_cinfo) _clpAdjustPt(-0.9350000000000023:0.6148999999999987 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-1.320000000000007:0.5500000000000043 _clp_cinfo) _clpAdjustPt(-1.335800000000006:0.5500000000000043 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-0.5200000000000102:0.5500000000000043 _clp_cinfo) _clpAdjustPt(-0.5358000000000089:0.5500000000000043 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-0.5200000000000102:0.8488000000000042 _clp_cinfo) _clpAdjustPt(-0.5200000000000102:0.8000000000000043 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-0.9200000000000088:0.75 _clp_cinfo) _clpAdjustPt(-0.904200000000003:0.75 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_path = _clpPathStart(list(_clpAdjustPt(3.954999999999998:-0.990000000000002 _clp_cinfo))                  
	_clpMKSConvert(0.000000 _clp_cinfo->t_from_units                  			_clp_cinfo->t_to_units))
_clp_path = _clpPathArcCenter(_clp_path _clpMKSConvert( 0.000000                   _clp_cinfo->t_from_units 
	_clp_cinfo->t_to_units)                   _clpAdjustPt(4.204999999999998:-0.740000000000002 _clp_cinfo) nil
 	_clpAdjustPt(3.955003700958343:-0.7400037009583542 _clp_cinfo))
_clp_dbid = _clpDBCreatePath(_clp_path "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = caar(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(1.830500000000001:0.75 _clp_cinfo) _clpAdjustPt(1.845799999999997:0.75 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(1.845799999999997:0.5500000000000043 _clp_cinfo) _clpAdjustPt(1.830500000000001:0.5500000000000043 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(1.879999999999996:0.5500000000000043 _clp_cinfo) _clpAdjustPt(1.879999999999996:0.75 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(1.864199999999997:0.75 _clp_cinfo) _clpAdjustPt(1.879999999999996:0.75 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(1.879999999999996:0.5500000000000043 _clp_cinfo) _clpAdjustPt(1.864199999999997:0.5500000000000043 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(3.954999999999998:-0.990000000000002 _clp_cinfo) _clpAdjustPt(2.629999999999996:-0.990000000000002 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(0.6799999999999926:0.75 _clp_cinfo) _clpAdjustPt(0.6957999999999913:0.75 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(1.845799999999997:0.75 _clp_cinfo) _clpAdjustPt(1.864199999999997:0.75 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(1.0642:0.75 _clp_cinfo) _clpAdjustPt(1.079999999999998:0.75 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(0.7141999999999911:0.75 _clp_cinfo) _clpAdjustPt(0.7294999999999874:0.75 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(1.809999999999988:-1.949999999999996 _clp_cinfo) _clpAdjustPt(1.549999999999997:-1.949999999999996 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(0.75:-1.949999999999996 _clp_cinfo) _clpAdjustPt(0.75:-1.640000000000001 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(0.6299999999999955:1 _clp_cinfo) _clpAdjustPt(0.6299999999999955:0.8488000000000042 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(1.464999999999989:0.7220000000000013 _clp_cinfo) _clpAdjustPt(1.464999999999989:0.6338000000000008 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(1.529499999999999:0.5500000000000043 _clp_cinfo) _clpAdjustPt(1.830500000000001:0.5500000000000043 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(0.7141999999999911:0.5500000000000043 _clp_cinfo) _clpAdjustPt(0.6957999999999913:0.5500000000000043 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(1.0642:0.5500000000000043 _clp_cinfo) _clpAdjustPt(1.0458:0.5500000000000043 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(1.009999999999991:-1.949999999999996 _clp_cinfo) _clpAdjustPt(0.75:-1.949999999999996 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(1.155000000000001:1.009999999999998 _clp_cinfo) _clpAdjustPt(0.6049999999999898:1.009999999999998 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(1.429999999999993:1 _clp_cinfo) _clpAdjustPt(1.5:1 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(1.079999999999998:0.8000000000000043 _clp_cinfo) _clpAdjustPt(1.079999999999998:0.75 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(0.6799999999999926:0.75 _clp_cinfo) _clpAdjustPt(0.6799999999999926:0.5500000000000043 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(1.5:0.8488000000000042 _clp_cinfo) _clpAdjustPt(1.429999999999993:0.8488000000000042 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(0.6999999999999886:0.8488000000000042 _clp_cinfo) _clpAdjustPt(0.6299999999999955:0.8488000000000042 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(1.809999999999988:-1.640000000000001 _clp_cinfo) _clpAdjustPt(1.809999999999988:-1.949999999999996 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(1.094999999999999:0.6148999999999987 _clp_cinfo) _clpAdjustPt(1.094999999999999:0.6338000000000008 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(1.059999999999988:1 _clp_cinfo) _clpAdjustPt(1.129999999999996:1 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(1.954999999999998:0.7899999999999992 _clp_cinfo) _clpAdjustPt(1.954999999999998:1.009999999999998 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(0.6299999999999955:1 _clp_cinfo) _clpAdjustPt(0.6999999999999886:1 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(2.879999999999996:-1.640000000000001 _clp_cinfo) _clpAdjustPt(2.97999999999999:-1.640000000000001 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(0.6799999999999926:0.8000000000000043 _clp_cinfo) _clpAdjustPt(0.6799999999999926:0.8488000000000042 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(1.47999999999999:0.8000000000000043 _clp_cinfo) _clpAdjustPt(1.47999999999999:0.75 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(1.530000000000001:0.8070000000000022 _clp_cinfo) _clpAdjustPt(1.530000000000001:0.8488000000000042 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(1.405000000000001:1.009999999999998 _clp_cinfo) _clpAdjustPt(1.405000000000001:0.7899999999999992 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(0.664999999999992:0.7899999999999992 _clp_cinfo) _clpAdjustPt(0.664999999999992:0.7220000000000013 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(1.464999999999989:0.7899999999999992 _clp_cinfo) _clpAdjustPt(1.464999999999989:0.7220000000000013 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(1.079999999999998:0.5500000000000043 _clp_cinfo) _clpAdjustPt(1.079999999999998:0.75 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(2.530000000000001:-0.990000000000002 _clp_cinfo) _clpAdjustPt(2.629999999999996:-0.990000000000002 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(1.079999999999998:0.8488000000000042 _clp_cinfo) _clpAdjustPt(1.079999999999998:0.8000000000000043 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(2.530000000000001:-0.990000000000002 _clp_cinfo) _clpAdjustPt(2.179999999999993:-1.278700000000001 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(0.6049999999999898:1.009999999999998 _clp_cinfo) _clpAdjustPt(0.6049999999999898:0.7899999999999992 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(2.879999999999996:-1.240000000000002 _clp_cinfo) _clpAdjustPt(2.629999999999996:-0.990000000000002 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(1.5:0.8488000000000042 _clp_cinfo) _clpAdjustPt(1.859999999999999:0.8488000000000042 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

printf(" 30 percent completed")
newline()

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(2.317999999999998:0.7220000000000013 _clp_cinfo) _clpAdjustPt(1.894999999999996:0.7220000000000013 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(1.495799999999989:0.75 _clp_cinfo) _clpAdjustPt(1.514199999999988:0.75 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(1.879999999999996:0.8000000000000043 _clp_cinfo) _clpAdjustPt(1.879999999999996:0.75 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(1.030000000000001:0.8488000000000042 _clp_cinfo) _clpAdjustPt(1.030000000000001:0.8070000000000022 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(0.6049999999999898:0.7899999999999992 _clp_cinfo) _clpAdjustPt(0.664999999999992:0.7899999999999992 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(1.894999999999996:0.6338000000000008 _clp_cinfo) _clpAdjustPt(1.894999999999996:0.7220000000000013 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(1.894999999999996:0.7899999999999992 _clp_cinfo) _clpAdjustPt(1.954999999999998:0.7899999999999992 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(1.094999999999999:0.6338000000000008 _clp_cinfo) _clpAdjustPt(1.094999999999999:0.7220000000000013 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(1.530000000000001:0.5502000000000038 _clp_cinfo) _clpAdjustPt(1.530000000000001:0.8070000000000022 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(1.929999999999993:0.8488000000000042 _clp_cinfo) _clpAdjustPt(1.859999999999999:0.8488000000000042 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(1.514199999999988:0.5500000000000043 _clp_cinfo) _clpAdjustPt(1.495799999999989:0.5500000000000043 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(1.429999999999993:1 _clp_cinfo) _clpAdjustPt(1.429999999999993:0.8488000000000042 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(1.864199999999997:0.5500000000000043 _clp_cinfo) _clpAdjustPt(1.845799999999997:0.5500000000000043 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(0.7294999999999874:0.5500000000000043 _clp_cinfo) _clpAdjustPt(0.7141999999999911:0.5500000000000043 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(1.514199999999988:0.75 _clp_cinfo) _clpAdjustPt(1.529499999999999:0.75 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(1.549999999999997:-1.640000000000001 _clp_cinfo) _clpAdjustPt(1.549999999999997:-1.949999999999996 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(2.879999999999996:-1.240000000000002 _clp_cinfo) _clpAdjustPt(2.879999999999996:-1.640000000000001 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(1.829999999999998:0.8488000000000042 _clp_cinfo) _clpAdjustPt(1.829999999999998:0.8070000000000022 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(2.317999999999998:0.7220000000000013 _clp_cinfo) _clpAdjustPt(2.346799999999988:0.6932000000000045 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(1.954999999999998:1.009999999999998 _clp_cinfo) _clpAdjustPt(1.405000000000001:1.009999999999998 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(0.7299999999999898:0.8070000000000022 _clp_cinfo) _clpAdjustPt(0.7299999999999898:0.8488000000000042 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(1.47999999999999:0.8000000000000043 _clp_cinfo) _clpAdjustPt(1.47999999999999:0.8488000000000042 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(1.464999999999989:0.6338000000000008 _clp_cinfo) _clpAdjustPt(1.464999999999989:0.6148999999999987 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(2.425100000000001:0.8149000000000015 _clp_cinfo) _clpAdjustPt(2.425100000000001:1.705100000000002 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(1.030499999999989:0.5500000000000043 _clp_cinfo) _clpAdjustPt(0.7294999999999874:0.5500000000000043 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(2.406199999999998:0.8337000000000003 _clp_cinfo) _clpAdjustPt(2.406199999999998:1.6862 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(2.317999999999998:1.798000000000002 _clp_cinfo) _clpAdjustPt(2.317999999999998:0.7220000000000013 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(1.929999999999993:0.8488000000000042 _clp_cinfo) _clpAdjustPt(1.929999999999993:1 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(2.97999999999999:-1.740000000000002 _clp_cinfo) _clpAdjustPt(2.97999999999999:-1.640000000000001 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(1.129999999999996:0.8488000000000042 _clp_cinfo) _clpAdjustPt(1.059999999999988:0.8488000000000042 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(1.529499999999999:0.5500000000000043 _clp_cinfo) _clpAdjustPt(1.514199999999988:0.5500000000000043 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(1.094999999999999:0.7220000000000013 _clp_cinfo) _clpAdjustPt(1.094999999999999:0.7899999999999992 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(1.829999999999998:0.8070000000000022 _clp_cinfo) _clpAdjustPt(1.829999999999998:0.5502000000000038 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(1.47999999999999:0.75 _clp_cinfo) _clpAdjustPt(1.495799999999989:0.75 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(1.155000000000001:0.7899999999999992 _clp_cinfo) _clpAdjustPt(1.155000000000001:1.009999999999998 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(1.5:1 _clp_cinfo) _clpAdjustPt(1.859999999999999:1 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(1.879999999999996:0.8488000000000042 _clp_cinfo) _clpAdjustPt(1.879999999999996:0.8000000000000043 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(1.495799999999989:0.5500000000000043 _clp_cinfo) _clpAdjustPt(1.47999999999999:0.5500000000000043 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(1.094999999999999:0.6338000000000008 _clp_cinfo) _clpAdjustPt(1.464999999999989:0.6338000000000008 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(0.7299999999999898:0.5502000000000038 _clp_cinfo) _clpAdjustPt(0.7299999999999898:0.8070000000000022 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(0.664999999999992:0.6338000000000008 _clp_cinfo) _clpAdjustPt(0.664999999999992:0.6148999999999987 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(2.179999999999993:-1.278700000000001 _clp_cinfo) _clpAdjustPt(2.179999999999993:-1.640000000000001 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(1.894999999999996:0.6148999999999987 _clp_cinfo) _clpAdjustPt(1.894999999999996:0.6338000000000008 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(1.0458:0.75 _clp_cinfo) _clpAdjustPt(1.0642:0.75 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(2.879999999999996:-1.640000000000001 _clp_cinfo) _clpAdjustPt(2.179999999999993:-1.640000000000001 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(0.6957999999999913:0.5500000000000043 _clp_cinfo) _clpAdjustPt(0.6799999999999926:0.5500000000000043 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(1.0458:0.5500000000000043 _clp_cinfo) _clpAdjustPt(1.030499999999989:0.5500000000000043 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(1.059999999999988:1 _clp_cinfo) _clpAdjustPt(0.6999999999999886:1 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(1.47999999999999:0.75 _clp_cinfo) _clpAdjustPt(1.47999999999999:0.5500000000000043 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(1.894999999999996:0.6338000000000008 _clp_cinfo) _clpAdjustPt(2.206199999999996:0.6338000000000008 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(5.72999999999999:-1.740000000000002 _clp_cinfo) _clpAdjustPt(2.97999999999999:-1.740000000000002 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(1.094999999999999:0.6148999999999987 _clp_cinfo) _clpAdjustPt(1.464999999999989:0.6148999999999987 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(1.894999999999996:0.7220000000000013 _clp_cinfo) _clpAdjustPt(1.894999999999996:0.7899999999999992 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(1.094999999999999:0.7899999999999992 _clp_cinfo) _clpAdjustPt(1.155000000000001:0.7899999999999992 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(1.464999999999989:0.7220000000000013 _clp_cinfo) _clpAdjustPt(1.094999999999999:0.7220000000000013 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(1.059999999999988:0.8488000000000042 _clp_cinfo) _clpAdjustPt(0.6999999999999886:0.8488000000000042 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(1.030000000000001:0.8070000000000022 _clp_cinfo) _clpAdjustPt(1.030000000000001:0.5502000000000038 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(1.405000000000001:0.7899999999999992 _clp_cinfo) _clpAdjustPt(1.464999999999989:0.7899999999999992 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(1.009999999999991:-1.640000000000001 _clp_cinfo) _clpAdjustPt(1.009999999999991:-1.949999999999996 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(1.129999999999996:0.8488000000000042 _clp_cinfo) _clpAdjustPt(1.129999999999996:1 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(0.664999999999992:0.7220000000000013 _clp_cinfo) _clpAdjustPt(0.664999999999992:0.6338000000000008 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(1.079999999999998:0.5500000000000043 _clp_cinfo) _clpAdjustPt(1.0642:0.5500000000000043 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(1.859999999999999:1 _clp_cinfo) _clpAdjustPt(1.929999999999993:1 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

printf(" 40 percent completed")
newline()

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(0.6799999999999926:0.75 _clp_cinfo) _clpAdjustPt(0.6799999999999926:0.8000000000000043 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(1.030499999999989:0.75 _clp_cinfo) _clpAdjustPt(1.0458:0.75 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(0.6957999999999913:0.75 _clp_cinfo) _clpAdjustPt(0.7141999999999911:0.75 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(1.894999999999996:0.6148999999999987 _clp_cinfo) _clpAdjustPt(2.225099999999998:0.6148999999999987 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(2.530000000000001:-0.990000000000002 _clp_cinfo) _clpAdjustPt(-2.370000000000005:-0.990000000000002 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-2.265100000000004:1.705100000000002 _clp_cinfo) _clpAdjustPt(-2.265100000000004:0.8149000000000015 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-2.370000000000005:-0.990000000000002 _clp_cinfo) _clpAdjustPt(-2.020000000000003:-1.278700000000001 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-2.470000000000006:-0.990000000000002 _clp_cinfo) _clpAdjustPt(-2.370000000000005:-0.990000000000002 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-2.720000000000006:-1.640000000000001 _clp_cinfo) _clpAdjustPt(-2.720000000000006:-1.240000000000002 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-2.158000000000008:0.7220000000000013 _clp_cinfo) _clpAdjustPt(-2.158000000000008:1.798000000000002 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-1.735000000000007:0.7220000000000013 _clp_cinfo) _clpAdjustPt(-2.158000000000008:0.7220000000000013 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-2.020000000000003:-1.640000000000001 _clp_cinfo) _clpAdjustPt(-2.720000000000006:-1.640000000000001 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-2.246200000000009:1.6862 _clp_cinfo) _clpAdjustPt(-2.246200000000009:0.8337000000000003 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-2.820000000000007:-1.640000000000001 _clp_cinfo) _clpAdjustPt(-2.720000000000006:-1.640000000000001 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-2.820000000000007:-1.640000000000001 _clp_cinfo) _clpAdjustPt(-2.820000000000007:-1.740000000000002 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-2.720000000000006:-1.240000000000002 _clp_cinfo) _clpAdjustPt(-2.470000000000006:-0.990000000000002 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-2.158000000000008:0.7220000000000013 _clp_cinfo) _clpAdjustPt(-2.186800000000005:0.6932000000000045 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-2.065100000000008:0.6148999999999987 _clp_cinfo) _clpAdjustPt(-1.735000000000007:0.6148999999999987 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-2.046200000000006:0.6338000000000008 _clp_cinfo) _clpAdjustPt(-1.735000000000007:0.6338000000000008 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-0.05000000000001137:4.469999999999999 _clp_cinfo) _clpAdjustPt(0.2099999999999938:4.469999999999999 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-1.650000000000006:4.469999999999999 _clp_cinfo) _clpAdjustPt(-1.390000000000008:4.469999999999999 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-0.8500000000000085:4.469999999999999 _clp_cinfo) _clpAdjustPt(-0.5900000000000034:4.469999999999999 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(0.75:4.469999999999999 _clp_cinfo) _clpAdjustPt(1.009999999999991:4.469999999999999 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(1.549999999999997:4.469999999999999 _clp_cinfo) _clpAdjustPt(1.809999999999988:4.469999999999999 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(0.2099999999999938:4.160000000000004 _clp_cinfo) _clpAdjustPt(0.2099999999999938:4.469999999999999 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-0.05000000000001137:4.160000000000004 _clp_cinfo) _clpAdjustPt(-0.05000000000001137:4.469999999999999 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(0.2599999999999909:1.671100000000003 _clp_cinfo) _clpAdjustPt(0.3299999999999983:1.671100000000003 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(0.2299999999999898:1.969700000000003 _clp_cinfo) _clpAdjustPt(0.2299999999999898:1.713000000000001 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-0.1042000000000058:1.969999999999999 _clp_cinfo) _clpAdjustPt(-0.08580000000000609:1.969999999999999 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(0.2949999999999875:1.798000000000002 _clp_cinfo) _clpAdjustPt(0.664999999999992:1.798000000000002 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(0.664999999999992:1.886200000000002 _clp_cinfo) _clpAdjustPt(0.2949999999999875:1.886200000000002 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(0.2457999999999885:1.770000000000003 _clp_cinfo) _clpAdjustPt(0.2304999999999922:1.770000000000003 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(0.2800000000000011:1.719999999999999 _clp_cinfo) _clpAdjustPt(0.2800000000000011:1.671100000000003 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-0.1200000000000046:1.719999999999999 _clp_cinfo) _clpAdjustPt(-0.1200000000000046:1.770000000000003 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-0.08580000000000609:1.969999999999999 _clp_cinfo) _clpAdjustPt(-0.07050000000000978:1.969999999999999 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(0.2949999999999875:1.886200000000002 _clp_cinfo) _clpAdjustPt(0.2949999999999875:1.905100000000005 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(0.2641999999999882:1.969999999999999 _clp_cinfo) _clpAdjustPt(0.2800000000000011:1.969999999999999 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(0.3549999999999898:1.730000000000004 _clp_cinfo) _clpAdjustPt(0.2949999999999875:1.730000000000004 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(0.3299999999999983:1.520000000000003 _clp_cinfo) _clpAdjustPt(0.2599999999999909:1.520000000000003 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(0.3299999999999983:1.520000000000003 _clp_cinfo) _clpAdjustPt(0.3299999999999983:1.671100000000003 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-0.1200000000000046:1.969999999999999 _clp_cinfo) _clpAdjustPt(-0.1042000000000058:1.969999999999999 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(0.2800000000000011:1.770000000000003 _clp_cinfo) _clpAdjustPt(0.2641999999999882:1.770000000000003 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(0.2304999999999922:1.969999999999999 _clp_cinfo) _clpAdjustPt(-0.07050000000000978:1.969999999999999 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(0.2949999999999875:1.730000000000004 _clp_cinfo) _clpAdjustPt(0.2949999999999875:1.798000000000002 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(0.2457999999999885:1.969999999999999 _clp_cinfo) _clpAdjustPt(0.2641999999999882:1.969999999999999 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(0.2599999999999909:1.671100000000003 _clp_cinfo) _clpAdjustPt(-0.1000000000000085:1.671100000000003 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-0.07000000000000739:1.713000000000001 _clp_cinfo) _clpAdjustPt(-0.07000000000000739:1.969700000000003 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-0.07050000000000978:1.770000000000003 _clp_cinfo) _clpAdjustPt(-0.08580000000000609:1.770000000000003 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(0.3549999999999898:1.509999999999998 _clp_cinfo) _clpAdjustPt(0.3549999999999898:1.730000000000004 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(0.2800000000000011:1.770000000000003 _clp_cinfo) _clpAdjustPt(0.2800000000000011:1.969999999999999 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(0.664999999999992:1.905100000000005 _clp_cinfo) _clpAdjustPt(0.2949999999999875:1.905100000000005 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-0.1000000000000085:1.520000000000003 _clp_cinfo) _clpAdjustPt(-0.1700000000000017:1.520000000000003 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-0.08580000000000609:1.770000000000003 _clp_cinfo) _clpAdjustPt(-0.1042000000000058:1.770000000000003 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-0.1950000000000074:1.730000000000004 _clp_cinfo) _clpAdjustPt(-0.1950000000000074:1.509999999999998 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-0.1350000000000051:1.730000000000004 _clp_cinfo) _clpAdjustPt(-0.1950000000000074:1.730000000000004 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(0.2299999999999898:1.713000000000001 _clp_cinfo) _clpAdjustPt(0.2299999999999898:1.671100000000003 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(0.2304999999999922:1.969999999999999 _clp_cinfo) _clpAdjustPt(0.2457999999999885:1.969999999999999 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-0.1350000000000051:1.886200000000002 _clp_cinfo) _clpAdjustPt(-0.1350000000000051:1.798000000000002 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(0.2641999999999882:1.770000000000003 _clp_cinfo) _clpAdjustPt(0.2457999999999885:1.770000000000003 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-0.1950000000000074:1.509999999999998 _clp_cinfo) _clpAdjustPt(0.3549999999999898:1.509999999999998 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(0.2800000000000011:1.770000000000003 _clp_cinfo) _clpAdjustPt(0.2800000000000011:1.719999999999999 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(0.2949999999999875:1.798000000000002 _clp_cinfo) _clpAdjustPt(0.2949999999999875:1.886200000000002 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-0.1350000000000051:1.798000000000002 _clp_cinfo) _clpAdjustPt(-0.1350000000000051:1.730000000000004 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-0.1000000000000085:1.520000000000003 _clp_cinfo) _clpAdjustPt(0.2599999999999909:1.520000000000003 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

printf(" 50 percent completed")
newline()

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-0.1700000000000017:1.671100000000003 _clp_cinfo) _clpAdjustPt(-0.1000000000000085:1.671100000000003 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-0.1350000000000051:1.905100000000005 _clp_cinfo) _clpAdjustPt(-0.1350000000000051:1.886200000000002 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-0.1042000000000058:1.770000000000003 _clp_cinfo) _clpAdjustPt(-0.1200000000000046:1.770000000000003 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-0.1700000000000017:1.520000000000003 _clp_cinfo) _clpAdjustPt(-0.1700000000000017:1.671100000000003 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-0.1200000000000046:1.969999999999999 _clp_cinfo) _clpAdjustPt(-0.1200000000000046:1.770000000000003 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-0.07000000000000739:1.671100000000003 _clp_cinfo) _clpAdjustPt(-0.07000000000000739:1.713000000000001 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-0.1200000000000046:1.671100000000003 _clp_cinfo) _clpAdjustPt(-0.1200000000000046:1.719999999999999 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-0.5900000000000034:4.160000000000004 _clp_cinfo) _clpAdjustPt(-0.5900000000000034:4.469999999999999 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(2.179999999999993:4.160000000000004 _clp_cinfo) _clpAdjustPt(-2.020000000000003:4.160000000000004 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-1.390000000000008:4.160000000000004 _clp_cinfo) _clpAdjustPt(-1.390000000000008:4.469999999999999 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-0.8500000000000085:4.160000000000004 _clp_cinfo) _clpAdjustPt(-0.8500000000000085:4.469999999999999 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-2.020000000000003:3.798700000000004 _clp_cinfo) _clpAdjustPt(-2.020000000000003:4.160000000000004 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(2.179999999999993:3.798700000000004 _clp_cinfo) _clpAdjustPt(-2.020000000000003:3.798700000000004 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-1.650000000000006:4.160000000000004 _clp_cinfo) _clpAdjustPt(-1.650000000000006:4.469999999999999 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-1.354200000000006:1.770000000000003 _clp_cinfo) _clpAdjustPt(-1.369500000000002:1.770000000000003 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-1.795000000000009:1.730000000000004 _clp_cinfo) _clpAdjustPt(-1.795000000000009:1.509999999999998 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-1.700000000000003:1.520000000000003 _clp_cinfo) _clpAdjustPt(-1.770000000000003:1.520000000000003 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-1.270000000000003:1.520000000000003 _clp_cinfo) _clpAdjustPt(-1.340000000000003:1.520000000000003 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-0.5050000000000097:1.886200000000002 _clp_cinfo) _clpAdjustPt(-0.5050000000000097:1.905100000000005 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-0.4699999999999989:1.520000000000003 _clp_cinfo) _clpAdjustPt(-0.5400000000000063:1.520000000000003 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-1.340000000000003:1.671100000000003 _clp_cinfo) _clpAdjustPt(-1.270000000000003:1.671100000000003 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-1.305000000000007:1.730000000000004 _clp_cinfo) _clpAdjustPt(-1.305000000000007:1.798000000000002 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-0.4450000000000074:1.509999999999998 _clp_cinfo) _clpAdjustPt(-0.4450000000000074:1.730000000000004 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-0.5700000000000074:1.969700000000003 _clp_cinfo) _clpAdjustPt(-0.5700000000000074:1.713000000000001 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-0.904200000000003:1.770000000000003 _clp_cinfo) _clpAdjustPt(-0.9200000000000088:1.770000000000003 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-0.1350000000000051:1.886200000000002 _clp_cinfo) _clpAdjustPt(-0.5050000000000097:1.886200000000002 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-1.700000000000003:1.520000000000003 _clp_cinfo) _clpAdjustPt(-1.340000000000003:1.520000000000003 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-1.735000000000007:1.730000000000004 _clp_cinfo) _clpAdjustPt(-1.795000000000009:1.730000000000004 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-1.770000000000003:1.671100000000003 _clp_cinfo) _clpAdjustPt(-1.700000000000003:1.671100000000003 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-1.735000000000007:1.798000000000002 _clp_cinfo) _clpAdjustPt(-1.735000000000007:1.730000000000004 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-1.720000000000006:1.969999999999999 _clp_cinfo) _clpAdjustPt(-1.720000000000006:1.770000000000003 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-1.704200000000007:1.770000000000003 _clp_cinfo) _clpAdjustPt(-1.720000000000006:1.770000000000003 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-0.5400000000000063:1.671100000000003 _clp_cinfo) _clpAdjustPt(-0.4699999999999989:1.671100000000003 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-0.569500000000005:1.969999999999999 _clp_cinfo) _clpAdjustPt(-0.5542000000000087:1.969999999999999 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-0.5050000000000097:1.798000000000002 _clp_cinfo) _clpAdjustPt(-0.1350000000000051:1.798000000000002 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-0.1350000000000051:1.905100000000005 _clp_cinfo) _clpAdjustPt(-0.5050000000000097:1.905100000000005 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-0.8858000000000033:1.770000000000003 _clp_cinfo) _clpAdjustPt(-0.904200000000003:1.770000000000003 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-1.685800000000008:1.969999999999999 _clp_cinfo) _clpAdjustPt(-1.670500000000004:1.969999999999999 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-0.970000000000006:1.520000000000003 _clp_cinfo) _clpAdjustPt(-0.970000000000006:1.671100000000003 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-1.354200000000006:1.969999999999999 _clp_cinfo) _clpAdjustPt(-1.335800000000006:1.969999999999999 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-0.9350000000000023:1.798000000000002 _clp_cinfo) _clpAdjustPt(-0.9350000000000023:1.730000000000004 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-0.8705000000000069:1.770000000000003 _clp_cinfo) _clpAdjustPt(-0.8858000000000033:1.770000000000003 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-0.8700000000000046:1.713000000000001 _clp_cinfo) _clpAdjustPt(-0.8700000000000046:1.969700000000003 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-0.9350000000000023:1.886200000000002 _clp_cinfo) _clpAdjustPt(-0.9350000000000023:1.798000000000002 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-0.5200000000000102:1.770000000000003 _clp_cinfo) _clpAdjustPt(-0.5200000000000102:1.719999999999999 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-1.320000000000007:1.719999999999999 _clp_cinfo) _clpAdjustPt(-1.320000000000007:1.671100000000003 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-1.720000000000006:1.719999999999999 _clp_cinfo) _clpAdjustPt(-1.720000000000006:1.770000000000003 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-1.305000000000007:1.886200000000002 _clp_cinfo) _clpAdjustPt(-1.305000000000007:1.905100000000005 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-0.5050000000000097:1.798000000000002 _clp_cinfo) _clpAdjustPt(-0.5050000000000097:1.886200000000002 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-1.670000000000009:1.671100000000003 _clp_cinfo) _clpAdjustPt(-1.670000000000009:1.713000000000001 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-1.245000000000005:1.730000000000004 _clp_cinfo) _clpAdjustPt(-1.305000000000007:1.730000000000004 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-1.720000000000006:1.671100000000003 _clp_cinfo) _clpAdjustPt(-1.720000000000006:1.719999999999999 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-1.685800000000008:1.770000000000003 _clp_cinfo) _clpAdjustPt(-1.704200000000007:1.770000000000003 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-1.335800000000006:1.969999999999999 _clp_cinfo) _clpAdjustPt(-1.320000000000007:1.969999999999999 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-1.735000000000007:1.886200000000002 _clp_cinfo) _clpAdjustPt(-1.735000000000007:1.798000000000002 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-0.9350000000000023:1.886200000000002 _clp_cinfo) _clpAdjustPt(-1.305000000000007:1.886200000000002 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-0.9200000000000088:1.969999999999999 _clp_cinfo) _clpAdjustPt(-0.9200000000000088:1.770000000000003 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-1.735000000000007:1.905100000000005 _clp_cinfo) _clpAdjustPt(-1.735000000000007:1.886200000000002 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-0.5358000000000089:1.969999999999999 _clp_cinfo) _clpAdjustPt(-0.5200000000000102:1.969999999999999 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-1.720000000000006:1.969999999999999 _clp_cinfo) _clpAdjustPt(-1.704200000000007:1.969999999999999 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-1.320000000000007:1.770000000000003 _clp_cinfo) _clpAdjustPt(-1.335800000000006:1.770000000000003 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-0.9200000000000088:1.969999999999999 _clp_cinfo) _clpAdjustPt(-0.904200000000003:1.969999999999999 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-0.970000000000006:1.671100000000003 _clp_cinfo) _clpAdjustPt(-0.9000000000000057:1.671100000000003 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

printf(" 60 percent completed")
newline()

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-0.9350000000000023:1.905100000000005 _clp_cinfo) _clpAdjustPt(-0.9350000000000023:1.886200000000002 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-1.335800000000006:1.770000000000003 _clp_cinfo) _clpAdjustPt(-1.354200000000006:1.770000000000003 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-0.9950000000000046:1.730000000000004 _clp_cinfo) _clpAdjustPt(-0.9950000000000046:1.509999999999998 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-0.5400000000000063:1.671100000000003 _clp_cinfo) _clpAdjustPt(-0.9000000000000057:1.671100000000003 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-0.5358000000000089:1.770000000000003 _clp_cinfo) _clpAdjustPt(-0.5542000000000087:1.770000000000003 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-0.5542000000000087:1.770000000000003 _clp_cinfo) _clpAdjustPt(-0.569500000000005:1.770000000000003 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-1.370000000000005:1.713000000000001 _clp_cinfo) _clpAdjustPt(-1.370000000000005:1.671100000000003 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-0.5200000000000102:1.770000000000003 _clp_cinfo) _clpAdjustPt(-0.5200000000000102:1.969999999999999 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-0.9350000000000023:1.905100000000005 _clp_cinfo) _clpAdjustPt(-1.305000000000007:1.905100000000005 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-0.9000000000000057:1.520000000000003 _clp_cinfo) _clpAdjustPt(-0.5400000000000063:1.520000000000003 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-1.770000000000003:1.671100000000003 _clp_cinfo) _clpAdjustPt(-1.770000000000003:1.520000000000003 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-0.5700000000000074:1.713000000000001 _clp_cinfo) _clpAdjustPt(-0.5700000000000074:1.671100000000003 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-1.795000000000009:1.509999999999998 _clp_cinfo) _clpAdjustPt(-1.245000000000005:1.509999999999998 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-1.305000000000007:1.798000000000002 _clp_cinfo) _clpAdjustPt(-1.305000000000007:1.886200000000002 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-1.369500000000002:1.969999999999999 _clp_cinfo) _clpAdjustPt(-1.670500000000004:1.969999999999999 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-1.369500000000002:1.969999999999999 _clp_cinfo) _clpAdjustPt(-1.354200000000006:1.969999999999999 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-1.670000000000009:1.713000000000001 _clp_cinfo) _clpAdjustPt(-1.670000000000009:1.969700000000003 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-0.8700000000000046:1.671100000000003 _clp_cinfo) _clpAdjustPt(-0.8700000000000046:1.713000000000001 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-0.4450000000000074:1.730000000000004 _clp_cinfo) _clpAdjustPt(-0.5050000000000097:1.730000000000004 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-1.670500000000004:1.770000000000003 _clp_cinfo) _clpAdjustPt(-1.685800000000008:1.770000000000003 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-1.305000000000007:1.798000000000002 _clp_cinfo) _clpAdjustPt(-0.9350000000000023:1.798000000000002 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-0.904200000000003:1.969999999999999 _clp_cinfo) _clpAdjustPt(-0.8858000000000033:1.969999999999999 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-0.5050000000000097:1.730000000000004 _clp_cinfo) _clpAdjustPt(-0.5050000000000097:1.798000000000002 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-1.704200000000007:1.969999999999999 _clp_cinfo) _clpAdjustPt(-1.685800000000008:1.969999999999999 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-0.5542000000000087:1.969999999999999 _clp_cinfo) _clpAdjustPt(-0.5358000000000089:1.969999999999999 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-0.4699999999999989:1.520000000000003 _clp_cinfo) _clpAdjustPt(-0.4699999999999989:1.671100000000003 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-0.9000000000000057:1.520000000000003 _clp_cinfo) _clpAdjustPt(-0.970000000000006:1.520000000000003 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-1.700000000000003:1.671100000000003 _clp_cinfo) _clpAdjustPt(-1.340000000000003:1.671100000000003 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-1.270000000000003:1.520000000000003 _clp_cinfo) _clpAdjustPt(-1.270000000000003:1.671100000000003 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-0.9200000000000088:1.671100000000003 _clp_cinfo) _clpAdjustPt(-0.9200000000000088:1.719999999999999 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-1.245000000000005:1.509999999999998 _clp_cinfo) _clpAdjustPt(-1.245000000000005:1.730000000000004 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-0.9950000000000046:1.509999999999998 _clp_cinfo) _clpAdjustPt(-0.4450000000000074:1.509999999999998 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-0.9350000000000023:1.730000000000004 _clp_cinfo) _clpAdjustPt(-0.9950000000000046:1.730000000000004 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-1.370000000000005:1.969700000000003 _clp_cinfo) _clpAdjustPt(-1.370000000000005:1.713000000000001 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-1.320000000000007:1.770000000000003 _clp_cinfo) _clpAdjustPt(-1.320000000000007:1.969999999999999 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-0.9200000000000088:1.719999999999999 _clp_cinfo) _clpAdjustPt(-0.9200000000000088:1.770000000000003 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-1.320000000000007:1.770000000000003 _clp_cinfo) _clpAdjustPt(-1.320000000000007:1.719999999999999 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-0.5200000000000102:1.719999999999999 _clp_cinfo) _clpAdjustPt(-0.5200000000000102:1.671100000000003 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-0.569500000000005:1.969999999999999 _clp_cinfo) _clpAdjustPt(-0.8705000000000069:1.969999999999999 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-0.5200000000000102:1.770000000000003 _clp_cinfo) _clpAdjustPt(-0.5358000000000089:1.770000000000003 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-0.8858000000000033:1.969999999999999 _clp_cinfo) _clpAdjustPt(-0.8705000000000069:1.969999999999999 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_path = _clpPathStart(list(_clpAdjustPt(4.204999999999998:1.310000000000002 _clp_cinfo))                  
	_clpMKSConvert(0.000000 _clp_cinfo->t_from_units                  			_clp_cinfo->t_to_units))
_clp_path = _clpPathArcCenter(_clp_path _clpMKSConvert( 0.000000                   _clp_cinfo->t_from_units 
	_clp_cinfo->t_to_units)                   _clpAdjustPt(3.954999999999998:1.560000000000002 _clp_cinfo) nil
 	_clpAdjustPt(3.954991452522009:1.309991452522013 _clp_cinfo))
_clp_dbid = _clpDBCreatePath(_clp_path "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = caar(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(2.629999999999996:3.509999999999998 _clp_cinfo) _clpAdjustPt(3.179999999999993:3.509999999999998 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(2.879999999999996:4.160000000000004 _clp_cinfo) _clpAdjustPt(2.97999999999999:4.160000000000004 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(2.530000000000001:3.509999999999998 _clp_cinfo) _clpAdjustPt(2.179999999999993:3.798700000000004 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(1.549999999999997:4.160000000000004 _clp_cinfo) _clpAdjustPt(1.549999999999997:4.469999999999999 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(2.629999999999996:3.509999999999998 _clp_cinfo) _clpAdjustPt(2.879999999999996:3.759999999999998 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(2.97999999999999:4.160000000000004 _clp_cinfo) _clpAdjustPt(2.97999999999999:4.259999999999998 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(1.809999999999988:4.160000000000004 _clp_cinfo) _clpAdjustPt(1.809999999999988:4.469999999999999 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(2.629999999999996:3.509999999999998 _clp_cinfo) _clpAdjustPt(2.530000000000001:3.509999999999998 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(1.009999999999991:4.469999999999999 _clp_cinfo) _clpAdjustPt(1.009999999999991:4.160000000000004 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(2.179999999999993:4.160000000000004 _clp_cinfo) _clpAdjustPt(2.879999999999996:4.160000000000004 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(2.179999999999993:3.798700000000004 _clp_cinfo) _clpAdjustPt(2.179999999999993:4.160000000000004 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(2.879999999999996:3.759999999999998 _clp_cinfo) _clpAdjustPt(2.879999999999996:4.160000000000004 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(0.75:4.160000000000004 _clp_cinfo) _clpAdjustPt(0.75:4.469999999999999 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(2.97999999999999:4.259999999999998 _clp_cinfo) _clpAdjustPt(5.72999999999999:4.259999999999998 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(1.830500000000001:1.969999999999999 _clp_cinfo) _clpAdjustPt(1.845799999999997:1.969999999999999 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(1.845799999999997:1.770000000000003 _clp_cinfo) _clpAdjustPt(1.830500000000001:1.770000000000003 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(1.879999999999996:1.770000000000003 _clp_cinfo) _clpAdjustPt(1.879999999999996:1.969999999999999 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(1.864199999999997:1.969999999999999 _clp_cinfo) _clpAdjustPt(1.879999999999996:1.969999999999999 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(1.879999999999996:1.770000000000003 _clp_cinfo) _clpAdjustPt(1.864199999999997:1.770000000000003 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(3.429999999999993:1.810000000000002 _clp_cinfo) _clpAdjustPt(3.429999999999993:3.259999999999998 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(3.954999999999998:1.560000000000002 _clp_cinfo) _clpAdjustPt(3.679999999999993:1.560000000000002 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

printf(" 70 percent completed")
newline()

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(1.845799999999997:1.969999999999999 _clp_cinfo) _clpAdjustPt(1.864199999999997:1.969999999999999 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(1.094999999999999:1.886200000000002 _clp_cinfo) _clpAdjustPt(1.094999999999999:1.905100000000005 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(1.030499999999989:1.969999999999999 _clp_cinfo) _clpAdjustPt(0.7294999999999874:1.969999999999999 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(0.6957999999999913:1.969999999999999 _clp_cinfo) _clpAdjustPt(0.7141999999999911:1.969999999999999 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(1.894999999999996:1.798000000000002 _clp_cinfo) _clpAdjustPt(2.317999999999998:1.798000000000002 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(1.0642:1.969999999999999 _clp_cinfo) _clpAdjustPt(1.079999999999998:1.969999999999999 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(1.879999999999996:1.770000000000003 _clp_cinfo) _clpAdjustPt(1.879999999999996:1.719999999999999 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(1.030499999999989:1.969999999999999 _clp_cinfo) _clpAdjustPt(1.0458:1.969999999999999 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(0.6299999999999955:1.671100000000003 _clp_cinfo) _clpAdjustPt(0.6299999999999955:1.520000000000003 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(1.464999999999989:1.886200000000002 _clp_cinfo) _clpAdjustPt(1.094999999999999:1.886200000000002 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(2.206199999999996:1.886200000000002 _clp_cinfo) _clpAdjustPt(1.894999999999996:1.886200000000002 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(1.830500000000001:1.969999999999999 _clp_cinfo) _clpAdjustPt(1.529499999999999:1.969999999999999 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(0.664999999999992:1.730000000000004 _clp_cinfo) _clpAdjustPt(0.6049999999999898:1.730000000000004 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(1.079999999999998:1.719999999999999 _clp_cinfo) _clpAdjustPt(1.079999999999998:1.671100000000003 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(1.429999999999993:1.671100000000003 _clp_cinfo) _clpAdjustPt(1.5:1.671100000000003 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(2.225099999999998:1.905100000000005 _clp_cinfo) _clpAdjustPt(1.894999999999996:1.905100000000005 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(1.954999999999998:1.509999999999998 _clp_cinfo) _clpAdjustPt(1.954999999999998:1.730000000000004 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(1.894999999999996:1.886200000000002 _clp_cinfo) _clpAdjustPt(1.894999999999996:1.905100000000005 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(0.6957999999999913:1.770000000000003 _clp_cinfo) _clpAdjustPt(0.6799999999999926:1.770000000000003 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(1.0458:1.770000000000003 _clp_cinfo) _clpAdjustPt(1.030499999999989:1.770000000000003 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(1.079999999999998:1.770000000000003 _clp_cinfo) _clpAdjustPt(1.079999999999998:1.719999999999999 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(1.464999999999989:1.730000000000004 _clp_cinfo) _clpAdjustPt(1.405000000000001:1.730000000000004 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(1.059999999999988:1.671100000000003 _clp_cinfo) _clpAdjustPt(0.6999999999999886:1.671100000000003 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(1.879999999999996:1.719999999999999 _clp_cinfo) _clpAdjustPt(1.879999999999996:1.671100000000003 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(1.0458:1.969999999999999 _clp_cinfo) _clpAdjustPt(1.0642:1.969999999999999 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(0.6799999999999926:1.671100000000003 _clp_cinfo) _clpAdjustPt(0.6799999999999926:1.719999999999999 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(1.155000000000001:1.509999999999998 _clp_cinfo) _clpAdjustPt(1.155000000000001:1.730000000000004 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(0.664999999999992:1.905100000000005 _clp_cinfo) _clpAdjustPt(0.664999999999992:1.886200000000002 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(1.47999999999999:1.969999999999999 _clp_cinfo) _clpAdjustPt(1.47999999999999:1.770000000000003 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(1.464999999999989:1.905100000000005 _clp_cinfo) _clpAdjustPt(1.464999999999989:1.886200000000002 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(1.894999999999996:1.798000000000002 _clp_cinfo) _clpAdjustPt(1.894999999999996:1.886200000000002 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(1.405000000000001:1.730000000000004 _clp_cinfo) _clpAdjustPt(1.405000000000001:1.509999999999998 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(2.317999999999998:1.798000000000002 _clp_cinfo) _clpAdjustPt(2.346799999999988:1.826799999999999 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(0.664999999999992:1.886200000000002 _clp_cinfo) _clpAdjustPt(0.664999999999992:1.798000000000002 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(0.664999999999992:1.798000000000002 _clp_cinfo) _clpAdjustPt(0.664999999999992:1.730000000000004 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(1.47999999999999:1.719999999999999 _clp_cinfo) _clpAdjustPt(1.47999999999999:1.770000000000003 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(1.530000000000001:1.713000000000001 _clp_cinfo) _clpAdjustPt(1.530000000000001:1.969700000000003 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(0.6299999999999955:1.671100000000003 _clp_cinfo) _clpAdjustPt(0.6999999999999886:1.671100000000003 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(1.094999999999999:1.798000000000002 _clp_cinfo) _clpAdjustPt(1.094999999999999:1.886200000000002 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(1.859999999999999:1.671100000000003 _clp_cinfo) _clpAdjustPt(1.929999999999993:1.671100000000003 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(1.464999999999989:1.905100000000005 _clp_cinfo) _clpAdjustPt(1.094999999999999:1.905100000000005 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(0.7299999999999898:1.713000000000001 _clp_cinfo) _clpAdjustPt(0.7299999999999898:1.969700000000003 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(0.6799999999999926:1.969999999999999 _clp_cinfo) _clpAdjustPt(0.6957999999999913:1.969999999999999 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(1.129999999999996:1.520000000000003 _clp_cinfo) _clpAdjustPt(1.129999999999996:1.671100000000003 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(1.829999999999998:1.713000000000001 _clp_cinfo) _clpAdjustPt(1.829999999999998:1.671100000000003 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(1.405000000000001:1.509999999999998 _clp_cinfo) _clpAdjustPt(1.954999999999998:1.509999999999998 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(1.155000000000001:1.509999999999998 _clp_cinfo) _clpAdjustPt(0.6049999999999898:1.509999999999998 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(1.094999999999999:1.798000000000002 _clp_cinfo) _clpAdjustPt(1.464999999999989:1.798000000000002 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(1.929999999999993:1.520000000000003 _clp_cinfo) _clpAdjustPt(1.929999999999993:1.671100000000003 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(1.929999999999993:1.520000000000003 _clp_cinfo) _clpAdjustPt(1.859999999999999:1.520000000000003 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(0.6799999999999926:1.719999999999999 _clp_cinfo) _clpAdjustPt(0.6799999999999926:1.770000000000003 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(1.155000000000001:1.730000000000004 _clp_cinfo) _clpAdjustPt(1.094999999999999:1.730000000000004 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(1.0642:1.770000000000003 _clp_cinfo) _clpAdjustPt(1.0458:1.770000000000003 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(1.514199999999988:1.770000000000003 _clp_cinfo) _clpAdjustPt(1.495799999999989:1.770000000000003 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(1.530000000000001:1.671100000000003 _clp_cinfo) _clpAdjustPt(1.530000000000001:1.713000000000001 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(1.429999999999993:1.671100000000003 _clp_cinfo) _clpAdjustPt(1.429999999999993:1.520000000000003 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(0.7141999999999911:1.770000000000003 _clp_cinfo) _clpAdjustPt(0.6957999999999913:1.770000000000003 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(0.6799999999999926:1.969999999999999 _clp_cinfo) _clpAdjustPt(0.6799999999999926:1.770000000000003 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(1.47999999999999:1.671100000000003 _clp_cinfo) _clpAdjustPt(1.47999999999999:1.719999999999999 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(1.894999999999996:1.730000000000004 _clp_cinfo) _clpAdjustPt(1.894999999999996:1.798000000000002 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(0.7299999999999898:1.671100000000003 _clp_cinfo) _clpAdjustPt(0.7299999999999898:1.713000000000001 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(1.059999999999988:1.671100000000003 _clp_cinfo) _clpAdjustPt(1.129999999999996:1.671100000000003 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(1.464999999999989:1.886200000000002 _clp_cinfo) _clpAdjustPt(1.464999999999989:1.798000000000002 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(1.529499999999999:1.770000000000003 _clp_cinfo) _clpAdjustPt(1.514199999999988:1.770000000000003 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

printf(" 80 percent completed")
newline()

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(1.464999999999989:1.798000000000002 _clp_cinfo) _clpAdjustPt(1.464999999999989:1.730000000000004 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(1.079999999999998:1.770000000000003 _clp_cinfo) _clpAdjustPt(1.0642:1.770000000000003 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(1.5:1.671100000000003 _clp_cinfo) _clpAdjustPt(1.859999999999999:1.671100000000003 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(0.7294999999999874:1.770000000000003 _clp_cinfo) _clpAdjustPt(0.7141999999999911:1.770000000000003 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(1.864199999999997:1.770000000000003 _clp_cinfo) _clpAdjustPt(1.845799999999997:1.770000000000003 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(1.514199999999988:1.969999999999999 _clp_cinfo) _clpAdjustPt(1.529499999999999:1.969999999999999 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(1.129999999999996:1.520000000000003 _clp_cinfo) _clpAdjustPt(1.059999999999988:1.520000000000003 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(1.030000000000001:1.713000000000001 _clp_cinfo) _clpAdjustPt(1.030000000000001:1.671100000000003 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(1.094999999999999:1.730000000000004 _clp_cinfo) _clpAdjustPt(1.094999999999999:1.798000000000002 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(1.059999999999988:1.520000000000003 _clp_cinfo) _clpAdjustPt(0.6999999999999886:1.520000000000003 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(0.6049999999999898:1.730000000000004 _clp_cinfo) _clpAdjustPt(0.6049999999999898:1.509999999999998 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(1.495799999999989:1.969999999999999 _clp_cinfo) _clpAdjustPt(1.514199999999988:1.969999999999999 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(1.079999999999998:1.770000000000003 _clp_cinfo) _clpAdjustPt(1.079999999999998:1.969999999999999 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(1.5:1.520000000000003 _clp_cinfo) _clpAdjustPt(1.859999999999999:1.520000000000003 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(1.954999999999998:1.730000000000004 _clp_cinfo) _clpAdjustPt(1.894999999999996:1.730000000000004 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(1.829999999999998:1.969700000000003 _clp_cinfo) _clpAdjustPt(1.829999999999998:1.713000000000001 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(1.495799999999989:1.770000000000003 _clp_cinfo) _clpAdjustPt(1.47999999999999:1.770000000000003 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(1.47999999999999:1.969999999999999 _clp_cinfo) _clpAdjustPt(1.495799999999989:1.969999999999999 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(0.7141999999999911:1.969999999999999 _clp_cinfo) _clpAdjustPt(0.7294999999999874:1.969999999999999 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(1.030000000000001:1.969700000000003 _clp_cinfo) _clpAdjustPt(1.030000000000001:1.713000000000001 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(1.5:1.520000000000003 _clp_cinfo) _clpAdjustPt(1.429999999999993:1.520000000000003 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(0.6999999999999886:1.520000000000003 _clp_cinfo) _clpAdjustPt(0.6299999999999955:1.520000000000003 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_path = _clpPathStart(list(_clpAdjustPt(3.429999999999993:3.259999999999998 _clp_cinfo))                  
	_clpMKSConvert(0.000000 _clp_cinfo->t_from_units                  			_clp_cinfo->t_to_units))
_clp_path = _clpPathArcCenter(_clp_path _clpMKSConvert( 0.000000                   _clp_cinfo->t_from_units 
	_clp_cinfo->t_to_units)                   _clpAdjustPt(3.179999999999993:3.509999999999998 _clp_cinfo) nil
 	_clpAdjustPt(3.179991452522344:3.25999145252235 _clp_cinfo))
_clp_dbid = _clpDBCreatePath(_clp_path "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = caar(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_path = _clpPathStart(list(_clpAdjustPt(3.429999999999993:1.810000000000002 _clp_cinfo))                  
	_clpMKSConvert(0.000000 _clp_cinfo->t_from_units                  			_clp_cinfo->t_to_units))
_clp_path = _clpPathArcCenter(_clp_path _clpMKSConvert( 0.000000                   _clp_cinfo->t_from_units 
	_clp_cinfo->t_to_units)                   _clpAdjustPt(3.679999999999993:1.560000000000002 _clp_cinfo) nil
 	_clpAdjustPt(3.679991452750585:1.809991452750595 _clp_cinfo))
_clp_dbid = _clpDBCreatePath(_clp_path "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = caar(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-2.370000000000005:3.509999999999998 _clp_cinfo) _clpAdjustPt(2.530000000000001:3.509999999999998 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-2.720000000000006:4.160000000000004 _clp_cinfo) _clpAdjustPt(-2.820000000000007:4.160000000000004 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-2.820000000000007:4.259999999999998 _clp_cinfo) _clpAdjustPt(-2.820000000000007:4.160000000000004 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-2.720000000000006:4.160000000000004 _clp_cinfo) _clpAdjustPt(-2.020000000000003:4.160000000000004 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-2.470000000000006:3.509999999999998 _clp_cinfo) _clpAdjustPt(-2.720000000000006:3.759999999999998 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-2.370000000000005:3.509999999999998 _clp_cinfo) _clpAdjustPt(-2.470000000000006:3.509999999999998 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-2.720000000000006:3.759999999999998 _clp_cinfo) _clpAdjustPt(-2.720000000000006:4.160000000000004 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-2.370000000000005:3.509999999999998 _clp_cinfo) _clpAdjustPt(-2.020000000000003:3.798700000000004 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-2.158000000000008:1.798000000000002 _clp_cinfo) _clpAdjustPt(-2.186800000000005:1.826799999999999 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-1.735000000000007:1.886200000000002 _clp_cinfo) _clpAdjustPt(-2.046200000000006:1.886200000000002 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-1.735000000000007:1.905100000000005 _clp_cinfo) _clpAdjustPt(-2.065100000000008:1.905100000000005 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-2.158000000000008:1.798000000000002 _clp_cinfo) _clpAdjustPt(-1.735000000000007:1.798000000000002 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(4.204999999999998:-0.740000000000002 _clp_cinfo) _clpAdjustPt(4.204999999999998:1.310000000000002 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(5.219999999999999:-0.8699999999999974 _clp_cinfo) _clpAdjustPt(5.219999999999999:-0.9694999999999965 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(5.469999999999999:-0.1400000000000006 _clp_cinfo) _clpAdjustPt(5.219999999999999:-0.1400000000000006 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(4.949999999999989:-0.990000000000002 _clp_cinfo) _clpAdjustPt(5.219999999999999:-0.990000000000002 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(5.219999999999999:-0.8699999999999974 _clp_cinfo) _clpAdjustPt(5.219999999999999:3.390000000000001 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(5.72999999999999:-0.240000000000002 _clp_cinfo) _clpAdjustPt(5.72999999999999:-1.740000000000002 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(4.949999999999989:-0.990000000000002 _clp_cinfo) _clpAdjustPt(4.949999999999989:3.509999999999998 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(6.069999999999993:-0.1400000000000006 _clp_cinfo) _clpAdjustPt(6.069999999999993:0.8599999999999994 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(5.335499999999996:-1.105499999999999 _clp_cinfo) _clpAdjustPt(4.834499999999991:-1.105499999999999 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(5.469999999999999:-0.1400000000000006 _clp_cinfo) _clpAdjustPt(6.069999999999993:-0.1400000000000006 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(4.969999999999999:-0.9699999999999989 _clp_cinfo) _clpAdjustPt(4.969999999999999:-0.8699999999999974 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(4.969999999999999:3.390000000000001 _clp_cinfo) _clpAdjustPt(4.969999999999999:-0.8699999999999974 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(4.969999999999999:-0.5899999999999963 _clp_cinfo) _clpAdjustPt(4.949999999999989:-0.5899999999999963 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(4.834499999999991:-1.105499999999999 _clp_cinfo) _clpAdjustPt(4.834499999999991:3.625500000000002 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(5.219999999999999:-0.240000000000002 _clp_cinfo) _clpAdjustPt(5.335499999999996:-0.240000000000002 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(5.219999999999999:-0.990000000000002 _clp_cinfo) _clpAdjustPt(5.335499999999996:-1.105499999999999 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(5.219999999999999:-0.9699999999999989 _clp_cinfo) _clpAdjustPt(4.969999999999999:-0.9699999999999989 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(5.335499999999996:-0.240000000000002 _clp_cinfo) _clpAdjustPt(5.72999999999999:-0.240000000000002 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(5.335499999999996:-1.105499999999999 _clp_cinfo) _clpAdjustPt(5.335499999999996:-0.240000000000002 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(4.949999999999989:-0.990000000000002 _clp_cinfo) _clpAdjustPt(4.834499999999991:-1.105499999999999 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(4.969999999999999:-0.5300000000000011 _clp_cinfo) _clpAdjustPt(4.949999999999989:-0.5300000000000011 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(5.219999999999999:-0.990000000000002 _clp_cinfo) _clpAdjustPt(5.219999999999999:-0.9694999999999965 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_path = _clpPathStart(list(_clpAdjustPt(6.069999999999993:1.660000000000004 _clp_cinfo))                  
	_clpMKSConvert(0.000000 _clp_cinfo->t_from_units                  			_clp_cinfo->t_to_units))
_clp_path = _clpPathArcCenter(_clp_path _clpMKSConvert( 0.000000                   _clp_cinfo->t_from_units 
	_clp_cinfo->t_to_units)                   _clpAdjustPt(6.069999999999993:0.8599999999999994 _clp_cinfo) nil
 	_clpAdjustPt(6.069994064672471:1.259999999999998 _clp_cinfo))
_clp_dbid = _clpDBCreatePath(_clp_path "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = caar(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(5.219999999999999:3.4895 _clp_cinfo) _clpAdjustPt(5.219999999999999:3.509999999999998 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(4.969999999999999:3.390000000000001 _clp_cinfo) _clpAdjustPt(4.969999999999999:3.490000000000002 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(5.335499999999996:3.625500000000002 _clp_cinfo) _clpAdjustPt(5.219999999999999:3.509999999999998 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(5.219999999999999:3.4895 _clp_cinfo) _clpAdjustPt(5.219999999999999:3.390000000000001 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

printf(" 90 percent completed")
newline()

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(4.969999999999999:3.490000000000002 _clp_cinfo) _clpAdjustPt(5.219999999999999:3.490000000000002 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(4.834499999999991:3.625500000000002 _clp_cinfo) _clpAdjustPt(5.335499999999996:3.625500000000002 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(4.949999999999989:3.509999999999998 _clp_cinfo) _clpAdjustPt(5.219999999999999:3.509999999999998 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(4.949999999999989:3.509999999999998 _clp_cinfo) _clpAdjustPt(4.834499999999991:3.625500000000002 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(4.949999999999989:3.050000000000004 _clp_cinfo) _clpAdjustPt(4.969999999999999:3.050000000000004 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(5.469999999999999:2.660000000000004 _clp_cinfo) _clpAdjustPt(6.069999999999993:2.660000000000004 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(5.72999999999999:2.759999999999998 _clp_cinfo) _clpAdjustPt(5.335499999999996:2.759999999999998 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(5.219999999999999:2.660000000000004 _clp_cinfo) _clpAdjustPt(5.469999999999999:2.660000000000004 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(5.72999999999999:4.259999999999998 _clp_cinfo) _clpAdjustPt(5.72999999999999:2.759999999999998 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(4.949999999999989:3.109999999999999 _clp_cinfo) _clpAdjustPt(4.969999999999999:3.109999999999999 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(6.069999999999993:2.660000000000004 _clp_cinfo) _clpAdjustPt(6.069999999999993:1.660000000000004 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(5.335499999999996:2.759999999999998 _clp_cinfo) _clpAdjustPt(5.219999999999999:2.759999999999998 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(5.335499999999996:2.759999999999998 _clp_cinfo) _clpAdjustPt(5.335499999999996:3.625500000000002 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-4.045000000000009:-0.740000000000002 _clp_cinfo) _clpAdjustPt(-4.045000000000009:1.310000000000002 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-2.470000000000006:-0.990000000000002 _clp_cinfo) _clpAdjustPt(-3.795000000000009:-0.990000000000002 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-4.790000000000006:-0.5300000000000011 _clp_cinfo) _clpAdjustPt(-4.820000000000007:-0.5300000000000011 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-5.570000000000007:-0.240000000000002 _clp_cinfo) _clpAdjustPt(-5.175500000000007:-0.240000000000002 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-4.790000000000006:3.509999999999998 _clp_cinfo) _clpAdjustPt(-4.790000000000006:-0.990000000000002 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-4.820000000000007:-0.5899999999999963 _clp_cinfo) _clpAdjustPt(-4.790000000000006:-0.5899999999999963 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-5.570000000000007:-1.740000000000002 _clp_cinfo) _clpAdjustPt(-5.570000000000007:-0.240000000000002 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-5.060000000000002:-0.9694999999999965 _clp_cinfo) _clpAdjustPt(-5.060000000000002:-0.990000000000002 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-5.070000000000007:-0.1400000000000006 _clp_cinfo) _clpAdjustPt(-5.320000000000007:-0.1400000000000006 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-5.920000000000009:-0.1400000000000006 _clp_cinfo) _clpAdjustPt(-5.920000000000009:0.8599999999999994 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-5.175500000000007:-0.240000000000002 _clp_cinfo) _clpAdjustPt(-5.070000000000007:-0.240000000000002 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-4.820000000000007:-0.9699999999999989 _clp_cinfo) _clpAdjustPt(-5.060000000000002:-0.9699999999999989 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-4.674500000000009:-1.105499999999999 _clp_cinfo) _clpAdjustPt(-4.790000000000006:-0.990000000000002 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-5.060000000000002:-0.990000000000002 _clp_cinfo) _clpAdjustPt(-4.790000000000006:-0.990000000000002 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-5.070000000000007:3.390000000000001 _clp_cinfo) _clpAdjustPt(-5.070000000000007:-0.8699999999999974 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-5.320000000000007:-0.1400000000000006 _clp_cinfo) _clpAdjustPt(-5.920000000000009:-0.1400000000000006 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-4.674500000000009:-1.105499999999999 _clp_cinfo) _clpAdjustPt(-4.674500000000009:3.625500000000002 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-5.070000000000007:-0.9662000000000006 _clp_cinfo) _clpAdjustPt(-5.070000000000007:-0.8699999999999974 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-2.820000000000007:-1.740000000000002 _clp_cinfo) _clpAdjustPt(-5.570000000000007:-1.740000000000002 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-5.175500000000007:-0.240000000000002 _clp_cinfo) _clpAdjustPt(-5.175500000000007:-1.105499999999999 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-5.060000000000002:-0.990000000000002 _clp_cinfo) _clpAdjustPt(-5.175500000000007:-1.105499999999999 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-4.820000000000007:-0.8699999999999974 _clp_cinfo) _clpAdjustPt(-4.820000000000007:-0.9699999999999989 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-5.175500000000007:-1.105499999999999 _clp_cinfo) _clpAdjustPt(-4.674500000000009:-1.105499999999999 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-4.820000000000007:-0.8699999999999974 _clp_cinfo) _clpAdjustPt(-4.820000000000007:3.390000000000001 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_path = _clpPathStart(list(_clpAdjustPt(-4.045000000000009:-0.740000000000002 _clp_cinfo))                  
	_clpMKSConvert(0.000000 _clp_cinfo->t_from_units                  			_clp_cinfo->t_to_units))
_clp_path = _clpPathArcCenter(_clp_path _clpMKSConvert( 0.000000                   _clp_cinfo->t_from_units 
	_clp_cinfo->t_to_units)                   _clpAdjustPt(-3.795000000000009:-0.990000000000002 _clp_cinfo) nil
 	_clpAdjustPt(-3.795008547249651:-0.7400085472496514 _clp_cinfo))
_clp_dbid = _clpDBCreatePath(_clp_path "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = caar(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_path = _clpPathStart(list(_clpAdjustPt(-5.920000000000009:0.8599999999999994 _clp_cinfo))                  
	_clpMKSConvert(0.000000 _clp_cinfo->t_from_units                  			_clp_cinfo->t_to_units))
_clp_path = _clpPathArcCenter(_clp_path _clpMKSConvert( 0.000000                   _clp_cinfo->t_from_units 
	_clp_cinfo->t_to_units)                   _clpAdjustPt(-5.920000000000009:1.660000000000004 _clp_cinfo) nil
 	_clpAdjustPt(-5.920005935327531:1.259999999999998 _clp_cinfo))
_clp_dbid = _clpDBCreatePath(_clp_path "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = caar(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-3.020000000000003:3.509999999999998 _clp_cinfo) _clpAdjustPt(-2.470000000000006:3.509999999999998 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-4.674500000000009:3.625500000000002 _clp_cinfo) _clpAdjustPt(-4.790000000000006:3.509999999999998 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-5.175500000000007:3.625500000000002 _clp_cinfo) _clpAdjustPt(-5.060000000000002:3.509999999999998 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-5.060000000000002:3.509999999999998 _clp_cinfo) _clpAdjustPt(-5.060000000000002:3.4895 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-4.674500000000009:3.625500000000002 _clp_cinfo) _clpAdjustPt(-5.175500000000007:3.625500000000002 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-5.060000000000002:3.509999999999998 _clp_cinfo) _clpAdjustPt(-4.790000000000006:3.509999999999998 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-5.060000000000002:3.490000000000002 _clp_cinfo) _clpAdjustPt(-4.820000000000007:3.490000000000002 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-5.570000000000007:4.259999999999998 _clp_cinfo) _clpAdjustPt(-2.820000000000007:4.259999999999998 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-4.820000000000007:3.490000000000002 _clp_cinfo) _clpAdjustPt(-4.820000000000007:3.390000000000001 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-5.070000000000007:3.390000000000001 _clp_cinfo) _clpAdjustPt(-5.070000000000007:3.486200000000004 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-3.795000000000009:1.560000000000002 _clp_cinfo) _clpAdjustPt(-3.520000000000003:1.560000000000002 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-3.270000000000003:1.810000000000002 _clp_cinfo) _clpAdjustPt(-3.270000000000003:3.259999999999998 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-5.175500000000007:2.759999999999998 _clp_cinfo) _clpAdjustPt(-5.570000000000007:2.759999999999998 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-5.920000000000009:2.660000000000004 _clp_cinfo) _clpAdjustPt(-5.920000000000009:1.660000000000004 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-5.320000000000007:2.660000000000004 _clp_cinfo) _clpAdjustPt(-5.920000000000009:2.660000000000004 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-5.070000000000007:2.759999999999998 _clp_cinfo) _clpAdjustPt(-5.175500000000007:2.759999999999998 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-5.175500000000007:3.625500000000002 _clp_cinfo) _clpAdjustPt(-5.175500000000007:2.759999999999998 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-4.820000000000007:3.050000000000004 _clp_cinfo) _clpAdjustPt(-4.790000000000006:3.050000000000004 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-4.790000000000006:3.109999999999999 _clp_cinfo) _clpAdjustPt(-4.820000000000007:3.109999999999999 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-5.320000000000007:2.660000000000004 _clp_cinfo) _clpAdjustPt(-5.070000000000007:2.660000000000004 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-5.570000000000007:2.759999999999998 _clp_cinfo) _clpAdjustPt(-5.570000000000007:4.259999999999998 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_path = _clpPathStart(list(_clpAdjustPt(-3.795000000000009:1.560000000000002 _clp_cinfo))                  
	_clpMKSConvert(0.000000 _clp_cinfo->t_from_units                  			_clp_cinfo->t_to_units))
_clp_path = _clpPathArcCenter(_clp_path _clpMKSConvert( 0.000000                   _clp_cinfo->t_from_units 
	_clp_cinfo->t_to_units)                   _clpAdjustPt(-4.045000000000009:1.310000000000002 _clp_cinfo) nil
 	_clpAdjustPt(-3.794996298575967:1.309996298575953 _clp_cinfo))
_clp_dbid = _clpDBCreatePath(_clp_path "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = caar(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_path = _clpPathStart(list(_clpAdjustPt(-3.020000000000003:3.509999999999998 _clp_cinfo))                  
	_clpMKSConvert(0.000000 _clp_cinfo->t_from_units                  			_clp_cinfo->t_to_units))
_clp_path = _clpPathArcCenter(_clp_path _clpMKSConvert( 0.000000                   _clp_cinfo->t_from_units 
	_clp_cinfo->t_to_units)                   _clpAdjustPt(-3.270000000000003:3.259999999999998 _clp_cinfo) nil
 	_clpAdjustPt(-3.019996298575613:3.259996298575608 _clp_cinfo))
_clp_dbid = _clpDBCreatePath(_clp_path "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = caar(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_path = _clpPathStart(list(_clpAdjustPt(-3.520000000000003:1.560000000000002 _clp_cinfo))                  
	_clpMKSConvert(0.000000 _clp_cinfo->t_from_units                  			_clp_cinfo->t_to_units))
_clp_path = _clpPathArcCenter(_clp_path _clpMKSConvert( 0.000000                   _clp_cinfo->t_from_units 
	_clp_cinfo->t_to_units)                   _clpAdjustPt(-3.270000000000003:1.810000000000002 _clp_cinfo) nil
 	_clpAdjustPt(-3.519996299041395:1.809996299041394 _clp_cinfo))
_clp_dbid = _clpDBCreatePath(_clp_path "BOARD GEOMETRY/DXFBOTTOM" 'line _clp_sym)

_clp_dbid = caar(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

printf(" 100 percent completed")
newline()

axlFlushDisplay()
