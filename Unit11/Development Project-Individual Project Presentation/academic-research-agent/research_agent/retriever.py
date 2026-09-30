"""Retrieval agents for OpenAlex and reproducible offline demonstrations."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Protocol
from urllib.parse import urlencode
from urllib.request import Request, urlopen

from .models import Work


class Retriever(Protocol):
    def search(self, query: str, limit: int) -> list[Work]:
        """Return normalised scholarly works for a search query."""


def _abstract_from_index(index: dict[str, list[int]] | None) -> str:
    if not index:
        return ""
    positioned_words = (
        (position, word)
        for word, positions in index.items()
        for position in positions
    )
    return " ".join(word for _, word in sorted(positioned_words))


def _normalise_work(record: dict[str, Any], query: str) -> Work:
    authors = tuple(
        authorship.get("author", {}).get("display_name", "Unknown author")
        for authorship in record.get("authorships", [])
    )
    primary_location = record.get("primary_location") or {}
    source_url = (
        primary_location.get("landing_page_url")
        or record.get("doi")
        or record.get("id")
        or ""
    )
    return Work(
        title=record.get("title") or "Untitled work",
        authors=authors,
        year=record.get("publication_year"),
        abstract=_abstract_from_index(record.get("abstract_inverted_index")),
        doi=record.get("doi"),
        source_url=source_url,
        cited_by_count=int(record.get("cited_by_count") or 0),
        matched_query=query,
    )


class OpenAlexRetriever:
    """Retrieve public scholarly metadata without requiring an API key."""

    def __init__(self, contact_email: str = "ie25073@essex.ac.uk") -> None:
        self.contact_email = contact_email

    def search(self, query: str, limit: int = 5) -> list[Work]:
        parameters = urlencode(
            {
                "search": query,
                "per-page": max(1, min(limit, 25)),
                "mailto": self.contact_email,
            }
        )
        request = Request(
            f"https://api.openalex.org/works?{parameters}",
            headers={"User-Agent": f"AcademicResearchAgent/1.0 ({self.contact_email})"},
        )
        with urlopen(request, timeout=20) as response:
            payload = json.load(response)
        return [_normalise_work(record, query) for record in payload.get("results", [])]


class FixtureRetriever:
    """Replay captured metadata for tests and demonstrations without a network."""

    def __init__(self, fixture_path: Path) -> None:
        self.fixture_path = fixture_path

    def search(self, query: str, limit: int = 5) -> list[Work]:
        with self.fixture_path.open(encoding="utf-8") as fixture:
            records = json.load(fixture)
        return [_normalise_work(record, query) for record in records[:limit]]