from parsers.type_a_parser import TypeAParser
from models.report_types import ReportType


def test_type_a_parser():
    lines = [
        'שם העובד: ישראל ישראלי',
        '01/09/2022 08:30 12:00'
    ]

    parser = TypeAParser()
    report = parser.parse(lines)

    assert report.report_type == ReportType.TYPE_A
    assert len(report.rows) == 1
    assert report.rows[0].total_hours == 3.5