"""Operational benchmark for planning modes.

The benchmark is intentionally small and reproducible. It measures schema
compliance and planning latency for deterministic, mocked-model and available
Ollama modes. If no local Ollama endpoint is available, the result is recorded
rather than hidden.
"""

from __future__ import annotations

import io
import json
import statistics
import time
from dataclasses import asdict, dataclass
from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from research_agent.planner import OllamaPlanner, RuleBasedPlanner

OUTPUT_DIR = PROJECT_ROOT / "evidence" / "evaluation"
GOAL = "Explainable decisions in autonomous research agents"
ITERATIONS = 10


@dataclass(frozen=True)
class BenchmarkResult:
    mode: str
    iterations: int
    valid_schema_runs: int
    fallback_runs: int
    mean_latency_ms: float
    p95_latency_ms: float
    note: str


def percentile(values: list[float], pct: float) -> float:
    if not values:
        return 0.0
    ordered = sorted(values)
    index = min(len(ordered) - 1, int(round((pct / 100) * (len(ordered) - 1))))
    return ordered[index]


def run_mode(mode: str, planner_factory, note: str) -> BenchmarkResult:
    latencies: list[float] = []
    valid = 0
    fallback = 0
    fallback_reference = RuleBasedPlanner().create_plan(GOAL)
    for _ in range(ITERATIONS):
        planner = planner_factory()
        start = time.perf_counter()
        plan = planner.create_plan(GOAL)
        latencies.append((time.perf_counter() - start) * 1000)
        if 2 <= len(plan.tasks) <= 5 and all(task.query and task.rationale for task in plan.tasks):
            valid += 1
        if plan == fallback_reference and mode != "rules":
            fallback += 1
    return BenchmarkResult(
        mode=mode,
        iterations=ITERATIONS,
        valid_schema_runs=valid,
        fallback_runs=fallback,
        mean_latency_ms=round(statistics.mean(latencies), 3),
        p95_latency_ms=round(percentile(latencies, 95), 3),
        note=note,
    )


def valid_ollama_response(*_args, **_kwargs):
    model_content = {
        "tasks": [
            {"query": "agent provenance", "rationale": "Find evidence trails"},
            {"query": "agent evaluation", "rationale": "Find evaluation methods"},
        ]
    }
    return io.BytesIO(json.dumps({"message": {"content": json.dumps(model_content)}}).encode())


def invalid_ollama_response(*_args, **_kwargs):
    return io.BytesIO(json.dumps({"message": {"content": "not valid json"}}).encode())


def unavailable_endpoint(*_args, **_kwargs):
    raise OSError("model endpoint unavailable")


def benchmark() -> dict[str, object]:
    results = [
        run_mode("rules", RuleBasedPlanner, "Deterministic baseline with no model dependency."),
        run_mode(
            "mocked_ollama_valid",
            lambda: OllamaPlanner(opener=valid_ollama_response),
            "Simulates a schema-conforming Ollama response.",
        ),
        run_mode(
            "mocked_ollama_invalid",
            lambda: OllamaPlanner(opener=invalid_ollama_response),
            "Simulates malformed model output; fallback should activate.",
        ),
        run_mode(
            "ollama_unavailable",
            lambda: OllamaPlanner(opener=unavailable_endpoint),
            "Simulates missing local runtime; fallback should activate.",
        ),
    ]
    return {
        "goal": GOAL,
        "iterations_per_mode": ITERATIONS,
        "measures": [
            "valid schema runs",
            "fallback runs",
            "mean latency in milliseconds",
            "95th-percentile latency in milliseconds",
        ],
        "limitation": "This is an operational planner benchmark, not a comparative benchmark of real Qwen, Mistral or Llama model quality. Real local-model benchmarking requires those models to be installed on the target host and should additionally record memory, context size and token throughput.",
        "results": [asdict(result) for result in results],
    }


def write_markdown(results: dict[str, object]) -> str:
    lines = [
        "# Planner Operational Benchmark",
        "",
        f"Goal: {results['goal']}",
        "",
        str(results["limitation"]),
        "",
        "| Mode | Valid schema runs | Fallback runs | Mean latency ms | p95 latency ms | Note |",
        "|---|---:|---:|---:|---:|---|",
    ]
    for result in results["results"]:
        lines.append(
            f"| {result['mode']} | {result['valid_schema_runs']}/{result['iterations']} | "
            f"{result['fallback_runs']} | {result['mean_latency_ms']} | "
            f"{result['p95_latency_ms']} | {result['note']} |"
        )
    return "\n".join(lines) + "\n"


if __name__ == "__main__":
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    results = benchmark()
    (OUTPUT_DIR / "planner-benchmark.json").write_text(
        json.dumps(results, indent=2), encoding="utf-8"
    )
    (OUTPUT_DIR / "planner-benchmark.md").write_text(
        write_markdown(results), encoding="utf-8"
    )
    print(json.dumps(results, indent=2))
