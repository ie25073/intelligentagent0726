# Academic Research Agent: Presentation Transcript

**Student:** Imoh Etuk (ie25073)

**Presentation:** 10 slides

**Date:** 30 September 2026

## Slide 1 - Academic Research Agent

This presentation demonstrates my implementation of the Group C design proposal: an academic research agent that turns a high-level research goal into a structured set of scholarly evidence. I implemented it as a bounded multi-agent workflow because the problem has distinct responsibilities that benefit from explicit interfaces. My priorities were autonomous planning, reproducibility, source provenance and safe failure. The implementation uses only the Python standard library, with OpenAlex for live retrieval and Ollama as an optional local language-model provider.

## Slide 2 - Problem and design requirements

The system addresses the time-consuming first stage of academic research: translating a broad question into searches and organising the results. The assignment requires an LLM-powered planning agent that receives a goal, plans actions, retrieves and processes data, and produces meaningful output. I added operational requirements from the group design: distinct agent roles, lightweight storage, provider independence and transparent evaluation. I also treated bounded autonomy as a requirement. A research assistant should not continue searching indefinitely or conceal failures, and its evidence must remain available for human verification.

## Slide 3 - From proposal to implementation

This table shows how the team design became executable software. The provider-agnostic model layer is represented by an Ollama planner behind a simple planning interface. If Ollama is absent, deterministic planning preserves system availability. OpenAlex provides live scholarly metadata, while a fixture provides repeatable testing and demonstration. Four components implement the proposed planning, retrieval, processing and storage responsibilities. JSON was retained from the revised group design because it is lightweight and inspectable. Iterative retrieval is implemented through an evidence-sufficiency decision with an explicit three-cycle maximum.

## Slide 4 - System architecture

The user supplies one research goal. The planning agent creates typed search tasks, optionally using Ollama. The retrieval agent executes those searches against OpenAlex or the offline fixture. The processing agent normalises records, reconstructs available abstracts, removes duplicates and ranks results. If the evidence count is below the configured threshold, the workflow performs another bounded cycle. Finally, the storage agent creates a readable report, a machine-readable evidence file and an execution trace. Dependency injection keeps these roles testable and allows providers to change without rewriting the orchestration.

## Slide 5 - Planning and autonomous behaviour

Autonomy is demonstrated by the transition from one goal to a sequence of actions without the user specifying each query. The Ollama prompt requests between two and five tasks in a strict JSON shape. The response is parsed and validated before execution. Malformed output or an unavailable endpoint is not trusted; the planner falls back to transparent query templates. After retrieval, the workflow evaluates whether enough unique records exist and either stops or performs another cycle. The maximum cycle count is a practical kill switch that prevents an accidental or model-driven infinite loop.

## Slide 6 - Evidence retrieval and processing

The retrieval agent maps OpenAlex results into a consistent internal record. It preserves title, authors, publication year, citation count, DOI or source URL, abstract and the query that found the work. The processor deduplicates records so that one paper returned by several tasks does not gain artificial weight. Ranking uses explicit keyword overlap plus a bounded citation signal. I deliberately did not ask the language model to rank or summarise the evidence. Deterministic processing is easier to reproduce, inspect and test, while retrieved metadata remains connected to its source.

## Slide 7 - Explainability and responsible design

Explainability is implemented as evidence, not merely as a claim. The workflow trace records the generated plan, each retrieval, result counts, failures, sufficiency decisions and the reason execution stopped. This allows a reviewer to reconstruct the system's actions. Provenance helps address hallucinated citation risk because records retain links to their source. Nevertheless, the agent is a research aid rather than an autonomous author. OpenAlex can omit material, abstracts may be missing and citation counts can disadvantage recent work. A researcher must therefore inspect sources and confirm that they support downstream claims.

## Slide 8 - Testing strategy and results

I used eight automated tests at component, workflow and functional levels. Planner tests verify minimum goal quality, bounded and distinct tasks, acceptance of a schema-conforming model response, and fallback when the model endpoint fails. Processing tests verify duplicate removal and ranking order. Workflow tests inspect persisted outputs, evidence sufficiency and the cycle limit. A subprocess test runs the actual command-line entry point and verifies all three generated files. All eight tests passed with Python 3.13.7. The fixture separates code regressions from changing API data, internet availability and model nondeterminism.

## Slide 9 - Demonstration evidence

The demonstration command runs the complete workflow offline for the goal shown earlier. It retained three records and generated all expected artefacts. The report ranks work on explainable planning first, followed by risks of language-model research assistants and evaluation of evidence retrieval. The JSON file contains the same records for later processing, while the trace records how they were obtained. A live OpenAlex demonstration is also included in the repository, but the offline demonstration is the reliable assessment baseline because it can be repeated without credentials, network access or a running model.

## Slide 10 - Critical evaluation and conclusion

The main strengths are modularity, reproducibility, provenance, graceful fallback and bounded autonomy. The principal weakness is that keyword overlap is a limited proxy for semantic relevance, while citation counts can encode age and visibility bias. The fixture validates software behaviour but not the quality of live literature selection, and I did not conduct a user study. Future evaluation should use a manually labelled relevance set, precision and recall, DOI checks, model comparisons and adversarial prompt tests. Overall, the system fulfils the goal-plan-act-output requirement while preserving meaningful human oversight.

## References

Bandi, A. et al. (2025) 'The rise of agentic AI: a review of definitions, frameworks, architectures, applications, evaluation metrics, and challenges', *Future Internet*, 17(9), 404. https://doi.org/10.3390/fi17090404.

Lewis, P. et al. (2020) 'Retrieval-augmented generation for knowledge-intensive NLP tasks', *Advances in Neural Information Processing Systems*, 33, pp. 9459-9474.

OpenAlex (no date) *API documentation*. Available from: https://docs.openalex.org/ [Accessed 30 September 2026].

Russell, S. and Norvig, P. (2021) *Artificial Intelligence: A Modern Approach*. 4th edn. Harlow: Pearson.

Wooldridge, M. (2009) *An Introduction to MultiAgent Systems*. 2nd edn. Chichester: Wiley.