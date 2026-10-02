"""Evidence-preserving processing and ranking agent."""

from __future__ import annotations

import re
from dataclasses import replace

from .models import Work

_TOKEN_PATTERN = re.compile(r"[a-z0-9]+")
_STOP_WORDS = {
    "a",
    "an",
    "and",
    "in",
    "of",
    "on",
    "the",
    "to",
    "with",
}


def _tokens(value: str) -> set[str]:
    return {
        token
        for token in _TOKEN_PATTERN.findall(value.lower())
        if token not in _STOP_WORDS and len(token) > 1
    }


class ProcessingAgent:
    """Deduplicate and rank records using inspectable deterministic rules."""

    def process(self, goal: str, works: list[Work]) -> list[Work]:
        goal_tokens = _tokens(goal)
        best_by_identity: dict[str, Work] = {}

        for work in works:
            text_tokens = _tokens(f"{work.title} {work.abstract}")
            overlap = len(goal_tokens & text_tokens) / max(1, len(goal_tokens))
            # Citation count is capped and down-weighted so an older, highly
            # cited paper cannot overwhelm direct lexical relevance.
            citation_signal = min(work.cited_by_count, 1000) / 10000
            scored_work = replace(
                work,
                relevance_score=round(overlap + citation_signal, 4),
            )
            identity = (work.doi or work.title).casefold().strip()
            previous = best_by_identity.get(identity)
            # Keeping only the strongest occurrence prevents repeated retrieval
            # across queries from giving one publication artificial weight.
            if previous is None or scored_work.relevance_score > previous.relevance_score:
                best_by_identity[identity] = scored_work

        return sorted(
            best_by_identity.values(),
            key=lambda work: (-work.relevance_score, -work.cited_by_count, work.title),
        )