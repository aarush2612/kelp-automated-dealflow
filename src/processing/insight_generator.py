from typing import Dict, List


class InsightGenerator:
    """
    Generates high-signal insights for teaser slides.
    """

    def generate(self, canonical_data: Dict) -> Dict[str, List[str]]:
        insights = {
            "highlights": [],
            "financial_trends": []
        }

        self._financial_insights(canonical_data, insights)
        self._operational_insights(canonical_data, insights)

        return insights

    # ---------------- internal ----------------

    def _financial_insights(self, data: Dict, insights: Dict):
        income = data["financials"].get("Income Statement", {})
        revenue = income.get("Revenue From Operations", {})

        years = [y for y in revenue.keys() if revenue[y] is not None]
        if len(years) >= 2:
            start, end = years[-2], years[-1]
            r1, r2 = revenue[start], revenue[end]
            if r1 and r2 and r1 > 0:
                growth = ((r2 - r1) / r1) * 100
                insights["financial_trends"].append(
                    f"Revenue grew {growth:.1f}% from {start} to {end}"
                )

        pat = income.get("PAT", {})
        latest_year = max(pat.keys()) if pat else None
        if latest_year and pat.get(latest_year):
            insights["financial_trends"].append(
                f"Reported PAT of ₹{pat[latest_year]:.1f} Cr in {latest_year}"
            )

    def _operational_insights(self, data: Dict, insights: Dict):
        ops = data["operations"]["key_metrics"]

        if "Number of Screens" in ops:
            insights["highlights"].append(
                f"Operates {ops['Number of Screens']} screens across multiple cities"
            )

        if "Viewers (H1 FY26)" in ops:
            insights["highlights"].append(
                f"Served {ops['Viewers (H1 FY26)']} viewers in H1 FY26"
            )
