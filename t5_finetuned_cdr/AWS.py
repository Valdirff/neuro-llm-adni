from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

# Caminho do seu modelo treinado (troque pelo nome da sua pasta local do modelo)
local_model = r"C:\Valdir\t5_finetuned_cdr"

# Carregar modelo e tokenizer
model = AutoModelForSeq2SeqLM.from_pretrained(local_model)
tokenizer = AutoTokenizer.from_pretrained(local_model)

# Exportar em formato HuggingFace
export_dir = "./model_export"
model.save_pretrained(export_dir)
tokenizer.save_pretrained(export_dir)

print(f"✅ Modelo exportado para: {export_dir}")
