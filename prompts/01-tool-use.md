# Demo 1: Tool Use in a Loop — "Watch the Loop"

This demo is the setup step. Students use Claude Code to clone this repo — illustrating the most basic tool loop: the agent reads a URL, runs git, and writes files to disk.

## Instructions

In Claude Code (or your coding agent), paste:

```text
Clone the repo at https://github.com/danielyue/coding-agents-demo.git into a local directory and run the setup script.
```

## What to Watch

- The agent runs `git clone` — a bash tool call
- It may run `bash setup.sh` to check your environment
- It may read the README or CLAUDE.md to orient itself
- The entire interaction is a tool loop: think → act (git clone) → observe (files on disk) → act (run setup) → observe (output)
- **This is the simplest possible agent task — but it's still the ReAct pattern**
