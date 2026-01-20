import argparse
from pathlib import Path

from src.ingestion.markdown_reader import MarkdownCompanyParser
from src.processing.canonical_builder import CanonicalCompanyBuilder
from src.processing.sector_detector import SectorDetector
from src.processing.insight_generator import InsightGenerator
from src.processing.anonymizer import Anonymizer
from src.ppt.ppt_builder import PPTBuilder
from src.citations.citation_doc import CitationBuilder


def run_pipeline(company_slug: str):
    raw_dir = Path("data/raw") / company_slug
    md_files = list(raw_dir.glob("*.md"))

    if not md_files:
        raise FileNotFoundError(f"No markdown file found in {raw_dir}")

    md_path = md_files[0]

    print(f"[INFO] Processing company: {company_slug}")
    print(f"[INFO] Markdown source: {md_path.name}")

    # 1. Parse markdown
    parser = MarkdownCompanyParser(md_path)
    parsed = parser.parse()

    # 2. Canonical build
    canonical = CanonicalCompanyBuilder(parsed).build()

    # 3. Sector detection
    sector = SectorDetector().detect(canonical)
    print(f"[INFO] Detected sector: {sector}")

    # 4. Insight generation
    insights = InsightGenerator().generate(canonical)

    # 5. Anonymization
    original_name = md_path.stem.replace("-OnePager", "")
    anonymizer = Anonymizer(original_name)
    anon_data, anon_map = anonymizer.anonymize(canonical)

    # 6. PPT generation
    output_dir = Path("outputs") / company_slug
    ppt_path = output_dir / "TargetCo_Teaser.pptx"

    ppt = PPTBuilder()
    ppt.build(anon_data, insights, str(ppt_path))

    print(f"[SUCCESS] PPT generated: {ppt_path}")

    # 7. Citation document
    citation_path = output_dir / "TargetCo_Citations.docx"
    citation_builder = CitationBuilder(
        company_slug="TargetCo",
        source_md_path=md_path.name
    )
    citation_builder.build(anon_data, insights, str(citation_path))

    print(f"[SUCCESS] Citations generated: {citation_path}")

    print("\n🎉 Pipeline completed successfully.")
    print("You are ready to submit.")


if __name__ == "__main__":
    argp = argparse.ArgumentParser(description="Kelp Automated Deal Flow")
    argp.add_argument(
        "--company",
        required=True,
        help="Company folder name inside data/raw/"
    )
    args = argp.parse_args()

    run_pipeline(args.company)
