# data-analyst — Data Sub-Agent

**Category:** Data
**Sub-agent file:** `sub-agent.md`

## What data-analyst Does

The data-analyst sub-agent analyzes structured data and returns a clear, actionable report in markdown. Give it a CSV file, JSON payload, or pasted table, and it returns:

- 📊 **Key metrics** — totals, averages, ranges
- 📈 **Trend analysis** — directional patterns and changes over time
- ⚠️ **Anomaly flags** — outliers, missing values, unexpected data
- 💡 **Insights and recommendations** — plain-language takeaways
- ❓ **Question answering** — ask a specific question about the data

## Compatible Parent Agents

- [Maxwell](../../../agents/professional/executive-assistant/) — for analyzing reports and business data

## Requirements

- Skill: `file-reader` (for reading uploaded CSV/JSON files)

## Direct Usage

You can also use this sub-agent directly:

- "Analyze this CSV: [paste data]"
- "What trends does this sales data show?"
- "Are there any anomalies in this dataset?"
- "Which region had the highest growth? [paste data]"

## Notes

data-analyst does not retain raw data between sessions. Completed analysis reports are returned to you and then discarded. For sensitive business data, verify that your OpenClaw memory settings are configured appropriately.
