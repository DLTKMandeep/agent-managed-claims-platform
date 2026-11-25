"""Reference data for the synthetic claims platform.

All descriptions are short paraphrases written for this prototype.
Prices are synthetic and do not reflect any real fee schedule.
"""

SPECIALTIES = ["primary_care", "cardiology", "orthopedics", "dermatology"]

# ICD-10-CM diagnosis codes in use: (code, short description, specialty)
ICD10 = [
    ("I10", "High blood pressure", "primary_care"),
    ("E11.9", "Type 2 diabetes without complications", "primary_care"),
    ("J06.9", "Upper respiratory infection", "primary_care"),
    ("E78.5", "High cholesterol", "primary_care"),
    ("Z00.00", "Routine adult exam, no abnormal findings", "primary_care"),
    ("J02.9", "Sore throat infection", "primary_care"),
    ("N39.0", "Urinary tract infection", "primary_care"),
    ("R05.9", "Cough", "primary_care"),
    ("E66.9", "Obesity", "primary_care"),
    ("F41.1", "Generalized anxiety", "primary_care"),
    ("I25.10", "Coronary artery disease without angina", "cardiology"),
    ("I48.91", "Atrial fibrillation", "cardiology"),
    ("I50.9", "Heart failure", "cardiology"),
    ("R07.9", "Chest pain", "cardiology"),
    ("I20.9", "Angina", "cardiology"),
    ("R00.2", "Palpitations", "cardiology"),
    ("I35.0", "Aortic valve narrowing", "cardiology"),
    ("I34.0", "Mitral valve leakage", "cardiology"),
    ("R94.31", "Abnormal heart tracing", "cardiology"),
    ("I49.9", "Irregular heart rhythm", "cardiology"),
    ("S93.401A", "Right ankle ligament sprain, first visit", "orthopedics"),
    ("M17.11", "Right knee osteoarthritis", "orthopedics"),
    ("M54.50", "Low back pain", "orthopedics"),
    ("S82.61XA", "Right outer ankle bone fracture, first visit", "orthopedics"),
    ("M23.221", "Right knee meniscus derangement from old tear", "orthopedics"),
    ("M25.561", "Right knee pain", "orthopedics"),
    ("M65.4", "Thumb-side wrist tendon inflammation", "orthopedics"),
    ("G56.01", "Right carpal tunnel syndrome", "orthopedics"),
    ("S52.501A", "Right wrist (radius) fracture, first visit", "orthopedics"),
    ("M75.101", "Right rotator cuff tear, not from injury", "orthopedics"),
    ("L70.0", "Acne", "dermatology"),
    ("L40.0", "Plaque psoriasis", "dermatology"),
    ("L20.9", "Eczema", "dermatology"),
    ("L57.0", "Actinic keratosis (sun-damage spots)", "dermatology"),
    ("D22.5", "Mole on the trunk", "dermatology"),
    ("L82.1", "Seborrheic keratosis", "dermatology"),
    ("B07.9", "Viral wart", "dermatology"),
    ("L30.9", "Dermatitis", "dermatology"),
    ("C44.311", "Basal cell skin cancer of the nose", "dermatology"),
    ("L72.3", "Sebaceous cyst", "dermatology"),
]

# CPT procedure codes in use: (code, short description, specialty)
CPT = [
    ("99213", "Office visit, established patient, low complexity", "primary_care"),
    ("99214", "Office visit, established patient, moderate complexity", "primary_care"),
    ("99203", "Office visit, new patient, low complexity", "primary_care"),
    ("99395", "Preventive visit, established patient, age 18-39", "primary_care"),
    ("99396", "Preventive visit, established patient, age 40-64", "primary_care"),
    ("87880", "Rapid strep test", "primary_care"),
    ("81002", "Urine dipstick test", "primary_care"),
    ("36415", "Blood draw", "primary_care"),
    ("83036", "HbA1c blood sugar test", "primary_care"),
    ("80061", "Cholesterol panel", "primary_care"),
    ("93000", "Heart tracing (ECG) with report", "cardiology"),
    ("93005", "Heart tracing (ECG), tracing only", "cardiology"),
    ("93010", "Heart tracing (ECG), report only", "cardiology"),
    ("93306", "Heart ultrasound (echo), complete", "cardiology"),
    ("93350", "Stress echo", "cardiology"),
    ("93224", "48-hour heart monitor", "cardiology"),
    ("93015", "Treadmill stress test", "cardiology"),
    ("93880", "Neck artery ultrasound, both sides", "cardiology"),
    ("93970", "Leg vein ultrasound, both sides", "cardiology"),
    ("99243", "Specialist consultation, office", "cardiology"),
    ("73610", "Ankle X-ray, 3 or more views", "orthopedics"),
    ("73562", "Knee X-ray, 3 views", "orthopedics"),
    ("73110", "Wrist X-ray, 3 or more views", "orthopedics"),
    ("20610", "Joint injection or drainage, large joint", "orthopedics"),
    ("29881", "Knee arthroscopy with meniscus trimming", "orthopedics"),
    ("27786", "Ankle fibula fracture care without setting", "orthopedics"),
    ("29540", "Ankle strapping", "orthopedics"),
    ("97110", "Therapeutic exercise, per 15 minutes", "orthopedics"),
    ("64721", "Carpal tunnel release", "orthopedics"),
    ("25600", "Wrist radius fracture care without setting", "orthopedics"),
    ("11102", "Skin biopsy, single lesion", "dermatology"),
    ("17000", "Removal of first sun-damage spot", "dermatology"),
    ("17003", "Removal of each additional sun-damage spot (2-14)", "dermatology"),
    ("17110", "Removal of benign lesions such as warts, up to 14", "dermatology"),
    ("11402", "Removal of benign skin lesion on trunk, 1.1-2.0 cm", "dermatology"),
    ("11602", "Removal of skin cancer on trunk, 1.1-2.0 cm", "dermatology"),
    ("10060", "Drainage of skin abscess, simple", "dermatology"),
    ("11900", "Injection into skin lesions, up to 7", "dermatology"),
    ("99212", "Office visit, established patient, straightforward", "dermatology"),
    ("17311", "Mohs skin cancer surgery, first stage", "dermatology"),
]

# Internal data dictionary: price per CPT code (synthetic, USD).
# 29881 and 17311 are deliberately absent so the Pricing Agent must escalate.
FEE_SCHEDULE = {
    "99212": 60, "99213": 95, "99214": 140, "99203": 120, "99243": 190,
    "99395": 150, "99396": 165, "87880": 18, "81002": 6, "36415": 9,
    "83036": 15, "80061": 22, "93000": 30, "93005": 12, "93010": 10,
    "93306": 260, "93350": 310, "93224": 120, "93015": 115, "93880": 210,
    "93970": 205, "73610": 45, "73562": 48, "73110": 44, "20610": 85,
    "27786": 380, "29540": 25, "97110": 32, "64721": 610, "25600": 420,
    "11102": 110, "17000": 85, "17003": 9, "17110": 105, "11402": 210,
    "11602": 290, "10060": 140, "11900": 70,
}

# Modifier rules: payment factor applied to the line price.
MODIFIERS = {"25": 1.0, "59": 1.0, "RT": 1.0, "LT": 1.0, "50": 1.5}

ICD10_CODES = {c for c, _, _ in ICD10}
CPT_CODES = {c for c, _, _ in CPT}


def line_price(code, modifiers=(), units=1):
    """Price one claim line, or return None if the code is not in the dictionary."""
    if code not in FEE_SCHEDULE:
        return None
    factor = 1.0
    for m in modifiers:
        factor *= MODIFIERS.get(m, 1.0)
    return round(FEE_SCHEDULE[code] * factor * units, 2)


def claim_total(lines):
    """Total for a list of {code, modifiers, units} lines, or None if any line is unpriceable."""
    prices = [line_price(l["code"], l.get("modifiers", ()), l.get("units", 1)) for l in lines]
    if any(p is None for p in prices):
        return None
    return round(sum(prices), 2)
