"""Synthetic controls for XML-derived pin plans and effective-default handling."""
import argparse,hashlib,json,pathlib,sys,uuid,xml.etree.ElementTree as E
sys.path.insert(0,str(pathlib.Path(__file__).resolve().parent))
from generate_pst_pin_declaration_plan import generate
sys.path.insert(0,str(pathlib.Path(__file__).resolve().parent/'capture_xml_tools'))
from native_effective_evidence import resolve

def error(fn):
    try:fn()
    except ValueError:return
    raise AssertionError('Expected rejection')
def fixture(path,numeric=False,bad_type=False):
    r=E.Element('Design');cache=E.SubElement(r,'Cache');p=E.SubElement(cache,'Package');E.SubElement(p,'Defn',{'name':'GENERIC'});lp=E.SubElement(p,'LibPart');E.SubElement(lp,'Defn',{'CellName':'GENERIC'});v=E.SubElement(lp,'NormalView');E.SubElement(v,'Defn',{'suffix':'.Normal'})
    # XML child order is deliberately reverse; only integer position sets PST order.
    mapping=[('1','2'),('0','1')] if numeric else [('1','1'),('0','2')]
    pp=E.SubElement(lp,'PhysicalPart')
    for pos,num in mapping:
        pin=E.SubElement(v,'SymbolPinScalar');E.SubElement(pin,'Defn',{'position':pos,'name':num if numeric else 'FUNC_'+num,'type':'7' if bad_type and num=='1' else '4','visible':'1'});E.SubElement(E.SubElement(pin,'IsGlobal'),'Defn',{'val':'0'});E.SubElement(pp,'PinNumber');pp[-1].append(E.Element('Defn',{'position':pos,'number':num}))
    page=E.SubElement(E.SubElement(r,'Schematic'),'Page');E.SubElement(page,'Defn',{'name':'SYNTH'});i=E.SubElement(page,'PartInst');E.SubElement(i,'Defn',{'dbId':'1','pkgName':'GENERIC'});E.SubElement(E.SubElement(i,'Reference'),'Defn',{'name':'U1'});E.SubElement(E.SubElement(i,'GraphicName'),'Defn',{'name':'GENERIC.Normal'});override=E.SubElement(i,'PortInstScalar');E.SubElement(override,'Defn',{'name':'DISPLAY_OVERRIDE'});E.SubElement(E.SubElement(override,'PortInstUserProp'),'Defn',{'name':'Name','val':'DISPLAY_OVERRIDE'});E.ElementTree(r).write(path,encoding='utf-8')
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--temp-root',type=pathlib.Path,default=pathlib.Path.cwd());a=ap.parse_args();parent=a.temp_root.resolve();temp=parent/('capture_template_selftest_'+uuid.uuid4().hex);temp.mkdir(mode=0o777)
    try:
        source=temp/'source.xml';target=temp/'target.xml';trace=temp/'trace.json';fixture(source);fixture(target,True);trace.write_text(json.dumps([{'ref':'U1','family':'GENERIC'}]),encoding='utf-8');report=generate(source,target,[trace]);p=report['references']['U1'];assert p['before']==[{'number':'2','name':'FUNC_2'},{'number':'1','name':'FUNC_1'}];assert p['after']==[{'number':'1','name':'1'},{'number':'2','name':'2'}];assert all(x['name']!='DISPLAY_OVERRIDE' for x in p['after'])
        fixture(target,True,True);error(lambda:generate(source,target,[trace]));trace.write_text(json.dumps([{'ref':'MISSING'}]),encoding='utf-8');error(lambda:generate(source,target,[trace]))
        key=('1','RAW_ONLY');rows={key:{'read_failed':'1','state_code':'NOT_FOUND','value':'','error':'absent'}};error(lambda:resolve(rows,{},*key));missing=resolve(rows,{(*key,'NOT_FOUND'):'Independently verified native undefined result'},*key);assert missing['defined'] is False and 'value' not in missing
        defined=resolve({key:{'read_failed':'0','state_code':'0','value':'','error':''}},{},*key);assert defined=={'defined':True,'value':'','state_code':'0'}
        assert resolve({key:{'read_failed':'0','state_code':'0','value':r'A\\B\tC','error':''}},{},*key)['value']=='A\\B\tC'
    finally:
        assert temp.resolve().parent==parent and temp.name.startswith('capture_template_selftest_')
        for p in temp.iterdir():assert p.is_file();p.unlink()
        temp.rmdir()
    print(json.dumps({'status':'PASS_SYNTHETIC_XML_DECLARATION_AND_EFFECTIVE_DEFAULT_CONTROLS','integer_position_not_child_order':True,'cache_name_not_instance_override':True,'electrical_change_and_unknown_ref_rejected':True,'failed_not_materialized_as_empty_or_raw_value':True,'defined_empty_preserved':True,'CAD_started':False}))
if __name__=='__main__':main()
