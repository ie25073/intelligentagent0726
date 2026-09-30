# Unit 9 e-Portfolio Reflection

Draft for personal review, grounded in the existing Group C discussion record. The proposed safeguards below have not been implemented or evaluated.

## Reflection

Unit 9 connects the capabilities of deep learning with the responsibility to evaluate how intelligent systems affect people. My main learning point is that fluent outputs and strong benchmark performance do not establish that an agent is dependable in its intended setting. The WHO guidance links responsible deployment with transparency, human oversight and continuing evaluation (WHO, 2021).

This connects with the recorded Group C discussions about our Academic Research Agent. My contribution moved from an Agile prototyping proposal towards an architecture-first approach after team feedback. We also simplified storage from SQLite to JSON and adopted a provider-agnostic model layer. These changes reinforced the value of revising design choices against requirements and peer criticism.

I would now extend that reasoning to evidence quality. A clear architecture should identify which component retrieves sources, which synthesises findings and where unsupported claims are stopped. Provider independence also creates an evaluation obligation: replacing a model should trigger renewed checks of citation accuracy and claim support.

My next step would be to propose an evidence record and a small, manually checked evaluation set to the team. This would translate ethical principles into observable design requirements while keeping human responsibility explicit throughout the research workflow and its eventual use.

## References

World Health Organization (WHO) (2021) *Ethics and governance of artificial intelligence for health: WHO guidance*. Geneva: WHO. Available from: https://www.who.int/publications/i/item/9789240029200 [Accessed 24 September 2026].

## Supporting portfolio evidence

[Group Project C Teams Discussion and Reflection](../Team-project/Group%20C%20-%20Project/submission-ready%20files/Group%20Project%20C%20Teams-discussion-and-Reflection.md).
