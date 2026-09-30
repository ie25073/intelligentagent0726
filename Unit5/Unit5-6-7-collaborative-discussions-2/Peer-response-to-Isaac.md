# Peer Response to Isaac

Isaac, your distinction between communicative intention and direct execution is persuasive, particularly your observation that an ACL allows the receiver to retain autonomy over how, or whether, it responds. Your inventory example also makes loose coupling tangible. I would, however, qualify the claim that ACLs provide interoperability. They create the conditions for interoperability, but do not guarantee it. A shared message envelope can coexist with different interpretations of the performative, content or ontology. Payne and Tamma (2014) show that semantic heterogeneity persists when agents possess incomplete and private knowledge of correspondences, even if both parties communicate through a structured dialogue.

Several measures could reduce this risk. First, a system could adopt a small, versioned set of performatives, with explicit preconditions, expected replies and failure states. Second, message schemas and ontology identifiers should be validated at the boundary rather than trusted merely because a message parses. Third, conversation identifiers, time-outs and idempotency keys would help agents associate replies with requests and recover safely from duplicate or missing messages. Finally, authentication, authorisation and audit logs should be part of the protocol design because loose coupling otherwise enlarges the attack surface.

Your discussion of newer protocols is useful because it shows that the interoperability problem remains current. I think the strongest architectural response is therefore layered: use ACLs between independently governed agents, but retain ordinary methods within each agent for deterministic operations. This limits semantic and messaging overhead without sacrificing autonomy at the points where it matters. Would you also make ontology-version negotiation a mandatory opening stage of every inter-agent conversation, or only when the agents have not interacted before?

**Word count: 267**

## References

Finin, T., Weber, J., Wiederhold, G., Genesereth, M., Fritzson, R., McKay, D., McGuire, J., Pelavin, R., Shapiro, S. and Beck, C. (1993) *Specification of the KQML Agent-Communication Language*. DARPA Knowledge Sharing Initiative, External Interfaces Working Group. Available at: [https://research.cs.umbc.edu/kqml/papers/](https://research.cs.umbc.edu/kqml/papers/) (Accessed: 1 September 2026).

Payne, T.R. and Tamma, V. (2014) ‘Negotiating over ontological correspondences with asymmetric and incomplete knowledge’, in *Proceedings of the 13th International Conference on Autonomous Agents and Multiagent Systems (AAMAS 2014)*, pp. 517–524. Available at: [https://www.ifaamas.org/Proceedings/aamas2014/aamas/p517.pdf](https://www.ifaamas.org/Proceedings/aamas2014/aamas/p517.pdf) (Accessed: 1 September 2026).
