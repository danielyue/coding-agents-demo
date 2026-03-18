# Coding Agents Demo — NYC 311 Consulting Engagement

Demo materials for **L13: Coding Agents** (AI for Business, Georgia Tech Scheller).

Students use a coding agent (Claude Code, Gemini CLI, Codex CLI, or similar) to analyze real NYC public services data through four progressively complex tasks.

## Prerequisites

1. **Node.js 20+** — required by most coding agent CLIs
2. **A coding agent installed** — follow the [setup guide on the course website](https://ai-for-business.notion.site) to install one of:
   - [Claude Code](https://docs.anthropic.com/en/docs/claude-code) (`npm install -g @anthropic-ai/claude-code`)
   - [Gemini CLI](https://github.com/google-gemini/gemini-cli) (`npm install -g @anthropic-ai/claude-code` then follow Gemini docs)
   - [Codex CLI](https://github.com/openai/codex) (`npm install -g @openai/codex`)
   - [OpenCode](https://github.com/opencode-ai/opencode) (Go binary)

## Setup

```bash
git clone https://github.com/danielyue/coding-agents-demo.git
cd coding-agents-demo
bash setup.sh
```

## What's Here

| File / Folder | Description |
|---|---|
| `CLAUDE.md` | Project context file — describes the consulting scenario, data schema, and analysis goals. The agent reads this automatically. |
| `engagement-docs/` | Three real NYC government documents: Comptroller audit findings, Mayor's Management Report 311 data, State Comptroller monitoring tool findings. |
| `ops_data.csv` | 2,275 rows of real NYC 311 service request data (April–September 2025). 13 complaint types, 6 agencies, 5 boroughs. |
| `prompts/` | One prompt file per demo, matching the four principles covered in lecture. |
| `setup.sh` | Checks your environment and tells you if you're ready. |

## The Four Demos

Each prompt in `prompts/` maps to a principle from the lecture:

1. **Tool Use in a Loop** (`01-tool-use.md`) — Read documents, produce a findings memo
2. **Search Tools Build Context** (`02-context.md`) — Ask a strategic question, watch the agent find its own sources
3. **Agents Introspect and Extend** (`03-extensibility.md`) — Data analysis with auto-recovery from missing packages
4. **Climbing the Ladder of Abstraction** (`04-abstraction.md`) — Strategic synthesis across qualitative and quantitative sources

## Usage

Open your coding agent in this directory and either:

- Copy a prompt from `prompts/` and paste it
- Ask your own question about the NYC 311 data

The agent will read `CLAUDE.md` for context, then work through the task using the available files.

## Data Sources

- **ops_data.csv** — NYC 311 Service Requests via [NYC Open Data](https://data.cityofnewyork.us/Social-Services/311-Service-Requests-from-2010-to-Present/erm2-nwe9) (Socrata API). Stratified sample for analysis diversity.
- **engagement-docs/** — Synthesized from publicly available NYC Comptroller and Mayor's Management Report publications.
