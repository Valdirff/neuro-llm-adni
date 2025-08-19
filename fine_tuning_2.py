from transformers import T5ForConditionalGeneration, T5Tokenizer, Trainer, Seq2SeqTrainingArguments
from datasets import load_from_disk
import numpy as np
from evaluate import load
rouge = load("rouge")

# Tokenizer e modelo base
tokenizer = T5Tokenizer.from_pretrained("google/flan-t5-small")
model = T5ForConditionalGeneration.from_pretrained("google/flan-t5-small")

# Dataset
dataset = load_from_disk("Projeto_AWS_LLM_ADNI/cdr_llm_tokenized_5000")
dataset = dataset.train_test_split(test_size=0.1, seed=42, shuffle=True)

# Argumentos de treino
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
    predict_with_generate=True,
    generation_max_length=128,
    generation_num_beams=4,
    report_to="none"
)

# Métricas com ROUGE
def compute_metrics(eval_pred):
    predictions, labels = eval_pred
    if isinstance(predictions, tuple):
        predictions = predictions[0]
    if predictions.ndim == 3:
        predictions = np.argmax(predictions, axis=-1)

    labels = np.where(labels != -100, labels, tokenizer.pad_token_id)

    decoded_preds = tokenizer.batch_decode(predictions, skip_special_tokens=True)
    decoded_labels = tokenizer.batch_decode(labels, skip_special_tokens=True)

    result = rouge.compute(predictions=decoded_preds, references=decoded_labels)
    return {k: round(v, 4) for k, v in result.items()}

# Trainer
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=dataset["train"],
    eval_dataset=dataset["test"],
    tokenizer=tokenizer,
    compute_metrics=compute_metrics
)

# Treinar e salvar
trainer.train()
trainer.save_model("t5_finetuned_cdr_5000")
tokenizer.save_pretrained("t5_finetuned_cdr_5000")

# Avaliação final
metrics = trainer.evaluate()
print("Avaliação final:", metrics)
