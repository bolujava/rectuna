import json

with open("data/train.jsonl", encoding="utf-8") as f:
    lines = [json.loads(l) for l in f if l.strip()]

print(f"total: {len(lines)}")

# Mode distribution
from collections import Counter
modes = Counter(l["messages"][0]["content"].split("Mode: ")[1].rstrip(".") for l in lines)
print(f"modes: {dict(modes)}")

# Structure check
bad_struct = [i for i, l in enumerate(lines, 1) if len(l["messages"]) != 3]
print(f"bad structure: {bad_struct if bad_struct else 'none'}")

# Assistant JSON validity
bad_json = []
for i, l in enumerate(lines, 1):
    try:
        json.loads(l["messages"][2]["content"])
    except Exception as e:
        bad_json.append((i, str(e)[:60]))
print(f"bad assistant JSON: {bad_json if bad_json else 'none'}")