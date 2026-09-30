# Academic Research Agent

This project implements the Group C proposal for an LLM-powered academic research and information-gathering agent. A planning agent decomposes a high-level goal, a retrieval agent obtains scholarly metadata, a processing agent deduplicates and ranks evidence, and a storage agent writes inspectable Markdown and JSON outputs.

The implementation supports an Ollama model for LLM-based task decomposition. Deterministic planning and an offline OpenAlex fixture are also provided so that tests and demonstrations are repeatable when a model or network is unavailable. Retrieved abstracts and metadata remain linked to their source; the system does not invent references or generate unsupported conclusions.

## Architecture

```text
User goal
   |
   v
Planning agent ---- optional Ollama chat API
   |
   v
Retrieval agent --- OpenAlex API or offline fixture
   |
   v
Processing agent -- normalise, deduplicate, rank
   |
   +---- insufficient evidence? repeat, maximum 3 cycles
   |
   v
Storage agent ----- Markdown report + JSON evidence + workflow trace
```

The workflow uses explicit typed messages and dependency injection instead of a framework-specific graph. This keeps the implementation executable with the Python standard library while preserving the proposal's provider-agnostic agent boundaries. LLM output is schema-checked and falls back to transparent rules. Ranking remains deterministic so its behaviour can be inspected and tested.

## Requirements

- Python 3.10 or later (tested with Python 3.13.7).
- Internet access for live OpenAlex retrieval.
- Optional: Ollama and a locally available model such as Qwen for LLM planning.
- No Python packages outside the standard library.

## Run

From this directory, run a deterministic offline demonstration:

```bash
python3 -m research_agent \
  "Explainable decisions in autonomous research agents" \
  --offline \
  --output evidence/offline-demo
```

Run against the live OpenAlex API:

```bash
python3 -m research_agent \
  "Explainable decisions in autonomous research agents" \
  --output output
```

Use Ollama for task decomposition:

```bash
ollama pull qwen3:4b
python3 -m research_agent \
  "Explainable decisions in autonomous research agents" \
  --planner ollama \
  --model qwen3:4b \
  --output output
```

If Ollama is unavailable or returns malformed output, the planner records no fabricated content and falls back to the deterministic plan.

## Test

```bash
python3 -m unittest discover -s tests -v
```

The tests cover goal validation, bounded task generation, schema-conforming LLM output, unavailable-model fallback, retrieval fixture normalisation, deduplication, ranking, output persistence and the three-cycle safety bound.

## Outputs and evidence

- `research-report.md`: human-readable ranked records and retrieved abstracts.
- `research-report.json`: the same evidence in machine-readable form.
- `workflow-trace.json`: agent actions, queries, counts, failures and loop decisions.
- `evidence/test-results.txt`: captured unit-test output.
- `evidence/offline-demo/`: a reproducible execution example.

These outputs support review but are not a completed literature review. Keyword overlap and citation counts are imperfect proxies for relevance and quality. OpenAlex coverage and metadata may be incomplete, abstracts may be unavailable, and citation counts can privilege older work. A researcher must inspect the linked sources and verify that evidence supports any downstream claim.

## Design and safety decisions

- The maximum of three cycles prevents an uncontrolled planning/retrieval loop.
- LLM planning is constrained to two to five schema-validated tasks.
- Source URLs, DOI metadata, matched queries and retrieved abstract text preserve provenance.
- Deduplication prevents the same DOI from acquiring artificial weight across queries.
- A trace records retrieval failures and refinement decisions for explainability.
- No credentials, personal data or generated bibliographic details are stored.

## Sources and acknowledgements

The implementation uses the public OpenAlex API and supports the Ollama API. Its architecture is based on the Group C design proposal and the following sources:

- Bandi, A. et al. (2025) 'The rise of agentic AI: a review of definitions, frameworks, architectures, applications, evaluation metrics, and challenges', *Future Internet*, 17(9), 404. https://doi.org/10.3390/fi17090404.
- Lewis, P. et al. (2020) 'Retrieval-augmented generation for knowledge-intensive NLP tasks', *Advances in Neural Information Processing Systems*, 33, pp. 9459-9474.
- OpenAlex (no date) *API documentation*. Available from: https://docs.openalex.org/ [Accessed 30 September 2026].
- OWASP Foundation (2025) *OWASP Top 10 for LLM Applications 2025*. Available from: https://owasp.org/www-project-top-10-for-large-language-model-applications/ [Accessed 30 September 2026].
- Russell, S. and Norvig, P. (2021) *Artificial Intelligence: A Modern Approach*. 4th edn. Harlow: Pearson.
- Wooldridge, M. (2009) *An Introduction to MultiAgent Systems*. 2nd edn. Chichester: Wiley.

No model-generated text is used in the bundled fixture or expected test results.