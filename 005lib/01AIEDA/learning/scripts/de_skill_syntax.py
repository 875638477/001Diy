"""Reject malformed generated SKILL before an owned native batch starts."""
def validate_skill(text):
    depth=0;quoted=False;escaped=False;comment=False
    for index,char in enumerate(text):
        if comment:
            if char=='\n':comment=False
            continue
        if quoted:
            if escaped:escaped=False
            elif char=='\\':escaped=True
            elif char=='"':quoted=False
            continue
        if char==';':comment=True
        elif char=='"':quoted=True
        elif char=='(':depth+=1
        elif char==')':
            depth-=1
            if depth<0:raise ValueError(f'Unexpected closing parenthesis at offset {index}')
    if quoted:raise ValueError('Unterminated SKILL string')
    if depth:raise ValueError(f'Unbalanced SKILL source: {depth} open parentheses')
