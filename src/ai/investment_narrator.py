import os
from typing import Dict, List

try:
    import google.generativeai as genai
except ImportError:
    genai = None


class InvestmentNarrator:
    """
    Uses Gemini to convert structured company data into
    investment-grade narrative text.
    """

    def __init__(self):
        self.api_key = os.getenv("GEMINI_API_KEY")
        self.enabled = self.api_key is not None and genai is not None

        if self.enabled:
            genai.configure(api_key=self.api_key)
            self.model = genai.GenerativeModel("gemini-1.5-flash")
        else:
            self.model = None

    # ---------------- PUBLIC API ----------------

    def generate_overview(self, data: Dict, sector: str) -> str:
        if not self.enabled:
            return self._fallback_overview(data)

        prompt = self._overview_prompt(data, sector)
        return self._run(prompt)

    def generate_highlights(self, data: Dict, sector: str) -> List[str]:
        if not self.enabled:
            return self._fallback_highlights(data)

        prompt = self._highlights_prompt(data, sector)
        text = self._run(prompt)

        # Convert response into bullets
        bullets = [
            line.strip("-• ").strip()
            for line in text.split("\n")
            if len(line.strip()) > 10
        ]
        return bullets[:4]

    # ---------------- PROMPTS ----------------

    def _overview_prompt(self, data: Dict, sector: str) -> str:
        return f"""
You are an M&A investment banker.

Write a concise, professional executive summary (3–4 sentences)
for an anonymized company in the {sector} sector.

Rules:
- Use investment banking tone
- No company names
- No marketing language
- No numbers unless absolutely necessary
- Focus on business model, positioning, and scale

Raw description:
{data["company_profile"]["description"]}
"""

    def _highlights_prompt(self, data: Dict, sector: str) -> str:
        return f"""
You are preparing an M&A teaser.

From the information below, extract 3–4 sharp investment highlights
written as short bullets.

Rules:
- One line per bullet
- Focus on scale, growth, margins, differentiation
- Do NOT invent numbers
- Do NOT repeat raw sentences

Operational indicators:
{data.get("key_operational_indicators", {})}

Financial summary:
{data.get("financials", {}).get("Income Statement", {})}
"""

    # ---------------- HELPERS ----------------

    def _run(self, prompt: str) -> str:
        try:
            response = self.model.generate_content(prompt)
            return response.text.strip()
        except Exception:
            return ""

    # ---------------- FALLBACKS ----------------

    def _fallback_overview(self, data: Dict) -> str:
        return data["company_profile"]["description"]

    def _fallback_highlights(self, data: Dict) -> List[str]:
        return [
            "Established operating platform with multi-year growth visibility",
            "Demonstrated scale across core markets",
            "Improving profitability profile driven by operating leverage",
        ]
