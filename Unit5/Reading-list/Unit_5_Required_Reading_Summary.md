**UNIT 5**

Required Reading Summary

*Speech Acts, Agent Communication and Ontology Negotiation*

<table>
<colgroup>
<col style="width: 100%" />
</colgroup>
<thead>
<tr>
<th><strong>Required Reading 1</strong><br />
Searle, J.R. (1969) Speech Acts: An Essay in the Philosophy of Language. Cambridge: Cambridge University Press. pp. 1–53.</th>
</tr>
</thead>
<tbody>
<tr>
<td><strong>Required Reading 2</strong><br />
Payne, T.R. and Tamma, V. (2014) 'Negotiating over ontological correspondences with asymmetric and incomplete knowledge', AAMAS, 13(1), pp. 517–524.</td>
</tr>
</tbody>
</table>

| **Unit 5 focus:** Searle provides the philosophical basis for communication as action, while Payne and Tamma show how autonomous agents can use structured dialogue to negotiate shared meaning when their ontologies and knowledge differ. |
|----|

# 1. Searle (1969): Speech Acts, pp. 1–53

**Central idea:** speaking is a form of action. Language does not merely describe the world; speakers use language to perform actions such as asserting, asking, requesting, commanding, promising and warning. Searle therefore treats speaking a language as a rule-governed form of behaviour.

## Examples of communication as action

| **Utterance**                | **Action being performed** |
|------------------------------|----------------------------|
| “The server is unavailable.” | Informing / asserting      |
| “Is the server unavailable?” | Asking                     |
| “Restart the server.”        | Requesting / commanding    |
| “I promise to restart it.”   | Promising                  |

## 1.1 Methods and scope

Searle begins by asking how sounds or written symbols acquire meaning and how one person can communicate something to another. He is interested in how a listener recognises whether an utterance is a statement, question, command or promise, and how language refers to objects and situations in the world.

Rather than treating language simply as a collection of sentences, Searle focuses on linguistic communication as behaviour governed by rules. This makes the discussion relevant to agent-based systems because an agent message is not merely data: it can represent a communicative act.

| **Agent-system example:** A message such as REQUEST(agent2, retrieve_papers) is not just a string. It represents a request by one agent for another agent to perform an action. |
|----|

## 1.2 Linguistic characterisations

Searle argues that analysing ordinary language can reveal the underlying rules that govern communication. If speakers consistently recognise something as a promise, request or statement, the analyst can examine the conditions that make that interpretation possible.

The key point is that speech acts depend on conditions and conventions. Successful communication therefore requires more than producing grammatically correct words; the act must be interpretable within a shared system of rules.

## 1.3 The principle of expressibility

A further idea introduced in the opening chapters is the Principle of Expressibility. In simplified terms, whatever a speaker can mean can, in principle, be expressed linguistically. This does not mean that every language already contains a convenient word for every idea. Rather, linguistic resources can be combined or extended to communicate intended meaning.

For multi-agent systems, this highlights the need for communication languages that are sufficiently expressive to represent beliefs, goals, intentions and other relevant states.

## 1.4 Expressions, meaning and speech acts

Searle distinguishes several levels at which an act of communication can be understood:

- **Utterance act:** Producing words, symbols or sentences.

- **Propositional act:** Referring to something and predicating something about it.

- **Illocutionary act:** The communicative action being performed, such as asserting, requesting, commanding, promising, warning or questioning.

### Propositional content versus illocutionary force

Essentially the same subject matter can be expressed with different communicative forces. For example, “Sam smokes habitually” functions as an assertion, whereas “Does Sam smoke habitually?” functions as a question. The proposition concerns Sam and smoking, but the illocutionary force differs.

In agent communication, INFORM(B, task_complete) and QUERY(B, task_complete) may concern the same proposition, task_complete, while performing different communicative actions.

## 1.5 Regulative and constitutive rules

Searle distinguishes between regulative rules and constitutive rules:

- **Regulative rules:** Regulate activities that already exist.

- **Constitutive rules:** Help create or define the activity itself. They can be understood using a pattern such as “X counts as Y in context C.”

This distinction is especially important for agent protocols. A message such as ACCEPT has a particular operational meaning only because the protocol defines what ACCEPT counts as and what consequences follow from it.

## 1.6 Meaning and intention

Communication involves the relationship between speaker intention, linguistic conventions and listener recognition. When someone says “Please close the door,” the intended effect is not only that the hearer understands the words but that the hearer recognises them as a request.

For AI agents, exchanging JSON, XML or plain text does not automatically guarantee successful communication. Agents must also share enough semantic and protocol-level understanding to recognise the purpose of a message.

## 1.7 Brute facts and institutional facts

Searle also introduces a distinction between facts that exist independently of social institutions and facts that depend on systems of rules and conventions.

- **Brute fact:** A fact such as “the object weighs 5 kg,” which does not depend on a social institution.

- **Institutional fact:** A fact such as “this person is married,” “this paper is worth €20,” or “this team won the match,” which depends on socially established rules and institutions.

In agent systems, concepts such as permission, authority, ownership, payment, contracts and commitments are often institutional in this sense because their meaning depends on rules within the environment.

# 2. Payne and Tamma (2014): Negotiating Ontological Correspondences

**Central problem:** autonomous agents may need to communicate even though they use different ontologies, possess incomplete knowledge and hold private or asymmetric information about how their concepts correspond.

## 2.1 Why ontology alignment matters

An ontology provides a formal vocabulary and relationships for representing knowledge. If two agents use different conceptual structures or labels, they may interpret the same message differently. Effective communication therefore depends on establishing correspondences between concepts in their separate ontologies.

| **Simple example:** Agent A may use the concept ResearchPaper while Agent B uses AcademicArticle. If both concepts are intended to represent the same thing, the agents need a correspondence such as ResearchPaper ≡ AcademicArticle. |
|----|

## 2.2 The negotiation problem

A correspondence is a mapping connecting an entity in one ontology with an entity in another. A set of compatible correspondences can form an ontology alignment. The challenge is that autonomous agents may not have complete or identical knowledge.

- **Incomplete knowledge:** Neither agent necessarily knows every valid correspondence.

- **Asymmetric knowledge:** One agent may know correspondences that the other does not know.

- **Private knowledge:** Agents may not want to reveal all the correspondences or beliefs they possess.

- **Uncertainty:** Agents may assign different degrees of belief to the same correspondence.

These characteristics make ontology alignment a negotiation problem rather than a simple database-merging exercise.

## 2.3 Correspondence Inclusion Dialogue (CID)

The paper proposes the Correspondence Inclusion Dialogue (CID), a structured protocol that allows two agents to negotiate which ontological correspondences should be included in their shared alignment. Agents can selectively disclose information rather than revealing their complete knowledge bases.

The protocol uses communicative moves such as:

- **JOIN:** enter the dialogue.

- **ASSERT:** put forward a correspondence or belief.

- **OBJECT:** challenge a proposed correspondence.

- **ACCEPT / REJECT:** indicate whether a proposal is considered viable.

- **ENDASSERT:** signal the end of the assertion phase.

- **CLOSE:** terminate the dialogue.

The moves are governed by protocol conditions, making the dialogue explicitly rule-based. This provides a direct conceptual link to Searle: the messages do not merely contain information; they perform actions within a defined communicative context.

## 2.4 Degrees of belief and admissibility

Agents can associate a degree of belief with a proposed correspondence. Rather than treating a mapping as simply true or false, the protocol can represent uncertainty. The agents can combine their beliefs and use an admissibility threshold to decide whether a correspondence is strong enough to retain.

| **Illustrative example:** If Agent A assigns 0.8 confidence to Paper ≡ Article and Agent B assigns 0.6, the protocol can reason about their combined support rather than relying on a simple yes/no vote. |
|----|

## 2.5 Resolving disagreement: the attack graph

Conflicting or ambiguous correspondences can arise. For example, the same source concept might be mapped to more than one competing target concept. Agents can object to such mappings, and the proposed correspondences and their conflicts can be represented using an attack graph influenced by argumentation theory.

Stronger correspondences can defeat weaker competing correspondences, allowing the dialogue to finish with an unambiguous alignment rather than retaining incompatible mappings.

## 2.6 Alice and Bob example

The paper illustrates CID using two agents, Alice and Bob. Each agent has a private ontology, a different collection of known correspondences and individual degrees of belief. Through assertions, objections, acceptances and rejections, they negotiate which correspondences should survive without unnecessarily revealing all of their information.

The important lesson is that agreement can emerge through structured dialogue even when the agents begin with different and incomplete knowledge.

## 2.7 Evaluation and findings

The authors evaluate the approach using ontology-alignment data covering 21 ontology pairs. Sixteen existing alignments were divided randomly between the two agents, with each receiving eight, and each experiment was repeated 500 times.

- The dialogue produced solutions that were generally close to those obtained by a centralised exhaustive approach with complete information.

- In all but three ontology-pair cases under the reported comparison, solutions were within approximately 94.9% of the optimal exhaustive solution.

- Filtering weak correspondences could improve precision by up to approximately 40%, depending on the admissibility threshold, while only moderately affecting recall.

- The paper reports average disclosure of only 16.76% of the agents’ individual correspondences in its headline results, demonstrating the privacy advantage of selective disclosure.

## 2.8 Important limitation

A significant limitation is that no individual agent necessarily has enough information to verify whether the fully combined ontology is globally logically coherent. Each agent can reason relative to the information it possesses, but privacy and decentralisation restrict global verification.

| **Critical evaluation point:** CID trades complete global knowledge for privacy and decentralisation. This can improve autonomy and reduce disclosure, but it also makes full consistency checking more difficult. |
|----|

# 3. How the Two Readings Connect

The readings operate at different levels but address the same underlying question: how can meaningful communication take place when participants must interpret not only information but also the action and semantics attached to that information?

| **Searle (1969)** | **Payne and Tamma (2014)** |
|----|----|
| Communication involves performing actions. | Agents communicate using explicit dialogue moves. |
| Language is rule-governed behaviour. | CID is a rule-governed negotiation protocol. |
| Speech acts have illocutionary force. | ASSERT, OBJECT, ACCEPT and REJECT identify communicative purposes. |
| Constitutive rules give actions their meaning in context. | Protocol preconditions and consequences determine what agent moves mean and when they are valid. |
| Meaning must be recognised by communication participants. | Agents require shared semantic mappings to interpret one another. |
| Communication depends on conventions and shared rules. | Ontology alignment supports semantic interoperability between heterogeneous agents. |
| Institutional meaning depends on rule systems. | Protocol rules give otherwise simple messages operational significance. |

| **Big Unit 5 idea:** Autonomous agents cannot cooperate effectively merely by exchanging data. They also need agreed semantics for what the data means and protocols governing what communicative actions such as requesting, asserting, accepting and rejecting actually do. |
|----|

# 4. Five Concepts to Remember

**1. Speech act:** Communication is an action, not merely the transmission of words or data.

**2. Illocutionary force:** Identifies what the communicator is doing: asserting, requesting, promising, questioning and so on.

**3. Constitutive rules:** Rules can create the meaning of actions within a system or protocol.

**4. Ontology alignment:** Mappings allow agents that use different vocabularies to understand one another.

**5. Negotiation under incomplete knowledge:** Agents can reach useful agreements without revealing everything they know.

# 5. Quick Revision Questions

- What does Searle mean by describing speaking a language as rule-governed behaviour?

- What is the difference between propositional content and illocutionary force?

- How do constitutive rules differ from regulative rules?

- Why can two autonomous agents fail to understand one another even if both are communicating correctly at the syntactic level?

- What problem does ontology alignment solve?

- How does CID allow agents to negotiate while limiting disclosure of private knowledge?

- What role do degrees of belief and admissibility thresholds play in the negotiation?

- Why is global logical coherence difficult to guarantee when agents have asymmetric and incomplete knowledge?

# References

Payne, T.R. and Tamma, V. (2014) ‘Negotiating over ontological correspondences with asymmetric and incomplete knowledge’, in Lomuscio, A., Scerri, P., Bazzan, A. and Huhns, M. (eds.) Proceedings of the 13th International Conference on Autonomous Agents and Multiagent Systems (AAMAS 2014). Paris, France, 5–9 May 2014, pp. 517–524.

Searle, J.R. (1969) Speech Acts: An Essay in the Philosophy of Language. Cambridge: Cambridge University Press.
