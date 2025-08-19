import csv
import random
from collections import defaultdict

INPUT_FILE = "CDR_preprocessado.csv"
OUTPUT_FILE = "cdr_dataset_balanceado_5000.csv"
TARGET_SAMPLES = 5000

# Campos relevantes
cdr_fields = ["CDMEMORY", "CDORIENT", "CDJUDGE", "CDCOMMUN", "CDHOME", "CDCARE", "CDRSB"]
group_field = "CDGLOBAL"

# Carregar e agrupar amostras por CDGLOBAL
grouped_rows = defaultdict(list)

with open(INPUT_FILE, newline='', encoding="utf-8") as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        try:
            key = float(row[group_field])
            if key in [0.0, 0.5, 1.0, 2.0, 3.0]:
                grouped_rows[key].append(row)
        except ValueError:
            continue  # Pula se não for float

# Verificar distribuição atual
for k in sorted(grouped_rows):
    print(f"CDGLOBAL {k}: {len(grouped_rows[k])} amostras")

# Número de classes disponíveis
classes = list(grouped_rows.keys())
n_per_class = TARGET_SAMPLES // len(classes)

# Selecionar amostras balanceadas
# Número de classes disponíveis
classes = sorted(grouped_rows.keys())
n_per_class = TARGET_SAMPLES // len(classes)

balanced_data = []

for k in classes:
    samples = grouped_rows[k]
    if len(samples) >= n_per_class:
        # Amostras suficientes, sorteia sem reposição
        balanced_data.extend(random.sample(samples, n_per_class))
    else:
        # Oversampling com reposição
        needed = n_per_class - len(samples)
        print(f"[!] Classe {k} precisa de oversampling: duplicando {needed} amostras.")
        balanced_data.extend(samples)
        balanced_data.extend(random.choices(samples, k=needed))

print(f"\n✅ Total final de amostras balanceadas: {len(balanced_data)}")

with open(OUTPUT_FILE, mode="w", newline='', encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=cdr_fields)
    writer.writeheader()

    for row in balanced_data:
        random.shuffle(balanced_data)
        writer.writerow({k: row[k] for k in cdr_fields})

print(f"✅ CSV gerado com dados numéricos: {OUTPUT_FILE}")
