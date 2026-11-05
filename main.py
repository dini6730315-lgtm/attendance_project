
import sys
from parsers import extract_text_from_pdf, get_parser_for_report
from transformers import validate_report_invariants, TransformationService
from generators import generate_report_pdf
def execute_pipeline(pdf_filename: str, output_pdf_filename: str = "attendance_output.pdf"):
    print(f"=== מתחיל הרצת Pipeline על הקובץ: {pdf_filename} ===")
    # 1. Parsing & OCR
    raw_lines = extract_text_from_pdf(pdf_filename)
    if not raw_lines:
        print("לא חולץ טקסט מהקובץ. עוצר תהליך.")
        return
    # 2. Polymorphic Factory Selection & Parsing
    parser = get_parser_for_report(raw_lines)
    print("Selected parser:", type(parser).__name__)
    report_data = parser.parse(raw_lines)
    # 3. Business Invariants
    # 3. Business Invariants
    validated_report = validate_report_invariants(report_data)
    # בדיקה שלא קיבלנו דו"ח ריק
    if not validated_report.rows:
        raise ValueError("לא נמצאו שורות נוכחות תקינות!")
    # 4. Transformation
    transformation_service = TransformationService()
    transformed_report = transformation_service.transform(
        validated_report,
        seed=42
    )
    # 5. Generation
    generate_report_pdf(
        transformed_report,
        output_pdf_filename
    )
    # 5. Determinism Verification

    print("=== התהליך הושלם בהצלחה ===")
if __name__ == "__main__":
    input_pdf = sys.argv[1] if len(sys.argv) > 1 else "n_r_5_n.pdf"
    execute_pipeline(input_pdf)