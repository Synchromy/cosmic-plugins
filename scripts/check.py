"""Checks every build must pass before it is submitted. Exit 1 on any failure.

- Listing copy fits each directory's limits.
- No em dash and no emoji in any text a person or a model reads.
- The skill gives no order to call a tool: no "always call", "must call", "call X first" or "at session start" wording.
- The skill names only tools in the listing tool set.
- Exactly 5 positive and 3 negative review cases, each with the fields OpenAI asks for.
- With --live <tools/list JSON file>: the listing tool set matches the demo Cosmic's tools/list, names and annotations.
"""
import json, re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
fail = []


def check(ok, msg):
    if not ok:
        fail.append(msg)


copy = json.loads((ROOT / 'core/copy.json').read_text())
LIMITS = {'name': 30, 'short': 30, 'one_line': 200, 'description': 2000}
for key, n in LIMITS.items():
    check(len(copy[key]) <= n, f'copy.{key} is {len(copy[key])} characters, over {n}')
check(len(copy['default_prompts']) <= 3, 'more than 3 default prompts')
for p in copy['default_prompts']:
    check(len(p) <= 128, f'default prompt over 128 characters: {p}')

texts = [ROOT / 'core/copy.json', ROOT / 'core/skills/cosmic/SKILL.md', ROOT / 'README.md', ROOT / 'core/review/cases.json']
EMOJI = re.compile('[\U0001F300-\U0001FAFF☀-➿]')
for f in texts:
    if f.exists():
        t = f.read_text()
        check('—' not in t, f'{f.relative_to(ROOT)} has an em dash')
        check(not EMOJI.search(t), f'{f.relative_to(ROOT)} has an emoji')

skill = (ROOT / 'core/skills/cosmic/SKILL.md').read_text()
ORDERS = re.compile(r'\b(always (call|use|search)|must (call|use)|call \w+ first|at (the )?session start|before (any|every) (answer|reply|external))\b', re.I)
for m in ORDERS.finditer(skill):
    check(False, f'skill gives an order: "{m.group(0)}"')

tools = json.loads((ROOT / 'core/review/tools.json').read_text())['tools']
names = {t['name'] for t in tools}
for t in tools:
    a = t.get('annotations', {})
    for h in ('readOnlyHint', 'destructiveHint', 'openWorldHint'):
        check(isinstance(a.get(h), bool), f'{t["name"]} lacks an explicit {h}')
    check(bool(t.get('title')), f'{t["name"]} has no title')
for name in set(re.findall(r'`([a-z][a-z_]+)`', skill)):
    if '_' in name or name in {'search', 'query', 'entity', 'recall', 'remember', 'capture', 'whoami'}:
        check(name in names or name in {'include_content', 'prompt_context'} | names,
              f'skill names {name}, which is not in the listing tool set')

cases = json.loads((ROOT / 'core/review/cases.json').read_text())
check(len(cases['positive']) == 5, 'need exactly 5 positive review cases')
check(len(cases['negative']) == 3, 'need exactly 3 negative review cases')
for c in cases['positive'] + cases['negative']:
    for k in ('id', 'prompt', 'tools_triggered', 'expected_behavior'):
        check(k in c, f'case {c.get("id")} lacks {k}')

if '--live' in sys.argv:
    live = json.loads(Path(sys.argv[sys.argv.index('--live') + 1]).read_text())
    live_tools = {t['name']: t for t in live.get('tools', live.get('result', {}).get('tools', []))}
    check(set(live_tools) == names, f'live tools/list differs: missing {sorted(names - set(live_tools))}, extra {sorted(set(live_tools) - names)}')
    for t in tools:
        lt = live_tools.get(t['name'])
        if lt:
            la = lt.get('annotations', {})
            check(all(la.get(h) == v for h, v in t['annotations'].items()),
                  f'{t["name"]} annotations differ from the live server')

if fail:
    print('\n'.join('FAIL ' + f for f in fail))
    sys.exit(1)
print(f'ok: copy, skill, {len(tools)} tools, {len(cases["positive"])}+{len(cases["negative"])} review cases')
