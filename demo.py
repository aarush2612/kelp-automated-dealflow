from src.ingestion.markdown_reader import MarkdownCompanyParser
from src.processing.canonical_builder import CanonicalCompanyBuilder
from src.processing.insight_generator import InsightGenerator
from src.processing.anonymizer import Anonymizer
from src.ppt.ppt_builder import PPTBuilder

parser = MarkdownCompanyParser(
    "data/raw/entertainment-connplex/Connplex Cinemas-OnePager.md"
)
parsed = parser.parse()
canonical = CanonicalCompanyBuilder(parsed).build()

insights = InsightGenerator().generate(canonical)

anon_data, _ = Anonymizer("Connplex Cinemas").anonymize(canonical)

ppt = PPTBuilder()
ppt.build(
    anon_data,
    insights,
    "outputs/entertainment-connplex/TargetCo_Teaser.pptx"
)

