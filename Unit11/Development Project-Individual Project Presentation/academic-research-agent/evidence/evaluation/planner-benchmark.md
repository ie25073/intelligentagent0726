# Planner Operational Benchmark

Goal: Explainable decisions in autonomous research agents

This is an operational planner benchmark, not a comparative benchmark of real Qwen, Mistral or Llama model quality. Real local-model benchmarking requires those models to be installed on the target host and should additionally record memory, context size and token throughput.

| Mode | Valid schema runs | Fallback runs | Mean latency ms | p95 latency ms | Note |
|---|---:|---:|---:|---:|---|
| rules | 10/10 | 0 | 0.003 | 0.007 | Deterministic baseline with no model dependency. |
| mocked_ollama_valid | 10/10 | 0 | 0.079 | 0.554 | Simulates a schema-conforming Ollama response. |
| mocked_ollama_invalid | 10/10 | 10 | 0.018 | 0.038 | Simulates malformed model output; fallback should activate. |
| ollama_unavailable | 10/10 | 10 | 0.009 | 0.012 | Simulates missing local runtime; fallback should activate. |
