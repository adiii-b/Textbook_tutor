# Training Approach — Finetuning Dataset

## Goal

The baseline analysis showed that qwen2.5:1.5b responds accurately but behaves poorly as a tutor. The finetuning goal is not to make the model more knowledgeable — it is to make it explain better. The dataset targets behaviour, not facts.

---

## What the Baseline Got Wrong

Four consistent problems from the baseline:

1. **Prompt adherence** — ignored the "3-4 bullet points" instruction, producing walls of text disguised as bullets
2. **Repetition** — redefined the same concept multiple times within one response
3. **Example generation** — rephrased retrieved context rather than generating concrete real-world examples
4. **Cut-offs** — hit the token limit mid-sentence instead of concluding within budget

Teaching quality was the weakest dimension overall (avg 3.1/5). The model stated facts correctly but rarely explained *why* something is true or connected concepts to student experience.

---

## Dataset Design

**498 question-answer pairs** stored as simple `{"question": "...", "answer": "..."}` JSON lines.

### Format

Each answer demonstrates exactly the behaviour we want:
- 3–4 bullet points, no more, no less
- Each bullet adds new information — no repetition across bullets
- At least one concrete real-world example per response
- Explains the *why*, not just the *what*
- Completes fully within a short token budget — no trailing off

### Topic spread

Deliberately broad — economics, biology, physics, history, psychology, mathematics, philosophy, technology, and more. The goal is to instil a teaching *style*, not domain knowledge, so variety matters more than depth in any single subject.

### Question variety

A deliberate mix of question types so the model learns to respond well regardless of how a student phrases something:

- Factual recall ("What is X?")
- Process questions ("How does X work?", "Walk me through...")
- Causal questions ("Why does X happen?")
- Comparison ("What's the difference between X and Y?")
- Example requests ("Give me an example of...")
- Confused student questions ("I don't understand why...", "Can you explain X in a way that makes sense?")
- Counterintuitive and edge case questions ("Why does X seem wrong but is actually right?", "Is it possible to...")

Early drafts were almost entirely "What is X?" questions. The variety was added because the model needs to recognise different phrasings as requests for the same kind of structured explanation.

---

## What We Are Not Trying to Do

- We are not teaching the model new facts — it already knows the content
- We are not training it on textbook-specific material — the retriever handles that
- We are not trying to make it answer every possible question — we are shaping how it answers

The finetuned model will still use BM25-retrieved context at inference time. The training teaches it what to do with that context: structure it clearly, explain it simply, ground it in examples, and finish cleanly.
