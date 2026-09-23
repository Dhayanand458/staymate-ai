from datetime import date

from pydantic import BaseModel, Field, model_validator


class AvailabilityRequest(BaseModel):
    check_in: date
    check_out: date
    guests: int = Field(..., ge=1, le=20)

    @model_validator(mode="after")
    def validate_dates(self):
        if self.check_out <= self.check_in:
            raise ValueError("Check-out date must be after check-in date.")

        return self


class ChatMessage(BaseModel):
    role: str = Field(..., pattern="^(user|assistant)$")
    content: str = Field(..., min_length=1, max_length=4000)


class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1, max_length=4000)
    conversation: list[ChatMessage] = Field(default_factory=list)

    @model_validator(mode="after")
    def limit_conversation(self):
        if len(self.conversation) > 20:
            raise ValueError("Conversation history cannot exceed 20 messages.")

        return self


class ChatResponse(BaseModel):
    message: str
    response_type: str
    conversation: list[ChatMessage]
    availability: dict | None = None