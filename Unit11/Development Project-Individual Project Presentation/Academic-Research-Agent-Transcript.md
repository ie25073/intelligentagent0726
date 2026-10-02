# Academic Research Agent: Presentation Transcript

## Slide 1 - Academic Research Agent

This presentation demonstrates my implementation of the Group C design proposal: an academic research agent that turns a high-level research goal into a structured set of scholarly evidence. I implemented it as a bounded multi-agent workflow because the problem has distinct responsibilities that benefit from explicit interfaces. My priorities were autonomous planning, reproducibility, source provenance and safe failure. Following Peffers and colleagues, I treated the software as a Design Science artefact whose claims must be evaluated against explicit objectives. The implementation uses only the Python standard library, with OpenAlex for live retrieval and Ollama as an optional local language-model provider.

## Slide 2 - Problem and design requirements

The system addresses the time-consuming first stage of academic research: translating a broad question into searches and organising the results. The assignment requires an LLM-powered planning agent that receives a goal, plans actions, retrieves and processes data, and produces meaningful output. I added operational requirements from the group design: distinct agent roles, lightweight storage, provider independence and transparent evaluation. I also treated bounded autonomy as a requirement. A research assistant should not continue searching indefinitely or conceal failures, and its evidence must remain available for human verification.

## Slide 3 - From proposal to implementation

This table distinguishes architectural fidelity from technology substitution. The provider-agnostic model layer is represented by an Ollama planner behind a simple planning interface, and the CLI can name another compatible model. OpenAlex is the implemented live provider; arXiv and CORE remain extension points rather than completed connectors. Four components preserve the proposed planning, retrieval, processing and storage responsibilities. I replaced LangGraph, Pydantic, HTTPX and Tenacity with standard-library protocols, dataclasses and HTTP calls. This reduces installation risk while retaining explicit state, schemas and the three-cycle loop, but it also means asynchronous retrieval and exponential back-off are not implemented.

## Slide 4 - System architecture

The user supplies one research goal. The planning agent creates typed search tasks, optionally using Ollama. The retrieval agent executes those searches against OpenAlex or the offline fixture. The processing agent normalises records, reconstructs available abstracts, removes duplicates and ranks results. If the evidence count is below the configured threshold, the workflow performs another bounded cycle. Finally, the storage agent creates a readable report, a machine-readable evidence file and an execution trace. Dependency injection keeps these roles testable and allows providers to change without rewriting the orchestration.

## Slide 5 - Planning and autonomous behaviour

Autonomy is demonstrated by the transition from one goal to a sequence of actions without the user specifying each query. The Ollama prompt requests between two and five tasks in a strict JSON shape. The response is parsed and validated before execution. Malformed output or an unavailable endpoint is not trusted; the planner falls back to transparent query templates. After retrieval, the workflow evaluates whether enough unique records exist and either stops or performs another cycle. This is bounded workflow autonomy: the planner proposes actions and the orchestrator decides whether to continue, while retrieval, processing and storage are deterministic specialists rather than independent goal-seeking agents. The three-cycle limit is a practical kill switch.

## Slide 6 - Evidence retrieval and processing

The retrieval agent maps OpenAlex results into a consistent internal record. It preserves title, authors, publication year, citation count, DOI or source URL, abstract and the query that found the work. The processor deduplicates records so that one paper returned by several tasks does not gain artificial weight. Ranking uses explicit keyword overlap plus a bounded citation signal. I deliberately did not ask the language model to rank or summarise the evidence. Deterministic processing is easier to reproduce, inspect and test, while retrieved metadata remains connected to its source.

## Slide 7 - Explainability and responsible design

Explainability is implemented as evidence, not merely as a claim. The workflow trace records the generated plan, each retrieval, result counts, failures, sufficiency decisions and the reason execution stopped. This allows a reviewer to reconstruct the system's actions. Provenance helps address hallucinated citation risk because records retain links to their source. Schema validation rejects malformed model output, although it is not a complete defence against semantically valid prompt injection. The agent is therefore a research aid rather than an autonomous author. OpenAlex can omit material, abstracts may be missing and citation counts can disadvantage recent work, so a researcher must inspect sources and claims.

## Slide 8 - Testing strategy and results

I used eight automated tests at component, workflow and functional levels. Planner tests verify minimum goal quality, two-to-five valid tasks, acceptance of schema-conforming model output and fallback when the endpoint fails. Processing tests verify duplicate removal and ranking order. Workflow tests enforce the three-cycle ceiling, while a subprocess test requires exactly three generated files. All eight tests passed with Python 3.13.7. These are explicit software pass criteria. The fixture separates regressions from network and model nondeterminism, but it is synthetic and cannot establish real-world retrieval quality.

## Slide 9 - Demonstration evidence

The demonstration command runs the complete workflow offline for the goal shown earlier. It retained three records and generated all expected artefacts. The report ranks work on explainable planning first, followed by risks of language-model research assistants and evaluation of evidence retrieval. The JSON file contains the same records for later processing, while the trace records how they were obtained. A live OpenAlex demonstration is also included in the repository, but the offline demonstration is the reliable assessment baseline because it can be repeated without credentials, network access or a running model.

## Slide 10 - Critical evaluation and conclusion

The main strengths are modularity, reproducibility, provenance, graceful fallback and bounded autonomy. The principal weakness is that keyword overlap is a limited proxy for semantic relevance, citation counts encode age and visibility bias, and only OpenAlex is implemented as a live source. The fixture validates software behaviour but not literature quality. In response to the design feedback, the next evaluation should pre-register labelled queries and report precision at k and nDCG at k, DOI resolution, abstract-to-source agreement and appropriate abstention. Model comparison should report median and 95th-percentile latency, peak memory, token use and monetary cost for selected Qwen, Mistral and Llama variants. I make no benchmark claim for the illustrative qwen3:4b default.

## References

Bandi, A. et al. (2025) 'The rise of agentic AI: a review of definitions, frameworks, architectures, applications, evaluation metrics, and challenges', *Future Internet*, 17(9), 404. https://doi.org/10.3390/fi17090404.

Lewis, P. et al. (2020) 'Retrieval-augmented generation for knowledge-intensive NLP tasks', *Advances in Neural Information Processing Systems*, 33, pp. 9459-9474.

OpenAlex (no date) *API documentation*. Available from: https://docs.openalex.org/ [Accessed 30 September 2026].

Peffers, K., Tuunanen, T., Rothenberger, M.A. and Chatterjee, S. (2007) 'A design science research methodology for information systems research', *Journal of Management Information Systems*, 24(3), pp. 45-77. https://doi.org/10.2753/MIS0742-1222240302.

Russell, S. and Norvig, P. (2021) *Artificial Intelligence: A Modern Approach*. 4th edn. Harlow: Pearson.

Wooldridge, M. (2009) *An Introduction to MultiAgent Systems*. 2nd edn. Chichester: Wiley.