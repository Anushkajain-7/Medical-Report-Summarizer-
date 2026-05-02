"""
LSTM Seq2Seq Summarization Model with Attention
Implements a 2-layer stacked LSTM encoder-decoder with Bahdanau attention
for abstractive text summarization.

Architecture:
- Encoder: 2-layer stacked bidirectional LSTM (hidden=512)
- Attention: Bahdanau (additive) attention mechanism
- Decoder: 2-layer LSTM with attention context + teacher forcing (ratio=0.5)
"""

import torch
import torch.nn as nn
import torch.nn.functional as F
import random


class Encoder(nn.Module):
    """
    2-layer stacked bidirectional LSTM encoder.
    Processes input sequences and produces hidden states for attention.
    """

    def __init__(self, vocab_size, embed_dim=256, hidden_dim=512, n_layers=2, dropout=0.3):
        super().__init__()
        self.embedding = nn.Embedding(vocab_size, embed_dim, padding_idx=0)
        self.lstm = nn.LSTM(
            embed_dim, hidden_dim, num_layers=n_layers,
            bidirectional=True, dropout=dropout if n_layers > 1 else 0,
            batch_first=True
        )
        self.fc_hidden = nn.Linear(hidden_dim * 2, hidden_dim)
        self.fc_cell = nn.Linear(hidden_dim * 2, hidden_dim)
        self.dropout = nn.Dropout(dropout)
        self.hidden_dim = hidden_dim
        self.n_layers = n_layers

    def forward(self, src, src_lengths=None):
        # src: [batch, src_len]
        embedded = self.dropout(self.embedding(src))  # [batch, src_len, embed_dim]

        if src_lengths is not None:
            packed = nn.utils.rnn.pack_padded_sequence(
                embedded, src_lengths.cpu(), batch_first=True, enforce_sorted=False
            )
            outputs, (hidden, cell) = self.lstm(packed)
            outputs, _ = nn.utils.rnn.pad_packed_sequence(outputs, batch_first=True)
        else:
            outputs, (hidden, cell) = self.lstm(embedded)

        # hidden: [n_layers*2, batch, hidden_dim] -> [n_layers, batch, hidden_dim]
        # Concatenate forward and backward hidden states
        hidden = torch.cat([hidden[0::2], hidden[1::2]], dim=2)  # [n_layers, batch, hidden*2]
        cell = torch.cat([cell[0::2], cell[1::2]], dim=2)

        hidden = torch.tanh(self.fc_hidden(hidden))  # [n_layers, batch, hidden]
        cell = torch.tanh(self.fc_cell(cell))

        return outputs, hidden, cell


class BahdanauAttention(nn.Module):
    """
    Bahdanau (additive) attention mechanism.
    Computes attention weights between decoder hidden state and encoder outputs.
    """

    def __init__(self, hidden_dim=512, encoder_dim=1024):
        super().__init__()
        self.W_h = nn.Linear(encoder_dim, hidden_dim, bias=False)
        self.W_s = nn.Linear(hidden_dim, hidden_dim, bias=False)
        self.v = nn.Linear(hidden_dim, 1, bias=False)

    def forward(self, decoder_hidden, encoder_outputs, mask=None):
        """
        decoder_hidden: [batch, hidden_dim]
        encoder_outputs: [batch, src_len, encoder_dim]
        mask: [batch, src_len] - 1 for valid positions, 0 for padding
        """
        src_len = encoder_outputs.size(1)

        # Repeat decoder hidden state src_len times
        decoder_hidden = decoder_hidden.unsqueeze(1).repeat(1, src_len, 1)

        # Energy
        energy = torch.tanh(
            self.W_h(encoder_outputs) + self.W_s(decoder_hidden)
        )  # [batch, src_len, hidden_dim]

        attention = self.v(energy).squeeze(2)  # [batch, src_len]

        if mask is not None:
            attention = attention.masked_fill(mask == 0, -1e10)

        weights = F.softmax(attention, dim=1)  # [batch, src_len]

        # Context vector
        context = torch.bmm(weights.unsqueeze(1), encoder_outputs)  # [batch, 1, encoder_dim]
        context = context.squeeze(1)  # [batch, encoder_dim]

        return context, weights


class Decoder(nn.Module):
    """
    2-layer LSTM decoder with Bahdanau attention.
    Uses teacher forcing during training.
    """

    def __init__(self, vocab_size, embed_dim=256, hidden_dim=512, encoder_dim=1024,
                 n_layers=2, dropout=0.3, use_attention=True):
        super().__init__()
        self.embedding = nn.Embedding(vocab_size, embed_dim, padding_idx=0)
        self.use_attention = use_attention

        if use_attention:
            self.attention = BahdanauAttention(hidden_dim, encoder_dim)
            lstm_input_dim = embed_dim + encoder_dim
        else:
            lstm_input_dim = embed_dim

        self.lstm = nn.LSTM(
            lstm_input_dim, hidden_dim, num_layers=n_layers,
            dropout=dropout if n_layers > 1 else 0,
            batch_first=True
        )
        self.fc_out = nn.Linear(hidden_dim + encoder_dim if use_attention else hidden_dim, vocab_size)
        self.dropout = nn.Dropout(dropout)
        self.hidden_dim = hidden_dim
        self.vocab_size = vocab_size

    def forward(self, trg_token, hidden, cell, encoder_outputs, mask=None):
        """
        Single-step decoder forward pass.
        trg_token: [batch] - current target token
        """
        embedded = self.dropout(self.embedding(trg_token.unsqueeze(1)))  # [batch, 1, embed_dim]

        if self.use_attention:
            context, attn_weights = self.attention(hidden[-1], encoder_outputs, mask)
            lstm_input = torch.cat([embedded, context.unsqueeze(1)], dim=2)
        else:
            attn_weights = None
            lstm_input = embedded

        output, (hidden, cell) = self.lstm(lstm_input, (hidden, cell))
        output = output.squeeze(1)  # [batch, hidden_dim]

        if self.use_attention:
            output = torch.cat([output, context], dim=1)

        prediction = self.fc_out(output)  # [batch, vocab_size]

        return prediction, hidden, cell, attn_weights


class Seq2SeqLSTM(nn.Module):
    """
    Full Seq2Seq model combining encoder, attention, and decoder.
    Supports teacher forcing with configurable ratio.
    """

    def __init__(self, encoder, decoder, device, teacher_forcing_ratio=0.5):
        super().__init__()
        self.encoder = encoder
        self.decoder = decoder
        self.device = device
        self.teacher_forcing_ratio = teacher_forcing_ratio

    def forward(self, src, trg, src_lengths=None, teacher_forcing_ratio=None):
        """
        src: [batch, src_len]
        trg: [batch, trg_len]
        """
        if teacher_forcing_ratio is None:
            teacher_forcing_ratio = self.teacher_forcing_ratio

        batch_size = src.size(0)
        trg_len = trg.size(1)
        trg_vocab_size = self.decoder.vocab_size

        # Tensor to store decoder outputs
        outputs = torch.zeros(batch_size, trg_len, trg_vocab_size).to(self.device)

        # Create padding mask
        mask = (src != 0).float()

        # Encode
        encoder_outputs, hidden, cell = self.encoder(src, src_lengths)

        # First input to decoder is <SOS> token
        decoder_input = trg[:, 0]

        for t in range(1, trg_len):
            prediction, hidden, cell, _ = self.decoder(
                decoder_input, hidden, cell, encoder_outputs, mask
            )
            outputs[:, t] = prediction

            # Teacher forcing
            use_teacher = random.random() < teacher_forcing_ratio
            top1 = prediction.argmax(1)
            decoder_input = trg[:, t] if use_teacher else top1

        return outputs

    def generate(self, src, src_lengths=None, max_len=100, sos_idx=2, eos_idx=3):
        """Generate summary without teacher forcing (inference)."""
        self.eval()
        batch_size = src.size(0)
        mask = (src != 0).float()

        with torch.no_grad():
            encoder_outputs, hidden, cell = self.encoder(src, src_lengths)
            decoder_input = torch.full((batch_size,), sos_idx, dtype=torch.long).to(self.device)

            generated = []
            for _ in range(max_len):
                prediction, hidden, cell, _ = self.decoder(
                    decoder_input, hidden, cell, encoder_outputs, mask
                )
                top1 = prediction.argmax(1)
                generated.append(top1)

                if (top1 == eos_idx).all():
                    break

                decoder_input = top1

        return torch.stack(generated, dim=1)  # [batch, gen_len]


def build_seq2seq_model(vocab_size, device, embed_dim=256, hidden_dim=512,
                        n_layers=2, dropout=0.3, use_attention=True,
                        teacher_forcing_ratio=0.5):
    """Build and return a Seq2Seq LSTM model."""
    encoder = Encoder(vocab_size, embed_dim, hidden_dim, n_layers, dropout)
    decoder = Decoder(
        vocab_size, embed_dim, hidden_dim,
        encoder_dim=hidden_dim * 2,  # bidirectional encoder
        n_layers=n_layers, dropout=dropout,
        use_attention=use_attention
    )
    model = Seq2SeqLSTM(encoder, decoder, device, teacher_forcing_ratio)
    model = model.to(device)

    # Count parameters
    total_params = sum(p.numel() for p in model.parameters())
    trainable_params = sum(p.numel() for p in model.parameters() if p.requires_grad)
    print(f"[Seq2Seq] Total params: {total_params:,} | Trainable: {trainable_params:,}")
    print(f"[Seq2Seq] Attention: {use_attention} | Teacher forcing: {teacher_forcing_ratio}")

    return model
