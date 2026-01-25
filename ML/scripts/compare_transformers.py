import inspect
import json
import os

import pandas as pd
import torch
import joblib
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score, confusion_matrix, f1_score
from transformers import (
    AutoModelForSequenceClassification,
    AutoTokenizer,
    DataCollatorWithPadding,
    EarlyStoppingCallback,
    Trainer,
    TrainingArguments,
    set_seed,
)
from torch.utils.data import Dataset

try:
    import matplotlib.pyplot as plt
except ImportError:
    plt = None

DATA_DIR = "../data/sentence"
DATA_TRAIN = f"{DATA_DIR}/train.csv"
DATA_TEST = f"{DATA_DIR}/test.csv"
REPORT_ROOT = "../reports/transformers/sentence"
MODEL_ROOT = "../models/transformers/sentence"

MODELS = {
    "PubMedBERT": "microsoft/BiomedNLP-PubMedBERT-base-uncased-abstract",
    "RoBERTa": "roberta-base",
    "BioClinicalBERT": "emilyalsentzer/Bio_ClinicalBERT",
}
MODEL_KEYS = ["BioClinicalBERT"]


class SimpleDataset(Dataset):
    def __init__(self, encodings, labels):
        self.encodings = encodings
        self.labels = labels

    def __getitem__(self, idx):
        item = {k: torch.tensor(v[idx]) for k, v in self.encodings.items()}
        item["labels"] = torch.tensor(self.labels[idx])
        return item

    def __len__(self):
        return len(self.labels)


def compute_metrics(pred):
    preds = pred.predictions.argmax(-1)
    return {
        "accuracy": accuracy_score(pred.label_ids, preds),
        "f1_macro": f1_score(pred.label_ids, preds, average="macro", zero_division=0),
        "f1_weighted": f1_score(
            pred.label_ids, preds, average="weighted", zero_division=0
        ),
    }


def split_log_history(log_history):
    train_logs = []
    eval_logs = []
    for entry in log_history:
        if "loss" in entry and "eval_loss" not in entry:
            train_logs.append(entry)
        if "eval_loss" in entry:
            eval_logs.append(entry)
    return train_logs, eval_logs


def save_logs_and_curves(log_history, report_dir):
    os.makedirs(report_dir, exist_ok=True)
    with open(os.path.join(report_dir, "log_history.json"), "w") as f:
        json.dump(log_history, f, indent=2)

    train_logs, eval_logs = split_log_history(log_history)
    if train_logs:
        pd.DataFrame(train_logs).to_csv(
            os.path.join(report_dir, "train_log.csv"), index=False
        )
    if eval_logs:
        pd.DataFrame(eval_logs).to_csv(
            os.path.join(report_dir, "eval_log.csv"), index=False
        )

    if plt is None:
        return

    if train_logs or eval_logs:
        train_steps = [x.get("step") for x in train_logs]
        eval_steps = [x.get("step") for x in eval_logs]
        use_epoch = (
            (train_logs and any(s is None for s in train_steps))
            or (eval_logs and any(s is None for s in eval_steps))
        )
        if use_epoch:
            train_steps = [x.get("epoch") for x in train_logs]
            eval_steps = [x.get("epoch") for x in eval_logs]
            x_label = "Epoch"
        else:
            x_label = "Step"

        fig, ax = plt.subplots(figsize=(6, 4))
        if train_logs:
            train_losses = [x.get("loss") for x in train_logs]
            ax.plot(train_steps, train_losses, label="train_loss")
        if eval_logs:
            eval_loss = [x.get("eval_loss") for x in eval_logs]
            ax.plot(eval_steps, eval_loss, label="val_loss")
        ax.set_xlabel(x_label)
        ax.set_ylabel("Loss")
        ax.set_title("Loss curves")
        ax.grid(True, alpha=0.3)
        ax.legend()
        fig.tight_layout()
        fig.savefig(os.path.join(report_dir, "train_loss.png"))
        plt.close(fig)

    if eval_logs:
        epochs = [x.get("epoch") for x in eval_logs]
        eval_loss = [x.get("eval_loss") for x in eval_logs]
        eval_acc = [x.get("eval_accuracy") for x in eval_logs if "eval_accuracy" in x]
        fig, ax = plt.subplots(figsize=(6, 4))
        ax.plot(epochs, eval_loss, label="eval_loss")
        if eval_acc:
            ax.plot(epochs[: len(eval_acc)], eval_acc, label="eval_accuracy")
        ax.set_xlabel("Epoch")
        ax.set_title("Eval metrics")
        ax.grid(True, alpha=0.3)
        ax.legend()
        fig.tight_layout()
        fig.savefig(os.path.join(report_dir, "eval_metrics.png"))
        plt.close(fig)


def build_training_args(model_name):
    kwargs = {
        "output_dir": f"../models/temp/{model_name}",
        "num_train_epochs": 6,
        "per_device_train_batch_size": 8,
        "learning_rate": 2e-5,
        "fp16": torch.cuda.is_available(),
        "gradient_accumulation_steps": 4,
        "warmup_ratio": 0.1,
        "dataloader_num_workers": 2,
        "dataloader_pin_memory": True,
        "evaluation_strategy": "steps",
        "eval_steps": 3000,
        "logging_strategy": "steps",
        "logging_steps": 50,
        "save_strategy": "steps",
        "save_steps": 3000,
        "save_total_limit": 1,
        "load_best_model_at_end": True,
        "metric_for_best_model": "eval_loss",
        "greater_is_better": False,
        "tf32": torch.cuda.is_available(),
        "report_to": "none",
    }

    sig = inspect.signature(TrainingArguments.__init__)
    has_eval_strategy = "evaluation_strategy" in sig.parameters or "eval_strategy" in sig.parameters
    if "evaluation_strategy" not in sig.parameters and "eval_strategy" in sig.parameters:
        kwargs["eval_strategy"] = kwargs.pop("evaluation_strategy")

    if not has_eval_strategy:
        kwargs.pop("evaluation_strategy", None)
        kwargs.pop("eval_strategy", None)
        kwargs.pop("logging_strategy", None)
        kwargs.pop("save_strategy", None)
        kwargs.pop("save_total_limit", None)
        kwargs.pop("load_best_model_at_end", None)
        kwargs.pop("metric_for_best_model", None)
        kwargs.pop("greater_is_better", None)
        if "evaluate_during_training" in sig.parameters:
            kwargs["evaluate_during_training"] = True

    filtered = {k: v for k, v in kwargs.items() if k in sig.parameters}
    return TrainingArguments(**filtered)


def supports_eval(args):
    eval_strategy = getattr(args, "evaluation_strategy", None)
    if eval_strategy is None:
        eval_strategy = getattr(args, "eval_strategy", None)
    return eval_strategy and str(eval_strategy).lower() != "no"


def main():
    set_seed(42)

    train_df = pd.read_csv(DATA_TRAIN)
    test_df = pd.read_csv(DATA_TEST)

    le = LabelEncoder()
    y_train = le.fit_transform(train_df["label"])
    y_test = le.transform(test_df["label"])

    results = {}

    for name in MODEL_KEYS:
        hf_model = MODELS[name]
        print(f"\n=== {name} ===")
        model_report_dir = os.path.join(REPORT_ROOT, name)
        model_out_dir = os.path.join(MODEL_ROOT, name)
        os.makedirs(model_report_dir, exist_ok=True)
        os.makedirs(model_out_dir, exist_ok=True)

        tokenizer = AutoTokenizer.from_pretrained(hf_model)
        train_enc = tokenizer(
            train_df["text"].tolist(),
            truncation=True,
            max_length=64,
        )
        test_enc = tokenizer(
            test_df["text"].tolist(),
            truncation=True,
            max_length=64,
        )
        data_collator = DataCollatorWithPadding(
            tokenizer=tokenizer, pad_to_multiple_of=8
        )

        train_ds = SimpleDataset(train_enc, y_train)
        test_ds = SimpleDataset(test_enc, y_test)

        model = AutoModelForSequenceClassification.from_pretrained(
            hf_model, num_labels=len(le.classes_)
        )

        args = build_training_args(name)
        callbacks = []
        if supports_eval(args):
            callbacks.append(EarlyStoppingCallback(early_stopping_patience=2))

        trainer = Trainer(
            model=model,
            args=args,
            train_dataset=train_ds,
            eval_dataset=test_ds,
            compute_metrics=compute_metrics,
            callbacks=callbacks,
            data_collator=data_collator,
        )

        trainer.train()
        save_logs_and_curves(trainer.state.log_history, model_report_dir)
        trainer.save_model(model_out_dir)
        tokenizer.save_pretrained(model_out_dir)
        joblib.dump(le, os.path.join(model_out_dir, "label_encoder.pkl"))

        pred_output = trainer.predict(test_ds)
        y_true = pred_output.label_ids
        y_pred = pred_output.predictions.argmax(-1)

        acc = accuracy_score(y_true, y_pred)
        f1_macro = f1_score(y_true, y_pred, average="macro", zero_division=0)
        f1_weighted = f1_score(y_true, y_pred, average="weighted", zero_division=0)
        top_labels = (
            test_df["label"].value_counts().head(20).index.tolist()
        )
        top_labels = [label for label in top_labels if label in le.classes_]
        top_indices = le.transform(top_labels) if top_labels else []
        if top_indices:
            cm = confusion_matrix(y_true, y_pred, labels=top_indices)
            cm_df = pd.DataFrame(cm, index=top_labels, columns=top_labels)
            cm_path = os.path.join(model_report_dir, "confusion_matrix_top20.csv")
            cm_df.to_csv(cm_path)

        results[name] = {
            "accuracy": acc,
            "f1_macro": f1_macro,
            "f1_weighted": f1_weighted,
        }

        with open(os.path.join(model_report_dir, "metrics.json"), "w") as f:
            json.dump(results[name], f, indent=2)

        print(f"Accuracy: {acc:.4f}")


if __name__ == "__main__":
    main()
