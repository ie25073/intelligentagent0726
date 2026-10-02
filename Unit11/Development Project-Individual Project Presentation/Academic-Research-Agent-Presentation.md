---
title: "Academic Research Agent"
subtitle: "A bounded, explainable multi-agent workflow"
author: "Imoh Etuk | ie25073"
date: "30 September 2026"
---

# Problem and design requirements

- Goal: turn a research question into ranked, traceable scholarly evidence
- Plan autonomous actions from one high-level user goal
- Separate planning, retrieval, processing and storage responsibilities
- Preserve source provenance and expose workflow decisions
- Remain usable without paid services or credentials
- Bound retries and fail safely when a model or network is unavailable
- Design Science frames the artefact and its evaluation (Peffers *et al.*, 2007)

# From proposal to implementation

| Design proposal | Implemented decision |
|---|---|
| Provider-agnostic LLM layer | Optional Ollama planner plus deterministic fallback |
| arXiv, OpenAlex and CORE connectors | OpenAlex implemented; other connectors remain future work |
| Multi-agent responsibilities | Four typed components with explicit hand-offs |
| LangGraph, Pydantic, HTTPX, Tenacity | Standard-library protocols and typed dataclasses minimise dependencies |
| Lightweight journal/output | Markdown report, JSON evidence and JSON trace |
| Iterative retrieval | Sufficiency check with a maximum of three cycles |

# System architecture

```text
Research goal
     |
Planning agent ---- Ollama API (optional)
     |
Retrieval agent --- OpenAlex / offline fixture
     |
Processing agent -- normalise, deduplicate, rank
     |                    |
     +-- insufficient ---+  maximum 3 cycles
     |
Storage agent ----- report.md + evidence.json + trace.json
```

# Planning and autonomous behaviour

- The planner converts one goal into two to five bounded search tasks
- Ollama output must match a validated JSON schema
- Invalid or unavailable model output triggers a transparent rule-based plan
- The workflow executes tasks, evaluates evidence sufficiency and may refine
- A cycle limit acts as a kill switch against uncontrolled agent loops
- Autonomy is bounded at workflow level; deterministic specialists are not independent goal-seeking agents

```bash
python3 -m research_agent "Explainable decisions in autonomous research agents" --offline
```

# Evidence retrieval and processing

- OpenAlex returns scholarly metadata and reconstructed abstract text
- Every record retains authors, year, DOI/source URL and matched query
- DOI or source identity removes duplicates across search tasks
- Ranking combines inspectable keyword overlap with bounded citation evidence
- The report reproduces retrieved metadata; it does not invent citations

**Why deterministic ranking?** Safety-critical evidence selection remains repeatable and testable even when an LLM proposes the search plan.

# Explainability and responsible design

- `workflow-trace.json` records plans, searches, counts, failures and stop decisions
- Provenance supports human checking before evidence is used in academic work
- No credentials, personal data or fabricated bibliography are stored
- Human oversight remains necessary for relevance, source quality and claim support
- Risks remain: coverage gaps, missing abstracts and citation-age bias
- Schema validation reduces malformed output risk but is not a complete prompt-injection defence

# Testing strategy and results

- Eight automated unit, workflow and functional tests passed on Python 3.13.7
- Planner tests: validation, bounded tasks, model schema and fallback
- Processor test: duplicate removal and ranking order
- Workflow tests: persisted outputs, sufficiency decision and cycle bound
- CLI test: executable entry point and all three generated outputs
- Offline fixture makes regression tests independent of network and model availability

**Pass criteria:** 2-5 valid tasks; no more than 3 cycles; deterministic fallback; duplicate suppression; exactly 3 output files.

```text
Ran 8 tests
OK
```

# Demonstration evidence

**Offline run:** 3 evidence records retained

1. Explainable planning for autonomous research agents
2. Risks and limitations of language-model research assistants
3. Evaluating evidence retrieval in multi-agent systems

Generated artefacts:

- Human-readable ranked research report
- Machine-readable evidence record
- Inspectable workflow trace

# Critical evaluation and next steps

**Strengths:** modular, reproducible, traceable and bounded.

**Limits:** lexical ranking, age-biased citations, OpenAlex only, synthetic fixture and no model/user benchmark.

**Feedback-led evaluation:**

- Labelled queries: P@$k$, nDCG@$k$, DOI/source validity and abstention
- Models: p50/p95 latency, memory, tokens and cost

**Conclusion:** goal-plan-act-output with human oversight.

**Sources:** Peffers *et al.* (2007); Lewis *et al.* (2020); Russell and Norvig (2021); Bandi *et al.* (2025). Full references: transcript/README.