# StayMate AI — Engineering & Product Decisions

## 1. Customer Problem

Hotel guests usually want quick answers to simple practical questions, for example:

- What time is check-in?
- Is breakfast included?
- What rooms can fit my group?
- What amenities are available?
- What are the cancellation rules?

For this project, I wanted the guest to get these answers through one conversation instead of searching through different hotel pages or documents.

For availability questions, the assistant should collect the information it needs and then return the room types that match the request.

---

## 2. Guest Journey

The main guest flow I designed is:

```text
Open assistant
    ↓
Ask a hotel question
    ↓
Receive an answer based on hotel data
    ↓
Ask a follow-up question
    ↓
If checking availability:
    ↓
Provide dates + number of guests
    ↓
Receive eligible room options
```

I wanted this to feel like one continuous conversation rather than making the guest fill out a separate form for every task.

---

## 3. Why a Conversational UI?

A chat interface made sense for this use case because guests can ask the same thing in different ways.

For example:

- "What time can I check in?"
- "When is check-in?"
- "What time does check-in start?"

All of these should lead to the same hotel information.

Availability can also be asked naturally, for example:

> "Do you have a room from 2026-09-25 to 2026-09-27 for 3 guests?"

The chat layer can understand the request, while the backend still validates the important information before returning a result.

---

## 4. Frontend Decision

### Chosen technology

The frontend uses:

- Next.js
- React
- TypeScript
- Tailwind CSS

### Why

I chose Next.js and React because they give me a straightforward way to build the chat interface, manage conversation state, connect to the backend API, and handle loading and error states.

TypeScript is useful because the frontend receives structured responses from the backend. Having explicit types makes it easier to keep the UI and API response formats consistent.

I also kept the interface focused on the main guest task instead of adding unnecessary screens.

---

## 5. Backend Decision

### Chosen technology

The backend uses:

- Python
- FastAPI
- Pydantic

### Why

FastAPI worked well for this project because it provides clear API definitions, request validation, automatic API documentation, and a lightweight structure.

Python also made it easy to keep the hotel-data lookup and availability logic in small modules that can be tested separately.

---

## 6. Hotel Knowledge Base Decision

The hotel information is stored in:

```text
backend/data/hotel.json
```

I used a JSON file instead of a database because this is a small prototype for the assignment. A database would add extra setup without providing much benefit for the current scope.

The JSON contains:

- hotel details;
- room types;
- room capacities;
- prices;
- amenities;
- dining information;
- policies;
- accessibility information;
- frequently asked questions.

One benefit of this approach is that I can easily see and change the source information.

A production version could replace this file with a database or a hotel/PMS data source without needing to change the overall guest conversation flow.

> **Important:** The hotel data is mock/demo data created for this assignment.

---

## 7. AI vs. Deterministic Logic

One of the main design decisions was to keep conversational handling separate from important hotel business rules.

### Conversational responsibilities

The chat layer handles things such as:

- identifying the type of guest request;
- recognizing availability questions;
- extracting supported information from the message;
- detecting missing information;
- deciding what response to return;
- providing a fallback when the request is unsupported.

### Deterministic responsibilities

The service layer handles:

- date validation;
- guest-count validation;
- room capacity rules;
- hotel-data lookup;
- availability eligibility.

I made this separation because business rules should not depend on an uncertain model response.

For example, if the hotel data says a room has a capacity of two, I don't want a model deciding that the room can somehow accommodate three guests.

---

## 8. Current AI Implementation

The current local version does not depend on a paid external LLM API.

Instead, `ai_service.py` provides a deterministic conversational decision layer. It:

1. normalizes the guest message;
2. detects supported intents;
3. extracts supported availability information;
4. asks for missing information when needed;
5. calls the deterministic availability service;
6. returns hotel information from the configured knowledge base;
7. gives a safe fallback for unsupported questions.

I chose this approach so the project could run locally and be deployed without requiring paid API credentials.

### Limitation

The assignment describes an AI-powered assistant and asks for appropriate LLM use. The current implementation is therefore intentionally transparent about its limitation: it does not make a live external LLM call.

For a production version, I could add an external or self-hosted LLM for natural-language intent detection and structured extraction while keeping the important business logic deterministic.

---

## 9. Hallucination Prevention

The main approach I used to reduce hallucinations is to ground hotel answers in the configured hotel knowledge base.

If the system does not have enough information to support a request, it should use a fallback instead of making up an answer.

For example, if someone asks about a private helicopter service that is not in the hotel data, the assistant should not invent one.

This matters especially for:

- prices;
- hotel policies;
- room features;
- amenities;
- availability;
- cancellation rules.

---

## 10. Missing Information

An availability request needs:

- check-in date;
- check-out date;
- number of guests.

If a guest only asks:

> "Do you have a room?"

the system should not guess the dates or number of guests.

Instead, it asks the guest for the missing information.

This keeps the conversation useful without silently making assumptions.

---

## 11. Structured API Responses

The chat API returns structured information instead of only returning plain text.

A response can contain:

- assistant message;
- response type;
- availability data;
- updated conversation context.

This makes the frontend easier to control because it does not have to try to extract structured information from a text response.

For example:

```text
response_type = availability
```

tells the frontend that it can render room availability information in the appropriate UI.

---

## 12. Error Philosophy

I wanted the system to fail clearly rather than pretend that something worked.

### Unsupported request

Return a clear fallback instead of inventing information.

### Missing availability information

Ask the guest for the missing values.

### Invalid dates

Reject invalid date ranges instead of running an availability lookup.

### Frontend/API failure

Show an error state so the guest knows that the request was not completed.

The important point is that uncertain information should not be presented as confirmed hotel information.

---

## 13. Availability Tradeoff

The current availability implementation is intentionally simple.

The hotel JSON contains room capacities, but it does not contain real date-specific room inventory.

Because of that, the current availability function validates the date range and returns room types that can accommodate the requested number of guests.

This is enough to demonstrate:

- API design;
- validation;
- service/tool calling;
- structured results;
- frontend integration.

However, this should not be described as real-time hotel inventory.

A production version would connect the availability service to a database, PMS, or another inventory provider.

---

## 14. Production Improvements

If I were taking this prototype further, I would work on these areas first.

### Real inventory

Replace capacity-only matching with date-specific inventory from a hotel PMS or database.

### LLM integration

Use an external or self-hosted LLM for more flexible natural-language intent detection and structured extraction.

### Tool calling

Expose deterministic backend functions such as:

```text
checkAvailability(checkIn, checkOut, adults)
```

as controlled tools for the conversational layer.

### Booking workflow

Add a separate booking service instead of allowing a model to directly create reservations.

### Authentication

Associate conversations and bookings with authenticated users when required.

### Observability

Add structured logs, metrics, tracing, and alerts for:

- API failures;
- model failures;
- tool failures;
- latency;
- fallback frequency.

### Persistent conversations

Store conversation state if the product needs guests to continue their conversation across sessions.

### Security

Use server-side secret management, strict CORS, rate limiting, input validation, and suitable access controls.

---

## 15. Measuring Usefulness

For a real product, I would look at several measurements instead of relying on one number.

Useful metrics could include:

- percentage of guest questions answered successfully;
- fallback rate;
- availability-request completion rate;
- number of conversations requiring repeated clarification;
- API response latency;
- frontend error rate;
- tool/service failure rate;
- guest satisfaction feedback;
- successful completion of the intended guest task.

These measurements would help show whether the assistant is actually helping guests rather than just producing responses.

---

## 16. AI Tools Used During Development

I used AI assistance during development for things such as:

- planning the application structure;
- discussing implementation ideas;
- reviewing code;
- creating test cases;
- improving documentation;
- identifying edge cases;
- refining the conversational UI.

I still tested the resulting implementation locally and verified the main application flows. The goal was to use AI as a development aid, not to include code or decisions that I could not explain.

---

## 17. Engineering Principle

The main principle behind the project is:

> **Keep the guest experience conversational, but keep important hotel business rules explicit, deterministic, testable, and grounded in trusted data.**

That gives the assistant a natural interface while keeping important parts of the system predictable.
