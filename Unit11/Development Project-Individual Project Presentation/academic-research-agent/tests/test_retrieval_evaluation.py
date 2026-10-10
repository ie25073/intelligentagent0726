import json
import unittest

from tools.evaluate_retrieval import IDENTIFIER_NOTE, QUERIES, evaluate, write_markdown


class RetrievalEvaluationTests(unittest.TestCase):
    def test_reports_plain_synthetic_identifiers(self) -> None:
        results = evaluate()

        self.assertEqual("synthetic_fixture_identifier", results["identifier_type"])
        self.assertEqual(IDENTIFIER_NOTE, results["identifier_note"])
        expected_rankings = (
            ["10.1000/agent.1", "10.1000/agent.3", "10.1000/agent.2"],
            ["10.1000/agent.2", "10.1000/agent.1", "10.1000/agent.3"],
            ["10.1000/agent.3", "10.1000/agent.1", "10.1000/agent.2"],
            ["10.1000/agent.1", "10.1000/agent.2", "10.1000/agent.3"],
        )
        for case, labelled, ranking in zip(results["cases"], QUERIES, expected_rankings):
            with self.subTest(query=labelled.query):
                self.assertEqual(labelled.query, case["query"])
                self.assertEqual(ranking, case["ranked_fixture_identifiers"])
                self.assertEqual(
                    [doi.removeprefix("https://doi.org/") for doi in labelled.relevant_dois],
                    case["relevant_fixture_identifiers"],
                )
                self.assertNotIn("ranked_dois", case)
                self.assertNotIn("relevant_dois", case)
        self.assertNotIn("https://doi.org/", json.dumps(results))

    def test_metrics_and_expected_top_results_are_unchanged(self) -> None:
        results = evaluate()

        self.assertEqual(4, results["case_count"])
        self.assertEqual(1.0, results["mean_precision_at_1"])
        self.assertEqual(0.5, results["mean_precision_at_3"])
        self.assertEqual(1.0, results["mean_ndcg_at_3"])
        self.assertGreaterEqual(results["mean_precision_at_1"], 0.75)
        self.assertGreaterEqual(results["mean_ndcg_at_3"], 0.85)
        self.assertTrue(results["single_relevance_top_passed"])
        for index, case in enumerate(results["cases"]):
            with self.subTest(query=case["query"]):
                self.assertEqual(1.0, case["precision_at_1"])
                self.assertEqual(0.3333 if index < 3 else 1.0, case["precision_at_3"])
                self.assertEqual(1.0, case["ndcg_at_3"])
                self.assertTrue(case["expected_top_met"])

    def test_markdown_labels_identifiers_and_includes_note_near_top(self) -> None:
        markdown = write_markdown(evaluate())

        self.assertEqual(IDENTIFIER_NOTE, markdown.splitlines()[2])
        self.assertEqual(4, markdown.count("- Ranked synthetic fixture identifiers:"))
        for identifier in ("10.1000/agent.1", "10.1000/agent.2", "10.1000/agent.3"):
            self.assertEqual(4, markdown.count(f"`{identifier}`"))
        self.assertNotIn("Ranked DOIs:", markdown)
        self.assertNotIn("https://doi.org/", markdown)


if __name__ == "__main__":
    unittest.main()
