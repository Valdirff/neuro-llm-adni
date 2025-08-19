from datasets import load_dataset, Dataset
from transformers import T5Tokenizer
import pandas as pd

# Caminho para seu CSV
csv_path = "cdr_dataset_for_llm_5000.csv"

# Carrega CSV com pandas e converte para Dataset do HF
df = pd.read_csv(csv_path)
hf_dataset = Dataset.from_pandas(df)

# Tokenizer do FLAN-T5 Small
tokenizer = T5Tokenizer.from_pretrained("google/flan-t5-small")

# Tokenização
def tokenize_function(example):
    input_enc = tokenizer(example["input"], truncation=True, padding="max_length", max_length=128)
    output_enc = tokenizer(example["output"], truncation=True, padding="max_length", max_length=128)
    input_enc["labels"] = output_enc["input_ids"]
    return input_enc

# Aplica tokenização
tokenized_dataset = hf_dataset.map(tokenize_function, batched=False)

# Salva dataset tokenizado opcionalmente
tokenized_dataset.save_to_disk("cdr_llm_tokenized_5000")

print("✔ Tokenização completa. Dataset pronto para fine-tuning.")
