from src.processing.anonymizer import Anonymizer


def test_company_name_removed():
    data = {
        "company_profile": {
            "description": "Connplex Cinemas operates premium theatres."
        }
    }

    anonymizer = Anonymizer("Connplex Cinemas")
    anon_data, mapping = anonymizer.anonymize(data)

    assert "Connplex" not in anon_data["company_profile"]["description"]
    assert "TargetCo" in anon_data["company_profile"]["description"]


def test_numbers_preserved():
    data = {
        "financials": {
            "Income Statement": {
                "Revenue": {"2025": 959.9}
            }
        }
    }

    anonymizer = Anonymizer("AnyCo")
    anon_data, _ = anonymizer.anonymize(data)

    assert anon_data["financials"]["Income Statement"]["Revenue"]["2025"] == 959.9


def test_person_name_removed():
    data = {
        "company_profile": {
            "description": "Rahul Dhayani is the CEO."
        }
    }

    anonymizer = Anonymizer("AnyCo")
    anon_data, _ = anonymizer.anonymize(data)

    assert "Rahul" not in anon_data["company_profile"]["description"]
    assert "Executive (Anon)" in anon_data["company_profile"]["description"]
