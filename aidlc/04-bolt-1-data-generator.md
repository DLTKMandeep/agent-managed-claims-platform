# Bolt 1: Synthetic data generator

**Phase:** Construction
**Status:** Done, 2026-11-24

## What was built

| File | Purpose |
| --- | --- |
| `data/reference.py` | Code set (40 ICD-10, 40 CPT, 10 per specialty), internal fee schedule, modifier rules, pricing functions |
| `data/scenarios.py` | 17 clinical scenarios with correct codes and three note versions each (clear, vague, conflicting), plus 2 scenarios with codes missing from the fee schedule |
| `data/generate.py` | Generates claims and a hidden answer key; deterministic for a given seed |
| `tests/test_generator.py` | 12 tests covering the requirements below |

## How to run

```
python -m data.generate --count 200 --seed 42 --out data/out
pip install -r requirements-dev.txt
pytest
```

## Results (seed 42)

| Check | Result |
| --- | --- |
| Claims generated | 200: 140 clean (70%), 60 messy (30%) |
| Specialties | Primary care 49, cardiology 47, orthopedics 59, dermatology 45 |
| Messy issues | 7 or 8 each of: missing member ID, missing provider NPI, missing date of birth, duplicate, vague note, conflicting note, code not in dictionary, unusual total |
| Stage that should catch each | Intake 8, validation 24, clinical review 14, pricing 14 |
| Tests | 12 of 12 pass |

## Design notes

- **Agents never see the answers.** `claims.jsonl` holds only what a real claim would contain; `answer_key.jsonl` holds the correct codes, validity, expected escalation stage and total.
- **Everything is visibly fake.** Patient and provider names are invented, member IDs start with `SYN-`, and provider NPIs start with 9 (real NPIs start with 1 or 2).
- **Two codes are deliberately missing from the fee schedule** (29881 knee arthroscopy, 17311 Mohs surgery) so the Pricing Analyst has real escalations to raise.
- **Code descriptions are paraphrased** for this prototype and prices are synthetic.

## Next

Bolt 2: agent framework and team roster, plus the Intake Clerk and Claims Validator agents.
