# Academic Research Agent

This project implements the Group C proposal for an LLM-powered academic research and information-gathering agent, informed by Design Science artefact development (Peffers et al., 2007) and multi-agent system theory (Wooldridge, 2009). A planning agent decomposes a high-level goal, a retrieval agent obtains scholarly metadata, a processing agent deduplicates and ranks evidence, and a storage agent writes inspectable Markdown and JSON outputs, reflecting the use of specialist interacting components in LLM-based multi-agent systems (Guo et al., 2024; Bandi et al., 2025).

This is the authoritative technical application README for the Unit 11 final
assignment (University of Essex Online, 2026). Presentation materials and the
source download are linked in the [submission overview](../README.md). The
repository also supports the [Unit 12 e-portfolio](https://ie25073.github.io/).

The implementation supports an Ollama model for LLM-based task decomposition, consistent with literature on LLM-agent planning and task generation (Huang et al., 2024). Deterministic planning and an offline OpenAlex fixture are also provided so that tests and demonstrations are repeatable when a model or network is unavailable. Retrieved abstracts and metadata remain linked to their source; the system does not invent references or generate unsupported conclusions, aligning with retrieval-grounded generation principles (Lewis et al., 2020).

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

The workflow uses explicit typed messages and dependency injection instead of a framework-specific graph, keeping the implementation aligned with bounded rational-agent design and explicit state control (Russell and Norvig, 2021). This keeps the implementation executable with the Python standard library while preserving the proposal's provider-agnostic agent boundaries. LLM planning requests JSON, parses query/rationale strings, normalises whitespace and checks that two to five tasks remain; recognised parsing, value and availability errors trigger rule-based fallback. This is a limited local output contract, not comprehensive JSON Schema validation, and dataclass annotations do not enforce types at runtime. Ranking remains deterministic so its behaviour can be inspected and tested.

## Design-proposal traceability

The implementation follows the architecture developed in the Group C design proposal, with deliberate adaptations made during development to reduce dependency complexity while preserving the intended planning, retrieval, processing and storage responsibilities (Group C, 2026).

| Proposal commitment | Implemented evidence | Adaptation or limitation |
|---|---|---|
| Planning, retrieval, processing and storage responsibilities | Four typed components coordinated by `ResearchWorkflow` | These are bounded specialist components, not four independent goal-seeking agents |
| Loop-based refinement with a three-cycle limit | Sufficiency decision and enforced `max_cycles <= 3` | Refinement appends an evaluation-cycle term rather than asking an LLM to redesign the plan |
| LLM-based goal decomposition | Selectable Ollama model with JSON parsing and a two-to-five-task check | Deterministic planning takes over on recognised availability/parsing errors; this is not exhaustive schema validation |
| Provider-agnostic interfaces | `Planner` and `Retriever` protocols plus dependency injection | OpenAlex is the only live retrieval connector; arXiv and CORE remain future extensions |
| Structured exchange, provenance and auditability | Dataclasses, JSON evidence, matched queries, source URLs and workflow trace | Standard-library validation replaces the proposed Pydantic dependency |
| LangGraph, HTTPX and Tenacity | Equivalent orchestration, HTTP and bounded recovery use the Python standard library | Async retrieval, exponential back-off and LangGraph visualisation are not implemented |
| Relevance, recency and citation-aware ranking | Keyword overlap and a capped citation signal | Recency is reported but not scored; no claim of comprehensive retrieval quality is made |
| Publication summaries | Retrieved abstract metadata is reproduced | The agent does not generate summaries because unsupported paraphrases would increase hallucination risk |

The autonomy claim is therefore deliberately narrow, because autonomy in this artefact is demonstrated through goal-to-action planning and bounded workflow control rather than independent goal-seeking behaviour in every component (Russell and Norvig, 2021; Wooldridge, 2009). The planning component converts a user goal into actions and the workflow evaluates sufficiency and decides whether to continue without step-by-step user direction. Retrieval, processing and storage remain deterministic specialists. This is bounded workflow autonomy rather than a claim that every Python component is independently autonomous.

## Installation and requirements

- Python 3.10 or later (tested with Python 3.13.7).
- Internet access for live OpenAlex retrieval.
- Optional: Ollama and a locally available model such as Qwen for LLM planning.
- No Python packages outside the standard library.

Download and extract [academic-research-agent.zip](../academic-research-agent.zip),
or use the source folder in a clone of the repository. With Python installed,
open a terminal in `academic-research-agent/` and check `python3 --version`.
No `pip install`, dependency restoration or package build is required. All
commands below run from that application directory. Ollama installation and model
downloads are optional and separate from the offline demonstration.

## External services, models and test data

- **OpenAlex API:** supplies live scholarly metadata (OpenAlex, no date). OpenAlex coverage and metadata remain subject to its terms and documented limitations.
- **Ollama:** optional local model runtime used only for planning. The example configuration names Qwen, but no model weights are bundled or represented as original work.
- **Python standard library:** provides HTTP, JSON, command-line and file-handling functionality; no third-party Python framework or library is required.
- **Offline fixture:** the bundled records use synthetic identifiers, example URLs and
  fictional authors. The bundled fixture contains synthetic test data used only
  for reproducible testing and demonstration; it must not be treated as academic
  evidence. Its `10.1000/agent.1`, `10.1000/agent.2` and `10.1000/agent.3`
  identifiers are not registered scholarly DOIs. DOI-shaped URLs retained in
  the fixture and evaluation query labels are synthetic test data for matching,
  not scholarly links.

### Model constraints

`qwen3:4b` is an illustrative local default, not a benchmark winner. The CLI accepts any model exposed through the configured Ollama-compatible endpoint, including suitable Mistral or Llama variants. A local model avoids per-request API charges and keeps prompts on the host, but download size, memory use, context limits and throughput vary with model, quantisation, runtime and hardware; therefore, no untested model-performance claim is made (Huang et al., 2024). The Group C proposal suggested at least 8 GB RAM; this prototype does not treat that estimate as a guaranteed requirement. Hosted models introduce provider-specific prices, quotas, rate limits and data-handling terms. No comparative model benchmark was conducted, so the demonstration relies on schema compliance and fallback behaviour rather than an unsupported performance claim.

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

Fallback handles the error types recognised by the current planner; it is not a
guarantee for every possible malformed response. The workflow trace records the
plan's task count, but does not record whether Ollama or fallback produced it.
The planner benchmark detects fallback by comparison with a rule-based reference.

## Test

```bash
python3 -m unittest discover -s tests -v
```

The eleven tests cover goal validation, bounded task generation, contract-conforming LLM output, unavailable-model fallback, fixture-backed retrieval, deduplication, ranking order, output persistence, configured cycle stopping, an end-to-end command-line run and synthetic identifier labelling in the retrieval evaluation. The constructor's maximum-three-cycle bound is enforced by code; the workflow test exercises a configured two-cycle run.

Implemented pass/fail criteria include two to five parsed Ollama tasks, a maximum of three cycles, removal of repeated records, deterministic fallback on recognised model errors, and exactly three output files from a successful CLI run. The unit tests and planner benchmark exercise these controls within their documented cases; they do not establish real-world retrieval quality or exhaustive input validation.

A small evidence-enhancement stage has now been added, extending the evaluation evidence beyond code execution toward measurable retrieval-ranking behaviour (Sami et al., 2024). The offline labelled-query evaluation in `tools/evaluate_retrieval.py` uses four fixed queries and reports Precision@1, Precision@3 and nDCG@3 against the bundled fixture. The current fixture-ranking result is Mean Precision@1 = 1.0, Mean Precision@3 = 0.5 and Mean nDCG@3 = 1.0. This supports a narrow claim that deterministic ranking is testable and that expected single-relevance records are ranked first in the synthetic fixture. It does not establish live OpenAlex coverage, semantic relevance or source quality.

The planner benchmark in `tools/benchmark_planners.py` runs ten iterations for deterministic planning, contract-conforming mocked Ollama output, malformed mocked Ollama output and a simulated unavailable endpoint. Its saved `valid_schema_runs` field checks task count and non-empty query/rationale values, not a comprehensive schema. All modes passed that check; malformed and unavailable model modes activated fallback in all ten runs. This supports the measured task-contract and fallback behaviour, but it is not a comparative benchmark of real Qwen, Mistral or Llama model quality. A full model comparison would still need installed local models or hosted API access, with memory, context-window, token-throughput, price and provider rate-limit data recorded on the target platform.

## Outputs and evidence

- [research-report.md](evidence/offline-demo/research-report.md): human-readable ranked evidence records and retrieved abstracts.
- [research-report.json](evidence/offline-demo/research-report.json): machine-readable structured evidence output.
- [workflow-trace.json](evidence/offline-demo/workflow-trace.json): planning task counts, searches, failures, evidence counts and stopping/refinement decisions.
- [evidence/test-results.txt](evidence/test-results.txt): captured full unit-test output; test files are in [tests/](tests/).
- [evidence/offline-demo/](evidence/offline-demo/): a reproducible synthetic execution example, not scholarly evidence.
- [evidence/openalex-demo/](evidence/openalex-demo/): preserved historical live execution, including HTTP failures and later recovery; not a fresh live-service validation.
- [evidence/evaluation/retrieval-evaluation.md](evidence/evaluation/retrieval-evaluation.md): labelled-query ranking evaluation with Precision@k and nDCG@k; synthetic identifiers are shown in backticks.
- [evidence/evaluation/retrieval-evaluation.json](evidence/evaluation/retrieval-evaluation.json): the same evaluation with plain
  `ranked_fixture_identifiers` and `relevant_fixture_identifiers`, plus
  `identifier_type` and `identifier_note` metadata. These replace the report's
  former `ranked_dois` and `relevant_dois` fields without changing metric or
  expected-top calculations. Regenerate both retrieval reports with
  `python3 tools/evaluate_retrieval.py`.
- [evidence/evaluation/planner-benchmark.md](evidence/evaluation/planner-benchmark.md)
  and [planner-benchmark.json](evidence/evaluation/planner-benchmark.json):
  planner task-contract/fallback and recorded latency benchmark. All Ollama
  responses, including the unavailable-endpoint case, are simulated; no real
  model or endpoint is measured. Saved latencies are historical measurements,
  not performance guarantees.

The evaluation directory is `evidence/evaluation/`, not a separate top-level
`evaluation/` folder. The four labelled queries and their rankings are unchanged.

## Demonstration sequence

1. Run the test command and show all passing tests.
2. Run the offline command and inspect `research-report.md` and `workflow-trace.json`.
3. Run `python3 tools/evaluate_retrieval.py` and explain what the Precision@k and nDCG@k evidence does and does not prove.
4. Run `python3 tools/benchmark_planners.py` and explain schema compliance, fallback activation and the limits of mocked-model benchmarking.
5. Explain the planner schema/fallback in `planner.py` and the cycle bound in `workflow.py`.
6. Optionally run OpenAlex live, noting that network/API failures are recorded rather than hidden.

## Testing remediation record

Earlier verification found that stored evidence claimed seven tests while only five were initially discoverable. Two mocked Ollama tests and a subprocess-based CLI test established the eight-test snapshot used in the final presentation materials. Three retrieval-evaluation regression tests subsequently added checks for plain synthetic identifiers, unchanged rankings/metrics and Markdown labelling. The refreshed test evidence records eleven passing tests. A historical live OpenAlex run encountered HTTP failures before succeeding on a later bounded cycle; its original trace is preserved rather than presented as a fresh or failure-free run.

These outputs support review but are not a completed literature review; this boundary is consistent with Design Science evaluation, where the artefact is assessed against stated objectives rather than overstated as a complete domain solution (Peffers et al., 2007). Keyword overlap and citation counts are imperfect proxies for relevance and quality. OpenAlex coverage and metadata may be incomplete, abstracts may be unavailable, and citation counts can privilege older work. A researcher must inspect the linked sources and verify that evidence supports any downstream claim.

## Design and safety decisions

- The maximum of three cycles prevents an uncontrolled planning/retrieval loop.
- LLM planning requests JSON and checks a local two-to-five-task contract; this is not exhaustive schema or semantic validation.
- Source URLs, DOI metadata, matched queries and retrieved abstract text preserve provenance.
- Deduplication prevents the same DOI from acquiring artificial weight across queries.
- A trace records retrieval failures and refinement decisions for explainability.
- Output-contract checks are syntactic controls only; semantically malicious but valid JSON still requires restricted tools, trusted retrieval sources, provenance checking and human review, because prompt injection and component-chain risks remain recognised GAI security concerns (NIST, 2024; OWASP Foundation, 2025). These are design considerations, not a claim that every recommended security control is implemented.
- No API credentials or model-generated bibliographic details are stored. Retrieved author names and queries are retained as provenance; users should not enter sensitive personal data into research goals.

## Sources and acknowledgements

The implementation uses the public OpenAlex API and supports the Ollama API. Its architecture is based on the Group C design proposal and the following references:

### References

- Bandi, A. et al. (2025) 'The rise of agentic AI: a review of definitions, frameworks, architectures, applications, evaluation metrics, and challenges', *Future Internet*, 17(9), 404. https://doi.org/10.3390/fi17090404.
- Group C (2026) Design Proposal for an Academic and Information Gathering Multi-Agent Artificial Intelligence Tool. University of Essex Online, Intelligent Agents module.
- Guo, T. et al. (2024) 'Large language model based multi-agents: a survey of progress and challenges', *Proceedings of the Thirty-Third International Joint Conference on Artificial Intelligence*, pp. 8048-8057.
- Huang, X. et al. (2024) 'Understanding the planning of LLM agents: a survey', *arXiv* [Preprint]. https://doi.org/10.48550/arXiv.2402.02716.
- Lewis, P. et al. (2020) 'Retrieval-augmented generation for knowledge-intensive NLP tasks', *Advances in Neural Information Processing Systems*, 33, pp. 9459-9474.
- NIST (National Institute of Standards and Technology) (2024) *Artificial Intelligence Risk Management Framework: Generative Artificial Intelligence Profile*. NIST AI 600-1. https://doi.org/10.6028/NIST.AI.600-1.
- OpenAlex (no date) *API documentation*. Available from: https://docs.openalex.org/ [Accessed 30 September 2026].
- OWASP Foundation (2025) *OWASP Top 10 for LLM Applications 2025*. Available from: https://owasp.org/www-project-top-10-for-large-language-model-applications/ [Accessed 30 September 2026].
- Peffers, K. et al. (2007) 'A design science research methodology for information systems research', *Journal of Management Information Systems*, 24(3), pp. 45-77. https://doi.org/10.2753/MIS0742-1222240302.
- Russell, S. and Norvig, P. (2021) *Artificial Intelligence: A Modern Approach*. 4th edn. Harlow: Pearson.
- Sami, A.M. et al. (2024) 'System for systematic literature review using multiple AI agents: concept and an empirical evaluation', *arXiv* [Preprint]. https://doi.org/10.48550/arXiv.2403.08399.
- University of Essex Online (2026) *Unit 11 final assignment brief*. Intelligent Agents module.
- Wooldridge, M. (2009) *An Introduction to MultiAgent Systems*. 2nd edn. Chichester: Wiley.
