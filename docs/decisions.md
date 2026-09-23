# StayMate AI — Engineering & Product Decisions

## 1. Customer Problem

Hotel guests frequently need quick answers to practical questions such as:

- What time is check-in?
- Is breakfast included?
- What rooms are available for my group?
- What amenities does the hotel have?
- What are the cancellation rules?

The product goal is to provide these answers through a conversational interface rather than requiring guests to search through multiple hotel pages or documents.

For availability requests, the assistant should collect the required information and return relevant room options.

---

## 2. Guest Journey

The intended guest journey is:

```text
Open assistant
    ↓
Ask a hotel question
    ↓
Receive a grounded answer
    ↓
Ask follow-up questions
    ↓
If checking availability:
    ↓
Provide dates + number of guests
    ↓
Receive eligible room options
```

The experience is designed to feel like a single conversation rather than a collection of separate forms.

---

## 3. Why a Conversational UI?

A conversational interface is appropriate because hotel guests may express the same need in many different ways.

For example:

- "What time can I check in?"
- "When is check-in?"
- "What time does check-in start?"

These questions should map to the same hotel information.

For availability, guests may also naturally ask:

> "Do you have a room from 2026-09-25 to 2026-09-27 for 3 guests?"

The chat interface allows the product to handle this natural-language interaction while still using structured validation behind the scenes.

---

## 4. Frontend Decision

### Chosen technology

The frontend uses:

- Next.js
- React
- TypeScript
- Tailwind CSS

### Why

Next.js and React provide a straightforward way to build:

- a responsive conversational interface;
- reusable UI components;
- client-side conversation state;
- API integration;
- loading and error states.

TypeScript helps make the frontend API data structures explicit and reduces accidental mismatches between the UI and backend responses.

The interface was intentionally kept focused on the guest task instead of adding unnecessary screens.

---

## 5. Backend Decision

### Chosen technology

The backend uses:

- Python
- FastAPI
- Pydantic

### Why

FastAPI provides:

- clear HTTP API definitions;
- request validation;
- useful automatic API documentation;
- a lightweight structure suitable for the assignment;
- good separation between API routes and service logic.

Python also makes it simple to keep hotel-data processing and deterministic availability logic in small, testable modules.

---

## 6. Hotel Knowledge Base Decision

The hotel information is stored in:

```text
backend/data/hotel.json
```

This was chosen instead of introducing a database because the assignment is a small local prototype.

The JSON file contains structured information about:

- hotel details;
- room types;
- room capacities;
- prices;
- amenities;
- dining;
- policies;
- accessibility;
- frequently asked questions.

This makes the source of truth easy to inspect and modify.

A production system could replace this with a database or a hotel/PMS data source without changing the overall frontend conversation flow.

> **Important:** The hotel data is mock/demo data created for this assignment.

---

## 7. AI vs. Deterministic Logic

One of the most important engineering decisions is to separate conversational interpretation from business-critical logic.

### Conversational responsibilities

The chat layer handles:

- identifying the type of guest request;
- recognizing availability-related questions;
- extracting supported information from natural language;
- detecting missing information;
- generating an appropriate response;
- providing a safe fallback for unsupported requests.

### Deterministic responsibilities

The service layer handles:

- date validation;
- guest-count validation;
- room capacity rules;
- hotel-data lookup;
- availability eligibility.

This prevents business-critical rules from depending on an uncertain model response.

For example, the system should not ask a model to decide whether a room can accommodate three guests when the room capacity is already explicitly defined in the hotel data.

---

## 8. Current AI Implementation

The current local version does not depend on a paid external LLM API.

Instead, `ai_service.py` provides a deterministic conversational decision layer that:

1. normalizes the guest message;
2. detects supported intents;
3. extracts supported availability information;
4. requests missing information when necessary;
5. calls the deterministic availability service;
6. returns hotel information from the configured knowledge base;
7. provides a safe fallback for unsupported questions.

This approach keeps the project runnable without requiring paid services or API credentials.

### Limitation

The assignment describes an AI-powered assistant and asks for appropriate LLM use. The current implementation is therefore intentionally transparent about its limitation: it does not make a live external LLM call.

A production implementation could replace or extend the intent/extraction layer with an LLM while retaining the deterministic business services.

---

## 9. Hallucination Prevention

The main hallucination-prevention strategy is grounding.

Hotel answers should come from the configured hotel knowledge base rather than invented facts.

If the system cannot support a request from the available data, it uses a fallback response.

For example, a question about a private helicopter service should not result in the assistant inventing such a service.

This principle is particularly important for:

- prices;
- hotel policies;
- room features;
- amenities;
- availability;
- cancellation rules.

---

## 10. Missing Information

Availability requests require:

- check-in date;
- check-out date;
- number of guests.

If a guest asks:

> "Do you have a room?"

the system should not guess the dates or number of guests.

Instead, it asks the guest to provide the missing information.

This keeps the conversation useful without silently making assumptions.

---

## 11. Structured API Responses

The chat API returns structured information rather than only plain text.

A response can include:

- assistant message;
- response type;
- availability data;
- updated conversation context.

This allows the frontend to make UI decisions based on explicit backend data.

For example:

```text
response_type = availability
```

allows the frontend to render room cards instead of trying to parse availability information from a text response.

---

## 12. Error Philosophy

The product should fail safely.

### Unsupported request

Return a clear fallback rather than inventing information.

### Missing availability information

Ask for the missing values.

### Invalid dates

Reject invalid date ranges rather than attempting an availability lookup.

### Frontend/API failure

Show a visible error state so the guest knows the request was not completed.

The system should avoid presenting uncertain or fabricated information as confirmed hotel information.

---

## 13. Availability Tradeoff

The current availability implementation intentionally uses a simple mock model.

The hotel data contains room capacities, but does not contain real date-specific inventory.

Therefore the current function validates the date range and returns room types that can accommodate the requested number of guests.

This is useful for demonstrating:

- API design;
- validation;
- tool/service calling;
- structured results;
- frontend integration.

However, it should not be represented as real-time hotel inventory.

A production implementation would connect the availability service to a database, PMS, or inventory provider.

---

## 14. Production Improvements

If the prototype were taken toward production, the following areas would be prioritized:

### Real inventory

Replace capacity-only matching with date-specific inventory from a hotel PMS or database.

### LLM integration

Use an external or self-hosted LLM for robust natural-language intent detection and structured extraction.

### Tool calling

Expose deterministic backend functions such as:

```text
checkAvailability(checkIn, checkOut, adults)
```

as controlled tools available to the conversational layer.

### Booking workflow

Add a separate booking service rather than allowing a model to directly create reservations.

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

Store conversation state when the product requires continuity across sessions.

### Security

Use server-side secret management, strict CORS, rate limiting, input validation, and appropriate access controls.

---

## 15. Measuring Usefulness

Useful product measurements could include:

- percentage of guest questions answered successfully;
- fallback rate;
- availability-request completion rate;
- percentage of conversations requiring repeated clarification;
- API response latency;
- frontend error rate;
- tool/service failure rate;
- guest satisfaction feedback;
- successful completion of the intended guest task.

These metrics should be evaluated together rather than relying on a single metric.

---

## 16. AI Tools Used During Development

AI assistance was used during development for tasks such as:

- planning the application structure;
- drafting implementation ideas;
- reviewing code;
- creating test cases;
- improving documentation;
- identifying edge cases;
- refining the conversational UI.

The resulting implementation was tested locally and should be understood by the developer rather than treated as an unexplained generated artifact.

---

## 17. Engineering Principle

The overall design follows this principle:

> **Keep the guest experience conversational, but keep important hotel business rules explicit, deterministic, testable, and grounded in trusted data.**

This creates a useful balance between a natural guest experience and predictable software behavior.
