from transformers import AutoModelForCausalLM, AutoTokenizer, Trainer, TrainingArguments
from datasets import load_dataset
import requests

# Set your model name and API key
model_name = "nvidia/llama-3.1-nemotron-70b-instruct"
API_KEY = "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"

# Load the tokenizer and model
try:
    tokenizer = AutoTokenizer.from_pretrained(model_name)
except KeyError:
    # If AutoTokenizer fails, attempt to load a general tokenizer
    tokenizer = AutoTokenizer.from_pretrained("nvidia/llama-3.1-nemotron-70b-instruct")

model = AutoModelForCausalLM.from_pretrained(model_name)

# Load your fine-tuning dataset
dataset = load_dataset("json", data_files={"train": "your_fine_tune_data.json"})

def generate_response_nvidia(context_text, question):
    url = "https://integrate.api.nvidia.com/v1"
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": model_name,
        "messages": [
            {"role": "user", "content": f"{context_text}\n{question}"}
        ],
        "temperature": 0.5,
        "max_tokens": 1024,
        "top_p": 1
    }
    
    response = requests.post(url, headers=headers, json=payload)
    
    if response.status_code == 200:
        return response.json().get('choices')[0].get('message').get('content')
    else:
        return "Error fetching response from NVIDIA API."

def fine_tune_model():
    def tokenize_function(examples):
        return tokenizer(examples["input"], padding="max_length", truncation=True, max_length=128)

    tokenized_dataset = dataset["train"].map(tokenize_function, batched=True)

    # Training arguments
    training_args = TrainingArguments(
        output_dir="./fine_tuned_model",
        evaluation_strategy="epoch",
        learning_rate=5e-5,
        per_device_train_batch_size=2,
        num_train_epochs=3,
        weight_decay=0.01,
    )

    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=tokenized_dataset,
    )

    # Start fine-tuning
    trainer.train()

    # Save the fine-tuned model
    trainer.save_model("fine_tuned_njit_bot")
    tokenizer.save_pretrained("fine_tuned_njit_bot")

if __name__ == "__main__":
    fine_tune_model()
