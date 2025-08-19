import pandas as pd

# Caminho do arquivo original (ajuste se estiver em outro local)
caminho_arquivo = 'CDR_04Aug2025.csv'

# Leitura do arquivo
df = pd.read_csv(caminho_arquivo)

# Seleção das colunas de interesse
colunas_uteis = [
    'PTID', 'VISCODE', 'VISDATE',
    'CDMEMORY', 'CDORIENT', 'CDJUDGE', 'CDCOMMUN',
    'CDHOME', 'CDCARE', 'CDGLOBAL', 'CDRSB'
]
df = df[colunas_uteis]

# Remove linhas com valores nulos em colunas críticas
df = df.dropna(subset=['CDMEMORY', 'CDORIENT', 'CDJUDGE', 'CDGLOBAL'])

# Resetar o índice
df = df.reset_index(drop=True)

# Exportar para novo CSV limpo
df.to_csv('CDR_preprocessado.csv', index=False)

print("Pré-processamento completo. Arquivo salvo como 'CDR_preprocessado.csv'.")
