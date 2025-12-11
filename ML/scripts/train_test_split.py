import pandas as pd
import os
from sklearn.model_selection import train_test_split

# Ścieżki
INPUT_FILE = 'ML/data/raw/Symptom2Disease.csv'
OUTPUT_DIR = 'ML/data/processed'


def main():
    print("--- 1. PRZYGOTOWANIE DANYCH (Symptom2Disease) ---")

    if not os.path.exists(INPUT_FILE):
        print(f"BŁĄD: Brak pliku {INPUT_FILE}. Pobierz go z Kaggle!")
        return

    # Wczytanie i czyszczenie
    df = pd.read_csv(INPUT_FILE)
    # Usuwamy zbędną kolumnę z ID, jeśli jest
    if 'Unnamed: 0' in df.columns:
        df = df.drop(columns=['Unnamed: 0'])

    # Upewniamy się, że kolumny to 'label' (choroba) i 'text' (opis)
    df.columns = ['label', 'text']

    print(f"Liczba wierszy: {len(df)}")
    print(f"Przykład tekstu: {df['text'].iloc[0]}")

    # Podział 80/20
    train_df, test_df = train_test_split(df, test_size=0.2, random_state=42, stratify=df['label'])

    if not os.path.exists(OUTPUT_DIR): os.makedirs(OUTPUT_DIR)

    train_df.to_csv(f'{OUTPUT_DIR}/train.csv', index=False)
    test_df.to_csv(f'{OUTPUT_DIR}/test.csv', index=False)
    print("Gotowe. Pliki w folderze processed.")


if __name__ == "__main__":
    main()