"""Passive schema-1 reference shared by scripting and presentation consumers."""


def text_workflow_document() -> dict:
    """Return fresh data only; provider installation/activation belongs to the host."""
    return {"schema": 1, "name": "text-report", "version": "1", "steps": [
        {"id": "normalize", "capability": "text.normalize",
         "arguments": {"object": {"text": {"input": {"name": "text"}}}}},
        {"id": "report", "capability": "text.report",
         "arguments": {"object": {"text": {"ref": {"step": "normalize"}}}}},
    ], "outputs": {"object": {"report": {"ref": {"step": "report"}}}}}
