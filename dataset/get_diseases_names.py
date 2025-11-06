import pandas as pd

df = pd.read_csv("merged_dataset.csv")

if "prognosis" not in df.columns:
    raise ValueError("Didn't found collumn 'prognosis' in dataset")

diseases = sorted(df["prognosis"].unique())

print(f"found {len(diseases)} unique diseases.")

with open("disease_list.txt", "w") as f:
    for d in diseases:
        f.write(d + "\n")

print("💾 disease_list.txt")
