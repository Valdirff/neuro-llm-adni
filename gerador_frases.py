import csv
import random

# Campos clínicos e mapeamentos semânticos
cdr_fields = {
    "CDMEMORY": "Memory",
    "CDORIENT": "Orientation",
    "CDJUDGE": "Judgment",
    "CDCOMMUN": "Communication",
    "CDHOME": "Home and hobbies",
    "CDCARE": "Self-care"
}

# Frases variadas para os scores clínicos
status_map = {
    0.0: [
        "is preserved", "has no impairment", "remains intact", "is within normal limits",
        "is fully functional", "shows no decline", "is unimpaired", "presents as normal",
        "functions normally", "appears unaffected", "operates as expected"
    ],
    0.5: [
        "shows questionable impairment", "may have slight difficulty", "is borderline impaired",
        "exhibits mild uncertainty", "shows subtle signs of decline", "demonstrates early issues",
        "shows minor alterations", "presents possible concerns", "may indicate emerging changes",
        "reveals slight deviations", "suggests marginal impairment"
    ],
    1.0: [
        "has mild impairment", "shows definite decline", "has noticeable issues",
        "demonstrates minor functional loss", "presents clear initial deficits",
        "exhibits early-stage impairment", "functions below optimal level",
        "shows consistent minor deterioration", "indicates early cognitive disruption"
    ],
    2.0: [
        "has moderate impairment", "is clearly impaired", "shows considerable decline",
        "exhibits consistent dysfunction", "demonstrates moderate deficits",
        "shows degradation in function", "presents noticeable cognitive loss",
        "indicates substantial deterioration", "functions with limitations"
    ],
    3.0: [
        "has severe impairment", "is profoundly impaired", "has critical dysfunction",
        "shows advanced degeneration", "presents extreme cognitive loss",
        "reveals marked deficits", "functions with major restrictions",
        "is severely compromised", "is functionally incapacitated"
    ]
}

# Introdutores diversos (início de frase)
intro_phrases = [
    "Regarding {label}, the patient",
    "In terms of {label}, the subject",
    "Evaluation shows that {label}",
    "{label} performance",
    "{label} function",
    "Clinically, {label}",
    "From a clinical standpoint, {label}",
    "The assessment of {label} reveals that it",
    "{label} domain appears to",
    "The subject's {label} seems to",
    "In this evaluation, {label}",
    "Observed data indicate that {label}",
    "Based on the current evaluation, {label}",
    "When analyzing {label}, the clinician noted that it",
    "{label} has been examined and it",
    "Functional testing on {label} suggests that it"
]

# Finalizadores diversos (conclusão da frase)
concluding_phrases = [
    "is {status}.",
    "has been identified to be {status}.",
    "is currently assessed as {status}.",
    "has shown to be {status}.",
    "can be described as {status}.",
    "is overall {status}, based on symptoms.",
    "is functionally considered to be {status}.",
    "was evaluated and deemed {status}.",
    "reveals signs of being {status}.",
    "demonstrates a status of {status}.",
    "presents clear evidence of being {status}.",
    "continues to be {status}, as observed.",
    "is believed to be {status}, with moderate confidence.",
    "is aligned with prior scores indicating it {status}.",
    "is rated in the current session as {status}.",
    "remains {status} according to longitudinal evaluation.",
    "was reviewed independently and marked as {status}.",
    "has consistently been {status} throughout visits."
]

def generate_report(data_row: dict) -> str:
    fields = list(cdr_fields.items())
    random.shuffle(fields)  # Varia a ordem dos sintomas

    phrases = []
    for code, label in fields:
        value = data_row.get(code)
        if value in status_map:
            status = random.choice(status_map[value])
            intro = random.choice(intro_phrases).format(label=label)
            conclusion = random.choice(concluding_phrases).format(status=status)
            sentence = f"{intro} {conclusion}"
            phrases.append(sentence)

    cdrsb = data_row.get("CDRSB")
    if cdrsb is not None:
        # Alternar a forma de apresentar a soma
        sum_phrases = [
            f"The CDR-Sum-of-Boxes is {cdrsb}.",
            f"A total CDR-SB score of {cdrsb} was recorded.",
            f"Summing all domains, the CDRSB equals {cdrsb}.",
            f"This results in a CDR Sum-of-Boxes score of {cdrsb}.",
            f"Total score (CDRSB): {cdrsb}.",
            f"The composite score, known as CDRSB, amounts to {cdrsb}.",
            f"The overall clinical rating (CDRSB) is {cdrsb}.",
            f"The calculated CDR-SB is {cdrsb}.",
            f"The summed value across all dimensions is {cdrsb}.",
            f"The subject obtained a cumulative CDRSB of {cdrsb}.",
            f"Final CDR-Sum-of-Boxes outcome: {cdrsb}.",
            f"The comprehensive total of the CDR boxes is {cdrsb}.",
            f"Upon evaluation, the CDRSB was determined to be {cdrsb}.",
            f"The overall dementia rating sums to {cdrsb}.",
            f"A cumulative functional impairment score of {cdrsb} was derived."
]
        phrases.append(random.choice(sum_phrases))

    return " ".join(phrases)

def generate_dataset(n_samples=2000, output_file="cdr_dataset_for_llm.csv"):
    with open(output_file, mode="w", newline='', encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["input", "output"])  # Cabeçalho

        for _ in range(n_samples):
            # Gera valores clínicos plausíveis
            data = {field: random.choice(list(status_map.keys())) for field in cdr_fields}
            data["CDRSB"] = round(sum(data.values()), 1)  # Soma total, com 1 casa decimal

            # Input numérico estruturado
            input_string = " ".join([f"{k}: {v}" for k, v in data.items()])
            # Output textual variado
            output_sentence = generate_report(data)

            writer.writerow([input_string, output_sentence])

# Executar
generate_dataset()
