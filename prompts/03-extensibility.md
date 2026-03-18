# Demo 3: Agents Introspect and Extend — "Crunch the Numbers"

## Prompt

Analyze ops_data.csv — real NYC 311 data. Compute resolution times by complaint type and borough, identify worst performers, create visualizations, produce formatted Excel report. Look for patterns that explain why some categories take much longer.

## What to Watch

- The agent reads the CSV and understands the schema
- It writes and executes Python code for analysis
- When it hits a missing package (openpyxl, matplotlib), it installs it and retries
- Error recovery is the loop working as designed — "A script crashes; an agent adapts"
