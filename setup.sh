#!/bin/bash
# Setup check for coding-agents-demo

echo "=== Coding Agents Demo — Environment Check ==="
echo ""

# Check Node.js
if command -v node &> /dev/null; then
    NODE_VERSION=$(node --version)
    echo "✓ Node.js installed: $NODE_VERSION"
else
    echo "✗ Node.js not found. Install from https://nodejs.org (v20+ recommended)"
fi

echo ""

# Check for coding agent CLIs
AGENT_FOUND=false

if command -v claude &> /dev/null; then
    echo "✓ Claude Code found: $(claude --version 2>/dev/null || echo 'installed')"
    AGENT_FOUND=true
fi

if command -v gemini &> /dev/null; then
    echo "✓ Gemini CLI found"
    AGENT_FOUND=true
fi

if command -v codex &> /dev/null; then
    echo "✓ Codex CLI found"
    AGENT_FOUND=true
fi

if command -v opencode &> /dev/null; then
    echo "✓ OpenCode found"
    AGENT_FOUND=true
fi

if [ "$AGENT_FOUND" = false ]; then
    echo "✗ No coding agent CLI found in PATH."
    echo "  Install one of: claude, gemini, codex, or opencode"
    echo "  See the course setup guide for instructions."
fi

echo ""

# Check for data files
if [ -f "ops_data.csv" ] && [ -d "engagement-docs" ]; then
    echo "✓ Data files present"
else
    echo "✗ Data files missing — make sure you cloned the full repo"
fi

echo ""

if [ "$AGENT_FOUND" = true ]; then
    echo "=== Ready! Open your coding agent in this directory and try a prompt from prompts/ ==="
else
    echo "=== Not ready — install a coding agent CLI first ==="
fi
