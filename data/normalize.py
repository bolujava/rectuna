import json

KEEP_FIELDS = {"vendor", "date", "invoice_number", "items", "total"}

def normalize_invoice(obj):
    return {k: v for k, v in obj.items() if k in KEEP_FIELDS}

def normalize_product(obj):
    # Product schema: name, brand, price, category, rating, in_stock, description, sku
    keep = {"name", "brand", "price", "category", "rating", "in_stock", "description", "sku"}
    return {k: v for k, v in obj.items() if k in keep}

def normalize_receipt(obj):
    # Receipt schema: store, date, items, total, payment_method
    keep = {"store", "date", "items", "total", "payment_method"}
    return {k: v for k, v in obj.items() if k in keep}

def normalize_contact(obj):
    # Contact schema: name, title, company, email, phone, address
    keep = {"name", "title", "company", "email", "phone", "address"}
    return {k: v for k, v in obj.items() if k in keep}

NORMALIZERS = {
    "invoice": normalize_invoice,
    "product": normalize_product,
    "receipt": normalize_receipt,
    "contact": normalize_contact,
}

with open("data/train.jsonl", encoding="utf-8") as f:
    lines = [json.loads(l) for l in f if l.strip()]

normalized = []
for line in lines:
    mode = line["messages"][0]["content"].split("Mode: ")[1].rstrip(".")
    try:
        obj = json.loads(line["messages"][2]["content"])
        obj = NORMALIZERS[mode](obj)
        line["messages"][2]["content"] = json.dumps(obj)
        normalized.append(line)
    except Exception as e:
        print(f"Skipping bad line: {e}")

with open("data/train.jsonl", "w", encoding="utf-8") as f:
    for line in normalized:
        f.write(json.dumps(line) + "\n")

print(f"Normalized {len(normalized)} examples")