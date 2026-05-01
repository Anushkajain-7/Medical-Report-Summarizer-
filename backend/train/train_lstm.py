"""
LSTM Seq2Seq Training Script
Trains the Seq2Seq LSTM encoder-decoder on CNN/DailyMail dataset.

Features:
- CNN/DailyMail dataset via HuggingFace
- 2-layer stacked LSTM encoder (hidden=512)
- Bahdanau attention mechanism
- Teacher forcing (ratio=0.5)
- Adam optimizer with gradient clipping (max_norm=1.0)
- Packed sequences for variable lengths
- ROUGE evaluation
- Ablation: attention vs no-attention comparison

Usage:
    python train_lstm.py --epochs 5 --batch_size 16 --max_samples 5000
"""

import sys
import os
import argparse
import json
import time

import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import Dataset, DataLoader
from collections import Counter

# Add parent to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models.lstm_seq2seq import build_seq2seq_model
from pipeline.rouge_eval import compute_rouge_scores


# ============================================================
# Simple Tokenizer
# ============================================================

class SimpleTokenizer:
    """Word-level tokenizer with vocabulary building."""

    def __init__(self, max_vocab=30000):
        self.word2idx = {"<pad>": 0, "<unk>": 1, "<sos>": 2, "<eos>": 3}
        self.idx2word = {0: "<pad>", 1: "<unk>", 2: "<sos>", 3: "<eos>"}
        self.max_vocab = max_vocab

    def build_vocab(self, texts):
        """Build vocabulary from list of texts."""
        counter = Counter()
        for text in texts:
            tokens = text.lower().split()
            counter.update(tokens)

        for word, _ in counter.most_common(self.max_vocab - 4):
            idx = len(self.word2idx)
            self.word2idx[word] = idx
            self.idx2word[idx] = word

        print(f"[Tokenizer] Vocabulary size: {len(self.word2idx)}")

    def encode(self, text, max_len=512):
        """Convert text to token indices."""
        tokens = text.lower().split()[:max_len - 2]
        indices = [self.word2idx["<sos>"]]
        for token in tokens:
            indices.append(self.word2idx.get(token, self.word2idx["<unk>"]))
        indices.append(self.word2idx["<eos>"])
        return indices

    def decode(self, indices):
        """Convert token indices back to text."""
        words = []
        for idx in indices:
            if isinstance(idx, torch.Tensor):
                idx = idx.item()
            word = self.idx2word.get(idx, "<unk>")
            if word == "<eos>":
                break
            if word not in ("<pad>", "<sos>"):
                words.append(word)
        return " ".join(words)

    @property
    def vocab_size(self):
        return len(self.word2idx)


# ============================================================
# Dataset
# ============================================================

class SummarizationDataset(Dataset):
    """Dataset for seq2seq summarization."""

    def __init__(self, articles, summaries, tokenizer, max_src_len=512, max_trg_len=128):
        self.articles = articles
        self.summaries = summaries
        self.tokenizer = tokenizer
        self.max_src_len = max_src_len
        self.max_trg_len = max_trg_len

    def __len__(self):
        return len(self.articles)

    def __getitem__(self, idx):
        src = self.tokenizer.encode(self.articles[idx], self.max_src_len)
        trg = self.tokenizer.encode(self.summaries[idx], self.max_trg_len)
        return torch.tensor(src), torch.tensor(trg)


def collate_fn(batch):
    """Pad sequences to same length in batch."""
    src_batch, trg_batch = zip(*batch)

    src_lengths = torch.tensor([len(s) for s in src_batch])
    max_src = max(len(s) for s in src_batch)
    max_trg = max(len(t) for t in trg_batch)

    src_padded = torch.zeros(len(batch), max_src, dtype=torch.long)
    trg_padded = torch.zeros(len(batch), max_trg, dtype=torch.long)

    for i, (src, trg) in enumerate(zip(src_batch, trg_batch)):
        src_padded[i, :len(src)] = src
        trg_padded[i, :len(trg)] = trg

    return src_padded, trg_padded, src_lengths


# ============================================================
# Training Functions
# ============================================================

def train_epoch(model, dataloader, optimizer, criterion, clip, device):
    """Train for one epoch."""
    model.train()
    epoch_loss = 0
    n_batches = 0

    for src, trg, src_lengths in dataloader:
        src, trg, src_lengths = src.to(device), trg.to(device), src_lengths.to(device)

        optimizer.zero_grad()
        output = model(src, trg, src_lengths)

        # Reshape for loss: ignore <sos> token
        output = output[:, 1:].contiguous().view(-1, output.size(-1))
        trg = trg[:, 1:].contiguous().view(-1)

        loss = criterion(output, trg)
        loss.backward()

        # Gradient clipping
        torch.nn.utils.clip_grad_norm_(model.parameters(), clip)

        optimizer.step()
        epoch_loss += loss.item()
        n_batches += 1

    return epoch_loss / max(n_batches, 1)


def evaluate(model, dataloader, criterion, device):
    """Evaluate model on validation set."""
    model.eval()
    epoch_loss = 0
    n_batches = 0

    with torch.no_grad():
        for src, trg, src_lengths in dataloader:
            src, trg, src_lengths = src.to(device), trg.to(device), src_lengths.to(device)
            output = model(src, trg, src_lengths, teacher_forcing_ratio=0)

            output = output[:, 1:].contiguous().view(-1, output.size(-1))
            trg = trg[:, 1:].contiguous().view(-1)

            loss = criterion(output, trg)
            epoch_loss += loss.item()
            n_batches += 1

    return epoch_loss / max(n_batches, 1)


def evaluate_rouge(model, dataset, tokenizer, device, n_samples=100):
    """Evaluate ROUGE scores on a subset."""
    model.eval()
    rouge_scores = {"rouge1": [], "rouge2": [], "rougeL": []}

    with torch.no_grad():
        for i in range(min(n_samples, len(dataset))):
            src, trg = dataset[i]
            src = src.unsqueeze(0).to(device)
            src_lengths = torch.tensor([src.size(1)])

            generated = model.generate(src, src_lengths, max_len=128)
            pred_text = tokenizer.decode(generated[0])
            ref_text = tokenizer.decode(trg)

            if pred_text.strip() and ref_text.strip():
                scores = compute_rouge_scores(ref_text, pred_text)
                for metric in rouge_scores:
                    rouge_scores[metric].append(scores[metric]["f1"])

    avg_scores = {}
    for metric in rouge_scores:
        vals = rouge_scores[metric]
        avg_scores[metric] = round(sum(vals) / max(len(vals), 1), 4)

    return avg_scores


# ============================================================
# Main Training Loop
# ============================================================

def main():
    parser = argparse.ArgumentParser(description="Train LSTM Seq2Seq Summarizer")
    parser.add_argument("--epochs", type=int, default=5, help="Number of training epochs")
    parser.add_argument("--batch_size", type=int, default=16, help="Batch size")
    parser.add_argument("--hidden_dim", type=int, default=512, help="LSTM hidden dimension")
    parser.add_argument("--embed_dim", type=int, default=256, help="Embedding dimension")
    parser.add_argument("--n_layers", type=int, default=2, help="Number of LSTM layers")
    parser.add_argument("--lr", type=float, default=0.001, help="Learning rate")
    parser.add_argument("--clip", type=float, default=1.0, help="Gradient clipping max_norm")
    parser.add_argument("--teacher_forcing", type=float, default=0.5, help="Teacher forcing ratio")
    parser.add_argument("--max_samples", type=int, default=5000, help="Max training samples")
    parser.add_argument("--max_src_len", type=int, default=512, help="Max source sequence length")
    parser.add_argument("--max_trg_len", type=int, default=128, help="Max target sequence length")
    parser.add_argument("--max_vocab", type=int, default=30000, help="Max vocabulary size")
    parser.add_argument("--ablation", action="store_true", help="Run ablation study (with vs without attention)")
    parser.add_argument("--output_dir", type=str, default="./checkpoints", help="Output directory")
    args = parser.parse_args()

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"[Train] Using device: {device}")

    # Load CNN/DailyMail dataset
    print("[Train] Loading CNN/DailyMail dataset...")
    try:
        from datasets import load_dataset
        dataset = load_dataset("cnn_dailymail", "3.0.0", split="train", trust_remote_code=True)
        val_dataset = load_dataset("cnn_dailymail", "3.0.0", split="validation", trust_remote_code=True)

        articles = [d["article"][:2000] for d in dataset.select(range(min(args.max_samples, len(dataset))))]
        summaries = [d["highlights"][:500] for d in dataset.select(range(min(args.max_samples, len(dataset))))]
        val_articles = [d["article"][:2000] for d in val_dataset.select(range(min(500, len(val_dataset))))]
        val_summaries = [d["highlights"][:500] for d in val_dataset.select(range(min(500, len(val_dataset))))]

        print(f"[Train] Loaded {len(articles)} train, {len(val_articles)} val samples")
    except Exception as e:
        print(f"[Train] Error loading dataset: {e}")
        print("[Train] Using synthetic data for demonstration...")
        articles = ["This is a sample article about medical conditions. " * 50] * 100
        summaries = ["Sample summary of the article."] * 100
        val_articles = articles[:20]
        val_summaries = summaries[:20]

    # Build tokenizer
    tokenizer = SimpleTokenizer(max_vocab=args.max_vocab)
    tokenizer.build_vocab(articles + summaries)

    # Create datasets
    train_ds = SummarizationDataset(articles, summaries, tokenizer, args.max_src_len, args.max_trg_len)
    val_ds = SummarizationDataset(val_articles, val_summaries, tokenizer, args.max_src_len, args.max_trg_len)

    train_loader = DataLoader(train_ds, batch_size=args.batch_size, shuffle=True, collate_fn=collate_fn)
    val_loader = DataLoader(val_ds, batch_size=args.batch_size, shuffle=False, collate_fn=collate_fn)

    # Configurations to train
    configs = [{"name": "with_attention", "use_attention": True}]
    if args.ablation:
        configs.append({"name": "without_attention", "use_attention": False})

    results = {}

    for config in configs:
        print(f"\n{'='*60}")
        print(f"Training: {config['name']}")
        print(f"{'='*60}")

        model = build_seq2seq_model(
            vocab_size=tokenizer.vocab_size,
            device=device,
            embed_dim=args.embed_dim,
            hidden_dim=args.hidden_dim,
            n_layers=args.n_layers,
            use_attention=config["use_attention"],
            teacher_forcing_ratio=args.teacher_forcing,
        )

        optimizer = optim.Adam(model.parameters(), lr=args.lr)
        criterion = nn.CrossEntropyLoss(ignore_index=0)  # Ignore padding

        best_val_loss = float('inf')
        training_history = []

        for epoch in range(args.epochs):
            start_time = time.time()

            train_loss = train_epoch(model, train_loader, optimizer, criterion, args.clip, device)
            val_loss = evaluate(model, val_loader, criterion, device)

            elapsed = time.time() - start_time

            print(f"  Epoch {epoch+1}/{args.epochs} | "
                  f"Train Loss: {train_loss:.4f} | Val Loss: {val_loss:.4f} | "
                  f"Time: {elapsed:.1f}s")

            training_history.append({
                "epoch": epoch + 1,
                "train_loss": round(train_loss, 4),
                "val_loss": round(val_loss, 4),
                "time": round(elapsed, 1),
            })

            if val_loss < best_val_loss:
                best_val_loss = val_loss
                os.makedirs(args.output_dir, exist_ok=True)
                torch.save(model.state_dict(),
                          os.path.join(args.output_dir, f"seq2seq_{config['name']}.pt"))

        # ROUGE evaluation
        print(f"\n  Evaluating ROUGE scores for {config['name']}...")
        rouge = evaluate_rouge(model, val_ds, tokenizer, device, n_samples=50)
        print(f"  ROUGE-1: {rouge['rouge1']} | ROUGE-2: {rouge['rouge2']} | ROUGE-L: {rouge['rougeL']}")

        results[config["name"]] = {
            "rouge_scores": rouge,
            "best_val_loss": round(best_val_loss, 4),
            "training_history": training_history,
            "config": {
                "hidden_dim": args.hidden_dim,
                "n_layers": args.n_layers,
                "attention": config["use_attention"],
                "teacher_forcing": args.teacher_forcing,
            }
        }

    # Save results
    os.makedirs(args.output_dir, exist_ok=True)
    with open(os.path.join(args.output_dir, "training_results.json"), "w") as f:
        json.dump(results, f, indent=2)

    print(f"\n{'='*60}")
    print("TRAINING COMPLETE")
    print(f"{'='*60}")
    for name, res in results.items():
        print(f"\n{name}:")
        print(f"  ROUGE-1: {res['rouge_scores']['rouge1']}")
        print(f"  ROUGE-2: {res['rouge_scores']['rouge2']}")
        print(f"  ROUGE-L: {res['rouge_scores']['rougeL']}")
        print(f"  Best Val Loss: {res['best_val_loss']}")

    if args.ablation and len(results) == 2:
        print(f"\n{'='*60}")
        print("ABLATION STUDY: Attention vs No Attention")
        print(f"{'='*60}")
        with_attn = results["with_attention"]["rouge_scores"]
        without_attn = results["without_attention"]["rouge_scores"]
        for metric in ["rouge1", "rouge2", "rougeL"]:
            diff = with_attn[metric] - without_attn[metric]
            print(f"  {metric}: +attention={with_attn[metric]} | -attention={without_attn[metric]} | delta={diff:+.4f}")


if __name__ == "__main__":
    main()
