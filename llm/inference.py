from llama_cpp import Llama

MODEL_PATH = "models/lfm-tutor-q4.gguf"
N_THREADS  = 4
N_CTX      = 512

_llm = None


def _get_model() -> Llama:
    global _llm
    if _llm is None:
        _llm = Llama(model_path=MODEL_PATH, n_ctx=N_CTX, n_threads=N_THREADS, chat_format=None, verbose=False)
    return _llm


def _build_messages(context: str, question: str) -> list:
    if context.strip():
        user_content = (
            f"Context:\n{context}\n\n"
            f"Question:\n{question}\n\n"
            "Answer clearly in bullet points. For each point explain the why, "
            "and include real-world examples where they help. "
            "Answer only using the context provided — if the topic is not covered "
            "in the context, say \"That topic isn't covered in the loaded material.\""
        )
    else:
        user_content = question
    return [{"role": "user", "content": user_content}]


def explain(context: str, question: str, history=None) -> str:
    llm = _get_model()
    result = llm.create_chat_completion(
        messages=_build_messages(context, question),
        max_tokens=350,
        temperature=0.3,
        top_p=0.9,
    )
    return result["choices"][0]["message"]["content"].strip()


def explain_stream(context: str, question: str, history=None):
    llm = _get_model()
    stream = llm.create_chat_completion(
        messages=_build_messages(context, question),
        max_tokens=512,
        temperature=0.3,
        top_p=0.9,
        stream=True,
    )
    for chunk in stream:
        delta = chunk["choices"][0]["delta"]
        if "content" in delta:
            yield delta["content"]
