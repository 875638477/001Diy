"""Bind the independently executed0010 private gates; no CAD or public writes."""
from pathlib import Path
import argparse, hashlib, json

M = Path(__file__).resolve().parent
H = '07A0F9340CBC89718BD586DEFCC270E299E24242C6AA7A6FA78973C220E82A42'
BOARD = M / 'public0010_original_thermal_restore_run13_v5_pending/PUB0010_ORIGINAL_THERMAL_UNAPPROVED.brd'
FULL = M / 'w/module0010_final_full28'
sha = lambda p: hashlib.sha256(Path(p).read_bytes()).hexdigest().upper()
read = lambda p: json.loads(Path(p).read_text('utf-8-sig'))

def need(v, s):
    if not v:
        raise ValueError(s)

SPECS = [
    ('finite_source21_Cu', 'public0010_original_thermal_restore_run13_v5_pending/FINITE_ORIGINAL21_THERMAL_CU_REVIEW_V5.json', '557B1C9CEB25003CEF37816A8D492D8A78427F7342EAD940B7A862FD5F270C5D', 'PASS_FINITE_SOURCE21_THERMAL_CU_PHASE_FRESH915_AND_CFX_REQUIRED'),
    ('all2698_and915_exact_partitions', 'public0010_final2698_partition_gate13_v4/FULL2698_ACTUAL_CONNECTION_PARTITION_REVIEW.json', '351E45BEFBECF7C150134D132716DFBE029226A3DF08B5192807CADC084BC73D', 'PASS_FULL2698_TYPED_PHYSICAL_CONNECTION_PARTITION_EXACT'),
    ('all593_pose_text_properties_fonts', 'public0010_final593_fresh_gate13_v1/FINAL_FULL593_SOURCE_FRESH_REVIEW.json', '145250E466A9D04FB1C3D42590499EFB38B8D66EEE2617D00ED2629D9ECC4BF2', 'PASS_FINAL_FRESH_FULL593_SOURCE_ONLY403_DEFINITION_NAMES'),
    ('all70_selected_full_graph_and_PAD', 'public0010_final_all70_cache_gate13_v2/ALL70_ACTUAL_CACHE_FULLGRAPH_CONTEXT_REVIEW.json', 'D9BD62DBE6D5E6D9474D0EF023F2EF7E6D8ED4D64C5133BBC71259C3963EEF23', 'PASS_ALL70_CACHED_DEFINITIONS_SIX_PUBLIC_FULLGRAPH_PAD_AND64_ORIGINAL_EXACT'),
    ('all79_full_native_typed_ID_bijection', 'w/module0010_final_full28/FRESH79_STRICT_TYPED_ID_BIJECTION_REVIEW_V3.json', '44E5C3A1E193B397F36D12A7D47DB87DD25432D4A6EC861E0268E5387061C982', 'PASS_FRESH_COMPLETE_NATIVE_CACHE_EXACT_EXPLICIT_TYPED_ID_BIJECTION'),
    ('actual101_device_bodies_and_classes', 'public0010_final_actual_body_gate13_v5/PUBLIC_MODULE_ACTUAL_NATIVE_DEVICE_BODY_REVIEW.json', '04BB39171E4855129853F0D604430F090F51C94B82D20349E5FFE7CE12CC0247', 'PASS_ALL_ACTUAL_NATIVE_DEVICE_BODIES_AND_SOURCE_CLASSES'),
    ('complete4_actual_feedback_views', 'public0010_final4views_gate13_v4/PUBLIC_MODULE_MAPPED_COMPLETE_VIEWS_REVIEW.json', '179DE28482017D37F80B40B996462EA67F371DF60ED8A30197565BD4A0D4A2A2', 'PASS_COMPLETE_PUBLIC_MODULE_VIEWS_ONLY_PLANNED_FP_AND_FUNCTION_IDS'),
    ('complete_source_CFX_TCFX', 'public0010_final_bounded_cfx_gate13_v6/PUBLIC0010_COMPLETE_CFX_REVIEW.json', 'AAB1C37F2B32E4078DB56FD7A3308BEB001F5BA34B68AEBCC9EF5A4EE8AA351B', 'PASS_FULL0010_SOURCE_CFX_TCFX_EXACT_WITH_ONE_NATIVE_READONLY_MAX_LEDGER'),
]

def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--out', type=Path, required=True)
    a = ap.parse_args()
    need(not a.out.exists() and a.out.resolve().is_relative_to(M.resolve()), 'Fresh maintenance output required')
    need(sha(BOARD) == sha(FULL / 'INPUT_COPY.brd') == H, 'Final private board changed')
    launch = read(FULL / 'launch_report.json')
    need(launch['source_sha256_before'] == launch['source_sha256_after'] == launch['staged_sha256'] == H and launch['input_unchanged'] and launch['exit_code'] == 0 and not launch['write_candidate'] and '-readonly' in launch['arguments'], 'Fresh final native job protection failed')
    records = []
    for role, name, expected_sha, expected_status in SPECS:
        p = M / name
        need(sha(p) == expected_sha, 'Frozen independent report changed: ' + role)
        q = read(p)
        need(q['status'] == expected_status, 'Independent report did not pass: ' + role)
        if 'candidate_board_sha256' in q:
            need(q['candidate_board_sha256'] == H, 'Report is for another board: ' + role)
        if 'candidate_sha256' in q:
            need(q['candidate_sha256'] == H, 'Report candidate is another board: ' + role)
        if role == 'complete4_actual_feedback_views':
            need([v for k, v in q['inputs'].items() if k.lower().endswith('.brd')] == [H], 'Actual feedback views are for another board')
        if role == 'all79_full_native_typed_ID_bijection':
            need(Path(q['after']).resolve() == (FULL / 'FINAL_ALL_CACHED_DEFINITION_GRAPHS.ilist').resolve(), 'Fresh79 graph is not final protected native output')
            need(sha(q['before']) == q['before_sha256'] and sha(q['after']) == q['after_sha256'], 'Complete79 native graph evidence changed')
            need(q['proof']['full_roots'] == 79 and q['proof']['full_objects'] == 20080, 'Complete79 object coverage differs')
        records.append(dict(role=role, path=str(p), sha256=expected_sha, status=q['status']))
    report = dict(
        status='PASS_BOUND_FINAL_PRIVATE0010_ALL_EXECUTED_INDEPENDENT_GATES',
        source_board_sha256='680500B07BC97F2B9D47064F83A01D0376AE43ADD486171F9B46087109E1B898',
        candidate_board=str(BOARD), candidate_board_sha256=H,
        native_readonly_directory=str(FULL), native_launch_sha256=sha(FULL / 'launch_report.json'),
        counts=dict(components=572, physical_symbols=593, typed_pads=2698, vias=1739, physical_connection_partitions=915, migrated_physical_components=403, actual_device_definitions=101),
        cache_scope=dict(selected_definitions=70, PACKAGE=59, MECHANICAL=6, FORMAT=5, additional_SHAPE=9, all_symdefs=79, SHAPE_nil_instances_does_not_imply_unused=True),
        public_package_scope=dict(new_public_exact=6, untouched_original_selected=64, old_existing_generic_not_replaced=4, internal_module_specific_not_claimed_externalized=60),
        proofs=records,
        only_CFX_administrative_ledger=dict(name='MAX_FILENAME_VALUE', source_native_readonly_STRING='20624', candidate_native_readonly_STRING='20635', whole_attribute_outer_position_bound=True, no_other_rule_origin_date_revision_exception=True),
        publication_or_retirement_approval=False,
        boundary='This index binds already executed independent private-file proofs. Public0010 replacement, final public guard and all reference closure remain separate root-owned publication steps.',
        summarizer_sha256=sha(__file__))
    a.out.mkdir()
    p = a.out / 'PUBLIC0010_FINAL_PRIVATE_EXECUTED_PROOFS_INDEX.json'
    p.write_text(json.dumps(report, indent=2) + '\n', 'utf-8')
    print(json.dumps(dict(status=report['status'], report=str(p), sha256=sha(p)), indent=2))

if __name__ == '__main__':
    main()
