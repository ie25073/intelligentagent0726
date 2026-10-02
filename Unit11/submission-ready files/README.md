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

## Design-proposal traceability

The implementation follows the Group C architecture, but it does not reproduce every candidate technology named in the proposal.

| Proposal commitment | Implemented evidence | Adaptation or limitation |
|---|---|---|
| Planning, retrieval, processing and storage responsibilities | Four typed components coordinated by `ResearchWorkflow` | These are bounded specialist components, not four independent goal-seeking agents |
| Loop-based refinement with a three-cycle limit | Sufficiency decision and enforced `max_cycles <= 3` | Refinement appends an evaluation-cycle term rather than asking an LLM to redesign the plan |
| LLM-based goal decomposition | Selectable Ollama model with two-to-five-task schema validation | Deterministic planning takes over when the model is unavailable or malformed |
| Provider-agnostic interfaces | `Planner` and `Retriever` protocols plus dependency injection | OpenAlex is the only live retrieval connector; arXiv and CORE remain future extensions |
| Structured exchange, provenance and auditability | Dataclasses, JSON evidence, matched queries, source URLs and workflow trace | Standard-library validation replaces the proposed Pydantic dependency |
| LangGraph, HTTPX and Tenacity | Equivalent orchestration, HTTP and bounded recovery use the Python standard library | Async retrieval, exponential back-off and LangGraph visualisation are not implemented |
| Relevance, recency and citation-aware ranking | Keyword overlap and a capped citation signal | Recency is reported but not scored; no claim of comprehensive retrieval quality is made |
| Publication summaries | Retrieved abstract metadata is reproduced | The agent does not generate summaries because unsupported paraphrases would increase hallucination risk |

The autonomy claim is therefore deliberately narrow. The planning component converts a user goal into actions and the workflow evaluates sufficiency and decides whether to continue without step-by-step user direction. Retrieval, processing and storage remain deterministic specialists. This is bounded workflow autonomy rather than a claim that every Python component is independently autonomous.

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

### Model constraints

`qwen3:4b` is an illustrative local default, not a benchmark winner. The CLI accepts any model exposed through the configured Ollama-compatible endpoint, including suitable Mistral or Llama variants. A local model avoids per-request API charges and keeps prompts on the host, but download size, memory use, context limits and throughput vary with model, quantisation, runtime and hardware. The Group C proposal suggested at least 8 GB RAM; this prototype does not treat that estimate as a guaranteed requirement. Hosted models introduce provider-specific prices, quotas, rate limits and data-handling terms. No comparative model benchmark was conducted, so the demonstration relies on schema compliance and fallback behaviour rather than an unsupported performance claim.

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

Current automated pass/fail criteria are explicit: a plan contains two to five valid tasks, execution never exceeds three cycles, duplicate works do not gain weight, model failure produces a deterministic plan, and a successful CLI run creates exactly three output files. These tests establish software correctness and resilience; they do not establish real-world retrieval quality.

The next evaluation stage should use relevance-labelled queries and report precision at $k$ and nDCG at $k$, DOI-resolution accuracy, abstract/source agreement, and appropriate abstention when evidence is missing. Operational comparison should report median and 95th-percentile latency, peak memory, input/output tokens and monetary cost for each selected model/runtime. Targets must be fixed before evaluation rather than inferred from favourable results.

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
- Guo, T. et al. (2024) 'Large language model based multi-agents: a survey of progress and challenges', *Proceedings of the Thirty-Third International Joint Conference on Artificial Intelligence*, pp. 8048-8057.
- Huang, X. et al. (2024) 'Understanding the planning of LLM agents: a survey', *arXiv* [Preprint]. https://doi.org/10.48550/arXiv.2402.02716.
- OpenAlex (no date) *API documentation*. Available from: https://docs.openalex.org/ [Accessed 30 September 2026].
- OWASP Foundation (2025) *OWASP Top 10 for LLM Applications 2025*. Available from: https://owasp.org/www-project-top-10-for-large-language-model-applications/ [Accessed 30 September 2026].
- Peffers, K. et al. (2007) 'A design science research methodology for information systems research', *Journal of Management Information Systems*, 24(3), pp. 45-77. https://doi.org/10.2753/MIS0742-1222240302.
- Russell, S. and Norvig, P. (2021) *Artificial Intelligence: A Modern Approach*. 4th edn. Harlow: Pearson.
- Sami, A.M. et al. (2024) 'System for systematic literature review using multiple AI agents: concept and an empirical evaluation', *arXiv* [Preprint]. https://doi.org/10.48550/arXiv.2403.08399.
- Wooldridge, M. (2009) *An Introduction to MultiAgent Systems*. 2nd edn. Chichester: Wiley.

No model-generated text is used in the bundled fixture or expected test results. The fixture is synthetic and is included only to demonstrate reproducible software behaviour.