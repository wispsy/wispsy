import unittest

from wispsy.reference import run_reference
from wispsy.tabular import markdown_report, normalization_pipeline, normalize_table, table_source


class TabularReferenceTests(unittest.TestCase):
    def test_explicit_workflow_preserves_typed_rows_and_source_contract(self):
        texts = [" HéLLo   WORLD ", "", "3  4"]
        table = normalize_table(texts)
        source = table_source(table)
        snapshot = source.query()
        self.assertEqual([column.type for column in snapshot.columns], ["text", "integer", "integer"])
        self.assertTrue(all(not column.writable for column in snapshot.columns))
        for row, text in zip(snapshot.rows, texts):
            expected = run_reference(text)
            self.assertEqual([cell.value for cell in row.cells], [expected["text"], expected["words"], expected["characters"]])
            self.assertIs(type(row.cells[1].value), int)
            self.assertIsNone(row.revision)
        self.assertEqual(source.query(search={"fields": ["text"], "term": "héllo"}).rows[0].key, snapshot.rows[0].key)
        table.set("A2", "changed")
        self.assertEqual(snapshot.rows[0].cells[0].value, "héllo world")
        self.assertEqual(source.query().rows[0].cells[0].value, "changed")
        source.close()

    def test_selected_markdown_consumer_escapes_data_and_detaches(self):
        rendered = markdown_report(["<script> | \\ hello"])
        self.assertIn("&lt;script&gt;", rendered)
        self.assertIn("\\|", rendered)
        self.assertNotIn("<script>", rendered)
        table = normalize_table(["hello"])
        document = table.to_document()
        table.set("A2", "changed")
        self.assertIn("hello", document.to_markdown())
        self.assertNotIn("changed", document.to_markdown())

    def test_bounded_linear_definition_and_validation(self):
        pipeline = normalization_pipeline(2)
        self.assertEqual(pipeline.steps[1].arguments["text"].step, "normalize-0")
        for count in (0, 65, True):
            with self.assertRaises(ValueError):
                normalization_pipeline(count)
        for values in (["okay", 1], [float("nan")], "not a list"):
            with self.assertRaises(ValueError):
                normalize_table(values)
