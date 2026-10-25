"""Read-only Windows GDI LOGFONT text outlines in schematic logical units.
This module neither loads Capture nor opens a design. It is a font-model backend;
Capture anchor/rotation/display semantics still require native render calibration.
"""
import argparse,ctypes as C,json,math,pathlib,sys
from ctypes import wintypes as W

class LOGFONTW(C.Structure):
    _fields_=[(n,W.LONG) for n in ['lfHeight','lfWidth','lfEscapement','lfOrientation','lfWeight']]+[(n,W.BYTE) for n in ['lfItalic','lfUnderline','lfStrikeOut','lfCharSet','lfOutPrecision','lfClipPrecision','lfQuality','lfPitchAndFamily']]+[('lfFaceName',W.WCHAR*32)]
class SIZE(C.Structure):_fields_=[('cx',W.LONG),('cy',W.LONG)]
class TEXTMETRICW(C.Structure):
    _fields_=[(n,W.LONG) for n in ['tmHeight','tmAscent','tmDescent','tmInternalLeading','tmExternalLeading','tmAveCharWidth','tmMaxCharWidth','tmWeight','tmOverhang','tmDigitizedAspectX','tmDigitizedAspectY']]+[(n,W.WCHAR) for n in ['tmFirstChar','tmLastChar','tmDefaultChar','tmBreakChar']]+[(n,W.BYTE) for n in ['tmItalic','tmUnderlined','tmStruckOut','tmPitchAndFamily','tmCharSet']]

def _api():
    if sys.platform!='win32':raise RuntimeError('Windows GDI backend requires Windows')
    g=C.WinDLL('gdi32',use_last_error=True)
    specs={
      'CreateCompatibleDC':([W.HDC],W.HDC),'DeleteDC':([W.HDC],W.BOOL),
      'CreateFontIndirectW':([C.POINTER(LOGFONTW)],W.HFONT),'SelectObject':([W.HDC,W.HGDIOBJ],W.HGDIOBJ),'DeleteObject':([W.HGDIOBJ],W.BOOL),
      'SetBkMode':([W.HDC,C.c_int],C.c_int),'SetTextAlign':([W.HDC,W.UINT],W.UINT),'SetGraphicsMode':([W.HDC,C.c_int],C.c_int),
      'GetTextExtentPoint32W':([W.HDC,W.LPCWSTR,C.c_int,C.POINTER(SIZE)],W.BOOL),
      'GetTextMetricsW':([W.HDC,C.POINTER(TEXTMETRICW)],W.BOOL),'GetTextFaceW':([W.HDC,C.c_int,W.LPWSTR],C.c_int),
      'BeginPath':([W.HDC],W.BOOL),'EndPath':([W.HDC],W.BOOL),'TextOutW':([W.HDC,C.c_int,C.c_int,W.LPCWSTR,C.c_int],W.BOOL),
      'GetPath':([W.HDC,C.POINTER(W.POINT),C.POINTER(W.BYTE),C.c_int],C.c_int),
      'GetGlyphIndicesW':([W.HDC,W.LPCWSTR,C.c_int,C.POINTER(W.WORD),W.DWORD],W.DWORD)}
    for n,(a,r) in specs.items():f=getattr(g,n);f.argtypes=a;f.restype=r
    return g

def _flat_cubic(p0,p1,p2,p3,tol,out,depth=0):
    def distance(p,a,b):
        dx=b[0]-a[0];dy=b[1]-a[1]
        return abs(dx*(a[1]-p[1])-(a[0]-p[0])*dy)/math.hypot(dx,dy) if dx or dy else math.dist(p,a)
    if max(distance(p1,p0,p3),distance(p2,p0,p3))<=tol or depth>=24:out.append(p3);return
    def mid(a,b):return ((a[0]+b[0])/2,(a[1]+b[1])/2)
    a=mid(p0,p1);b=mid(p1,p2);c=mid(p2,p3);d=mid(a,b);e=mid(b,c);f=mid(d,e)
    _flat_cubic(p0,a,d,f,tol,out,depth+1);_flat_cubic(f,e,c,p3,tol,out,depth+1)

def _decode_path(points,types,scale,tol):
    contours=[];commands=[];ring=[];i=0;start=None;current=None
    def close():
        nonlocal ring
        if ring:
            if ring[-1]!=ring[0]:ring.append(ring[0])
            contours.append(ring);ring=[]
    while i<len(points):
        p=(points[i].x/scale,points[i].y/scale);typ=types[i];kind=typ&6
        if kind==6:
            close();start=current=p;ring=[p];commands.append(['M',*p]);i+=1
        elif kind==2:
            if current is None:raise ValueError('GDI line without initial move')
            ring.append(p);current=p;commands.append(['L',*p]);i+=1
            if typ&1:commands.append(['Z']);close();current=start
        elif kind==4:
            if current is None or i+2>=len(points) or any((types[j]&6)!=4 for j in range(i,i+3)):raise ValueError('Malformed GDI cubic path')
            p1=p;p2=(points[i+1].x/scale,points[i+1].y/scale);p3=(points[i+2].x/scale,points[i+2].y/scale)
            _flat_cubic(current,p1,p2,p3,tol,ring);commands.append(['C',*p1,*p2,*p3]);current=p3
            typ=types[i+2];i+=3
            if typ&1:commands.append(['Z']);close();current=start
        else:raise ValueError('Unsupported GDI path type '+str(typ))
    close();return contours,commands


def measure(text,font,scale=64,tolerance=.01,graphics_mode='compatible'):
    if any(ord(c)>0xffff for c in text):raise ValueError('Supplementary Unicode needs explicit UTF16 shaping support; not silently measured')
    if '\n' in text or '\r' in text:raise ValueError('Multiline layout requires explicit native line anchors')
    if not font.get('height'):raise ValueError('Zero/missing native font height cannot use a silent default')
    if scale<8 or tolerance<=0:raise ValueError('Invalid model precision')
    g=_api();hdc=g.CreateCompatibleDC(None)
    if not hdc:raise C.WinError(C.get_last_error())
    fobj=None;prior=None
    try:
        lf=LOGFONTW();mapping={'height':'lfHeight','width':'lfWidth','escapement':'lfEscapement','orientation':'lfOrientation','weight':'lfWeight','italic':'lfItalic','underline':'lfUnderline','strikeout':'lfStrikeOut','charset':'lfCharSet','out_precision':'lfOutPrecision','clip_precision':'lfClipPrecision','quality':'lfQuality','pitch_and_family':'lfPitchAndFamily'}
        defaults={'width':0,'escapement':0,'orientation':0,'weight':400,'italic':0,'underline':0,'strikeout':0,'charset':1,'out_precision':0,'clip_precision':0,'quality':0,'pitch_and_family':0}
        for key,field in mapping.items():
            value=font.get(key,defaults.get(key,0));value=round(value*scale) if key in ['height','width'] else int(value);setattr(lf,field,value)
        lf.lfFaceName=font.get('name','')[:31]
        g.SetGraphicsMode(hdc,1 if graphics_mode=='compatible' else 2);g.SetBkMode(hdc,1);g.SetTextAlign(hdc,24)
        fobj=g.CreateFontIndirectW(C.byref(lf))
        if not fobj:raise C.WinError(C.get_last_error())
        prior=g.SelectObject(hdc,fobj);size=SIZE();tm=TEXTMETRICW();face=C.create_unicode_buffer(128)
        if not g.GetTextExtentPoint32W(hdc,text,len(text),C.byref(size)):raise C.WinError(C.get_last_error())
        if not g.GetTextMetricsW(hdc,C.byref(tm)):raise C.WinError(C.get_last_error())
        g.GetTextFaceW(hdc,len(face),face);indices=(W.WORD*len(text))();ret=g.GetGlyphIndicesW(hdc,text,len(text),indices,1)
        missing=[dict(index=i,character=c,unicode=f'U+{ord(c):04X}') for i,c in enumerate(text) if ret==0xffffffff or indices[i]==0xffff]
        if not g.BeginPath(hdc) or not g.TextOutW(hdc,0,0,text,len(text)) or not g.EndPath(hdc):raise C.WinError(C.get_last_error())
        n=g.GetPath(hdc,None,None,0)
        if n<0:raise C.WinError(C.get_last_error())
        pts=(W.POINT*n)();typ=(W.BYTE*n)()
        if n and g.GetPath(hdc,pts,typ,n)!=n:raise C.WinError(C.get_last_error())
        contours,commands=_decode_path(pts,typ,scale,tolerance)
        flat=[q for ring in contours for q in ring];bounds=[min(q[0] for q in flat),min(q[1] for q in flat),max(q[0] for q in flat),max(q[1] for q in flat)] if flat else None
        metrics={n:getattr(tm,n)/scale for n in ['tmHeight','tmAscent','tmDescent','tmInternalLeading','tmExternalLeading','tmAveCharWidth','tmMaxCharWidth','tmOverhang']}
        supported=not missing and (bool(contours) or not text.strip())
        return dict(status='FONT_MODEL_READY_REQUIRES_CAPTURE_CALIBRATION' if supported else 'FONT_GLYPH_COVERAGE_REVIEW',text=text,font_requested=font,font_resolved=face.value,font_family_substituted=bool(lf.lfFaceName) and face.value.casefold()!=lf.lfFaceName.casefold(),missing_primary_font_glyphs=missing,graphics_mode=graphics_mode,coordinate_convention='left baseline at(0,0), x right, y down, before caller owner/display transform',supersample_scale=scale,path_coordinate_quantum=1/scale,bezier_flattening_tolerance=tolerance,advance_width=size.cx/scale,cell_height=size.cy/scale,metrics=metrics,ink_bounds=bounds,contours=contours,path_commands=commands,capture_pixel_render_verified=False)
    finally:
        if prior:g.SelectObject(hdc,prior)
        if fobj:g.DeleteObject(fobj)
        g.DeleteDC(hdc)

def main():
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--text',required=True);ap.add_argument('--font-json',required=True);ap.add_argument('--output',type=pathlib.Path,required=True);ap.add_argument('--scale',type=int,default=64);ap.add_argument('--tolerance',type=float,default=.01);ap.add_argument('--graphics-mode',choices=['compatible','advanced'],default='compatible');a=ap.parse_args()
    f=json.loads(a.font_json);r=measure(a.text,f,a.scale,a.tolerance,a.graphics_mode);a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_text(json.dumps(r,indent=2,ensure_ascii=False),encoding='utf-8');print(json.dumps({k:v for k,v in r.items() if k not in ['contours','path_commands','text']}))
if __name__=='__main__':main()