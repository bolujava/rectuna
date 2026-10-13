import json

CANONICAL = {
    "invoice": {"vendor", "date", "items", "total"},
    "product": {"name", "brand", "price", "category", "rating"},
    "receipt": {"store", "date", "items", "total"},
    "contact": {"name", "title", "company", "email", "phone", "address"},
}

# Optional fields — allowed but not required
OPTIONAL = {
    "invoice": {"invoice_number", "customer", "due_date"},
    "product": {"description", "in_stock", "sku"},
    "receipt": {"payment_method", "subtotal", "tax"},
    "contact": set(),
}

with open("data/train.jsonl", encoding="utf-8") as f:
    lines = [json.loads(l) for l in f if l.strip()]

kept = []
dropped = []

for line in lines:
    mode = line["messages"][0]["content"].split("Mode: ")[1].rstrip(".")
    try:
        obj = json.loads(line["messages"][2]["content"])
    except Exception:
        dropped.append((mode, "invalid json"))
        continue

    required = CANONICAL[mode]
    optional = OPTIONAL[mode]
    keys = set(obj.keys())

    # Must have all required fields
    if not required.issubset(keys):
        dropped.append((mode, f"missing {required - keys}"))
        continue

    # Must not have unknown fields
    extra = keys - required - optional
    if extra:
        dropped.append((mode, f"unknown {extra}"))
        continue

    # Strip optional fields to keep schema tight
    clean = {k: v for k, v in obj.items() if k in required}
    line["messages"][2]["content"] = json.dumps(clean)
    kept.append(line)

with open("data/train.jsonl", "w", encoding="utf-8") as f:
    for line in kept:
        f.write(json.dumps(line) + "\n")

print(f"Kept: {len(kept)}, Dropped: {len(dropped)}")
from collections import Counter
print(Counter(d[1][:40] for d in dropped).most_common(5))