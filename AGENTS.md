# AGENTS.md

## Cursor Cloud specific instructions

### Project overview
This repo contains a single Python project, the **Marine Business AI Agent**, located at
`Projects/AI Agent/` (note the space in the directory name — always quote the path). It is a
rule-based CLI/data-analysis tool that reads a local CSV
(`merged_central_current - merged_central.csv`) and produces sales-lead analysis and JSON reports.
There is no web server, database, cache, or queue — everything runs as one-shot CLI scripts.

### Environment
- Python dependencies are installed into a virtual environment at `/workspace/.venv` (the update
  script creates/refreshes it). Run scripts with `/workspace/.venv/bin/python`, or activate with
  `source /workspace/.venv/bin/activate`.
- System package `python3.12-venv` is required to create the venv; it is preinstalled in the VM
  snapshot, so the update script does not reinstall it.

### Running (all commands run from inside the `Projects/AI Agent/` directory)
The scripts reference the CSV by a relative filename, so they must be launched from that directory:
```bash
cd "Projects/AI Agent"
/workspace/.venv/bin/python demo.py                  # non-interactive demo -> writes demo_marine_report.json
/workspace/.venv/bin/python marine_business_agent.py # interactive menu (reads stdin; choices 1-7)
/workspace/.venv/bin/python test_csv.py              # CSV sanity check
```

### Notes / gotchas
- Running `demo.py` overwrites the tracked file `demo_marine_report.json`, and interactive
  "Export Report" overwrites `marine_analysis_report.json`. These are committed artifacts — use
  `git checkout -- <file>` to discard regenerated changes unless you intend to update them.
- There is no lint or automated test suite configured; `test_csv.py` is a manual sanity check, not a
  unit-test framework.
- pandas 3.x emits a `Pandas4Warning` deprecation notice from `marine_business_agent.py` (boolean/str
  `and` operations in `generate_sales_leads`). It is a warning only and does not affect output.
