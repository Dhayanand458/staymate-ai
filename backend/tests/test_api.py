from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_health_endpoint():
    response = client.get("/api/health")

    assert response.status_code == 200
    assert response.json() == {
        "status": "ok",
        "service": "staymate-ai-backend",
    }


def test_hotel_endpoint():
    response = client.get("/api/hotel")

    assert response.status_code == 200

    data = response.json()

    assert data["name"] == "StayMate Grand Hotel"


def test_rooms_endpoint():
    response = client.get("/api/rooms")

    assert response.status_code == 200

    rooms = response.json()

    assert len(rooms) == 4


def test_availability_endpoint():
    response = client.post(
        "/api/availability",
        json={
            "check_in": "2026-09-23",
            "check_out": "2026-09-25",
            "guests": 3,
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["guests"] == 3
    assert [room["name"] for room in data["rooms"]] == ["Family Suite"]


def test_availability_rejects_same_day_stay():
    response = client.post(
        "/api/availability",
        json={
            "check_in": "2026-09-23",
            "check_out": "2026-09-23",
            "guests": 3,
        },
    )

    assert response.status_code == 422


def test_availability_rejects_zero_guests():
    response = client.post(
        "/api/availability",
        json={
            "check_in": "2026-09-23",
            "check_out": "2026-09-25",
            "guests": 0,
        },
    )

    assert response.status_code == 422

def test_chat_answers_hotel_question():
    response = client.post(
        "/api/chat",
        json={
            "message": "What time is check-in?",
            "conversation": [],
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["response_type"] == "hotel_information"
    assert "3:00 PM" in data["message"]
    assert data["availability"] is None

    assert data["conversation"][0]["role"] == "user"
    assert data["conversation"][0]["content"] == "What time is check-in?"

    assert data["conversation"][1]["role"] == "assistant"


def test_chat_uses_safe_fallback_for_unsupported_question():
    response = client.post(
        "/api/chat",
        json={
            "message": "Does the hotel have a private helicopter service?",
            "conversation": [],
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["response_type"] == "fallback"
    assert data["availability"] is None
    assert "hotel knowledge base" in data["message"]


def test_chat_requests_missing_availability_information():
    response = client.post(
        "/api/chat",
        json={
            "message": "Do you have a room?",
            "conversation": [],
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["response_type"] == "needs_information"
    assert data["availability"] is None
    assert "check-in date" in data["message"]
    assert "check-out date" in data["message"]
    assert "number of guests" in data["message"]


def test_chat_returns_availability_for_complete_request():
    response = client.post(
        "/api/chat",
        json={
            "message": (
                "Do you have a room from 2026-09-25 "
                "to 2026-09-27 for 3 guests?"
            ),
            "conversation": [],
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["response_type"] == "availability"
    assert data["availability"] is not None

    availability = data["availability"]

    assert availability["check_in"] == "2026-09-25"
    assert availability["check_out"] == "2026-09-27"
    assert availability["guests"] == 3

    assert len(availability["rooms"]) == 1
    assert availability["rooms"][0]["name"] == "Family Suite"


def test_chat_preserves_conversation_context():
    response = client.post(
        "/api/chat",
        json={
            "message": "Is breakfast included?",
            "conversation": [
                {
                    "role": "user",
                    "content": "What rooms do you have?",
                },
                {
                    "role": "assistant",
                    "content": (
                        "Our room types include Deluxe King, Deluxe Twin, "
                        "Premium King and Family Suite."
                    ),
                },
            ],
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["response_type"] == "hotel_information"

    conversation = data["conversation"]

    assert conversation[0]["role"] == "user"
    assert conversation[0]["content"] == "What rooms do you have?"

    assert conversation[1]["role"] == "assistant"

    assert conversation[2]["role"] == "user"
    assert conversation[2]["content"] == "Is breakfast included?"

    assert conversation[3]["role"] == "assistant"