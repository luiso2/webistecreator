#!/usr/bin/env python3
"""Synchronize generated site artifacts and outreach messages by canonical language.

This is intentionally an artifact migration, not a registry overwrite. Run it first
without ``--apply`` to inspect the deterministic decision, then regenerate the HTML and
upsert only the corresponding unsent records through the panel's serialized endpoint.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / 'railway-forge'))

from contenido_script import decidir_idioma, generar_dm  # noqa: E402


def migrate(root: Path, slug: str, apply: bool) -> dict:
    site = root / slug
    data_path = site / 'data.json'
    content_path = site / 'content.json'
    if not data_path.exists() or not content_path.exists():
        return {'slug': slug, 'status': 'missing'}

    data = json.loads(data_path.read_text(encoding='utf-8'))
    content = json.loads(content_path.read_text(encoding='utf-8'))
    facts = {
        **data,
        'nombre': data.get('name') or content.get('brand', {}).get('name') or slug,
        'ciudad': data.get('ciudad') or data.get('city') or '',
        'nicho': data.get('nicho') or '',
    }
    decision = decidir_idioma(facts, fallback='en', usar_explicito=False)
    language = decision['language']
    url = f'https://siteforge-demos.odd-forest-9504.workers.dev/{slug}/'
    message = generar_dm({**facts, 'primary_language': language}, url, facts.get('nicho'))
    before_language = content.get('lang')
    before_message = content.get('dm_message') or ''
    changed = before_language != language or before_message != message

    if apply and changed:
        data.update({
            'idioma_principal': language,
            'primary_language': language,
            'language_source': decision['source'],
            'language_confidence': decision['confidence'],
        })
        content['lang'] = language
        content['dm_message'] = message
        data_path.write_text(json.dumps(data, ensure_ascii=False, indent=1) + '\n', encoding='utf-8')
        content_path.write_text(json.dumps(content, ensure_ascii=False, indent=1) + '\n', encoding='utf-8')

    return {
        'slug': slug,
        'status': 'changed' if changed else 'already_correct',
        'before_language': before_language,
        'language': language,
        'source': decision['source'],
        'confidence': decision['confidence'],
        'message_prefix': message[:24],
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument('slugs', nargs='+')
    parser.add_argument('--output-root', type=Path, default=REPO / 'output')
    parser.add_argument('--apply', action='store_true')
    args = parser.parse_args()
    results = [migrate(args.output_root, slug, args.apply) for slug in args.slugs]
    print(json.dumps({'apply': args.apply, 'results': results}, ensure_ascii=False, indent=2))
    if any(item['status'] == 'missing' for item in results):
        raise SystemExit(2)


if __name__ == '__main__':
    main()
