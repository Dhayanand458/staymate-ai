from app.services.hotel_service import (
    find_rooms_for_guests,
    get_hotel_info,
    get_rooms,
)


def test_hotel_info():
    hotel = get_hotel_info()

    assert hotel["name"] == "StayMate Grand Hotel"
    assert hotel["location"] == "Bengaluru, Karnataka, India"
    assert hotel["currency"] == "INR"


def test_rooms_exist():
    rooms = get_rooms()

    assert len(rooms) == 4

    room_names = [room["name"] for room in rooms]

    assert "Deluxe King" in room_names
    assert "Deluxe Twin" in room_names
    assert "Premium King" in room_names
    assert "Family Suite" in room_names


def test_three_guests_can_fit_in_family_suite():
    rooms = find_rooms_for_guests(3)

    room_names = [room["name"] for room in rooms]

    assert room_names == ["Family Suite"]


def test_two_guests_can_fit_in_all_rooms():
    rooms = find_rooms_for_guests(2)

    assert len(rooms) == 4