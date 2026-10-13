I fine-tuned Qwen2.5-1.5B on 383 examples to extract structured JSON across four schemas — invoices, products, receipts, and contacts.
The adapter is on HuggingFace.
The base Qwen2.5-1.5B produced no valid JSON on any of the 20 test cases.
This is expected — the base model has no knowledge of the four extraction schemas.
The fine-tuned model scored 100% on all three metrics
Base model:
  JSON validity:  0/20 = 0.0%
  Schema match:   0/20 = 0.0%
  Exact match:    0/20 = 0.0%

Fine-tuned model:
  JSON validity:  20/20 = 100.0%
  Schema match:   20/20 = 100.0%
  Exact match:    20/20 = 100.0%