from datetime import time

from models.attendance_models import AttendanceRow
from transformers.invariants import validate_row_invariants


def create_row(
    entry=time(8, 30),
    exit_time=time(12, 0),
    break_hours=0.0,
    total_hours=3.5,
    h_100=3.5
):
    return AttendanceRow(
        date="01/09/2022",
        day="חמישי",
        entry=entry,
        exit_time=exit_time,
        break_hours=break_hours,
        total_hours=total_hours,
        h_100=h_100
    )


def test_valid_row():
    row = create_row()

    assert validate_row_invariants(row) is True


def test_invalid_entry():
    row = create_row(entry="25:30")

    assert validate_row_invariants(row) is False


def test_exit_before_entry():
    row = create_row(
        entry=time(12, 0),
        exit_time=time(8, 30)
    )

    assert validate_row_invariants(row) is False


def test_negative_break():
    row = create_row(break_hours=-0.5)

    assert validate_row_invariants(row) is False


def test_wrong_total_hours():
    row = create_row(
        total_hours=5.0,
        h_100=5.0
    )

    assert validate_row_invariants(row) is False
def test_wrong_hours_breakdown():
    row = create_row(
        total_hours=3.5,
        h_100=2.0
    )

    assert validate_row_invariants(row) is False