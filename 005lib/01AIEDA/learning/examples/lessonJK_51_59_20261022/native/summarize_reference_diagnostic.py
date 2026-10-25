from pathlib import Path
import csv,json,re,collections,hashlib
R=Path(r'D:\001DIY\005lib\01AIEDA\learning\examples\lessonJK_51_59_20261022');P=R/'logs/native_newstack_reference_segments_01/actual_path_segments.tsv'
r=list(csv.DictReader([l for l in P.read_text().splitlines() if not l.startswith('ACTUAL_PATH_SEGMENTS_COMPLETE')],delimiter='\t',quotechar='\0'))
q=R/'logs/native_newstack_reference_segments_01/newstack_reference_samples.tsv';s=list(csv.DictReader([l for l in q.read_text().splitlines() if not l.startswith('NEW_STACK_CENTERLINE_REFERENCE_SAMPLES_COMPLETE')],delimiter='\t',quotechar='\0'))
out={'status':'NONEMPTY_NATIVE_PATH_SEGMENT_AND_CENTERLINE_DIAGNOSTIC_NOT_HF_APPROVAL','segmentRows':len(r),'manual':sum(x['thermal']=='nil' for x in r),'thermal':sum(x['thermal']=='t' for x in r),'sampleRows':len(s),'referenceSampleCountByLayer':dict(collections.Counter(x['referenceLayer'] for x in s)),'zeroCommonPlaneSampleCountByLayer':dict(collections.Counter(x['referenceLayer'] for x in s if x['actualCommonPlaneCount']=='0')),'scope':'Sampling is actual point-in-filled-shape excludes voids, not full-width projection or HF impedance; independent engineering audit required','originalEmptySamplingEvidence':'NOT_EVIDENCE_RETAINED_UNCHANGED','correctedSupplementDirectory':str(P.parent)}
assert len(r)==932 and out['manual']==750 and out['thermal']==182 and len(s)==18854
(R/'native/reference_sample_diagnostic.json').write_text(json.dumps(out,indent=2),encoding='utf8')
print(json.dumps(out,indent=2))
