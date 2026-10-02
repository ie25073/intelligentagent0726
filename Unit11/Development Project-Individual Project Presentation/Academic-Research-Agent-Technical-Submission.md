---
title: "Academic Research Agent: Technical Submission"
author: "Student ID: ie25073"
date: "Unit 11 Development Project"
toc: true
---

# Submission overview

This document consolidates the source-code rationale, requirements evidence, execution instructions, testing results and critical evaluation for the Academic Research Agent. The presentation contains exactly 10 slides, and the separate Word transcript provides narration for each slide. The published project source is available at <https://github.com/ie25073/intelligentagent0726/tree/main/Unit11/Development%20Project-Individual%20Project%20Presentation/academic-research-agent>; the final verified source remains in the accompanying project folder.

The prototype accepts a scholarly research goal, delegates focused searches, retrieves publication metadata, normalises and ranks evidence, and stores both human-readable and machine-readable outputs. It uses an optional Ollama language model for planning and the OpenAlex API for live scholarly metadata. A deterministic planner and captured fixture permit reproducible execution when the model or network is unavailable.

# Requirements traceability

| ID | Requirement | Implementation evidence | Verification evidence |
|---|---|---|---|
| R1 | Accept and validate a research goal | `cli.py`; `RuleBasedPlanner.create_plan` | Rejects underspecified goals test |
| R2 | Decompose the goal into focused searches | `RuleBasedPlanner`; `OllamaPlanner` | Bounded/distinct task and schema tests |
| R3 | Retrieve scholarly metadata | `OpenAlexRetriever`; `FixtureRetriever` | Fixture workflow and live execution trace |
| R4 | Preserve provenance | `Work.source_url`, DOI and matched query | Generated JSON/Markdown reports |
| R5 | Deduplicate and rank evidence | `ProcessingAgent.process` | Deduplication/ranking test |
| R6 | Persist inspectable outputs | `StorageAgent.save` | Persistence and CLI functional tests |
| R7 | Tolerate model and retrieval failure | Ollama fallback; per-task exception boundary | Unavailable-model test and live trace |
| R8 | Prevent uncontrolled execution | Maximum three workflow cycles | Cycle-bound test |
| R9 | Support reproducible assessment | Offline fixture and standard-library implementation | Eight-test clean discovery run |

# Architecture and data flow

The design uses four cooperating roles rather than one opaque prompt. A planning agent creates a typed `ResearchPlan`; a retrieval agent returns normalised `Work` records; a processing agent applies deterministic deduplication and scoring; and a storage agent persists the report and trace. Dependency injection allows the workflow to use either live OpenAlex retrieval or a captured fixture without changing orchestration logic.

```text
Research goal
    |
    v
Planning agent ---- invalid/unavailable model ----> deterministic fallback
    |
    v
ResearchPlan[SearchTask]
    |
    v
Retrieval agent ---- per-task failure -----------> trace error and continue
    |
    v
Processing agent --> deduplicate --> score --> rank
    |
    +---- insufficient evidence and cycles remain --> refine plan
    |
    v
Storage agent --> research-report.md
              --> research-report.json
              --> workflow-trace.json
```

Typed dataclasses define the message contract. This prevents arbitrary model output from flowing directly into retrieval. The Ollama response is parsed as JSON and must contain between two and five non-empty tasks. Any connection, parsing, shape or value error selects the deterministic fallback. This choice favours completion and inspectability over dependence on an external generative service.

The workflow catches retrieval failures at task scope. One failed OpenAlex query therefore does not discard successful work from another query. Every failure is included in the trace. The loop has a hard three-cycle maximum, preventing evidence scarcity from creating uncontrolled retrieval. The ranking formula combines goal-token overlap with a small bounded citation signal:

$$
s(w) = \frac{|T_g \cap T_w|}{\max(1, |T_g|)} + \frac{\min(c_w, 1000)}{10000}
$$

where $T_g$ is the set of meaningful goal tokens, $T_w$ is the title-and-abstract token set and $c_w$ is the citation count. Capping and down-weighting citation count prevents older, highly cited work from overwhelming direct lexical relevance. This is transparent and reproducible, although it is not a substitute for semantic relevance judgement.

# Installation and execution

## Prerequisites

- Python 3.10 or later. Final verification used Python 3.13.7.
- No mandatory third-party Python packages.
- Optional Ollama service with a local Qwen-compatible model for LLM planning.
- Internet access only for live OpenAlex retrieval.

## Reproducible offline run

From the `academic-research-agent` directory:

```bash
python3 -m research_agent \
  "Explainable decisions in autonomous research agents" \
  --offline \
  --output evidence/offline-demo
```

Expected terminal result:

```text
Retained 3 evidence records.
markdown: evidence/offline-demo/research-report.md
json: evidence/offline-demo/research-report.json
trace: evidence/offline-demo/workflow-trace.json
```

## Live run with Ollama

```bash
ollama serve
ollama pull qwen2.5:3b
python3 -m research_agent \
  "Explainable decisions in autonomous research agents" \
  --planner ollama \
  --model qwen2.5:3b \
  --output output/live-demo
```

If Ollama is absent, planning falls back deterministically. If an OpenAlex request fails, the error appears in `workflow-trace.json`; remaining tasks and bounded refinement cycles continue.

# Testing and functional demonstration

Run the complete suite with:

```bash
python3 -m unittest discover -s tests -v
```

Final verification produced:

```text
Ran 8 tests
OK
```

The eight tests cover:

1. rejection of an underspecified goal;
2. bounded and distinct deterministic search tasks;
3. acceptance of schema-conforming mocked Ollama output;
4. fallback when the Ollama endpoint is unavailable;
5. deduplication and ranking of repeated records;
6. persistence of the offline report and trace;
7. termination after the configured evidence cycles; and
8. a subprocess functional run of the actual CLI, including all three outputs.

The offline demonstration retained three records and generated Markdown, JSON and trace files. This provides stable evidence independent of network state. A separate live run recorded OpenAlex HTTP failures and later successful retrieval within the three-cycle limit. The trace therefore demonstrates both failure visibility and bounded recovery; it does not conceal unreliable external behaviour.

# Development and remediation record

The implementation progressed from typed domain messages to deterministic planning, retrieval adapters, processing/ranking, storage and finally orchestration. Testing then expanded from component-level validation to workflow persistence and executable CLI behaviour. The presentation and transcript were generated only after this evidence existed.

Final submission verification identified two evidence-quality issues. First, a stored record claimed seven tests while a clean discovery run initially found five. The intended model-contract tests had not been saved. They were added using a mocked Ollama endpoint, proving both schema-valid planning and unavailable-service fallback. Second, the existing tests invoked workflow classes directly but did not prove that the advertised command line worked. A subprocess functional test was added to run `python -m research_agent`, check the success status and record count, and assert the exact output set. A fresh clean run now reports eight passing tests, and the evidence file was regenerated from that run.

The PowerPoint initially rendered as 11 slides because the conversion tool inserted a title slide. The source was consolidated and re-rendered to the required 10-slide maximum. These remediations illustrate why final artefacts and executable behaviour must be verified independently of their editable sources.

# Critical evaluation

## Strengths

The implementation has explicit boundaries and replaceable dependencies. Typed messages make agent communication inspectable. Validation prevents malformed LLM output from directing external requests. Deterministic fallback and an offline fixture improve reproducibility. The trace gives assessors and users evidence of state transitions and failures. A bounded loop limits cost and prevents runaway autonomy. The standard-library implementation also reduces installation risk.

## Limitations

The relevance score is a heuristic based on lexical overlap and citation count. It has not been evaluated against a labelled relevance dataset, and citation count can encode disciplinary and age biases. OpenAlex metadata may be incomplete, particularly abstracts. The prototype retrieves metadata rather than full text and does not perform systematic-review screening. The LLM planner has mocked contract tests but no quantitative comparison across models or prompts. Live API behaviour remains dependent on rate limits and network availability.

## Responsible-use controls

The generated report states that abstracts reproduce retrieved metadata rather than model-generated claims. Every result includes a source URL and matched query. Model output is restricted to validated search tasks; it cannot write final scholarly claims directly. Errors are preserved in the trace. These controls support accountability, but a human researcher must still verify relevance, source quality, authorship and interpretation before relying on the output.

## Future development

The next iteration should evaluate ranking against a human-labelled set using precision at $k$ and nDCG, add retry/backoff and mocked HTTP error tests, expose date and open-access filters, and introduce a human approval gate before broad or costly searches. Semantic embeddings could improve recall, but should be compared empirically with the transparent baseline rather than assumed superior.

# Key source excerpts

The excerpts below evidence the two highest-risk controls. Complete source and tests are available through the repository link in the submission overview.

## Validated LLM planning and deterministic fallback

```python
def create_plan(self, goal: str) -> ResearchPlan:
    fallback = RuleBasedPlanner().create_plan(goal)
    prompt = (
        "Return JSON only with a top-level 'tasks' array. Each task must have "
        "a non-empty 'query' and 'rationale'. Create 2 to 5 scholarly search "
        f"tasks for this research goal: {fallback.goal}"
    )
    try:
        request = Request(
            f"{self.base_url}/api/generate",
            data=json.dumps(
                {"model": self.model, "prompt": prompt, "stream": False}
            ).encode("utf-8"),
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        with urlopen(request, timeout=self.timeout) as response:
            model_response = json.load(response)
        payload = json.loads(model_response["response"])
        tasks = tuple(
            SearchTask(
                query=item["query"].strip(),
                rationale=item["rationale"].strip(),
            )
            for item in payload["tasks"]
            if item.get("query", "").strip()
            and item.get("rationale", "").strip()
        )
        if not 2 <= len(tasks) <= 5:
            raise ValueError("Ollama returned an invalid number of tasks")
        return ResearchPlan(goal=fallback.goal, tasks=tasks)
    except (OSError, KeyError, TypeError, ValueError, json.JSONDecodeError):
        return fallback
```

## Bounded, traceable workflow

```python
def run(self, goal: str, output_directory: Path) -> WorkflowResult:
    trace = WorkflowTrace()
    plan = self.planner.create_plan(goal)
    trace.record("planning", "plan_created", task_count=len(plan.tasks))
    ranked: list[Work] = []

    for cycle in range(1, self.max_cycles + 1):
        trace.record("workflow", "cycle_started", cycle=cycle)
        retrieved: list[Work] = []
        for task in plan.tasks:
            try:
                works = self.retriever.search(task.query, self.per_query_limit)
                retrieved.extend(works)
                trace.record(
                    "retrieval", "search_completed",
                    query=task.query, count=len(works),
                )
            except Exception as error:
                trace.record(
                    "retrieval", "search_failed",
                    query=task.query, error=str(error),
                )

        ranked = self.processor.process(goal, [*ranked, *retrieved])
        sufficient = len(ranked) >= self.minimum_results
        trace.record(
            "processing", "evidence_evaluated",
            retained=len(ranked), sufficient=sufficient,
        )
        if sufficient:
            break
        plan = self.planner.refine_plan(plan, cycle)

    files = self.storage.save(output_directory, goal, ranked, trace)
    return WorkflowResult(works=ranked, files=files, trace=trace)
```

# References

OpenAlex (n.d.) *OpenAlex API documentation*. Available at: <https://docs.openalex.org/>.

Ollama (n.d.) *Ollama API documentation*. Available at: <https://github.com/ollama/ollama/blob/main/docs/api.md>.

Wooldridge, M. (2009) *An Introduction to MultiAgent Systems*. 2nd edn. Chichester: Wiley.

Russell, S. and Norvig, P. (2021) *Artificial Intelligence: A Modern Approach*. 4th edn. Harlow: Pearson.

# Submission inventory

The submission folder contains:

- `ie25073_Academic_Research_Agent_Technical_Submission.docx`: this consolidated report, including key source excerpts.
- `ie25073_Academic_Research_Agent_Transcript.docx`: slide-by-slide narration.
- `ie25073_Academic_Research_Agent_Presentation.pptx`: required 10-slide PowerPoint presentation.
- `README.md`: installation, execution, architecture and evidence guide in Markdown format.

Complete Python source, tests and execution evidence remain in the `academic-research-agent` project folder and its linked GitHub repository.