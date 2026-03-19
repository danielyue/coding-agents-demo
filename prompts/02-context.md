# Demo 2: Search Tools Build Context — "Read the Room"

The agent searches for and reads files on its own. No files are specified in the prompt — the agent builds its own context through search.

## Prompt

```text
Read through all the files in engagement-docs/. Produce a structured findings memo with key themes and operational pain points. Write it to FINDINGS.md.
```

## What to Watch

- The agent reads CLAUDE.md first to understand the project context
- It searches/lists available files without being told which ones matter
- It reads all three engagement documents and cross-references them
- Connections between documents emerge unprompted (e.g., linking the comptroller's complaint-driven enforcement finding to 311 volume data)
- The output is structured around themes, not per-document summaries
- **The agent built its own context — you didn't copy-paste anything into the prompt**
