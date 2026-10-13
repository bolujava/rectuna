import gradio as gr
import os
import json
from unsloth import FastLanguageModel
from peft import PeftModel

# Load model once when Space starts
print("Loading base model...")
base, tokenizer = FastLanguageModel.from_pretrained(
    model_name="unsloth/Qwen2.5-1.5B-Instruct-bnb-4bit",
    max_seq_length=2048,
    load_in_4bit=True,
)

print("Loading adapter...")
model = PeftModel.from_pretrained(base, "heydothan/rectuna-qwen2.5-1.5b")
FastLanguageModel.for_inference(model)
print("Ready.")


def extract(mode, text):
    """Extract structured data from text using the fine-tuned model."""
    messages = [
        {"role": "system", "content": f"Extract structured data as JSON. Mode: {mode}."},
        {"role": "user", "content": text},
    ]
    inputs = tokenizer.apply_chat_template(
        messages, tokenize=True, add_generation_prompt=True, return_tensors="pt"
    ).to("cuda" if os.getenv("SPACE_ID") else "cpu")

    out = model.generate(
        input_ids=inputs, max_new_tokens=256, temperature=0.1, do_sample=False
    )
    raw = tokenizer.decode(out[0][inputs.shape[1]:], skip_special_tokens=True)

    # Try to validate as JSON
    try:
        parsed = json.loads(raw.strip())
        return json.dumps(parsed, indent=2)
    except Exception:
        return raw


demo = gr.Interface(
    fn=extract,
    inputs=[
        gr.Dropdown(choices=["invoice", "product", "receipt", "contact"], value="invoice", label="Mode"),
        gr.Textbox(lines=10, label="Input Text",
                   placeholder="Paste your invoice, product listing, receipt, or contact info here..."),
    ],
    outputs=gr.Code(language="json", label="Extracted JSON"),
    title="Rectuna — JSON Extractor",
    description="Fine-tuned Qwen2.5-1.5B for structured JSON extraction across four schemas.",
)

demo.launch()