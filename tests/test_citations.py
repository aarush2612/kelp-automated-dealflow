from src.citations.citation_doc import CitationBuilder
from pathlib import Path


def test_citation_doc_creation(tmp_path):
    builder = CitationBuilder(
        company_slug="TargetCo",
        source_md_path="Connplex Cinemas-OnePager.md"
    )

    canonical = {
        "company_profile": {"website": "https://example.com"},
        "financials": {},
        "swot": {}
    }

    insights = {
        "highlights": ["Operates 88 screens nationwide"]
    }

    out = tmp_path / "citations.docx"
    builder.build(canonical, insights, out)

    assert out.exists()
