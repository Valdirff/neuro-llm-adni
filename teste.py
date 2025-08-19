import torch
from transformers import T5Tokenizer, T5ForConditionalGeneration

# Caminhos dos arquivos salvos
checkpoint_dir = r"C:\Valdir\t5_finetuned_cdr_5000"

# Carregar tokenizer e modelo
tokenizer = T5Tokenizer.from_pretrained(checkpoint_dir)
model = T5ForConditionalGeneration.from_pretrained(checkpoint_dir)

# Usar GPU se disponível
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model = model.to(device)

# === Inputs de teste ===
# Substitua ou expanda essa lista conforme necessário
# === Inputs de teste ===
inputs = [
    "CDR global score: 2.0; Memory: 2; Orientation: 2; Judgment: 2; Community: 2; Home: 2; Personal Care: 2",
    "CDR global score: 0.5; Memory: 0; Orientation: 1; Judgment: 0; Community: 1; Home: 0; Personal Care: 0",
    "CDR global score: 1.0; Memory: 2; Orientation: 1; Judgment: 1; Community: 1; Home: 1; Personal Care: 0",
    "CDR global score: 0.0; Memory: 0; Orientation: 0; Judgment: 0; Community: 0; Home: 0; Personal Care: 0",
    "CDR global score: 0.5; Memory: 1; Orientation: 0; Judgment: 0; Community: 0.5; Home: 0; Personal Care: 0",
    "CDR global score: 1.0; Memory: 1; Orientation: 1; Judgment: 2; Community: 1; Home: 2; Personal Care: 1",
    "CDR global score: 2.0; Memory: 3; Orientation: 3; Judgment: 3; Community: 3; Home: 3; Personal Care: 3"
]

# Tokenizar
encodings = tokenizer(inputs, padding=True, truncation=True, return_tensors="pt").to(device)

# Gerar predições
with torch.no_grad():
    generated_ids = model.generate(
        input_ids=encodings["input_ids"],
        attention_mask=encodings["attention_mask"],
        max_length=128,
        num_beams=4,
        early_stopping=True,
    )

# Decodificar
predictions = tokenizer.batch_decode(generated_ids, skip_special_tokens=True)

# Mostrar os resultados
for i, (inp, pred) in enumerate(zip(inputs, predictions)):
    print(f"\n🧠 Entrada {i+1}: {inp}")
    print(f"📝 Predição: {pred}")
