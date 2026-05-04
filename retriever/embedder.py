import numpy as np
from pathlib import Path
from tokenizers import Tokenizer
import onnxruntime as ort
from huggingface_hub import hf_hub_download

MODEL_REPO = "sentence-transformers/all-MiniLM-L6-v2"
MODEL_DIR = Path(__file__).parent.parent / "models" / "minilm-onnx"

_session = None
_tokenizer = None


def _load():
    global _session, _tokenizer
    if _session is not None:
        return

    onnx_path = MODEL_DIR / "onnx" / "model.onnx"
    if not onnx_path.exists():
        MODEL_DIR.mkdir(parents=True, exist_ok=True)
        print("Downloading ONNX embedding model (first run only)...")
        hf_hub_download(
            repo_id=MODEL_REPO,
            filename="onnx/model.onnx",
            local_dir=str(MODEL_DIR),
            local_dir_use_symlinks=False,
        )

    _session = ort.InferenceSession(str(onnx_path))
    _tokenizer = Tokenizer.from_pretrained(MODEL_REPO)
    _tokenizer.enable_padding(pad_id=0, pad_token="[PAD]", length=128)
    _tokenizer.enable_truncation(max_length=128)


def encode(texts) -> np.ndarray:
    _load()
    if isinstance(texts, str):
        texts = [texts]

    encoded = _tokenizer.encode_batch(texts)
    input_ids = np.array([e.ids for e in encoded], dtype=np.int64)
    attention_mask = np.array([e.attention_mask for e in encoded], dtype=np.int64)
    token_type_ids = np.zeros_like(input_ids, dtype=np.int64)

    outputs = _session.run(None, {
        "input_ids": input_ids,
        "attention_mask": attention_mask,
        "token_type_ids": token_type_ids,
    })

    token_embeddings = outputs[0]
    mask = attention_mask[:, :, np.newaxis].astype(np.float32)
    pooled = (token_embeddings * mask).sum(axis=1) / mask.sum(axis=1).clip(min=1e-9)
    norms = np.linalg.norm(pooled, axis=1, keepdims=True)
    return pooled / np.maximum(norms, 1e-9)


def encode_corpus(texts, batch_size=32) -> np.ndarray:
    all_embeddings = []
    for i in range(0, len(texts), batch_size):
        all_embeddings.append(encode(texts[i:i + batch_size]))
    return np.vstack(all_embeddings)
