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
_clp_cinfo->t_from_units = "mils"
_clp_cinfo->t_to_units = car(axlDBGetDesignUnits())
_clp_cinfo->preserve_shape_net = nil
_clp_cinfo->preserve_via_net = nil
_clp_cinfo->snapToObject = nil
_clp_cinfo->createNCLayers = nil
_clp_group_info = make_clp_group_info()
_clp_cinfo->group_info = _clp_group_info
_clp_accuracy =2
_clpCheckAccuracy(_clp_accuracy _clp_cinfo->t_from_units	 	_clp_cinfo->t_to_units)
(putprop _clp_cinfo (list (_clpAdjustPt -2102.65:-8528.25 _clp_cinfo)	
	(_clpAdjustPt 6033.17:205 _clp_cinfo)) 'l_extents)
(putprop _clp_cinfo (_clpAdjustPt '(905.71 6185.0) _clp_cinfo) 'l_zeropt)
(unless (_clpSelectRotOrg _clp_cinfo)
	(error "CANCEL"))
_clp_clip_prop_value = _clpGetClipPropValue()

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(979.29:-4637.5 _clp_cinfo) _clpAdjustPt(979.29:-4652.5 _clp_cinfo) ) _clpMKSConvert(5.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(986.79:-4645 _clp_cinfo) _clpAdjustPt(971.79:-4645 _clp_cinfo) ) _clpMKSConvert(5.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(1099.29:-4645 _clp_cinfo) _clpAdjustPt(1084.29:-4645 _clp_cinfo) ) _clpMKSConvert(5.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(998.8899999999999:-4642.4 _clp_cinfo) _clpAdjustPt(998.8899999999999:-4650.3 _clp_cinfo) ) _clpMKSConvert(5.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(1069.69:-4642.4 _clp_cinfo) _clpAdjustPt(998.8899999999999:-4642.4 _clp_cinfo) ) _clpMKSConvert(5.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(1069.69:-4642.4 _clp_cinfo) _clpAdjustPt(1069.69:-4650.3 _clp_cinfo) ) _clpMKSConvert(5.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(998.8899999999999:-4689.7 _clp_cinfo) _clpAdjustPt(998.8899999999999:-4697.6 _clp_cinfo) ) _clpMKSConvert(5.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(1069.69:-4697.6 _clp_cinfo) _clpAdjustPt(998.8899999999999:-4697.6 _clp_cinfo) ) _clpMKSConvert(5.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(1069.69:-4689.7 _clp_cinfo) _clpAdjustPt(1069.69:-4697.6 _clp_cinfo) ) _clpMKSConvert(5.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(1050.39:-4642.4 _clp_cinfo) _clpAdjustPt(1050.39:-4697.6 _clp_cinfo) ) _clpMKSConvert(5.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(4168.72:-6278.11 _clp_cinfo) _clpAdjustPt(3928.72:-6278.11 _clp_cinfo) ) _clpMKSConvert(7.870000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(4168.72:-6278.11 _clp_cinfo) _clpAdjustPt(4168.72:-6408.11 _clp_cinfo) ) _clpMKSConvert(7.870000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(4773.72:-6408.11 _clp_cinfo) _clpAdjustPt(4168.72:-6408.11 _clp_cinfo) ) _clpMKSConvert(7.870000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(4773.72:-5828.11 _clp_cinfo) _clpAdjustPt(4773.72:-6408.11 _clp_cinfo) ) _clpMKSConvert(7.870000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(4773.72:-5828.11 _clp_cinfo) _clpAdjustPt(4168.72:-5828.11 _clp_cinfo) ) _clpMKSConvert(7.870000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(4168.72:-5828.11 _clp_cinfo) _clpAdjustPt(4168.72:-5958.11 _clp_cinfo) ) _clpMKSConvert(7.870000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(4168.72:-5958.11 _clp_cinfo) _clpAdjustPt(3928.72:-5958.11 _clp_cinfo) ) _clpMKSConvert(7.870000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(368.29:-6062.99 _clp_cinfo) _clpAdjustPt(321.04:-6062.99 _clp_cinfo) ) _clpMKSConvert(6.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(368.29:-6062.99 _clp_cinfo) _clpAdjustPt(328.9200000000001:-6055.12 _clp_cinfo) ) _clpMKSConvert(6.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(328.9200000000001:-6055.12 _clp_cinfo) _clpAdjustPt(328.9200000000001:-6074.8 _clp_cinfo) ) _clpMKSConvert(6.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(368.29:-6062.99 _clp_cinfo) _clpAdjustPt(328.9200000000001:-6074.8 _clp_cinfo) ) _clpMKSConvert(6.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(368.29:-6062.99 _clp_cinfo) _clpAdjustPt(321.04:-6043.31 _clp_cinfo) ) _clpMKSConvert(6.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(321.04:-6043.31 _clp_cinfo) _clpAdjustPt(321.04:-6082.68 _clp_cinfo) ) _clpMKSConvert(6.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(368.29:-6062.99 _clp_cinfo) _clpAdjustPt(321.04:-6082.68 _clp_cinfo) ) _clpMKSConvert(6.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(3928.72:-6278.11 _clp_cinfo) _clpAdjustPt(373.72:-6278.11 _clp_cinfo) ) _clpMKSConvert(7.870000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(3928.72:-5958.11 _clp_cinfo) _clpAdjustPt(3928.72:-6278.11 _clp_cinfo) ) _clpMKSConvert(7.870000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(3928.72:-5958.11 _clp_cinfo) _clpAdjustPt(373.72:-5958.11 _clp_cinfo) ) _clpMKSConvert(7.870000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(373.72:-5958.11 _clp_cinfo) _clpAdjustPt(373.72:-6278.11 _clp_cinfo) ) _clpMKSConvert(7.870000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_path = _clpPathStart(list(_clpAdjustPt(3148.65:-6612.17 _clp_cinfo))                  
	_clpMKSConvert(5.900000 _clp_cinfo->t_from_units                  			_clp_cinfo->t_to_units))
_clp_path = _clpPathArcCenter(_clp_path _clpMKSConvert( 5.900000                   _clp_cinfo->t_from_units 
	_clp_cinfo->t_to_units)                   _clpAdjustPt(3148.65:-6887.67 _clp_cinfo) nil
 	_clpAdjustPt(3144.88:-6749.92 _clp_cinfo))
_clp_dbid = _clpDBCreatePath(_clp_path "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = caar(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(3282.47:-6612 _clp_cinfo) _clpAdjustPt(3144.75:-6612.07 _clp_cinfo) ) _clpMKSConvert(5.900000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(4542.47:-6612 _clp_cinfo) _clpAdjustPt(3282.47:-6612 _clp_cinfo) ) _clpMKSConvert(6.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(3282.47:-6612 _clp_cinfo) _clpAdjustPt(3282.47:-7872 _clp_cinfo) ) _clpMKSConvert(6.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(4542.47:-6612 _clp_cinfo) _clpAdjustPt(4542.47:-7872 _clp_cinfo) ) _clpMKSConvert(6.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(3839.29:-6640 _clp_cinfo) _clpAdjustPt(3839.29:-6660 _clp_cinfo) ) _clpMKSConvert(6.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(3629.29:-138.25 _clp_cinfo) _clpAdjustPt(3629.29:-178.25 _clp_cinfo) ) _clpMKSConvert(5.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(3639.29:-138.25 _clp_cinfo) _clpAdjustPt(3639.29:-178.25 _clp_cinfo) ) _clpMKSConvert(5.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(3629.29:-158.25 _clp_cinfo) _clpAdjustPt(3624.29:-158.25 _clp_cinfo) ) _clpMKSConvert(5.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(3644.29:-158.25 _clp_cinfo) _clpAdjustPt(3639.29:-158.25 _clp_cinfo) ) _clpMKSConvert(5.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(3569.29:-138.25 _clp_cinfo) _clpAdjustPt(3569.29:-178.25 _clp_cinfo) ) _clpMKSConvert(5.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(3584.29:-193.25 _clp_cinfo) _clpAdjustPt(3569.29:-178.25 _clp_cinfo) ) _clpMKSConvert(5.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(3684.29:-193.25 _clp_cinfo) _clpAdjustPt(3584.29:-193.25 _clp_cinfo) ) _clpMKSConvert(5.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(3699.29:-178.25 _clp_cinfo) _clpAdjustPt(3684.29:-193.25 _clp_cinfo) ) _clpMKSConvert(5.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(3699.29:-138.25 _clp_cinfo) _clpAdjustPt(3699.29:-178.25 _clp_cinfo) ) _clpMKSConvert(5.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(3699.29:-138.25 _clp_cinfo) _clpAdjustPt(3684.29:-123.25 _clp_cinfo) ) _clpMKSConvert(5.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(3684.29:-123.25 _clp_cinfo) _clpAdjustPt(3584.29:-123.25 _clp_cinfo) ) _clpMKSConvert(5.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(3584.29:-123.25 _clp_cinfo) _clpAdjustPt(3569.29:-138.25 _clp_cinfo) ) _clpMKSConvert(5.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(5574.47:-6545 _clp_cinfo) _clpAdjustPt(5523.16:-6545 _clp_cinfo) ) _clpMKSConvert(10.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(3352.52:-16.19999999999982 _clp_cinfo) _clpAdjustPt(3312.52:-16.19999999999982 _clp_cinfo) ) _clpMKSConvert(5.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(3352.52:-26.19999999999982 _clp_cinfo) _clpAdjustPt(3312.52:-26.19999999999982 _clp_cinfo) ) _clpMKSConvert(5.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(3332.52:-11.19999999999982 _clp_cinfo) _clpAdjustPt(3332.52:-16.19999999999982 _clp_cinfo) ) _clpMKSConvert(5.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(3332.52:-26.19999999999982 _clp_cinfo) _clpAdjustPt(3332.52:-31.19999999999982 _clp_cinfo) ) _clpMKSConvert(5.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(3352.52:43.80000000000018 _clp_cinfo) _clpAdjustPt(3312.52:43.80000000000018 _clp_cinfo) ) _clpMKSConvert(5.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(3312.52:43.80000000000018 _clp_cinfo) _clpAdjustPt(3297.52:28.80000000000018 _clp_cinfo) ) _clpMKSConvert(5.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(3297.52:28.80000000000018 _clp_cinfo) _clpAdjustPt(3297.52:-71.19999999999982 _clp_cinfo) ) _clpMKSConvert(5.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(3312.52:-86.19999999999982 _clp_cinfo) _clpAdjustPt(3297.52:-71.19999999999982 _clp_cinfo) ) _clpMKSConvert(5.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(3352.52:-86.19999999999982 _clp_cinfo) _clpAdjustPt(3312.52:-86.19999999999982 _clp_cinfo) ) _clpMKSConvert(5.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(3367.52:-71.19999999999982 _clp_cinfo) _clpAdjustPt(3352.52:-86.19999999999982 _clp_cinfo) ) _clpMKSConvert(5.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(3367.52:28.80000000000018 _clp_cinfo) _clpAdjustPt(3367.52:-71.19999999999982 _clp_cinfo) ) _clpMKSConvert(5.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(3367.52:28.80000000000018 _clp_cinfo) _clpAdjustPt(3352.52:43.80000000000018 _clp_cinfo) ) _clpMKSConvert(5.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_path = _clpPathStart(list(_clpAdjustPt(5076.56:-3766 _clp_cinfo))                  
	_clpMKSConvert(10.000000 _clp_cinfo->t_from_units                  			_clp_cinfo->t_to_units))
_clp_path = _clpPathArcCenter(_clp_path _clpMKSConvert( 10.000000                   _clp_cinfo->t_from_units 
	_clp_cinfo->t_to_units)                   _clpAdjustPt(5176.56:-3666 _clp_cinfo) nil
 	_clpAdjustPt(5076.56:-3666 _clp_cinfo))
_clp_dbid = _clpDBCreatePath(_clp_path "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = caar(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_path = _clpPathStart(list(_clpAdjustPt(5176.56:-3494 _clp_cinfo))                  
	_clpMKSConvert(10.000000 _clp_cinfo->t_from_units                  			_clp_cinfo->t_to_units))
_clp_path = _clpPathArcCenter(_clp_path _clpMKSConvert( 10.000000                   _clp_cinfo->t_from_units 
	_clp_cinfo->t_to_units)                   _clpAdjustPt(5076.56:-3394 _clp_cinfo) nil
 	_clpAdjustPt(5076.56:-3494 _clp_cinfo))
_clp_dbid = _clpDBCreatePath(_clp_path "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = caar(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_path = _clpPathStart(list(_clpAdjustPt(4985.56:-3394 _clp_cinfo))                  
	_clpMKSConvert(10.000000 _clp_cinfo->t_from_units                  			_clp_cinfo->t_to_units))
_clp_path = _clpPathArcCenter(_clp_path _clpMKSConvert( 10.000000                   _clp_cinfo->t_from_units 
	_clp_cinfo->t_to_units)                   _clpAdjustPt(4885.56:-3494 _clp_cinfo) nil
 	_clpAdjustPt(4985.56:-3494 _clp_cinfo))
_clp_dbid = _clpDBCreatePath(_clp_path "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = caar(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_path = _clpPathStart(list(_clpAdjustPt(4885.56:-3666 _clp_cinfo))                  
	_clpMKSConvert(10.000000 _clp_cinfo->t_from_units                  			_clp_cinfo->t_to_units))
_clp_path = _clpPathArcCenter(_clp_path _clpMKSConvert( 10.000000                   _clp_cinfo->t_from_units 
	_clp_cinfo->t_to_units)                   _clpAdjustPt(4985.56:-3766 _clp_cinfo) nil
 	_clpAdjustPt(4985.56:-3666 _clp_cinfo))
_clp_dbid = _clpDBCreatePath(_clp_path "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = caar(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(5076.56:-3766 _clp_cinfo) _clpAdjustPt(5015.56:-3766 _clp_cinfo) ) _clpMKSConvert(10.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(5176.56:-3494 _clp_cinfo) _clpAdjustPt(5176.56:-3666 _clp_cinfo) ) _clpMKSConvert(10.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(5076.56:-3394 _clp_cinfo) _clpAdjustPt(5030.56:-3394 _clp_cinfo) ) _clpMKSConvert(10.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(5042.56:-3394 _clp_cinfo) _clpAdjustPt(4985.56:-3394 _clp_cinfo) ) _clpMKSConvert(10.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(4885.56:-3494 _clp_cinfo) _clpAdjustPt(4885.56:-3666 _clp_cinfo) ) _clpMKSConvert(10.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(5034.56:-3766 _clp_cinfo) _clpAdjustPt(4985.56:-3766 _clp_cinfo) ) _clpMKSConvert(10.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(4081.94:88.39999999999964 _clp_cinfo) _clpAdjustPt(4081.94:-5502.5 _clp_cinfo) ) _clpMKSConvert(8.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(4389.24:-5502.5 _clp_cinfo) _clpAdjustPt(4081.94:-5502.5 _clp_cinfo) ) _clpMKSConvert(8.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(4389.24:88.39999999999964 _clp_cinfo) _clpAdjustPt(4389.24:-5502.5 _clp_cinfo) ) _clpMKSConvert(8.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(4389.24:88.39999999999964 _clp_cinfo) _clpAdjustPt(4081.94:88.39999999999964 _clp_cinfo) ) _clpMKSConvert(8.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_path = _clpPathStart(list(_clpAdjustPt(4995.29:-639 _clp_cinfo))                  
	_clpMKSConvert(0.100000 _clp_cinfo->t_from_units                  			_clp_cinfo->t_to_units))
_clp_path = _clpPathArcCenter(_clp_path _clpMKSConvert( 0.100000                   _clp_cinfo->t_from_units 
	_clp_cinfo->t_to_units)                   _clpAdjustPt(4995.29:-639 _clp_cinfo) nil
 	_clpAdjustPt(4984.29:-639 _clp_cinfo))
_clp_dbid = _clpDBCreatePath(_clp_path "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = caar(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(4981.29:-777 _clp_cinfo) _clpAdjustPt(4969.29:-777 _clp_cinfo) ) _clpMKSConvert(5.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(4981.29:-658 _clp_cinfo) _clpAdjustPt(4981.29:-777 _clp_cinfo) ) _clpMKSConvert(5.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(4981.29:-658 _clp_cinfo) _clpAdjustPt(4968.29:-645 _clp_cinfo) ) _clpMKSConvert(5.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(4869.29:-645 _clp_cinfo) _clpAdjustPt(4857.29:-645 _clp_cinfo) ) _clpMKSConvert(5.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(4857.29:-645 _clp_cinfo) _clpAdjustPt(4857.29:-777 _clp_cinfo) ) _clpMKSConvert(5.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(4868.29:-777 _clp_cinfo) _clpAdjustPt(4857.29:-777 _clp_cinfo) ) _clpMKSConvert(5.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(5154.29:-3223 _clp_cinfo) _clpAdjustPt(5142.29:-3223 _clp_cinfo) ) _clpMKSConvert(5.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(5142.29:-3223 _clp_cinfo) _clpAdjustPt(5142.29:-3342 _clp_cinfo) ) _clpMKSConvert(5.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(5155.29:-3355 _clp_cinfo) _clpAdjustPt(5142.29:-3342 _clp_cinfo) ) _clpMKSConvert(5.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(5266.29:-3355 _clp_cinfo) _clpAdjustPt(5254.29:-3355 _clp_cinfo) ) _clpMKSConvert(5.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(5266.29:-3223 _clp_cinfo) _clpAdjustPt(5266.29:-3355 _clp_cinfo) ) _clpMKSConvert(5.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(5266.29:-3223 _clp_cinfo) _clpAdjustPt(5255.29:-3223 _clp_cinfo) ) _clpMKSConvert(5.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(489.29:-2848.25 _clp_cinfo) _clpAdjustPt(449.29:-2848.25 _clp_cinfo) ) _clpMKSConvert(20.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(489.29:-2813.25 _clp_cinfo) _clpAdjustPt(489.29:-2848.25 _clp_cinfo) ) _clpMKSConvert(20.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(419.29:-2843.25 _clp_cinfo) _clpAdjustPt(379.29:-2843.25 _clp_cinfo) ) _clpMKSConvert(8.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(379.29:-2843.25 _clp_cinfo) _clpAdjustPt(314.29:-2843.25 _clp_cinfo) ) _clpMKSConvert(8.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(399.29:-2823.25 _clp_cinfo) _clpAdjustPt(379.29:-2843.25 _clp_cinfo) ) _clpMKSConvert(8.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(419.29:-2843.25 _clp_cinfo) _clpAdjustPt(399.29:-2823.25 _clp_cinfo) ) _clpMKSConvert(8.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(484.29:-2843.25 _clp_cinfo) _clpAdjustPt(419.29:-2843.25 _clp_cinfo) ) _clpMKSConvert(8.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(484.29:-2703.25 _clp_cinfo) _clpAdjustPt(484.29:-2843.25 _clp_cinfo) ) _clpMKSConvert(8.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(484.29:-2703.25 _clp_cinfo) _clpAdjustPt(314.29:-2703.25 _clp_cinfo) ) _clpMKSConvert(8.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(314.29:-2703.25 _clp_cinfo) _clpAdjustPt(314.29:-2843.25 _clp_cinfo) ) _clpMKSConvert(8.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(2599.29:-733.25 _clp_cinfo) _clpAdjustPt(2599.29:-773.25 _clp_cinfo) ) _clpMKSConvert(20.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(2634.29:-773.25 _clp_cinfo) _clpAdjustPt(2599.29:-773.25 _clp_cinfo) ) _clpMKSConvert(20.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(2604.29:-663.25 _clp_cinfo) _clpAdjustPt(2604.29:-703.25 _clp_cinfo) ) _clpMKSConvert(8.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(2604.29:-598.25 _clp_cinfo) _clpAdjustPt(2604.29:-663.25 _clp_cinfo) ) _clpMKSConvert(8.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(2624.29:-683.25 _clp_cinfo) _clpAdjustPt(2604.29:-663.25 _clp_cinfo) ) _clpMKSConvert(8.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(2624.29:-683.25 _clp_cinfo) _clpAdjustPt(2604.29:-703.25 _clp_cinfo) ) _clpMKSConvert(8.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(2604.29:-703.25 _clp_cinfo) _clpAdjustPt(2604.29:-768.25 _clp_cinfo) ) _clpMKSConvert(8.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(2744.29:-768.25 _clp_cinfo) _clpAdjustPt(2604.29:-768.25 _clp_cinfo) ) _clpMKSConvert(8.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

printf(" 10 percent completed")
newline()

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(2744.29:-598.25 _clp_cinfo) _clpAdjustPt(2744.29:-768.25 _clp_cinfo) ) _clpMKSConvert(8.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(2744.29:-598.25 _clp_cinfo) _clpAdjustPt(2604.29:-598.25 _clp_cinfo) ) _clpMKSConvert(8.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(5024.29:-818 _clp_cinfo) _clpAdjustPt(5018.29:-818 _clp_cinfo) ) _clpMKSConvert(6.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(5018.29:-672 _clp_cinfo) _clpAdjustPt(5018.29:-818 _clp_cinfo) ) _clpMKSConvert(6.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(5024.29:-672 _clp_cinfo) _clpAdjustPt(5018.29:-672 _clp_cinfo) ) _clpMKSConvert(6.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(5179.29:-705 _clp_cinfo) _clpAdjustPt(5139.29:-745 _clp_cinfo) ) _clpMKSConvert(6.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(5179.29:-705 _clp_cinfo) _clpAdjustPt(5179.29:-785 _clp_cinfo) ) _clpMKSConvert(6.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(5179.29:-785 _clp_cinfo) _clpAdjustPt(5139.29:-745 _clp_cinfo) ) _clpMKSConvert(6.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(5139.29:-710 _clp_cinfo) _clpAdjustPt(5139.29:-780 _clp_cinfo) ) _clpMKSConvert(6.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(5294.29:-818 _clp_cinfo) _clpAdjustPt(5024.29:-818 _clp_cinfo) ) _clpMKSConvert(6.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(5294.29:-672 _clp_cinfo) _clpAdjustPt(5294.29:-818 _clp_cinfo) ) _clpMKSConvert(6.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(5294.29:-672 _clp_cinfo) _clpAdjustPt(5024.29:-672 _clp_cinfo) ) _clpMKSConvert(6.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(5024.29:-672 _clp_cinfo) _clpAdjustPt(5024.29:-818 _clp_cinfo) ) _clpMKSConvert(6.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_path = _clpPathStart(list(_clpAdjustPt(-170.71:-1563.25 _clp_cinfo))                  
	_clpMKSConvert(6.000000 _clp_cinfo->t_from_units                  			_clp_cinfo->t_to_units))
_clp_path = _clpPathArcCenter(_clp_path _clpMKSConvert( 6.000000                   _clp_cinfo->t_from_units 
	_clp_cinfo->t_to_units)                   _clpAdjustPt(-170.71:-1563.25 _clp_cinfo) nil
 	_clpAdjustPt(-300.71:-1563.25 _clp_cinfo))
_clp_dbid = _clpDBCreatePath(_clp_path "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = caar(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-170.71:-1563.25 _clp_cinfo) _clpAdjustPt(-430.71:-1563.25 _clp_cinfo) ) _clpMKSConvert(6.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_path = _clpPathStart(list(_clpAdjustPt(5286.79:-965 _clp_cinfo))                  
	_clpMKSConvert(8.000000 _clp_cinfo->t_from_units                  			_clp_cinfo->t_to_units))
_clp_path = _clpPathArcCenter(_clp_path _clpMKSConvert( 8.000000                   _clp_cinfo->t_from_units 
	_clp_cinfo->t_to_units)                   _clpAdjustPt(5286.79:-965 _clp_cinfo) nil
 	_clpAdjustPt(5156.79:-965 _clp_cinfo))
_clp_dbid = _clpDBCreatePath(_clp_path "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = caar(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(5286.79:-965 _clp_cinfo) _clpAdjustPt(5026.79:-965 _clp_cinfo) ) _clpMKSConvert(8.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_path = _clpPathStart(list(_clpAdjustPt(5124.29:-5816.19 _clp_cinfo))                  
	_clpMKSConvert(8.000000 _clp_cinfo->t_from_units                  			_clp_cinfo->t_to_units))
_clp_path = _clpPathArcCenter(_clp_path _clpMKSConvert( 8.000000                   _clp_cinfo->t_from_units 
	_clp_cinfo->t_to_units)                   _clpAdjustPt(5124.29:-5816.19 _clp_cinfo) nil
 	_clpAdjustPt(4994.29:-5816.19 _clp_cinfo))
_clp_dbid = _clpDBCreatePath(_clp_path "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = caar(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(5124.29:-5816.19 _clp_cinfo) _clpAdjustPt(4864.29:-5816.19 _clp_cinfo) ) _clpMKSConvert(8.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_path = _clpPathStart(list(_clpAdjustPt(1977.52:-21.19999999999982 _clp_cinfo))                  
	_clpMKSConvert(8.000000 _clp_cinfo->t_from_units                  			_clp_cinfo->t_to_units))
_clp_path = _clpPathArcCenter(_clp_path _clpMKSConvert( 8.000000                   _clp_cinfo->t_from_units 
	_clp_cinfo->t_to_units)                   _clpAdjustPt(1977.52:-21.19999999999982 _clp_cinfo) nil
 	_clpAdjustPt(1847.52:-21.19999999999982 _clp_cinfo))
_clp_dbid = _clpDBCreatePath(_clp_path "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = caar(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(1977.52:-21.19999999999982 _clp_cinfo) _clpAdjustPt(1717.52:-21.19999999999982 _clp_cinfo) ) _clpMKSConvert(8.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(3552.29:149 _clp_cinfo) _clpAdjustPt(3552.29:-106 _clp_cinfo) ) _clpMKSConvert(10.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(3962.29:-106 _clp_cinfo) _clpAdjustPt(3552.29:-106 _clp_cinfo) ) _clpMKSConvert(10.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(3962.29:149 _clp_cinfo) _clpAdjustPt(3962.29:-106 _clp_cinfo) ) _clpMKSConvert(10.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(3962.29:149 _clp_cinfo) _clpAdjustPt(3552.29:149 _clp_cinfo) ) _clpMKSConvert(10.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(3957.29:-71 _clp_cinfo) _clpAdjustPt(3557.29:-71 _clp_cinfo) ) _clpMKSConvert(10.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_path = _clpPathStart(list(_clpAdjustPt(3833.09:-4257.8 _clp_cinfo))                  
	_clpMKSConvert(6.000000 _clp_cinfo->t_from_units                  			_clp_cinfo->t_to_units))
_clp_path = _clpPathArcCenter(_clp_path _clpMKSConvert( 6.000000                   _clp_cinfo->t_from_units 
	_clp_cinfo->t_to_units)                   _clpAdjustPt(3833.09:-4257.8 _clp_cinfo) nil
 	_clpAdjustPt(3714.99:-4257.8 _clp_cinfo))
_clp_dbid = _clpDBCreatePath(_clp_path "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = caar(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_path = _clpPathStart(list(_clpAdjustPt(762.29:-4257.8 _clp_cinfo))                  
	_clpMKSConvert(6.000000 _clp_cinfo->t_from_units                  			_clp_cinfo->t_to_units))
_clp_path = _clpPathArcCenter(_clp_path _clpMKSConvert( 6.000000                   _clp_cinfo->t_from_units 
	_clp_cinfo->t_to_units)                   _clpAdjustPt(762.29:-4257.8 _clp_cinfo) nil
 	_clpAdjustPt(644.1900000000001:-4257.8 _clp_cinfo))
_clp_dbid = _clpDBCreatePath(_clp_path "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = caar(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_path = _clpPathStart(list(_clpAdjustPt(3006.49:-1547.2 _clp_cinfo))                  
	_clpMKSConvert(6.000000 _clp_cinfo->t_from_units                  			_clp_cinfo->t_to_units))
_clp_path = _clpPathArcCenter(_clp_path _clpMKSConvert( 6.000000                   _clp_cinfo->t_from_units 
	_clp_cinfo->t_to_units)                   _clpAdjustPt(3006.49:-1547.2 _clp_cinfo) nil
 	_clpAdjustPt(2888.29:-1547.2 _clp_cinfo))
_clp_dbid = _clpDBCreatePath(_clp_path "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = caar(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_path = _clpPathStart(list(_clpAdjustPt(1588.99:-1547.2 _clp_cinfo))                  
	_clpMKSConvert(6.000000 _clp_cinfo->t_from_units                  			_clp_cinfo->t_to_units))
_clp_path = _clpPathArcCenter(_clp_path _clpMKSConvert( 6.000000                   _clp_cinfo->t_from_units 
	_clp_cinfo->t_to_units)                   _clpAdjustPt(1588.99:-1547.2 _clp_cinfo) nil
 	_clpAdjustPt(1470.99:-1547.2 _clp_cinfo))
_clp_dbid = _clpDBCreatePath(_clp_path "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = caar(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_path = _clpPathStart(list(_clpAdjustPt(762.29:-1187 _clp_cinfo))                  
	_clpMKSConvert(6.000000 _clp_cinfo->t_from_units                  			_clp_cinfo->t_to_units))
_clp_path = _clpPathArcCenter(_clp_path _clpMKSConvert( 6.000000                   _clp_cinfo->t_from_units 
	_clp_cinfo->t_to_units)                   _clpAdjustPt(762.29:-1187 _clp_cinfo) nil
 	_clpAdjustPt(644.1900000000001:-1187 _clp_cinfo))
_clp_dbid = _clpDBCreatePath(_clp_path "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = caar(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_path = _clpPathStart(list(_clpAdjustPt(3085.19:-3897.6 _clp_cinfo))                  
	_clpMKSConvert(6.000000 _clp_cinfo->t_from_units                  			_clp_cinfo->t_to_units))
_clp_path = _clpPathArcCenter(_clp_path _clpMKSConvert( 6.000000                   _clp_cinfo->t_from_units 
	_clp_cinfo->t_to_units)                   _clpAdjustPt(3085.19:-3897.6 _clp_cinfo) nil
 	_clpAdjustPt(2966.99:-3897.6 _clp_cinfo))
_clp_dbid = _clpDBCreatePath(_clp_path "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = caar(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_path = _clpPathStart(list(_clpAdjustPt(1510.39:-3897.6 _clp_cinfo))                  
	_clpMKSConvert(6.000000 _clp_cinfo->t_from_units                  			_clp_cinfo->t_to_units))
_clp_path = _clpPathArcCenter(_clp_path _clpMKSConvert( 6.000000                   _clp_cinfo->t_from_units 
	_clp_cinfo->t_to_units)                   _clpAdjustPt(1510.39:-3897.6 _clp_cinfo) nil
 	_clpAdjustPt(1392.19:-3897.6 _clp_cinfo))
_clp_dbid = _clpDBCreatePath(_clp_path "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = caar(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(3016.19:-2003.9 _clp_cinfo) _clpAdjustPt(3016.19:-3559 _clp_cinfo) ) _clpMKSConvert(6.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(1342.99:-2003.9 _clp_cinfo) _clpAdjustPt(1342.99:-3480.3 _clp_cinfo) ) _clpMKSConvert(6.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(3016.19:-1885.8 _clp_cinfo) _clpAdjustPt(3016.19:-3559 _clp_cinfo) ) _clpMKSConvert(6.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(1342.99:-1885.8 _clp_cinfo) _clpAdjustPt(1342.99:-3559 _clp_cinfo) ) _clpMKSConvert(6.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(1339.19:-4190.2 _clp_cinfo) _clpAdjustPt(1142.39:-4190.2 _clp_cinfo) ) _clpMKSConvert(6.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(1339.19:-4190.2 _clp_cinfo) _clpAdjustPt(1142.39:-3993.3 _clp_cinfo) ) _clpMKSConvert(6.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(1142.39:-3993.3 _clp_cinfo) _clpAdjustPt(1142.39:-4190.2 _clp_cinfo) ) _clpMKSConvert(6.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(3016.19:-3706.7 _clp_cinfo) _clpAdjustPt(1342.99:-3706.7 _clp_cinfo) ) _clpMKSConvert(6.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(3016.19:-1738.1 _clp_cinfo) _clpAdjustPt(3016.19:-3706.7 _clp_cinfo) ) _clpMKSConvert(6.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(3016.19:-1738.1 _clp_cinfo) _clpAdjustPt(1342.99:-1738.1 _clp_cinfo) ) _clpMKSConvert(6.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(1342.99:-1738.1 _clp_cinfo) _clpAdjustPt(1342.99:-3706.7 _clp_cinfo) ) _clpMKSConvert(6.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(3354.39:-1213.5 _clp_cinfo) _clpAdjustPt(1004.89:-1213.5 _clp_cinfo) ) _clpMKSConvert(6.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(4049.69:-1186.4 _clp_cinfo) _clpAdjustPt(3715.69:-852.3000000000002 _clp_cinfo) ) _clpMKSConvert(6.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(4049.69:-1186.4 _clp_cinfo) _clpAdjustPt(3374.89:-1861.2 _clp_cinfo) ) _clpMKSConvert(6.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(3374.59:-1197.4 _clp_cinfo) _clpAdjustPt(3374.59:-3582.4 _clp_cinfo) ) _clpMKSConvert(6.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(4049.69:-4258.4 _clp_cinfo) _clpAdjustPt(3374.89:-3583.6 _clp_cinfo) ) _clpMKSConvert(6.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(4049.69:-4258.4 _clp_cinfo) _clpAdjustPt(3715.69:-4592.5 _clp_cinfo) ) _clpMKSConvert(6.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(1004.59:-1212.4 _clp_cinfo) _clpAdjustPt(643.5899999999999:-852.3000000000002 _clp_cinfo) ) _clpMKSConvert(6.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(643.5899999999999:-852.3000000000002 _clp_cinfo) _clpAdjustPt(309.5899999999999:-1186.4 _clp_cinfo) ) _clpMKSConvert(6.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(1174.59:-2052.4 _clp_cinfo) _clpAdjustPt(309.5899999999999:-1186.4 _clp_cinfo) ) _clpMKSConvert(6.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(949.29:-1826.1 _clp_cinfo) _clpAdjustPt(949.29:-3618.6 _clp_cinfo) ) _clpMKSConvert(6.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(1174.59:-3392.4 _clp_cinfo) _clpAdjustPt(309.5899999999999:-4258.4 _clp_cinfo) ) _clpMKSConvert(6.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(643.5899999999999:-4592.5 _clp_cinfo) _clpAdjustPt(309.5899999999999:-4258.4 _clp_cinfo) ) _clpMKSConvert(6.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(965.5899999999999:-1174.3 _clp_cinfo) _clpAdjustPt(631.5899999999999:-1508.4 _clp_cinfo) ) _clpMKSConvert(6.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(965.5899999999999:-4270.5 _clp_cinfo) _clpAdjustPt(631.5899999999999:-3936.4 _clp_cinfo) ) _clpMKSConvert(6.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(3727.69:-1508.4 _clp_cinfo) _clpAdjustPt(3393.69:-1174.3 _clp_cinfo) ) _clpMKSConvert(6.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(3554.59:-3762.4 _clp_cinfo) _clpAdjustPt(3374.59:-1857.4 _clp_cinfo) ) _clpMKSConvert(6.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(3715.69:-4592.5 _clp_cinfo) _clpAdjustPt(2789.69:-4592.5 _clp_cinfo) ) _clpMKSConvert(6.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(2789.69:-4592.5 _clp_cinfo) _clpAdjustPt(2789.59:-4592.4 _clp_cinfo) ) _clpMKSConvert(6.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(2789.59:-4272.4 _clp_cinfo) _clpAdjustPt(2789.59:-4592.4 _clp_cinfo) ) _clpMKSConvert(6.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(2789.59:-4272.4 _clp_cinfo) _clpAdjustPt(2624.59:-4272.4 _clp_cinfo) ) _clpMKSConvert(6.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(2624.59:-4162.4 _clp_cinfo) _clpAdjustPt(2624.59:-4272.4 _clp_cinfo) ) _clpMKSConvert(6.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(2624.59:-4162.4 _clp_cinfo) _clpAdjustPt(2244.59:-4162.4 _clp_cinfo) ) _clpMKSConvert(6.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(2244.59:-4162.4 _clp_cinfo) _clpAdjustPt(2244.59:-4272.4 _clp_cinfo) ) _clpMKSConvert(6.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(2244.59:-4272.4 _clp_cinfo) _clpAdjustPt(2114.59:-4272.4 _clp_cinfo) ) _clpMKSConvert(6.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(2114.59:-4162.4 _clp_cinfo) _clpAdjustPt(2114.59:-4272.4 _clp_cinfo) ) _clpMKSConvert(6.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(2114.59:-4162.4 _clp_cinfo) _clpAdjustPt(1744.59:-4162.4 _clp_cinfo) ) _clpMKSConvert(6.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(1744.59:-4162.4 _clp_cinfo) _clpAdjustPt(1744.59:-4272.4 _clp_cinfo) ) _clpMKSConvert(6.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(1744.59:-4272.4 _clp_cinfo) _clpAdjustPt(1519.59:-4272.4 _clp_cinfo) ) _clpMKSConvert(6.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(1519.59:-4162.4 _clp_cinfo) _clpAdjustPt(1519.59:-4272.4 _clp_cinfo) ) _clpMKSConvert(6.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(1519.59:-4162.4 _clp_cinfo) _clpAdjustPt(1174.59:-4162.4 _clp_cinfo) ) _clpMKSConvert(6.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(1174.59:-1702.4 _clp_cinfo) _clpAdjustPt(1174.59:-4162.4 _clp_cinfo) ) _clpMKSConvert(6.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(1174.59:-1702.4 _clp_cinfo) _clpAdjustPt(1074.59:-1602.4 _clp_cinfo) ) _clpMKSConvert(6.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(1074.59:-1213.4 _clp_cinfo) _clpAdjustPt(1074.59:-1602.4 _clp_cinfo) ) _clpMKSConvert(6.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(3715.69:-852.3000000000002 _clp_cinfo) _clpAdjustPt(3355.09:-1212.9 _clp_cinfo) ) _clpMKSConvert(6.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(1174.09:-4062 _clp_cinfo) _clpAdjustPt(643.5899999999999:-4592.5 _clp_cinfo) ) _clpMKSConvert(6.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(2439.59:-2212.4 _clp_cinfo) _clpAdjustPt(1919.59:-2212.4 _clp_cinfo) ) _clpMKSConvert(6.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(2439.59:-2212.4 _clp_cinfo) _clpAdjustPt(2439.59:-3167.4 _clp_cinfo) ) _clpMKSConvert(6.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(2439.59:-3167.4 _clp_cinfo) _clpAdjustPt(1919.59:-3167.4 _clp_cinfo) ) _clpMKSConvert(6.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(1919.59:-2212.4 _clp_cinfo) _clpAdjustPt(1919.59:-3167.4 _clp_cinfo) ) _clpMKSConvert(6.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(3374.59:-3582.4 _clp_cinfo) _clpAdjustPt(3374.59:-4162.4 _clp_cinfo) ) _clpMKSConvert(6.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(3374.59:-4162.4 _clp_cinfo) _clpAdjustPt(1519.59:-4162.4 _clp_cinfo) ) _clpMKSConvert(6.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(3714.69:-4592.4 _clp_cinfo) _clpAdjustPt(3284.09:-4161.8 _clp_cinfo) ) _clpMKSConvert(6.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_path = _clpPathStart(list(_clpAdjustPt(608.81:-2958.53 _clp_cinfo))                  
	_clpMKSConvert(10.000000 _clp_cinfo->t_from_units                  			_clp_cinfo->t_to_units))
_clp_path = _clpPathArcCenter(_clp_path _clpMKSConvert( 10.000000                   _clp_cinfo->t_from_units 
	_clp_cinfo->t_to_units)                   _clpAdjustPt(589.1299999999999:-2938.85 _clp_cinfo) nil
 	_clpAdjustPt(589.1299999999999:-2958.53 _clp_cinfo))
_clp_dbid = _clpDBCreatePath(_clp_path "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = caar(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_path = _clpPathStart(list(_clpAdjustPt(589.1299999999999:-3234.11 _clp_cinfo))                  
	_clpMKSConvert(10.000000 _clp_cinfo->t_from_units                  			_clp_cinfo->t_to_units))
_clp_path = _clpPathArcCenter(_clp_path _clpMKSConvert( 10.000000                   _clp_cinfo->t_from_units 
	_clp_cinfo->t_to_units)                   _clpAdjustPt(608.81:-3214.43 _clp_cinfo) nil
 	_clpAdjustPt(589.1299999999999:-3214.43 _clp_cinfo))
_clp_dbid = _clpDBCreatePath(_clp_path "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = caar(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_path = _clpPathStart(list(_clpAdjustPt(193.8599999999999:-3214.43 _clp_cinfo))                  
	_clpMKSConvert(10.000000 _clp_cinfo->t_from_units                  			_clp_cinfo->t_to_units))
_clp_path = _clpPathArcCenter(_clp_path _clpMKSConvert( 10.000000                   _clp_cinfo->t_from_units 
	_clp_cinfo->t_to_units)                   _clpAdjustPt(213.54:-3234.11 _clp_cinfo) nil
 	_clpAdjustPt(213.54:-3214.43 _clp_cinfo))
_clp_dbid = _clpDBCreatePath(_clp_path "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = caar(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_path = _clpPathStart(list(_clpAdjustPt(213.54:-2938.85 _clp_cinfo))                  
	_clpMKSConvert(10.000000 _clp_cinfo->t_from_units                  			_clp_cinfo->t_to_units))
_clp_path = _clpPathArcCenter(_clp_path _clpMKSConvert( 10.000000                   _clp_cinfo->t_from_units 
	_clp_cinfo->t_to_units)                   _clpAdjustPt(193.8599999999999:-2958.53 _clp_cinfo) nil
 	_clpAdjustPt(213.54:-2958.53 _clp_cinfo))
_clp_dbid = _clpDBCreatePath(_clp_path "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = caar(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(589.1299999999999:-2938.84 _clp_cinfo) _clpAdjustPt(213.54:-2938.84 _clp_cinfo) ) _clpMKSConvert(10.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(608.8199999999999:-2958.53 _clp_cinfo) _clpAdjustPt(608.8199999999999:-3214.43 _clp_cinfo) ) _clpMKSConvert(10.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(589.1299999999999:-3234.12 _clp_cinfo) _clpAdjustPt(213.54:-3234.12 _clp_cinfo) ) _clpMKSConvert(10.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(193.8599999999999:-2958.53 _clp_cinfo) _clpAdjustPt(193.8599999999999:-3214.43 _clp_cinfo) ) _clpMKSConvert(10.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_path = _clpPathStart(list(_clpAdjustPt(273.3799999999999:-3343.73 _clp_cinfo))                  
	_clpMKSConvert(10.000000 _clp_cinfo->t_from_units                  			_clp_cinfo->t_to_units))
_clp_path = _clpPathArcCenter(_clp_path _clpMKSConvert( 10.000000                   _clp_cinfo->t_from_units 
	_clp_cinfo->t_to_units)                   _clpAdjustPt(253.7000000000001:-3363.41 _clp_cinfo) nil
 	_clpAdjustPt(273.3799999999999:-3363.41 _clp_cinfo))
_clp_dbid = _clpDBCreatePath(_clp_path "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = caar(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_path = _clpPathStart(list(_clpAdjustPt(548.97:-3363.41 _clp_cinfo))                  
	_clpMKSConvert(10.000000 _clp_cinfo->t_from_units                  			_clp_cinfo->t_to_units))
_clp_path = _clpPathArcCenter(_clp_path _clpMKSConvert( 10.000000                   _clp_cinfo->t_from_units 
	_clp_cinfo->t_to_units)                   _clpAdjustPt(529.29:-3343.73 _clp_cinfo) nil
 	_clpAdjustPt(529.29:-3363.41 _clp_cinfo))
_clp_dbid = _clpDBCreatePath(_clp_path "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = caar(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_path = _clpPathStart(list(_clpAdjustPt(529.29:-3758.68 _clp_cinfo))                  
	_clpMKSConvert(10.000000 _clp_cinfo->t_from_units                  			_clp_cinfo->t_to_units))
_clp_path = _clpPathArcCenter(_clp_path _clpMKSConvert( 10.000000                   _clp_cinfo->t_from_units 
	_clp_cinfo->t_to_units)                   _clpAdjustPt(548.97:-3739 _clp_cinfo) nil
 	_clpAdjustPt(529.29:-3739 _clp_cinfo))
_clp_dbid = _clpDBCreatePath(_clp_path "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = caar(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_path = _clpPathStart(list(_clpAdjustPt(253.7000000000001:-3739 _clp_cinfo))                  
	_clpMKSConvert(10.000000 _clp_cinfo->t_from_units                  			_clp_cinfo->t_to_units))
_clp_path = _clpPathArcCenter(_clp_path _clpMKSConvert( 10.000000                   _clp_cinfo->t_from_units 
	_clp_cinfo->t_to_units)                   _clpAdjustPt(273.3799999999999:-3758.68 _clp_cinfo) nil
 	_clpAdjustPt(273.3799999999999:-3739 _clp_cinfo))
_clp_dbid = _clpDBCreatePath(_clp_path "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = caar(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(253.7000000000001:-3363.41 _clp_cinfo) _clpAdjustPt(253.7000000000001:-3739 _clp_cinfo) ) _clpMKSConvert(10.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(529.29:-3343.72 _clp_cinfo) _clpAdjustPt(273.3799999999999:-3343.72 _clp_cinfo) ) _clpMKSConvert(10.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(548.98:-3363.41 _clp_cinfo) _clpAdjustPt(548.98:-3739 _clp_cinfo) ) _clpMKSConvert(10.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(529.29:-3758.68 _clp_cinfo) _clpAdjustPt(273.3799999999999:-3758.68 _clp_cinfo) ) _clpMKSConvert(10.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_path = _clpPathStart(list(_clpAdjustPt(180:0 _clp_cinfo))                  
	_clpMKSConvert(8.000000 _clp_cinfo->t_from_units                  			_clp_cinfo->t_to_units))
_clp_path = _clpPathArcCenter(_clp_path _clpMKSConvert( 8.000000                   _clp_cinfo->t_from_units 
	_clp_cinfo->t_to_units)                   _clpAdjustPt(180:0 _clp_cinfo) nil
 	_clpAdjustPt(0:0 _clp_cinfo))
_clp_dbid = _clpDBCreatePath(_clp_path "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = caar(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

printf(" 20 percent completed")
newline()

_clp_path = _clpPathStart(list(_clpAdjustPt(5394.29:-6170 _clp_cinfo))                  
	_clpMKSConvert(8.000000 _clp_cinfo->t_from_units                  			_clp_cinfo->t_to_units))
_clp_path = _clpPathArcCenter(_clp_path _clpMKSConvert( 8.000000                   _clp_cinfo->t_from_units 
	_clp_cinfo->t_to_units)                   _clpAdjustPt(5394.29:-6170 _clp_cinfo) nil
 	_clpAdjustPt(5214.29:-6170 _clp_cinfo))
_clp_dbid = _clpDBCreatePath(_clp_path "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = caar(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-709.4500000000001:-1133.25 _clp_cinfo) _clpAdjustPt(-884.4500000000001:-1133.25 _clp_cinfo) ) _clpMKSConvert(8.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-884.4500000000001:-1133.25 _clp_cinfo) _clpAdjustPt(-884.4500000000001:-1333.25 _clp_cinfo) ) _clpMKSConvert(8.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-709.4500000000001:-1333.25 _clp_cinfo) _clpAdjustPt(-884.4500000000001:-1333.25 _clp_cinfo) ) _clpMKSConvert(8.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-709.4500000000001:-1133.25 _clp_cinfo) _clpAdjustPt(-709.4500000000001:-1333.25 _clp_cinfo) ) _clpMKSConvert(8.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-939.4500000000001:-1133.25 _clp_cinfo) _clpAdjustPt(-1099.45:-1133.25 _clp_cinfo) ) _clpMKSConvert(8.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-1099.45:-1133.25 _clp_cinfo) _clpAdjustPt(-1099.45:-1333.25 _clp_cinfo) ) _clpMKSConvert(8.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-944.4500000000001:-1333.25 _clp_cinfo) _clpAdjustPt(-1099.45:-1333.25 _clp_cinfo) ) _clpMKSConvert(8.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-929.4500000000001:-1318.25 _clp_cinfo) _clpAdjustPt(-944.4500000000001:-1333.25 _clp_cinfo) ) _clpMKSConvert(8.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-929.4500000000001:-1143.25 _clp_cinfo) _clpAdjustPt(-929.4500000000001:-1318.25 _clp_cinfo) ) _clpMKSConvert(8.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-929.4500000000001:-1143.25 _clp_cinfo) _clpAdjustPt(-939.4500000000001:-1133.25 _clp_cinfo) ) _clpMKSConvert(8.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-719.4500000000001:-963.6499999999996 _clp_cinfo) _clpAdjustPt(-884.4500000000001:-963.6499999999996 _clp_cinfo) ) _clpMKSConvert(8.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-884.4500000000001:-963.6499999999996 _clp_cinfo) _clpAdjustPt(-884.4500000000001:-1113.65 _clp_cinfo) ) _clpMKSConvert(8.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-719.4500000000001:-1113.65 _clp_cinfo) _clpAdjustPt(-884.4500000000001:-1113.65 _clp_cinfo) ) _clpMKSConvert(8.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-709.4500000000001:-1103.65 _clp_cinfo) _clpAdjustPt(-719.4500000000001:-1113.65 _clp_cinfo) ) _clpMKSConvert(8.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-709.4500000000001:-973.6499999999996 _clp_cinfo) _clpAdjustPt(-709.4500000000001:-1103.65 _clp_cinfo) ) _clpMKSConvert(8.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-709.4500000000001:-973.6499999999996 _clp_cinfo) _clpAdjustPt(-719.4500000000001:-963.6499999999996 _clp_cinfo) ) _clpMKSConvert(8.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-929.4500000000001:-963.6499999999996 _clp_cinfo) _clpAdjustPt(-1099.45:-963.25 _clp_cinfo) ) _clpMKSConvert(8.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-1099.45:-963.25 _clp_cinfo) _clpAdjustPt(-1099.45:-1113.25 _clp_cinfo) ) _clpMKSConvert(8.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-929.4500000000001:-1113.25 _clp_cinfo) _clpAdjustPt(-1099.45:-1113.25 _clp_cinfo) ) _clpMKSConvert(8.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-929.4500000000001:-963.6499999999996 _clp_cinfo) _clpAdjustPt(-929.4500000000001:-1113.25 _clp_cinfo) ) _clpMKSConvert(8.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-1124.45:-1238.25 _clp_cinfo) _clpAdjustPt(-1364.45:-1238.25 _clp_cinfo) ) _clpMKSConvert(8.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-1364.45:-658.25 _clp_cinfo) _clpAdjustPt(-1364.45:-1238.25 _clp_cinfo) ) _clpMKSConvert(8.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-1124.45:-658.25 _clp_cinfo) _clpAdjustPt(-1364.45:-658.25 _clp_cinfo) ) _clpMKSConvert(8.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-939.4500000000001:-583.25 _clp_cinfo) _clpAdjustPt(-1099.45:-583.25 _clp_cinfo) ) _clpMKSConvert(8.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-1099.45:-583.25 _clp_cinfo) _clpAdjustPt(-1099.45:-783.25 _clp_cinfo) ) _clpMKSConvert(8.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-944.4500000000001:-783.25 _clp_cinfo) _clpAdjustPt(-1099.45:-783.25 _clp_cinfo) ) _clpMKSConvert(8.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-929.4500000000001:-768.25 _clp_cinfo) _clpAdjustPt(-944.4500000000001:-783.25 _clp_cinfo) ) _clpMKSConvert(8.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-929.4500000000001:-593.25 _clp_cinfo) _clpAdjustPt(-929.4500000000001:-768.25 _clp_cinfo) ) _clpMKSConvert(8.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-929.4500000000001:-593.25 _clp_cinfo) _clpAdjustPt(-939.4500000000001:-583.25 _clp_cinfo) ) _clpMKSConvert(8.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-929.4500000000001:-798.25 _clp_cinfo) _clpAdjustPt(-1099.45:-798.25 _clp_cinfo) ) _clpMKSConvert(8.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-1099.45:-798.25 _clp_cinfo) _clpAdjustPt(-1099.45:-948.25 _clp_cinfo) ) _clpMKSConvert(8.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-929.4500000000001:-948.25 _clp_cinfo) _clpAdjustPt(-1099.45:-948.25 _clp_cinfo) ) _clpMKSConvert(8.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-929.4500000000001:-798.25 _clp_cinfo) _clpAdjustPt(-929.4500000000001:-948.25 _clp_cinfo) ) _clpMKSConvert(8.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-1124.45:-703.25 _clp_cinfo) _clpAdjustPt(-1174.45:-703.25 _clp_cinfo) ) _clpMKSConvert(8.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-1174.45:-703.25 _clp_cinfo) _clpAdjustPt(-1174.45:-1193.25 _clp_cinfo) ) _clpMKSConvert(8.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-1124.45:-1193.25 _clp_cinfo) _clpAdjustPt(-1174.45:-1193.25 _clp_cinfo) ) _clpMKSConvert(8.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-719.4500000000001:-798.25 _clp_cinfo) _clpAdjustPt(-884.4500000000001:-798.25 _clp_cinfo) ) _clpMKSConvert(8.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-884.4500000000001:-798.25 _clp_cinfo) _clpAdjustPt(-884.4500000000001:-948.25 _clp_cinfo) ) _clpMKSConvert(8.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-719.4500000000001:-948.25 _clp_cinfo) _clpAdjustPt(-884.4500000000001:-948.25 _clp_cinfo) ) _clpMKSConvert(8.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-709.4500000000001:-938.25 _clp_cinfo) _clpAdjustPt(-719.4500000000001:-948.25 _clp_cinfo) ) _clpMKSConvert(8.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-709.4500000000001:-808.25 _clp_cinfo) _clpAdjustPt(-709.4500000000001:-938.25 _clp_cinfo) ) _clpMKSConvert(8.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-709.4500000000001:-808.25 _clp_cinfo) _clpAdjustPt(-719.4500000000001:-798.25 _clp_cinfo) ) _clpMKSConvert(8.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-709.4500000000001:-583.25 _clp_cinfo) _clpAdjustPt(-884.4500000000001:-583.25 _clp_cinfo) ) _clpMKSConvert(8.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-884.4500000000001:-583.25 _clp_cinfo) _clpAdjustPt(-884.4500000000001:-783.25 _clp_cinfo) ) _clpMKSConvert(8.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-709.4500000000001:-783.25 _clp_cinfo) _clpAdjustPt(-884.4500000000001:-783.25 _clp_cinfo) ) _clpMKSConvert(8.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-709.4500000000001:-583.25 _clp_cinfo) _clpAdjustPt(-709.4500000000001:-783.25 _clp_cinfo) ) _clpMKSConvert(8.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-689.4500000000001:-563.25 _clp_cinfo) _clpAdjustPt(-1124.45:-563.25 _clp_cinfo) ) _clpMKSConvert(8.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-1124.45:-563.25 _clp_cinfo) _clpAdjustPt(-1124.45:-1353.95 _clp_cinfo) ) _clpMKSConvert(8.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-689.4500000000001:-1353.95 _clp_cinfo) _clpAdjustPt(-1124.45:-1353.95 _clp_cinfo) ) _clpMKSConvert(8.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-689.4500000000001:-563.25 _clp_cinfo) _clpAdjustPt(-689.4500000000001:-1353.95 _clp_cinfo) ) _clpMKSConvert(8.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(5734.17:-2665 _clp_cinfo) _clpAdjustPt(5349.17:-2665 _clp_cinfo) ) _clpMKSConvert(8.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(5734.17:-630 _clp_cinfo) _clpAdjustPt(5734.17:-2665 _clp_cinfo) ) _clpMKSConvert(8.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(5734.17:-630 _clp_cinfo) _clpAdjustPt(5349.17:-630 _clp_cinfo) ) _clpMKSConvert(8.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(5349.17:-630 _clp_cinfo) _clpAdjustPt(5349.17:-2665 _clp_cinfo) ) _clpMKSConvert(8.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(5839.17:-1710 _clp_cinfo) _clpAdjustPt(5774.17:-1710 _clp_cinfo) ) _clpMKSConvert(8.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(5839.17:-1550 _clp_cinfo) _clpAdjustPt(5839.17:-1710 _clp_cinfo) ) _clpMKSConvert(8.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(5839.17:-1550 _clp_cinfo) _clpAdjustPt(5774.17:-1550 _clp_cinfo) ) _clpMKSConvert(8.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(6029.17:-1485 _clp_cinfo) _clpAdjustPt(5779.17:-1485 _clp_cinfo) ) _clpMKSConvert(8.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(6029.17:-1485 _clp_cinfo) _clpAdjustPt(6029.17:-1815 _clp_cinfo) ) _clpMKSConvert(8.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(6029.17:-1815 _clp_cinfo) _clpAdjustPt(5779.17:-1815 _clp_cinfo) ) _clpMKSConvert(8.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(5774.17:-630 _clp_cinfo) _clpAdjustPt(5774.17:-1015 _clp_cinfo) ) _clpMKSConvert(8.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(5774.17:-590 _clp_cinfo) _clpAdjustPt(5774.17:-630 _clp_cinfo) ) _clpMKSConvert(6.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(5774.17:-590 _clp_cinfo) _clpAdjustPt(5309.17:-590 _clp_cinfo) ) _clpMKSConvert(6.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(5309.17:-590 _clp_cinfo) _clpAdjustPt(5309.17:-2705 _clp_cinfo) ) _clpMKSConvert(6.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(5349.17:-2705 _clp_cinfo) _clpAdjustPt(5309.17:-2705 _clp_cinfo) ) _clpMKSConvert(6.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(5827.67:-737.5 _clp_cinfo) _clpAdjustPt(5772.67:-737.5 _clp_cinfo) ) _clpMKSConvert(6.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(5827.67:-737.5 _clp_cinfo) _clpAdjustPt(5827.67:-2557.5 _clp_cinfo) ) _clpMKSConvert(6.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(5827.67:-2557.5 _clp_cinfo) _clpAdjustPt(5772.67:-2557.5 _clp_cinfo) ) _clpMKSConvert(6.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(5774.17:-2705 _clp_cinfo) _clpAdjustPt(5349.17:-2705 _clp_cinfo) ) _clpMKSConvert(8.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(5774.17:-1410 _clp_cinfo) _clpAdjustPt(5774.17:-2705 _clp_cinfo) ) _clpMKSConvert(8.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-123.21:-3149.5 _clp_cinfo) _clpAdjustPt(-123.21:-3234.5 _clp_cinfo) ) _clpMKSConvert(6.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(171.79:-3234.5 _clp_cinfo) _clpAdjustPt(-123.21:-3234.5 _clp_cinfo) ) _clpMKSConvert(6.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(171.79:-3172 _clp_cinfo) _clpAdjustPt(171.79:-3234.5 _clp_cinfo) ) _clpMKSConvert(6.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(171.79:-3172 _clp_cinfo) _clpAdjustPt(156.79:-3172 _clp_cinfo) ) _clpMKSConvert(6.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(156.79:-3077 _clp_cinfo) _clpAdjustPt(156.79:-3172 _clp_cinfo) ) _clpMKSConvert(6.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(171.79:-3077 _clp_cinfo) _clpAdjustPt(156.79:-3077 _clp_cinfo) ) _clpMKSConvert(6.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(171.79:-3012 _clp_cinfo) _clpAdjustPt(171.79:-3077 _clp_cinfo) ) _clpMKSConvert(6.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(171.79:-3012 _clp_cinfo) _clpAdjustPt(-123.21:-3012 _clp_cinfo) ) _clpMKSConvert(6.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-123.21:-3012 _clp_cinfo) _clpAdjustPt(-123.21:-3149.5 _clp_cinfo) ) _clpMKSConvert(6.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(2115.54:-455.75 _clp_cinfo) _clpAdjustPt(2030.54:-455.75 _clp_cinfo) ) _clpMKSConvert(6.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(2115.54:-160.75 _clp_cinfo) _clpAdjustPt(2115.54:-455.75 _clp_cinfo) ) _clpMKSConvert(6.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(2115.54:-160.75 _clp_cinfo) _clpAdjustPt(2053.04:-160.75 _clp_cinfo) ) _clpMKSConvert(6.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(2053.04:-160.75 _clp_cinfo) _clpAdjustPt(2053.04:-175.75 _clp_cinfo) ) _clpMKSConvert(6.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(2053.04:-175.75 _clp_cinfo) _clpAdjustPt(1958.04:-175.75 _clp_cinfo) ) _clpMKSConvert(6.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(1958.04:-160.75 _clp_cinfo) _clpAdjustPt(1958.04:-175.75 _clp_cinfo) ) _clpMKSConvert(6.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(1958.04:-160.75 _clp_cinfo) _clpAdjustPt(1893.04:-160.75 _clp_cinfo) ) _clpMKSConvert(6.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(1893.04:-160.75 _clp_cinfo) _clpAdjustPt(1893.04:-455.75 _clp_cinfo) ) _clpMKSConvert(6.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(2030.54:-455.75 _clp_cinfo) _clpAdjustPt(1893.04:-455.75 _clp_cinfo) ) _clpMKSConvert(6.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(1668.04:-160.75 _clp_cinfo) _clpAdjustPt(1583.04:-160.75 _clp_cinfo) ) _clpMKSConvert(6.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(1583.04:-160.75 _clp_cinfo) _clpAdjustPt(1583.04:-455.75 _clp_cinfo) ) _clpMKSConvert(6.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(1645.54:-455.75 _clp_cinfo) _clpAdjustPt(1583.04:-455.75 _clp_cinfo) ) _clpMKSConvert(6.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(1645.54:-440.75 _clp_cinfo) _clpAdjustPt(1645.54:-455.75 _clp_cinfo) ) _clpMKSConvert(6.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(1740.54:-440.75 _clp_cinfo) _clpAdjustPt(1645.54:-440.75 _clp_cinfo) ) _clpMKSConvert(6.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(1740.54:-440.75 _clp_cinfo) _clpAdjustPt(1740.54:-455.75 _clp_cinfo) ) _clpMKSConvert(6.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(1805.54:-455.75 _clp_cinfo) _clpAdjustPt(1740.54:-455.75 _clp_cinfo) ) _clpMKSConvert(6.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(1805.54:-160.75 _clp_cinfo) _clpAdjustPt(1805.54:-455.75 _clp_cinfo) ) _clpMKSConvert(6.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(1805.54:-160.75 _clp_cinfo) _clpAdjustPt(1668.04:-160.75 _clp_cinfo) ) _clpMKSConvert(6.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(2745.54:-455.75 _clp_cinfo) _clpAdjustPt(2660.54:-455.75 _clp_cinfo) ) _clpMKSConvert(6.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(2745.54:-160.75 _clp_cinfo) _clpAdjustPt(2745.54:-455.75 _clp_cinfo) ) _clpMKSConvert(6.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(2745.54:-160.75 _clp_cinfo) _clpAdjustPt(2683.04:-160.75 _clp_cinfo) ) _clpMKSConvert(6.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(2683.04:-160.75 _clp_cinfo) _clpAdjustPt(2683.04:-175.75 _clp_cinfo) ) _clpMKSConvert(6.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(2683.04:-175.75 _clp_cinfo) _clpAdjustPt(2588.04:-175.75 _clp_cinfo) ) _clpMKSConvert(6.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(2588.04:-160.75 _clp_cinfo) _clpAdjustPt(2588.04:-175.75 _clp_cinfo) ) _clpMKSConvert(6.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

printf(" 30 percent completed")
newline()

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(2588.04:-160.75 _clp_cinfo) _clpAdjustPt(2523.04:-160.75 _clp_cinfo) ) _clpMKSConvert(6.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(2523.04:-160.75 _clp_cinfo) _clpAdjustPt(2523.04:-455.75 _clp_cinfo) ) _clpMKSConvert(6.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(2660.54:-455.75 _clp_cinfo) _clpAdjustPt(2523.04:-455.75 _clp_cinfo) ) _clpMKSConvert(6.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(2298.04:-160.75 _clp_cinfo) _clpAdjustPt(2213.04:-160.75 _clp_cinfo) ) _clpMKSConvert(6.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(2213.04:-160.75 _clp_cinfo) _clpAdjustPt(2213.04:-455.75 _clp_cinfo) ) _clpMKSConvert(6.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(2275.54:-455.75 _clp_cinfo) _clpAdjustPt(2213.04:-455.75 _clp_cinfo) ) _clpMKSConvert(6.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(2275.54:-440.75 _clp_cinfo) _clpAdjustPt(2275.54:-455.75 _clp_cinfo) ) _clpMKSConvert(6.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(2370.54:-440.75 _clp_cinfo) _clpAdjustPt(2275.54:-440.75 _clp_cinfo) ) _clpMKSConvert(6.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(2370.54:-440.75 _clp_cinfo) _clpAdjustPt(2370.54:-455.75 _clp_cinfo) ) _clpMKSConvert(6.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(2435.54:-455.75 _clp_cinfo) _clpAdjustPt(2370.54:-455.75 _clp_cinfo) ) _clpMKSConvert(6.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(2435.54:-160.75 _clp_cinfo) _clpAdjustPt(2435.54:-455.75 _clp_cinfo) ) _clpMKSConvert(6.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(2435.54:-160.75 _clp_cinfo) _clpAdjustPt(2298.04:-160.75 _clp_cinfo) ) _clpMKSConvert(6.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(1124.29:-605 _clp_cinfo) _clpAdjustPt(1074.29:-555 _clp_cinfo) ) _clpMKSConvert(8.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(1074.29:-555 _clp_cinfo) _clpAdjustPt(764.29:-555 _clp_cinfo) ) _clpMKSConvert(8.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(764.29:-555 _clp_cinfo) _clpAdjustPt(764.29:-915 _clp_cinfo) ) _clpMKSConvert(8.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(1124.29:-915 _clp_cinfo) _clpAdjustPt(764.29:-915 _clp_cinfo) ) _clpMKSConvert(8.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(1124.29:-605 _clp_cinfo) _clpAdjustPt(1124.29:-915 _clp_cinfo) ) _clpMKSConvert(8.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(1054.29:-570 _clp_cinfo) _clpAdjustPt(1049.29:-555 _clp_cinfo) ) _clpMKSConvert(8.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(1059.29:-555 _clp_cinfo) _clpAdjustPt(1054.29:-570 _clp_cinfo) ) _clpMKSConvert(8.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(1059.29:-555 _clp_cinfo) _clpAdjustPt(1054.29:-555 _clp_cinfo) ) _clpMKSConvert(8.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(1054.29:-555 _clp_cinfo) _clpAdjustPt(1054.29:-570 _clp_cinfo) ) _clpMKSConvert(8.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(1054.29:-570 _clp_cinfo) _clpAdjustPt(1044.29:-555 _clp_cinfo) ) _clpMKSConvert(8.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(1064.29:-555 _clp_cinfo) _clpAdjustPt(1044.29:-555 _clp_cinfo) ) _clpMKSConvert(8.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(1064.29:-555 _clp_cinfo) _clpAdjustPt(1054.29:-570 _clp_cinfo) ) _clpMKSConvert(8.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(834.29:-555 _clp_cinfo) _clpAdjustPt(834.29:-570 _clp_cinfo) ) _clpMKSConvert(8.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(779.29:-690 _clp_cinfo) _clpAdjustPt(764.29:-690 _clp_cinfo) ) _clpMKSConvert(8.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(779.29:-845 _clp_cinfo) _clpAdjustPt(764.29:-845 _clp_cinfo) ) _clpMKSConvert(8.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(894.29:-900 _clp_cinfo) _clpAdjustPt(894.29:-915 _clp_cinfo) ) _clpMKSConvert(8.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(1054.29:-900 _clp_cinfo) _clpAdjustPt(1054.29:-915 _clp_cinfo) ) _clpMKSConvert(8.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(1124.29:-625 _clp_cinfo) _clpAdjustPt(1109.29:-625 _clp_cinfo) ) _clpMKSConvert(8.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(1124.29:-705 _clp_cinfo) _clpAdjustPt(1109.29:-705 _clp_cinfo) ) _clpMKSConvert(8.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(974.29:-900 _clp_cinfo) _clpAdjustPt(974.29:-915 _clp_cinfo) ) _clpMKSConvert(8.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(989.29:-555 _clp_cinfo) _clpAdjustPt(989.29:-570 _clp_cinfo) ) _clpMKSConvert(8.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(1124.29:-780 _clp_cinfo) _clpAdjustPt(1109.29:-780 _clp_cinfo) ) _clpMKSConvert(8.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(779.29:-765 _clp_cinfo) _clpAdjustPt(764.29:-765 _clp_cinfo) ) _clpMKSConvert(8.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(914.29:-555 _clp_cinfo) _clpAdjustPt(914.29:-570 _clp_cinfo) ) _clpMKSConvert(8.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(2189.29:-4398.25 _clp_cinfo) _clpAdjustPt(2189.29:-4418.25 _clp_cinfo) ) _clpMKSConvert(6.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(59.28999999999996:-2943.25 _clp_cinfo) _clpAdjustPt(59.28999999999996:-2993.25 _clp_cinfo) ) _clpMKSConvert(5.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(59.28999999999996:-2943.25 _clp_cinfo) _clpAdjustPt(-50.71000000000004:-2943.25 _clp_cinfo) ) _clpMKSConvert(5.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-50.71000000000004:-2943.25 _clp_cinfo) _clpAdjustPt(-50.71000000000004:-2993.25 _clp_cinfo) ) _clpMKSConvert(5.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(59.28999999999996:-2993.25 _clp_cinfo) _clpAdjustPt(-50.71000000000004:-2993.25 _clp_cinfo) ) _clpMKSConvert(5.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(4.289999999999964:-2953.25 _clp_cinfo) _clpAdjustPt(4.289999999999964:-2983.25 _clp_cinfo) ) _clpMKSConvert(12.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_path = _clpPathStart(list(_clpAdjustPt(1327.17:-5360 _clp_cinfo))                  
	_clpMKSConvert(10.000000 _clp_cinfo->t_from_units                  			_clp_cinfo->t_to_units))
_clp_path = _clpPathArcCenter(_clp_path _clpMKSConvert( 10.000000                   _clp_cinfo->t_from_units 
	_clp_cinfo->t_to_units)                   _clpAdjustPt(1327.17:-5360 _clp_cinfo) nil
 	_clpAdjustPt(1193.28:-5360 _clp_cinfo))
_clp_dbid = _clpDBCreatePath(_clp_path "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = caar(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_path = _clpPathStart(list(_clpAdjustPt(2035.73:-5360.01 _clp_cinfo))                  
	_clpMKSConvert(10.000000 _clp_cinfo->t_from_units                  			_clp_cinfo->t_to_units))
_clp_path = _clpPathArcCenter(_clp_path _clpMKSConvert( 10.000000                   _clp_cinfo->t_from_units 
	_clp_cinfo->t_to_units)                   _clpAdjustPt(2035.73:-5360.01 _clp_cinfo) nil
 	_clpAdjustPt(1901.84:-5360.01 _clp_cinfo))
_clp_dbid = _clpDBCreatePath(_clp_path "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = caar(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_path = _clpPathStart(list(_clpAdjustPt(539.77:-5360 _clp_cinfo))                  
	_clpMKSConvert(10.000000 _clp_cinfo->t_from_units                  			_clp_cinfo->t_to_units))
_clp_path = _clpPathArcCenter(_clp_path _clpMKSConvert( 10.000000                   _clp_cinfo->t_from_units 
	_clp_cinfo->t_to_units)                   _clpAdjustPt(539.77:-5360 _clp_cinfo) nil
 	_clpAdjustPt(405.8799999999999:-5360 _clp_cinfo))
_clp_dbid = _clpDBCreatePath(_clp_path "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = caar(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_path = _clpPathStart(list(_clpAdjustPt(5114.29:-2785 _clp_cinfo))                  
	_clpMKSConvert(10.000000 _clp_cinfo->t_from_units                  			_clp_cinfo->t_to_units))
_clp_path = _clpPathArcCenter(_clp_path _clpMKSConvert( 10.000000                   _clp_cinfo->t_from_units 
	_clp_cinfo->t_to_units)                   _clpAdjustPt(5114.29:-2785 _clp_cinfo) nil
 	_clpAdjustPt(5109.29:-2785 _clp_cinfo))
_clp_dbid = _clpDBCreatePath(_clp_path "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = caar(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(5109.29:-2850 _clp_cinfo) _clpAdjustPt(5109.29:-2980 _clp_cinfo) ) _clpMKSConvert(5.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(5109.29:-2980 _clp_cinfo) _clpAdjustPt(4909.29:-2980 _clp_cinfo) ) _clpMKSConvert(5.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(4909.29:-2850 _clp_cinfo) _clpAdjustPt(4909.29:-2980 _clp_cinfo) ) _clpMKSConvert(5.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(5109.29:-2850 _clp_cinfo) _clpAdjustPt(4909.29:-2850 _clp_cinfo) ) _clpMKSConvert(5.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(5109.29:-2895 _clp_cinfo) _clpAdjustPt(5089.29:-2915 _clp_cinfo) ) _clpMKSConvert(5.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(5109.29:-2935 _clp_cinfo) _clpAdjustPt(5089.29:-2915 _clp_cinfo) ) _clpMKSConvert(5.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_path = _clpPathStart(list(_clpAdjustPt(1294.08:-5360 _clp_cinfo))                  
	_clpMKSConvert(15.000000 _clp_cinfo->t_from_units                  			_clp_cinfo->t_to_units))
_clp_path = _clpPathArcCenter(_clp_path _clpMKSConvert( 15.000000                   _clp_cinfo->t_from_units 
	_clp_cinfo->t_to_units)                   _clpAdjustPt(1294.08:-5360 _clp_cinfo) nil
 	_clpAdjustPt(1193.28:-5360 _clp_cinfo))
_clp_dbid = _clpDBCreatePath(_clp_path "ETCH/TOP" 'line _clp_sym)

_clp_dbid = caar(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_path = _clpPathStart(list(_clpAdjustPt(2002.64:-5360.01 _clp_cinfo))                  
	_clpMKSConvert(15.000000 _clp_cinfo->t_from_units                  			_clp_cinfo->t_to_units))
_clp_path = _clpPathArcCenter(_clp_path _clpMKSConvert( 15.000000                   _clp_cinfo->t_from_units 
	_clp_cinfo->t_to_units)                   _clpAdjustPt(2002.64:-5360.01 _clp_cinfo) nil
 	_clpAdjustPt(1901.84:-5360.01 _clp_cinfo))
_clp_dbid = _clpDBCreatePath(_clp_path "ETCH/TOP" 'line _clp_sym)

_clp_dbid = caar(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_path = _clpPathStart(list(_clpAdjustPt(506.6800000000001:-5360 _clp_cinfo))                  
	_clpMKSConvert(15.000000 _clp_cinfo->t_from_units                  			_clp_cinfo->t_to_units))
_clp_path = _clpPathArcCenter(_clp_path _clpMKSConvert( 15.000000                   _clp_cinfo->t_from_units 
	_clp_cinfo->t_to_units)                   _clpAdjustPt(506.6800000000001:-5360 _clp_cinfo) nil
 	_clpAdjustPt(405.8799999999999:-5360 _clp_cinfo))
_clp_dbid = _clpDBCreatePath(_clp_path "ETCH/TOP" 'line _clp_sym)

_clp_dbid = caar(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(2885.09:-1918.8 _clp_cinfo) _clpAdjustPt(2900.29:-1903.6 _clp_cinfo) ) _clpMKSConvert(8.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "ETCH/TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(2874.59:-1918.8 _clp_cinfo) _clpAdjustPt(2885.09:-1918.8 _clp_cinfo) ) _clpMKSConvert(8.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "ETCH/TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(2685.59:-1855.8 _clp_cinfo) _clpAdjustPt(2701.39:-1840 _clp_cinfo) ) _clpMKSConvert(8.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "ETCH/TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(2678.23:-1855.8 _clp_cinfo) _clpAdjustPt(2685.59:-1855.8 _clp_cinfo) ) _clpMKSConvert(8.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "ETCH/TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(2676.93:-1854.5 _clp_cinfo) _clpAdjustPt(2678.23:-1855.8 _clp_cinfo) ) _clpMKSConvert(8.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "ETCH/TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(2662.85:-1854.5 _clp_cinfo) _clpAdjustPt(2676.93:-1854.5 _clp_cinfo) ) _clpMKSConvert(8.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "ETCH/TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(2661.55:-1855.8 _clp_cinfo) _clpAdjustPt(2662.85:-1854.5 _clp_cinfo) ) _clpMKSConvert(8.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "ETCH/TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(2654.09:-1855.8 _clp_cinfo) _clpAdjustPt(2661.55:-1855.8 _clp_cinfo) ) _clpMKSConvert(8.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "ETCH/TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(2748.59:-1844.2 _clp_cinfo) _clpAdjustPt(2759.29:-1833.5 _clp_cinfo) ) _clpMKSConvert(8.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "ETCH/TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(2748.59:-1855.8 _clp_cinfo) _clpAdjustPt(2748.59:-1844.2 _clp_cinfo) ) _clpMKSConvert(8.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "ETCH/TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(2638.29:-2410.6 _clp_cinfo) _clpAdjustPt(2638.29:-2438.5 _clp_cinfo) ) _clpMKSConvert(4.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "ETCH/TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(2512.59:-1839.8 _clp_cinfo) _clpAdjustPt(2496.59:-1855.8 _clp_cinfo) ) _clpMKSConvert(8.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "ETCH/TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(2528.09:-1855.2 _clp_cinfo) _clpAdjustPt(2512.69:-1839.8 _clp_cinfo) ) _clpMKSConvert(8.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "ETCH/TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(2528.09:-1855.8 _clp_cinfo) _clpAdjustPt(2528.09:-1855.2 _clp_cinfo) ) _clpMKSConvert(8.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "ETCH/TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(2621.29:-1818.4 _clp_cinfo) _clpAdjustPt(2638.39:-1801.3 _clp_cinfo) ) _clpMKSConvert(8.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "ETCH/TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(2621.29:-1846.94 _clp_cinfo) _clpAdjustPt(2621.29:-1818.4 _clp_cinfo) ) _clpMKSConvert(8.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "ETCH/TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(2622.59:-1848.24 _clp_cinfo) _clpAdjustPt(2621.29:-1846.94 _clp_cinfo) ) _clpMKSConvert(8.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "ETCH/TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(2622.59:-1855.8 _clp_cinfo) _clpAdjustPt(2622.59:-1848.24 _clp_cinfo) ) _clpMKSConvert(8.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "ETCH/TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(4013.64:-2733.4 _clp_cinfo) _clpAdjustPt(4088.74:-2733.4 _clp_cinfo) ) _clpMKSConvert(8.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "ETCH/TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(3999.64:-2719.4 _clp_cinfo) _clpAdjustPt(4013.64:-2733.4 _clp_cinfo) ) _clpMKSConvert(8.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "ETCH/TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(3999.64:-2678.6 _clp_cinfo) _clpAdjustPt(3999.64:-2719.4 _clp_cinfo) ) _clpMKSConvert(8.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "ETCH/TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(3991.64:-2670.6 _clp_cinfo) _clpAdjustPt(3999.64:-2678.6 _clp_cinfo) ) _clpMKSConvert(8.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "ETCH/TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(3973.64:-2670.6 _clp_cinfo) _clpAdjustPt(3991.64:-2670.6 _clp_cinfo) ) _clpMKSConvert(8.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "ETCH/TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(3965.64:-2678.6 _clp_cinfo) _clpAdjustPt(3973.64:-2670.6 _clp_cinfo) ) _clpMKSConvert(8.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "ETCH/TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(3965.64:-2718.4 _clp_cinfo) _clpAdjustPt(3965.64:-2678.6 _clp_cinfo) ) _clpMKSConvert(8.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "ETCH/TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(3949.54:-2734.5 _clp_cinfo) _clpAdjustPt(3965.64:-2718.4 _clp_cinfo) ) _clpMKSConvert(8.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "ETCH/TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(3920.74:-2734.5 _clp_cinfo) _clpAdjustPt(3949.54:-2734.5 _clp_cinfo) ) _clpMKSConvert(8.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "ETCH/TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(3905.64:-2719.4 _clp_cinfo) _clpAdjustPt(3920.74:-2734.5 _clp_cinfo) ) _clpMKSConvert(8.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "ETCH/TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(3905.64:-2672.6 _clp_cinfo) _clpAdjustPt(3905.64:-2719.4 _clp_cinfo) ) _clpMKSConvert(8.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "ETCH/TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(3897.64:-2664.6 _clp_cinfo) _clpAdjustPt(3905.64:-2672.6 _clp_cinfo) ) _clpMKSConvert(8.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "ETCH/TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(3879.64:-2664.6 _clp_cinfo) _clpAdjustPt(3897.64:-2664.6 _clp_cinfo) ) _clpMKSConvert(8.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "ETCH/TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(3871.64:-2672.6 _clp_cinfo) _clpAdjustPt(3879.64:-2664.6 _clp_cinfo) ) _clpMKSConvert(8.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "ETCH/TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(3871.64:-2679.8 _clp_cinfo) _clpAdjustPt(3871.64:-2672.6 _clp_cinfo) ) _clpMKSConvert(8.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "ETCH/TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(3856.04:-2695.4 _clp_cinfo) _clpAdjustPt(3871.64:-2679.8 _clp_cinfo) ) _clpMKSConvert(8.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "ETCH/TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(3823.74:-2695.4 _clp_cinfo) _clpAdjustPt(3856.04:-2695.4 _clp_cinfo) ) _clpMKSConvert(8.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "ETCH/TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(3808.14:-2679.8 _clp_cinfo) _clpAdjustPt(3823.74:-2695.4 _clp_cinfo) ) _clpMKSConvert(8.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "ETCH/TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(3808.14:-2672.6 _clp_cinfo) _clpAdjustPt(3808.14:-2679.8 _clp_cinfo) ) _clpMKSConvert(8.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "ETCH/TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(3800.14:-2664.6 _clp_cinfo) _clpAdjustPt(3808.14:-2672.6 _clp_cinfo) ) _clpMKSConvert(8.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "ETCH/TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(3782.14:-2664.6 _clp_cinfo) _clpAdjustPt(3800.14:-2664.6 _clp_cinfo) ) _clpMKSConvert(8.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "ETCH/TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(3774.14:-2672.6 _clp_cinfo) _clpAdjustPt(3782.14:-2664.6 _clp_cinfo) ) _clpMKSConvert(8.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "ETCH/TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(3774.14:-2679.8 _clp_cinfo) _clpAdjustPt(3774.14:-2672.6 _clp_cinfo) ) _clpMKSConvert(8.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "ETCH/TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(3758.54:-2695.4 _clp_cinfo) _clpAdjustPt(3774.14:-2679.8 _clp_cinfo) ) _clpMKSConvert(8.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "ETCH/TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(3729.74:-2695.4 _clp_cinfo) _clpAdjustPt(3758.54:-2695.4 _clp_cinfo) ) _clpMKSConvert(8.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "ETCH/TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(3714.14:-2679.8 _clp_cinfo) _clpAdjustPt(3729.74:-2695.4 _clp_cinfo) ) _clpMKSConvert(8.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "ETCH/TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(3714.14:-2672.6 _clp_cinfo) _clpAdjustPt(3714.14:-2679.8 _clp_cinfo) ) _clpMKSConvert(8.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "ETCH/TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(3706.14:-2664.6 _clp_cinfo) _clpAdjustPt(3714.14:-2672.6 _clp_cinfo) ) _clpMKSConvert(8.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "ETCH/TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(3688.14:-2664.6 _clp_cinfo) _clpAdjustPt(3706.14:-2664.6 _clp_cinfo) ) _clpMKSConvert(8.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "ETCH/TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(3680.14:-2672.6 _clp_cinfo) _clpAdjustPt(3688.14:-2664.6 _clp_cinfo) ) _clpMKSConvert(8.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "ETCH/TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

printf(" 40 percent completed")
newline()

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(3680.14:-2679.8 _clp_cinfo) _clpAdjustPt(3680.14:-2672.6 _clp_cinfo) ) _clpMKSConvert(8.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "ETCH/TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(3664.54:-2695.4 _clp_cinfo) _clpAdjustPt(3680.14:-2679.8 _clp_cinfo) ) _clpMKSConvert(8.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "ETCH/TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(3635.74:-2695.4 _clp_cinfo) _clpAdjustPt(3664.54:-2695.4 _clp_cinfo) ) _clpMKSConvert(8.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "ETCH/TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(3620.14:-2679.8 _clp_cinfo) _clpAdjustPt(3635.74:-2695.4 _clp_cinfo) ) _clpMKSConvert(8.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "ETCH/TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(3620.14:-2672.6 _clp_cinfo) _clpAdjustPt(3620.14:-2679.8 _clp_cinfo) ) _clpMKSConvert(8.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "ETCH/TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(3612.14:-2664.6 _clp_cinfo) _clpAdjustPt(3620.14:-2672.6 _clp_cinfo) ) _clpMKSConvert(8.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "ETCH/TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(3594.14:-2664.6 _clp_cinfo) _clpAdjustPt(3612.14:-2664.6 _clp_cinfo) ) _clpMKSConvert(8.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "ETCH/TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(3586.14:-2672.6 _clp_cinfo) _clpAdjustPt(3594.14:-2664.6 _clp_cinfo) ) _clpMKSConvert(8.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "ETCH/TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(3586.14:-2679.8 _clp_cinfo) _clpAdjustPt(3586.14:-2672.6 _clp_cinfo) ) _clpMKSConvert(8.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "ETCH/TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(3570.54:-2695.4 _clp_cinfo) _clpAdjustPt(3586.14:-2679.8 _clp_cinfo) ) _clpMKSConvert(8.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "ETCH/TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(3541.74:-2695.4 _clp_cinfo) _clpAdjustPt(3570.54:-2695.4 _clp_cinfo) ) _clpMKSConvert(8.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "ETCH/TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(3526.14:-2679.8 _clp_cinfo) _clpAdjustPt(3541.74:-2695.4 _clp_cinfo) ) _clpMKSConvert(8.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "ETCH/TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(3526.14:-2672.6 _clp_cinfo) _clpAdjustPt(3526.14:-2679.8 _clp_cinfo) ) _clpMKSConvert(8.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "ETCH/TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(3518.14:-2664.6 _clp_cinfo) _clpAdjustPt(3526.14:-2672.6 _clp_cinfo) ) _clpMKSConvert(8.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "ETCH/TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(3500.14:-2664.6 _clp_cinfo) _clpAdjustPt(3518.14:-2664.6 _clp_cinfo) ) _clpMKSConvert(8.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "ETCH/TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(3492.14:-2672.6 _clp_cinfo) _clpAdjustPt(3500.14:-2664.6 _clp_cinfo) ) _clpMKSConvert(8.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "ETCH/TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(3492.14:-2679.8 _clp_cinfo) _clpAdjustPt(3492.14:-2672.6 _clp_cinfo) ) _clpMKSConvert(8.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "ETCH/TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(3476.54:-2695.4 _clp_cinfo) _clpAdjustPt(3492.14:-2679.8 _clp_cinfo) ) _clpMKSConvert(8.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "ETCH/TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(3447.74:-2695.4 _clp_cinfo) _clpAdjustPt(3476.54:-2695.4 _clp_cinfo) ) _clpMKSConvert(8.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "ETCH/TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(3432.14:-2679.8 _clp_cinfo) _clpAdjustPt(3447.74:-2695.4 _clp_cinfo) ) _clpMKSConvert(8.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "ETCH/TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(3432.14:-2672.6 _clp_cinfo) _clpAdjustPt(3432.14:-2679.8 _clp_cinfo) ) _clpMKSConvert(8.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "ETCH/TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(3424.14:-2664.6 _clp_cinfo) _clpAdjustPt(3432.14:-2672.6 _clp_cinfo) ) _clpMKSConvert(8.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "ETCH/TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(3406.14:-2664.6 _clp_cinfo) _clpAdjustPt(3424.14:-2664.6 _clp_cinfo) ) _clpMKSConvert(8.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "ETCH/TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(3375.34:-2695.4 _clp_cinfo) _clpAdjustPt(3406.14:-2664.6 _clp_cinfo) ) _clpMKSConvert(8.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "ETCH/TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(3148.44:-2695.4 _clp_cinfo) _clpAdjustPt(3375.34:-2695.4 _clp_cinfo) ) _clpMKSConvert(8.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "ETCH/TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(3062.24:-2609.2 _clp_cinfo) _clpAdjustPt(3148.44:-2695.4 _clp_cinfo) ) _clpMKSConvert(8.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "ETCH/TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(2970.94:-2609.2 _clp_cinfo) _clpAdjustPt(3062.24:-2609.2 _clp_cinfo) ) _clpMKSConvert(8.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "ETCH/TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-435.71:-633.3800000000001 _clp_cinfo) _clpAdjustPt(-435.71:-1243.25 _clp_cinfo) ) _clpMKSConvert(393.700000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "ETCH/TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(1626.32:-2848.83 _clp_cinfo) _clpAdjustPt(1626.32:-2880.33 _clp_cinfo) ) _clpMKSConvert(5.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "ETCH/TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_path = _clpPathStart(list(_clpAdjustPt(-1285.71:85 _clp_cinfo))                  
	_clpMKSConvert(0.000000 _clp_cinfo->t_from_units                  			_clp_cinfo->t_to_units))
_clp_path = _clpPathArcCenter(_clp_path _clpMKSConvert( 0.000000                   _clp_cinfo->t_from_units 
	_clp_cinfo->t_to_units)                   _clpAdjustPt(-1165.71:205 _clp_cinfo) t
 	_clpAdjustPt(-1165.71:85 _clp_cinfo))
_clp_dbid = _clpDBCreatePath(_clp_path "BOARD GEOMETRY/DXFTOP" 'line _clp_sym)

_clp_dbid = caar(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_path = _clpPathStart(list(_clpAdjustPt(5679.04:205 _clp_cinfo))                  
	_clpMKSConvert(0.000000 _clp_cinfo->t_from_units                  			_clp_cinfo->t_to_units))
_clp_path = _clpPathArcCenter(_clp_path _clpMKSConvert( 0.000000                   _clp_cinfo->t_from_units 
	_clp_cinfo->t_to_units)                   _clpAdjustPt(5799.04:85 _clp_cinfo) t
 	_clpAdjustPt(5679.04:85 _clp_cinfo))
_clp_dbid = _clpDBCreatePath(_clp_path "BOARD GEOMETRY/DXFTOP" 'line _clp_sym)

_clp_dbid = caar(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(5799.04:-8528.25 _clp_cinfo) _clpAdjustPt(5799.04:85 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFTOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-1285.71:-6488 _clp_cinfo) _clpAdjustPt(-1285.71:-8528.25 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFTOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(5679.04:-6488 _clp_cinfo) _clpAdjustPt(5407.29:-6488 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFTOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(5407.29:-6488 _clp_cinfo) _clpAdjustPt(5407.29:-8528.25 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFTOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-1285.71:-6368 _clp_cinfo) _clpAdjustPt(-1285.71:85 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFTOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_path = _clpPathStart(list(_clpAdjustPt(-1285.71:-6368 _clp_cinfo))                  
	_clpMKSConvert(0.000000 _clp_cinfo->t_from_units                  			_clp_cinfo->t_to_units))
_clp_path = _clpPathArcCenter(_clp_path _clpMKSConvert( 0.000000                   _clp_cinfo->t_from_units 
	_clp_cinfo->t_to_units)                   _clpAdjustPt(-1165.71:-6488 _clp_cinfo) nil
 	_clpAdjustPt(-1165.71:-6368 _clp_cinfo))
_clp_dbid = _clpDBCreatePath(_clp_path "BOARD GEOMETRY/DXFTOP" 'line _clp_sym)

_clp_dbid = caar(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(5287.29:-6488 _clp_cinfo) _clpAdjustPt(-1165.71:-6488 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFTOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_path = _clpPathStart(list(_clpAdjustPt(5287.29:-6488 _clp_cinfo))                  
	_clpMKSConvert(0.000000 _clp_cinfo->t_from_units                  			_clp_cinfo->t_to_units))
_clp_path = _clpPathArcCenter(_clp_path _clpMKSConvert( 0.000000                   _clp_cinfo->t_from_units 
	_clp_cinfo->t_to_units)                   _clpAdjustPt(5407.29:-6368 _clp_cinfo) nil
 	_clpAdjustPt(5287.29:-6368 _clp_cinfo))
_clp_dbid = _clpDBCreatePath(_clp_path "BOARD GEOMETRY/DXFTOP" 'line _clp_sym)

_clp_dbid = caar(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(5407.29:205 _clp_cinfo) _clpAdjustPt(5679.04:205 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFTOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(5407.29:85 _clp_cinfo) _clpAdjustPt(5407.29:-6368 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFTOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_path = _clpPathStart(list(_clpAdjustPt(5407.29:85 _clp_cinfo))                  
	_clpMKSConvert(0.000000 _clp_cinfo->t_from_units                  			_clp_cinfo->t_to_units))
_clp_path = _clpPathArcCenter(_clp_path _clpMKSConvert( 0.000000                   _clp_cinfo->t_from_units 
	_clp_cinfo->t_to_units)                   _clpAdjustPt(5287.29:205 _clp_cinfo) nil
 	_clpAdjustPt(5287.29:85 _clp_cinfo))
_clp_dbid = _clpDBCreatePath(_clp_path "BOARD GEOMETRY/DXFTOP" 'line _clp_sym)

_clp_dbid = caar(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-1165.71:205 _clp_cinfo) _clpAdjustPt(5287.29:205 _clp_cinfo) ) _clpMKSConvert(0.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "BOARD GEOMETRY/DXFTOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(2634.29:-4297.25 _clp_cinfo) _clpAdjustPt(2634.29:-4329.25 _clp_cinfo) ) _clpMKSConvert(12.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(2634.29:-4367.25 _clp_cinfo) _clpAdjustPt(2634.29:-4399.25 _clp_cinfo) ) _clpMKSConvert(12.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(2319.29:-4367.25 _clp_cinfo) _clpAdjustPt(2319.29:-4399.25 _clp_cinfo) ) _clpMKSConvert(12.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(2319.29:-4297.25 _clp_cinfo) _clpAdjustPt(2319.29:-4329.25 _clp_cinfo) ) _clpMKSConvert(12.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(2294.29:-4807.25 _clp_cinfo) _clpAdjustPt(2294.29:-4839.25 _clp_cinfo) ) _clpMKSConvert(12.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(2599.29:-4807.25 _clp_cinfo) _clpAdjustPt(2599.29:-4839.25 _clp_cinfo) ) _clpMKSConvert(12.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(2024.29:-1184.25 _clp_cinfo) _clpAdjustPt(2024.29:-1152.25 _clp_cinfo) ) _clpMKSConvert(12.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(3985.29:-3181 _clp_cinfo) _clpAdjustPt(3985.29:-3149 _clp_cinfo) ) _clpMKSConvert(12.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(3985.29:-2836 _clp_cinfo) _clpAdjustPt(3985.29:-2804 _clp_cinfo) ) _clpMKSConvert(12.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(3985.29:-2238 _clp_cinfo) _clpAdjustPt(3985.29:-2206 _clp_cinfo) ) _clpMKSConvert(12.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(3985.29:-3374 _clp_cinfo) _clpAdjustPt(3985.29:-3406 _clp_cinfo) ) _clpMKSConvert(12.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(4675.88:-6601 _clp_cinfo) _clpAdjustPt(4675.88:-6569 _clp_cinfo) ) _clpMKSConvert(12.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(4845.88:-6569 _clp_cinfo) _clpAdjustPt(4845.88:-6601 _clp_cinfo) ) _clpMKSConvert(12.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(2489.29:-4329.25 _clp_cinfo) _clpAdjustPt(2489.29:-4297.25 _clp_cinfo) ) _clpMKSConvert(12.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(2634.29:-4437.25 _clp_cinfo) _clpAdjustPt(2634.29:-4469.25 _clp_cinfo) ) _clpMKSConvert(12.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(2024.29:-1246 _clp_cinfo) _clpAdjustPt(2024.29:-1214 _clp_cinfo) ) _clpMKSConvert(12.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(2031.88:-2275 _clp_cinfo) _clpAdjustPt(1999.88:-2275 _clp_cinfo) ) _clpMKSConvert(12.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(2290.29:-2870 _clp_cinfo) _clpAdjustPt(2258.29:-2870 _clp_cinfo) ) _clpMKSConvert(12.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(2420.29:-2870 _clp_cinfo) _clpAdjustPt(2388.29:-2870 _clp_cinfo) ) _clpMKSConvert(12.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(2355.29:-2870 _clp_cinfo) _clpAdjustPt(2323.29:-2870 _clp_cinfo) ) _clpMKSConvert(12.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(3645.29:-2130 _clp_cinfo) _clpAdjustPt(3613.29:-2130 _clp_cinfo) ) _clpMKSConvert(12.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(3645.29:-3145 _clp_cinfo) _clpAdjustPt(3613.29:-3145 _clp_cinfo) ) _clpMKSConvert(12.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(4460.29:-2835 _clp_cinfo) _clpAdjustPt(4428.29:-2835 _clp_cinfo) ) _clpMKSConvert(12.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(4428.29:-3490 _clp_cinfo) _clpAdjustPt(4460.29:-3490 _clp_cinfo) ) _clpMKSConvert(12.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(5120.29:-3290 _clp_cinfo) _clpAdjustPt(5088.29:-3290 _clp_cinfo) ) _clpMKSConvert(12.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(4428.29:-5110 _clp_cinfo) _clpAdjustPt(4460.29:-5110 _clp_cinfo) ) _clpMKSConvert(12.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(2319.29:-4437.25 _clp_cinfo) _clpAdjustPt(2319.29:-4469.25 _clp_cinfo) ) _clpMKSConvert(12.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(2421.88:-2275 _clp_cinfo) _clpAdjustPt(2389.88:-2275 _clp_cinfo) ) _clpMKSConvert(12.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(2356.88:-2275 _clp_cinfo) _clpAdjustPt(2324.88:-2275 _clp_cinfo) ) _clpMKSConvert(12.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(2291.88:-2275 _clp_cinfo) _clpAdjustPt(2259.88:-2275 _clp_cinfo) ) _clpMKSConvert(12.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(2226.88:-2275 _clp_cinfo) _clpAdjustPt(2194.88:-2275 _clp_cinfo) ) _clpMKSConvert(12.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(2161.88:-2275 _clp_cinfo) _clpAdjustPt(2129.88:-2275 _clp_cinfo) ) _clpMKSConvert(12.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(2096.88:-2275 _clp_cinfo) _clpAdjustPt(2064.88:-2275 _clp_cinfo) ) _clpMKSConvert(12.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(1966.88:-2275 _clp_cinfo) _clpAdjustPt(1934.88:-2275 _clp_cinfo) ) _clpMKSConvert(12.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(2226.88:-2750 _clp_cinfo) _clpAdjustPt(2194.88:-2750 _clp_cinfo) ) _clpMKSConvert(12.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(2161.88:-2750 _clp_cinfo) _clpAdjustPt(2129.88:-2750 _clp_cinfo) ) _clpMKSConvert(12.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(2096.88:-2750 _clp_cinfo) _clpAdjustPt(2064.88:-2750 _clp_cinfo) ) _clpMKSConvert(12.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(1966.88:-2510 _clp_cinfo) _clpAdjustPt(1934.88:-2510 _clp_cinfo) ) _clpMKSConvert(12.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(2031.88:-2510 _clp_cinfo) _clpAdjustPt(1999.88:-2510 _clp_cinfo) ) _clpMKSConvert(12.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(2096.88:-2510 _clp_cinfo) _clpAdjustPt(2064.88:-2510 _clp_cinfo) ) _clpMKSConvert(12.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(2161.88:-2510 _clp_cinfo) _clpAdjustPt(2129.88:-2510 _clp_cinfo) ) _clpMKSConvert(12.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(2226.88:-2510 _clp_cinfo) _clpAdjustPt(2194.88:-2510 _clp_cinfo) ) _clpMKSConvert(12.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(2291.88:-2510 _clp_cinfo) _clpAdjustPt(2259.88:-2510 _clp_cinfo) ) _clpMKSConvert(12.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(2356.88:-2510 _clp_cinfo) _clpAdjustPt(2324.88:-2510 _clp_cinfo) ) _clpMKSConvert(12.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(2421.88:-2510 _clp_cinfo) _clpAdjustPt(2389.88:-2510 _clp_cinfo) ) _clpMKSConvert(12.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(2161.88:-2990 _clp_cinfo) _clpAdjustPt(2129.88:-2990 _clp_cinfo) ) _clpMKSConvert(12.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(2096.88:-2990 _clp_cinfo) _clpAdjustPt(2064.88:-2990 _clp_cinfo) ) _clpMKSConvert(12.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(2031.88:-2990 _clp_cinfo) _clpAdjustPt(1999.88:-2990 _clp_cinfo) ) _clpMKSConvert(12.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(1966.88:-2990 _clp_cinfo) _clpAdjustPt(1934.88:-2990 _clp_cinfo) ) _clpMKSConvert(12.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(2421.88:-2990 _clp_cinfo) _clpAdjustPt(2389.88:-2990 _clp_cinfo) ) _clpMKSConvert(12.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(2356.88:-2990 _clp_cinfo) _clpAdjustPt(2324.88:-2990 _clp_cinfo) ) _clpMKSConvert(12.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(2291.88:-2990 _clp_cinfo) _clpAdjustPt(2259.88:-2990 _clp_cinfo) ) _clpMKSConvert(12.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(2226.88:-2990 _clp_cinfo) _clpAdjustPt(2194.88:-2990 _clp_cinfo) ) _clpMKSConvert(12.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(4941.88:-5335 _clp_cinfo) _clpAdjustPt(4909.88:-5335 _clp_cinfo) ) _clpMKSConvert(12.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(5001.88:-5335 _clp_cinfo) _clpAdjustPt(4969.88:-5335 _clp_cinfo) ) _clpMKSConvert(12.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(3259.29:-5021 _clp_cinfo) _clpAdjustPt(3259.29:-4989 _clp_cinfo) ) _clpMKSConvert(12.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-220.71:-3668.25 _clp_cinfo) _clpAdjustPt(-205.71:-3683.25 _clp_cinfo) ) _clpMKSConvert(5.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-220.71:-3568.25 _clp_cinfo) _clpAdjustPt(-220.71:-3668.25 _clp_cinfo) ) _clpMKSConvert(5.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-205.71:-3553.25 _clp_cinfo) _clpAdjustPt(-220.71:-3568.25 _clp_cinfo) ) _clpMKSConvert(5.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-205.71:-3553.25 _clp_cinfo) _clpAdjustPt(-165.71:-3553.25 _clp_cinfo) ) _clpMKSConvert(5.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-165.71:-3553.25 _clp_cinfo) _clpAdjustPt(-150.71:-3568.25 _clp_cinfo) ) _clpMKSConvert(5.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

printf(" 50 percent completed")
newline()

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-150.71:-3568.25 _clp_cinfo) _clpAdjustPt(-150.71:-3668.25 _clp_cinfo) ) _clpMKSConvert(5.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-150.71:-3668.25 _clp_cinfo) _clpAdjustPt(-165.71:-3683.25 _clp_cinfo) ) _clpMKSConvert(5.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-205.71:-3683.25 _clp_cinfo) _clpAdjustPt(-165.71:-3683.25 _clp_cinfo) ) _clpMKSConvert(5.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-185.71:-3608.25 _clp_cinfo) _clpAdjustPt(-185.71:-3613.25 _clp_cinfo) ) _clpMKSConvert(5.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-185.71:-3623.25 _clp_cinfo) _clpAdjustPt(-185.71:-3628.25 _clp_cinfo) ) _clpMKSConvert(5.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-205.71:-3613.25 _clp_cinfo) _clpAdjustPt(-165.71:-3613.25 _clp_cinfo) ) _clpMKSConvert(5.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-205.71:-3623.25 _clp_cinfo) _clpAdjustPt(-165.71:-3623.25 _clp_cinfo) ) _clpMKSConvert(5.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-220.71:-3043.25 _clp_cinfo) _clpAdjustPt(-205.71:-3058.25 _clp_cinfo) ) _clpMKSConvert(5.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-220.71:-2943.25 _clp_cinfo) _clpAdjustPt(-220.71:-3043.25 _clp_cinfo) ) _clpMKSConvert(5.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-205.71:-2928.25 _clp_cinfo) _clpAdjustPt(-220.71:-2943.25 _clp_cinfo) ) _clpMKSConvert(5.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-205.71:-2928.25 _clp_cinfo) _clpAdjustPt(-165.71:-2928.25 _clp_cinfo) ) _clpMKSConvert(5.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-165.71:-2928.25 _clp_cinfo) _clpAdjustPt(-150.71:-2943.25 _clp_cinfo) ) _clpMKSConvert(5.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-150.71:-2943.25 _clp_cinfo) _clpAdjustPt(-150.71:-3043.25 _clp_cinfo) ) _clpMKSConvert(5.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-150.71:-3043.25 _clp_cinfo) _clpAdjustPt(-165.71:-3058.25 _clp_cinfo) ) _clpMKSConvert(5.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-205.71:-3058.25 _clp_cinfo) _clpAdjustPt(-165.71:-3058.25 _clp_cinfo) ) _clpMKSConvert(5.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-185.71:-2983.25 _clp_cinfo) _clpAdjustPt(-185.71:-2988.25 _clp_cinfo) ) _clpMKSConvert(5.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-185.71:-2998.25 _clp_cinfo) _clpAdjustPt(-185.71:-3003.25 _clp_cinfo) ) _clpMKSConvert(5.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-205.71:-2988.25 _clp_cinfo) _clpAdjustPt(-165.71:-2988.25 _clp_cinfo) ) _clpMKSConvert(5.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-205.71:-2998.25 _clp_cinfo) _clpAdjustPt(-165.71:-2998.25 _clp_cinfo) ) _clpMKSConvert(5.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-220.71:-2418.25 _clp_cinfo) _clpAdjustPt(-205.71:-2433.25 _clp_cinfo) ) _clpMKSConvert(5.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-220.71:-2318.25 _clp_cinfo) _clpAdjustPt(-220.71:-2418.25 _clp_cinfo) ) _clpMKSConvert(5.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-205.71:-2303.25 _clp_cinfo) _clpAdjustPt(-220.71:-2318.25 _clp_cinfo) ) _clpMKSConvert(5.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-205.71:-2303.25 _clp_cinfo) _clpAdjustPt(-165.71:-2303.25 _clp_cinfo) ) _clpMKSConvert(5.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-165.71:-2303.25 _clp_cinfo) _clpAdjustPt(-150.71:-2318.25 _clp_cinfo) ) _clpMKSConvert(5.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-150.71:-2318.25 _clp_cinfo) _clpAdjustPt(-150.71:-2418.25 _clp_cinfo) ) _clpMKSConvert(5.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-150.71:-2418.25 _clp_cinfo) _clpAdjustPt(-165.71:-2433.25 _clp_cinfo) ) _clpMKSConvert(5.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-205.71:-2433.25 _clp_cinfo) _clpAdjustPt(-165.71:-2433.25 _clp_cinfo) ) _clpMKSConvert(5.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-185.71:-2358.25 _clp_cinfo) _clpAdjustPt(-185.71:-2363.25 _clp_cinfo) ) _clpMKSConvert(5.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-185.71:-2373.25 _clp_cinfo) _clpAdjustPt(-185.71:-2378.25 _clp_cinfo) ) _clpMKSConvert(5.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-205.71:-2363.25 _clp_cinfo) _clpAdjustPt(-165.71:-2363.25 _clp_cinfo) ) _clpMKSConvert(5.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-205.71:-2373.25 _clp_cinfo) _clpAdjustPt(-165.71:-2373.25 _clp_cinfo) ) _clpMKSConvert(5.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-220.71:-1793.25 _clp_cinfo) _clpAdjustPt(-205.71:-1808.25 _clp_cinfo) ) _clpMKSConvert(5.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-220.71:-1693.25 _clp_cinfo) _clpAdjustPt(-220.71:-1793.25 _clp_cinfo) ) _clpMKSConvert(5.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-205.71:-1678.25 _clp_cinfo) _clpAdjustPt(-220.71:-1693.25 _clp_cinfo) ) _clpMKSConvert(5.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-205.71:-1678.25 _clp_cinfo) _clpAdjustPt(-165.71:-1678.25 _clp_cinfo) ) _clpMKSConvert(5.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-165.71:-1678.25 _clp_cinfo) _clpAdjustPt(-150.71:-1693.25 _clp_cinfo) ) _clpMKSConvert(5.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-150.71:-1693.25 _clp_cinfo) _clpAdjustPt(-150.71:-1793.25 _clp_cinfo) ) _clpMKSConvert(5.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-150.71:-1793.25 _clp_cinfo) _clpAdjustPt(-165.71:-1808.25 _clp_cinfo) ) _clpMKSConvert(5.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-205.71:-1808.25 _clp_cinfo) _clpAdjustPt(-165.71:-1808.25 _clp_cinfo) ) _clpMKSConvert(5.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-185.71:-1733.25 _clp_cinfo) _clpAdjustPt(-185.71:-1738.25 _clp_cinfo) ) _clpMKSConvert(5.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-185.71:-1748.25 _clp_cinfo) _clpAdjustPt(-185.71:-1753.25 _clp_cinfo) ) _clpMKSConvert(5.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-205.71:-1738.25 _clp_cinfo) _clpAdjustPt(-165.71:-1738.25 _clp_cinfo) ) _clpMKSConvert(5.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-205.71:-1748.25 _clp_cinfo) _clpAdjustPt(-165.71:-1748.25 _clp_cinfo) ) _clpMKSConvert(5.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(2112.52:28.80000000000018 _clp_cinfo) _clpAdjustPt(2097.52:43.80000000000018 _clp_cinfo) ) _clpMKSConvert(5.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(2112.52:-71.19999999999982 _clp_cinfo) _clpAdjustPt(2112.52:28.80000000000018 _clp_cinfo) ) _clpMKSConvert(5.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(2097.52:-86.19999999999982 _clp_cinfo) _clpAdjustPt(2112.52:-71.19999999999982 _clp_cinfo) ) _clpMKSConvert(5.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(2097.52:-86.19999999999982 _clp_cinfo) _clpAdjustPt(2057.52:-86.19999999999982 _clp_cinfo) ) _clpMKSConvert(5.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(2057.52:-86.19999999999982 _clp_cinfo) _clpAdjustPt(2042.52:-71.19999999999982 _clp_cinfo) ) _clpMKSConvert(5.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(2042.52:-71.19999999999982 _clp_cinfo) _clpAdjustPt(2042.52:28.80000000000018 _clp_cinfo) ) _clpMKSConvert(5.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(2042.52:28.80000000000018 _clp_cinfo) _clpAdjustPt(2057.52:43.80000000000018 _clp_cinfo) ) _clpMKSConvert(5.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(2097.52:43.80000000000018 _clp_cinfo) _clpAdjustPt(2057.52:43.80000000000018 _clp_cinfo) ) _clpMKSConvert(5.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(2077.52:-31.19999999999982 _clp_cinfo) _clpAdjustPt(2077.52:-26.19999999999982 _clp_cinfo) ) _clpMKSConvert(5.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(2077.52:-16.19999999999982 _clp_cinfo) _clpAdjustPt(2077.52:-11.19999999999982 _clp_cinfo) ) _clpMKSConvert(5.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(2097.52:-26.19999999999982 _clp_cinfo) _clpAdjustPt(2057.52:-26.19999999999982 _clp_cinfo) ) _clpMKSConvert(5.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(2097.52:-16.19999999999982 _clp_cinfo) _clpAdjustPt(2057.52:-16.19999999999982 _clp_cinfo) ) _clpMKSConvert(5.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(2742.52:28.80000000000018 _clp_cinfo) _clpAdjustPt(2727.52:43.80000000000018 _clp_cinfo) ) _clpMKSConvert(5.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(2742.52:-71.19999999999982 _clp_cinfo) _clpAdjustPt(2742.52:28.80000000000018 _clp_cinfo) ) _clpMKSConvert(5.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(2727.52:-86.19999999999982 _clp_cinfo) _clpAdjustPt(2742.52:-71.19999999999982 _clp_cinfo) ) _clpMKSConvert(5.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(2727.52:-86.19999999999982 _clp_cinfo) _clpAdjustPt(2687.52:-86.19999999999982 _clp_cinfo) ) _clpMKSConvert(5.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(2687.52:-86.19999999999982 _clp_cinfo) _clpAdjustPt(2672.52:-71.19999999999982 _clp_cinfo) ) _clpMKSConvert(5.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(2672.52:-71.19999999999982 _clp_cinfo) _clpAdjustPt(2672.52:28.80000000000018 _clp_cinfo) ) _clpMKSConvert(5.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(2672.52:28.80000000000018 _clp_cinfo) _clpAdjustPt(2687.52:43.80000000000018 _clp_cinfo) ) _clpMKSConvert(5.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(2727.52:43.80000000000018 _clp_cinfo) _clpAdjustPt(2687.52:43.80000000000018 _clp_cinfo) ) _clpMKSConvert(5.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(2707.52:-31.19999999999982 _clp_cinfo) _clpAdjustPt(2707.52:-26.19999999999982 _clp_cinfo) ) _clpMKSConvert(5.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(2707.52:-16.19999999999982 _clp_cinfo) _clpAdjustPt(2707.52:-11.19999999999982 _clp_cinfo) ) _clpMKSConvert(5.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(2727.52:-26.19999999999982 _clp_cinfo) _clpAdjustPt(2687.52:-26.19999999999982 _clp_cinfo) ) _clpMKSConvert(5.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(2727.52:-16.19999999999982 _clp_cinfo) _clpAdjustPt(2687.52:-16.19999999999982 _clp_cinfo) ) _clpMKSConvert(5.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(4879.29:-1235 _clp_cinfo) _clpAdjustPt(4894.29:-1250 _clp_cinfo) ) _clpMKSConvert(5.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(4879.29:-1135 _clp_cinfo) _clpAdjustPt(4879.29:-1235 _clp_cinfo) ) _clpMKSConvert(5.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(4894.29:-1120 _clp_cinfo) _clpAdjustPt(4879.29:-1135 _clp_cinfo) ) _clpMKSConvert(5.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(4894.29:-1120 _clp_cinfo) _clpAdjustPt(4934.29:-1120 _clp_cinfo) ) _clpMKSConvert(5.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(4934.29:-1120 _clp_cinfo) _clpAdjustPt(4949.29:-1135 _clp_cinfo) ) _clpMKSConvert(5.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(4949.29:-1135 _clp_cinfo) _clpAdjustPt(4949.29:-1235 _clp_cinfo) ) _clpMKSConvert(5.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(4949.29:-1235 _clp_cinfo) _clpAdjustPt(4934.29:-1250 _clp_cinfo) ) _clpMKSConvert(5.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(4894.29:-1250 _clp_cinfo) _clpAdjustPt(4934.29:-1250 _clp_cinfo) ) _clpMKSConvert(5.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(4914.29:-1175 _clp_cinfo) _clpAdjustPt(4914.29:-1180 _clp_cinfo) ) _clpMKSConvert(5.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(4914.29:-1190 _clp_cinfo) _clpAdjustPt(4914.29:-1195 _clp_cinfo) ) _clpMKSConvert(5.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(4894.29:-1180 _clp_cinfo) _clpAdjustPt(4934.29:-1180 _clp_cinfo) ) _clpMKSConvert(5.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(4894.29:-1190 _clp_cinfo) _clpAdjustPt(4934.29:-1190 _clp_cinfo) ) _clpMKSConvert(5.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(4.289999999999964:-3608.25 _clp_cinfo) _clpAdjustPt(4.289999999999964:-3578.25 _clp_cinfo) ) _clpMKSConvert(12.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(2584.29:-593.25 _clp_cinfo) _clpAdjustPt(2554.29:-593.25 _clp_cinfo) ) _clpMKSConvert(12.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(244.29:-2683.25 _clp_cinfo) _clpAdjustPt(244.29:-2653.25 _clp_cinfo) ) _clpMKSConvert(12.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(244.29:-2058.25 _clp_cinfo) _clpAdjustPt(244.29:-2028.25 _clp_cinfo) ) _clpMKSConvert(12.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(244.29:-1433.25 _clp_cinfo) _clpAdjustPt(244.29:-1403.25 _clp_cinfo) ) _clpMKSConvert(12.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(2764.29:-528.25 _clp_cinfo) _clpAdjustPt(2794.29:-528.25 _clp_cinfo) ) _clpMKSConvert(12.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(599.29:-798.25 _clp_cinfo) _clpAdjustPt(599.29:-768.25 _clp_cinfo) ) _clpMKSConvert(12.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(5159.29:-3130 _clp_cinfo) _clpAdjustPt(5129.29:-3130 _clp_cinfo) ) _clpMKSConvert(12.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(4909.29:-1355 _clp_cinfo) _clpAdjustPt(4939.29:-1355 _clp_cinfo) ) _clpMKSConvert(12.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(4899.29:-960 _clp_cinfo) _clpAdjustPt(4899.29:-930 _clp_cinfo) ) _clpMKSConvert(12.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(4934.29:-860 _clp_cinfo) _clpAdjustPt(4964.29:-860 _clp_cinfo) ) _clpMKSConvert(12.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(244.29:-1463.25 _clp_cinfo) _clpAdjustPt(244.29:-1493.25 _clp_cinfo) ) _clpMKSConvert(12.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(309.29:-1613.25 _clp_cinfo) _clpAdjustPt(309.29:-1643.25 _clp_cinfo) ) _clpMKSConvert(12.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(2104.29:-528.25 _clp_cinfo) _clpAdjustPt(2074.29:-528.25 _clp_cinfo) ) _clpMKSConvert(12.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(1954.29:-593.25 _clp_cinfo) _clpAdjustPt(1924.29:-593.25 _clp_cinfo) ) _clpMKSConvert(12.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-90.71000000000004:-3985 _clp_cinfo) _clpAdjustPt(-120.71:-3985 _clp_cinfo) ) _clpMKSConvert(12.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(69.28999999999996:-3985 _clp_cinfo) _clpAdjustPt(39.28999999999996:-3985 _clp_cinfo) ) _clpMKSConvert(12.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(309.29:-2863.25 _clp_cinfo) _clpAdjustPt(309.29:-2893.25 _clp_cinfo) ) _clpMKSConvert(12.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(309.29:-2238.25 _clp_cinfo) _clpAdjustPt(309.29:-2268.25 _clp_cinfo) ) _clpMKSConvert(12.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(1864.29:-308.25 _clp_cinfo) _clpAdjustPt(1834.29:-308.25 _clp_cinfo) ) _clpMKSConvert(12.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(1554.29:-223.25 _clp_cinfo) _clpAdjustPt(1524.29:-223.25 _clp_cinfo) ) _clpMKSConvert(12.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(2494.29:-308.25 _clp_cinfo) _clpAdjustPt(2464.29:-308.25 _clp_cinfo) ) _clpMKSConvert(12.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(2734.29:-528.25 _clp_cinfo) _clpAdjustPt(2704.29:-528.25 _clp_cinfo) ) _clpMKSConvert(12.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(3359.29:-528.25 _clp_cinfo) _clpAdjustPt(3329.29:-528.25 _clp_cinfo) ) _clpMKSConvert(12.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

printf(" 60 percent completed")
newline()

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(3209.29:-593.25 _clp_cinfo) _clpAdjustPt(3179.29:-593.25 _clp_cinfo) ) _clpMKSConvert(12.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(589.29:-343.25 _clp_cinfo) _clpAdjustPt(619.29:-343.25 _clp_cinfo) ) _clpMKSConvert(12.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(3389.29:-528.25 _clp_cinfo) _clpAdjustPt(3419.29:-528.25 _clp_cinfo) ) _clpMKSConvert(12.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(2184.29:-223.25 _clp_cinfo) _clpAdjustPt(2154.29:-223.25 _clp_cinfo) ) _clpMKSConvert(12.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(3119.29:-308.25 _clp_cinfo) _clpAdjustPt(3089.29:-308.25 _clp_cinfo) ) _clpMKSConvert(12.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(2809.29:-223.25 _clp_cinfo) _clpAdjustPt(2779.29:-223.25 _clp_cinfo) ) _clpMKSConvert(12.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(2134.29:-528.25 _clp_cinfo) _clpAdjustPt(2164.29:-528.25 _clp_cinfo) ) _clpMKSConvert(12.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-123.21:-2387 _clp_cinfo) _clpAdjustPt(-123.21:-2524.5 _clp_cinfo) ) _clpMKSConvert(6.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(171.79:-2387 _clp_cinfo) _clpAdjustPt(-123.21:-2387 _clp_cinfo) ) _clpMKSConvert(6.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(171.79:-2387 _clp_cinfo) _clpAdjustPt(171.79:-2452 _clp_cinfo) ) _clpMKSConvert(6.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(171.79:-2452 _clp_cinfo) _clpAdjustPt(156.79:-2452 _clp_cinfo) ) _clpMKSConvert(6.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(156.79:-2452 _clp_cinfo) _clpAdjustPt(156.79:-2547 _clp_cinfo) ) _clpMKSConvert(6.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(171.79:-2547 _clp_cinfo) _clpAdjustPt(156.79:-2547 _clp_cinfo) ) _clpMKSConvert(6.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(171.79:-2547 _clp_cinfo) _clpAdjustPt(171.79:-2609.5 _clp_cinfo) ) _clpMKSConvert(6.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(171.79:-2609.5 _clp_cinfo) _clpAdjustPt(-123.21:-2609.5 _clp_cinfo) ) _clpMKSConvert(6.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-123.21:-2524.5 _clp_cinfo) _clpAdjustPt(-123.21:-2609.5 _clp_cinfo) ) _clpMKSConvert(6.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-123.21:-1762 _clp_cinfo) _clpAdjustPt(-123.21:-1899.5 _clp_cinfo) ) _clpMKSConvert(6.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(171.79:-1762 _clp_cinfo) _clpAdjustPt(-123.21:-1762 _clp_cinfo) ) _clpMKSConvert(6.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(171.79:-1762 _clp_cinfo) _clpAdjustPt(171.79:-1827 _clp_cinfo) ) _clpMKSConvert(6.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(171.79:-1827 _clp_cinfo) _clpAdjustPt(156.79:-1827 _clp_cinfo) ) _clpMKSConvert(6.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(156.79:-1827 _clp_cinfo) _clpAdjustPt(156.79:-1922 _clp_cinfo) ) _clpMKSConvert(6.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(171.79:-1922 _clp_cinfo) _clpAdjustPt(156.79:-1922 _clp_cinfo) ) _clpMKSConvert(6.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(171.79:-1922 _clp_cinfo) _clpAdjustPt(171.79:-1984.5 _clp_cinfo) ) _clpMKSConvert(6.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(171.79:-1984.5 _clp_cinfo) _clpAdjustPt(-123.21:-1984.5 _clp_cinfo) ) _clpMKSConvert(6.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-123.21:-1899.5 _clp_cinfo) _clpAdjustPt(-123.21:-1984.5 _clp_cinfo) ) _clpMKSConvert(6.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-123.21:-3637 _clp_cinfo) _clpAdjustPt(-123.21:-3774.5 _clp_cinfo) ) _clpMKSConvert(6.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(171.79:-3637 _clp_cinfo) _clpAdjustPt(-123.21:-3637 _clp_cinfo) ) _clpMKSConvert(6.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(171.79:-3637 _clp_cinfo) _clpAdjustPt(171.79:-3702 _clp_cinfo) ) _clpMKSConvert(6.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(171.79:-3702 _clp_cinfo) _clpAdjustPt(156.79:-3702 _clp_cinfo) ) _clpMKSConvert(6.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(156.79:-3702 _clp_cinfo) _clpAdjustPt(156.79:-3797 _clp_cinfo) ) _clpMKSConvert(6.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(171.79:-3797 _clp_cinfo) _clpAdjustPt(156.79:-3797 _clp_cinfo) ) _clpMKSConvert(6.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(171.79:-3797 _clp_cinfo) _clpAdjustPt(171.79:-3859.5 _clp_cinfo) ) _clpMKSConvert(6.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(171.79:-3859.5 _clp_cinfo) _clpAdjustPt(-123.21:-3859.5 _clp_cinfo) ) _clpMKSConvert(6.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-123.21:-3774.5 _clp_cinfo) _clpAdjustPt(-123.21:-3859.5 _clp_cinfo) ) _clpMKSConvert(6.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(4886.79:-1423.75 _clp_cinfo) _clpAdjustPt(4886.79:-1561.25 _clp_cinfo) ) _clpMKSConvert(6.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(5181.79:-1423.75 _clp_cinfo) _clpAdjustPt(4886.79:-1423.75 _clp_cinfo) ) _clpMKSConvert(6.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(5181.79:-1423.75 _clp_cinfo) _clpAdjustPt(5181.79:-1488.75 _clp_cinfo) ) _clpMKSConvert(6.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(5181.79:-1488.75 _clp_cinfo) _clpAdjustPt(5166.79:-1488.75 _clp_cinfo) ) _clpMKSConvert(6.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(5166.79:-1488.75 _clp_cinfo) _clpAdjustPt(5166.79:-1583.75 _clp_cinfo) ) _clpMKSConvert(6.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(5181.79:-1583.75 _clp_cinfo) _clpAdjustPt(5166.79:-1583.75 _clp_cinfo) ) _clpMKSConvert(6.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(5181.79:-1583.75 _clp_cinfo) _clpAdjustPt(5181.79:-1646.25 _clp_cinfo) ) _clpMKSConvert(6.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(5181.79:-1646.25 _clp_cinfo) _clpAdjustPt(4886.79:-1646.25 _clp_cinfo) ) _clpMKSConvert(6.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(4886.79:-1561.25 _clp_cinfo) _clpAdjustPt(4886.79:-1646.25 _clp_cinfo) ) _clpMKSConvert(6.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(5259.63:-6647.5 _clp_cinfo) _clpAdjustPt(5259.63:-6942.5 _clp_cinfo) ) _clpMKSConvert(6.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(5259.63:-6647.5 _clp_cinfo) _clpAdjustPt(5324.63:-6647.5 _clp_cinfo) ) _clpMKSConvert(6.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(5324.63:-6647.5 _clp_cinfo) _clpAdjustPt(5324.63:-6662.5 _clp_cinfo) ) _clpMKSConvert(6.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(5419.63:-6647.5 _clp_cinfo) _clpAdjustPt(5419.63:-6662.5 _clp_cinfo) ) _clpMKSConvert(6.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(5419.63:-6647.5 _clp_cinfo) _clpAdjustPt(5482.13:-6647.5 _clp_cinfo) ) _clpMKSConvert(6.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(5482.13:-6647.5 _clp_cinfo) _clpAdjustPt(5482.13:-6942.5 _clp_cinfo) ) _clpMKSConvert(6.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(171.79:-2924.5 _clp_cinfo) _clpAdjustPt(171.79:-2787 _clp_cinfo) ) _clpMKSConvert(6.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-123.21:-2924.5 _clp_cinfo) _clpAdjustPt(171.79:-2924.5 _clp_cinfo) ) _clpMKSConvert(6.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-123.21:-2924.5 _clp_cinfo) _clpAdjustPt(-123.21:-2859.5 _clp_cinfo) ) _clpMKSConvert(6.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-123.21:-2859.5 _clp_cinfo) _clpAdjustPt(-108.21:-2859.5 _clp_cinfo) ) _clpMKSConvert(6.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-108.21:-2859.5 _clp_cinfo) _clpAdjustPt(-108.21:-2764.5 _clp_cinfo) ) _clpMKSConvert(6.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-123.21:-2764.5 _clp_cinfo) _clpAdjustPt(-108.21:-2764.5 _clp_cinfo) ) _clpMKSConvert(6.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-123.21:-2764.5 _clp_cinfo) _clpAdjustPt(-123.21:-2702 _clp_cinfo) ) _clpMKSConvert(6.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-123.21:-2702 _clp_cinfo) _clpAdjustPt(171.79:-2702 _clp_cinfo) ) _clpMKSConvert(6.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(171.79:-2787 _clp_cinfo) _clpAdjustPt(171.79:-2702 _clp_cinfo) ) _clpMKSConvert(6.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(171.79:-2299.5 _clp_cinfo) _clpAdjustPt(171.79:-2162 _clp_cinfo) ) _clpMKSConvert(6.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-123.21:-2299.5 _clp_cinfo) _clpAdjustPt(171.79:-2299.5 _clp_cinfo) ) _clpMKSConvert(6.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-123.21:-2299.5 _clp_cinfo) _clpAdjustPt(-123.21:-2234.5 _clp_cinfo) ) _clpMKSConvert(6.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-123.21:-2234.5 _clp_cinfo) _clpAdjustPt(-108.21:-2234.5 _clp_cinfo) ) _clpMKSConvert(6.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-108.21:-2234.5 _clp_cinfo) _clpAdjustPt(-108.21:-2139.5 _clp_cinfo) ) _clpMKSConvert(6.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-123.21:-2139.5 _clp_cinfo) _clpAdjustPt(-108.21:-2139.5 _clp_cinfo) ) _clpMKSConvert(6.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-123.21:-2139.5 _clp_cinfo) _clpAdjustPt(-123.21:-2077 _clp_cinfo) ) _clpMKSConvert(6.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-123.21:-2077 _clp_cinfo) _clpAdjustPt(171.79:-2077 _clp_cinfo) ) _clpMKSConvert(6.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(171.79:-2162 _clp_cinfo) _clpAdjustPt(171.79:-2077 _clp_cinfo) ) _clpMKSConvert(6.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(171.79:-1674.5 _clp_cinfo) _clpAdjustPt(171.79:-1537 _clp_cinfo) ) _clpMKSConvert(6.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-123.21:-1674.5 _clp_cinfo) _clpAdjustPt(171.79:-1674.5 _clp_cinfo) ) _clpMKSConvert(6.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-123.21:-1674.5 _clp_cinfo) _clpAdjustPt(-123.21:-1609.5 _clp_cinfo) ) _clpMKSConvert(6.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-123.21:-1609.5 _clp_cinfo) _clpAdjustPt(-108.21:-1609.5 _clp_cinfo) ) _clpMKSConvert(6.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-108.21:-1609.5 _clp_cinfo) _clpAdjustPt(-108.21:-1514.5 _clp_cinfo) ) _clpMKSConvert(6.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-123.21:-1514.5 _clp_cinfo) _clpAdjustPt(-108.21:-1514.5 _clp_cinfo) ) _clpMKSConvert(6.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-123.21:-1514.5 _clp_cinfo) _clpAdjustPt(-123.21:-1452 _clp_cinfo) ) _clpMKSConvert(6.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-123.21:-1452 _clp_cinfo) _clpAdjustPt(171.79:-1452 _clp_cinfo) ) _clpMKSConvert(6.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(171.79:-1537 _clp_cinfo) _clpAdjustPt(171.79:-1452 _clp_cinfo) ) _clpMKSConvert(6.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(5436.79:-496.25 _clp_cinfo) _clpAdjustPt(5436.79:-358.75 _clp_cinfo) ) _clpMKSConvert(6.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(5141.79:-496.25 _clp_cinfo) _clpAdjustPt(5436.79:-496.25 _clp_cinfo) ) _clpMKSConvert(6.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(5141.79:-496.25 _clp_cinfo) _clpAdjustPt(5141.79:-431.25 _clp_cinfo) ) _clpMKSConvert(6.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(5141.79:-431.25 _clp_cinfo) _clpAdjustPt(5156.79:-431.25 _clp_cinfo) ) _clpMKSConvert(6.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(5156.79:-431.25 _clp_cinfo) _clpAdjustPt(5156.79:-336.25 _clp_cinfo) ) _clpMKSConvert(6.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(5141.79:-336.25 _clp_cinfo) _clpAdjustPt(5156.79:-336.25 _clp_cinfo) ) _clpMKSConvert(6.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(5141.79:-336.25 _clp_cinfo) _clpAdjustPt(5141.79:-273.75 _clp_cinfo) ) _clpMKSConvert(6.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(5141.79:-273.75 _clp_cinfo) _clpAdjustPt(5436.79:-273.75 _clp_cinfo) ) _clpMKSConvert(6.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(5436.79:-358.75 _clp_cinfo) _clpAdjustPt(5436.79:-273.75 _clp_cinfo) ) _clpMKSConvert(6.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(171.79:-3549.5 _clp_cinfo) _clpAdjustPt(171.79:-3412 _clp_cinfo) ) _clpMKSConvert(6.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-123.21:-3549.5 _clp_cinfo) _clpAdjustPt(171.79:-3549.5 _clp_cinfo) ) _clpMKSConvert(6.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-123.21:-3549.5 _clp_cinfo) _clpAdjustPt(-123.21:-3484.5 _clp_cinfo) ) _clpMKSConvert(6.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-123.21:-3484.5 _clp_cinfo) _clpAdjustPt(-108.21:-3484.5 _clp_cinfo) ) _clpMKSConvert(6.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-108.21:-3484.5 _clp_cinfo) _clpAdjustPt(-108.21:-3389.5 _clp_cinfo) ) _clpMKSConvert(6.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-123.21:-3389.5 _clp_cinfo) _clpAdjustPt(-108.21:-3389.5 _clp_cinfo) ) _clpMKSConvert(6.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-123.21:-3389.5 _clp_cinfo) _clpAdjustPt(-123.21:-3327 _clp_cinfo) ) _clpMKSConvert(6.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-123.21:-3327 _clp_cinfo) _clpAdjustPt(171.79:-3327 _clp_cinfo) ) _clpMKSConvert(6.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(171.79:-3412 _clp_cinfo) _clpAdjustPt(171.79:-3327 _clp_cinfo) ) _clpMKSConvert(6.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(2189.29:-4443.25 _clp_cinfo) _clpAdjustPt(2189.29:-4463.25 _clp_cinfo) ) _clpMKSConvert(6.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(3839.29:-6590 _clp_cinfo) _clpAdjustPt(3839.29:-6610 _clp_cinfo) ) _clpMKSConvert(6.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(545.8799999999999:-5840 _clp_cinfo) _clpAdjustPt(525.8799999999999:-5840 _clp_cinfo) ) _clpMKSConvert(6.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(819.29:-5840 _clp_cinfo) _clpAdjustPt(799.29:-5840 _clp_cinfo) ) _clpMKSConvert(6.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(289.29:-2803.25 _clp_cinfo) _clpAdjustPt(269.29:-2803.25 _clp_cinfo) ) _clpMKSConvert(6.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(289.29:-2178.25 _clp_cinfo) _clpAdjustPt(269.29:-2178.25 _clp_cinfo) ) _clpMKSConvert(6.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(1019.29:-373.25 _clp_cinfo) _clpAdjustPt(999.29:-373.25 _clp_cinfo) ) _clpMKSConvert(6.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(819.29:-373.25 _clp_cinfo) _clpAdjustPt(799.29:-373.25 _clp_cinfo) ) _clpMKSConvert(6.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(849.29:-373.25 _clp_cinfo) _clpAdjustPt(869.29:-373.25 _clp_cinfo) ) _clpMKSConvert(6.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

printf(" 70 percent completed")
newline()

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(919.29:-373.25 _clp_cinfo) _clpAdjustPt(899.29:-373.25 _clp_cinfo) ) _clpMKSConvert(6.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(749.29:-373.25 _clp_cinfo) _clpAdjustPt(769.29:-373.25 _clp_cinfo) ) _clpMKSConvert(6.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(719.29:-373.25 _clp_cinfo) _clpAdjustPt(699.29:-373.25 _clp_cinfo) ) _clpMKSConvert(6.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(3269.29:-573.25 _clp_cinfo) _clpAdjustPt(3269.29:-553.25 _clp_cinfo) ) _clpMKSConvert(6.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(3394.29:-683.25 _clp_cinfo) _clpAdjustPt(3414.29:-683.25 _clp_cinfo) ) _clpMKSConvert(6.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(1859.29:-203.25 _clp_cinfo) _clpAdjustPt(1839.29:-203.25 _clp_cinfo) ) _clpMKSConvert(6.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(2489.29:-203.25 _clp_cinfo) _clpAdjustPt(2469.29:-203.25 _clp_cinfo) ) _clpMKSConvert(6.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(3114.29:-203.25 _clp_cinfo) _clpAdjustPt(3094.29:-203.25 _clp_cinfo) ) _clpMKSConvert(6.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(2769.29:-638.25 _clp_cinfo) _clpAdjustPt(2789.29:-638.25 _clp_cinfo) ) _clpMKSConvert(6.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(5269.29:-1255 _clp_cinfo) _clpAdjustPt(5289.29:-1255 _clp_cinfo) ) _clpMKSConvert(6.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(5289.29:-1640 _clp_cinfo) _clpAdjustPt(5269.29:-1640 _clp_cinfo) ) _clpMKSConvert(6.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(4909.29:-845 _clp_cinfo) _clpAdjustPt(4889.29:-845 _clp_cinfo) ) _clpMKSConvert(6.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(4454.29:-4045 _clp_cinfo) _clpAdjustPt(4434.29:-4045 _clp_cinfo) ) _clpMKSConvert(6.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(4454.29:-2455 _clp_cinfo) _clpAdjustPt(4434.29:-2455 _clp_cinfo) ) _clpMKSConvert(6.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(4454.29:-2600 _clp_cinfo) _clpAdjustPt(4434.29:-2600 _clp_cinfo) ) _clpMKSConvert(6.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(4454.29:-2690 _clp_cinfo) _clpAdjustPt(4434.29:-2690 _clp_cinfo) ) _clpMKSConvert(6.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(4434.29:-3275 _clp_cinfo) _clpAdjustPt(4454.29:-3275 _clp_cinfo) ) _clpMKSConvert(6.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(4454.29:-3360 _clp_cinfo) _clpAdjustPt(4434.29:-3360 _clp_cinfo) ) _clpMKSConvert(6.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(4434.29:-2005 _clp_cinfo) _clpAdjustPt(4454.29:-2005 _clp_cinfo) ) _clpMKSConvert(6.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(5159.29:-2955 _clp_cinfo) _clpAdjustPt(5139.29:-2955 _clp_cinfo) ) _clpMKSConvert(6.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(4454.29:-1900 _clp_cinfo) _clpAdjustPt(4434.29:-1900 _clp_cinfo) ) _clpMKSConvert(6.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(4455.29:-4910 _clp_cinfo) _clpAdjustPt(4435.29:-4910 _clp_cinfo) ) _clpMKSConvert(6.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(4869.29:-5000 _clp_cinfo) _clpAdjustPt(4849.29:-5000 _clp_cinfo) ) _clpMKSConvert(6.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(4849.29:-5335 _clp_cinfo) _clpAdjustPt(4869.29:-5335 _clp_cinfo) ) _clpMKSConvert(6.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(194.29:-4270 _clp_cinfo) _clpAdjustPt(214.29:-4270 _clp_cinfo) ) _clpMKSConvert(6.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(14.28999999999996:-3995 _clp_cinfo) _clpAdjustPt(-5.710000000000036:-3995 _clp_cinfo) ) _clpMKSConvert(6.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(2489.29:-4373.25 _clp_cinfo) _clpAdjustPt(2489.29:-4353.25 _clp_cinfo) ) _clpMKSConvert(6.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(4870.88:-4800 _clp_cinfo) _clpAdjustPt(4850.88:-4800 _clp_cinfo) ) _clpMKSConvert(6.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(5124.29:-370 _clp_cinfo) _clpAdjustPt(4864.29:-370 _clp_cinfo) ) _clpMKSConvert(8.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_path = _clpPathStart(list(_clpAdjustPt(5124.29:-370 _clp_cinfo))                  
	_clpMKSConvert(8.000000 _clp_cinfo->t_from_units                  			_clp_cinfo->t_to_units))
_clp_path = _clpPathArcCenter(_clp_path _clpMKSConvert( 8.000000                   _clp_cinfo->t_from_units 
	_clp_cinfo->t_to_units)                   _clpAdjustPt(5124.29:-370 _clp_cinfo) nil
 	_clpAdjustPt(4994.29:-370 _clp_cinfo))
_clp_dbid = _clpDBCreatePath(_clp_path "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = caar(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(5124.29:-5540 _clp_cinfo) _clpAdjustPt(4864.29:-5540 _clp_cinfo) ) _clpMKSConvert(8.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_path = _clpPathStart(list(_clpAdjustPt(5124.29:-5540 _clp_cinfo))                  
	_clpMKSConvert(8.000000 _clp_cinfo->t_from_units                  			_clp_cinfo->t_to_units))
_clp_path = _clpPathArcCenter(_clp_path _clpMKSConvert( 8.000000                   _clp_cinfo->t_from_units 
	_clp_cinfo->t_to_units)                   _clpAdjustPt(5124.29:-5540 _clp_cinfo) nil
 	_clpAdjustPt(4994.29:-5540 _clp_cinfo))
_clp_dbid = _clpDBCreatePath(_clp_path "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = caar(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(5714.29:-370 _clp_cinfo) _clpAdjustPt(5454.29:-370 _clp_cinfo) ) _clpMKSConvert(8.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_path = _clpPathStart(list(_clpAdjustPt(5714.29:-370 _clp_cinfo))                  
	_clpMKSConvert(8.000000 _clp_cinfo->t_from_units                  			_clp_cinfo->t_to_units))
_clp_path = _clpPathArcCenter(_clp_path _clpMKSConvert( 8.000000                   _clp_cinfo->t_from_units 
	_clp_cinfo->t_to_units)                   _clpAdjustPt(5714.29:-370 _clp_cinfo) nil
 	_clpAdjustPt(5584.29:-370 _clp_cinfo))
_clp_dbid = _clpDBCreatePath(_clp_path "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = caar(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(5124.29:-2230 _clp_cinfo) _clpAdjustPt(4864.29:-2230 _clp_cinfo) ) _clpMKSConvert(8.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_path = _clpPathStart(list(_clpAdjustPt(5124.29:-2230 _clp_cinfo))                  
	_clpMKSConvert(8.000000 _clp_cinfo->t_from_units                  			_clp_cinfo->t_to_units))
_clp_path = _clpPathArcCenter(_clp_path _clpMKSConvert( 8.000000                   _clp_cinfo->t_from_units 
	_clp_cinfo->t_to_units)                   _clpAdjustPt(5124.29:-2230 _clp_cinfo) nil
 	_clpAdjustPt(4994.29:-2230 _clp_cinfo))
_clp_dbid = _clpDBCreatePath(_clp_path "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = caar(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(3964.29:-2440 _clp_cinfo) _clpAdjustPt(3704.29:-2440 _clp_cinfo) ) _clpMKSConvert(8.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_path = _clpPathStart(list(_clpAdjustPt(3964.29:-2440 _clp_cinfo))                  
	_clpMKSConvert(8.000000 _clp_cinfo->t_from_units                  			_clp_cinfo->t_to_units))
_clp_path = _clpPathArcCenter(_clp_path _clpMKSConvert( 8.000000                   _clp_cinfo->t_from_units 
	_clp_cinfo->t_to_units)                   _clpAdjustPt(3964.29:-2440 _clp_cinfo) nil
 	_clpAdjustPt(3834.29:-2440 _clp_cinfo))
_clp_dbid = _clpDBCreatePath(_clp_path "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = caar(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(5124.29:-2505 _clp_cinfo) _clpAdjustPt(4864.29:-2505 _clp_cinfo) ) _clpMKSConvert(8.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_path = _clpPathStart(list(_clpAdjustPt(5124.29:-2505 _clp_cinfo))                  
	_clpMKSConvert(8.000000 _clp_cinfo->t_from_units                  			_clp_cinfo->t_to_units))
_clp_path = _clpPathArcCenter(_clp_path _clpMKSConvert( 8.000000                   _clp_cinfo->t_from_units 
	_clp_cinfo->t_to_units)                   _clpAdjustPt(5124.29:-2505 _clp_cinfo) nil
 	_clpAdjustPt(4994.29:-2505 _clp_cinfo))
_clp_dbid = _clpDBCreatePath(_clp_path "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = caar(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-170.61:-3438.25 _clp_cinfo) _clpAdjustPt(-430.61:-3438.25 _clp_cinfo) ) _clpMKSConvert(8.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_path = _clpPathStart(list(_clpAdjustPt(-170.61:-3438.25 _clp_cinfo))                  
	_clpMKSConvert(8.000000 _clp_cinfo->t_from_units                  			_clp_cinfo->t_to_units))
_clp_path = _clpPathArcCenter(_clp_path _clpMKSConvert( 8.000000                   _clp_cinfo->t_from_units 
	_clp_cinfo->t_to_units)                   _clpAdjustPt(-170.61:-3438.25 _clp_cinfo) nil
 	_clpAdjustPt(-300.61:-3438.25 _clp_cinfo))
_clp_dbid = _clpDBCreatePath(_clp_path "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = caar(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(909.29:-3273.25 _clp_cinfo) _clpAdjustPt(649.29:-3273.25 _clp_cinfo) ) _clpMKSConvert(8.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_path = _clpPathStart(list(_clpAdjustPt(909.29:-3273.25 _clp_cinfo))                  
	_clpMKSConvert(8.000000 _clp_cinfo->t_from_units                  			_clp_cinfo->t_to_units))
_clp_path = _clpPathArcCenter(_clp_path _clpMKSConvert( 8.000000                   _clp_cinfo->t_from_units 
	_clp_cinfo->t_to_units)                   _clpAdjustPt(909.29:-3273.25 _clp_cinfo) nil
 	_clpAdjustPt(779.29:-3273.25 _clp_cinfo))
_clp_dbid = _clpDBCreatePath(_clp_path "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = caar(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(909.29:-2998.25 _clp_cinfo) _clpAdjustPt(649.29:-2998.25 _clp_cinfo) ) _clpMKSConvert(8.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_path = _clpPathStart(list(_clpAdjustPt(909.29:-2998.25 _clp_cinfo))                  
	_clpMKSConvert(8.000000 _clp_cinfo->t_from_units                  			_clp_cinfo->t_to_units))
_clp_path = _clpPathArcCenter(_clp_path _clpMKSConvert( 8.000000                   _clp_cinfo->t_from_units 
	_clp_cinfo->t_to_units)                   _clpAdjustPt(909.29:-2998.25 _clp_cinfo) nil
 	_clpAdjustPt(779.29:-2998.25 _clp_cinfo))
_clp_dbid = _clpDBCreatePath(_clp_path "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = caar(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(909.29:-2723.25 _clp_cinfo) _clpAdjustPt(649.29:-2723.25 _clp_cinfo) ) _clpMKSConvert(8.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_path = _clpPathStart(list(_clpAdjustPt(909.29:-2723.25 _clp_cinfo))                  
	_clpMKSConvert(8.000000 _clp_cinfo->t_from_units                  			_clp_cinfo->t_to_units))
_clp_path = _clpPathArcCenter(_clp_path _clpMKSConvert( 8.000000                   _clp_cinfo->t_from_units 
	_clp_cinfo->t_to_units)                   _clpAdjustPt(909.29:-2723.25 _clp_cinfo) nil
 	_clpAdjustPt(779.29:-2723.25 _clp_cinfo))
_clp_dbid = _clpDBCreatePath(_clp_path "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = caar(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(909.29:-2448.25 _clp_cinfo) _clpAdjustPt(649.29:-2448.25 _clp_cinfo) ) _clpMKSConvert(8.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_path = _clpPathStart(list(_clpAdjustPt(909.29:-2448.25 _clp_cinfo))                  
	_clpMKSConvert(8.000000 _clp_cinfo->t_from_units                  			_clp_cinfo->t_to_units))
_clp_path = _clpPathArcCenter(_clp_path _clpMKSConvert( 8.000000                   _clp_cinfo->t_from_units 
	_clp_cinfo->t_to_units)                   _clpAdjustPt(909.29:-2448.25 _clp_cinfo) nil
 	_clpAdjustPt(779.29:-2448.25 _clp_cinfo))
_clp_dbid = _clpDBCreatePath(_clp_path "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = caar(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(909.29:-2173.25 _clp_cinfo) _clpAdjustPt(649.29:-2173.25 _clp_cinfo) ) _clpMKSConvert(8.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_path = _clpPathStart(list(_clpAdjustPt(909.29:-2173.25 _clp_cinfo))                  
	_clpMKSConvert(8.000000 _clp_cinfo->t_from_units                  			_clp_cinfo->t_to_units))
_clp_path = _clpPathArcCenter(_clp_path _clpMKSConvert( 8.000000                   _clp_cinfo->t_from_units 
	_clp_cinfo->t_to_units)                   _clpAdjustPt(909.29:-2173.25 _clp_cinfo) nil
 	_clpAdjustPt(779.29:-2173.25 _clp_cinfo))
_clp_dbid = _clpDBCreatePath(_clp_path "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = caar(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(909.29:-1898.25 _clp_cinfo) _clpAdjustPt(649.29:-1898.25 _clp_cinfo) ) _clpMKSConvert(8.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_path = _clpPathStart(list(_clpAdjustPt(909.29:-1898.25 _clp_cinfo))                  
	_clpMKSConvert(8.000000 _clp_cinfo->t_from_units                  			_clp_cinfo->t_to_units))
_clp_path = _clpPathArcCenter(_clp_path _clpMKSConvert( 8.000000                   _clp_cinfo->t_from_units 
	_clp_cinfo->t_to_units)                   _clpAdjustPt(909.29:-1898.25 _clp_cinfo) nil
 	_clpAdjustPt(779.29:-1898.25 _clp_cinfo))
_clp_dbid = _clpDBCreatePath(_clp_path "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = caar(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(909.29:-3548.25 _clp_cinfo) _clpAdjustPt(649.29:-3548.25 _clp_cinfo) ) _clpMKSConvert(8.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_path = _clpPathStart(list(_clpAdjustPt(909.29:-3548.25 _clp_cinfo))                  
	_clpMKSConvert(8.000000 _clp_cinfo->t_from_units                  			_clp_cinfo->t_to_units))
_clp_path = _clpPathArcCenter(_clp_path _clpMKSConvert( 8.000000                   _clp_cinfo->t_from_units 
	_clp_cinfo->t_to_units)                   _clpAdjustPt(909.29:-3548.25 _clp_cinfo) nil
 	_clpAdjustPt(779.29:-3548.25 _clp_cinfo))
_clp_dbid = _clpDBCreatePath(_clp_path "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = caar(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-170.61:-2813.25 _clp_cinfo) _clpAdjustPt(-430.61:-2813.25 _clp_cinfo) ) _clpMKSConvert(8.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_path = _clpPathStart(list(_clpAdjustPt(-170.61:-2813.25 _clp_cinfo))                  
	_clpMKSConvert(8.000000 _clp_cinfo->t_from_units                  			_clp_cinfo->t_to_units))
_clp_path = _clpPathArcCenter(_clp_path _clpMKSConvert( 8.000000                   _clp_cinfo->t_from_units 
	_clp_cinfo->t_to_units)                   _clpAdjustPt(-170.61:-2813.25 _clp_cinfo) nil
 	_clpAdjustPt(-300.61:-2813.25 _clp_cinfo))
_clp_dbid = _clpDBCreatePath(_clp_path "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = caar(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-170.61:-2188.25 _clp_cinfo) _clpAdjustPt(-430.61:-2188.25 _clp_cinfo) ) _clpMKSConvert(8.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_path = _clpPathStart(list(_clpAdjustPt(-170.61:-2188.25 _clp_cinfo))                  
	_clpMKSConvert(8.000000 _clp_cinfo->t_from_units                  			_clp_cinfo->t_to_units))
_clp_path = _clpPathArcCenter(_clp_path _clpMKSConvert( 8.000000                   _clp_cinfo->t_from_units 
	_clp_cinfo->t_to_units)                   _clpAdjustPt(-170.61:-2188.25 _clp_cinfo) nil
 	_clpAdjustPt(-300.61:-2188.25 _clp_cinfo))
_clp_dbid = _clpDBCreatePath(_clp_path "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = caar(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(2289.29:-1033.25 _clp_cinfo) _clpAdjustPt(2029.29:-1033.25 _clp_cinfo) ) _clpMKSConvert(8.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_path = _clpPathStart(list(_clpAdjustPt(2289.29:-1033.25 _clp_cinfo))                  
	_clpMKSConvert(8.000000 _clp_cinfo->t_from_units                  			_clp_cinfo->t_to_units))
_clp_path = _clpPathArcCenter(_clp_path _clpMKSConvert( 8.000000                   _clp_cinfo->t_from_units 
	_clp_cinfo->t_to_units)                   _clpAdjustPt(2289.29:-1033.25 _clp_cinfo) nil
 	_clpAdjustPt(2159.29:-1033.25 _clp_cinfo))
_clp_dbid = _clpDBCreatePath(_clp_path "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = caar(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(5124.29:-3920 _clp_cinfo) _clpAdjustPt(4864.29:-3920 _clp_cinfo) ) _clpMKSConvert(8.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_path = _clpPathStart(list(_clpAdjustPt(5124.29:-3920 _clp_cinfo))                  
	_clpMKSConvert(8.000000 _clp_cinfo->t_from_units                  			_clp_cinfo->t_to_units))
_clp_path = _clpPathArcCenter(_clp_path _clpMKSConvert( 8.000000                   _clp_cinfo->t_from_units 
	_clp_cinfo->t_to_units)                   _clpAdjustPt(5124.29:-3920 _clp_cinfo) nil
 	_clpAdjustPt(4994.29:-3920 _clp_cinfo))
_clp_dbid = _clpDBCreatePath(_clp_path "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = caar(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-85.61000000000001:-4448.25 _clp_cinfo) _clpAdjustPt(-345.61:-4448.25 _clp_cinfo) ) _clpMKSConvert(8.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_path = _clpPathStart(list(_clpAdjustPt(-85.61000000000001:-4448.25 _clp_cinfo))                  
	_clpMKSConvert(8.000000 _clp_cinfo->t_from_units                  			_clp_cinfo->t_to_units))
_clp_path = _clpPathArcCenter(_clp_path _clpMKSConvert( 8.000000                   _clp_cinfo->t_from_units 
	_clp_cinfo->t_to_units)                   _clpAdjustPt(-85.61000000000001:-4448.25 _clp_cinfo) nil
 	_clpAdjustPt(-215.61:-4448.25 _clp_cinfo))
_clp_dbid = _clpDBCreatePath(_clp_path "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = caar(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(2559.29:-1033.25 _clp_cinfo) _clpAdjustPt(2299.29:-1033.25 _clp_cinfo) ) _clpMKSConvert(8.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_path = _clpPathStart(list(_clpAdjustPt(2559.29:-1033.25 _clp_cinfo))                  
	_clpMKSConvert(8.000000 _clp_cinfo->t_from_units                  			_clp_cinfo->t_to_units))
_clp_path = _clpPathArcCenter(_clp_path _clpMKSConvert( 8.000000                   _clp_cinfo->t_from_units 
	_clp_cinfo->t_to_units)                   _clpAdjustPt(2559.29:-1033.25 _clp_cinfo) nil
 	_clpAdjustPt(2429.29:-1033.25 _clp_cinfo))
_clp_dbid = _clpDBCreatePath(_clp_path "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = caar(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(2019.29:-1033.25 _clp_cinfo) _clpAdjustPt(1759.29:-1033.25 _clp_cinfo) ) _clpMKSConvert(8.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_path = _clpPathStart(list(_clpAdjustPt(2019.29:-1033.25 _clp_cinfo))                  
	_clpMKSConvert(8.000000 _clp_cinfo->t_from_units                  			_clp_cinfo->t_to_units))
_clp_path = _clpPathArcCenter(_clp_path _clpMKSConvert( 8.000000                   _clp_cinfo->t_from_units 
	_clp_cinfo->t_to_units)                   _clpAdjustPt(2019.29:-1033.25 _clp_cinfo) nil
 	_clpAdjustPt(1889.29:-1033.25 _clp_cinfo))
_clp_dbid = _clpDBCreatePath(_clp_path "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = caar(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(1749.29:-1033.25 _clp_cinfo) _clpAdjustPt(1489.29:-1033.25 _clp_cinfo) ) _clpMKSConvert(8.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_path = _clpPathStart(list(_clpAdjustPt(1749.29:-1033.25 _clp_cinfo))                  
	_clpMKSConvert(8.000000 _clp_cinfo->t_from_units                  			_clp_cinfo->t_to_units))
_clp_path = _clpPathArcCenter(_clp_path _clpMKSConvert( 8.000000                   _clp_cinfo->t_from_units 
	_clp_cinfo->t_to_units)                   _clpAdjustPt(1749.29:-1033.25 _clp_cinfo) nil
 	_clpAdjustPt(1619.29:-1033.25 _clp_cinfo))
_clp_dbid = _clpDBCreatePath(_clp_path "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = caar(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(193.8599999999999:-2333.53 _clp_cinfo) _clpAdjustPt(193.8599999999999:-2589.43 _clp_cinfo) ) _clpMKSConvert(10.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(589.1299999999999:-2609.12 _clp_cinfo) _clpAdjustPt(213.54:-2609.12 _clp_cinfo) ) _clpMKSConvert(10.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(608.8199999999999:-2333.53 _clp_cinfo) _clpAdjustPt(608.8199999999999:-2589.43 _clp_cinfo) ) _clpMKSConvert(10.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(589.1299999999999:-2313.84 _clp_cinfo) _clpAdjustPt(213.54:-2313.84 _clp_cinfo) ) _clpMKSConvert(10.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_path = _clpPathStart(list(_clpAdjustPt(213.54:-2313.85 _clp_cinfo))                  
	_clpMKSConvert(10.000000 _clp_cinfo->t_from_units                  			_clp_cinfo->t_to_units))
_clp_path = _clpPathArcCenter(_clp_path _clpMKSConvert( 10.000000                   _clp_cinfo->t_from_units 
	_clp_cinfo->t_to_units)                   _clpAdjustPt(193.8599999999999:-2333.53 _clp_cinfo) nil
 	_clpAdjustPt(213.54:-2333.53 _clp_cinfo))
_clp_dbid = _clpDBCreatePath(_clp_path "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = caar(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_path = _clpPathStart(list(_clpAdjustPt(193.8599999999999:-2589.43 _clp_cinfo))                  
	_clpMKSConvert(10.000000 _clp_cinfo->t_from_units                  			_clp_cinfo->t_to_units))
_clp_path = _clpPathArcCenter(_clp_path _clpMKSConvert( 10.000000                   _clp_cinfo->t_from_units 
	_clp_cinfo->t_to_units)                   _clpAdjustPt(213.54:-2609.11 _clp_cinfo) nil
 	_clpAdjustPt(213.54:-2589.43 _clp_cinfo))
_clp_dbid = _clpDBCreatePath(_clp_path "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = caar(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_path = _clpPathStart(list(_clpAdjustPt(589.1299999999999:-2609.11 _clp_cinfo))                  
	_clpMKSConvert(10.000000 _clp_cinfo->t_from_units                  			_clp_cinfo->t_to_units))
_clp_path = _clpPathArcCenter(_clp_path _clpMKSConvert( 10.000000                   _clp_cinfo->t_from_units 
	_clp_cinfo->t_to_units)                   _clpAdjustPt(608.81:-2589.43 _clp_cinfo) nil
 	_clpAdjustPt(589.1299999999999:-2589.43 _clp_cinfo))
_clp_dbid = _clpDBCreatePath(_clp_path "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = caar(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_path = _clpPathStart(list(_clpAdjustPt(608.81:-2333.53 _clp_cinfo))                  
	_clpMKSConvert(10.000000 _clp_cinfo->t_from_units                  			_clp_cinfo->t_to_units))
_clp_path = _clpPathArcCenter(_clp_path _clpMKSConvert( 10.000000                   _clp_cinfo->t_from_units 
	_clp_cinfo->t_to_units)                   _clpAdjustPt(589.1299999999999:-2313.85 _clp_cinfo) nil
 	_clpAdjustPt(589.1299999999999:-2333.53 _clp_cinfo))
_clp_dbid = _clpDBCreatePath(_clp_path "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = caar(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(193.8599999999999:-1708.53 _clp_cinfo) _clpAdjustPt(193.8599999999999:-1964.43 _clp_cinfo) ) _clpMKSConvert(10.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(589.1299999999999:-1984.12 _clp_cinfo) _clpAdjustPt(213.54:-1984.12 _clp_cinfo) ) _clpMKSConvert(10.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(608.8199999999999:-1708.53 _clp_cinfo) _clpAdjustPt(608.8199999999999:-1964.43 _clp_cinfo) ) _clpMKSConvert(10.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(589.1299999999999:-1688.84 _clp_cinfo) _clpAdjustPt(213.54:-1688.84 _clp_cinfo) ) _clpMKSConvert(10.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_path = _clpPathStart(list(_clpAdjustPt(213.54:-1688.85 _clp_cinfo))                  
	_clpMKSConvert(10.000000 _clp_cinfo->t_from_units                  			_clp_cinfo->t_to_units))
_clp_path = _clpPathArcCenter(_clp_path _clpMKSConvert( 10.000000                   _clp_cinfo->t_from_units 
	_clp_cinfo->t_to_units)                   _clpAdjustPt(193.8599999999999:-1708.53 _clp_cinfo) nil
 	_clpAdjustPt(213.54:-1708.53 _clp_cinfo))
_clp_dbid = _clpDBCreatePath(_clp_path "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = caar(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_path = _clpPathStart(list(_clpAdjustPt(193.8599999999999:-1964.43 _clp_cinfo))                  
	_clpMKSConvert(10.000000 _clp_cinfo->t_from_units                  			_clp_cinfo->t_to_units))
_clp_path = _clpPathArcCenter(_clp_path _clpMKSConvert( 10.000000                   _clp_cinfo->t_from_units 
	_clp_cinfo->t_to_units)                   _clpAdjustPt(213.54:-1984.11 _clp_cinfo) nil
 	_clpAdjustPt(213.54:-1964.43 _clp_cinfo))
_clp_dbid = _clpDBCreatePath(_clp_path "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = caar(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_path = _clpPathStart(list(_clpAdjustPt(589.1299999999999:-1984.11 _clp_cinfo))                  
	_clpMKSConvert(10.000000 _clp_cinfo->t_from_units                  			_clp_cinfo->t_to_units))
_clp_path = _clpPathArcCenter(_clp_path _clpMKSConvert( 10.000000                   _clp_cinfo->t_from_units 
	_clp_cinfo->t_to_units)                   _clpAdjustPt(608.81:-1964.43 _clp_cinfo) nil
 	_clpAdjustPt(589.1299999999999:-1964.43 _clp_cinfo))
_clp_dbid = _clpDBCreatePath(_clp_path "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = caar(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_path = _clpPathStart(list(_clpAdjustPt(608.81:-1708.53 _clp_cinfo))                  
	_clpMKSConvert(10.000000 _clp_cinfo->t_from_units                  			_clp_cinfo->t_to_units))
_clp_path = _clpPathArcCenter(_clp_path _clpMKSConvert( 10.000000                   _clp_cinfo->t_from_units 
	_clp_cinfo->t_to_units)                   _clpAdjustPt(589.1299999999999:-1688.85 _clp_cinfo) nil
 	_clpAdjustPt(589.1299999999999:-1708.53 _clp_cinfo))
_clp_dbid = _clpDBCreatePath(_clp_path "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = caar(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(1859.01:-472.8199999999997 _clp_cinfo) _clpAdjustPt(1603.11:-472.8199999999997 _clp_cinfo) ) _clpMKSConvert(10.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(1583.42:-868.0900000000002 _clp_cinfo) _clpAdjustPt(1583.42:-492.5 _clp_cinfo) ) _clpMKSConvert(10.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(1859.01:-887.7799999999998 _clp_cinfo) _clpAdjustPt(1603.11:-887.7799999999998 _clp_cinfo) ) _clpMKSConvert(10.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(1878.7:-868.0900000000002 _clp_cinfo) _clpAdjustPt(1878.7:-492.5 _clp_cinfo) ) _clpMKSConvert(10.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_path = _clpPathStart(list(_clpAdjustPt(1878.69:-492.5 _clp_cinfo))                  
	_clpMKSConvert(10.000000 _clp_cinfo->t_from_units                  			_clp_cinfo->t_to_units))
_clp_path = _clpPathArcCenter(_clp_path _clpMKSConvert( 10.000000                   _clp_cinfo->t_from_units 
	_clp_cinfo->t_to_units)                   _clpAdjustPt(1859.01:-472.8199999999997 _clp_cinfo) nil
 	_clpAdjustPt(1859.01:-492.5 _clp_cinfo))
_clp_dbid = _clpDBCreatePath(_clp_path "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = caar(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_path = _clpPathStart(list(_clpAdjustPt(1603.11:-472.8199999999997 _clp_cinfo))                  
	_clpMKSConvert(10.000000 _clp_cinfo->t_from_units                  			_clp_cinfo->t_to_units))
_clp_path = _clpPathArcCenter(_clp_path _clpMKSConvert( 10.000000                   _clp_cinfo->t_from_units 
	_clp_cinfo->t_to_units)                   _clpAdjustPt(1583.43:-492.5 _clp_cinfo) nil
 	_clpAdjustPt(1603.11:-492.5 _clp_cinfo))
_clp_dbid = _clpDBCreatePath(_clp_path "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = caar(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_path = _clpPathStart(list(_clpAdjustPt(1583.43:-868.0900000000002 _clp_cinfo))                  
	_clpMKSConvert(10.000000 _clp_cinfo->t_from_units                  			_clp_cinfo->t_to_units))
_clp_path = _clpPathArcCenter(_clp_path _clpMKSConvert( 10.000000                   _clp_cinfo->t_from_units 
	_clp_cinfo->t_to_units)                   _clpAdjustPt(1603.11:-887.7700000000004 _clp_cinfo) nil
 	_clpAdjustPt(1603.11:-868.0900000000002 _clp_cinfo))
_clp_dbid = _clpDBCreatePath(_clp_path "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = caar(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_path = _clpPathStart(list(_clpAdjustPt(1859.01:-887.7700000000004 _clp_cinfo))                  
	_clpMKSConvert(10.000000 _clp_cinfo->t_from_units                  			_clp_cinfo->t_to_units))
_clp_path = _clpPathArcCenter(_clp_path _clpMKSConvert( 10.000000                   _clp_cinfo->t_from_units 
	_clp_cinfo->t_to_units)                   _clpAdjustPt(1878.69:-868.0900000000002 _clp_cinfo) nil
 	_clpAdjustPt(1859.01:-868.0900000000002 _clp_cinfo))
_clp_dbid = _clpDBCreatePath(_clp_path "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = caar(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(2489.01:-472.8199999999997 _clp_cinfo) _clpAdjustPt(2233.11:-472.8199999999997 _clp_cinfo) ) _clpMKSConvert(10.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(2213.42:-868.0900000000002 _clp_cinfo) _clpAdjustPt(2213.42:-492.5 _clp_cinfo) ) _clpMKSConvert(10.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(2489.01:-887.7799999999998 _clp_cinfo) _clpAdjustPt(2233.11:-887.7799999999998 _clp_cinfo) ) _clpMKSConvert(10.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(2508.7:-868.0900000000002 _clp_cinfo) _clpAdjustPt(2508.7:-492.5 _clp_cinfo) ) _clpMKSConvert(10.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_path = _clpPathStart(list(_clpAdjustPt(2508.69:-492.5 _clp_cinfo))                  
	_clpMKSConvert(10.000000 _clp_cinfo->t_from_units                  			_clp_cinfo->t_to_units))
_clp_path = _clpPathArcCenter(_clp_path _clpMKSConvert( 10.000000                   _clp_cinfo->t_from_units 
	_clp_cinfo->t_to_units)                   _clpAdjustPt(2489.01:-472.8199999999997 _clp_cinfo) nil
 	_clpAdjustPt(2489.01:-492.5 _clp_cinfo))
_clp_dbid = _clpDBCreatePath(_clp_path "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = caar(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_path = _clpPathStart(list(_clpAdjustPt(2233.11:-472.8199999999997 _clp_cinfo))                  
	_clpMKSConvert(10.000000 _clp_cinfo->t_from_units                  			_clp_cinfo->t_to_units))
_clp_path = _clpPathArcCenter(_clp_path _clpMKSConvert( 10.000000                   _clp_cinfo->t_from_units 
	_clp_cinfo->t_to_units)                   _clpAdjustPt(2213.43:-492.5 _clp_cinfo) nil
 	_clpAdjustPt(2233.11:-492.5 _clp_cinfo))
_clp_dbid = _clpDBCreatePath(_clp_path "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = caar(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_path = _clpPathStart(list(_clpAdjustPt(2213.43:-868.0900000000002 _clp_cinfo))                  
	_clpMKSConvert(10.000000 _clp_cinfo->t_from_units                  			_clp_cinfo->t_to_units))
_clp_path = _clpPathArcCenter(_clp_path _clpMKSConvert( 10.000000                   _clp_cinfo->t_from_units 
	_clp_cinfo->t_to_units)                   _clpAdjustPt(2233.11:-887.7700000000004 _clp_cinfo) nil
 	_clpAdjustPt(2233.11:-868.0900000000002 _clp_cinfo))
_clp_dbid = _clpDBCreatePath(_clp_path "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = caar(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_path = _clpPathStart(list(_clpAdjustPt(2489.01:-887.7700000000004 _clp_cinfo))                  
	_clpMKSConvert(10.000000 _clp_cinfo->t_from_units                  			_clp_cinfo->t_to_units))
_clp_path = _clpPathArcCenter(_clp_path _clpMKSConvert( 10.000000                   _clp_cinfo->t_from_units 
	_clp_cinfo->t_to_units)                   _clpAdjustPt(2508.69:-868.0900000000002 _clp_cinfo) nil
 	_clpAdjustPt(2489.01:-868.0900000000002 _clp_cinfo))
_clp_dbid = _clpDBCreatePath(_clp_path "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = caar(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

printf(" 80 percent completed")
newline()

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(3114.01:-472.8199999999997 _clp_cinfo) _clpAdjustPt(2858.11:-472.8199999999997 _clp_cinfo) ) _clpMKSConvert(10.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(2838.42:-868.0900000000002 _clp_cinfo) _clpAdjustPt(2838.42:-492.5 _clp_cinfo) ) _clpMKSConvert(10.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(3114.01:-887.7799999999998 _clp_cinfo) _clpAdjustPt(2858.11:-887.7799999999998 _clp_cinfo) ) _clpMKSConvert(10.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(3133.7:-868.0900000000002 _clp_cinfo) _clpAdjustPt(3133.7:-492.5 _clp_cinfo) ) _clpMKSConvert(10.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_path = _clpPathStart(list(_clpAdjustPt(3133.69:-492.5 _clp_cinfo))                  
	_clpMKSConvert(10.000000 _clp_cinfo->t_from_units                  			_clp_cinfo->t_to_units))
_clp_path = _clpPathArcCenter(_clp_path _clpMKSConvert( 10.000000                   _clp_cinfo->t_from_units 
	_clp_cinfo->t_to_units)                   _clpAdjustPt(3114.01:-472.8199999999997 _clp_cinfo) nil
 	_clpAdjustPt(3114.01:-492.5 _clp_cinfo))
_clp_dbid = _clpDBCreatePath(_clp_path "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = caar(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_path = _clpPathStart(list(_clpAdjustPt(2858.11:-472.8199999999997 _clp_cinfo))                  
	_clpMKSConvert(10.000000 _clp_cinfo->t_from_units                  			_clp_cinfo->t_to_units))
_clp_path = _clpPathArcCenter(_clp_path _clpMKSConvert( 10.000000                   _clp_cinfo->t_from_units 
	_clp_cinfo->t_to_units)                   _clpAdjustPt(2838.43:-492.5 _clp_cinfo) nil
 	_clpAdjustPt(2858.11:-492.5 _clp_cinfo))
_clp_dbid = _clpDBCreatePath(_clp_path "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = caar(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_path = _clpPathStart(list(_clpAdjustPt(2838.43:-868.0900000000002 _clp_cinfo))                  
	_clpMKSConvert(10.000000 _clp_cinfo->t_from_units                  			_clp_cinfo->t_to_units))
_clp_path = _clpPathArcCenter(_clp_path _clpMKSConvert( 10.000000                   _clp_cinfo->t_from_units 
	_clp_cinfo->t_to_units)                   _clpAdjustPt(2858.11:-887.7700000000004 _clp_cinfo) nil
 	_clpAdjustPt(2858.11:-868.0900000000002 _clp_cinfo))
_clp_dbid = _clpDBCreatePath(_clp_path "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = caar(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_path = _clpPathStart(list(_clpAdjustPt(3114.01:-887.7700000000004 _clp_cinfo))                  
	_clpMKSConvert(10.000000 _clp_cinfo->t_from_units                  			_clp_cinfo->t_to_units))
_clp_path = _clpPathArcCenter(_clp_path _clpMKSConvert( 10.000000                   _clp_cinfo->t_from_units 
	_clp_cinfo->t_to_units)                   _clpAdjustPt(3133.69:-868.0900000000002 _clp_cinfo) nil
 	_clpAdjustPt(3114.01:-868.0900000000002 _clp_cinfo))
_clp_dbid = _clpDBCreatePath(_clp_path "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = caar(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(5159.01:-1669.57 _clp_cinfo) _clpAdjustPt(4903.11:-1669.57 _clp_cinfo) ) _clpMKSConvert(10.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(4883.42:-2064.84 _clp_cinfo) _clpAdjustPt(4883.42:-1689.25 _clp_cinfo) ) _clpMKSConvert(10.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(5159.01:-2084.53 _clp_cinfo) _clpAdjustPt(4903.11:-2084.53 _clp_cinfo) ) _clpMKSConvert(10.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(5178.7:-2064.84 _clp_cinfo) _clpAdjustPt(5178.7:-1689.25 _clp_cinfo) ) _clpMKSConvert(10.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_path = _clpPathStart(list(_clpAdjustPt(5178.69:-1689.25 _clp_cinfo))                  
	_clpMKSConvert(10.000000 _clp_cinfo->t_from_units                  			_clp_cinfo->t_to_units))
_clp_path = _clpPathArcCenter(_clp_path _clpMKSConvert( 10.000000                   _clp_cinfo->t_from_units 
	_clp_cinfo->t_to_units)                   _clpAdjustPt(5159.01:-1669.57 _clp_cinfo) nil
 	_clpAdjustPt(5159.01:-1689.25 _clp_cinfo))
_clp_dbid = _clpDBCreatePath(_clp_path "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = caar(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_path = _clpPathStart(list(_clpAdjustPt(4903.11:-1669.57 _clp_cinfo))                  
	_clpMKSConvert(10.000000 _clp_cinfo->t_from_units                  			_clp_cinfo->t_to_units))
_clp_path = _clpPathArcCenter(_clp_path _clpMKSConvert( 10.000000                   _clp_cinfo->t_from_units 
	_clp_cinfo->t_to_units)                   _clpAdjustPt(4883.43:-1689.25 _clp_cinfo) nil
 	_clpAdjustPt(4903.11:-1689.25 _clp_cinfo))
_clp_dbid = _clpDBCreatePath(_clp_path "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = caar(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_path = _clpPathStart(list(_clpAdjustPt(4883.43:-2064.84 _clp_cinfo))                  
	_clpMKSConvert(10.000000 _clp_cinfo->t_from_units                  			_clp_cinfo->t_to_units))
_clp_path = _clpPathArcCenter(_clp_path _clpMKSConvert( 10.000000                   _clp_cinfo->t_from_units 
	_clp_cinfo->t_to_units)                   _clpAdjustPt(4903.11:-2084.52 _clp_cinfo) nil
 	_clpAdjustPt(4903.11:-2064.84 _clp_cinfo))
_clp_dbid = _clpDBCreatePath(_clp_path "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = caar(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_path = _clpPathStart(list(_clpAdjustPt(5159.01:-2084.52 _clp_cinfo))                  
	_clpMKSConvert(10.000000 _clp_cinfo->t_from_units                  			_clp_cinfo->t_to_units))
_clp_path = _clpPathArcCenter(_clp_path _clpMKSConvert( 10.000000                   _clp_cinfo->t_from_units 
	_clp_cinfo->t_to_units)                   _clpAdjustPt(5178.69:-2064.84 _clp_cinfo) nil
 	_clpAdjustPt(5159.01:-2064.84 _clp_cinfo))
_clp_dbid = _clpDBCreatePath(_clp_path "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = caar(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(244.29:-2713.25 _clp_cinfo) _clpAdjustPt(244.29:-2743.25 _clp_cinfo) ) _clpMKSConvert(12.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(299.29:-2753.25 _clp_cinfo) _clpAdjustPt(189.29:-2753.25 _clp_cinfo) ) _clpMKSConvert(5.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(189.29:-2703.25 _clp_cinfo) _clpAdjustPt(189.29:-2753.25 _clp_cinfo) ) _clpMKSConvert(5.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(299.29:-2703.25 _clp_cinfo) _clpAdjustPt(189.29:-2703.25 _clp_cinfo) ) _clpMKSConvert(5.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(299.29:-2703.25 _clp_cinfo) _clpAdjustPt(299.29:-2753.25 _clp_cinfo) ) _clpMKSConvert(5.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-60.61000000000001:-3263.15 _clp_cinfo) _clpAdjustPt(-60.61000000000001:-3293.15 _clp_cinfo) ) _clpMKSConvert(12.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-5.610000000000014:-3303.15 _clp_cinfo) _clpAdjustPt(-115.61:-3303.15 _clp_cinfo) ) _clpMKSConvert(5.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-115.61:-3253.15 _clp_cinfo) _clpAdjustPt(-115.61:-3303.15 _clp_cinfo) ) _clpMKSConvert(5.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-5.610000000000014:-3253.15 _clp_cinfo) _clpAdjustPt(-115.61:-3253.15 _clp_cinfo) ) _clpMKSConvert(5.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-5.610000000000014:-3253.15 _clp_cinfo) _clpAdjustPt(-5.610000000000014:-3303.15 _clp_cinfo) ) _clpMKSConvert(5.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(4.289999999999964:-2328.25 _clp_cinfo) _clpAdjustPt(4.289999999999964:-2358.25 _clp_cinfo) ) _clpMKSConvert(12.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(59.28999999999996:-2368.25 _clp_cinfo) _clpAdjustPt(-50.71000000000004:-2368.25 _clp_cinfo) ) _clpMKSConvert(5.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-50.71000000000004:-2318.25 _clp_cinfo) _clpAdjustPt(-50.71000000000004:-2368.25 _clp_cinfo) ) _clpMKSConvert(5.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(59.28999999999996:-2318.25 _clp_cinfo) _clpAdjustPt(-50.71000000000004:-2318.25 _clp_cinfo) ) _clpMKSConvert(5.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(59.28999999999996:-2318.25 _clp_cinfo) _clpAdjustPt(59.28999999999996:-2368.25 _clp_cinfo) ) _clpMKSConvert(5.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(244.29:-2088.25 _clp_cinfo) _clpAdjustPt(244.29:-2118.25 _clp_cinfo) ) _clpMKSConvert(12.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(299.29:-2128.25 _clp_cinfo) _clpAdjustPt(189.29:-2128.25 _clp_cinfo) ) _clpMKSConvert(5.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(189.29:-2078.25 _clp_cinfo) _clpAdjustPt(189.29:-2128.25 _clp_cinfo) ) _clpMKSConvert(5.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(299.29:-2078.25 _clp_cinfo) _clpAdjustPt(189.29:-2078.25 _clp_cinfo) ) _clpMKSConvert(5.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(299.29:-2078.25 _clp_cinfo) _clpAdjustPt(299.29:-2128.25 _clp_cinfo) ) _clpMKSConvert(5.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-60.71000000000004:-2638.25 _clp_cinfo) _clpAdjustPt(-60.71000000000004:-2668.25 _clp_cinfo) ) _clpMKSConvert(12.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-5.710000000000036:-2678.25 _clp_cinfo) _clpAdjustPt(-115.71:-2678.25 _clp_cinfo) ) _clpMKSConvert(5.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-115.71:-2628.25 _clp_cinfo) _clpAdjustPt(-115.71:-2678.25 _clp_cinfo) ) _clpMKSConvert(5.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-5.710000000000036:-2628.25 _clp_cinfo) _clpAdjustPt(-115.71:-2628.25 _clp_cinfo) ) _clpMKSConvert(5.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-5.710000000000036:-2628.25 _clp_cinfo) _clpAdjustPt(-5.710000000000036:-2678.25 _clp_cinfo) ) _clpMKSConvert(5.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(4.289999999999964:-1703.25 _clp_cinfo) _clpAdjustPt(4.289999999999964:-1733.25 _clp_cinfo) ) _clpMKSConvert(12.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(59.28999999999996:-1743.25 _clp_cinfo) _clpAdjustPt(-50.71000000000004:-1743.25 _clp_cinfo) ) _clpMKSConvert(5.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-50.71000000000004:-1693.25 _clp_cinfo) _clpAdjustPt(-50.71000000000004:-1743.25 _clp_cinfo) ) _clpMKSConvert(5.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(59.28999999999996:-1693.25 _clp_cinfo) _clpAdjustPt(-50.71000000000004:-1693.25 _clp_cinfo) ) _clpMKSConvert(5.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(59.28999999999996:-1693.25 _clp_cinfo) _clpAdjustPt(59.28999999999996:-1743.25 _clp_cinfo) ) _clpMKSConvert(5.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-60.71000000000004:-2013.25 _clp_cinfo) _clpAdjustPt(-60.71000000000004:-2043.25 _clp_cinfo) ) _clpMKSConvert(12.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-5.710000000000036:-2053.25 _clp_cinfo) _clpAdjustPt(-115.71:-2053.25 _clp_cinfo) ) _clpMKSConvert(5.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-115.71:-2003.25 _clp_cinfo) _clpAdjustPt(-115.71:-2053.25 _clp_cinfo) ) _clpMKSConvert(5.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-5.710000000000036:-2003.25 _clp_cinfo) _clpAdjustPt(-115.71:-2003.25 _clp_cinfo) ) _clpMKSConvert(5.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-5.710000000000036:-2003.25 _clp_cinfo) _clpAdjustPt(-5.710000000000036:-2053.25 _clp_cinfo) ) _clpMKSConvert(5.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(1029.29:-1128.25 _clp_cinfo) _clpAdjustPt(1029.29:-1158.25 _clp_cinfo) ) _clpMKSConvert(12.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(1084.29:-1168.25 _clp_cinfo) _clpAdjustPt(974.29:-1168.25 _clp_cinfo) ) _clpMKSConvert(5.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(974.29:-1118.25 _clp_cinfo) _clpAdjustPt(974.29:-1168.25 _clp_cinfo) ) _clpMKSConvert(5.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(1084.29:-1118.25 _clp_cinfo) _clpAdjustPt(974.29:-1118.25 _clp_cinfo) ) _clpMKSConvert(5.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(1084.29:-1118.25 _clp_cinfo) _clpAdjustPt(1084.29:-1168.25 _clp_cinfo) ) _clpMKSConvert(5.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_path = _clpPathStart(list(_clpAdjustPt(-725.71:-6185 _clp_cinfo))                  
	_clpMKSConvert(8.000000 _clp_cinfo->t_from_units                  			_clp_cinfo->t_to_units))
_clp_path = _clpPathArcCenter(_clp_path _clpMKSConvert( 8.000000                   _clp_cinfo->t_from_units 
	_clp_cinfo->t_to_units)                   _clpAdjustPt(-725.71:-6185 _clp_cinfo) nil
 	_clpAdjustPt(-905.71:-6185 _clp_cinfo))
_clp_dbid = _clpDBCreatePath(_clp_path "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = caar(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(5215.88:-6495 _clp_cinfo) _clpAdjustPt(4955.88:-6495 _clp_cinfo) ) _clpMKSConvert(8.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_path = _clpPathStart(list(_clpAdjustPt(5215.88:-6495 _clp_cinfo))                  
	_clpMKSConvert(8.000000 _clp_cinfo->t_from_units                  			_clp_cinfo->t_to_units))
_clp_path = _clpPathArcCenter(_clp_path _clpMKSConvert( 8.000000                   _clp_cinfo->t_from_units 
	_clp_cinfo->t_to_units)                   _clpAdjustPt(5215.88:-6495 _clp_cinfo) nil
 	_clpAdjustPt(5085.88:-6495 _clp_cinfo))
_clp_dbid = _clpDBCreatePath(_clp_path "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = caar(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(5500.88:-6495 _clp_cinfo) _clpAdjustPt(5240.88:-6495 _clp_cinfo) ) _clpMKSConvert(8.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_path = _clpPathStart(list(_clpAdjustPt(5500.88:-6495 _clp_cinfo))                  
	_clpMKSConvert(8.000000 _clp_cinfo->t_from_units                  			_clp_cinfo->t_to_units))
_clp_path = _clpPathArcCenter(_clp_path _clpMKSConvert( 8.000000                   _clp_cinfo->t_from_units 
	_clp_cinfo->t_to_units)                   _clpAdjustPt(5500.88:-6495 _clp_cinfo) nil
 	_clpAdjustPt(5370.88:-6495 _clp_cinfo))
_clp_dbid = _clpDBCreatePath(_clp_path "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = caar(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(2607.52:-21.19999999999982 _clp_cinfo) _clpAdjustPt(2347.52:-21.19999999999982 _clp_cinfo) ) _clpMKSConvert(8.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_path = _clpPathStart(list(_clpAdjustPt(2607.52:-21.19999999999982 _clp_cinfo))                  
	_clpMKSConvert(8.000000 _clp_cinfo->t_from_units                  			_clp_cinfo->t_to_units))
_clp_path = _clpPathArcCenter(_clp_path _clpMKSConvert( 8.000000                   _clp_cinfo->t_from_units 
	_clp_cinfo->t_to_units)                   _clpAdjustPt(2607.52:-21.19999999999982 _clp_cinfo) nil
 	_clpAdjustPt(2477.52:-21.19999999999982 _clp_cinfo))
_clp_dbid = _clpDBCreatePath(_clp_path "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = caar(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(3232.52:-21.19999999999982 _clp_cinfo) _clpAdjustPt(2972.52:-21.19999999999982 _clp_cinfo) ) _clpMKSConvert(8.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_path = _clpPathStart(list(_clpAdjustPt(3232.52:-21.19999999999982 _clp_cinfo))                  
	_clpMKSConvert(8.000000 _clp_cinfo->t_from_units                  			_clp_cinfo->t_to_units))
_clp_path = _clpPathArcCenter(_clp_path _clpMKSConvert( 8.000000                   _clp_cinfo->t_from_units 
	_clp_cinfo->t_to_units)                   _clpAdjustPt(3232.52:-21.19999999999982 _clp_cinfo) nil
 	_clpAdjustPt(3102.52:-21.19999999999982 _clp_cinfo))
_clp_dbid = _clpDBCreatePath(_clp_path "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = caar(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_path = _clpPathStart(list(_clpAdjustPt(5421.29:0 _clp_cinfo))                  
	_clpMKSConvert(8.000000 _clp_cinfo->t_from_units                  			_clp_cinfo->t_to_units))
_clp_path = _clpPathArcCenter(_clp_path _clpMKSConvert( 8.000000                   _clp_cinfo->t_from_units 
	_clp_cinfo->t_to_units)                   _clpAdjustPt(5421.29:0 _clp_cinfo) nil
 	_clpAdjustPt(5241.29:0 _clp_cinfo))
_clp_dbid = _clpDBCreatePath(_clp_path "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = caar(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(5095.54:-1407.5 _clp_cinfo) _clpAdjustPt(4958.04:-1407.5 _clp_cinfo) ) _clpMKSConvert(6.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(4958.04:-1112.5 _clp_cinfo) _clpAdjustPt(4958.04:-1407.5 _clp_cinfo) ) _clpMKSConvert(6.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(5023.04:-1112.5 _clp_cinfo) _clpAdjustPt(4958.04:-1112.5 _clp_cinfo) ) _clpMKSConvert(6.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(5023.04:-1112.5 _clp_cinfo) _clpAdjustPt(5023.04:-1127.5 _clp_cinfo) ) _clpMKSConvert(6.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(5118.04:-1127.5 _clp_cinfo) _clpAdjustPt(5023.04:-1127.5 _clp_cinfo) ) _clpMKSConvert(6.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(5118.04:-1112.5 _clp_cinfo) _clpAdjustPt(5118.04:-1127.5 _clp_cinfo) ) _clpMKSConvert(6.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(5180.54:-1112.5 _clp_cinfo) _clpAdjustPt(5118.04:-1112.5 _clp_cinfo) ) _clpMKSConvert(6.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(5180.54:-1112.5 _clp_cinfo) _clpAdjustPt(5180.54:-1407.5 _clp_cinfo) ) _clpMKSConvert(6.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(5180.54:-1407.5 _clp_cinfo) _clpAdjustPt(5095.54:-1407.5 _clp_cinfo) ) _clpMKSConvert(6.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(3060.54:-160.75 _clp_cinfo) _clpAdjustPt(2923.04:-160.75 _clp_cinfo) ) _clpMKSConvert(6.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(3060.54:-160.75 _clp_cinfo) _clpAdjustPt(3060.54:-455.75 _clp_cinfo) ) _clpMKSConvert(6.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(3060.54:-455.75 _clp_cinfo) _clpAdjustPt(2995.54:-455.75 _clp_cinfo) ) _clpMKSConvert(6.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(2995.54:-440.75 _clp_cinfo) _clpAdjustPt(2995.54:-455.75 _clp_cinfo) ) _clpMKSConvert(6.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(2995.54:-440.75 _clp_cinfo) _clpAdjustPt(2900.54:-440.75 _clp_cinfo) ) _clpMKSConvert(6.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(2900.54:-440.75 _clp_cinfo) _clpAdjustPt(2900.54:-455.75 _clp_cinfo) ) _clpMKSConvert(6.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(2900.54:-455.75 _clp_cinfo) _clpAdjustPt(2838.04:-455.75 _clp_cinfo) ) _clpMKSConvert(6.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(2838.04:-160.75 _clp_cinfo) _clpAdjustPt(2838.04:-455.75 _clp_cinfo) ) _clpMKSConvert(6.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(2923.04:-160.75 _clp_cinfo) _clpAdjustPt(2838.04:-160.75 _clp_cinfo) ) _clpMKSConvert(6.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(3285.54:-455.75 _clp_cinfo) _clpAdjustPt(3148.04:-455.75 _clp_cinfo) ) _clpMKSConvert(6.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(3148.04:-160.75 _clp_cinfo) _clpAdjustPt(3148.04:-455.75 _clp_cinfo) ) _clpMKSConvert(6.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(3213.04:-160.75 _clp_cinfo) _clpAdjustPt(3148.04:-160.75 _clp_cinfo) ) _clpMKSConvert(6.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(3213.04:-160.75 _clp_cinfo) _clpAdjustPt(3213.04:-175.75 _clp_cinfo) ) _clpMKSConvert(6.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(3308.04:-175.75 _clp_cinfo) _clpAdjustPt(3213.04:-175.75 _clp_cinfo) ) _clpMKSConvert(6.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(3308.04:-160.75 _clp_cinfo) _clpAdjustPt(3308.04:-175.75 _clp_cinfo) ) _clpMKSConvert(6.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(3370.54:-160.75 _clp_cinfo) _clpAdjustPt(3308.04:-160.75 _clp_cinfo) ) _clpMKSConvert(6.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(3370.54:-160.75 _clp_cinfo) _clpAdjustPt(3370.54:-455.75 _clp_cinfo) ) _clpMKSConvert(6.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(3370.54:-455.75 _clp_cinfo) _clpAdjustPt(3285.54:-455.75 _clp_cinfo) ) _clpMKSConvert(6.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(5109.29:-4910 _clp_cinfo) _clpAdjustPt(5089.29:-4890 _clp_cinfo) ) _clpMKSConvert(5.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(5109.29:-4870 _clp_cinfo) _clpAdjustPt(5089.29:-4890 _clp_cinfo) ) _clpMKSConvert(5.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(5109.29:-4825 _clp_cinfo) _clpAdjustPt(4909.29:-4825 _clp_cinfo) ) _clpMKSConvert(5.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(4909.29:-4825 _clp_cinfo) _clpAdjustPt(4909.29:-4955 _clp_cinfo) ) _clpMKSConvert(5.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(5109.29:-4955 _clp_cinfo) _clpAdjustPt(4909.29:-4955 _clp_cinfo) ) _clpMKSConvert(5.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(5109.29:-4825 _clp_cinfo) _clpAdjustPt(5109.29:-4955 _clp_cinfo) ) _clpMKSConvert(5.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_path = _clpPathStart(list(_clpAdjustPt(5114.29:-4760 _clp_cinfo))                  
	_clpMKSConvert(10.000000 _clp_cinfo->t_from_units                  			_clp_cinfo->t_to_units))
_clp_path = _clpPathArcCenter(_clp_path _clpMKSConvert( 10.000000                   _clp_cinfo->t_from_units 
	_clp_cinfo->t_to_units)                   _clpAdjustPt(5114.29:-4760 _clp_cinfo) nil
 	_clpAdjustPt(5109.29:-4760 _clp_cinfo))
_clp_dbid = _clpDBCreatePath(_clp_path "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = caar(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(314.29:-2078.25 _clp_cinfo) _clpAdjustPt(314.29:-2218.25 _clp_cinfo) ) _clpMKSConvert(8.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(484.29:-2078.25 _clp_cinfo) _clpAdjustPt(314.29:-2078.25 _clp_cinfo) ) _clpMKSConvert(8.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(484.29:-2078.25 _clp_cinfo) _clpAdjustPt(484.29:-2218.25 _clp_cinfo) ) _clpMKSConvert(8.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

printf(" 90 percent completed")
newline()

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(484.29:-2218.25 _clp_cinfo) _clpAdjustPt(419.29:-2218.25 _clp_cinfo) ) _clpMKSConvert(8.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(419.29:-2218.25 _clp_cinfo) _clpAdjustPt(399.29:-2198.25 _clp_cinfo) ) _clpMKSConvert(8.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(399.29:-2198.25 _clp_cinfo) _clpAdjustPt(379.29:-2218.25 _clp_cinfo) ) _clpMKSConvert(8.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(379.29:-2218.25 _clp_cinfo) _clpAdjustPt(314.29:-2218.25 _clp_cinfo) ) _clpMKSConvert(8.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(419.29:-2218.25 _clp_cinfo) _clpAdjustPt(379.29:-2218.25 _clp_cinfo) ) _clpMKSConvert(8.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(489.29:-2188.25 _clp_cinfo) _clpAdjustPt(489.29:-2223.25 _clp_cinfo) ) _clpMKSConvert(20.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(489.29:-2223.25 _clp_cinfo) _clpAdjustPt(449.29:-2223.25 _clp_cinfo) ) _clpMKSConvert(20.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(2469.29:-4633.25 _clp_cinfo) _clpAdjustPt(2449.29:-4613.25 _clp_cinfo) ) _clpMKSConvert(5.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(2469.29:-4633.25 _clp_cinfo) _clpAdjustPt(2449.29:-4653.25 _clp_cinfo) ) _clpMKSConvert(5.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(2649.29:-4698.25 _clp_cinfo) _clpAdjustPt(2449.29:-4698.25 _clp_cinfo) ) _clpMKSConvert(5.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(2649.29:-4568.25 _clp_cinfo) _clpAdjustPt(2649.29:-4698.25 _clp_cinfo) ) _clpMKSConvert(5.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(2649.29:-4568.25 _clp_cinfo) _clpAdjustPt(2449.29:-4568.25 _clp_cinfo) ) _clpMKSConvert(5.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(2449.29:-4568.25 _clp_cinfo) _clpAdjustPt(2449.29:-4698.25 _clp_cinfo) ) _clpMKSConvert(5.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_path = _clpPathStart(list(_clpAdjustPt(2454.29:-4763.25 _clp_cinfo))                  
	_clpMKSConvert(10.000000 _clp_cinfo->t_from_units                  			_clp_cinfo->t_to_units))
_clp_path = _clpPathArcCenter(_clp_path _clpMKSConvert( 10.000000                   _clp_cinfo->t_from_units 
	_clp_cinfo->t_to_units)                   _clpAdjustPt(2454.29:-4763.25 _clp_cinfo) nil
 	_clpAdjustPt(2449.29:-4763.25 _clp_cinfo))
_clp_dbid = _clpDBCreatePath(_clp_path "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = caar(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(2164.29:-4633.25 _clp_cinfo) _clpAdjustPt(2144.29:-4613.25 _clp_cinfo) ) _clpMKSConvert(5.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(2164.29:-4633.25 _clp_cinfo) _clpAdjustPt(2144.29:-4653.25 _clp_cinfo) ) _clpMKSConvert(5.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(2344.29:-4698.25 _clp_cinfo) _clpAdjustPt(2144.29:-4698.25 _clp_cinfo) ) _clpMKSConvert(5.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(2344.29:-4568.25 _clp_cinfo) _clpAdjustPt(2344.29:-4698.25 _clp_cinfo) ) _clpMKSConvert(5.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(2344.29:-4568.25 _clp_cinfo) _clpAdjustPt(2144.29:-4568.25 _clp_cinfo) ) _clpMKSConvert(5.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(2144.29:-4568.25 _clp_cinfo) _clpAdjustPt(2144.29:-4698.25 _clp_cinfo) ) _clpMKSConvert(5.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_path = _clpPathStart(list(_clpAdjustPt(2149.29:-4763.25 _clp_cinfo))                  
	_clpMKSConvert(10.000000 _clp_cinfo->t_from_units                  			_clp_cinfo->t_to_units))
_clp_path = _clpPathArcCenter(_clp_path _clpMKSConvert( 10.000000                   _clp_cinfo->t_from_units 
	_clp_cinfo->t_to_units)                   _clpAdjustPt(2149.29:-4763.25 _clp_cinfo) nil
 	_clpAdjustPt(2144.29:-4763.25 _clp_cinfo))
_clp_dbid = _clpDBCreatePath(_clp_path "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = caar(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(5082.38:-6644 _clp_cinfo) _clpAdjustPt(5131.38:-6644 _clp_cinfo) ) _clpMKSConvert(10.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(5040.38:-6644 _clp_cinfo) _clpAdjustPt(5101.38:-6644 _clp_cinfo) ) _clpMKSConvert(10.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_path = _clpPathStart(list(_clpAdjustPt(5231.38:-6744 _clp_cinfo))                  
	_clpMKSConvert(10.000000 _clp_cinfo->t_from_units                  			_clp_cinfo->t_to_units))
_clp_path = _clpPathArcCenter(_clp_path _clpMKSConvert( 10.000000                   _clp_cinfo->t_from_units 
	_clp_cinfo->t_to_units)                   _clpAdjustPt(5131.38:-6644 _clp_cinfo) nil
 	_clpAdjustPt(5131.38:-6744 _clp_cinfo))
_clp_dbid = _clpDBCreatePath(_clp_path "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = caar(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_path = _clpPathStart(list(_clpAdjustPt(5040.38:-6644 _clp_cinfo))                  
	_clpMKSConvert(10.000000 _clp_cinfo->t_from_units                  			_clp_cinfo->t_to_units))
_clp_path = _clpPathArcCenter(_clp_path _clpMKSConvert( 10.000000                   _clp_cinfo->t_from_units 
	_clp_cinfo->t_to_units)                   _clpAdjustPt(4940.38:-6744 _clp_cinfo) nil
 	_clpAdjustPt(5040.38:-6744 _clp_cinfo))
_clp_dbid = _clpDBCreatePath(_clp_path "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = caar(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(4811.29:88.39999999999964 _clp_cinfo) _clpAdjustPt(4503.99:88.39999999999964 _clp_cinfo) ) _clpMKSConvert(8.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(4811.29:88.39999999999964 _clp_cinfo) _clpAdjustPt(4811.29:-5502.5 _clp_cinfo) ) _clpMKSConvert(8.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(4811.29:-5502.5 _clp_cinfo) _clpAdjustPt(4503.99:-5502.5 _clp_cinfo) ) _clpMKSConvert(8.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(4503.99:88.39999999999964 _clp_cinfo) _clpAdjustPt(4503.99:-5502.5 _clp_cinfo) ) _clpMKSConvert(8.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(36.28999999999996:-4063 _clp_cinfo) _clpAdjustPt(25.28999999999996:-4063 _clp_cinfo) ) _clpMKSConvert(5.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(36.28999999999996:-4063 _clp_cinfo) _clpAdjustPt(36.28999999999996:-4195 _clp_cinfo) ) _clpMKSConvert(5.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(36.28999999999996:-4195 _clp_cinfo) _clpAdjustPt(24.28999999999996:-4195 _clp_cinfo) ) _clpMKSConvert(5.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-74.71000000000004:-4195 _clp_cinfo) _clpAdjustPt(-87.71000000000004:-4182 _clp_cinfo) ) _clpMKSConvert(5.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-87.71000000000004:-4063 _clp_cinfo) _clpAdjustPt(-87.71000000000004:-4182 _clp_cinfo) ) _clpMKSConvert(5.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-75.71000000000004:-4063 _clp_cinfo) _clpAdjustPt(-87.71000000000004:-4063 _clp_cinfo) ) _clpMKSConvert(5.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(314.29:-1453.25 _clp_cinfo) _clpAdjustPt(314.29:-1593.25 _clp_cinfo) ) _clpMKSConvert(8.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(314.29:-1453.25 _clp_cinfo) _clpAdjustPt(484.29:-1453.25 _clp_cinfo) ) _clpMKSConvert(8.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(484.29:-1453.25 _clp_cinfo) _clpAdjustPt(484.29:-1593.25 _clp_cinfo) ) _clpMKSConvert(8.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(419.29:-1593.25 _clp_cinfo) _clpAdjustPt(484.29:-1593.25 _clp_cinfo) ) _clpMKSConvert(8.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(399.29:-1573.25 _clp_cinfo) _clpAdjustPt(419.29:-1593.25 _clp_cinfo) ) _clpMKSConvert(8.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(399.29:-1573.25 _clp_cinfo) _clpAdjustPt(379.29:-1593.25 _clp_cinfo) ) _clpMKSConvert(8.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(314.29:-1593.25 _clp_cinfo) _clpAdjustPt(379.29:-1593.25 _clp_cinfo) ) _clpMKSConvert(8.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(379.29:-1593.25 _clp_cinfo) _clpAdjustPt(419.29:-1593.25 _clp_cinfo) ) _clpMKSConvert(8.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(489.29:-1563.25 _clp_cinfo) _clpAdjustPt(489.29:-1598.25 _clp_cinfo) ) _clpMKSConvert(20.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(449.29:-1598.25 _clp_cinfo) _clpAdjustPt(489.29:-1598.25 _clp_cinfo) ) _clpMKSConvert(20.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(2114.29:-598.25 _clp_cinfo) _clpAdjustPt(1974.29:-598.25 _clp_cinfo) ) _clpMKSConvert(8.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(2114.29:-598.25 _clp_cinfo) _clpAdjustPt(2114.29:-768.25 _clp_cinfo) ) _clpMKSConvert(8.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(2114.29:-768.25 _clp_cinfo) _clpAdjustPt(1974.29:-768.25 _clp_cinfo) ) _clpMKSConvert(8.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(1974.29:-703.25 _clp_cinfo) _clpAdjustPt(1974.29:-768.25 _clp_cinfo) ) _clpMKSConvert(8.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(1994.29:-683.25 _clp_cinfo) _clpAdjustPt(1974.29:-703.25 _clp_cinfo) ) _clpMKSConvert(8.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(1994.29:-683.25 _clp_cinfo) _clpAdjustPt(1974.29:-663.25 _clp_cinfo) ) _clpMKSConvert(8.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(1974.29:-598.25 _clp_cinfo) _clpAdjustPt(1974.29:-663.25 _clp_cinfo) ) _clpMKSConvert(8.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(1974.29:-663.25 _clp_cinfo) _clpAdjustPt(1974.29:-703.25 _clp_cinfo) ) _clpMKSConvert(8.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(2004.29:-773.25 _clp_cinfo) _clpAdjustPt(1969.29:-773.25 _clp_cinfo) ) _clpMKSConvert(20.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(1969.29:-733.25 _clp_cinfo) _clpAdjustPt(1969.29:-773.25 _clp_cinfo) ) _clpMKSConvert(20.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(3369.29:-598.25 _clp_cinfo) _clpAdjustPt(3229.29:-598.25 _clp_cinfo) ) _clpMKSConvert(8.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(3369.29:-598.25 _clp_cinfo) _clpAdjustPt(3369.29:-768.25 _clp_cinfo) ) _clpMKSConvert(8.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(3369.29:-768.25 _clp_cinfo) _clpAdjustPt(3229.29:-768.25 _clp_cinfo) ) _clpMKSConvert(8.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(3229.29:-703.25 _clp_cinfo) _clpAdjustPt(3229.29:-768.25 _clp_cinfo) ) _clpMKSConvert(8.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(3249.29:-683.25 _clp_cinfo) _clpAdjustPt(3229.29:-703.25 _clp_cinfo) ) _clpMKSConvert(8.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(3249.29:-683.25 _clp_cinfo) _clpAdjustPt(3229.29:-663.25 _clp_cinfo) ) _clpMKSConvert(8.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(3229.29:-598.25 _clp_cinfo) _clpAdjustPt(3229.29:-663.25 _clp_cinfo) ) _clpMKSConvert(8.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(3229.29:-663.25 _clp_cinfo) _clpAdjustPt(3229.29:-703.25 _clp_cinfo) ) _clpMKSConvert(8.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(3259.29:-773.25 _clp_cinfo) _clpAdjustPt(3224.29:-773.25 _clp_cinfo) ) _clpMKSConvert(20.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(3224.29:-733.25 _clp_cinfo) _clpAdjustPt(3224.29:-773.25 _clp_cinfo) ) _clpMKSConvert(20.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(1018.19:-4772.4 _clp_cinfo) _clpAdjustPt(1018.19:-4827.6 _clp_cinfo) ) _clpMKSConvert(5.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(998.8899999999999:-4772.4 _clp_cinfo) _clpAdjustPt(998.8899999999999:-4780.3 _clp_cinfo) ) _clpMKSConvert(5.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(1069.69:-4772.4 _clp_cinfo) _clpAdjustPt(998.8899999999999:-4772.4 _clp_cinfo) ) _clpMKSConvert(5.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(1069.69:-4772.4 _clp_cinfo) _clpAdjustPt(1069.69:-4780.3 _clp_cinfo) ) _clpMKSConvert(5.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(998.8899999999999:-4819.7 _clp_cinfo) _clpAdjustPt(998.8899999999999:-4827.6 _clp_cinfo) ) _clpMKSConvert(5.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(1069.69:-4827.6 _clp_cinfo) _clpAdjustPt(998.8899999999999:-4827.6 _clp_cinfo) ) _clpMKSConvert(5.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(1069.69:-4819.7 _clp_cinfo) _clpAdjustPt(1069.69:-4827.6 _clp_cinfo) ) _clpMKSConvert(5.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(984.29:-4825 _clp_cinfo) _clpAdjustPt(969.29:-4825 _clp_cinfo) ) _clpMKSConvert(5.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(1096.79:-4825 _clp_cinfo) _clpAdjustPt(1081.79:-4825 _clp_cinfo) ) _clpMKSConvert(5.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(1089.29:-4817.5 _clp_cinfo) _clpAdjustPt(1089.29:-4832.5 _clp_cinfo) ) _clpMKSConvert(5.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(868.1900000000001:-4642.4 _clp_cinfo) _clpAdjustPt(868.1900000000001:-4697.6 _clp_cinfo) ) _clpMKSConvert(5.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(848.8899999999999:-4642.4 _clp_cinfo) _clpAdjustPt(848.8899999999999:-4650.3 _clp_cinfo) ) _clpMKSConvert(5.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(919.6900000000001:-4642.4 _clp_cinfo) _clpAdjustPt(848.8899999999999:-4642.4 _clp_cinfo) ) _clpMKSConvert(5.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(919.6900000000001:-4642.4 _clp_cinfo) _clpAdjustPt(919.6900000000001:-4650.3 _clp_cinfo) ) _clpMKSConvert(5.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(848.8899999999999:-4689.7 _clp_cinfo) _clpAdjustPt(848.8899999999999:-4697.6 _clp_cinfo) ) _clpMKSConvert(5.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(919.6900000000001:-4697.6 _clp_cinfo) _clpAdjustPt(848.8899999999999:-4697.6 _clp_cinfo) ) _clpMKSConvert(5.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(919.6900000000001:-4689.7 _clp_cinfo) _clpAdjustPt(919.6900000000001:-4697.6 _clp_cinfo) ) _clpMKSConvert(5.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(834.29:-4695 _clp_cinfo) _clpAdjustPt(819.29:-4695 _clp_cinfo) ) _clpMKSConvert(5.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(946.79:-4695 _clp_cinfo) _clpAdjustPt(931.79:-4695 _clp_cinfo) ) _clpMKSConvert(5.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(939.29:-4687.5 _clp_cinfo) _clpAdjustPt(939.29:-4702.5 _clp_cinfo) ) _clpMKSConvert(5.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(5024.29:-517 _clp_cinfo) _clpAdjustPt(5024.29:-663 _clp_cinfo) ) _clpMKSConvert(6.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(5294.29:-517 _clp_cinfo) _clpAdjustPt(5024.29:-517 _clp_cinfo) ) _clpMKSConvert(6.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(5294.29:-517 _clp_cinfo) _clpAdjustPt(5294.29:-663 _clp_cinfo) ) _clpMKSConvert(6.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(5294.29:-663 _clp_cinfo) _clpAdjustPt(5024.29:-663 _clp_cinfo) ) _clpMKSConvert(6.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(5139.29:-555 _clp_cinfo) _clpAdjustPt(5139.29:-625 _clp_cinfo) ) _clpMKSConvert(6.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(5179.29:-630 _clp_cinfo) _clpAdjustPt(5139.29:-590 _clp_cinfo) ) _clpMKSConvert(6.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(5179.29:-550 _clp_cinfo) _clpAdjustPt(5179.29:-630 _clp_cinfo) ) _clpMKSConvert(6.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(5179.29:-550 _clp_cinfo) _clpAdjustPt(5139.29:-590 _clp_cinfo) ) _clpMKSConvert(6.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(5024.29:-517 _clp_cinfo) _clpAdjustPt(5018.29:-517 _clp_cinfo) ) _clpMKSConvert(6.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(5018.29:-517 _clp_cinfo) _clpAdjustPt(5018.29:-663 _clp_cinfo) ) _clpMKSConvert(6.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(5024.29:-663 _clp_cinfo) _clpAdjustPt(5018.29:-663 _clp_cinfo) ) _clpMKSConvert(6.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_path = _clpPathStart(list(_clpAdjustPt(-1659.53:-6018.8 _clp_cinfo))                  
	_clpMKSConvert(15.000000 _clp_cinfo->t_from_units                  			_clp_cinfo->t_to_units))
_clp_path = _clpPathArcCenter(_clp_path _clpMKSConvert( 15.000000                   _clp_cinfo->t_from_units 
	_clp_cinfo->t_to_units)                   _clpAdjustPt(-1659.53:-6018.8 _clp_cinfo) nil
 	_clpAdjustPt(-1667.15:-6018.8 _clp_cinfo))
_clp_dbid = _clpDBCreatePath(_clp_path "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = caar(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-1700.15:-5504.8 _clp_cinfo) _clpAdjustPt(-1700.15:-5565.8 _clp_cinfo) ) _clpMKSConvert(5.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-1700.15:-5504.8 _clp_cinfo) _clpAdjustPt(-2100.15:-5504.8 _clp_cinfo) ) _clpMKSConvert(5.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-1887.15:-6104.8 _clp_cinfo) _clpAdjustPt(-1902.15:-6089.8 _clp_cinfo) ) _clpMKSConvert(5.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-1700.15:-6104.8 _clp_cinfo) _clpAdjustPt(-1887.15:-6104.8 _clp_cinfo) ) _clpMKSConvert(5.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_dbid = _clpDBCreateLine( list(_clpAdjustPt(-1700.15:-6042.8 _clp_cinfo) _clpAdjustPt(-1700.15:-6104.8 _clp_cinfo) ) _clpMKSConvert(5.000000 _clp_cinfo->t_from_units _clp_cinfo->t_to_units) "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = car(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

_clp_path = _clpPathStart(list(_clpAdjustPt(2329.56:-6825 _clp_cinfo))                  
	_clpMKSConvert(6.000000 _clp_cinfo->t_from_units                  			_clp_cinfo->t_to_units))
_clp_path = _clpPathArcCenter(_clp_path _clpMKSConvert( 6.000000                   _clp_cinfo->t_from_units 
	_clp_cinfo->t_to_units)                   _clpAdjustPt(2329.56:-6825 _clp_cinfo) nil
 	_clpAdjustPt(1891.22:-6825 _clp_cinfo))
_clp_dbid = _clpDBCreatePath(_clp_path "PACKAGE GEOMETRY/SILKSCREEN_TOP" 'line _clp_sym)

_clp_dbid = caar(_clp_dbid)
when(_clp_dbid _clpDBAddProp( _clp_dbid list(
	list("CLIP_DRAWING" _clp_clip_prop_value))))

printf(" 100 percent completed")
newline()

axlFlushDisplay()
