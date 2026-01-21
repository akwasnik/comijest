import os

os.environ['TF_USE_LEGACY_KERAS'] = '1'

import pandas as pd
import torch
import joblib
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score
from transformers import AutoTokenizer, AutoModelForSequenceClassification, Trainer, TrainingArguments
from torch.utils.data import Dataset

# --- KONFIGURACJA MODELU ---
# BioBERT - specjalista od medycyny
NAZWA_MODELU_HUGGINGFACE = "dmis-lab/biobert-v1.1"
NAZWA_NASZA = "BioBERT"


# --- KLASA Z DANYMI (Kopiuj-Wklej, żeby plik był niezależny) ---
class ProstyZestawDanych(Dataset):
    def __init__(self, tokeny, etykiety):
        self.tokeny = tokeny
        self.etykiety = etykiety

    def __getitem__(self, idx):
        item = {key: torch.tensor(val[idx]) for key, val in self.tokeny.items()}
        item['labels'] = torch.tensor(self.etykiety[idx])
        return item

    def __len__(self):
        return len(self.etykiety)


def oblicz_dokladnosc(pred):
    return {'dokladnosc': accuracy_score(pred.label_ids, pred.predictions.argmax(-1))}


def main():
    print(f"--- TRENING MODELU: {NAZWA_NASZA} (Specjalista Medyczny) ---")

    # 1. Wczytanie danych
    train_df = pd.read_csv('../data/processed/train.csv')
    test_df = pd.read_csv('../data/processed/test.csv')

    # 2. Zamiana chorób na liczby
    le = LabelEncoder()
    train_labels = le.fit_transform(train_df['label'])
    test_labels = le.transform(test_df['label'])

    # 3. Tokenizer (Tłumacz specyficzny dla BioBERT)
    print("Pobieranie tokenizera...")
    tokenizer = AutoTokenizer.from_pretrained(NAZWA_MODELU_HUGGINGFACE)
    train_enc = tokenizer(train_df['text'].tolist(), truncation=True, padding=True, max_length=64)
    test_enc = tokenizer(test_df['text'].tolist(), truncation=True, padding=True, max_length=64)

    dataset_train = ProstyZestawDanych(train_enc, train_labels)
    dataset_test = ProstyZestawDanych(test_enc, test_labels)

    # 4. Pobranie Modelu
    print("Pobieranie modelu...")
    model = AutoModelForSequenceClassification.from_pretrained(NAZWA_MODELU_HUGGINGFACE, num_labels=len(le.classes_))

    # 5. Trening
    trener = Trainer(
        model=model,
        args=TrainingArguments(
            output_dir=f'../models/temp/{NAZWA_NASZA}',  # Zapis brudnopisu do folderu temp
            num_train_epochs=3,
            per_device_train_batch_size=8,
            logging_steps=10
        ),
        train_dataset=dataset_train,
        eval_dataset=dataset_test,
        compute_metrics=oblicz_dokladnosc
    )

    print("Rozpoczynam trening...")
    trener.train()

    # 6. Zapis wyniku (liczby)
    wynik = trener.evaluate()['eval_dokladnosc']
    print(f"--> SKUTECZNOŚĆ KOŃCOWA: {wynik:.2%}")

    if not os.path.exists('../reports'): os.makedirs('../reports')
    joblib.dump(wynik, f'../reports/score_{NAZWA_NASZA}.pkl')

    # 7. Zapis gotowego modelu
    sciezka = f'../models/model_{NAZWA_NASZA}'
    model.save_pretrained(sciezka)
    tokenizer.save_pretrained(sciezka)
    print(f"✅ Model zapisany w: {sciezka}")


if __name__ == "__main__":
    main()