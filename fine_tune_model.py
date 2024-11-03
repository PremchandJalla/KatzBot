import json
from datasets import Dataset
from transformers import AutoModelForCausalLM, AutoTokenizer, Trainer, TrainingArguments

# Load the model and tokenizer
model_name = "gpt2"  # Change as needed
model = AutoModelForCausalLM.from_pretrained(model_name)
tokenizer = AutoTokenizer.from_pretrained(model_name)

# Add padding token if it doesn’t exist
if tokenizer.pad_token is None:
    tokenizer.pad_token = tokenizer.eos_token

# Load and preprocess the fine-tuning data
def load_finetune_data(filename):
    with open(filename, 'r') as f:
        data = json.load(f)
    questions = [ex["question"] for ex in data]
    responses = [ex["response"] for ex in data]
    return {"question": questions, "response": responses}

data = load_finetune_data("njit_finetune_data.json")
dataset = Dataset.from_dict(data)

# Split dataset into train and validation
dataset = dataset.train_test_split(test_size=0.1)
train_dataset = dataset["train"]
eval_dataset = dataset["test"]

# Tokenize function
def tokenize_function(examples):
    input_texts = [f"Question: {q}\nAnswer:" for q in examples["question"]]
    target_texts = examples["response"]
    model_inputs = tokenizer(input_texts, padding="max_length", truncation=True, max_length=128)
    labels = tokenizer(target_texts, padding="max_length", truncation=True, max_length=128)["input_ids"]
    model_inputs["labels"] = labels
    return model_inputs

# Tokenize the dataset
tokenized_train = train_dataset.map(tokenize_function, batched=True)
tokenized_eval = eval_dataset.map(tokenize_function, batched=True)

# Set up training arguments
training_args = TrainingArguments(
    output_dir="./finetuned_njit_bot",
    evaluation_strategy="steps",
    learning_rate=2e-5,
    per_device_train_batch_size=2,
    num_train_epochs=3,
    weight_decay=0.01,
    logging_dir="./logs",
    logging_steps=10
)

# Initialize Trainer with eval_dataset
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_train,
    eval_dataset=tokenized_eval,  # Now we have an eval dataset
    tokenizer=tokenizer,
)

# Train and save the model
trainer.train()
model.save_pretrained("./finetuned_njit_bot")
tokenizer.save_pretrained("./finetuned_njit_bot")
