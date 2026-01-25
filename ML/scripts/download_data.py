import argparse
import os

import pandas as pd
from datasets import ClassLabel, load_dataset

DEFAULT_DATASET = "fhai50032/SymptomsDisease246k"
DEFAULT_TEXT_COL = "query"
DEFAULT_LABEL_COL = "response"
OUTPUT_DIR = "../data/processed"


def clean_text(value):
    text = str(value).strip()
    prefix = "Having these specific symptoms :->"
    suffix = "may indicate"
    if text.lower().startswith(prefix.lower()):
        text = text[len(prefix):].strip()
    if text.lower().endswith(suffix):
        text = text[:-len(suffix)].strip(" ,.-")
    return text


def clean_label(value):
    label = str(value).strip()
    prefix = "you may have"
    if label.lower().startswith(prefix):
        label = label[len(prefix):].strip(" :-")
    return label


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--dataset", default=DEFAULT_DATASET)
    parser.add_argument("--text-col", default=DEFAULT_TEXT_COL)
    parser.add_argument("--label-col", default=DEFAULT_LABEL_COL)
    parser.add_argument("--test-size", type=float, default=0.2)
    parser.add_argument("--seed", type=int, default=42)
    args = parser.parse_args()

    print(f"Loading dataset: {args.dataset}")
    data = load_dataset(args.dataset)
    base = data["train"] if "train" in data else data

    try:
        split = base.train_test_split(
            test_size=args.test_size,
            seed=args.seed,
            stratify_by_column=args.label_col,
        )
    except Exception:
        split = base.train_test_split(
            test_size=args.test_size,
            seed=args.seed,
        )

    train_df = split["train"].to_pandas()
    test_df = split["test"].to_pandas()

    if isinstance(base.features.get(args.label_col), ClassLabel):
        mapping = base.features[args.label_col].int2str
        train_df[args.label_col] = train_df[args.label_col].map(mapping)
        test_df[args.label_col] = test_df[args.label_col].map(mapping)

    train_df = train_df[[args.text_col, args.label_col]].rename(
        columns={args.text_col: "text", args.label_col: "label"}
    )
    test_df = test_df[[args.text_col, args.label_col]].rename(
        columns={args.text_col: "text", args.label_col: "label"}
    )

    train_df["text"] = train_df["text"].apply(clean_text)
    test_df["text"] = test_df["text"].apply(clean_text)
    train_df["label"] = train_df["label"].apply(clean_label)
    test_df["label"] = test_df["label"].apply(clean_label)

    train_labels = set(train_df["label"])
    unseen_mask = ~test_df["label"].isin(train_labels)
    if unseen_mask.any():
        moved = test_df[unseen_mask]
        test_df = test_df[~unseen_mask]
        train_df = pd.concat([train_df, moved], ignore_index=True)
        print(f"Moved {len(moved)} samples from test to train (unseen labels).")

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    train_df.to_csv(f"{OUTPUT_DIR}/train.csv", index=False)
    test_df.to_csv(f"{OUTPUT_DIR}/test.csv", index=False)
    print(f"Saved: {OUTPUT_DIR}/train.csv, {OUTPUT_DIR}/test.csv")

if __name__ == "__main__":
    main()
