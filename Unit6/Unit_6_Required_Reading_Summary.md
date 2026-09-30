# Unit 6 Required Reading Summary

## Required Reading

**Finin, T., Fritzson, R., McKay, D. and McEntire, R. (1994) ‘KQML as an agent communication language’, in *Proceedings of the Third International Conference on Information and Knowledge Management (CIKM ’94)*, pp. 456–463.**

## Overview

Finin et al. (1994) present the Knowledge Query and Manipulation Language (KQML) as both a message format and a protocol for exchanging information and knowledge between autonomous software agents. KQML emerged from the US Advanced Research Projects Agency (ARPA) Knowledge Sharing Effort, which sought to make large knowledge-based systems more reusable and interoperable.

The paper responds to a distributed-computing problem that remains important: independently developed systems may use different platforms, programming languages, data formats, internal representations and communication mechanisms. Direct integration creates tight dependencies between these systems. KQML instead provides a common communication layer through which an agent can express the purpose of a message while remaining largely independent of the receiver’s internal implementation.

The paper’s central claim is that exchanging data is not sufficient for intelligent-agent communication. An agent must also indicate what communicative action it is performing, such as asking a question, asserting a belief, requesting an ongoing stream of information or advertising a capability.

## 1. The Distributed-Agent Problem

The authors describe emerging information environments as distributed, heterogeneous, dynamic and composed of autonomous nodes. Conventional client-server communication is considered too restrictive because a participant may need to act as both client and server, initiate communication and respond asynchronously to changing information.

Intelligent agents offer a possible solution because they can:

- Communicate through an expressive agent communication language.
- Cooperate to achieve goals that are difficult for one system to accomplish alone.
- Act on their own initiative rather than only responding to direct calls.
- Use local knowledge to manage resources and answer requests from other agents.

KQML is intended to support these capabilities without requiring every agent to share the same software architecture.

## 2. The ARPA Knowledge Sharing Effort

The Knowledge Sharing Effort divided the knowledge-interoperability problem among four complementary groups:

1. **Interlingua:** developed the Knowledge Interchange Format (KIF), a common language based largely on first-order logic for expressing knowledge.
2. **Knowledge Representation System Specification (KRSS):** sought common constructs across families of knowledge-representation systems.
3. **Shared, Reusable Knowledge Bases (SRKB):** addressed shared ontologies, reusable knowledge and supporting repositories.
4. **External Interfaces:** addressed run-time interaction between knowledge-based systems and other components. KQML was a principal result of this group.

This division reveals an important distinction. KIF represents the actual knowledge contained in a message, while KQML specifies the communicative purpose and handling of that message. An agent could therefore carry KIF, SQL, Prolog or another representation language inside a KQML envelope.

## 3. Syntax, Semantics and Pragmatics

The paper explains agent communication through three related requirements:

- **Syntax:** agents need a common representation language, or languages that can be translated.
- **Semantics:** agents need shared concepts and relationships, normally expressed through an ontology, so that message content has a mutually understood meaning.
- **Pragmatics:** agents need to know whom to contact, how to locate them, what communicative act is being performed and how the interaction should continue.

KQML primarily addresses pragmatics and only indirectly addresses semantics. It cannot by itself guarantee that two agents interpret a domain concept identically. The agents must still agree on an ontology or possess a reliable translation between ontologies.

## 4. KQML Message Structure

KQML uses a parenthesised, Lisp-like syntax. The first element identifies the **performative**, while the remaining keyword-value pairs provide arguments and metadata. A simplified message has the following form:

```lisp
(ask-one
  :sender Alice
  :receiver Bob
  :language KIF
  :ontology warehouse-stock
  :content "(available-stock ?television ?quantity)")
```

The important fields include:

- **Performative:** the communicative act, such as `ask-one` or `tell`.
- **Content:** the proposition, query or instruction being communicated.
- **Language:** the representation language used for the content, such as KIF.
- **Ontology:** the vocabulary and conceptual interpretation assumed by the content.
- **Sender and receiver:** the participating agents or services.
- **Message identifiers:** information that allows replies to be associated with the original request.

KQML infrastructure normally treats the content as opaque. Routers can deliver a message using its performative and metadata without understanding the domain-specific proposition contained inside it. This separation supports heterogeneous agents because their communication mechanism does not need to implement every possible content language.

## 5. Performatives and Speech Acts

Performatives form the core of KQML. They describe the sender’s intended speech act and help determine the expected interaction protocol.

Examples discussed in the paper include:

- **`ask-one`:** request one answer to a query.
- **`ask-all`:** request the complete set of answers.
- **`stream-all`:** request answers as a sequence of separate messages.
- **`tell`:** communicate that the sender considers some content to be true.
- **`deny`:** communicate that a proposition is not accepted as true.
- **`subscribe` or `monitor`:** request future updates whenever the answer changes.
- **`advertise`:** announce the kinds of messages or services an agent can handle.
- **`recruit`:** ask another agent, often a facilitator, to find an agent capable of processing an embedded request.

Performatives can be combined to create richer protocols. For example, a subscription can request a continuing stream of answers, while `standby` can ask a receiver to hold a stream and release each answer only when prompted. KQML therefore supports synchronous questions, asynchronous notifications, streamed answers and capability discovery rather than only one-request/one-response communication.

The performative vocabulary is extensible. This enables communities of agents to develop specialised interactions, but interoperability depends on all participants assigning the same meaning and protocol to each extension.

## 6. Facilitators and Mediators

An agent may know what information it needs without knowing which other agent can supply it. KQML addresses this problem through **communication facilitators**. A facilitator is itself an agent and may provide services such as:

- Registering agent names and capabilities.
- Forwarding messages to named services.
- Routing messages according to metadata or content descriptions.
- Matching information consumers with suitable providers.
- Recommending or recruiting agents.
- Translating or mediating between different services.

For example, Alice might ask a facilitator to find an agent capable of answering a warehouse-stock query. If Bob has advertised that capability, the facilitator can route Alice’s query to Bob or tell Alice how to contact him. This reduces the need for every agent to contain a manually maintained list of all other agents.

## 7. KQML Software Architecture

The paper does not prescribe one mandatory architecture, but describes an experimental implementation containing three main elements:

### Router

Each agent can have a separate router process that handles incoming and outgoing KQML traffic. The router manages communication connections and routes messages using addresses, service names and message metadata. It does not interpret the domain content.

### Facilitator

A facilitator maintains a service registry and assists routers with incompletely addressed messages. Agents register when they start and unregister when they stop. Multiple facilitators can be used for different sites or to provide redundancy.

### KQML Router Interface Library (KRIL)

A KRIL connects an application to its router. It can provide operations for sending messages and registering handlers for asynchronous incoming messages. Different KRIL implementations can integrate KQML with different languages and systems. The authors report experimental interfaces for Common Lisp, C, Prolog, Mosaic and SQL.

This architecture enabled existing applications to participate in a multi-agent system without being completely rewritten. The paper describes a Prolog integration in which remote predicates could appear to the application as though they came from its own local database.

## 8. Reported Applications

The authors describe prototype use across several domains, including:

- Concurrent hardware and software engineering.
- Military transportation planning and scheduling.
- Integration of heterogeneous information sources.
- Cooperative information retrieval and query planning.
- General agent-based software integration.
- Distributed database mediation.

One experiment connected a planner, scheduler, knowledge base and case-based reasoning tool, even though the components were pre-existing systems not originally designed for distributed cooperation. Another connected CoBASE, SIMS and relational-data mediators across three geographically separated Internet sites. These examples support the authors’ claim that KQML can lower the cost of integrating heterogeneous systems by allowing developers to concentrate on what the systems should exchange rather than constructing a bespoke communication mechanism for every pair of tools.

## 9. Advantages of KQML

The main advantages presented or implied by the paper are:

- **Loose coupling:** senders express intentions without depending on the receiver’s internal method names or implementation.
- **Content-language independence:** KQML can transport KIF, SQL, Prolog and other representations.
- **Architectural flexibility:** it supports point-to-point, brokered, synchronous, asynchronous and streaming interactions.
- **Agent discovery:** advertising, recruiting and facilitation help agents locate appropriate services.
- **Legacy integration:** routers and interface libraries can connect existing systems with limited modification.
- **Extensibility:** communities can add performatives for new interaction patterns.
- **Autonomy:** agents can decide how to respond to communicative requests instead of behaving only as remotely invoked procedures.

## 10. Critical Evaluation and Limitations

The paper is an influential design and prototype report, but it does not demonstrate that KQML solves every interoperability problem.

First, KQML separates the message envelope from its content but does not eliminate semantic disagreement. Agents still require compatible content languages and ontologies. A syntactically correct message can therefore be misunderstood.

Second, extensibility creates a trade-off. New performatives allow specialised behaviour, but independently extended vocabularies may no longer be interoperable. The agents must agree on both the meaning of a performative and the protocol that follows from it.

Third, routers and facilitators simplify discovery and delivery but create infrastructure dependencies. A central facilitator may become a bottleneck or single point of failure unless the architecture provides replication, hierarchy or redundancy.

Fourth, the paper reports persuasive prototype examples rather than controlled quantitative evaluation. Claims about lower integration cost and scalability are consequently promising but not comprehensively measured.

Finally, security, authentication, authorisation, malicious messages and accountability receive little attention. These concerns would be essential when applying the design to contemporary open multi-agent systems.

## 11. Connection to the Alice and Bob Exercise

The Unit 6 Python dialogue applies the paper’s central design principles:

- Alice uses `ask-one` because she expects one answer about the televisions.
- Bob uses `tell` to communicate warehouse facts.
- KQML expresses the communicative act and message-handling metadata.
- KIF expresses the stock and HDMI-slot propositions.
- `:language KIF` identifies the content language.
- `:ontology warehouse-stock` identifies the shared vocabulary.
- Conversation and reply identifiers associate Bob’s answers with Alice’s questions.

The exercise therefore demonstrates why an agent message is more than a direct Python method call. Alice communicates what she wants to know, while Bob retains responsibility for interpreting the request and obtaining the answer from his own warehouse knowledge.

## Key Takeaway

> KQML provides a communication layer in which autonomous agents can state the purpose of a message independently of the language used to represent its content. Its performatives, routing metadata and facilitator services support flexible interaction between heterogeneous systems, but genuine interoperability still depends on shared semantics, ontologies and protocol agreements.

## Reference

Finin, T., Fritzson, R., McKay, D. and McEntire, R. (1994) ‘KQML as an agent communication language’, in *Proceedings of the Third International Conference on Information and Knowledge Management (CIKM ’94)*, pp. 456–463. Available at: [https://doi.org/10.1145/191246.191322](https://doi.org/10.1145/191246.191322) (Accessed: 2 September 2026). Original author-hosted version available at: [https://research.cs.umbc.edu/kqml/papers/kqml-acl-html/root2.html](https://research.cs.umbc.edu/kqml/papers/kqml-acl-html/root2.html).
