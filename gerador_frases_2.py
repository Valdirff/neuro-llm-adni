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

status_map = {
    0.0: [
        "is preserved", "has no impairment", "remains intact", "is within normal limits",
        "is fully functional", "shows no decline", "is unimpaired", "presents as normal",
        "functions normally", "appears unaffected", "operates as expected",
        "demonstrates baseline functioning", "is operating at standard capacity",
        "is not compromised", "remains unimpaired by clinical standards",
        "is functionally sound", "reflects no abnormality", "exhibits normal behavior",
        "meets age-appropriate expectations", "presents no evidence of dysfunction",
        "is indistinguishable from healthy control", "remains fully preserved",
        "performs within expected cognitive parameters", "retains full integrity",
        "maintains optimal status", "remains clinically stable", "shows no signs of disruption",
        "functions at optimal level", "does not deviate from healthy baseline"
    ],

    0.5: [
        "shows questionable impairment", "may have slight difficulty", "is borderline impaired",
        "exhibits mild uncertainty", "shows subtle signs of decline", "demonstrates early issues",
        "shows minor alterations", "presents possible concerns", "may indicate emerging changes",
        "reveals slight deviations", "suggests marginal impairment",
        "falls near the lower end of normal", "presents early-stage anomalies",
        "exhibits signs that may warrant monitoring", "may reflect a transitional phase",
        "functions with occasional lapses", "has moments of subtle disruption",
        "operates near the threshold of impairment", "is slightly off baseline",
        "demonstrates mild inconsistencies", "may reflect subclinical symptoms",
        "presents borderline clinical relevance", "may signal prodromal state",
        "shows hints of incipient dysfunction", "indicates potential early involvement"
    ],

    1.0: [
        "has mild impairment", "shows definite decline", "has noticeable issues",
        "demonstrates minor functional loss", "presents clear initial deficits",
        "exhibits early-stage impairment", "functions below optimal level",
        "shows consistent minor deterioration", "indicates early cognitive disruption",
        "is moderately compromised", "presents stable mild deficits",
        "demonstrates functional weakening", "reveals discernible signs of decline",
        "has entered mild dysfunction phase", "functions with reduced reliability",
        "experiences difficulty in daily tasks", "shows measurable change from baseline",
        "displays early clinical manifestations", "presents with low-grade impairment",
        "aligns with mild neurocognitive disorder criteria", "is modestly impacted",
        "reflects disruption in limited domains", "reveals impairments in selective functions",
        "retains partial function with mild challenges", "functions with observable reduction"
    ],

    2.0: [
        "has moderate impairment", "is clearly impaired", "shows considerable decline",
        "exhibits consistent dysfunction", "demonstrates moderate deficits",
        "shows degradation in function", "presents noticeable cognitive loss",
        "indicates substantial deterioration", "functions with limitations",
        "is impacted across multiple domains", "has widespread disruption",
        "demonstrates substantial functional compromise", "shows mid-stage impairment",
        "requires assistance in complex tasks", "has declining cognitive efficiency",
        "exhibits impaired capacity in various settings", "presents progressive symptomatology",
        "shows structured and measurable losses", "functions below independence threshold",
        "suffers from moderate neurodegeneration", "presents multidimensional dysfunction",
        "has compromised autonomy", "struggles with executive and memory tasks",
        "displays significant but non-total loss", "operates with reduced cognitive resilience"
    ],

    3.0: [
        "has severe impairment", "is profoundly impaired", "has critical dysfunction",
        "shows advanced degeneration", "presents extreme cognitive loss",
        "reveals marked deficits", "functions with major restrictions",
        "is severely compromised", "is functionally incapacitated",
        "shows global deterioration", "has near-total loss of function",
        "exhibits terminal-stage decline", "presents end-stage symptoms",
        "displays pervasive deficits", "operates under severe limitations",
        "has lost essential cognitive functions", "is dependent for most activities",
        "shows unremitting cognitive failure", "has entered advanced disease phase",
        "suffers from irreversible decline", "presents full-blown dementia",
        "demonstrates structural and functional collapse", "fails to meet basic cognitive demands",
        "is unable to perform autonomously", "exhibits complete neurocognitive breakdown"
    ]
}


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
    "Functional testing on {label} suggests that it",
    "Clinical records show that {label}",
    "Based on neuropsychological observations, {label}",
    "Initial evaluation of {label} indicates that it",
    "{label} was assessed and found to",
    "Ongoing monitoring of {label} demonstrates that it",
    "According to the patient’s file, {label}",
    "Clinician reports describe {label} as",
    "Interviews and tests suggest that {label}",
    "Patient feedback indicates that {label}",
    "Cognitive testing results show that {label}",
    "Upon review of the case, {label} appears to",
    "A review of patient history highlights that {label}",
    "Diagnostic tools reveal that {label}",
    "Clinical judgement suggests {label}",
    "During assessment, {label} was observed to",
    "Test outcomes suggest a trend in {label}",
    "When questioned, the patient’s {label}",
    "Medical history documents that {label}",
    "Performance on {label} tasks reflects that it",
    "Throughout the session, {label} was noted to",
    "Professional evaluation revealed {label} to",
    "Neurocognitive review indicates that {label}",
    "During clinical interview, {label} emerged as a concern",
    "Healthcare notes state that {label}",
    "Functional capacity in {label} has been described as",
    "Based on cumulative assessment, {label}",
    "The examination pointed out that {label}",
    "Upon closer analysis, {label} was found to",
    "Neurobehavioral testing identified that {label}"
]


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
    "has consistently been {status} throughout visits.",
    "is documented as {status} in the patient record.",
    "has been repeatedly classified as {status} in past evaluations.",
    "is interpreted clinically as {status}.",
    "has been recognized by the examiner as {status}.",
    "falls within the spectrum of being {status}.",
    "shows clinical alignment with the profile of {status}.",
    "meets criteria for being considered {status}.",
    "displays characteristics consistent with being {status}.",
    "has a clinical manifestation typical of {status}.",
    "correlates with functional patterns seen in {status} cases.",
    "is coded diagnostically as {status}.",
    "was found to be {status} through cumulative assessment.",
    "is understood within the clinical context to be {status}.",
    "was consistently identified as {status} in multidisciplinary review.",
    "has been confirmed as {status} upon further analysis.",
    "exhibited performance traits aligned with being {status}.",
    "is best classified at this stage as {status}.",
    "may be conservatively described as {status}.",
    "is characterized functionally and cognitively as {status}.",
    "has been determined to fall into the category of {status}.",
    "conforms to clinical expectations of a {status} profile.",
    "has presented a trajectory consistent with being {status}.",
    "was verified through multiple modalities as {status}."
]


def generate_report(data_row: dict) -> str:
    fields = list(cdr_fields.items())
    random.shuffle(fields)

    phrases = []
    for code, label in fields:
        value = data_row.get(code)
        if value in status_map:
            status = random.choice(status_map[value])
            intro = random.choice(intro_phrases).format(label=label)
            conclusion = random.choice(concluding_phrases).format(status=status)
            phrases.append(f"{intro} {conclusion}")

    cdrsb = data_row.get("CDRSB")
    if cdrsb is not None:
        cdrsb_phrases = [
            f"The CDR-Sum-of-Boxes is {cdrsb}.", f"A total CDR-SB score of {cdrsb} was recorded.",
            f"Summing all domains, the CDRSB equals {cdrsb}.", f"This results in a CDR Sum-of-Boxes score of {cdrsb}.",
            f"Total score (CDRSB): {cdrsb}.", f"The composite score, known as CDRSB, amounts to {cdrsb}.",
            f"The overall clinical rating (CDRSB) is {cdrsb}.", f"The calculated CDR-SB is {cdrsb}.",
            f"The summed value across all dimensions is {cdrsb}.",
            f"The subject obtained a cumulative CDRSB of {cdrsb}.",
            f"Final CDR-Sum-of-Boxes outcome: {cdrsb}.",
            f"The comprehensive total of the CDR boxes is {cdrsb}.",
            f"Upon evaluation, the CDRSB was determined to be {cdrsb}.",
            f"The overall dementia rating sums to {cdrsb}.",
            f"A cumulative functional impairment score of {cdrsb} was derived."
            f"Clinical evaluation concluded with a CDRSB of {cdrsb}.",
            f"The consolidated CDR sum is {cdrsb}.",
            f"The functional impairment summary yields a value of {cdrsb}.",
            f"Based on the patient's performance, CDRSB was calculated as {cdrsb}.",
            f"Total impairment index (CDRSB) is recorded as {cdrsb}.",
            f"Final multidomain score (CDRSB) stands at {cdrsb}.",
            f"The clinician-assessed CDR-SB score reached {cdrsb}.",
            f"The patient's domain score aggregation totals {cdrsb}.",
            f"Longitudinal evaluation points to a current CDRSB of {cdrsb}.",
            f"Evidence supports a summed box score of {cdrsb}.",
            f"CDRSB score, integrating all functional aspects, is {cdrsb}.",
            f"The final box total (CDR-SB) confirms a score of {cdrsb}.",
            f"After full scoring, the CDR Sum-of-Boxes reached {cdrsb}.",
            f"This patient achieved a global CDR-SB of {cdrsb}.",
            f"The scoring tool yielded a total of {cdrsb} on the CDR-SB scale.",
            f"The quantitative clinical summary (CDRSB) is valued at {cdrsb}.",
            f"Total CDR sum, reflecting functional and cognitive loss, is {cdrsb}.",
            f"All domains considered, the subject's score was {cdrsb}."
        ]
        phrases.append(random.choice(cdrsb_phrases))

    return " ".join(phrases)

# Caminhos de entrada e saída
INPUT_FILE = "cdr_dataset_balanceado_5000.csv"
OUTPUT_FILE = "cdr_dataset_for_llm_5000.csv"

# Geração final com frases
with open(INPUT_FILE, newline='', encoding="utf-8") as infile, \
     open(OUTPUT_FILE, mode="w", newline='', encoding="utf-8") as outfile:

    reader = csv.DictReader(infile)
    writer = csv.writer(outfile)
    writer.writerow(["input", "output"])  # cabeçalho

    for row in reader:
        input_str = " ".join([f"{k}: {row[k]}" for k in row])
        row_as_float = {}
        for k in row:
            try:
                row_as_float[k] = float(row[k])
            except (ValueError, TypeError):
                continue  # pula qualquer campo que esteja vazio ou inválido
            
        output_str = generate_report(row_as_float)
        writer.writerow([input_str, output_str])

print(f"✅ Arquivo final com frases geradas: {OUTPUT_FILE}")
