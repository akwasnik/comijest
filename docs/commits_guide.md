✅ Każdy commit mówi co zrobił

## type(scope):opis


feat(frontend): add symptom input form
fix(backend): handle empty request body in /predict
refactor(ml): clean up model loading logic
docs(api): update /predict endpoint description

| Typ          | Znaczenie                                             | Przykład                                       |
| ------------ | ----------------------------------------------------- | ---------------------------------------------- |
| **feat**     | nowa funkcjonalność                                   | `feat(backend): add /predict endpoint`         |
| **fix**      | poprawka błędu                                        | `fix(frontend): crash on missing symptoms`     |
| **refactor** | zmiana struktury kodu bez zmiany funkcji              | `refactor(ai): simplify preprocessing`         |
| **chore**    | zmiana niezwiązana z kodem logiki (np. config, CI/CD) | `chore(ci): add build workflow`                |
| **docs**     | zmiany w dokumentacji                                 | `docs(readme): add setup guide`                |
| **style**    | poprawki formatowania, linting, brak wpływu na logikę | `style(frontend): fix eslint warnings`         |
| **test**     | dodanie / modyfikacja testów                          | `test(backend): add tests for /predict`        |
| **perf**     | poprawa wydajności                                    | `perf(ai): reduce model load time`             |
| **build**    | zmiany w procesie buildowania (webpack, vite, docker) | `build(docker): optimize backend image`        |
| **ci**       | zmiany w pipeline’ach CI/CD                           | `ci(actions): trigger deploy on main push`     |
| **revert**   | cofnięcie wcześniejszego commita                      | `revert: feat(backend): add /predict endpoint` |
| **merge**    | merge branchy (używa się automatycznie przy PR)       | `merge: feature/ai-model into dev`             |
| **deps**     | aktualizacja zależności                               | `deps(frontend): update next to 14.1.2`        |
