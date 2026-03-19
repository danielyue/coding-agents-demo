# Demo 3: Agents Introspect and Extend — "Crunch the Numbers"

The agent learns a new capability mid-task. Instead of using pandas (which it already knows), we ask it to use DuckDB — a tool it needs to research, install as a skill, and then use.

## Prompt

```text
I'd like you to analyze ops_data.csv using DuckDB instead of pandas. Can you research how to set up DuckDB as a skill or capability, install what you need, and then use it to compute resolution times by complaint type and borough? Identify the worst performers and look for patterns that explain why some categories take much longer. Produce a summary report.
```

## What to Watch

- The agent doesn't know DuckDB yet — watch it research how to use it
- It may read its own documentation, search the web, or inspect available MCP servers
- It installs DuckDB (pip install or skill/MCP setup) — extending its own capabilities mid-task
- It writes and runs DuckDB SQL queries against the CSV
- If something fails, it diagnoses the error and retries — the recursive loop in action
- **"A script crashes; an agent adapts." The agent expanded its own toolset to complete the task.**
