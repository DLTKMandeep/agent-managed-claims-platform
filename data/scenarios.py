"""Clinical scenarios used to generate synthetic claims.

Each scenario has the correct codes (the answer key) and three versions of the
doctor's note: clear, vague (missing detail), and conflicting (contradicts itself).
"""


def L(code, modifiers=(), units=1):
    return {"code": code, "modifiers": list(modifiers), "units": units}


SCENARIOS = [
    # ---------- primary care ----------
    {"id": "P1", "specialty": "primary_care", "icd10": ["I10", "E78.5"],
     "cpt": [L("99214"), L("80061"), L("36415")],
     "clear": "Follow-up for high blood pressure and high cholesterol. BP 142/90 on current medication. Reviewed diet and dosing in detail. Blood drawn for a cholesterol panel.",
     "vague": "Follow-up visit. Talked about numbers and meds. Labs sent.",
     "conflict": "Follow-up for blood pressure, which is well controlled with no concerns. Increased medication dose because BP remains high. Blood drawn for cholesterol panel."},
    {"id": "P2", "specialty": "primary_care", "icd10": ["E11.9"],
     "cpt": [L("99213"), L("83036"), L("36415")],
     "clear": "Routine check of type 2 diabetes with no complications. Feet and eyes normal. Blood drawn for HbA1c.",
     "vague": "Sugar check. Drew blood.",
     "conflict": "Type 2 diabetes check with no complications. Notes possible early nerve damage in both feet. Blood drawn for HbA1c."},
    {"id": "P3", "specialty": "primary_care", "icd10": ["J02.9"],
     "cpt": [L("99213"), L("87880")],
     "clear": "Sore throat and fever for two days. Tonsils red and swollen. Rapid strep test performed. Diagnosis: throat infection.",
     "vague": "Throat bothering patient. Did a quick test.",
     "conflict": "Sore throat for two days, no fever. Temperature 38.9 C. Rapid strep test performed. Likely viral cold, but treating as throat infection."},
    {"id": "P4", "specialty": "primary_care", "icd10": ["N39.0"],
     "cpt": [L("99213"), L("81002")],
     "clear": "Burning with urination for three days. Urine dipstick positive for infection. Diagnosis: urinary tract infection.",
     "vague": "Bathroom complaints. Checked urine.",
     "conflict": "Burning with urination. Urine dipstick negative. Diagnosis: urinary tract infection confirmed by dipstick."},
    # ---------- cardiology ----------
    {"id": "C1", "specialty": "cardiology", "icd10": ["R07.9"],
     "cpt": [L("99243"), L("93000")],
     "clear": "Specialist consultation for chest pain on exertion, referred by primary care. ECG performed and interpreted: normal sinus rhythm.",
     "vague": "Chest thing. Did a tracing.",
     "conflict": "Consultation for chest pain at rest, only when exercising. ECG performed and interpreted. Rhythm abnormal; rhythm normal on review."},
    {"id": "C2", "specialty": "cardiology", "icd10": ["I48.91"],
     "cpt": [L("99214"), L("93224")],
     "clear": "Atrial fibrillation follow-up. Reviewed medication and bleeding risk in detail. 48-hour heart monitor placed.",
     "vague": "Rhythm follow-up. Monitor on.",
     "conflict": "Atrial fibrillation follow-up; patient has never had an irregular rhythm. 48-hour heart monitor placed."},
    {"id": "C3", "specialty": "cardiology", "icd10": ["I50.9"],
     "cpt": [L("93306"), L("93000")],
     "clear": "Heart failure with worsening ankle swelling. Complete heart ultrasound and ECG performed and interpreted.",
     "vague": "Swelling issue. Imaging done.",
     "conflict": "Heart failure, no swelling. Severe swelling of both ankles noted. Complete heart ultrasound and ECG performed."},
    {"id": "C4", "specialty": "cardiology", "icd10": ["I25.10"],
     "cpt": [L("93015")],
     "clear": "Coronary artery disease without chest pain. Treadmill stress test completed with supervision and report.",
     "vague": "Heart test on the treadmill.",
     "conflict": "Coronary artery disease with frequent angina. Patient denies any chest pain. Treadmill stress test completed."},
    # ---------- orthopedics ----------
    {"id": "O1", "specialty": "orthopedics", "icd10": ["S93.401A"],
     "cpt": [L("99203"), L("73610", ["RT"]), L("29540", ["RT"])],
     "clear": "New patient. Twisted right ankle playing soccer yesterday. Swelling over the outer ligaments, able to bear weight. Right ankle X-ray, 3 views, negative for fracture. Diagnosis: right ankle sprain. Ankle strapped.",
     "vague": "Ankle hurts after a fall. Looked at it, did an X-ray. Taped it.",
     "conflict": "Possible fracture of the right ankle. Right ankle X-ray, 3 views, negative. Assessment: ankle sprain. Ankle strapped."},
    {"id": "O2", "specialty": "orthopedics", "icd10": ["M17.11"],
     "cpt": [L("99213", ["25"]), L("20610", ["RT"]), L("73562", ["RT"])],
     "clear": "Established patient with right knee osteoarthritis. Separate evaluation of new hip complaint. Right knee X-ray, 3 views. Steroid injected into the right knee.",
     "vague": "Knee again. Shot given. Pictures taken.",
     "conflict": "Left knee osteoarthritis. Right knee X-ray, 3 views. Steroid injected into the right knee; left knee not examined."},
    {"id": "O3", "specialty": "orthopedics", "icd10": ["S52.501A"],
     "cpt": [L("25600", ["RT"]), L("73110", ["RT"])],
     "clear": "Fell on outstretched right hand. Right wrist X-ray, 3 views, shows a radius fracture in good position. Splinted without setting.",
     "vague": "Wrist injury. X-ray done. Splint.",
     "conflict": "Right wrist X-ray, 3 views, normal with no fracture. Radius fracture treated with splint, no setting needed."},
    {"id": "O4", "specialty": "orthopedics", "icd10": ["G56.01"],
     "cpt": [L("64721", ["RT"])],
     "clear": "Right carpal tunnel syndrome confirmed by nerve testing. Carpal tunnel release performed on the right hand.",
     "vague": "Hand numbness. Procedure done.",
     "conflict": "Left carpal tunnel syndrome. Carpal tunnel release performed on the right hand."},
    {"id": "O6", "specialty": "orthopedics", "icd10": ["M54.50"],
     "cpt": [L("97110", units=2)],
     "clear": "Low back pain. Therapeutic exercise for 30 minutes (2 units): core strengthening and stretching.",
     "vague": "Back session today.",
     "conflict": "No back pain reported. Therapeutic exercise for 30 minutes for low back pain."},
    # ---------- dermatology ----------
    {"id": "D1", "specialty": "dermatology", "icd10": ["L57.0"],
     "cpt": [L("17000"), L("17003", units=4)],
     "clear": "Five sun-damage spots (actinic keratoses) on the scalp and forehead. All five removed with freezing.",
     "vague": "Some spots frozen off.",
     "conflict": "Two sun-damage spots on the scalp. Five lesions removed with freezing."},
    {"id": "D2", "specialty": "dermatology", "icd10": ["D22.5"],
     "cpt": [L("11102")],
     "clear": "Changing mole on the back. Single shave biopsy taken and sent to pathology.",
     "vague": "Mole looked at. Sample taken.",
     "conflict": "Mole on the back unchanged for years, patient reports it changed last month. Single shave biopsy taken."},
    {"id": "D3", "specialty": "dermatology", "icd10": ["B07.9"],
     "cpt": [L("17110")],
     "clear": "Three common warts on the left hand. All removed with freezing.",
     "vague": "Hand bumps treated.",
     "conflict": "Three warts on the left hand, which look like skin cancer. All removed with freezing as warts."},
    {"id": "D4", "specialty": "dermatology", "icd10": ["L70.0"],
     "cpt": [L("99212")],
     "clear": "Acne follow-up. Improving on topical treatment. Continue current plan.",
     "vague": "Skin follow-up.",
     "conflict": "Acne follow-up, much worse. Acne improving, continue plan."},
]

# Scenarios whose procedure codes are missing from the data dictionary.
UNPRICED_SCENARIOS = [
    {"id": "O5", "specialty": "orthopedics", "icd10": ["M23.221"],
     "cpt": [L("29881", ["RT"])],
     "clear": "Old tear of the right medial meniscus with locking. Right knee arthroscopy with meniscus trimming performed.",
     "vague": "Knee scope done.", "conflict": "Knee scope done."},
    {"id": "D5", "specialty": "dermatology", "icd10": ["C44.311"],
     "cpt": [L("17311")],
     "clear": "Basal cell skin cancer on the nose. Mohs surgery, first stage, clear margins.",
     "vague": "Nose skin surgery.", "conflict": "Nose skin surgery."},
]

# Scenario used to create an unusually large total (many therapy units).
UNUSUAL_TOTAL = {"scenario": "O6", "units": 32,
                 "note": "Low back pain. Therapeutic exercise for 8 hours (32 units)."}
