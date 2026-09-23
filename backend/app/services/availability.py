from datetime import date

from app.services.hotel_service import get_rooms


def check_availability(
    check_in: date,
    check_out: date,
    guests: int,
) -> list[dict]:
    """
    Find room types that can accommodate the requested number of guests.

    The current hotel knowledge base contains room capacity information,
    but does not contain date-specific inventory. Therefore, this function
    performs deterministic room eligibility based on capacity.
    """

    if check_out <= check_in:
        raise ValueError("Check-out date must be after check-in date.")

    if guests < 1:
        raise ValueError("Guests must be at least 1.")

    rooms = get_rooms()

    return [
        room
        for room in rooms
        if room["capacity"] >= guests
    ]