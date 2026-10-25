"""Small ordered-XML helpers for controlled template candidates; no CAD calls."""
import argparse, collections, copy, csv, hashlib, json, pathlib, re, xml.etree.ElementTree as E
D = lambda e: dict(e.find('Defn').attrib) if e is not None and e.find('Defn') is not None else {}

def C(e):
    return [e.tag, sorted(e.attrib.items()), (e.text or '').strip(), [C(x) for x in e], (e.tail or '').strip()]

def J(v):
    return json.dumps(v, ensure_ascii=True, separators=(',', ':'))

def H(e):
    return hashlib.sha256(J(C(e)).encode()).hexdigest().upper()

def FS(p):
    return hashlib.sha256(p.read_bytes()).hexdigest().upper()

def dump(p, x):
    p.write_text(json.dumps(x, ensure_ascii=False, indent=2), encoding='utf8')
VIEWS = {'NormalView', 'ConvertView'}
DEFAULT = {'SymbolUserProp', 'PartValue', 'Reference'}

def defaults(p):
    r = {}
    for ch in p.findall('PackageUserProp'):
        r.setdefault('Package/PackageUserProp/' + D(ch).get('name', ''), []).append(ch)
    for ci, lp, v in views(p):
        for ch in v:
            if ch.tag in DEFAULT | {'SymbolDisplayProp'}:
                name = D(ch).get('name', '') if ch.tag in {'SymbolUserProp', 'SymbolDisplayProp'} else ''
                r.setdefault('Cell[%d]/%s/%s/%s' % (ci, v.tag, ch.tag, name), []).append(ch)
    return r

def active(p, i):
    name = D(i.find('GraphicName')).get('name')
    a = [(ci, v.tag) for ci, lp, v in views(p) if D(lp)['CellName'] + D(v).get('suffix', '') == name]
    assert len(a) == 1, (D(i), a)
    return a[0]

def props(i, tag):
    r = collections.defaultdict(list)
    for x in i.findall(tag):
        r[D(x).get('name', '')].append(x)
    return r

def applies(k, av):
    return k.startswith('Package/') or k.startswith('Cell[%d]/%s/' % av)

def word(s):
    r = ''
    for c in s:
        r += {'\\': '\\\\', ' ': '\\ ', '{': '\\{', '}': '\\}', '\n': '\\n', '\r': '\\r', '\t': '\\t'}.get(c, c)
    return r or '{}'
