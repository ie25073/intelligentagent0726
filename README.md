# Intelligent Agents - July 2026

**Module 5 | MSc Computer Science | University of Essex Online**

This repository is Imoh Etuk's completed learning e-portfolio for Module 5, Intelligent Agents. The public portfolio is available at [ie25073.github.io](https://ie25073.github.io/).

## Assessed Deliverables

- [Unit 11 presentation source](Unit11/Development%20Project-Individual%20Project%20Presentation/Academic-Research-Agent-Presentation.md) and generated PowerPoint.
- [Unit 11 narration transcript](Unit11/Development%20Project-Individual%20Project%20Presentation/Academic-Research-Agent-Transcript.md).
- [Academic Research Agent](Unit11/Development%20Project-Individual%20Project%20Presentation/academic-research-agent/) with source, tests, README and execution evidence.
- [Unit 12 individual e-portfolio submission](Unit12/Final-Assignment/Individual-e-Portfolio-Submission/ie25073_Intelligent_Agents.md) and generated Word document.

## Learning Activities

| Units | Evidence |
|---|---|
| 1-3 | Collaborative Discussion 1: initial post, peer responses and [summary](Unit1/Collaborative%20Discussion-1-Agent-Based-Systems/Summary-Post.md) |
| 5-7 | Collaborative Discussion 2, [required reading summary](Unit5/Reading-list/Unit_5_Required_Reading_Summary.md) and [KQML/KIF dialogue](Unit6/agent-dialogues/) |
| 8 | [Constituency parse trees](Unit8/e-Portfolio-Element/constituency-parse-trees.md) with two ambiguity readings |
| 9-11 | Collaborative Discussion 3, ethical additional task and [reflection](Unit9/e-portfolio-reflection.md) |
| 10 | [Deep-learning application and societal impact](Unit10/e-Portfolio-Element-task/deep-learning-application.md) |
| Team project | Group C design files, peer evaluation and individual contribution reflection |

## Final Project

The Academic Research Agent is a standard-library Python workflow with four explicit roles: planning, retrieval, processing and storage. It supports optional Ollama planning, live OpenAlex retrieval and a deterministic offline demonstration. Outputs retain source provenance and the workflow stops after a maximum of three retrieval cycles.

Run the reproducible demonstration:

```bash
cd "Unit11/Development Project-Individual Project Presentation/academic-research-agent"
python3 -m research_agent \
	"Explainable decisions in autonomous research agents" \
	--offline \
	--output evidence/offline-demo
```

Run the tests:

```bash
python3 -m unittest discover -s tests -v
```

## Module Learning Outcomes

1. Identify and critically analyse agent-based systems, differentiating between architectures and approaches.
2. Apply and critically evaluate intelligent-agent techniques to real-world problems involving risk and uncertainty.
3. Use appropriate software tools while considering legal, social, ethical and professional issues.
4. Work effectively in a virtual development team with real-world roles and responsibilities.

---

University of Essex Online | ie25073@essex.ac.uk
