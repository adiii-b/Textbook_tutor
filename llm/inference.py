"""
Runs inference using the loaded model.
Keeps context small and output short for low-resource performance.
"""
import ollama


PROMPT_TEMPLATE = """Context:
{context}

Question:
{question}

Task:
Answer clearly in bullet points, using as many as the concept requires. For each point explain the why, and include real-world examples where they help understanding. Answer only using the context provided — if the topic is not covered in the context, say "That topic isn't covered in the loaded material.\""""


def build_prompt(context: str, question: str) -> str:
    return PROMPT_TEMPLATE.format(context=context, question=question)


def explain(context, question, history=None):
    prompt = build_prompt(context, question)
    try:
        response = ollama.generate(
            model="smollm2-tutor",
            prompt=prompt,
            options={
                "temperature": 0.3,
                "top_p": 0.9,
                "num_predict": 350,
            }
        )
        return response["response"].strip()
    except Exception as e:
        raise ConnectionError("Ollama is not running. Start it with 'ollama serve'.") from e


def explain_stream(context: str, question: str, history=None):
    try:
        stream = ollama.chat(
            model="smollm2-tutor",
            messages=[{"role": "user", "content": build_prompt(context, question)}],
            stream=True,
            options={"temperature": 0.3, "top_p": 0.9, "num_predict": 512}
        )
        for chunk in stream:
            yield chunk["message"]["content"]
    except Exception as e:
        raise ConnectionError("Ollama is not running. Start it with 'ollama serve'.") from e
