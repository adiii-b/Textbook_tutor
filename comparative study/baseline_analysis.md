# Baseline Analysis — Untrained Model (qwen2.5:1.5b)

Model: qwen2.5:1.5b via Ollama
Retrieval: BM25, top_k=1, context truncated to 200 words
Date: April 2026

---

## Scoring Rubric

Each response is scored across four dimensions (1–5):
- **Accuracy** — does it match what the textbook says?
- **Clarity** — would a student understand it?
- **Teaching quality** — does it explain *why*, or just state facts?
- **Completeness** — does it cover the question fully without cutting off?

---

## Q1 — Factual Recall: "What is scarcity in economics?"

**Response summary:**
Three bullet points rendered, but the third is extremely long — the model repeated itself multiple times within a single bullet, defining scarcity 3-4 times with slight variations. It eventually started generating an example (food on Earth) but cut off mid-sentence.

| Dimension | Score | Notes |
|---|---|---|
| Accuracy | 4/5 | Definition is correct — wants exceed availability |
| Clarity | 2/5 | Third bullet is a wall of repeated text, hard to read |
| Teaching quality | 2/5 | States the definition, no explanation of *why* it matters |
| Completeness | 2/5 | Cuts off mid-sentence, loops back on itself |

**Key issue:** The model did not respect the bullet point structure. It generated one coherent point, then lost structure and repeated itself. This is a prompt adherence problem — the untrained model doesn't reliably follow the "3-4 bullet points" instruction.

---

## Q2 — Factual Recall: "What is the difference between microeconomics and macroeconomics?"

**Response summary:**
Five bullet points rendered. First two are clean and accurate. The third is very long and loses structure mid-way. Points four and five are clean again. Last bullet cuts off with "while macro".

| Dimension | Score | Notes |
|---|---|---|
| Accuracy | 4/5 | Both definitions are factually correct |
| Clarity | 3/5 | Good points sandwiching a bloated middle point |
| Teaching quality | 3/5 | Gives contrast between the two, which is appropriate |
| Completeness | 3/5 | Cuts off in the last bullet |

**Key issue:** Inconsistent bullet length — some points are one clean sentence, others run on for a paragraph. A tutor-trained model should produce uniformly sized, digestible points.

---

## Q3 — Explanation Quality: "Why do people have to make choices?"

**Response summary:**
Three clean, concise bullet points. No cut-offs, no repetition. This is the best response of the set.

| Dimension | Score | Notes |
|---|---|---|
| Accuracy | 4/5 | Correct — scarcity forces trade-offs |
| Clarity | 5/5 | Short, readable, well-structured |
| Teaching quality | 3/5 | States the what, but doesn't connect back to scarcity explicitly |
| Completeness | 5/5 | Fully answers the question |

**Key issue:** The answer explains *that* choices involve sacrifices, but doesn't explain the root cause — that scarcity is what makes choices necessary. A trained tutor would make that connection explicit.

---

## Q4 — Explanation Quality: "Explain opportunity cost in simple terms"

**Response summary:**
Three bullet points. First gives a correct definition. Second gives a relatable example (reading vs watching TV). Third connects it to economic efficiency.

| Dimension | Score | Notes |
|---|---|---|
| Accuracy | 5/5 | Textbook-accurate definition and application |
| Clarity | 5/5 | The TV example makes it very approachable |
| Teaching quality | 4/5 | Uses an analogy, which is good teaching practice |
| Completeness | 4/5 | Covers definition, example, and application |

**Key issue:** Minor — the third point shifts to production efficiency which feels slightly disconnected from the "simple terms" framing. A tutor would keep all three points at the same level of simplicity.

---

## Q5 — Example Generation: "Give me an example of scarcity in everyday life"

**Response summary:**
Three bullet points but none of them are concrete examples. Instead they are abstract principles — "Limited Resources", "Comparative Value", "Trade-offs". The third cuts off mid-sentence.

| Dimension | Score | Notes |
|---|---|---|
| Accuracy | 3/5 | Concepts are related to scarcity but don't answer the question |
| Clarity | 3/5 | Well-written but not what was asked |
| Teaching quality | 2/5 | Fails to ground the concept in a real-world scenario |
| Completeness | 2/5 | Cuts off, and never actually gives an example |

**Key issue:** This is a retrieval problem compounded by a model problem. BM25 likely returned a chunk about scarcity in general, and the model rephrased the chunk rather than generating an example. A tutor-trained model should recognise when to generate an example vs when to retrieve.

---

## Q6 — Example Generation: "What is an example of a trade-off?"

**Response summary:**
Three clean bullet points. Gives a concrete example (burger vs bus tickets). Explains the underlying principle across all three points.

| Dimension | Score | Notes |
|---|---|---|
| Accuracy | 5/5 | Correct definition and example |
| Clarity | 5/5 | Concrete, easy to follow |
| Teaching quality | 4/5 | Grounds the concept in a real decision |
| Completeness | 5/5 | No cut-offs, well-rounded |

**Key issue:** None significant. This is the second-best response in the set.

---

## Q7 — Multi-concept: "How are scarcity and choice related?"

**Response summary:**
Four bullet points. First sets up the relationship clearly. Second and third are clean. Fourth cuts off mid-sentence with "These".

| Dimension | Score | Notes |
|---|---|---|
| Accuracy | 5/5 | Correctly identifies that scarcity creates the need for choice |
| Clarity | 4/5 | Clear until the cut-off |
| Teaching quality | 4/5 | Good relational explanation, connects two concepts well |
| Completeness | 3/5 | Cuts off in the last point |

**Key issue:** Cut-off is caused by the `num_predict: 80` token limit being hit. This question requires more output than single-concept questions.

---

## Overall Baseline Summary

| Question | Accuracy | Clarity | Teaching | Completeness | Avg |
|---|---|---|---|---|---|
| Q1 — What is scarcity? | 4 | 2 | 2 | 2 | **2.5** |
| Q2 — Micro vs Macro | 4 | 3 | 3 | 3 | **3.25** |
| Q3 — Why make choices? | 4 | 5 | 3 | 5 | **4.25** |
| Q4 — Opportunity cost | 5 | 5 | 4 | 4 | **4.5** |
| Q5 — Example of scarcity | 3 | 3 | 2 | 2 | **2.5** |
| Q6 — Example of trade-off | 5 | 5 | 4 | 5 | **4.75** |
| Q7 — Scarcity and choice | 5 | 4 | 4 | 3 | **4.0** |
| **Overall** | **4.3** | **3.9** | **3.1** | **3.4** | **3.68** |

---

## Patterns to Address with Finetuning

1. **Prompt adherence** — the model frequently ignores the "3-4 bullet points" instruction and generates one long paragraph disguised as a bullet. A finetuned model should produce consistently structured, uniform-length points.

2. **Repetition** — Q1 showed the model redefining the same concept 3-4 times within one response. Training data should demonstrate that each point adds new information.

3. **Example generation** — Q5 showed the model cannot reliably generate concrete examples on demand. Training data should include question-answer pairs that explicitly demonstrate moving from concept to real-world example.

4. **Cut-offs** — 4 of 7 responses cut off mid-sentence. This is partly a `num_predict` limit issue, but a trained model should learn to conclude within the token budget rather than trail off.

5. **Teaching voice** — responses state facts accurately but rarely explain *why* something is true or connect concepts to student experience. The finetuned model should be trained on responses that use analogies, ask rhetorical questions, and build understanding progressively.

---

*This document serves as the baseline for comparison against the finetuned model.*
