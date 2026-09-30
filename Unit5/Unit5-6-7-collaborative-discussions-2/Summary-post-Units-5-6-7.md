# Summary Post

Across Units 5–7, my understanding of agent communication has shifted from comparing mechanisms to considering the agreements that make communication dependable. My initial post argued that KQML expresses communicative intentions through performatives while allowing receivers to choose their internal implementation (Finin et al., 1994). This supports autonomy and loose coupling, although parsing, routing and conversation management introduce overhead compared with Python or Java method calls.

Unit 5 highlighted the distinction between message structure and shared meaning. Isaac’s discussion prompted me to emphasise that valid ACL messages cannot guarantee interoperability. Yasmin’s feedback extended this concern to scalability. Payne and Tamma (2014) show how two agents can negotiate ontological correspondences under incomplete knowledge; their findings do not establish semantic consistency across an expanding network. I would therefore reuse validated mappings with ontology versions and renegotiate when assumptions change.

Dragos’s examples clarified the architectural boundary: DOI deduplication suits a deterministic method, whereas query reformulation may require autonomous interpretation. My response added that reformulation needs agreed constraints and failure outcomes. The Unit 6 Alice and Bob exercise made these distinctions concrete: KQML identified the communicative act, KIF represented warehouse facts, and reply identifiers connected questions with answers. However, its predefined shared ontology leaves open the harder problem of communication between unfamiliar agents.

Unit 7’s treatment of pragmatics reinforced the importance of context. Word representations can capture semantic relationships (Mikolov et al., 2013), but I would treat similarity as evidence for investigating a mapping, rather than proof of equivalent operational meaning.

I therefore retain the hybrid approach, with stronger conditions: methods for stable internal operations and ACLs where autonomy and negotiation justify their cost. My main learning is that reliable coordination requires explicit semantic agreements, bounded conversations and recoverable failures. I would assess success through correct task outcomes and communication costs as the system grows.


## References

Finin, T., Fritzson, R., McKay, D. and McEntire, R. (1994) ‘KQML as an agent communication language’, in *Proceedings of the Third International Conference on Information and Knowledge Management*, pp. 456–463. Available at: [author-hosted paper](https://research.cs.umbc.edu/kqml/papers/kqml-acl-html/root2.html) (Accessed: 15 September 2026).

Mikolov, T., Sutskever, I., Chen, K., Corrado, G.S. and Dean, J. (2013) ‘Distributed representations of words and phrases and their compositionality’, *Advances in Neural Information Processing Systems*, 26, pp. 3111–3119. Available at: [author manuscript](https://arxiv.org/abs/1310.4546) (Accessed: 15 September 2026).

Payne, T.R. and Tamma, V. (2014) ‘Negotiating over ontological correspondences with asymmetric and incomplete knowledge’, in *Proceedings of the 13th International Conference on Autonomous Agents and Multiagent Systems (AAMAS 2014)*, pp. 517–524. Available at: [conference paper](https://www.ifaamas.org/Proceedings/aamas2014/aamas/p517.pdf) (Accessed: 15 September 2026).
