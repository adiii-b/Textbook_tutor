import json

INPUT_PATH = "training_data.jsonl"
OUTPUT_PATH = "training_data_clean.jsonl"

def clean():
    good = []
    seen = set()
    skipped_bad = 0
    skipped_dupes = 0
    skipped_format = 0

    with open(INPUT_PATH, encoding="utf-8") as f:
        for i, line in enumerate(f, 1):
            line = line.strip()
            if not line:
                continue

            try:
                record = json.loads(line)
            except json.JSONDecodeError:
                skipped_bad += 1
                continue

            if "question" not in record or "answer" not in record:
                skipped_bad += 1
                continue

            q = record["question"].strip()
            a = record["answer"].strip()

            if not q or not a:
                skipped_bad += 1
                continue

            if not a.startswith("-"):
                skipped_format += 1
                continue

            key = (q, a)
            if key in seen:
                skipped_dupes += 1
                continue

            seen.add(key)
            good.append({"question": q, "answer": a})

    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        for record in good:
            f.write(json.dumps(record, ensure_ascii=False) + "\n")

    print(f"Clean samples written : {len(good)}")
    print(f"Skipped (bad JSON)    : {skipped_bad}")
    print(f"Skipped (format)      : {skipped_format}")
    print(f"Skipped (exact dupes) : {skipped_dupes}")
    print(f"Output: {OUTPUT_PATH}")

if __name__ == "__main__":
    clean()
