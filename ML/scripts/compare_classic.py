import json
import os

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from sklearn.naive_bayes import MultinomialNB
from sklearn.svm import LinearSVC

DATA_DIR = "../data/sentence"
DATA_TRAIN = f"{DATA_DIR}/train.csv"
DATA_TEST = f"{DATA_DIR}/test.csv"
REPORT_PATH = "../reports/compare_classic_sentence.json"


def main():
    train_df = pd.read_csv(DATA_TRAIN)
    test_df = pd.read_csv(DATA_TEST)

    X_train = train_df["text"]
    y_train = train_df["label"]
    X_test = test_df["text"]
    y_test = test_df["label"]

    vectorizer = TfidfVectorizer(
        stop_words="english",
        ngram_range=(1, 2),
        max_features=20000,
    )
    X_train_vec = vectorizer.fit_transform(X_train)
    X_test_vec = vectorizer.transform(X_test)

    models = {
        "LogReg": LogisticRegression(max_iter=2000, n_jobs=-1),
        "LinearSVM": LinearSVC(),
        "MultinomialNB": MultinomialNB(),
    }

    results = {}
    for name, model in models.items():
        print(f"Training: {name}")
        model.fit(X_train_vec, y_train)
        preds = model.predict(X_test_vec)
        acc = accuracy_score(y_test, preds)
        results[name] = acc
        print(f"Accuracy: {acc:.4f}")

    os.makedirs(os.path.dirname(REPORT_PATH), exist_ok=True)
    with open(REPORT_PATH, "w") as f:
        json.dump(results, f, indent=2)

    print(f"Saved results to {REPORT_PATH}")


if __name__ == "__main__":
    main()
