import json
import httpx

LLAMA_SERVER = "http://127.0.0.1:8080"


def _build_messages(context: str, question: str) -> list:
    if context.strip():
        user_content = (
            f"Context:\n{context}\n\n"
            f"Question:\n{question}\n\n"
            "Answer in 3 bullet points using only the context. "
            "If not covered, say so."
        )
    else:
        user_content = question
    return [{"role": "user", "content": user_content}]


def explain(context: str, question: str, history=None) -> str:
    return "".join(explain_stream(context, question, history))


def explain_stream(context: str, question: str, history=None):
    payload = {
        "messages": _build_messages(context, question),
        "max_tokens": 512,
        "temperature": 0.3,
        "top_p": 0.9,
        "stream": True,
    }
    with httpx.Client(timeout=None) as client:
        with client.stream("POST", f"{LLAMA_SERVER}/chat/completions", json=payload) as response:
            for line in response.iter_lines():
                if not line.startswith("data: "):
                    continue
                data = line[6:]
                if data == "[DONE]":
                    break
                try:
                    chunk = json.loads(data)
                    delta = chunk["choices"][0]["delta"]
                    if "content" in delta and delta["content"]:
                        yield delta["content"]
                except (json.JSONDecodeError, KeyError, IndexError):
                    continue
