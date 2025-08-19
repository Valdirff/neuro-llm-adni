from transformers import T5ForConditionalGeneration, T5Tokenizer, Trainer, Seq2SeqTrainingArguments
from datasets import load_from_disk
import numpy as np

tokenizer = T5Tokenizer.from_pretrained("google/flan-t5-small")

# 1. Carregar dataset tokenizado
dataset = load_from_disk("Projeto_AWS_LLM_ADNI/cdr_llm_tokenized")

# 2. Carregar o modelo base
model = T5ForConditionalGeneration.from_pretrained("google/flan-t5-small")

# 3. Dividir treino e validação
dataset = dataset.train_test_split(test_size=0.1)

# 4. Argumentos de treinamento
training_args = Seq2SeqTrainingArguments(
    output_dir="./t5_finetuned_cdr",
    per_device_train_batch_size=8,
    per_device_eval_batch_size=8,
    evaluation_strategy="epoch",
    save_strategy="epoch",
    num_train_epochs=5,
    logging_dir="./logs",
    logging_steps=10,
    save_total_limit=2,
    load_best_model_at_end=True,
    predict_with_generate=True
)

def compute_metrics(eval_pred):
    predictions, labels = eval_pred

    # Garantir que predictions está no formato correto
    # Alguns modelos retornam tupla com logits como primeiro elemento
    if isinstance(predictions, tuple):
        predictions = predictions[0]

    # Caso predictions venha com forma (batch_size, seq_len, vocab_size), aplica argmax
    if predictions.ndim == 3:
        predictions = np.argmax(predictions, axis=-1)

    # Corrige os rótulos (-100 → pad_token_id)
    labels = np.where(labels != -100, labels, tokenizer.pad_token_id)

    # Decodifica previsões e rótulos
    decoded_preds = tokenizer.batch_decode(predictions, skip_special_tokens=True)
    decoded_labels = tokenizer.batch_decode(labels, skip_special_tokens=True)

    # Calcula acurácia básica
    accuracy = sum(p.strip() == l.strip() for p, l in zip(decoded_preds, decoded_labels)) / len(decoded_preds)

    return {"accuracy": accuracy}



# 6. Instanciar trainer
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=dataset["train"],
    eval_dataset=dataset["test"],
    tokenizer=tokenizer,
    compute_metrics=compute_metrics
)

# 7. Treinar
trainer.train()
