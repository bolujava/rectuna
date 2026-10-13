import requests

tests = [
    ("product", "Product: Sony Headphones\nBrand: Sony\nPrice: $299.99\nCategory: Audio\nRating: 4.8 stars"),
    ("receipt", "Target\n2024-06-15\n\nBread $3.50\nMilk $4.20\n\nTOTAL: $7.70"),
    ("contact", "Jane Doe\nCTO\nStartup Inc.\njane@startup.com\n+1 555 1234\nAustin, TX"),
    ("invoice", "Vendor: TestCo\nDate: 2024-06-01\n\n- 2x Notebook @ $5.00\n\nTotal: $10.00"),
]

for mode, text in tests:
    print(f"\n=== {mode} ===")
    r = requests.post("http://localhost:8000/api/extract", data={"mode": mode, "text": text})
    print(r.json())