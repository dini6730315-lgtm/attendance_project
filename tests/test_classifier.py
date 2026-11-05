from parsers import get_parser_for_report
from parsers.type_a_parser import TypeAParser
from parsers.type_b_parser import TypeBParser


def test_classifier_type_a():
    lines = [
        'סה"כ ימי עבודה לחודש',
        'שעות 100%',
        'שבת 150%'
    ]

    parser = get_parser_for_report(lines)

    assert isinstance(parser, TypeAParser)


def test_classifier_type_b():
    lines = [
        'מקום עבודה',
        '125%',
        '150%'
    ]

    parser = get_parser_for_report(lines)

    assert isinstance(parser, TypeBParser)