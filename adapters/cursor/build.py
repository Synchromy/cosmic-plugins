"""Build the Cursor plugin from core/ into cursor/ (committed, since the Cursor Marketplace reads the
repository) and the marketplace at .cursor-plugin/marketplace.json.

Format: cursor.com/docs/plugins and cursor.com/docs/reference/plugins (read 18 November 2026).
.cursor-plugin/plugin.json with a remote server at the shared address. Cursor signs in to remote
servers with OAuth and dynamic client registration by default (cursor.com/docs/mcp), so the entry
carries no auth block and no headers. The cosmic skill, no hooks, no rules, no programs.
"""
import json, shutil, sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common import ROOT, copy, skill_for, version  # noqa: E402

OUT = ROOT / 'cursor'


def build() -> Path:
    c = copy()
    if OUT.exists():
        shutil.rmtree(OUT)
    (OUT / '.cursor-plugin').mkdir(parents=True)
    (OUT / 'skills' / 'cosmic').mkdir(parents=True)
    (OUT / 'assets').mkdir()
    shutil.copy(ROOT / 'core' / 'assets' / 'cosmic.png', OUT / 'assets' / 'cosmic.png')
    shutil.copy(ROOT / 'LICENSE', OUT / 'LICENSE')
    shutil.copy(ROOT / 'adapters' / 'cursor' / 'README.md', OUT / 'README.md')
    (OUT / 'skills' / 'cosmic' / 'SKILL.md').write_text(skill_for('cursor'))
    plugin = {
        'name': c['slug'],
        'version': version(),
        'description': c['one_line'],
        'author': {'name': c['developer'], 'email': c['email']},
        'homepage': c['urls']['docs'],
        'repository': c['urls']['repository'],
        'license': 'MIT',
        'keywords': ['memory', 'knowledge', 'context', 'notes', 'cosmic'],
        'logo': 'assets/cosmic.png',
    }
    mcp = {'mcpServers': {'cosmic': {'url': c['server_url']}}}
    (OUT / '.cursor-plugin' / 'plugin.json').write_text(json.dumps(plugin, indent=2) + '\n')
    (OUT / 'mcp.json').write_text(json.dumps(mcp, indent=2) + '\n')
    market = {
        'name': 'synchromy',
        'owner': {'name': c['developer'], 'email': c['email']},
        'metadata': {'description': "Synchromy's plugins for Cursor."},
        'plugins': [{'name': c['slug'], 'source': 'cursor', 'description': c['one_line']}],
    }
    (ROOT / '.cursor-plugin').mkdir(exist_ok=True)
    (ROOT / '.cursor-plugin' / 'marketplace.json').write_text(json.dumps(market, indent=2) + '\n')
    return OUT


if __name__ == '__main__':
    print(build())
