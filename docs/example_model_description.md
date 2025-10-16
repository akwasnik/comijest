
---

### 📄 `docs/model_description.md`
```markdown
# 🧠 Model AI — comijest.pl

## Cel
Model ma przewidywać najbardziej prawdopodobną diagnozę na podstawie objawów wprowadzonych przez użytkownika.

---

## Dane treningowe
- Źródło: zestawy symptom–disease z publicznych datasetów medycznych
- Rozmiar: ~10 000 przykładów
- Format: JSON / CSV (`symptom`, `diagnosis`)

---

## Architektura modelu
- Wersja 1: klasyfikator SVM (sklearn)
- Wersja 2: sieć neuronowa (TensorFlow / Keras)

---

## Metryki
| Metryka | Wartość |
|----------|----------|
| Accuracy | 0.83 |
| Precision | 0.81 |
| Recall | 0.79 |
| F1-score | 0.80 |

---

## Eksport
Model zapisany jako `model.pkl` (lub `model.h5`).
Ładowany w Flasku przy starcie serwera:
```python
import joblib
model = joblib.load("ml/model.pkl")
