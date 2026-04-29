import json

DATA_PATH = "training_data.jsonl"

def validate():
    good = []
    bad_lines = []

    with open(DATA_PATH, encoding="utf-8") as f:
        for i, line in enumerate(f, 1):
            line = line.strip()
            if not line:
                continue
            try:
                record = json.loads(line)
            except json.JSONDecodeError as e:
                bad_lines.append((i, str(e)))
                continue

            if "question" not in record or "answer" not in record:
                bad_lines.append((i, f"missing keys: {list(record.keys())}"))
                continue

            q = record["question"].strip()
            a = record["answer"].strip()

            if not q:
                bad_lines.append((i, "empty question"))
                continue
            if not a:
                bad_lines.append((i, "empty answer"))
                continue
            if not a.startswith("-"):
                bad_lines.append((i, f"answer does not start with '-': {a[:60]}"))
                continue

            good.append(record)

    print(f"Total valid samples : {len(good)}")
    print(f"Total bad lines     : {len(bad_lines)}")

    if bad_lines:
        print("\nBad lines:")
        for lineno, reason in bad_lines:
            print(f"  Line {lineno}: {reason}")

    dupes = len(good) - len({r["question"] for r in good})
    if dupes:
        print(f"\nDuplicate questions : {dupes}")
    else:
        print("No duplicate questions found.")

if __name__ == "__main__":
    validate()
