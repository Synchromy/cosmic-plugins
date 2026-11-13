# Cosmic for Claude

Cosmic is one memory of your work, kept by you, for every assistant you use. It reads the sources you connect, such as mail, calendar, meetings, tasks and files, and keeps pages about your work, the people in it and the decisions you make. This plugin brings your Cosmic into Claude Code, Cowork and claude.ai.

## What it adds

- **One MCP server, `cosmic`, at `https://app.gocosmic.ai/mcp`.** It searches, reads and adds to your Cosmic.
- **A skill, `cosmic`,** that describes how the tools fit together: searching your own work, picking up handoffs, reading a page before replacing it, and keeping session digests at the level you chose.
- **One hook, before each prompt, in Claude Code.** See "What it sends" below.

## Setting it up

1. Install the plugin. In Claude Code:

   ```
   /plugin marketplace add Synchromy/cosmic-plugins
   /plugin install cosmic@synchromy
   ```

   In claude.ai and Cowork, add Cosmic from the directory.
2. Sign in when Claude asks. You sign in at app.gocosmic.ai, pick your Cosmic if you have more than one, and press Allow on your Cosmic's own page. There you choose the access, Read or Read and add, and for Read and add whether sessions are kept as a summary or in full detail.
3. Nothing is stored in a file by this plugin. Claude holds the sign-in.

You can change the access or the digest level, or disconnect Claude, from the Agents page in your Cosmic at any time.

## What it sends, and where

Everything this plugin sends goes to your own Cosmic through app.gocosmic.ai, over HTTPS. The app passes each call to your Cosmic and keeps no tokens or message bodies. Nothing goes anywhere else.

- **Tool calls.** When Claude calls a Cosmic tool, the call and its arguments go to your Cosmic, and the answer comes back to Claude.
- **Each prompt, in Claude Code, before Claude answers it.** A `UserPromptSubmit` hook calls `prompt_context` on your Cosmic with the text of the prompt and the session id. Your Cosmic answers with what it already holds that bears on the prompt, and Claude reads it as context. To stop this, disable the plugin.
- **Session digests, if you chose them.** At Summary, Claude saves a short page per session: what was decided, done and left open, and who and what was involved, with no pasted text. At Detailed, the page also holds every turn of the session in full. At Read, nothing is saved.

The plugin runs no programs on your computer, installs no packages and reads no files from it.

## Privacy and support

- Privacy policy: https://app.gocosmic.ai/privacy
- Terms: https://app.gocosmic.ai/terms
- Documentation: https://app.gocosmic.ai/docs/connector
- Support: hello@synchromy.ai

Published by Synchromy under the MIT License.
