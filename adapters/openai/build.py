"""Build the OpenAI plugin (ChatGPT and Codex) from core/ into dist/openai/ and dist/openai/cosmic.zip.

Format: developers.openai.com/plugins/build/plugins (read 12 November 2026).
Root plugin.json on the agent-plugins.org 1.0.0 schema with extensions["com.openai"].interface,
root mcp.json with one streamable-http server and OAuth by DCR, skills/ discovered from the root.
No hooks: a plugin with lifecycle hooks is not eligible for the public directory.
"""
import json, shutil, sys, zipfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common import ROOT, copy, skill_for, version  # noqa: E402

OUT = ROOT / 'dist' / 'openai'


def review() -> dict:
    """The review cases from core/review/cases.json in the shape the portal imports."""
    cases = json.loads((ROOT / 'core' / 'review' / 'cases.json').read_text())

    def case(x):
        return {
            'description': x['description'],
            'prompt': x['prompt'],
            'tools_triggered': ', '.join(x['tools_triggered']),
            'expected_behavior': x['expected_behavior'],
        }

    return {
        'test_cases': {'positive': [case(x) for x in cases['positive']], 'negative': [case(x) for x in cases['negative']]},
        'commerce': False,
        'commerce_description': 'Cosmic does not sell products or process payments.',
    }


def build() -> Path:
    c = copy()
    if OUT.exists():
        shutil.rmtree(OUT)
    (OUT / 'skills' / 'cosmic').mkdir(parents=True)
    (OUT / 'assets').mkdir()
    shutil.copy(ROOT / 'core' / 'assets' / 'cosmic.png', OUT / 'assets' / 'cosmic.png')
    shutil.copy(ROOT / 'LICENSE', OUT / 'LICENSE')
    (OUT / 'skills' / 'cosmic' / 'SKILL.md').write_text(skill_for('openai'))
    plugin = {
        '$schema': 'https://agent-plugins.org/schemas/1.0.0/plugin.schema.json',
        'name': c['slug'],
        'version': version(),
        'description': c['one_line'],
        'author': {'name': c['developer'], 'email': c['email'], 'url': c['urls']['website']},
        'homepage': c['urls']['docs'],
        'repository': c['urls']['repository'],
        'license': 'MIT',
        'keywords': ['memory', 'knowledge', 'context', 'notes', 'cosmic'],
        'extensions': {
            'com.openai': {
                'interface': {
                    'displayName': c['name'],
                    'shortDescription': c['short'],
                    'longDescription': c['description'],
                    'developerName': c['developer'],
                    'category': 'Productivity',
                    'capabilities': ['Read', 'Write'],
                    'websiteURL': c['urls']['website'],
                    'supportURL': c['urls']['docs'],
                    'privacyPolicyURL': c['urls']['privacy'],
                    'termsOfServiceURL': c['urls']['terms'],
                    'defaultPrompt': c['default_prompts'],
                    'brandColor': c['brand_color'],
                    'brandColorDark': c['brand_color'],
                    'composerIcon': './assets/cosmic.png',
                    'composerIconDark': './assets/cosmic.png',
                    'logo': './assets/cosmic.png',
                    'logoDark': './assets/cosmic.png',
                },
                'review': review(),
                'publication': {'release_notes': c['release_notes']},
            }
        },
    }
    mcp = {
        '$schema': 'https://agent-plugins.org/schemas/1.0.0/mcp.schema.json',
        'mcpServers': {
            'cosmic': {
                'type': 'streamable-http',
                'url': c['server_url'],
                'extensions': {'com.openai': {'auth': {'type': 'oauth', 'client': {'mode': 'dcr'}}}},
            }
        },
    }
    (OUT / 'plugin.json').write_text(json.dumps(plugin, indent=2, ensure_ascii=False) + '\n')
    (OUT / 'mcp.json').write_text(json.dumps(mcp, indent=2) + '\n')
    z = ROOT / 'dist' / 'cosmic-openai.zip'
    with zipfile.ZipFile(z, 'w', zipfile.ZIP_DEFLATED) as f:
        for p in sorted(OUT.rglob('*')):
            if p.is_file():
                f.write(p, p.relative_to(OUT))
    return OUT


if __name__ == '__main__':
    print(build())
