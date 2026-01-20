import re
from typing import Dict, Any, Tuple
from copy import deepcopy


class Anonymizer:
    """
    Deterministic anonymization for investment teasers.
    """

    COMPANY_TOKEN = "TargetCo"
    PERSON_TOKEN = "Executive (Anon)"
    BRAND_TOKEN = "BrandX"

    def __init__(self, original_company_name: str):
        self.original_company_name = original_company_name
        self.mapping = {
            original_company_name: self.COMPANY_TOKEN
        }

    def anonymize(self, canonical_data: Dict[str, Any]) -> Tuple[Dict[str, Any], Dict[str, str]]:
        anonymized = deepcopy(canonical_data)

        anonymized = self._anonymize_strings(anonymized)

        return anonymized, self.mapping

    # ---------------- internal ----------------

    def _anonymize_strings(self, obj):
        if isinstance(obj, dict):
            return {k: self._anonymize_strings(v) for k, v in obj.items()}

        if isinstance(obj, list):
            return [self._anonymize_strings(i) for i in obj]

        if isinstance(obj, str):
            return self._anonymize_text(obj)

        return obj

    def _anonymize_text(self, text: str) -> str:
        # Replace company name
        text = re.sub(
            re.escape(self.original_company_name),
            self.COMPANY_TOKEN,
            text,
            flags=re.IGNORECASE
        )

        # Replace common brand references (Connplex → BrandX)
        if "connplex" in text.lower():
            self.mapping["Connplex"] = self.BRAND_TOKEN
            text = re.sub("connplex", self.BRAND_TOKEN, text, flags=re.IGNORECASE)

        # Replace person names (simple heuristic: Firstname Lastname)
        text = re.sub(
            r"\b[A-Z][a-z]+ [A-Z][a-z]+\b",
            self.PERSON_TOKEN,
            text
        )

        return text
