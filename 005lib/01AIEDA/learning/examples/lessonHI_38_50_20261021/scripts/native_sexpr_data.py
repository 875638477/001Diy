"""Read canonical numeric/quoted-string SKILL data exports. No evaluation of code."""
import re,json
def parse(text):
 tokens=re.findall(r'\(|\)|"(?:[^"\\]|\\.)*"|[^\s()]+',text);i=0
 def one():
  nonlocal i
  token=tokens[i];i+=1
  if token=='(':
   out=[]
   while tokens[i]!=')':out.append(one())
   i+=1;return out
  if token.startswith('"'):return json.loads(token)
  if token=='nil':return None
  if token=='t':return True
  return float(token)
 out=one();assert i==len(tokens);return out