# Normalization to typed tables

Install the `table` profile on Python 3.14+. The base reference stays dependency
free on Python 3.11+.

```python
from wispsy.tabular import markdown_report, normalize_table, table_source
table = normalize_table([" Hello WORLD ", " More  WORDS "])
source = table_source(table)
snapshot = source.query(limit=50)
print(markdown_report([" Hello WORLD "]))
source.close()
```

Each selected input maps explicitly to a normalization step, then a report step.
The explicit rows output becomes Headless Spreadsheets Table.from_records; strings
and integer counts keep their types. The reference accepts 1–64 rows, within the
pipeline's 256-step and 1 MiB limits. No hidden coercion, provider activation,
persistence or table writes occur in the workflow.

TableSource reuses tabular/1 identity, detached snapshots, typed SourceColumn and
SourceRow cells, projection, bounded literal search and read-only capabilities.
In-memory identity is instance-local; rows have no durable revision. Source.close
releases this binding. No new revision/edit/transport contract is introduced.

The selected installed presentation is the existing detached TableDocument
Markdown renderer. It escapes data and does not parse Markdown or preserve types
on Markdown roundtrip. It is selected by calling markdown_report, independently
of persistence, HTTP and graphical adapters. Other applications can pass this same
TableSource into the established optional Expose API/Spatial UI table consumers;
those consumers retain their existing authorization, revision and transport rules.
They are not dependencies of this headless/Markdown profile. Hosting is separate.

The exact optional sources are recorded in pyproject.toml. Installed wheel/source
qualification checks typed headless execution, source snapshots, search and escaped
Markdown on Linux/macOS/Windows. This evidence does not qualify other versions or
claim a hosted application deployment.
