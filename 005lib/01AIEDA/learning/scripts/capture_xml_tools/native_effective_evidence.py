"""Read hash-bound native effective-property evidence; never calls Capture."""
import csv,hashlib,json,pathlib,re

def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest().upper()
def unescape(value):return re.sub(r'\\([\\tnr])',lambda m:{'\\':'\\','t':'\t','n':'\n','r':'\r'}[m.group(1)],value)

def read_binding(path,reference_xml_sha256):
    binding=json.loads(path.read_text(encoding='utf-8-sig'))
    if binding.get('schema')!='CAPTURE_NATIVE_EFFECTIVE_PROPERTY_BINDING_V1' or binding.get('source_xml_sha256','').upper()!=reference_xml_sha256.upper():raise ValueError('Native effective evidence must bind this exact reference XML')
    rows={}
    for table in binding['tables']:
        file=pathlib.Path(table['path'])
        if sha(file)!=table['sha256'].upper():raise ValueError('Native effective table hash mismatch')
        for raw in csv.DictReader(file.open(encoding='utf-8-sig'),delimiter='\t'):
            key=(raw['instance_id'],unescape(raw['property']));row={k:raw[k] for k in ('read_failed','state_code','value','error')}
            if key in rows and rows[key]!=row:raise ValueError('Conflicting native effective evidence for '+str(key))
            rows[key]=row
    approved={}
    for item in binding.get('reviewed_undefined_results',[]):
        if not item.get('basis'):raise ValueError('An undefined-result exception requires reviewed native evidence')
        approved[(str(item['instance_id']),item['property'],str(item['state_code']))]=item['basis']
    return rows,approved

def resolve(rows,approved,instance_id,name):
    key=(str(instance_id),name)
    if key not in rows:raise ValueError('Missing native effective-property query: '+str(key))
    row=rows[key]
    if str(row['read_failed'])=='0':return {'defined':True,'value':unescape(row['value']),'state_code':row['state_code']}
    review_key=(*key,str(row['state_code']))
    if review_key not in approved:raise ValueError('Unreviewed native property read failure; never convert to empty or copy a raw library value: '+str(review_key))
    return {'defined':False,'state_code':row['state_code'],'basis':approved[review_key],'raw_failure_preserved':True}
