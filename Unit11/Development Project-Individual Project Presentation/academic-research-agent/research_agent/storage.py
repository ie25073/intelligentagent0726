"""Storage agent for human-readable and machine-readable evidence."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .models import Work, WorkflowTrace


class StorageAgent:
    def save(
        self,
        output_directory: Path,
        goal: str,
        works: list[Work],
        trace: WorkflowTrace,
    ) -> dict[str, Path]:
        output_directory.mkdir(parents=True, exist_ok=True)
        report_data: dict[str, Any] = {
            "goal": goal,
            "result_count": len(works),
            "works": [work.to_dict() for work in works],
        }

        json_path = output_directory / "research-report.json"
        markdown_path = output_directory / "research-report.md"
        trace_path = output_directory / "workflow-trace.json"
        json_path.write_text(
            json.dumps(report_data, indent=2, ensure_ascii=False), encoding="utf-8"
        )
        trace_path.write_text(
            json.dumps(trace.events, indent=2, ensure_ascii=False), encoding="utf-8"
        )
        markdown_path.write_text(
            self._render_markdown(goal, works), encoding="utf-8"
        )
        return {"markdown": markdown_path, "json": json_path, "trace": trace_path}

    @staticmethod
    def _render_markdown(goal: str, works: list[Work]) -> str:
        lines = [
            "# Academic Research Agent Report",
            "",
            f"**Research goal:** {goal}",
            "",
            f"**Evidence records retained:** {len(works)}",
            "",
            "Results are ranked using transparent keyword overlap and a bounded citation-count signal. Summaries below reproduce retrieved abstract metadata; they are not model-generated claims.",
            "",
        ]
        for index, work in enumerate(works, start=1):
            author_text = ", ".join(work.authors) or "Authors unavailable"
            abstract = work.abstract or "Abstract unavailable; inspect the source record."
            lines.extend(
                [
                    f"## {index}. {work.title}",
                    "",
                    f"- **Authors:** {author_text}",
                    f"- **Year:** {work.year or 'Unknown'}",
                    f"- **Relevance score:** {work.relevance_score:.4f}",
                    f"- **Cited by:** {work.cited_by_count}",
                    f"- **Source:** {work.source_url}",
                    f"- **Matched query:** {work.matched_query}",
                    "",
                    abstract,
                    "",
                ]
            )
        return "\n".join(lines)