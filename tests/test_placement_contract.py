"""Synthetic parser controls only; these are not observed agent reports."""
import unittest
from placement_contract import placement_errors

SECTIONS = {
    'assigned': 'Outstanding actions and requirements',
    'unassigned_requirement': 'Outstanding actions and requirements',
    'proposal': 'Proposals — not outstanding commitments',
    'historical': 'Historical items — not outstanding work',
    'unresolved': 'Unresolved items',
}
RECORDS = [{'key': f'key-{n}', 'category': category}
           for n, category in enumerate(SECTIONS)]


def mapping(ids=None):
    ids = ids or ['X8', 'Zeta', 'R3', 'H4', 'U9']
    return [{'key': record['key'], 'heading': f'### {identity} — a synthetic record'}
            for record, identity in zip(RECORDS, ids)]


def fixture(ids=None, overrides=None):
    overrides = overrides or {}
    headings = {row['key']: row['heading'] for row in mapping(ids)}
    groups = {title: [] for title in dict.fromkeys(SECTIONS.values())}
    for record in RECORDS:
        category = overrides.get(record['key'], record['category'])
        groups[SECTIONS[category]].append(headings[record['key']] + '\n\n- Category: ' + record['category'] + '\n')
    parts = ['# Synthetic report\n']
    for title, entries in groups.items():
        parts.append('## ' + title + '\n\n' + '\n'.join(entries))
    return '\n'.join(parts)


class PlacementContractTests(unittest.TestCase):
    def test_complete_unique_inventory_and_mapping_are_required(self):
        text = fixture()
        maps = mapping()
        variants = [
            (text, RECORDS, maps[:-1]),
            (text, RECORDS, maps + [dict(maps[0])]),
            (text, RECORDS[:-1], maps),
            (text, RECORDS + [dict(RECORDS[0])], maps),
            (text, RECORDS, [dict(x, key='unexpected') if x['key'] == 'key-0' else x for x in maps]),
            (text, RECORDS, [dict(x, heading=maps[0]['heading']) if x['key'] == 'key-1' else x for x in maps]),
            (text.replace(maps[0]['heading'], maps[0]['heading'] + '\n\n' + maps[0]['heading']), RECORDS, maps),
            (text + '\n### EXTRA — unmapped record\n', RECORDS, maps),
        ]
        for index, (report, expected, record_map) in enumerate(variants):
            with self.subTest(mutation=index):
                try:
                    errors = placement_errors(report, expected, record_map)
                except (TypeError, KeyError, AttributeError):
                    self.fail('malformed inventory raised instead of returning a diagnostic')
                self.assertTrue(errors)
        self.assertEqual(placement_errors(text, RECORDS, maps), [])

    def test_required_sections_and_empty_markers_are_structural(self):
        text = fixture()
        for title in set(SECTIONS.values()):
            with self.subTest(duplicate_section=title):
                self.assertTrue(placement_errors(text + '\n## ' + title + '\n', RECORDS, mapping()))
        h = mapping()[0]['heading']
        self.assertTrue(placement_errors(text.replace(h, 'None identified within the supplied scope.\n\n' + h), RECORDS, mapping()))
        solo = '# Report\n\n## ' + SECTIONS['assigned'] + '\n\n' + h + '\n'
        self.assertTrue(placement_errors(solo, RECORDS[:1], mapping()[:1]))
        for title in list(dict.fromkeys(SECTIONS.values()))[1:]:
            solo += '\n## ' + title + '\n\nNone identified within the supplied scope.\n'
        self.assertEqual(placement_errors(solo, RECORDS[:1], mapping()[:1]), [])

    def test_fenced_and_quoted_headings_are_data_and_h1_resets_context(self):
        text = fixture()
        snippets = [
            '\n```md\n## Unknown\n### Ghost\n```\n',
            '\n~~~text\n## Unknown\n### Ghost\n~~~\n',
            '\n````md\n```\n## Unknown\n### Ghost\n````\n',
            '\n> ## Unknown\n> ### Ghost\n',
        ]
        for snippet in snippets:
            with self.subTest(snippet=snippet):
                self.assertEqual(placement_errors(text + snippet, RECORDS, mapping()), [])
        h = mapping()[2]['heading']
        self.assertTrue(placement_errors(text.replace(h, '# Another document\n\n' + h), RECORDS, mapping()))

    def test_wrong_sections_reject_every_record_with_unchanged_category_labels(self):
        for record in RECORDS:
            for wrong in SECTIONS:
                if SECTIONS[wrong] != SECTIONS[record['category']]:
                    with self.subTest(key=record['key'], wrong=wrong):
                        text = fixture(overrides={record['key']: wrong})
                        self.assertTrue(placement_errors(text, RECORDS, mapping()))
        self.assertEqual(placement_errors(fixture(), RECORDS, mapping()), [])

    def test_malformed_metadata_returns_bounded_diagnostics(self):
        for expected, maps in [(None, mapping()), ('bad', mapping()), ([None], mapping()),
                               ([{'key': [], 'category': 3}], mapping()), (RECORDS, None),
                               (RECORDS, [None]), (RECORDS, [{'key': [], 'heading': '### X'}])]:
            with self.subTest(expected=expected, maps=maps):
                errors = placement_errors(fixture(), expected, maps)
                self.assertTrue(errors)
                self.assertLessEqual(len(errors), 20)

    def test_indented_atx_headings_do_not_hide_wrong_containing_sections(self):
        for spaces in (1, 2, 3):
            prefix = ' ' * spaces
            text = fixture().replace('\n##', '\n' + prefix + '##')
            maps = [dict(row, heading=prefix + row['heading']) for row in mapping()]
            self.assertEqual(placement_errors(text, RECORDS, maps), [])
        h = mapping()[0]['heading']
        wrong = fixture().replace(h, '  ## Other section\n\n' + h)
        self.assertTrue(placement_errors(wrong, RECORDS, mapping()))

    def test_unicode_separators_do_not_create_markdown_heading_lines(self):
        for separator in ('\u2028', '\u2029', '\u0085'):
            with self.subTest(separator=repr(separator)):
                title = '## ' + SECTIONS['assigned']
                hidden = fixture().replace(title, 'Literal paragraph' + separator + title)
                self.assertTrue(placement_errors(hidden, RECORDS, mapping()))
                literal = fixture() + '\nLiteral paragraph' + separator + '### Not a record\n'
                self.assertEqual(placement_errors(literal, RECORDS, mapping()), [])
        self.assertEqual(placement_errors(fixture().replace('\n', '\r'), RECORDS, mapping()), [])

    def test_missing_record_marker_keeps_independent_placement_diagnostics(self):
        maps = mapping()
        report = fixture(overrides={'key-4': 'assigned'})
        report = report.replace(maps[2]['heading'] + '\n\n- Category: proposal\n', '')
        missing_maps = [dict(row, heading=None) if i == 2 else row for i, row in enumerate(maps)]
        errors = placement_errors(report, RECORDS, missing_maps)
        self.assertTrue(any('missing canonical record' in error for error in errors))
        self.assertTrue(any('wrong containing section' in error for error in errors))

    def test_valid_records_accept_arbitrary_id_schemes_and_crlf(self):
        for ids in (['X8', 'Zeta', 'R3', 'H4', 'U9'], ['B74', 'Alpha', 'N9', 'Old1', 'Pending2']):
            with self.subTest(ids=ids):
                self.assertEqual(placement_errors(fixture(ids), RECORDS, mapping(ids)), [])
                self.assertEqual(placement_errors(fixture(ids).replace('\n', '\r\n'), RECORDS, mapping(ids)), [])
