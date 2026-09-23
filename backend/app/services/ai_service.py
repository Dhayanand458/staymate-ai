import re
from datetime import date
from typing import Any

from app.services.availability import check_availability
from app.services.hotel_service import load_hotel_data


MAX_CONTEXT_MESSAGES = 8


def normalize_text(text: str) -> str:
    """Normalize user text for simple intent detection."""
    return re.sub(r"\s+", " ", text.strip().lower())


def detect_intent(message: str) -> str:
    """
    Detect the user's primary intent.

    Availability requests are routed to deterministic business logic.
    The local/offline version uses transparent rules rather than guessing.
    """
    text = normalize_text(message)

    availability_keywords = [
        "available",
        "availability",
        "vacancy",
        "book a room",
        "rooms for",
        "room for",
        "check availability",
        "is there a room",
        "do you have a room",
        "do you have rooms",
    ]

    if any(keyword in text for keyword in availability_keywords):
        return "availability"

    date_pattern = r"\d{4}-\d{2}-\d{2}"
    guest_pattern = r"\d+\s*(?:guest|guests|adult|adults|people|person)"

    if (
        re.search(date_pattern, text)
        and re.search(guest_pattern, text)
        and (
            "from" in text
            or "to" in text
            or "until" in text
            or "-" in text
        )
    ):
        return "availability"

    return "hotel_information"


def get_grounding_data() -> dict[str, Any]:
    """Load the hotel knowledge base used to ground responses."""
    return load_hotel_data()


def answer_hotel_question(message: str) -> str | None:
    """
    Answer common hotel questions using only the hotel knowledge base.

    Returns None when the knowledge base does not support an answer.
    """
    data = get_grounding_data()
    hotel = data["hotel"]
    rooms = data["rooms"]
    amenities = data["amenities"]
    dining = data["dining"]
    policies = data["policies"]
    accessibility = data["accessibility"]
    check_in_requirements = data["check_in_requirements"]

    text = normalize_text(message)

    # Check-in / check-out
    if "check-in" in text or "check in" in text:
        return (
            f"Check-in is from {hotel['check_in']}. "
            f"Front desk service is available {hotel['front_desk']}."
        )

    if "check-out" in text or "check out" in text:
        return f"Check-out is by {hotel['check_out']}."

    # Wi-Fi
    if "wifi" in text or "wi-fi" in text or "internet" in text:
        wifi = hotel["wifi"]

        if wifi["available"] and wifi["complimentary"]:
            return (
                f"Yes. Complimentary Wi-Fi is available "
                f"{wifi['coverage'].lower()}."
            )

    # Parking
    if "parking" in text or "car park" in text:
        parking = hotel["parking"]

        if parking["available"]:
            return (
                f"Yes. Parking is complimentary and available "
                f"{parking['notes'].lower()}."
            )

    # Swimming pool
    if (
        "pool" in text
        or "swimming" in text
        or "swimming pool" in text
    ):
        pool = amenities["swimming_pool"]

        if pool["available"]:
            return (
                f"Yes. The swimming pool is on the {pool['location']} "
                f"and is open {pool['hours']}."
            )

    # Fitness centre
    if (
        "gym" in text
        or "fitness" in text
        or "fitness centre" in text
    ):
        fitness = amenities["fitness_centre"]

        if fitness["available"]:
            return (
                f"Yes. The fitness centre is on the {fitness['location']} "
                f"and is open {fitness['hours']}."
            )

    # Breakfast
    if "breakfast" in text:
        breakfast = dining["breakfast"]

        if any(
            phrase in text
            for phrase in [
                "free breakfast",
                "complimentary breakfast",
                "breakfast included",
                "breakfast include",
            ]
        ):
            complimentary = ", ".join(breakfast["complimentary_rooms"])
            return (
                f"Breakfast is complimentary with these room types: "
                f"{complimentary}. For other room types, a paid breakfast "
                f"option is available. Breakfast hours are {breakfast['hours']}."
            )

        return (
            f"Breakfast is served from {breakfast['hours']}. "
            f"It is complimentary with Premium King and Family Suite, "
            f"while a paid option is available for Deluxe King and Deluxe Twin."
        )

    # Restaurant
    if (
        "restaurant" in text
        or "dining" in text
        or "lunch" in text
        or "dinner" in text
    ):
        restaurant = dining["restaurant"]

        return (
            f"The hotel restaurant serves breakfast from "
            f"{restaurant['breakfast']}, lunch from {restaurant['lunch']}, "
            f"and dinner from {restaurant['dinner']}."
        )

    # Cancellation
    if "cancel" in text or "cancellation" in text:
        cancellation = policies["cancellation"]

        return (
            f"Free cancellation is available {cancellation['free_cancellation']}. "
            f"{cancellation['late_cancellation']}. "
            f"For a no-show, {cancellation['no_show']}."
        )

    # Early check-in
    if "early check" in text:
        return policies["early_check_in"]

    # Late check-out
    if "late check" in text:
        return policies["late_check_out"]

    # Children
    if (
        "child" in text
        or "children" in text
        or "kid" in text
        or "kids" in text
    ):
        return policies["children"]

    # Pets
    if "pet" in text or "dog" in text or "cat" in text:
        return policies["pets"]

    # Smoking
    if "smok" in text:
        return policies["smoking"]

    # Accessibility
    if (
        "accessible" in text
        or "wheelchair" in text
        or "disability" in text
        or "disabled" in text
    ):
        features = ", ".join(accessibility["features"])

        return (
            f"{accessibility['accessible_rooms']} "
            f"Accessibility features include {features}."
        )

    # Identification / check-in documents
    if (
        "id" in text
        or "identification" in text
        or "passport" in text
        or "document" in text
    ):
        return (
            f"{check_in_requirements['identification']} "
            f"{check_in_requirements['international_guests']}"
        )

    # Room information
    room_keywords = [
        "room",
        "suite",
        "king",
        "twin",
        "bed",
        "price",
        "rate",
        "cost",
    ]

    if any(keyword in text for keyword in room_keywords):
        for room in rooms:
            room_name = normalize_text(room["name"])

            if room_name in text:
                breakfast = (
                    "Breakfast included."
                    if room["breakfast_included"]
                    else "Breakfast is not included."
                )

                features = ", ".join(room["features"])

                return (
                    f"{room['name']} accommodates up to {room['capacity']} "
                    f"guests and has {room['bed_configuration']}. "
                    f"The rate is INR {room['price_per_night']:,} per night. "
                    f"{breakfast} Features include {features}."
                )

        if "room" in text or "suite" in text:
            room_summaries = []

            for room in rooms:
                room_summaries.append(
                    f"{room['name']} ({room['capacity']} guests, "
                    f"INR {room['price_per_night']:,}/night)"
                )

            return "Our room types are: " + "; ".join(room_summaries) + "."

    # Hotel identity/location
    if (
        "hotel" in text
        and (
            "where" in text
            or "location" in text
            or "located" in text
            or "name" in text
        )
    ):
        return (
            f"{hotel['name']} is located in {hotel['location']}. "
            f"{hotel['tagline']}"
        )

    return None


def build_availability_response(
    check_in: date,
    check_out: date,
    guests: int,
) -> dict[str, Any]:
    """
    Run the deterministic availability tool and return structured results.
    """
    rooms = check_availability(
        check_in=check_in,
        check_out=check_out,
        guests=guests,
    )

    return {
        "check_in": check_in,
        "check_out": check_out,
        "guests": guests,
        "rooms": rooms,
    }


def generate_fallback_response() -> str:
    """Return a safe response when the knowledge base cannot answer."""
    return (
        "I can help with StayMate Grand Hotel information such as "
        "check-in and check-out, rooms, breakfast, Wi-Fi, parking, "
        "pool, fitness centre, cancellation, accessibility, pets, "
        "smoking, and room eligibility. I don't have enough information "
        "in the hotel knowledge base to answer that question reliably."
    )