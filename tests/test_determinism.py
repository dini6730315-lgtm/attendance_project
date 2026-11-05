import hashlib
import json
from dataclasses import asdict
from datetime import time
from pathlib import Path

from parsers import extract_text_from_pdf, get_parser_for_report
from transformers import validate_report_invariants
from transformers.transformation_strategy import StandardTransformationStrategy


def test_pipeline_determinism():
    """בדיקה ששתי הרצות עם אותו קלט ואותו seed מפיקות תוצאה זהה."""

    pdf_filename = Path(__file__).resolve().parent.parent / "n_r_5_n.pdf"

    lines1 = extract_text_from_pdf(str(pdf_filename))
    lines2 = extract_text_from_pdf(str(pdf_filename))

    parser1 = get_parser_for_report(lines1)
    parser2 = get_parser_for_report(lines2)

    report1 = validate_report_invariants(parser1.parse(lines1))
    report2 = validate_report_invariants(parser2.parse(lines2))

    strategy = StandardTransformationStrategy()

    result1 = strategy.transform(report1, seed=42)
    result2 = strategy.transform(report2, seed=42)

    def serialize_report(report):
        return json.dumps(
            asdict(report),
            ensure_ascii=False,
            sort_keys=True,
            default=lambda value: value.isoformat()
            if isinstance(value, time)
            else str(value)
        )

    hash1 = hashlib.md5(serialize_report(result1).encode("utf-8")).hexdigest()
    hash2 = hashlib.md5(serialize_report(result2).encode("utf-8")).hexdigest()

    assert hash1 == hash2, (
        "כישלון בדטרמיניזם: שתי הרצות נתנו תוצאות שונות!"
    )