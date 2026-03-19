# Demo 4: Climbing the Ladder of Abstraction — "Connect the Dots"

The most complex demo. The agent orchestrates a multi-step investigation with iteration, self-critique, and sub-agent delegation. Use plan mode and let the agent decide its own investigation path.

## Prompt

```text
Use /plan mode. The city wants to reduce average resolution time by 30% without increasing headcount. You have audit reports in engagement-docs/ and 311 data in ops_data.csv. Develop three concrete recommendations. Each must cite BOTH qualitative and quantitative evidence. Write to RECOMMENDATIONS.md. Then use a subagent to critique it. Then plan how to solve the critiques, implement new analyses, and update RECOMMENDATIONS.md. Iterate until you hit a point of saturation.
```

## What to Watch

- **Plan mode:** The agent writes a plan before executing — you approve the investigation strategy
- **Cross-source synthesis:** The agent ping-pongs between qualitative documents and quantitative data
- **Sub-agent critique:** After writing recommendations, it spawns a sub-agent to critique its own work
- **Iteration:** It plans fixes for the critiques, runs new analyses, and updates the recommendations
- **Saturation:** The agent decides when further iteration won't improve the output
- **The human role:** You defined the problem and the process (plan → write → critique → iterate). The agent decided everything else — what to investigate, what data to pull, what analysis to run.
