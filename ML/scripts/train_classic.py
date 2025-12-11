import pandas as pd
import joblib
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score


def main():
    print("--- 2. TRENING MODELI KLASYCZNYCH (KROK PO KROKU) ---")

    # ==========================================
    # KROK 1: WCZYTANIE DANYCH
    # ==========================================
    try:
        train_df = pd.read_csv('../data/processed/train.csv')
        test_df = pd.read_csv('../data/processed/test.csv')
    except FileNotFoundError:
        print("BŁĄD: Brak plików w folderze data/processed.")
        return

    X_train_text = train_df['text']
    y_train = train_df['label']
    X_test_text = test_df['text']
    y_test = test_df['label']

    print(f"Dane wczytane. Treningowych: {len(X_train_text)}, Testowych: {len(X_test_text)}")

    # ==========================================
    # KROK 2: TWORZENIE TABELI Z TEKSTU (VECTORIZER)
    # ==========================================
    print("\n[INFO] Rozpoczynam wektoryzację (zamianę słów na kolumny)...")

    # Tworzymy obiekt tłumacza (Parsera)
    # binary=True -> Interesuje nas tylko czy objaw wystąpił (0 lub 1)
    vectorizer = CountVectorizer(stop_words='english', binary=True, max_features=500)

    # A. UCZYMY SIĘ SŁOWNIKA na danych treningowych
    # fit -> naucz się jakie słowa istnieją
    # transform -> zamień tekst na liczby
    X_train_vec = vectorizer.fit_transform(X_train_text)

    # B. TYLKO ZAMIENIAMY dane testowe (używając słownika z A)
    # UWAGA: Tutaj robimy tylko transform! Nie wolno robić fit na teście!
    X_test_vec = vectorizer.transform(X_test_text)

    print(f"Wektoryzacja zakończona.")
    print(f"Wymiary tabeli treningowej: {X_train_vec.shape} (Wiersze, Kolumny-Słowa)")

    # Zapisujemy sam Vectorizer (żeby aplikacja mogła tłumaczyć tekst usera)
    joblib.dump(vectorizer, '../models/classic_vectorizer.pkl')
    print("Zapisano: classic_vectorizer.pkl")

    # ==========================================
    # KROK 3: TRENOWANIE MODELI NA LICZBACH
    # ==========================================
    models = {
        "Random Forest": RandomForestClassifier(n_estimators=100, random_state=42),
        "KNN": KNeighborsClassifier(n_neighbors=5),
        "SVM": SVC(kernel='linear', random_state=42)
    }

    results = {}

    print("\n[INFO] Rozpoczynam trening modeli...")

    for name, model in models.items():
        print(f"--> Trenuję model: {name}")

        # A. TRENING (Model dostaje macierz liczb X_train_vec i odpowiedzi y_train)
        model.fit(X_train_vec, y_train)

        # B. TESTOWANIE (Model dostaje macierz liczb X_test_vec)
        preds = model.predict(X_test_vec)

        # C. OCENA
        acc = accuracy_score(y_test, preds)
        results[name] = acc
        print(f"    Skuteczność: {acc:.4f}")

        # Zapisujemy sam model (bez vectorizera)
        filename = f'../models/model_{name.replace(" ", "_")}.pkl'
        joblib.dump(model, filename)

    joblib.dump(results, '../reports/classic_results.pkl')

    # ==========================================
    # KROK 4: WIZUALIZACJA (JAK TO DZIAŁA?)
    # ==========================================
    print("\n" + "=" * 50)
    print("JAK KOMPUTER WIDZI TEKST? (PODGLĄD)")
    print("=" * 50)

    sample_text = ["I have severe skin rash and high fever"]
    print(f"Tekst pacjenta: '{sample_text[0]}'")

    # 1. Używamy vectorizera (już nauczonego), żeby zamienić to na liczby
    vectorized_sample = vectorizer.transform(sample_text).toarray()

    # 2. Pobieramy nazwy kolumn
    feature_names = vectorizer.get_feature_names_out()

    # 3. Tworzymy ładną tabelkę do wyświetlenia
    df_view = pd.DataFrame(vectorized_sample, columns=feature_names)

    # Wyciągamy tylko te kolumny, gdzie jest 1 (żeby pokazać co wykrył)
    detected = df_view.loc[:, (df_view != 0).any(axis=0)]

    print("\nModel widzi to jako tabelę z jedynkami w tych miejscach:")
    print(detected)
    print("\n(Wszystkie inne słowa, np. 'severe', 'have', 'and' zostały zignorowane lub uznane za nieistotne)")


if __name__ == "__main__":
    main()