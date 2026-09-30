import json
import tempfile
import unittest
from pathlib import Path

from research_agent.planner import RuleBasedPlanner
from research_agent.processor import ProcessingAgent
from research_agent.retriever import FixtureRetriever
from research_agent.workflow import ResearchWorkflow


PROJECT_ROOT = Path(__file__).resolve().parent.parent
FIXTURE = PROJECT_ROOT / "tests" / "fixtures" / "openalex.json"


class ProcessingAgentTests(unittest.TestCase):
    def test_deduplicates_records_retrieved_for_multiple_queries(self) -> None:
        retriever = FixtureRetriever(FIXTURE)
        repeated = retriever.search("research agents", 3) * 2

        works = ProcessingAgent().process("autonomous research agents", repeated)

        self.assertEqual(3, len(works))
        self.assertGreaterEqual(works[0].relevance_score, works[-1].relevance_score)


class ResearchWorkflowTests(unittest.TestCase):
    def test_offline_run_persists_report_and_trace(self) -> None:
        workflow = ResearchWorkflow(
            RuleBasedPlanner(), FixtureRetriever(FIXTURE), minimum_results=3
        )
        with tempfile.TemporaryDirectory() as temporary_directory:
            result = workflow.run(
                "Explainable decisions in autonomous research agents",
                Path(temporary_directory),
            )

            self.assertEqual(3, len(result.works))
            self.assertTrue(all(path.exists() for path in result.output_paths.values()))
            report = json.loads(result.output_paths["json"].read_text())
            self.assertEqual(3, report["result_count"])
            self.assertTrue(
                any(event["action"] == "sufficiency_reached" for event in result.trace.events)
            )

    def test_stops_after_configured_cycles_when_evidence_is_insufficient(self) -> None:
        workflow = ResearchWorkflow(
            RuleBasedPlanner(),
            FixtureRetriever(FIXTURE),
            max_cycles=2,
            minimum_results=10,
        )
        with tempfile.TemporaryDirectory() as temporary_directory:
            result = workflow.run("Research agent safety", Path(temporary_directory))

        cycles = [
            event
            for event in result.trace.events
            if event["action"] == "started_cycle"
        ]
        self.assertEqual(2, len(cycles))


if __name__ == "__main__":
    unittest.main()