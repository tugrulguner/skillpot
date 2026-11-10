"""Structural checks for the explicit actions-template ATX report profile.

This test helper is not a semantic classifier, general Markdown parser or sandbox.
Independent grading maps source record keys to literal H3 lines. Category labels in
report bodies are never used to infer expected categories or physical placement.
"""
from collections import Counter
import re
from typing import Any

SECTIONS = {
    'assigned': 'Outstanding actions and requirements',
    'unassigned_requirement': 'Outstanding actions and requirements',
    'proposal': 'Proposals — not outstanding commitments',
    'historical': 'Historical items — not outstanding work',
    'unresolved': 'Unresolved items',
}


def placement_errors(text: str, expected_records: Any, record_map: Any) -> list[str]:
    """Check complete source-derived identity mapping and actual containing H2."""
    if not isinstance(text, str) or not isinstance(expected_records, list) or not expected_records:
        return ['invalid report or expected inventory']
    expected = {}
    for row in expected_records:
        if (not isinstance(row, dict) or not isinstance(row.get('key'), str) or not row['key'].strip()
                or not isinstance(row.get('category'), str) or row['category'] not in SECTIONS):
            return ['invalid expected record']
        if row['key'] in expected:
            return ['duplicate expected record']
        expected[row['key']] = row['category']
    if not isinstance(record_map, list):
        return ['invalid record map']
    mapped = {}
    for row in record_map:
        if (not isinstance(row, dict) or not isinstance(row.get('key'), str)
                or 'heading' not in row or (row['heading'] is not None and
                    (not isinstance(row['heading'], str) or not re.fullmatch(r' {0,3}###[ \t]+[^\r\n]+', row['heading'])))):
            return ['invalid record mapping']
        if row['key'] in mapped:
            return ['duplicate mapped key']
        mapped[row['key']] = row['heading']
    if set(mapped) != set(expected):
        return ['incomplete or unexpected mapping keys']
    present_headings = [heading for heading in mapped.values() if heading is not None]
    if len(set(present_headings)) != len(present_headings):
        return ['multiple source records mapped to one heading']

    current = None
    records = []
    section_counts = Counter()
    empty_sections = set()
    fence = None
    # Markdown physical lines are LF, CRLF or CR, not Unicode text separators.
    for line in text.replace('\r\n', '\n').replace('\r', '\n').split('\n'):
        delimiter = re.fullmatch(r' {0,3}(`{3,}|~{3,})(.*)', line)
        if fence is not None:
            if (delimiter and delimiter[1][0] == fence[0] and len(delimiter[1]) >= fence[1]
                    and not delimiter[2].strip()):
                fence = None
            continue
        if delimiter and (delimiter[1][0] != '`' or '`' not in delimiter[2]):
            fence = (delimiter[1][0], len(delimiter[1]))
            continue
        heading = re.fullmatch(r' {0,3}(#{1,6})(?:[ \t]+(.*))?', line)
        if heading:
            level = len(heading[1])
            if level == 1:
                current = None
            elif level == 2:
                title = (heading[2] or '').rstrip(' \t')
                current = re.sub(r'[ \t]+#+$', '', title).strip(' \t')
                section_counts[current] += 1
            elif level == 3:
                records.append((line, current))
        elif line.strip().rstrip('.') == 'None identified within the supplied scope':
            empty_sections.add(current)
    if any(section_counts[title] != 1 for title in set(SECTIONS.values())):
        return ['missing or duplicate category section']
    if any(section in empty_sections for _, section in records):
        return ['nonempty section marked empty']
    counts = Counter(heading for heading, _ in records)
    if set(counts) != set(present_headings) or any(count != 1 for count in counts.values()):
        return ['missing, duplicated or unmapped canonical record']
    containing = dict(records)
    errors = [f'{key}: missing canonical record' for key, heading in mapped.items() if heading is None]
    errors.extend(f'{key}: wrong containing section' for key, heading in mapped.items()
                  if heading is not None and containing[heading] != SECTIONS[expected[key]])
    return errors[:20]
