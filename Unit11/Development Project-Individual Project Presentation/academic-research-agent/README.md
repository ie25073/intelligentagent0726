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

## External services, models and test data

- **OpenAlex API:** supplies live scholarly metadata. OpenAlex coverage and metadata remain subject to its terms and documented limitations.
- **Ollama:** optional local model runtime used only for planning. The example configuration names Qwen, but no model weights are bundled or represented as original work.
- **Python standard library:** provides HTTP, JSON, command-line and file-handling functionality; no third-party Python framework or library is required.
- **Offline fixture:** the bundled records use reserved example identifiers and fictional authors. They are synthetic regression-test data, not publications, and must not be cited as academic evidence.

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

The eight tests cover goal validation, bounded task generation, schema-conforming LLM output, unavailable-model fallback, retrieval fixture normalisation, deduplication, ranking, output persistence, the three-cycle safety bound and an end-to-end command-line run.

## Outputs and evidence

- `research-report.md`: human-readable ranked records and retrieved abstracts.
- `research-report.json`: the same evidence in machine-readable form.
- `workflow-trace.json`: agent actions, queries, counts, failures and loop decisions.
- `evidence/test-results.txt`: captured unit-test output.
- `evidence/offline-demo/`: a reproducible execution example.

## Demonstration sequence

1. Run the test command and show all eight passing tests.
2. Run the offline command and inspect `research-report.md` and `workflow-trace.json`.
3. Explain the planner schema/fallback in `planner.py` and the cycle bound in `workflow.py`.
4. Optionally run OpenAlex live, noting that network/API failures are recorded rather than hidden.

## Testing remediation record

Final verification found that stored evidence claimed seven tests while only five were initially discoverable. Two mocked Ollama tests were added to prove schema-conforming planning and deterministic fallback. A separate subprocess-based functional test was then added to verify the real `python -m research_agent` entry point and all three generated outputs. The refreshed evidence now records eight passing tests. A live OpenAlex run also encountered HTTP failures before succeeding on a later bounded cycle; the trace preserves those failures and demonstrates graceful recovery rather than presenting the run as failure-free.

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

No model-generated text is used in the bundled fixture or expected test results. The fixture is synthetic and is included only to demonstrate reproducible software behaviour.