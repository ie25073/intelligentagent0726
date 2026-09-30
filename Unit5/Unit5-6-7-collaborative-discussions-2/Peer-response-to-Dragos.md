# Peer Response to Dragos

Dragos, your DOI-deduplication and query-reformulation examples establish a useful boundary between method invocation and agent communication. I agree that deterministic deduplication belongs inside the orchestrator: its result should follow a stable contract, and wrapping it in KQML would introduce parsing and coordination without adding meaningful autonomy. Your reformulation example is different because the receiving agent must interpret a goal and choose how to pursue it.

One nuance is that an action-oriented performative does not by itself make the request unambiguous. Speech-act theory separates the proposition from its illocutionary force (Searle, 1969), but both levels still need shared rules. The agents must agree on what “reformulate” permits: for example, whether the planning agent may broaden the topic, replace terms using an ontology, or relax inclusion criteria. Otherwise, two agents can recognise the message as a request yet disagree about a valid outcome. This reflects Payne and Tamma’s (2014) finding that heterogeneous, incomplete ontological knowledge can obstruct mutual interpretation.

I would therefore strengthen your hybrid design with an explicit interaction contract. The request should include the source query, objective, ontology version, constraints and a correlation identifier. The response should report the revised query, transformations made and confidence; refusal, timeout and low-confidence outcomes should also be defined. An audit log would then allow the orchestrator to explain why retrieval changed, while a fallback could preserve the original query if reformulation fails.

Your practical boundary is convincing because it bases the choice on autonomy rather than physical distribution. Would you treat a frequently repeated reformulation as evidence that it should become a deterministic local method, or retain it as agent work because its interpretation remains context-dependent?

**Word count: 272**

## References

Payne, T.R. and Tamma, V. (2014) ‘Negotiating over ontological correspondences with asymmetric and incomplete knowledge’, in *Proceedings of the 13th International Conference on Autonomous Agents and Multiagent Systems (AAMAS 2014)*, pp. 517–524. Available at: [https://www.ifaamas.org/Proceedings/aamas2014/aamas/p517.pdf](https://www.ifaamas.org/Proceedings/aamas2014/aamas/p517.pdf) (Accessed: 1 September 2026).

Searle, J.R. (1969) *Speech Acts: An Essay in the Philosophy of Language*. Cambridge: Cambridge University Press. Available at: [https://doi.org/10.1017/CBO9781139173438](https://doi.org/10.1017/CBO9781139173438) (Accessed: 1 September 2026).
