# Moduł AI: Diagnoza Chorób na Podstawie Objawów

Ten katalog zawiera kod źródłowy, skrypty trenujące oraz modele uczenia maszynowego (ML/DL) wykorzystywane w pracy licencjackiej.

Celem projektu jest porównanie skuteczności **klasycznych algorytmów** (opartych na słowach kluczowych) z **zaawansowanymi modelami językowymi** (Transformers), które rozumieją kontekst wypowiedzi pacjenta.

---

## 1. Źródło Danych

W projekcie wykorzystano zbiór danych zawierający naturalne wypowiedzi pacjentów:
* **Nazwa zbioru:** [Symptom2Disease](https://www.kaggle.com/datasets/niyarrbarman/symptom2disease)
* **Charakterystyka:** Zbiór zawiera 1200 wpisów tekstowych przypisanych do 24 różnych jednostek chorobowych.
* **Lokalizacja pliku:** `data/raw/Symptom2Disease.csv`

### Przetwarzanie danych (Preprocessing)
Skrypt `01_prepare_s2d.py` wykonuje:
1.  Czyszczenie danych i standaryzację nazw kolumn (`text`, `label`).
2.  Podział na zbiór treningowy (**80%**) i testowy (**20%**) z zachowaniem proporcji klas (stratyfikacja).
3.  Zapis przetworzonych plików do `data/processed/`.

---

## 2. Metodologia Badawcza

Projekt porównuje dwa podejścia do diagnozy:

### Podejście A: Klasyczne (Symulacja "Checkboxów")
Modele te nie rozumieją języka naturalnego. Tekst pacjenta jest przepuszczany przez **Parser (Bag-of-Words)**, który zamienia zdanie na wektor binarny (0/1).
* **Mechanizm:** `CountVectorizer` (binary=True).
* **Interpretacja:** Model widzi tylko, czy dane słowo (objaw) wystąpiło, ignorując kontekst, negacje ("nie mam gorączki") i kolejność słów.
* **Cel:** Symulacja klasycznej aplikacji medycznej, gdzie użytkownik zaznacza objawy z listy.

### Podejście B: Nowoczesne (Deep Learning / NLP)
Wykorzystanie sieci neuronowych typu **Transformer**, które analizują całe zdanie jako sekwencję.
* **Mechanizm:** Tokenizacja i Embeddings.
* **Interpretacja:** Model rozumie kontekst, synonimy (np. "puking" ≈ "vomiting") oraz gramatykę.
* **Cel:** Stworzenie inteligentnego asystenta, któremu można opisać problem własnymi słowami.

---

## 3. Zastosowane Modele

### Grupa 1: Modele Klasyczne
1.  **Random Forest (Las Losowy):** Zespół drzew decyzyjnych. Odporny na overfitting.
2.  **KNN (K-Najbliższych Sąsiadów):** Klasyfikacja na podstawie podobieństwa do innych pacjentów.
3.  **SVM (Support Vector Machine):** Jądro liniowe. Model szukający optymalnej granicy (hiperpłaszczyzny) między chorobami w przestrzeni cech.

### Grupa 2: Modele Językowe (Transformers)
1.  **DistilBERT (`distilbert-base-uncased`):** Lżejsza, szybsza wersja BERTa (o 40% mniej parametrów).
2.  **BioBERT (`dmis-lab/biobert-v1.1`):** Model BERT dotrenowany na milionach artykułów biomedycznych (PubMed). Specjalista w dziedzinie medycyny.
3.  **RoBERTa (`roberta-base`):** Ulepszona wersja BERTa trenowana na większym korpusie danych.

