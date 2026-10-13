import json
from collections import Counter

with open("data/train.jsonl", encoding="utf-8") as f:
    lines = [json.loads(l) for l in f if l.strip()]

for mode in ["invoice", "product", "receipt", "contact"]:
    examples = [l for l in lines if f"Mode: {mode}" in l["messages"][0]["content"]]
    print(f"\n=== {mode} ({len(examples)} examples) ===")

    keysets = Counter()
    for ex in examples:
        try:
            obj = json.loads(ex["messages"][2]["content"])
            keysets[tuple(sorted(obj.keys()))] += 1
        except Exception as e:
            print(f"  BAD JSON: {e}")

    for keys, count in keysets.most_common():
        print(f"  {count}x: {keys}")