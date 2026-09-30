import io
import json
import unittest

from research_agent.planner import OllamaPlanner, RuleBasedPlanner


class RuleBasedPlannerTests(unittest.TestCase):
    def test_creates_bounded_distinct_tasks(self) -> None:
        plan = RuleBasedPlanner().create_plan(
            "Explainable decisions in autonomous research agents"
        )

        self.assertEqual(3, len(plan.tasks))
        self.assertEqual(3, len({task.query for task in plan.tasks}))
        self.assertTrue(all(plan.goal in task.query for task in plan.tasks))

    def test_rejects_an_underspecified_goal(self) -> None:
        with self.assertRaisesRegex(ValueError, "at least eight"):
            RuleBasedPlanner().create_plan("AI")


class OllamaPlannerTests(unittest.TestCase):
    def test_accepts_a_schema_conforming_model_plan(self) -> None:
        model_content = {
            "tasks": [
                {"query": "agent provenance", "rationale": "Find evidence trails"},
                {"query": "agent evaluation", "rationale": "Find evaluation methods"},
            ]
        }
        response = io.BytesIO(
            json.dumps(
                {"message": {"content": json.dumps(model_content)}}
            ).encode("utf-8")
        )

        plan = OllamaPlanner(opener=lambda *_args, **_kwargs: response).create_plan(
            "Explainable decisions in autonomous research agents"
        )

        self.assertEqual(2, len(plan.tasks))
        self.assertEqual("agent provenance", plan.tasks[0].query)

    def test_falls_back_when_the_model_is_unavailable(self) -> None:
        def unavailable(*_args: object, **_kwargs: object) -> object:
            raise OSError("model endpoint unavailable")

        goal = "Explainable decisions in autonomous research agents"
        plan = OllamaPlanner(opener=unavailable).create_plan(goal)

        self.assertEqual(RuleBasedPlanner().create_plan(goal), plan)


if __name__ == "__main__":
    unittest.main()