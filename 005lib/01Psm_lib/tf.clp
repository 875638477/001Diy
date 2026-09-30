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
_clp_cinfo->snapToObject = nil
_clp_cinfo->createNCLayers = nil
_clp_group_info = make_clp_group_info()
_clp_cinfo->group_info = _clp_group_info
_clp_accuracy =4
_clpCheckAccuracy(_clp_accuracy _clp_cinfo->t_from_units	 	_clp_cinfo->t_to_units)
(putprop _clp_cinfo (list (_clpAdjustPt -5.755:-3.125 _clp_cinfo)	
	(_clpAdjustPt 5.7634:12.125 _clp_cinfo)) 'l_extents)
(putprop _clp_cinfo (_clpAdjustPt '(0.0 0.0) _clp_cinfo) 'l_zeropt)
(unless (_clpSelectRotOrg _clp_cinfo)
	(error "CANCEL"))
_clp_clip_prop_value = _clpGetClipPropValue()

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(5.625:2.125 _clp_cinfo) _clpAdjustPt(5.625:2.3 _clp_cinfo) ) _clpMKSConvert(0.250000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(4.1:2.125 _clp_cinfo) _clpAdjustPt(5.625:2.125 _clp_cinfo) ) _clpMKSConvert(0.250000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(5.575:2.3 _clp_cinfo) _clpAdjustPt(5.575:12 _clp_cinfo) ) _clpMKSConvert(0.250000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

printf(" 10 percent completed")
newline()

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(5.625:-2.125 _clp_cinfo) _clpAdjustPt(5.625:-3 _clp_cinfo) ) _clpMKSConvert(0.250000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(5.625:-3 _clp_cinfo) _clpAdjustPt(5.625:-3 _clp_cinfo) ) _clpMKSConvert(0.250000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(5.0084:-2.5246 _clp_cinfo) _clpAdjustPt(5.0084:-2.9746 _clp_cinfo) ) _clpMKSConvert(0.250000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

printf(" 20 percent completed")
newline()

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(5.0084:-2.5246 _clp_cinfo) _clpAdjustPt(5.6384:-2.5246 _clp_cinfo) ) _clpMKSConvert(0.250000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_path = _clpPathStart(list(_clpAdjustPt(1:0 _clp_cinfo))                  
	_clpMKSConvert(0.200000 _clp_cinfo->t_from_units                  			_clp_cinfo->t_to_units))
_clp_path = _clpPathArcCenter(_clp_path _clpMKSConvert( 0.200000                   _clp_cinfo->t_from_units 
	_clp_cinfo->t_to_units)                   _clpAdjustPt(1:0 _clp_cinfo) nil
 	_clpAdjustPt(0:0 _clp_cinfo))
_clp_dbid = _clpDBCreatePath(_clp_path "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = caar(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(0:-0.5 _clp_cinfo) _clpAdjustPt(0:0 _clp_cinfo) ) _clpMKSConvert(0.200000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

printf(" 30 percent completed")
newline()

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-0.5:0 _clp_cinfo) _clpAdjustPt(0:0 _clp_cinfo) ) _clpMKSConvert(0.200000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(0:0.5 _clp_cinfo) _clpAdjustPt(0:0 _clp_cinfo) ) _clpMKSConvert(0.200000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(0.5:0 _clp_cinfo) _clpAdjustPt(0:0 _clp_cinfo) ) _clpMKSConvert(0.200000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

printf(" 40 percent completed")
newline()

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(5.575:12 _clp_cinfo) _clpAdjustPt(-5.575:12 _clp_cinfo) ) _clpMKSConvert(0.250000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-4.875:4.98 _clp_cinfo) _clpAdjustPt(-5.575:6.9 _clp_cinfo) ) _clpMKSConvert(0.250000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-5.575:4.98 _clp_cinfo) _clpAdjustPt(-4.875:4.98 _clp_cinfo) ) _clpMKSConvert(0.250000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

printf(" 50 percent completed")
newline()

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-5.575:12 _clp_cinfo) _clpAdjustPt(-5.575:6.9 _clp_cinfo) ) _clpMKSConvert(0.250000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-4.875:2.3 _clp_cinfo) _clpAdjustPt(-4.875:3.03 _clp_cinfo) ) _clpMKSConvert(0.250000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

printf(" 60 percent completed")
newline()

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(5.625:2.3 _clp_cinfo) _clpAdjustPt(-4.875:2.3 _clp_cinfo) ) _clpMKSConvert(0.250000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-5.625:2.3 _clp_cinfo) _clpAdjustPt(-5.3016:2.3 _clp_cinfo) ) _clpMKSConvert(0.250000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-5.625:0.975 _clp_cinfo) _clpAdjustPt(-5.625:2.3 _clp_cinfo) ) _clpMKSConvert(0.250000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

printf(" 70 percent completed")
newline()

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-5.3016:2.3 _clp_cinfo) _clpAdjustPt(-4.875:2.3 _clp_cinfo) ) _clpMKSConvert(0.250000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-5.575:3.05 _clp_cinfo) _clpAdjustPt(-5.3016:2.3 _clp_cinfo) ) _clpMKSConvert(0.250000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-5.575:3.03 _clp_cinfo) _clpAdjustPt(-5.575:4.98 _clp_cinfo) ) _clpMKSConvert(0.250000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

printf(" 80 percent completed")
newline()

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-4.875:3.03 _clp_cinfo) _clpAdjustPt(-5.575:3.03 _clp_cinfo) ) _clpMKSConvert(0.250000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-5.625:-3 _clp_cinfo) _clpAdjustPt(5.625:-3 _clp_cinfo) ) _clpMKSConvert(0.250000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-5.625:-1.625 _clp_cinfo) _clpAdjustPt(-5.625:-3 _clp_cinfo) ) _clpMKSConvert(0.250000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

printf(" 90 percent completed")
newline()

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-5:-2.55 _clp_cinfo) _clpAdjustPt(-5.63:-2.55 _clp_cinfo) ) _clpMKSConvert(0.250000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-5:-3 _clp_cinfo) _clpAdjustPt(-5:-2.55 _clp_cinfo) ) _clpMKSConvert(0.250000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

printf(" 100 percent completed")
newline()

axlFlushDisplay()
