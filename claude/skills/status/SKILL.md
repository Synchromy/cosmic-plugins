---
name: status
description: Show what this Cosmic connection can do, which sources it reads, and the session digest level.
disable-model-invocation: true
---

Show the person the state of their Cosmic connection.

1. Call `whoami` and report the access level (Read, or Read and add), which Cosmic this is, and the session digest level.
2. Call `cosmic_status` and report which sources are connected and how current each one is.
3. Call `sources_list` if a source the person asked about is not in that answer.

Keep it to a few lines. If a call is refused, say which one and why.
