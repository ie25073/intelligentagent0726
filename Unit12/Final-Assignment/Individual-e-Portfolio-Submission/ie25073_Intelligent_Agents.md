---
title: "Intelligent Agents: Individual e-Portfolio Submission"
author: "Imoh Etuk (ie25073)"
date: "30 September 2026"
---

**E-portfolio URL:** https://ie25073.github.io/

**Module repository:** https://github.com/ie25073/intelligentagent0726

**Student email:** ie25073@essex.ac.uk

# Portfolio Narrative

<!-- SUPPORTING-NARRATIVE-START -->

## Learning journey and evidence

This portfolio records my progression from analysing autonomous agents to designing, implementing and evaluating an academic research agent. In Units 1–3, the first collaborative discussion established that autonomy is not an isolated technical property. My initial emphasis on delegation developed through peer exchanges into a risk-based view: routine, reversible actions may be delegated, but consequential decisions require monitoring, approval and override. The summary connects autonomy with reactivity, proactivity, social ability and the possibility of emergent behaviour (Wooldridge and Jennings, 1995; Jennings, 2000). It provides evidence for learning outcomes 1 and 4 because it compares agent properties while showing how discussion changed my position on organisational responsibility.

Units 5–7 moved from agent architecture to communication. My forum work compared KQML with conventional method invocation. KQML can express communicative intent while preserving internal autonomy, whereas a Python or Java call is simpler and faster inside a stable component. The Alice and Bob exercise then converted theory into executable Python: KQML performatives represent the dialogue act, KIF represents warehouse facts, and conversation and reply identifiers preserve context. Tests cover valid replies and an unknown-stock failure. The exercise also exposed a limitation: syntactically valid messages do not guarantee shared meaning. My summary therefore argues for ontology versioning, bounded conversations and recoverable failures rather than treating an agent communication language as sufficient interoperability.

The Unit 8 constituency exercise strengthened my understanding of representation. Two parse trees for “The man saw the dog with the telescope” encode different prepositional-phrase attachments. An agent selecting one interpretation from syntax alone may act on the wrong meaning; semantic and contextual evidence is required. This small task connects directly to the final project, where a plausible title or abstract is not automatically relevant evidence.

Units 9–11 focused on deep learning, ethics and deployment. My discussion traced risks including confabulation, bias, privacy, intellectual property and over-reliance. Peer responses broadened my initial output-focused view into a lifecycle perspective involving representative evaluation, provenance, human review and continuing monitoring (NIST, 2024). The additional activity applied this directly to fabricated academic citations, defining publication-identity and claim-support checks rather than relying on fluent output.

The Group C project designed an Academic Research Agent. My recorded individual contribution concerned development methodology and selection of frameworks, APIs and models. I initially proposed Agile prototyping, SQLite and named development tools. Team discussion showed that the assessed task needed an architecture-first account of responsibilities, interfaces, data flow and evaluation. I revised my contribution accordingly, supported replacing SQLite with lightweight JSON, removed tools from architectural requirements and helped make the LLM layer provider-agnostic. I also reviewed LangGraph, Pydantic, HTTPX, Tenacity, arXiv, OpenAlex and CORE and added supporting sources. This evidence demonstrates that I responded constructively to peers rather than defending familiar choices.

The Unit 11 implementation realises that design as four cooperating components. A planning agent converts a goal into bounded search tasks; a retrieval agent queries OpenAlex or an offline fixture; a processing agent normalises, deduplicates and ranks records; and a storage agent writes Markdown, JSON and an execution trace. Ollama supplies optional LLM planning, but schema validation and deterministic fallback prevent malformed model output from controlling execution. Seven automated tests cover validation, planning bounds, model failure, retrieval, ranking, persistence, evidence sufficiency and the cycle limit. The reproducible demonstration retained three evidence records and generated all expected outputs. These results demonstrate software behaviour, not the scholarly quality of a real literature review.

## Learning outcomes

1. **Architectures and approaches:** forum analysis, the KQML/KIF exercise and the four-role project distinguish reactive communication, deliberative planning and cooperative agent responsibilities.
2. **Application under uncertainty:** the final system applies planning and retrieval to academic research while exposing incomplete metadata, shallow relevance scoring and model/network failure.
3. **Tools and responsibility:** Python, unit testing, OpenAlex, Ollama, provenance records and bounded execution demonstrate deployment choices informed by ethical and professional risk.
4. **Virtual teamwork:** discussion posts, peer responses and the Group C design record evidence review, negotiation and revision of my own proposals.

## Formative case studies

### Case study 1: Bias in autonomous ranking

**What?** The processing agent ranks retrieved works using keyword overlap and a bounded citation-count signal. This is transparent and repeatable, but citation counts can favour older, highly visible or well-resourced research communities.

**So what?** A deterministic score is not neutral merely because it is explainable. Ranking affects which evidence a researcher sees first and can reproduce structural inequalities in scholarly visibility. OpenAlex coverage and missing abstracts add source-selection bias. This challenged my earlier tendency to equate reproducibility with fairness.

**Now what?** I would create a manually labelled evaluation set spanning publication years, disciplines and regions, report ranking performance by subgroup, and let users switch or remove citation weighting. The interface should explain the score and show unranked or low-ranked results rather than hiding them.

### Case study 2: Safety constraints and bounded autonomy

**What?** The workflow can autonomously plan, retrieve, assess sufficiency and repeat. I implemented two boundaries: two-to-five validated planning tasks and a maximum of three retrieval cycles. An unavailable or malformed LLM response triggers a deterministic fallback.

**So what?** Unit 1 discussions had framed overrides abstractly; implementation made the issue operational. A loop without a stop condition can waste resources, amplify poor queries or repeatedly contact an external service. Safe failure is therefore part of correct behaviour, not an optional restriction. The test that forces insufficient evidence and confirms the cycle limit provides direct evidence.

**Now what?** A deployed version should add time and request budgets, cancellation, rate-limit handling and alerts. Higher-risk actions should require explicit human approval, with the trace preserving who approved what and why.

### Case study 3: Explainable decisions and evidence provenance

**What?** The agent preserves source URLs, DOI metadata, matched queries and retrieved abstract text. Its trace records planning, searches, failures, counts and stopping decisions. Reports explicitly state that retrieved summaries are not model-generated conclusions.

**So what?** Walters and Wilder (2023) show that language models can fabricate citations. In a multi-agent system, unsupported content can pass between roles and acquire credibility through repetition. Exposing process steps helps, but a trace only explains what the software did; it does not prove that a source is credible or supports a claim.

**Now what?** I would add DOI-resolution checks and sentence-level links between claims and source passages. A manually assessed claim-support benchmark and appropriate-abstention measure would test whether explanation corresponds to evidence. Human verification would remain mandatory before academic use.

## Professional skills matrix and action plan

| Skill | Evidence developed | Current evaluation | Action |
|---|---|---|---|
| Critical analysis | Three discussion summaries and design critique | Stronger at comparing trade-offs than at the module start | Quantify comparisons with explicit evaluation criteria |
| Software engineering | Modular Python, typed models, CLI and seven tests | Reproducible core with clear boundaries | Add integration tests for live API failure modes |
| Research | Reading summaries, scholarly APIs and referenced discussions | Improved provenance awareness | Build a manually labelled relevance dataset |
| Teamwork | Peer responses and revision of Group C contribution | Demonstrated responsiveness to criticism | Record decisions and ownership during future meetings |
| Ethical awareness | Risk discussion, three case studies and safety controls | Able to translate principles into controls | Add bias, privacy and prompt-injection checks before deployment |
| Communication | KQML exercise, reports, README and presentation | Technical ideas expressed for different audiences | Practise shorter evidence-led demonstrations |

<!-- SUPPORTING-NARRATIVE-END -->

# Final Reflective Commentary

<!-- REFLECTION-START -->

## What?

My central project was an Academic Research Agent that receives a research goal, plans searches, retrieves scholarly metadata, processes the results and stores an inspectable report. The implemented workflow separates planning, retrieval, processing and storage. It supports Ollama for language-model planning and OpenAlex for live evidence retrieval, while deterministic planning and an offline fixture make execution reproducible when a model or network is unavailable. Seven automated tests passed, and the demonstration generated a Markdown report, JSON evidence and a workflow trace.

The project brought together a sequence of module activities. Early discussion led me to see autonomy as bounded delegation rather than unrestricted independent action. The KQML/KIF exercise demonstrated that communication has layers: a performative can state intent, formal content can encode a proposition, and identifiers can preserve conversational context. The constituency trees then showed that a valid representation may still permit competing interpretations. Later work on deep learning and responsible AI connected these technical uncertainties with provenance, bias, privacy, oversight and accountability.

My individual Group C contribution focused on development methodology and technology selection. I began with an Agile prototyping approach and suggestions including SQLite and named development tools. Peer discussion challenged whether these decisions belonged in the architecture and whether they were proportionate to a lightweight academic prototype. I changed the proposal to an architecture-first method, accepted JSON storage and removed avoidable provider and tooling dependencies. That change became important during implementation: explicit component interfaces made the final system testable without requiring every external service.

## So what?

At the start, I was most comfortable evaluating an agent by what it could do. The discussions and implementation shifted my attention to the conditions under which its output should be trusted. I found the move away from familiar tools uncomfortable because my initial choices felt concrete and practical. However, defending a preferred stack would have confused implementation convenience with system requirements. The team’s criticism helped me treat revision as evidence of engineering judgement rather than as failure of the first idea.

This changed how I understand autonomy. Wooldridge and Jennings (1995) identify autonomy, reactivity, proactivity and social ability as central agent characteristics, but these properties do not establish that behaviour is safe or useful. In the final system, autonomous task creation creates risk as well as efficiency. A poor plan can produce repeated weak searches, and an LLM can return malformed or unsupported content. I therefore constrained the planner’s schema, limited task and cycle counts, and preserved a deterministic fallback. The cycle-limit test matters because it converts the abstract concept of a kill switch into observable behaviour.

Communication work produced a related insight. KQML can communicate intention, but shared syntax does not ensure shared semantics. Likewise, a pipeline can successfully pass a record between agents even when that record is irrelevant or misleading. The Unit 8 ambiguous parse reinforced this distinction between valid structure and justified meaning. In the research agent, typed records ensure structural consistency, while provenance and human review address meaning and evidence quality. Neither substitutes for the other.

My view of explainability also became more critical. Recording a trace improves accountability because it exposes queries, failures and stop decisions. Yet a transparent keyword score can still be biased, and a DOI can identify a real paper without proving that it supports a generated claim. Walters and Wilder’s (2023) findings on fabricated citations made this risk concrete, while NIST’s (2024) lifecycle approach showed why one test result cannot guarantee responsible deployment. I learned to distinguish software correctness, information quality and fitness for use. The offline tests establish the first; they do not establish the other two.

The strongest evidence of my technical development is the path from a design contribution to executable, tested components. I can now define agent boundaries, inject replaceable dependencies, validate model output, design deterministic fallbacks and capture execution evidence. My weakest area remains empirical evaluation. The current ranking uses transparent proxies rather than a labelled relevance dataset, and I did not conduct a user study. Acknowledging these limits is more useful than overstating the prototype as a complete systematic-review tool.

Team participation also altered my working practice. My peer responses across the three discussions did more than confirm agreement: they introduced coordination risk, ontology alignment, representative testing, privacy and provenance into my conclusions. In Group C, simplifying storage and decoupling providers resulted from collaborative review. I learned that effective virtual teamwork requires visible reasoning and a willingness to update decisions. In future, I would strengthen this by maintaining a decision log that records options, evidence, owners and acceptance criteria, making contribution and accountability easier to evaluate.

## Now what?

My next technical step is to build a small, manually labelled collection of research goals and candidate papers. I would measure retrieval precision and recall, citation validity, claim support and appropriate abstention, then examine results across disciplines and publication years. I would add DOI resolution, sentence-level evidence links, request and time budgets, cancellation and tests for prompt injection or hostile metadata. Any model or data-provider change would trigger renewed evaluation rather than inheriting trust from the previous configuration.

Professionally, I will begin future intelligent-agent projects with three parallel questions: what behaviour is required, what evidence demonstrates it, and what boundary limits harm when assumptions fail? I will separate architectural requirements from preferred tools, make uncertainty visible, and preserve human approval for consequential actions. The module has therefore changed my conception of a successful agent from one that completes a task to one whose actions, limitations and responsibilities can be examined and governed.

<!-- REFLECTION-END -->

# References

Jennings, N.R. (2000) 'On agent based software engineering', *Artificial Intelligence*, 117(2), pp. 277-296.

National Institute of Standards and Technology (NIST) (2024) *Artificial Intelligence Risk Management Framework: Generative Artificial Intelligence Profile*. NIST AI 600-1. Gaithersburg, MD: NIST. Available from: https://doi.org/10.6028/NIST.AI.600-1 [Accessed 29 September 2026].

Rolfe, G., Freshwater, D. and Jasper, M. (2001) *Critical reflection in nursing and the helping professions: a user's guide*. Basingstoke: Palgrave Macmillan.

Russell, S.J. and Norvig, P. (2021) *Artificial Intelligence: A Modern Approach*. 4th edn. Harlow: Pearson Education.

Walters, W.H. and Wilder, E.I. (2023) 'Fabrication and errors in the bibliographic citations generated by ChatGPT', *Scientific Reports*, 13, article 14045. Available from: https://doi.org/10.1038/s41598-023-41032-5 [Accessed 29 September 2026].

Wooldridge, M.J. and Jennings, N.R. (1995) 'Intelligent agents: theory and practice', *The Knowledge Engineering Review*, 10(2), pp. 115-152.

# Evidence Index

- Units 1-3: Collaborative Discussion 1 initial post, three peer responses and summary post.
- Units 5-7: Collaborative Discussion 2 posts; Unit 5 required reading summary; Unit 6 KQML/KIF dialogue, README and tests.
- Unit 8: Constituency parse trees, including both readings of prepositional-phrase attachment.
- Units 9-11: Collaborative Discussion 3 posts, ethical additional task and Unit 9 reflection.
- Group project: Design proposal, peer evaluation and individual team-discussion reflection.
- Unit 11: Academic Research Agent source, tests, README, execution evidence, presentation and transcript.

**Submission note:** Verify this account against your own experience and the University's current guidance on declaring AI assistance before submission to Turnitin.