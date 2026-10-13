import json
import time
from pathlib import Path


from unsloth import FastLanguageModel
from peft import PeftModel

# --- Load both models ---
print("Loading base model...")
base, tokenizer = FastLanguageModel.from_pretrained(
    model_name="unsloth/Qwen2.5-1.5B-Instruct-bnb-4bit",
    max_seq_length=2048,
    load_in_4bit=True,
)
FastLanguageModel.for_inference(base)

print("Loading fine-tuned model...")
finetuned, _ = FastLanguageModel.from_pretrained(
    model_name="unsloth/Qwen2.5-1.5B-Instruct-bnb-4bit",
    max_seq_length=2048,
    load_in_4bit=True,
)
finetuned = PeftModel.from_pretrained(finetuned, "heydothan/rectuna-qwen2.5-1.5b")
FastLanguageModel.for_inference(finetuned)

# --- Load test cases ---
with open("test_cases.jsonl", encoding="utf-8") as f:
    cases = [json.loads(l) for l in f if l.strip()]

print(f"Loaded {len(cases)} test cases")


def run_model(model, mode, input_text):
    messages = [
        {"role": "system", "content": f"Extract structured data as JSON. Mode: {mode}."},
        {"role": "user", "content": input_text},
    ]
    inputs = tokenizer.apply_chat_template(messages, tokenize=True, add_generation_prompt=True, return_tensors="pt").to("cuda")
    out = model.generate(input_ids=inputs, max_new_tokens=256, temperature=0.1, do_sample=False)
    return tokenizer.decode(out[0][inputs.shape[1]:], skip_special_tokens=True)


def evaluate(model, cases):
    results = []
    for i, case in enumerate(cases, 1):
        raw = run_model(model, case["mode"], case["input"])

        # Try to parse JSON
        try:
            got = json.loads(raw.strip())
            valid = True
        except Exception:
            got = None
            valid = False

        # Schema match: all expected keys present
        schema_ok = False
        if valid:
            schema_ok = set(got.keys()) == set(case["expected"].keys())

        # Exact match: identical to expected
        exact = False
        if valid:
            exact = got == case["expected"]

        results.append({
            "mode": case["mode"],
            "valid_json": valid,
            "schema_match": schema_ok,
            "exact_match": exact,
            "raw_output": raw.strip()[:200],
        })
        print(f"[{i:2}/{len(cases)}] {case['mode']:8s} | valid={valid} | schema={schema_ok} | exact={exact}")

    return results


print("\n=== BASE MODEL ===")
base_results = evaluate(base, cases)

print("\n=== FINE-TUNED MODEL ===")
ft_results = evaluate(finetuned, cases)

# --- Summary ---
def summary(results, name):
    n = len(results)
    valid = sum(1 for r in results if r["valid_json"])
    schema = sum(1 for r in results if r["schema_match"])
    exact = sum(1 for r in results if r["exact_match"])
    print(f"\n{name}:")
    print(f"  JSON validity:  {valid}/{n} = {valid/n*100:.1f}%")
    print(f"  Schema match:   {schema}/{n} = {schema/n*100:.1f}%")
    print(f"  Exact match:    {exact}/{n} = {exact/n*100:.1f}%")

summary(base_results, "Base model")
summary(ft_results, "Fine-tuned model")

# Save
with open("eval_results.json", "w", encoding="utf-8") as f:
    json.dump({
        "base": base_results,
        "finetuned": ft_results,
    }, f, indent=2)
print("\nSaved eval_results.json")