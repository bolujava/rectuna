---
title: Rectuna JSON Extractor
emoji: 📄
colorFrom: blue
colorTo: purple
sdk: gradio
sdk_version: 5.0.0
app_file: app.py
pinned: false
---

# Rectuna — JSON Extractor

Fine-tuned Qwen2.5-1.5B for structured JSON extraction.

GPT-4 can perform this task.
This project explores when fine-tuning a small model is the better engineering choice:
when cost per query, data privacy, or output consistency matters more than general capability.
Fine-tuning a 1.5B model on 383 examples produced 100% schema match and 0% cost per query — compared to GPT-4's per-query
API cost and third-party data dependency.
