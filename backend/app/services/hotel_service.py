import json
from pathlib import Path
from typing import Any


# backend/app/services/hotel_service.py
# hotel.json lives at: backend/data/hotel.json

DATA_FILE = Path(__file__).resolve().parents[2] / "data" / "hotel.json"


def load_hotel_data() -> dict[str, Any]:
    """Load and return the complete hotel knowledge base."""

    with DATA_FILE.open("r", encoding="utf-8") as file:
        return json.load(file)


def get_hotel_info() -> dict[str, Any]:
    """Return basic hotel information."""

    data = load_hotel_data()
    return data["hotel"]


def get_rooms() -> list[dict[str, Any]]:
    """Return all room types."""

    data = load_hotel_data()
    return data["rooms"]


def get_room_by_name(room_name: str) -> dict[str, Any] | None:
    """Find a room by its name."""

    rooms = get_rooms()

    for room in rooms:
        if room["name"].lower() == room_name.lower():
            return room

    return None


def find_rooms_for_guests(adults: int) -> list[dict[str, Any]]:
    """Return rooms capable of accommodating the requested number of guests."""

    rooms = get_rooms()

    return [
        room
        for room in rooms
        if room["capacity"] >= adults
    ]