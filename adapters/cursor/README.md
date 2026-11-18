# Cosmic for Cursor

Cosmic is one memory of your work, kept by you, for every assistant you use. It reads the sources you connect, such as mail, calendar, meetings, tasks and files, and keeps pages about your work, the people in it and the decisions you make. This plugin brings your Cosmic into Cursor.

## What it adds

- **One MCP server, `cosmic`, at `https://app.gocosmic.ai/mcp`.** It searches, reads and adds to your Cosmic.
- **A skill, `cosmic`,** that describes how the tools fit together: searching your own work, picking up handoffs, reading a page before replacing it, and saving session digests at the level you chose.

## Setting it up

1. Install the plugin from the Cursor Marketplace.
2. Sign in when Cursor asks. You sign in at app.gocosmic.ai, pick your Cosmic if you have more than one, and press Allow on your Cosmic's own page. There you choose the access, Read or Read and add, and for Read and add whether sessions are saved as a summary or in full detail.
3. Nothing is stored in a file by this plugin. Cursor holds the sign-in.

You can change the access or the digest level, or disconnect Cursor, from the Agents page in your Cosmic at any time.

## What it sends, and where

Everything this plugin sends goes to your own Cosmic through app.gocosmic.ai, over HTTPS. The app passes each call to your Cosmic and keeps no tokens or message bodies. Nothing goes anywhere else.

- **Tool calls.** When Cursor's agent calls a Cosmic tool, the call and its arguments go to your Cosmic, and the answer comes back to the agent.
- **Session digests, if you chose them.** At Summary, the agent saves a short page per session: what was decided, done and left open, and who and what was involved, with no pasted text. At Detailed, the page also holds every turn of the session in full. At Read, nothing is saved.

The plugin has no hooks. It runs no programs on your computer, installs no packages and reads no files from it.

## Privacy and support

- Privacy policy: https://app.gocosmic.ai/privacy
- Terms: https://app.gocosmic.ai/terms
- Documentation: https://app.gocosmic.ai/docs/connector
- Support: hello@synchromy.ai

Published by Synchromy under the MIT License.
