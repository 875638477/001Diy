from pathlib import Path
import re
import hashlib
import json

base = Path(__file__).resolve().parent
md = (base / 'lesson05_instances_notes_20261018.md').read_text(encoding='utf-8')
doc = Path('C:/Program0/Cadence/SPB172/doc')
refs = re.findall(r'((?:algroskill|algrolibdev|propref)/[A-Za-z0-9_.]+\.html)#([A-Za-z0-9_]+)', md)
missing = []
for file, anchor in refs:
    content = (doc / file).read_bytes()
    if ('name="' + anchor + '"').encode('ascii') not in content and ('id="' + anchor + '"').encode('ascii') not in content:
        missing.append(file + '#' + anchor)
il = (base / 'lesson06_native_operations_suggestion.il').read_text(encoding='utf-8')
depth = 0
state = 'code'
escaped = False
for c in il:
    if state == 'comment':
        if c == '\n':
            state = 'code'
    elif state == 'string':
        if escaped:
            escaped = False
        elif c == '\\':
            escaped = True
        elif c == '"':
            state = 'code'
    elif c == ';':
        state = 'comment'
    elif c == '"':
        state = 'string'
    elif c == '(':
        depth += 1
    elif c == ')':
        depth -= 1
    assert depth >= 0
assert depth == 0
assert state != 'string'
print(json.dumps({'note_lines': len(md.splitlines()), 'official_anchor_references': len(refs),
    'missing_anchors': missing, 'suggestion_il_parentheses_balanced': True,
    'cadence_execution': 'NOT PERFORMED', 'files': [
        {'name': p.name, 'bytes': p.stat().st_size,
         'sha256': hashlib.sha256(p.read_bytes()).hexdigest().upper()}
        for p in [base / 'lesson05_instances_notes_20261018.md',
                  base / 'lesson06_native_operations_suggestion.il']]}, indent=2))
assert not missing
