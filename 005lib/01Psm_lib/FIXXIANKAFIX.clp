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
(putprop _clp_cinfo (list (_clpAdjustPt 44.604:-0.5415 _clp_cinfo)	
	(_clpAdjustPt 49.8871:4.7417 _clp_cinfo)) 'l_extents)
(putprop _clp_cinfo (_clpAdjustPt '(-48.25 -168.65) _clp_cinfo) 'l_zeropt)
(unless (_clpSelectRotOrg _clp_cinfo)
	(error "CANCEL"))
_clp_clip_prop_value = _clpGetClipPropValue()

_clp_path = _clpPathStart(list(_clpAdjustPt(49.7855:2.100099999999998 _clp_cinfo))                  
	_clpMKSConvert(0.203200 _clp_cinfo->t_from_units                  			_clp_cinfo->t_to_units))
_clp_path = _clpPathArcCenter(_clp_path _clpMKSConvert( 0.203200                   _clp_cinfo->t_from_units 
	_clp_cinfo->t_to_units)                   _clpAdjustPt(49.7855:2.100099999999998 _clp_cinfo) nil
 	_clpAdjustPt(47.24554000000001:2.100099999999998 _clp_cinfo))
_clp_dbid = _clpDBCreatePath(_clp_path "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = caar(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

printf(" 10 percent completed")
newline()

printf(" 100 percent completed")
newline()

axlFlushDisplay()
