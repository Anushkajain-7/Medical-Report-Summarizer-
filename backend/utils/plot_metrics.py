import os
import json
import matplotlib.pyplot as plt

def plot_loss_curves(results_file="checkpoints/training_results.json", output_file="checkpoints/training_loss_curves.png"):
    """
    Reads the training_results.json file and plots the training and validation loss curves
    for both 'with_attention' and 'without_attention' models.
    """
    if not os.path.exists(results_file):
        print(f"Error: {results_file} not found.")
        return

    with open(results_file, 'r') as f:
        data = json.load(f)

    plt.figure(figsize=(10, 6))

    colors = {"with_attention": ("blue", "cyan"), "without_attention": ("red", "orange")}

    for config_name, results in data.items():
        history = results.get("training_history", [])
        if not history:
            continue
            
        epochs = [h["epoch"] for h in history]
        train_loss = [h["train_loss"] for h in history]
        val_loss = [h["val_loss"] for h in history]

        primary_color, secondary_color = colors.get(config_name, ("black", "gray"))

        plt.plot(epochs, train_loss, label=f"Train Loss ({config_name})", linestyle="--", color=primary_color)
        plt.plot(epochs, val_loss, label=f"Val Loss ({config_name})", linestyle="-", color=secondary_color, linewidth=2)

    plt.title("LSTM Seq2Seq: Training & Validation Loss Curves", fontsize=14)
    plt.xlabel("Epochs", fontsize=12)
    plt.ylabel("Cross-Entropy Loss", fontsize=12)
    plt.legend()
    plt.grid(True, linestyle=":", alpha=0.7)
    
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    print(f"Successfully saved loss curves to {output_file}")

if __name__ == "__main__":
    plot_loss_curves()
