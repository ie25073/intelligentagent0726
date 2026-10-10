"""Typed messages exchanged by the research agents."""

from dataclasses import asdict, dataclass, field
from typing import Any


# Messages passed between specialist components are immutable so downstream
# agents cannot silently change a plan or evidence record after it is created.
@dataclass(frozen=True)
class SearchTask:
    """A focused scholarly search delegated by the planning agent."""

    query: str
    rationale: str


@dataclass(frozen=True)
class ResearchPlan:
    """A bounded sequence of search tasks for a user's research goal."""

    goal: str
    tasks: tuple[SearchTask, ...]


@dataclass(frozen=True)
class Work:
    """A normalised scholarly record with provenance."""

    title: str
    authors: tuple[str, ...]
    year: int | None
    abstract: str
    doi: str | None
    source_url: str
    cited_by_count: int = 0
    relevance_score: float = 0.0
    matched_query: str = ""

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


# The trace is deliberately mutable because it is an append-only audit record
# that must accumulate decisions and failures as the workflow progresses.
@dataclass
class WorkflowTrace:
    """Inspectable state transitions captured during a workflow run."""

    events: list[dict[str, Any]] = field(default_factory=list)

    def record(self, agent: str, action: str, **details: Any) -> None:
        self.events.append({"agent": agent, "action": action, **details})