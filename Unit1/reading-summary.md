# Unit 1 Reading Summary

## Required Reading

**Wooldridge, M.J. (2009) *An Introduction to Multiagent Systems*. Chichester: John Wiley & Sons. — Chapter 2**

---

## Chapter 2 Summary: Intelligent Agents

### What is an Agent?

Wooldridge defines an agent as a computer system situated in some **environment** and capable of taking **autonomous action** in that environment in order to meet its design objectives. This distinguishes agents from conventional software programs, which passively wait for instructions. Crucially, agents must decide for themselves what actions to take to achieve their goals.

### Key Properties of Agents (PRAS)

Wooldridge identifies four core properties that define an intelligent agent:

| Property | Description |
|----------|-------------|
| **Proactiveness** | Agents do not simply react to events — they take initiative and pursue goals |
| **Reactivity** | Agents perceive their environment and respond to changes in a timely manner |
| **Autonomy** | Agents operate without direct human control, using their own reasoning |
| **Social ability** | Agents interact with other agents (and humans) via agent communication languages |

These four properties are sometimes referred to as the **"weak notion"** of agency.

### Agents and Environments

An agent is always embedded within an environment. Wooldridge characterises environments along five dimensions:

- **Accessible vs. Inaccessible** — Can the agent sense the complete state of the environment?
- **Deterministic vs. Non-deterministic** — Do actions have guaranteed, predictable outcomes?
- **Episodic vs. Non-episodic** — Is agent performance dependent on past interactions?
- **Static vs. Dynamic** — Does the environment change while the agent deliberates?
- **Discrete vs. Continuous** — Is the number of possible states and actions finite?

Most real-world environments are inaccessible, non-deterministic, non-episodic, dynamic, and continuous — making agent design a significant challenge.

### Abstract Agent Architecture

Wooldridge introduces a simple abstract model: an agent maps **perceptions** (inputs from the environment) to **actions** (outputs back to the environment) via an internal decision function. This function encapsulates the agent's reasoning and determines its behaviour.

### Agent Types

The chapter distinguishes between progressively sophisticated agent architectures:

1. **Purely reactive agents** — Select actions based solely on the current percept; no internal state or memory.
2. **Agents with state** — Maintain an internal model of the world to inform decision-making.
3. **Goal-based agents** — Act to achieve explicitly represented goals.
4. **Utility-based agents** — Choose actions that maximise a utility function, enabling trade-offs between competing goals.

### Relevance to Multi-Agent Systems

Chapter 2 establishes the foundational vocabulary for the rest of the book. Understanding what constitutes an agent — and what types of environments they operate in — is essential before examining how *multiple* agents interact, cooperate, and compete in a shared environment.

---

## Key Takeaway

> An intelligent agent is not merely a program that responds to inputs. It is an autonomous, goal-directed system capable of perceiving its environment, deliberating, and acting — independently and in coordination with others — to achieve its objectives.

---

*Reference: Wooldridge, M.J. (2009) An Introduction to Multiagent Systems. 2nd edn. Chichester: John Wiley & Sons.*
