import pandas as pd

# Caminho para o arquivo CSV gerado
csv_path = "cdr_dataset_for_llm_5000.csv"  # altere o caminho se necessário

# Carrega o dataset
df = pd.read_csv(csv_path)

# Conta as ocorrências de cada frase na coluna 'output'
duplicates = df['output'].value_counts()
repeated_phrases = duplicates[duplicates > 1]

# Exibe frases repetidas com o número de vezes que aparecem
repeated_df = repeated_phrases.reset_index()
repeated_df.columns = ['repeated_phrase', 'count']

# Exibe ou salva
if repeated_df.empty:
    print("✔ Nenhuma frase repetida encontrada.")
else:
    print("❗ Frases repetidas detectadas:")
    print(repeated_df)
    # repeated_df.to_csv("repeated_phrases.csv", index=False)
