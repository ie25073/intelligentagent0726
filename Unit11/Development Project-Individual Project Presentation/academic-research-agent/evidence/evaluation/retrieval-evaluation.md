# Retrieval Ranking Evaluation

The identifiers used in this evaluation belong to synthetic fixture records. They are not registered scholarly DOIs and are included only for reproducible testing.

Offline fixture ranking evaluation; not a live OpenAlex coverage benchmark.

## Summary

- Labelled queries: 4
- Mean Precision@1: 1.0
- Mean Precision@3: 0.5
- Mean nDCG@3: 1.0
- Single-relevance top-rank target passed: True

## Interpretation

The fixture confirms that deterministic keyword/citation ranking can be tested repeatably. It does not prove live search coverage, semantic relevance or source quality. Those claims require a larger labelled dataset and live retrieval runs.

## Cases

### explainable planning autonomous research agents
- Ranked synthetic fixture identifiers: `10.1000/agent.1`, `10.1000/agent.3`, `10.1000/agent.2`
- Precision@1: 1.0
- Precision@3: 0.3333
- nDCG@3: 1.0
- Expected top met: True

### evidence retrieval multi-agent systems evaluation
- Ranked synthetic fixture identifiers: `10.1000/agent.2`, `10.1000/agent.1`, `10.1000/agent.3`
- Precision@1: 1.0
- Precision@3: 0.3333
- nDCG@3: 1.0
- Expected top met: True

### language model research assistants citation hallucination provenance
- Ranked synthetic fixture identifiers: `10.1000/agent.3`, `10.1000/agent.1`, `10.1000/agent.2`
- Precision@1: 1.0
- Precision@3: 0.3333
- nDCG@3: 1.0
- Expected top met: True

### autonomous research agents evidence retrieval safety
- Ranked synthetic fixture identifiers: `10.1000/agent.1`, `10.1000/agent.2`, `10.1000/agent.3`
- Precision@1: 1.0
- Precision@3: 1.0
- nDCG@3: 1.0
- Expected top met: True
