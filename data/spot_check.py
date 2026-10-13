import json

with open("data/train.jsonl", encoding="utf-8") as f:
    lines = [json.loads(l) for l in f if l.strip()]

invoices = [l for l in lines if "Mode: invoice" in l["messages"][0]["content"]]

print(f"Total invoices: {len(invoices)}\n")

for i, inv in enumerate(invoices[10:15], 1):
    print(f"--- Invoice {i} ---")
    print(inv["messages"][1]["content"][:300])
    print()