from typing import Dict, Any


class CanonicalCompanyBuilder:
    """
    Converts parsed markdown data into a canonical internal schema
    used by the rest of the pipeline.
    """

    def __init__(self, parsed_data: Dict[str, Any]):
        self.data = parsed_data

    def build(self) -> Dict[str, Any]:
        canonical = {
            "company_profile": self._company_profile(),
            "operations": self._operations(),
            "financials": self._financials(),
            "market": self._market(),
            "swot": self.data.get("swot", {}),
            "metadata": self.data.get("metadata", {})
        }
        return canonical

    # ---------------- internal ----------------

    def _company_profile(self) -> Dict[str, Any]:
        return {
            "description": self.data.get("business_description", ""),
            "website": self.data.get("website", ""),
            "products_services": self.data.get("products_services", []),
            "geography": self.data.get("metadata", {}).get("Domain", "")
        }

    def _operations(self) -> Dict[str, Any]:
        return {
            "key_metrics": self.data.get("operational_indicators", {}),
            "channel_mix": self.data.get("channel_mix", {}),
            "milestones": self.data.get("milestones", [])
        }

    def _financials(self) -> Dict[str, Any]:
        return self.data.get("financials", {})

    def _market(self) -> Dict[str, Any]:
        return {
            "market_size": self.data.get("market_size", [])
        }
