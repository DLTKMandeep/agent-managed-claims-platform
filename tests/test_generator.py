"""Tests for Bolt 1: synthetic data generator."""
from collections import Counter, defaultdict

import pytest

from data.generate import ISSUES, generate
from data.reference import CPT_CODES, FEE_SCHEDULE, ICD10_CODES, SPECIALTIES, claim_total


@pytest.fixture(scope="module")
def data():
    return generate(count=200, seed=42)


def test_volume_and_mix(data):
    claims, answers = data
    assert len(claims) == len(answers) == 200
    assert sum(a["is_clean"] for a in answers) == 140
    assert sum(not a["is_clean"] for a in answers) == 60


def test_same_seed_same_data():
    assert generate(200, 42) == generate(200, 42)
    assert generate(200, 42) != generate(200, 7)


def test_every_issue_type_appears(data):
    counts = Counter(a["issue"] for a in data[1] if a["issue"])
    assert set(counts) == set(ISSUES)
    assert min(counts.values()) >= 5


def test_specialties_are_balanced(data):
    counts = Counter(a["specialty"] for a in data[1])
    assert set(counts) == set(SPECIALTIES)
    assert min(counts.values()) >= 30


def test_answer_key_uses_known_codes(data):
    for a in data[1]:
        assert set(a["icd10"]) <= ICD10_CODES
        assert {l["code"] for l in a["cpt"]} <= CPT_CODES


def test_clean_claims_are_fully_priced(data):
    for a in data[1]:
        if a["is_clean"]:
            assert all(l["code"] in FEE_SCHEDULE for l in a["cpt"])
            assert a["expected_total"] == claim_total(a["cpt"])


def test_unpriced_codes_have_no_total(data):
    for a in data[1]:
        if a["issue"] == "code_not_in_dictionary":
            assert a["expected_total"] is None
            assert a["expected_escalation_stage"] == "pricing"


def test_missing_fields_are_blank_and_invalid(data):
    claims, answers = data
    field = {"missing_member_id": ("patient", "member_id"),
             "missing_dob": ("patient", "dob"),
             "missing_provider_npi": ("provider", "npi")}
    for c, a in zip(claims, answers):
        if a["issue"] in field:
            group, key = field[a["issue"]]
            assert c[group][key] == ""
            assert a["expected_valid"] is False


def test_duplicates_copy_an_earlier_claim(data):
    claims, answers = data
    by_id = {c["claim_id"]: (i, c) for i, c in enumerate(claims)}
    for i, (c, a) in enumerate(zip(claims, answers)):
        if a["issue"] == "duplicate":
            j, original = by_id[a["duplicate_of"]]
            assert j < i
            assert c["note"] == original["note"]
            assert c["patient"] == original["patient"]


def test_unusual_totals_exceed_three_times_specialty_average(data):
    totals = defaultdict(list)
    for a in data[1]:
        if a["is_clean"]:
            totals[a["specialty"]].append(a["expected_total"])
    for a in data[1]:
        if a["issue"] == "unusual_total":
            avg = sum(totals[a["specialty"]]) / len(totals[a["specialty"]])
            assert a["expected_total"] > 3 * avg


def test_claims_hide_the_answers(data):
    allowed = {"claim_id", "received_at", "visit_date", "patient", "provider", "note"}
    for c in data[0]:
        assert set(c) == allowed


def test_provider_npis_are_fake(data):
    for c in data[0]:
        npi = c["provider"]["npi"]
        assert npi == "" or (npi.startswith("9") and len(npi) == 10)
