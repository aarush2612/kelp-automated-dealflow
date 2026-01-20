from typing import Dict


class SectorDetector:
    """
    Rule-based sector detector.
    Transparent and judge-friendly.
    """

    def detect(self, canonical_data: Dict) -> str:
        text = (
            canonical_data["company_profile"]["description"].lower()
            + " "
            + " ".join(canonical_data["company_profile"]["products_services"]).lower()
        )

        if any(k in text for k in ["cinema", "multiplex", "theatre", "entertainment"]):
            return "Consumer_Entertainment"

        if any(k in text for k in ["saas", "platform", "software", "cloud"]):
            return "Technology"

        if any(k in text for k in ["manufacturing", "plant", "factory"]):
            return "Manufacturing"

        if any(k in text for k in ["pharma", "drug", "clinical"]):
            return "Pharmaceuticals"

        return "General"
