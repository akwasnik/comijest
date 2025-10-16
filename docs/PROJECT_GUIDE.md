# 🧭 Project Guide — comijest.pl

Dokument opisujący zasady pracy zespołu, organizację repozytorium, strukturę branchy oraz dobre praktyki w projekcie **comijest.pl**.

## 🌿 1. Git workflow

Używamy uproszczonego modelu **Git Flow**:

### 🔹 Główne branche
| Branch | Cel |
|--------|------|
| `main` | stabilna, produkcyjna wersja projektu |
| `dev` | bieżący rozwój i integracja feature’ów |

### 🔹 Feature branche
Każdy nowy element tworzymy na osobnej gałęzi w formacie:

```
feature/<nazwa-funkcji>
```

Przykłady:
```
feature/backend-login
feature/frontend-symptom-form
feature/ml-model-v1
```

---

## 🔄 2. Zasady pracy z Gitem

1. **Nie pracujemy bezpośrednio na `main` ani `dev`.**  
   Wszystkie zmiany robimy na branchach `feature/...`.

2. **Po ukończeniu zadania:**
   - Tworzymy **Pull Request (PR)** → z `feature/...` do `dev`.

3. **Po akceptacji PR:**
   - Merge `feature/...` → `dev` (squash lub merge commit).
   - CI (testy) powinny przejść automatycznie.

4. **Po przetestowaniu wersji developerskiej:**
   - Merge `dev` → `main`  
   - To oznacza *stabilne wydanie projektu* (np. `v0.1.0`).

---

## 🧱 3. Konwencje commitów

- Zawarta jest w docs/commits_guide.md

---

## 🧠 4. Zasady pracy z backendem

- W katalogu `backend/.env` trzymaj klucze, tokeny i sekrety:
  ```
  API_KEY=...
  MODEL_PATH=ml/model.pkl
  DATABASE_URL=...
  ```
- **Nigdy nie commituj pliku `.env` do repozytorium.**
  - Jeśli potrzebujesz udostępnić wartości innym członkom zespołu, zrób to przez osobny dokument `.env.example` (bez prawdziwych kluczy).

---

## 🧩 5. CI/CD i testy

- Każdy push do `dev` lub `main` uruchamia **GitHub Actions** (CI).
- CI sprawdza:
  - Czy backend i frontend się budują,
  - Czy testy przechodzą bez błędów.
- Deploy do środowiska testowego lub produkcyjnego wykonujemy dopiero po merge `dev` → `main`.

---

## 🧰 6. Dobre praktyki zespołowe

✅ **PR’y nie mogą być ogromne.**  
Zmieniaj jedną rzecz naraz – łatwiejsze review.

✅ **Każdy PR wymaga opisu.**  
Krótko: co zostało zmienione i dlaczego.

✅ **Review jest obowiązkowe.**  
Co najmniej jedna osoba musi zaakceptować PR.

✅ **Nie commituj plików builda.**  
(np. `node_modules/`, `.next/`, `__pycache__/`, `venv/`)

✅ **Dokumentuj API i model AI.**  
Aktualizuj `docs/api_endpoints.md` i `docs/model_description.md` przy każdej zmianie.

---

## 🔒 7. Zasady bezpieczeństwa

- Nigdy nie commituj sekretów, tokenów, danych użytkowników.
- Używaj `.env` + `python-dotenv` / `next.config.js` do ładowania kluczy.
- Jeśli korzystasz z zewnętrznych API, ogranicz klucze tylko do potrzebnych uprawnień.
- Regularnie aktualizuj zależności (`pip install --upgrade` / `npm audit`).

---

## 📞 8. Komunikacja i organizacja

- Komunikacja zespołu: Discord

---

## ✨ 9. Podsumowanie

**Zasada główna:**  
> „Małe, czytelne zmiany — testowane, opisane i przemyślane.”

Ten projekt ma być nie tylko działającą aplikacją, ale też **pokazem dobrej organizacji zespołu developerskiego**.

---

🧑‍💻 **Autorzy:** 
  ### wstępnie :
- Adrian Kwaśnik — Frontend / koordynacja projektu  
- Maksymilian Janica — Backend (Flask)  
- Arek Lorek — AI / ML Model  
