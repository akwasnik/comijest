import pandas as pd
from rapidfuzz import process, fuzz

df_train = pd.read_csv("dataset_1/Training.csv")
df_dataset = pd.read_csv("dataset_2/dataset.csv")
        

print("✅ Wczytano:")
print("Training:", df_train.shape)
print("Dataset:", df_dataset.shape)

# === Normalize collumns names ===
df_train.columns = [c.strip().lower().replace(" ", "_") for c in df_train.columns]
df_dataset.columns = [c.strip().lower().replace(" ", "_") for c in df_dataset.columns]
df_dataset = df_dataset.rename(columns={"disease": "prognosis"})

# === Identify collumns with symptoms ===
symptom_columns_train = [c for c in df_train.columns if c != "prognosis"]
symptom_cols_dataset = [c for c in df_dataset.columns if "symptom" in c]

# === normalize symtopms names ===
def normalize_symptom(s):
    return s.strip().lower().replace(" ", "_").replace("-", "_")

df_dataset[symptom_cols_dataset] = df_dataset[symptom_cols_dataset].fillna("").applymap(normalize_symptom)

ml_symptom_set = set(symptom_columns_train)

def match_symptom(symptom):
    if not symptom:
        return None
    if symptom in ml_symptom_set:
        return symptom
    match, score, _ = process.extractOne(symptom, ml_symptom_set, scorer=fuzz.partial_ratio)
    return match if score > 80 else None

# === create binaray dataframe for dataset.csv ===
df_dataset_encoded = pd.DataFrame(0, index=df_dataset.index, columns=symptom_columns_train)
for i, row in df_dataset.iterrows():
    for col in symptom_cols_dataset:
        symp = row[col]
        matched = match_symptom(symp)
        if matched:
            df_dataset_encoded.at[i, matched] = 1
df_dataset_encoded["prognosis"] = df_dataset["prognosis"]

# === Merge datasets ===
merged_df = pd.concat([df_train, df_dataset_encoded], axis=0, ignore_index=True)
merged_df = merged_df.loc[:, ~merged_df.columns.str.contains('^Unnamed')]
# merged_df = merged_df.drop_duplicates(subset=["prognosis"], keep="first")

merged_df.to_csv("merged_dataset.csv", index=False)
print("💾 Saved as merged_dataset.csv")
