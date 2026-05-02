"""
BART Fine-tuning Script
Fine-tunes facebook/bart-large-cnn on a subset of the CNN/DailyMail dataset.
Includes evaluation against the pretrained baseline to measure improvements.
"""

import os
import argparse
import torch
from datasets import load_dataset
from transformers import (
    AutoTokenizer,
    AutoModelForSeq2SeqLM,
    DataCollatorForSeq2Seq,
    Seq2SeqTrainingArguments,
    Seq2SeqTrainer
)
import evaluate
import numpy as np

def main():
    parser = argparse.ArgumentParser(description="Fine-tune BART on CNN/DailyMail")
    parser.add_argument("--model_name", type=str, default="facebook/bart-large-cnn")
    parser.add_argument("--output_dir", type=str, default="./checkpoints/bart_finetuned")
    parser.add_argument("--epochs", type=int, default=3)
    parser.add_argument("--batch_size", type=int, default=4)
    parser.add_argument("--train_samples", type=int, default=500, help="Subset size for quick fine-tuning")
    parser.add_argument("--val_samples", type=int, default=100)
    args = parser.parse_args()

    print(f"Loading {args.model_name}...")
    tokenizer = AutoTokenizer.from_pretrained(args.model_name)
    model = AutoModelForSeq2SeqLM.from_pretrained(args.model_name)

    print("Loading CNN/DailyMail dataset subset...")
    # Load dataset
    dataset = load_dataset("cnn_dailymail", "3.0.0", trust_remote_code=True)
    
    # Create small subsets
    train_dataset = dataset["train"].select(range(args.train_samples))
    eval_dataset = dataset["validation"].select(range(args.val_samples))

    def preprocess_function(examples):
        inputs = [doc for doc in examples["article"]]
        model_inputs = tokenizer(inputs, max_length=1024, truncation=True)

        # Setup the tokenizer for targets
        labels = tokenizer(text_target=examples["highlights"], max_length=128, truncation=True)

        model_inputs["labels"] = labels["input_ids"]
        return model_inputs

    print("Tokenizing datasets...")
    tokenized_train = train_dataset.map(preprocess_function, batched=True, remove_columns=train_dataset.column_names)
    tokenized_eval = eval_dataset.map(preprocess_function, batched=True, remove_columns=eval_dataset.column_names)

    data_collator = DataCollatorForSeq2Seq(tokenizer=tokenizer, model=model)

    # ROUGE metric
    rouge = evaluate.load("rouge")

    def compute_metrics(eval_pred):
        predictions, labels = eval_pred
        decoded_preds = tokenizer.batch_decode(predictions, skip_special_tokens=True)
        # Replace -100 in the labels as we can't decode them
        labels = np.where(labels != -100, labels, tokenizer.pad_token_id)
        decoded_labels = tokenizer.batch_decode(labels, skip_special_tokens=True)

        # ROUGE expects a newline after each sentence
        decoded_preds = ["\n".join(pred.strip().split(" ")) for pred in decoded_preds]
        decoded_labels = ["\n".join(label.strip().split(" ")) for label in decoded_labels]

        result = rouge.compute(predictions=decoded_preds, references=decoded_labels, use_stemmer=True)
        result = {key: value * 100 for key, value in result.items()}
        return {k: round(v, 4) for k, v in result.items()}

    training_args = Seq2SeqTrainingArguments(
        output_dir=args.output_dir,
        evaluation_strategy="epoch",
        learning_rate=2e-5,
        per_device_train_batch_size=args.batch_size,
        per_device_eval_batch_size=args.batch_size,
        weight_decay=0.01,
        save_total_limit=2,
        num_train_epochs=args.epochs,
        predict_with_generate=True,
        fp16=torch.cuda.is_available(),
        logging_steps=10,
    )

    trainer = Seq2SeqTrainer(
        model=model,
        args=training_args,
        train_dataset=tokenized_train,
        eval_dataset=tokenized_eval,
        tokenizer=tokenizer,
        data_collator=data_collator,
        compute_metrics=compute_metrics,
    )

    print("Evaluating pre-trained baseline...")
    baseline_metrics = trainer.evaluate()
    print("Baseline Metrics:", baseline_metrics)

    print("Starting Fine-tuning...")
    trainer.train()

    print("Evaluating fine-tuned model...")
    finetuned_metrics = trainer.evaluate()
    print("Fine-tuned Metrics:", finetuned_metrics)

    print("Saving fine-tuned model...")
    trainer.save_model(os.path.join(args.output_dir, "final"))

if __name__ == "__main__":
    main()
