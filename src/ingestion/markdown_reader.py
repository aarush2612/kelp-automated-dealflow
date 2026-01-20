from pathlib import Path
import re
from typing import Dict, Any, List


class MarkdownCompanyParser:
    """
    Parses a single-company markdown OnePager into structured JSON.
    """

    def __init__(self, md_path: str):
        self.md_path = Path(md_path)
        if not self.md_path.exists():
            raise FileNotFoundError(f"Markdown file not found: {md_path}")

        self.raw_text = self.md_path.read_text(encoding="utf-8")

    def parse(self) -> Dict[str, Any]:
        sections = self._split_sections()
        parsed = {
            "business_description": sections.get("Business Description", ""),
            "website": self._extract_website(sections),
            "products_services": self._extract_bullets(sections.get("Product & Services", "")),
            "operational_indicators": self._extract_key_values(sections.get("Key Operational Indicators", "")),
            "channel_mix": self._extract_key_values(sections.get("Channel Mix", "")),
            "swot": self._extract_swot(sections),
            "milestones": self._extract_table(sections.get("Key Milestones", "")),
            "market_size": self._extract_table(sections.get("Market Size", "")),
            "financials": self._extract_financials(sections),
            "metadata": self._extract_metadata(sections)
        }
        return parsed

    # ---------- Internal helpers ----------

    def _split_sections(self) -> Dict[str, str]:
        sections = {}
        current = None
        buffer = []

        for line in self.raw_text.splitlines():
            if line.startswith("## "):
                if current:
                    sections[current] = "\n".join(buffer).strip()
                current = line.replace("## ", "").strip()
                buffer = []
            else:
                buffer.append(line)

        if current:
            sections[current] = "\n".join(buffer).strip()

        return sections

    def _extract_website(self, sections: Dict[str, str]) -> str:
        website_block = sections.get("Website", "")
        match = re.search(r"https?://[^\s]+", website_block)
        return match.group(0) if match else ""

    def _extract_bullets(self, text: str) -> List[str]:
        return [
            re.sub(r"^\-\s*", "", line).strip()
            for line in text.splitlines()
            if line.strip().startswith("-")
        ]

    def _extract_key_values(self, text: str) -> Dict[str, Any]:
        data = {}
        for line in text.splitlines():
            if "|" in line:
                continue
            match = re.match(r"[\*\-]*\s*\*\*(.+?)\:\*\*\s*(.+)", line)
            if match:
                key, value = match.groups()
                data[key.strip()] = value.strip()
        return data

    def _extract_table(self, text: str) -> List[Dict[str, str]]:
        lines = [l.strip() for l in text.splitlines() if "|" in l]
        if len(lines) < 2:
            return []

        headers = [h.strip() for h in lines[0].split("|") if h.strip()]
        rows = []

        for line in lines[2:]:
            values = [v.strip() for v in line.split("|") if v.strip()]
            if len(values) == len(headers):
                rows.append(dict(zip(headers, values)))

        return rows

    def _extract_swot(self, sections: Dict[str, str]) -> Dict[str, List[str]]:
        swot = {}
        swot_block = sections.get("SWOT", "")
        current = None
        buffer = []

        for line in swot_block.splitlines():
            if line.startswith("### "):
                if current:
                    swot[current] = buffer
                current = line.replace("### ", "").strip()
                buffer = []
            elif line.strip().startswith("-"):
                buffer.append(line.replace("-", "").strip())

        if current:
            swot[current] = buffer

        return swot

    def _extract_financials(self, sections: Dict[str, str]) -> Dict[str, Dict[str, Dict[str, float]]]:
        financials = {}
        block = sections.get("Financials Status", "")
        current_section = None

        for line in block.splitlines():
            if line.startswith("### "):
                current_section = line.replace("### ", "").strip()
                financials[current_section] = {}
            elif "|" in line and current_section:
                parts = [p.strip() for p in line.split("|")]
                metric = parts[0].replace("-", "").strip()
                yearly = {}
                for part in parts[1:]:
                    if ":" in part:
                        year, value = part.split(":")
                        try:
                            yearly[year.strip()] = float(value.strip())
                        except:
                            yearly[year.strip()] = None
                financials[current_section][metric] = yearly

        return financials

    def _extract_metadata(self, sections: Dict[str, str]) -> Dict[str, str]:
        meta = {}
        details = sections.get("Details", "")
        for line in details.splitlines():
            if ":" in line:
                key, val = line.split(":", 1)
                meta[key.strip()] = val.strip().replace("**", "")
        return meta
