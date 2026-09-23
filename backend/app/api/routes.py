import logging
from datetime import date

from fastapi import APIRouter, HTTPException

from app.models import (
    AvailabilityRequest,
    ChatMessage,
    ChatRequest,
    ChatResponse,
)
from app.services.ai_service import (
    answer_hotel_question,
    build_availability_response,
    detect_intent,
    generate_fallback_response,
)
from app.services.availability import check_availability
from app.services.hotel_service import get_hotel_info, get_rooms

router = APIRouter(prefix="/api")

logger = logging.getLogger(__name__)


@router.get("/hotel")
def hotel_info():
    """Return basic hotel information."""
    return get_hotel_info()


@router.get("/rooms")
def rooms():
    """Return all room types."""
    return get_rooms()


@router.post("/availability")
def availability(request: AvailabilityRequest):
    """Find rooms that can accommodate the requested guests."""

    rooms = check_availability(
        check_in=request.check_in,
        check_out=request.check_out,
        guests=request.guests,
    )

    return {
        "check_in": request.check_in,
        "check_out": request.check_out,
        "guests": request.guests,
        "rooms": rooms,
    }


@router.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    """
    Process a guest message using the hotel knowledge base.

    The current implementation is intentionally grounded in the local
    hotel knowledge base and deterministic business logic. A real LLM
    provider can be plugged into the AI service later without changing
    the frontend API contract.
    """
    try:
        intent = detect_intent(request.message)

        # Availability requires structured information that should not
        # be guessed by an AI model.
        if intent == "availability":
            return _handle_availability_message(request)

        answer = answer_hotel_question(request.message)

        if answer is None:
            answer = generate_fallback_response()
            response_type = "fallback"
        else:
            response_type = "hotel_information"

        conversation = list(request.conversation)
        conversation.append(
            ChatMessage(
                role="user",
                content=request.message,
            )
        )
        conversation.append(
            ChatMessage(
                role="assistant",
                content=answer,
            )
        )

        return ChatResponse(
            message=answer,
            response_type=response_type,
            conversation=conversation[-10:],
            availability=None,
        )

    except Exception:
        logger.exception("Unexpected error while processing chat request.")
        raise HTTPException(
            status_code=500,
            detail="The assistant could not process your request.",
        )


def _handle_availability_message(request: ChatRequest) -> ChatResponse:
    """
    Handle availability questions.

    The current version requires explicit check-in, check-out and guest
    information rather than guessing missing booking details.
    """
    parsed = _extract_availability_details(request.message)

    if parsed is None:
        message = (
            "I can check room eligibility for your stay. "
            "Please provide your check-in date, check-out date, "
            "and number of guests. For example: "
            "'September 25 to September 27 for 3 guests.'"
        )

        conversation = list(request.conversation)
        conversation.append(
            ChatMessage(
                role="user",
                content=request.message,
            )
        )
        conversation.append(
            ChatMessage(
                role="assistant",
                content=message,
            )
        )

        return ChatResponse(
            message=message,
            response_type="needs_information",
            conversation=conversation[-10:],
            availability=None,
        )

    check_in, check_out, guests = parsed

    try:
        availability_result = build_availability_response(
            check_in=check_in,
            check_out=check_out,
            guests=guests,
        )
    except ValueError as exc:
        message = str(exc)

        conversation = list(request.conversation)
        conversation.append(
            ChatMessage(
                role="user",
                content=request.message,
            )
        )
        conversation.append(
            ChatMessage(
                role="assistant",
                content=message,
            )
        )

        return ChatResponse(
            message=message,
            response_type="validation_error",
            conversation=conversation[-10:],
            availability=None,
        )

    rooms = availability_result["rooms"]

    if rooms:
        room_names = ", ".join(room["name"] for room in rooms)

        message = (
            f"For {guests} guest"
            f"{'s' if guests != 1 else ''}, the eligible room type"
            f"{'s are' if len(rooms) != 1 else ' is'}: {room_names}. "
            "The current demo knowledge base checks room capacity; "
            "it does not contain live date-specific inventory."
        )
    else:
        message = (
            f"I couldn't find a room type in the current hotel data "
            f"that can accommodate {guests} guest"
            f"{'s' if guests != 1 else ''}."
        )

    conversation = list(request.conversation)
    conversation.append(
        ChatMessage(
            role="user",
            content=request.message,
        )
    )
    conversation.append(
        ChatMessage(
            role="assistant",
            content=message,
        )
    )

    return ChatResponse(
        message=message,
        response_type="availability",
        conversation=conversation[-10:],
        availability=availability_result,
    )


def _extract_availability_details(
    message: str,
) -> tuple[date, date, int] | None:
    """
    Extract simple ISO-date availability details.

    Supported format:
        2026-09-25 to 2026-09-27 for 3 guests

    We deliberately avoid guessing dates from ambiguous natural language.
    """
    import re

    match = re.search(
        r"(\d{4}-\d{2}-\d{2})"
        r"\s*(?:to|-|until)\s*"
        r"(\d{4}-\d{2}-\d{2})"
        r".*?"
        r"(\d+)\s*(?:guest|guests|adult|adults|people|person)",
        message.lower(),
    )

    if not match:
        return None

    try:
        check_in = date.fromisoformat(match.group(1))
        check_out = date.fromisoformat(match.group(2))
        guests = int(match.group(3))
    except ValueError:
        return None

    return check_in, check_out, guests