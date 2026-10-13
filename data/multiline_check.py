import json

lines = open("data/train.jsonl", encoding="utf-8").read().splitlines()
print(f"total lines: {len(lines)}")

bad = []
for i, line in enumerate(lines, 1):
    if not line.strip():
        continue
    try:
        json.loads(line)
    except Exception as e:
        bad.append((i, len(line), str(e)[:80]))

print(f"bad lines: {bad if bad else 'none'}")