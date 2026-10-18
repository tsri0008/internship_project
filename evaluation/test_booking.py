"""Hard task evaluator for booking.py, class booking.

Contract: preserve class/method names; validate HH:MM times, YYYY-MM-DD dates,
nonempty room and ID; allow adjacent bookings; reject overlapping reservations
for the same room and day; raise ValueError for invalid inputs and duplicate IDs;
book_room returns bool; cancel_booking returns bool; list_bookings(room, day)
returns only matching bookings sorted by start_time.

Set AGENTFLOW_TARGET to the absolute path of the code to evaluate.
"""
import importlib.util
import os
from pathlib import Path

import pytest

DEFAULT_TARGET = Path(__file__).resolve().parent.parent / "tasks" / "hard" / "booking.py"
TARGET = Path(os.environ.get("AGENTFLOW_TARGET", str(DEFAULT_TARGET))).resolve()
spec = importlib.util.spec_from_file_location("agentflow_hard_target", TARGET)
if spec is None or spec.loader is None:
    raise RuntimeError(f"Cannot load target: {TARGET}")
booking_task = importlib.util.module_from_spec(spec)
spec.loader.exec_module(booking_task)

DAY = "2026-10-20"


@pytest.fixture
def system():
    return booking_task.booking()


def seed(system, bid="B1", room="Room A", day=DAY, start="10:00", end="12:00"):
    """Set up an existing booking without relying on the buggy book_room method."""
    system.booking[bid] = {
        "id": bid, "room": room, "day": day,
        "start_time": start, "end_time": end,
    }


@pytest.mark.parametrize("time,expected", [
    ("00:00", 0), ("09:30", 570), ("12:00", 720), ("23:59", 1439),
])
def test_valid_time_conversion(system, time, expected):
    assert system.calculate_time(time) == expected


@pytest.mark.parametrize("invalid_time", [
    "24:00", "12:60", "12:90", "-1:00", "9:5", "abc", "12:00:00",
])
def test_invalid_time_rejected(system, invalid_time):
    with pytest.raises(ValueError):
        system.calculate_time(invalid_time)


def test_first_booking_succeeds(system):
    assert system.book_room("B1", "Room A", DAY, "09:00", "11:00") is True
    assert "B1" in system.booking


def test_nonoverlapping_same_room_same_day(system):
    seed(system)
    assert system.availability("Room A", DAY, "13:00", "14:00") is True


@pytest.mark.parametrize("start,end", [
    ("11:00", "13:00"),  # overlaps at beginning of existing booking's end
    ("09:00", "11:00"),  # overlaps at end of requested booking
    ("09:00", "13:00"),  # completely surrounds an existing booking
    ("10:30", "11:30"),  # completely inside existing booking
    ("10:00", "12:00"),  # identical interval
])
def test_overlaps_rejected(system, start, end):
    seed(system)
    assert system.availability("Room A", DAY, start, end) is False


@pytest.mark.parametrize("start,end", [
    ("08:00", "10:00"),  # ends when the existing booking begins
    ("12:00", "13:00"),  # begins when the existing booking ends
])
def test_adjacent_bookings_allowed(system, start, end):
    seed(system)
    assert system.availability("Room A", DAY, start, end) is True


def test_different_room_same_time_allowed(system):
    seed(system)
    assert system.availability("Room B", DAY, "10:30", "11:30") is True


def test_different_day_same_room_same_time_allowed(system):
    seed(system)
    assert system.availability("Room A", "2026-10-21", "10:30", "11:30") is True


def test_multiple_existing_bookings_checked(system):
    seed(system, "B1", start="09:00", end="10:00")
    seed(system, "B2", start="11:00", end="12:00")
    assert system.availability("Room A", DAY, "11:30", "13:00") is False


@pytest.mark.parametrize("start,end", [
    ("15:00", "10:00"), ("10:00", "10:00"),
])
def test_invalid_interval_rejected_even_in_empty_system(system, start, end):
    with pytest.raises(ValueError):
        system.availability("Room A", DAY, start, end)


def test_bad_time_rejected_even_in_empty_system(system):
    with pytest.raises(ValueError):
        system.availability("Room A", DAY, "25:00", "13:00")


@pytest.mark.parametrize("invalid_day", ["2026-99-99", "2026-02-30", "20-10-2026", ""])
def test_invalid_date_rejected(system, invalid_day):
    with pytest.raises(ValueError):
        system.book_room("B1", "Room A", invalid_day, "09:00", "10:00")


@pytest.mark.parametrize("bad_id,bad_room", [("", "Room A"), ("B1", "")])
def test_empty_booking_id_or_room_rejected(system, bad_id, bad_room):
    with pytest.raises(ValueError):
        system.book_room(bad_id, bad_room, DAY, "09:00", "10:00")


def test_duplicate_booking_id_rejected(system):
    seed(system)
    with pytest.raises(ValueError):
        system.book_room("B1", "Room B", "2026-10-21", "13:00", "14:00")
    assert system.booking["B1"]["room"] == "Room A"


def test_booking_conflict_returns_false_and_does_not_create_entry(system):
    seed(system)
    assert system.book_room("B2", "Room A", DAY, "11:00", "13:00") is False
    assert "B2" not in system.booking


def test_cancel_existing_booking_after_another_id(system):
    seed(system, "B1")
    seed(system, "B2", start="13:00", end="14:00")
    assert system.cancel_booking("B2") is True
    assert "B2" not in system.booking
    assert "B1" in system.booking


def test_cancel_nonexistent_booking_returns_false(system):
    seed(system)
    assert system.cancel_booking("MISSING") is False


def test_cancel_with_no_bookings_returns_false(system):
    assert system.cancel_booking("MISSING") is False


def test_list_filters_room_and_day_and_sorts_by_start(system):
    seed(system, "B_late", start="15:00", end="16:00")
    seed(system, "B_other_room", room="Room B", start="08:00", end="09:00")
    seed(system, "B_other_day", day="2026-10-21", start="08:00", end="09:00")
    seed(system, "B_early", start="09:00", end="10:00")
    matches = system.list_bookings("Room A", DAY)
    assert [entry["id"] for entry in matches] == ["B_early", "B_late"]


def test_list_no_matching_bookings_returns_empty_list(system):
    seed(system)
    assert system.list_bookings("Room B", DAY) == []
