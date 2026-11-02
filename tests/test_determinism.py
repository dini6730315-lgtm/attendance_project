import hashlib
import json
from dataclasses import asdict
from parsers import extract_text_from_pdf, get_parser_for_report
from transformers import validate_report_invariants
from transformers.transformation_strategy import StandardTransformationStrategy
def test_pipeline_determinism(pdf_filename: str):
    """בדיקה ששתי הרצות עוקבות על קובץ קלט מייצרות פלט זהה ברמת הנתונים"""
    lines1 = extract_text_from_pdf(pdf_filename)
    lines2 = extract_text_from_pdf(pdf_filename)

    parser1 = get_parser_for_report(lines1)
    parser2 = get_parser_for_report(lines2)


    rep1 = validate_report_invariants(parser1.parse(lines1))
    rep2 = validate_report_invariants(parser2.parse(lines2))

    strategy = StandardTransformationStrategy()
    assert validate_report_invariants(rep1)
    assert validate_report_invariants(rep2)

    rep1 = strategy.transform(rep1, seed=42)
    rep2 = strategy.transform(rep2, seed=42)
    validate_report_invariants(rep1)
    validate_report_invariants(rep2)
    hash1 = hashlib.md5(json.dumps(asdict(rep1), ensure_ascii=False).encode("utf-8")).hexdigest()
    hash2 = hashlib.md5(json.dumps(asdict(rep2), ensure_ascii=False).encode("utf-8")).hexdigest()

    assert hash1 == hash2, "כישלון בדטרמיניזם: שתי הרצות נתנו תוצאות שונות!"
    print(f"בדיקת דטרמיניזם עברה בהצלחה עבור הקובץ: {pdf_filename}")
    return True

def run_all_tests(sample_pdf: str):
    test_pipeline_determinism(sample_pdf)