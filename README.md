# Cosmic plugins

The official Cosmic packages for Claude (connector and plugin) and for OpenAI (ChatGPT and Codex), built from one source. Every package connects to the same address, `https://app.gocosmic.ai/mcp`, where the person signs in and picks their own Cosmic.

## Layout

- `core/`: written once and shared by every package.
  - `copy.json`: the name, descriptions, prompts and links.
  - `skills/cosmic/SKILL.md`: the skill. A block between `<!-- only: claude -->` and `<!-- end -->` goes into one package only.
  - `review/tools.json`: the listing tool set a directory install gets, with each tool's title and hints.
  - `review/cases.json`: five cases where Cosmic should be used and three where it should not.
  - `assets/`: the icon.
- `adapters/claude/build.py`: writes `claude/` (the plugin Claude's directory reads) and `.claude-plugin/marketplace.json`.
- `adapters/openai/build.py`: writes `dist/openai/` and `dist/cosmic-openai.zip` for platform.openai.com/plugins.
- `scripts/check.py`: the listing copy limits, no em dash or emoji, no orders to the model in the skill, every tool annotated, and the review case counts. With `--live <file>` it compares the tool set with a `tools/list` answer from the demo Cosmic.

## Build and check

```
python3 adapters/claude/build.py
python3 adapters/openai/build.py
python3 scripts/check.py
claude plugin validate claude --strict
claude plugin validate . --strict
```

CI runs the same and fails when `claude/` is not what the build writes.

## Adding an assistant

Add `adapters/<name>/build.py` that reads `core/` through `adapters/common.py`, and a CI step for it. `core/` does not change.
