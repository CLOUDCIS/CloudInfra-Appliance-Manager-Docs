#!/usr/bin/env python3
"""Generate the control catalogue from the appliance's own control packs.

Written by hand, the catalogue would describe the controls somebody remembered shipping.
Generated from the YAML the appliance actually loads, it describes the ones it has.

Usage:
    python3 tools/generate-control-reference.py /path/to/CloudInfra-Appliance-Manager
"""
import sys
import pathlib
import re

SOURCE = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else '.')
OUT = pathlib.Path(__file__).resolve().parent.parent / 'docs' / 'reference' / 'controls.md'


def parse(path):
    """A deliberately small parser for the subset of YAML these packs use."""
    controls, current, key, section = [], None, None, None
    for raw in path.read_text().splitlines():
        stripped = raw.strip()
        if stripped.startswith('- id:'):
            if current:
                controls.append(current)
            current = {'id': stripped.split(':', 1)[1].strip()}
            key, section = None, None
            continue
        if current is None:
            continue

        # A nested key, two levels in. The one that matters is "supported" under
        # "remediation": whether the appliance can offer to fix this control.
        nested = re.match(r'^\s{6}(\w+):\s*(.*)$', raw)
        if nested and section == 'remediation':
            if nested.group(1) == 'supported':
                current['remediable'] = nested.group(2).strip() == 'true'
            continue

        m = re.match(r'^\s{4}(\w+):\s*(.*)$', raw)
        if m:
            key, value = m.group(1), m.group(2).strip()
            section = key
            if value in ('>-', '>', '|'):
                current[key] = ''
                continue
            if value:
                current[key] = value.strip('"\'')
                key = None
            continue
        if key and stripped and not stripped.endswith(':'):
            current[key] = (current.get(key, '') + ' ' + stripped).strip()
    if current:
        controls.append(current)
    return controls


def main():
    packs = sorted(SOURCE.glob('modules/*/controls/*.yaml'))
    if not packs:
        sys.exit(f'no control packs under {SOURCE}')

    by_category = {}
    total = 0
    for pack in packs:
        module = pack.parent.parent.name
        for control in parse(pack):
            if 'id' not in control:
                continue
            total += 1
            by_category.setdefault(control.get('category', 'Uncategorised'), []).append(
                (control, module))

    lines = [
        '# Control catalogue',
        '',
        f'The appliance ships **{total} controls** across {len(by_category)} categories.',
        '',
        'This page is generated from the control packs the appliance loads, so it describes',
        'the controls it has rather than the ones somebody remembered shipping. Regenerate it',
        'with `tools/generate-control-reference.py`.',
        '',
        'Severity is how much a failure costs the score. "Remediable" means the appliance can',
        'offer to fix it — see [Remediation](../guide/remediation.md) for why some cannot be.',
        '',
    ]

    for category in sorted(by_category):
        entries = sorted(by_category[category], key=lambda e: e[0]['id'])
        lines += [f'## {category}', '']
        lines += ['| ID | Control | Severity | Remediable |', '|---|---|---|---|']
        for control, _ in entries:
            remediable = 'Yes' if control.get('remediable') else '—'
            lines.append(
                f"| `{control['id']}` | {control.get('title', '')} "
                f"| {control.get('severity', '')} | {remediable} |")
        lines.append('')
        for control, module in entries:
            lines += [f"### {control['id']} — {control.get('title', '')}", '']
            if control.get('rationale'):
                lines += [control['rationale'], '']
            if control.get('recommendation'):
                lines += [f"**What to do:** {control['recommendation']}", '']
            lines += [f"*Module: `{module}`*", '']

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text('\n'.join(lines))
    print(f'wrote {OUT} ({total} controls, {len(by_category)} categories)')


if __name__ == '__main__':
    main()
