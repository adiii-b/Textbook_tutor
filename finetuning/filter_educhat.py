import re
from datasets import load_dataset
import json

def load_educhat():
    ds = load_dataset("ecnu-icalk/educhat-sft-002-data-osm", split="train")
    examples = []
    for i, entry in enumerate(ds):
        if i>10000:
            break
        if len(entry["data"]) < 2:
            continue
        examples.append({
            "question": entry["data"][0],
            "answer": entry["data"][1]
        })
    return examples



def is_english(text):
    chinese_chars = sum(1 for c in text if '\u4e00' <= c <= '\u9fff')
    return chinese_chars / max(len(text.split()), 1) < 0.1

def length_check(text):
    return 40 <= len(text.split()) <= 250

def no_repetitions(text):
    sentences = [s.strip() for s in re.split(r'[.!?]', text) if s.strip()]
    for i in range(len(sentences)):
        for j in range(i + 1, len(sentences)):
            a = set(sentences[i].lower().split())
            b = set(sentences[j].lower().split())
            if len(a) > 3 and len(b) > 3:
                overlap = len(a & b) / len(a | b)
                if overlap > 0.6:
                    return False
    return True

def ends_correctly(text):
    return text.strip().endswith(('.', '!', '?', '。', '！', '？'))

def has_explanation(text):
    keywords = [
        'because', 'therefore', 'this means', 'the reason',
        'for example', 'for instance', 'such as',
        'think of it', 'imagine', 'in other words', 'which is why',
        'this is why', 'as a result', 'this happens',
        'the key', 'essentially', 'in practice', 'what this means'
    ]
    return any(keyword in text.lower() for keyword in keywords)

def passes_filter(example):
    answer = example["answer"]
    return (
        is_english(answer) and
        length_check(answer) and
        no_repetitions(answer) and
        ends_correctly(answer)
        # and has_explanation(answer)
    )

def main():
    print("Loading dataset...")
    examples = load_educhat()
    print(f"Loaded {len(examples)} examples")

    counts = {"is_english": 0, "length_check": 0, "no_repetitions": 0, "ends_correctly": 0, "has_explanation": 0}
    for ex in examples:
        a = ex["answer"]
        if is_english(a): counts["is_english"] += 1
        if length_check(a): counts["length_check"] += 1
        if no_repetitions(a): counts["no_repetitions"] += 1
        if ends_correctly(a): counts["ends_correctly"] += 1
        if has_explanation(a): counts["has_explanation"] += 1
    print(counts)

    filtered = [ex for ex in examples if passes_filter(ex)]
    print(f"Passed filter: {len(filtered)}")

    output_path = "finetuning/filtered_educhat.jsonl"
    with open(output_path, "w", encoding="utf-8") as f:
        for ex in filtered:
            f.write(json.dumps(ex) + "\n")

    print(f"Saved to {output_path}")

if __name__ == "__main__":
    main()