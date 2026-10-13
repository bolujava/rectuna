import json
import random
from pathlib import Path

random.seed(42)

OUT = Path("data/train.jsonl")


# ---------- INVOICE ----------
VENDORS = ["Acme Corp", "Global Supplies Ltd.", "TechParts Inc", "Nordic Systems", "Zenith Trading Co.", "Eastwood Logistics", "BluePeak Industries", "Orion Components"]
ITEMS = ["Widget", "Gizmo", "USB-C Cable", "Monitor Stand", "Printer Paper", "Ink Cartridge", "HDMI Adapter", "Wireless Mouse", "Keyboard", "Webcam", "Desk Lamp", "Notebook", "Pen Pack", "Stapler", "Toner"]
DATES = ["2024-01-15", "2024-02-03", "2024-03-22", "2024-04-05", "2024-05-10", "2024-06-18", "2024-07-25", "2024-08-11"]


def gen_invoice():
    vendor = random.choice(VENDORS)
    date = random.choice(DATES)
    n = random.randint(1, 4)

    items = []
    total = 0.0
    item_lines = []
    for _ in range(n):
        name = random.choice(ITEMS)
        qty = random.randint(1, 10)
        price = round(random.uniform(5, 300), 2)
        items.append({"name": name, "qty": qty, "price": price})
        total += qty * price
        item_lines.append(f"- {qty}x {name} @ ${price}")
    total = round(total, 2)

    variant = random.choice(["full", "no_tax", "no_header", "inline", "no_subtotal"])

    if variant == "full":
        tax = round(total * 0.10, 2)
        grand = round(total + tax, 2)
        user = (
            f"Invoice #{random.randint(1000, 9999)}\n"
            f"Vendor: {vendor}\nDate: {date}\n\nItems:\n"
            + "\n".join(item_lines)
            + f"\n\nSubtotal: ${total}\nTax: ${tax}\nTotal: ${grand}"
        )
        assistant = json.dumps({"vendor": vendor, "date": date, "items": items, "subtotal": total, "tax": tax, "total": grand})

    elif variant == "no_tax":
        user = (
            f"Invoice #{random.randint(1000, 9999)}\n"
            f"Vendor: {vendor}\nDate: {date}\n\nItems:\n"
            + "\n".join(item_lines)
            + f"\n\nTotal: ${total}"
        )
        assistant = json.dumps({"vendor": vendor, "date": date, "items": items, "total": total})

    elif variant == "no_header":
        user = (
            f"From: {vendor}\nDated {date}\n\n"
            + "\n".join(item_lines)
            + f"\n\nAmount Due: ${total}"
        )
        assistant = json.dumps({"vendor": vendor, "date": date, "items": items, "total": total})

    elif variant == "inline":
        items_inline = ", ".join(f"{i['qty']}x {i['name']} at ${i['price']} each" for i in items)
        user = f"{vendor} billed us on {date} for {items_inline}. Grand total: ${total}."
        assistant = json.dumps({"vendor": vendor, "date": date, "items": items, "total": total})

    else:  # no_subtotal
        tax = round(total * 0.10, 2)
        grand = round(total + tax, 2)
        user = (
            f"Invoice #{random.randint(1000, 9999)}\n"
            f"Vendor: {vendor}\nDate: {date}\n\n"
            + "\n".join(item_lines)
            + f"\n\nTax: ${tax}\nTotal Due: ${grand}"
        )
        assistant = json.dumps({"vendor": vendor, "date": date, "items": items, "tax": tax, "total": grand})

    return {"messages": [
        {"role": "system", "content": "Extract structured data as JSON. Mode: invoice."},
        {"role": "user", "content": user},
        {"role": "assistant", "content": assistant},
    ]}


# ---------- PRODUCT ----------
BRANDS = ["Apple", "Logitech", "Samsung", "Sony", "Anker", "Dell", "HP", "Bose", "JBL", "Xiaomi"]
CATEGORIES = ["Electronics", "Computer Accessories", "Audio", "Home Office", "Mobile Accessories", "Kitchen", "Sports"]
PRODUCTS = ["iPad Air", "Wireless Mouse", "Bluetooth Speaker", "Phone Case", "Laptop Stand", "USB Hub", "Earbuds", "Webcam", "Monitor", "Keyboard", "Backpack", "Water Bottle", "Desk Pad", "Charger", "Cable Organizer"]


def gen_product():
    name = random.choice(PRODUCTS)
    brand = random.choice(BRANDS)
    price = round(random.uniform(10, 1500), 2)
    category = random.choice(CATEGORIES)
    rating = round(random.uniform(3.0, 5.0), 1)
    user = f"Product: {name}\nBrand: {brand}\nPrice: ${price}\nCategory: {category}\nRating: {rating} stars"
    assistant = json.dumps({"name": name, "brand": brand, "price": price, "category": category, "rating": rating})
    return {"messages": [
        {"role": "system", "content": "Extract structured data as JSON. Mode: product."},
        {"role": "user", "content": user},
        {"role": "assistant", "content": assistant},
    ]}


# ---------- RECEIPT ----------
STORES = ["Walmart Supercenter", "Starbucks #4521", "Target", "Whole Foods Market", "CVS Pharmacy", "Shell Gas Station", "McDonald's", "Kroger", "Costco", "Trader Joe's"]
RECEIPT_ITEMS = ["Milk 2%", "Bread Wheat", "Eggs Dozen", "Bananas 1lb", "Latte Grande", "Croissant", "Coffee", "Sandwich", "Apple Juice", "Chicken Breast", "Rice 5lb", "Cereal", "Yogurt", "Cheese", "Chips"]


def gen_receipt():
    store = random.choice(STORES)
    date = random.choice(DATES)
    n = random.randint(1, 5)
    items = []
    total = 0.0
    lines = []
    for _ in range(n):
        name = random.choice(RECEIPT_ITEMS)
        price = round(random.uniform(0.5, 30), 2)
        items.append({"name": name, "price": price})
        total += price
        lines.append(f"{name:20s} ${price}")
    total = round(total, 2)
    user = f"{store}\n{date}\n\n" + "\n".join(lines) + f"\n\nTOTAL: ${total}\nVISA ****{random.randint(1000, 9999)}"
    assistant = json.dumps({"store": store, "date": date, "items": items, "total": total})
    return {"messages": [
        {"role": "system", "content": "Extract structured data as JSON. Mode: receipt."},
        {"role": "user", "content": user},
        {"role": "assistant", "content": assistant},
    ]}


# ---------- CONTACT ----------
NAMES = ["John Smith", "Amara Okonkwo", "Maria Garcia", "Chen Wei", "Priya Sharma", "Ahmed Hassan", "Sarah Johnson", "Kwame Mensah", "Elena Petrov", "Yuki Tanaka"]
TITLES = ["Senior Product Manager", "Head of Research", "CTO", "Marketing Director", "Software Engineer", "Data Scientist", "Sales Lead", "Operations Manager", "Founder & CEO", "Consultant"]
COMPANIES = ["TechCorp Inc.", "BioGen Labs", "Nova Systems", "Bright Future LLC", "DataWorks", "Green Energy Co.", "MedPlus", "FinEdge", "CloudBase", "StartupHub"]
CITIES = ["San Francisco, CA", "Lagos, Nigeria", "Berlin, Germany", "Singapore", "London, UK", "Toronto, Canada", "Nairobi, Kenya", "Tokyo, Japan", "Sydney, Australia", "Accra, Ghana"]


def gen_contact():
    name = random.choice(NAMES)
    title = random.choice(TITLES)
    company = random.choice(COMPANIES)
    email = name.lower().replace(" ", ".").replace("&", "") + "@" + company.lower().replace(" ", "").replace(".", "").replace(",", "")[:12] + ".com"
    phone = f"+{random.randint(1, 99)} {random.randint(100, 999)} {random.randint(100, 999)} {random.randint(1000, 9999)}"
    city = random.choice(CITIES)
    user = f"{name}\n{title}\n{company}\n{email}\n{phone}\n{city}"
    assistant = json.dumps({"name": name, "title": title, "company": company, "email": email, "phone": phone, "address": city})
    return {"messages": [
        {"role": "system", "content": "Extract structured data as JSON. Mode: contact."},
        {"role": "user", "content": user},
        {"role": "assistant", "content": assistant},
    ]}


# ---------- MAIN ----------
GENERATORS = {
    "invoice": gen_invoice,
    "product": gen_product,
    "receipt": gen_receipt,
    "contact": gen_contact,
}

N_PER_MODE = 88

new = []
for mode, gen in GENERATORS.items():
    for _ in range(N_PER_MODE):
        new.append(gen())

with open(OUT, "a", encoding="utf-8") as f:
    for line in new:
        f.write(json.dumps(line) + "\n")

print(f"Appended {len(new)} examples ({N_PER_MODE} per mode)")