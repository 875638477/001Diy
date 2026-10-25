"""Synthetic negative controls for native-affine binding; never opens CAD."""
import argparse,csv,json,pathlib,subprocess,sys,uuid,hashlib,contextlib,xml.etree.ElementTree as E
sys.path.insert(0,str(pathlib.Path(__file__).resolve().parent))
from native_affine import read_frames,bind_part,apply_frame

def expect_error(fn):
    try:fn()
    except ValueError:return
    raise AssertionError('Expected unsafe frame binding to be rejected')

@contextlib.contextmanager
def temporary_directory(parent):
    parent=parent.resolve();root=parent/('capture_affine_selftest_'+uuid.uuid4().hex)
    root.mkdir(mode=0o777)
    try:yield root
    finally:
        assert root.resolve().parent==parent and root.name.startswith('capture_affine_selftest_')
        for child in root.iterdir():
            assert child.is_file();child.unlink()
        root.rmdir()

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--temp-root',type=pathlib.Path,default=pathlib.Path.cwd());args=parser.parse_args()
    columns='page id ref rotation mirror ox oy frame_origin_x frame_origin_y a_xx a_xy a_yx a_yy offset_x offset_y'.split()
    with temporary_directory(args.temp_root) as temp:
        root=pathlib.Path(temp);p=root/'frames.tsv'
        row=dict(zip(columns,['SYNTH','1','R1','1','0','100','200','100','220','0','1','-1','0','0','20']))
        def write(r):
            with p.open('w',encoding='utf-8',newline='') as f:
                w=csv.DictWriter(f,fieldnames=columns,delimiter='\t');w.writeheader();w.writerow(r)
        write(row);frames=read_frames(p);owner={'dbId':'1','rotation':'1','mirror':'0','locX':'100','locY':'200'}
        bound=bind_part(owner,'SYNTH',frames)
        assert apply_frame(-10,10,bound,lambda *args: (_ for _ in ()).throw(AssertionError('must not use legacy')))==[110,230]
        expect_error(lambda:bind_part(owner,'SYNTH',{}))
        expect_error(lambda:bind_part(dict(owner,locX='105'),'SYNTH',frames))
        bad=dict(row,offset_y='0');write(bad);expect_error(lambda:read_frames(p))
        bad=dict(row,a_yx='0');write(bad);expect_error(lambda:read_frames(p))
        # Old origin-rebase protocol must refuse a nonzero part pose before editing.
        xml=root/'nonzero.xml';xml.write_text('<Design><Schematic><Page><PartInst><Defn dbId="1" rotation="1" mirror="0"/></PartInst></Page></Schematic></Design>',encoding='utf-8')
        sha=hashlib.sha256(xml.read_bytes()).hexdigest().upper();cal=root/'legacy.json';cal.write_text(json.dumps({'status':'PASS','input_xml_sha256':sha,'point_transform':'MIRROR_X_THEN_CLOCKWISE_QUARTER_TURN','partinst_display_prop_transform':'ORIGIN_PLUS_LOCAL_NO_RM'}),encoding='utf-8')
        tool=pathlib.Path(__file__).resolve().parent.parent/'capture_xml_tools/symbol_origin_rebase.py';out=root/'out.xml'
        result=subprocess.run([sys.executable,str(tool),'--input',str(xml),'--output',str(out),'--expected-input-sha',sha,'--native-frame-calibration',str(cal)],capture_output=True,text=True)
        assert result.returncode!=0 and 'Legacy zero-pose rebase only' in result.stderr and not out.exists()
    print(json.dumps({'status':'PASS_SYNTHETIC_NATIVE_AFFINE_BINDING_CONTROLS','bbox_offset_regression':True,'missing_stale_invalid_frames_rejected':True,'legacy_nonzero_rebase_rejected_before_output':True,'CAD_started':False}))
if __name__=='__main__':main()
