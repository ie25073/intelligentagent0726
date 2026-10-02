"""Command-line entry point for the academic research agent."""

from __future__ import annotations

import argparse
from pathlib import Path

from .planner import OllamaPlanner, RuleBasedPlanner
from .retriever import FixtureRetriever, OpenAlexRetriever
from .workflow import ResearchWorkflow


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("goal", help="High-level academic research goal")
    parser.add_argument("--output", type=Path, default=Path("output"))
    parser.add_argument("--offline", action="store_true")
    parser.add_argument("--planner", choices=("rules", "ollama"), default="rules")
    parser.add_argument("--model", default="qwen3:4b")
    return parser


def main() -> int:
    arguments = build_parser().parse_args()
    project_root = Path(__file__).resolve().parent.parent
    planner = (
        OllamaPlanner(model=arguments.model)
        if arguments.planner == "ollama"
        else RuleBasedPlanner()
    )
    # Provider selection stays at the composition boundary so offline evidence,
    # tests and live execution exercise the same workflow implementation.
    retriever = (
        FixtureRetriever(project_root / "tests" / "fixtures" / "openalex.json")
        if arguments.offline
        else OpenAlexRetriever()
    )
    result = ResearchWorkflow(planner, retriever).run(arguments.goal, arguments.output)
    print(f"Retained {len(result.works)} evidence records.")
    for name, path in result.output_paths.items():
        print(f"{name}: {path}")
    return 0