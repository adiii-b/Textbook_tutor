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
Explain this simply in 3-4 bullet points."""

def build_prompt(context: str, question: str) -> str:
    return PROMPT_TEMPLATE.format(context=context, question=question)


def explain(context, question):
    prompt = build_prompt(context, question)
    try:
        response = ollama.generate(
            model="qwen2.5:1.5b",
            prompt=prompt,
            options={
                "temperature": 0.4,
                "top_p": 0.9,
                "num_predict": 80,
                "stop": ["Question:", "Context:"]
            }
        )
        return response["response"].strip()
    except Exception as e:
        raise ConnectionError("Ollama is not running. Start it with 'ollama serve'.") from e


def explain_stream(context: str, question: str):
    prompt = build_prompt(context, question)
    try:
        stream = ollama.generate(
            model="qwen2.5:1.5b",
            prompt=prompt,
            stream=True,
            options={
                "temperature": 0.4,
                "top_p": 0.9,
                "num_predict": 80,
                "stop": ["Question:", "Context:"]
            }
        )
        for chunk in stream:
            yield chunk["response"]
    except Exception as e:
        raise ConnectionError("Ollama is not running. Start it with 'ollama serve'.") from e
