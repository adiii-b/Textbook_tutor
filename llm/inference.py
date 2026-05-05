import subprocess
from pathlib import Path

MODEL_PATH = Path(__file__).parent.parent / "models" / "lfm-tutor-q4.gguf"
LLAMA_CLI  = Path(__file__).parent.parent / "llama.cpp" / "build" / "bin" / "llama-cli"
N_THREADS  = 4
N_CTX      = 512


def _build_prompt(context: str, question: str) -> str:
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
    return f"<|im_start|>user\n{user_content}<|im_end|>\n<|im_start|>assistant\n"


def explain(context: str, question: str, history=None) -> str:
    return "".join(explain_stream(context, question, history))


def explain_stream(context: str, question: str, history=None):
    prompt = _build_prompt(context, question)
    cmd = [
        str(LLAMA_CLI),
        "-m", str(MODEL_PATH),
        "-t", str(N_THREADS),
        "-c", str(N_CTX),
        "-n", "512",
        "--temp", "0.3",
        "--top-p", "0.9",
        "--no-display-prompt",
        "-p", prompt,
    ]
    process = subprocess.Popen(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.DEVNULL,
        bufsize=0,
    )
    for chunk in iter(lambda: process.stdout.read(1), b""):
        yield chunk.decode("utf-8", errors="replace")
    process.wait()
