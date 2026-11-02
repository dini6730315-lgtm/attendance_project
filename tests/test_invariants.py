from models.attendance_models import AttendanceRow
from transformers.invariants import validate_row_invariants


def test_valid_row():
    row = AttendanceRow(
        date="01/09/2022",
        day="חמישי",
        entry="08:30",
        exit_time="12:00",
        break_hours=0,
        total_hours=3.5
    )
    assert validate_row_invariants(row)


def test_invalid_entry():
    row = AttendanceRow(
        date="01/09/2022",
        day="חמישי",
        entry="25:30",
        exit_time="12:00",
        break_hours=0,
        total_hours=3.5
    )
    assert not validate_row_invariants(row)


def test_exit_before_entry():
    row = AttendanceRow(
        date="01/09/2022",
        day="חמישי",
        entry="12:00",
        exit_time="08:30",
        break_hours=0,
        total_hours=3.5
    )
    assert not validate_row_invariants(row)


def test_negative_break():
    row = AttendanceRow(
        date="01/09/2022",
        day="חמישי",
        entry="08:30",
        exit_time="12:00",
        break_hours=-1,
        total_hours=3.5
    )
    assert not validate_row_invariants(row)


def test_wrong_total_hours():
    row = AttendanceRow(
        date="01/09/2022",
        day="חמישי",
        entry="08:30",
        exit_time="12:00",
        break_hours=0,
        total_hours=5
    )
    assert not validate_row_invariants(row)