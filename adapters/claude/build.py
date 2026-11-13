"""Build the Claude plugin from core/ into claude/ (committed, so Claude's directory can read it),
and the marketplace at .claude-plugin/marketplace.json.

Format: code.claude.com/docs/en/plugins/manifest-reference, hooks reference and
marketplace-reference (read 12 November 2026). One http server at the shared address, the cosmic
skill, and one UserPromptSubmit mcp_tool hook calling prompt_context on the plugin's own server.
No userConfig, no scripts, no command hooks.
"""
import json, shutil, sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common import ROOT, copy, skill_for, version  # noqa: E402

OUT = ROOT / 'claude'


def build() -> Path:
    c = copy()
    if OUT.exists():
        shutil.rmtree(OUT)
    (OUT / '.claude-plugin').mkdir(parents=True)
    (OUT / 'skills' / 'cosmic').mkdir(parents=True)
    (OUT / 'hooks').mkdir()
    (OUT / 'assets').mkdir()
    shutil.copy(ROOT / 'core' / 'assets' / 'cosmic.png', OUT / 'assets' / 'cosmic.png')
    shutil.copy(ROOT / 'LICENSE', OUT / 'LICENSE')
    shutil.copy(ROOT / 'adapters' / 'claude' / 'README.md', OUT / 'README.md')
    (OUT / 'skills' / 'cosmic' / 'SKILL.md').write_text(skill_for('claude'))
    plugin = {
        'name': c['slug'],
        'displayName': c['name'],
        'version': version(),
        'description': c['one_line'],
        'author': {'name': c['developer'], 'email': c['email'], 'url': c['urls']['website']},
        'homepage': c['urls']['docs'],
        'repository': c['urls']['repository'],
        'license': 'MIT',
        'keywords': ['memory', 'knowledge', 'context', 'notes', 'cosmic'],
        'icon': './assets/cosmic.png',
        'documentationUrl': c['urls']['docs'],
        'supportUrl': c['urls']['docs'],
        'privacyPolicyUrl': c['urls']['privacy'],
        'termsOfServiceUrl': c['urls']['terms'],
        'mcpServers': {'cosmic': {'type': 'http', 'url': c['server_url']}},
    }
    hooks = {
        'hooks': {
            'UserPromptSubmit': [{
                'hooks': [{
                    'type': 'mcp_tool',
                    'server': f'plugin:{c["slug"]}:cosmic',
                    'tool': 'prompt_context',
                    'input': {'prompt': '${prompt}', 'session_id': '${session_id}'},
                    'timeout': 10,
                }]
            }]
        }
    }
    (OUT / '.claude-plugin' / 'plugin.json').write_text(json.dumps(plugin, indent=2) + '\n')
    (OUT / 'hooks' / 'hooks.json').write_text(json.dumps(hooks, indent=2) + '\n')
    market = {
        'name': 'synchromy',
        'owner': {'name': c['developer'], 'email': c['email']},
        'description': "Synchromy's plugins for Claude.",
        'plugins': [{'name': c['slug'], 'source': './claude', 'description': c['one_line'], 'version': version()}],
    }
    (ROOT / '.claude-plugin').mkdir(exist_ok=True)
    (ROOT / '.claude-plugin' / 'marketplace.json').write_text(json.dumps(market, indent=2) + '\n')
    return OUT


if __name__ == '__main__':
    print(build())
