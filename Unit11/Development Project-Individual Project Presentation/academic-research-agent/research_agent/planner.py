"""Planning-agent implementations."""

from __future__ import annotations

import json
from collections.abc import Callable
from typing import Any, Protocol
from urllib.request import Request, urlopen

from .models import ResearchPlan, SearchTask


class Planner(Protocol):
    def create_plan(self, goal: str) -> ResearchPlan:
        """Convert a high-level goal into validated search tasks."""


class RuleBasedPlanner:
    """Create transparent, reproducible tasks without a model dependency."""

    _ASPECTS = (
        ("evidence", "Find empirical evidence and reported outcomes"),
        ("methods", "Identify methods, architectures and evaluation approaches"),
        ("risks limitations", "Find limitations, risks and unresolved questions"),
    )

    def create_plan(self, goal: str) -> ResearchPlan:
        normalised_goal = " ".join(goal.split())
        if len(normalised_goal) < 8:
            raise ValueError("The research goal must contain at least eight characters")

        tasks = tuple(
            SearchTask(
                query=f"{normalised_goal} {keywords}",
                rationale=rationale,
            )
            for keywords, rationale in self._ASPECTS
        )
        return ResearchPlan(goal=normalised_goal, tasks=tasks)


class OllamaPlanner:
    """Use an Ollama-compatible chat endpoint while enforcing local schemas."""

    def __init__(
        self,
        model: str = "qwen3:4b",
        endpoint: str = "http://localhost:11434/api/chat",
        opener: Callable[..., Any] = urlopen,
    ) -> None:
        self.model = model
        self.endpoint = endpoint
        self._opener = opener

    def create_plan(self, goal: str) -> ResearchPlan:
        fallback = RuleBasedPlanner().create_plan(goal)
        prompt = (
            "Return JSON only with a tasks array containing 2-5 objects. "
            "Each object must have query and rationale strings. Decompose this "
            f"academic research goal without answering it: {fallback.goal}"
        )
        payload = json.dumps(
            {
                "model": self.model,
                "stream": False,
                "format": "json",
                "messages": [{"role": "user", "content": prompt}],
            }
        ).encode("utf-8")
        request = Request(
            self.endpoint,
            data=payload,
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        try:
            with self._opener(request, timeout=30) as response:
                response_data = json.load(response)
            model_data = json.loads(response_data["message"]["content"])
            tasks = tuple(
                SearchTask(
                    query=" ".join(item["query"].split()),
                    rationale=" ".join(item["rationale"].split()),
                )
                for item in model_data["tasks"]
                if item.get("query") and item.get("rationale")
            )
            if not 2 <= len(tasks) <= 5:
                raise ValueError("Ollama returned an invalid number of tasks")
            return ResearchPlan(goal=fallback.goal, tasks=tasks)
        except (OSError, KeyError, TypeError, ValueError, json.JSONDecodeError):
            return fallback