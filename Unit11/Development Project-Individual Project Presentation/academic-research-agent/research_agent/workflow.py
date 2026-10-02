"""Bounded multi-agent research workflow."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from .models import Work, WorkflowTrace
from .planner import Planner
from .processor import ProcessingAgent
from .retriever import Retriever
from .storage import StorageAgent


@dataclass(frozen=True)
class WorkflowResult:
    works: tuple[Work, ...]
    output_paths: dict[str, Path]
    trace: WorkflowTrace


class ResearchWorkflow:
    """Coordinate specialist agents with an explicit maximum cycle count."""

    def __init__(
        self,
        planner: Planner,
        retriever: Retriever,
        processor: ProcessingAgent | None = None,
        storage: StorageAgent | None = None,
        max_cycles: int = 3,
        minimum_results: int = 3,
        results_per_query: int = 5,
    ) -> None:
        if not 1 <= max_cycles <= 3:
            raise ValueError("max_cycles must be between 1 and 3")
        self.planner = planner
        self.retriever = retriever
        self.processor = processor or ProcessingAgent()
        self.storage = storage or StorageAgent()
        self.max_cycles = max_cycles
        self.minimum_results = minimum_results
        self.results_per_query = results_per_query

    def run(self, goal: str, output_directory: Path) -> WorkflowResult:
        trace = WorkflowTrace()
        plan = self.planner.create_plan(goal)
        trace.record("planning", "created_plan", task_count=len(plan.tasks))
        collected: list[Work] = []
        ranked: list[Work] = []

        # The hard upper bound is a safety control: evidence scarcity may refine
        # a search, but it cannot create an uncontrolled retrieval loop.
        for cycle in range(1, self.max_cycles + 1):
            trace.record("orchestrator", "started_cycle", cycle=cycle)
            refinement = "" if cycle == 1 else f" evaluation cycle {cycle}"
            for task in plan.tasks:
                query = f"{task.query}{refinement}"
                try:
                    retrieved = self.retriever.search(query, self.results_per_query)
                    collected.extend(retrieved)
                    trace.record(
                        "retrieval",
                        "completed_search",
                        query=query,
                        result_count=len(retrieved),
                    )
                except (OSError, TimeoutError, ValueError, KeyError) as error:
                    trace.record(
                        "retrieval",
                        "search_failed",
                        query=query,
                        error=type(error).__name__,
                    )

            ranked = self.processor.process(plan.goal, collected)
            trace.record(
                "processing",
                "ranked_evidence",
                retained_count=len(ranked),
            )
            if len(ranked) >= self.minimum_results:
                trace.record("orchestrator", "sufficiency_reached", cycle=cycle)
                break
            trace.record("orchestrator", "refinement_required", cycle=cycle)

        output_paths = self.storage.save(output_directory, plan.goal, ranked, trace)
        trace.record("storage", "saved_outputs", files=len(output_paths))
        output_paths["trace"].write_text(
            __import__("json").dumps(trace.events, indent=2), encoding="utf-8"
        )
        return WorkflowResult(tuple(ranked), output_paths, trace)