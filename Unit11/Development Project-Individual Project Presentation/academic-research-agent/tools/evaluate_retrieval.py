"""Small labelled retrieval-ranking evaluation for the Academic Research Agent.

This script deliberately uses the offline fixture so the assessor can rerun the
same measurement without network access or paid services. It evaluates ranking
behaviour, not OpenAlex coverage quality.

The DOI-shaped URLs below are synthetic test data retained for fixture matching,
not registered scholarly DOIs. Reports expose only their plain identifiers.
"""

from __future__ import annotations

import json
import math
from dataclasses import asdict, dataclass
from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from research_agent.processor import ProcessingAgent
from research_agent.retriever import FixtureRetriever

FIXTURE = PROJECT_ROOT / "tests" / "fixtures" / "openalex.json"
OUTPUT_DIR = PROJECT_ROOT / "evidence" / "evaluation"
IDENTIFIER_NOTE = (
    "The identifiers used in this evaluation belong to synthetic fixture records. "
    "They are not registered scholarly DOIs and are included only for reproducible testing."
)


@dataclass(frozen=True)
class LabelledQuery:
    query: str
    relevant_dois: tuple[str, ...]
    expected_top_doi: str | None


QUERIES = (
    LabelledQuery(
        query="explainable planning autonomous research agents",
        relevant_dois=("https://doi.org/10.1000/agent.1",),
        expected_top_doi="https://doi.org/10.1000/agent.1",
    ),
    LabelledQuery(
        query="evidence retrieval multi-agent systems evaluation",
        relevant_dois=("https://doi.org/10.1000/agent.2",),
        expected_top_doi="https://doi.org/10.1000/agent.2",
    ),
    LabelledQuery(
        query="language model research assistants citation hallucination provenance",
        relevant_dois=("https://doi.org/10.1000/agent.3",),
        expected_top_doi="https://doi.org/10.1000/agent.3",
    ),
    LabelledQuery(
        query="autonomous research agents evidence retrieval safety",
        relevant_dois=(
            "https://doi.org/10.1000/agent.1",
            "https://doi.org/10.1000/agent.2",
            "https://doi.org/10.1000/agent.3",
        ),
        expected_top_doi=None,
    ),
)


def dcg(relevances: list[int]) -> float:
    return sum(rel / math.log2(index + 2) for index, rel in enumerate(relevances))


def ndcg_at_k(ranked_dois: list[str], relevant_dois: set[str], k: int) -> float:
    observed = [1 if doi in relevant_dois else 0 for doi in ranked_dois[:k]]
    ideal = sorted(observed, reverse=True)
    ideal_score = dcg(ideal)
    return 0.0 if ideal_score == 0 else dcg(observed) / ideal_score


def evaluate() -> dict[str, object]:
    retriever = FixtureRetriever(FIXTURE)
    processor = ProcessingAgent()
    cases: list[dict[str, object]] = []

    for labelled in QUERIES:
        works = retriever.search(labelled.query, limit=5)
        ranked = processor.process(labelled.query, works)
        ranked_dois = [work.doi or work.source_url for work in ranked]
        relevant = set(labelled.relevant_dois)
        precision_at_1 = sum(1 for doi in ranked_dois[:1] if doi in relevant) / 1
        precision_at_3 = sum(1 for doi in ranked_dois[:3] if doi in relevant) / min(3, len(ranked_dois))
        top_doi = ranked_dois[0] if ranked_dois else None
        expected_top_met = (
            True if labelled.expected_top_doi is None else top_doi == labelled.expected_top_doi
        )
        cases.append(
            {
                "query": labelled.query,
                "relevant_fixture_identifiers": [
                    doi.removeprefix("https://doi.org/") for doi in labelled.relevant_dois
                ],
                "ranked_fixture_identifiers": [
                    doi.removeprefix("https://doi.org/") for doi in ranked_dois
                ],
                "precision_at_1": round(precision_at_1, 4),
                "precision_at_3": round(precision_at_3, 4),
                "ndcg_at_3": round(ndcg_at_k(ranked_dois, relevant, 3), 4),
                "expected_top_met": expected_top_met,
            }
        )

    return {
        "scope": "Offline fixture ranking evaluation; not a live OpenAlex coverage benchmark.",
        "identifier_type": "synthetic_fixture_identifier",
        "identifier_note": IDENTIFIER_NOTE,
        "pass_targets": {
            "expected_top_met": "true for all single-relevance cases",
            "mean_precision_at_1": ">= 0.75",
            "mean_ndcg_at_3": ">= 0.85",
        },
        "case_count": len(cases),
        "mean_precision_at_1": round(
            sum(case["precision_at_1"] for case in cases) / len(cases), 4
        ),
        "mean_precision_at_3": round(
            sum(case["precision_at_3"] for case in cases) / len(cases), 4
        ),
        "mean_ndcg_at_3": round(sum(case["ndcg_at_3"] for case in cases) / len(cases), 4),
        "single_relevance_top_passed": all(
            case["expected_top_met"]
            for case in cases
            if len(case["relevant_fixture_identifiers"]) == 1
        ),
        "cases": cases,
    }


def write_markdown(results: dict[str, object]) -> str:
    lines = [
        "# Retrieval Ranking Evaluation",
        "",
        str(results["identifier_note"]),
        "",
        str(results["scope"]),
        "",
        "## Summary",
        "",
        f"- Labelled queries: {results['case_count']}",
        f"- Mean Precision@1: {results['mean_precision_at_1']}",
        f"- Mean Precision@3: {results['mean_precision_at_3']}",
        f"- Mean nDCG@3: {results['mean_ndcg_at_3']}",
        f"- Single-relevance top-rank target passed: {results['single_relevance_top_passed']}",
        "",
        "## Interpretation",
        "",
        "The fixture confirms that deterministic keyword/citation ranking can be tested repeatably. It does not prove live search coverage, semantic relevance or source quality. Those claims require a larger labelled dataset and live retrieval runs.",
        "",
        "## Cases",
        "",
    ]
    for case in results["cases"]:
        lines.extend(
            [
                f"### {case['query']}",
                "- Ranked synthetic fixture identifiers: "
                + ", ".join(f"`{identifier}`" for identifier in case["ranked_fixture_identifiers"]),
                f"- Precision@1: {case['precision_at_1']}",
                f"- Precision@3: {case['precision_at_3']}",
                f"- nDCG@3: {case['ndcg_at_3']}",
                f"- Expected top met: {case['expected_top_met']}",
                "",
            ]
        )
    return "\n".join(lines)


if __name__ == "__main__":
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    results = evaluate()
    (OUTPUT_DIR / "retrieval-evaluation.json").write_text(
        json.dumps(results, indent=2), encoding="utf-8"
    )
    (OUTPUT_DIR / "retrieval-evaluation.md").write_text(
        write_markdown(results), encoding="utf-8"
    )
    print(json.dumps(results, indent=2))
