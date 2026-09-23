from datetime import date

import pytest

from app.services.availability import check_availability


def test_availability_for_three_guests():
    rooms = check_availability(
        check_in=date(2026, 9, 23),
        check_out=date(2026, 9, 25),
        guests=3,
    )

    assert [room["name"] for room in rooms] == ["Family Suite"]


def test_availability_for_two_guests():
    rooms = check_availability(
        check_in=date(2026, 9, 23),
        check_out=date(2026, 9, 25),
        guests=2,
    )

    assert len(rooms) == 4


def test_check_out_must_be_after_check_in():
    with pytest.raises(ValueError, match="Check-out date must be after check-in date"):
        check_availability(
            check_in=date(2026, 9, 25),
            check_out=date(2026, 9, 23),
            guests=3,
        )


def test_zero_guests_is_invalid():
    with pytest.raises(ValueError, match="Guests must be at least 1"):
        check_availability(
            check_in=date(2026, 9, 23),
            check_out=date(2026, 9, 25),
            guests=0,
        )