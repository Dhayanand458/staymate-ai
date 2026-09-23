# StayMate AI — Architecture

## 1. Overview

StayMate AI is a full-stack hotel guest assistant designed to answer hotel questions and help guests check room availability through a conversational interface.

The application is split into two independently runnable parts:

- **Frontend:** Next.js + React + TypeScript
- **Backend:** FastAPI + Python
- **Knowledge base:** Local JSON hotel data
- **Availability logic:** Deterministic Python service
- **Conversation handling:** Backend chat endpoint with structured responses

The frontend never calls an AI provider directly. It sends guest messages to the backend API, which owns the hotel data, business rules, validation, and response generation.

> **Demo data note:** The hotel information in this project is mock data created for the assignment. It represents a fictional StayMate Grand Hotel and should not be treated as real hotel information.

---

## 2. High-Level Architecture

```text
┌───────────────────────────────┐
│        Guest / Browser        │
└───────────────┬───────────────┘
                │
                │ HTTP / JSON
                ▼
┌───────────────────────────────┐
│      Next.js Frontend         │
│                               │
│  • Chat UI                    │
│  • Conversation state         │
│  • Loading / error states     │
│  • Availability form          │
│  • Availability result cards  │
└───────────────┬───────────────┘
                │
                │ POST /api/chat
                │ POST /api/availability
                ▼
┌───────────────────────────────┐
│        FastAPI Backend        │
│                               │
│  • Request validation         │
│  • API routes                 │
│  • Chat orchestration         │
│  • Structured responses       │
└───────────────┬───────────────┘
                │
       ┌────────┴─────────┐
       ▼                  ▼
┌───────────────┐  ┌────────────────┐
│ Hotel Service │  │ Availability   │
│               │  │ Service        │
│ hotel.json    │  │ deterministic  │
│ room data     │  │ room matching  │
│ policies      │  │ by capacity    │
└───────────────┘  └────────────────┘
```
---

## 3. Frontend Architecture

The frontend is implemented with Next.js and React.

The main chat page is responsible for:

- displaying the hotel assistant interface;
- storing the current conversation in React state;
- submitting guest messages to the backend;
- showing assistant responses;
- displaying loading indicators while waiting for the backend;
- showing API/network errors;
- collecting availability information;
- displaying available room types;
- supporting follow-up questions within the same conversation.

The frontend uses the backend API rather than calling an AI service directly. This keeps API/business logic out of the browser and prevents server-side configuration or credentials from being exposed.

### Main frontend flow

```text
Guest enters message
        ↓
React state updates
        ↓
POST /api/chat
        ↓
Backend processes request
        ↓
Structured JSON response
        ↓
React updates conversation
        ↓
Assistant message displayed
```

---

## 4. Backend Architecture

The backend uses FastAPI.

### Main layers

```text
app/
├── main.py
├── models.py
├── api/
│   └── routes.py
└── services/
    ├── ai_service.py
    ├── availability.py
    └── hotel_service.py
```

### `main.py`

Creates the FastAPI application and configures:

- application metadata;
- CORS for the local frontend;
- API routes;
- health check endpoint.

### `models.py`

Defines validated request/response-related data structures used by the API, including availability input and chat-related models.

### `api/routes.py`

Exposes HTTP endpoints such as:

- `GET /api/health`
- `GET /api/hotel`
- `GET /api/rooms`
- `POST /api/availability`
- `POST /api/chat`

The route layer handles HTTP concerns and delegates hotel and availability logic to service modules.

---

## 5. Service Layer

### Hotel service

`hotel_service.py` loads the local hotel knowledge base from:

```text
backend/data/hotel.json
```

It provides functions for:

- loading hotel information;
- retrieving room types;
- finding a room by name;
- finding rooms that can accommodate a requested number of guests.

Keeping this logic in a service module avoids putting file-access logic directly inside API routes.

### Availability service

`availability.py` provides the deterministic availability function:

```text
check_availability(check_in, check_out, guests)
```

The function validates the date range and guest count and returns room types whose configured capacity can accommodate the requested number of guests.

The current dataset does **not** contain date-specific room inventory. Therefore, the current implementation is a deterministic **room eligibility/capacity check**, rather than a live inventory system.

This limitation is intentionally disclosed in the UI and documentation.

### Chat service

`ai_service.py` handles the conversational decision layer.

The current local implementation:

1. normalizes the guest message;
2. detects the likely request type;
3. checks hotel knowledge-base information;
4. detects availability requests;
5. extracts supported availability information from the message;
6. asks for missing availability information when required;
7. calls the deterministic availability service for complete requests;
8. returns a safe fallback when the requested information is not supported;
9. preserves conversation context in the API response.

The current version does not require a paid external LLM API.

---

## 6. Request Flow: Hotel Question

Example:

> "What time is check-in?"

```text
Frontend
   │
   │ POST /api/chat
   ▼
FastAPI route
   │
   ▼
Chat service
   │
   ├── Detect hotel-information intent
   │
   └── Read hotel knowledge base
   │
   ▼
Structured response
   │
   ▼
Frontend
   │
   ▼
Assistant message
```

The response is generated from the configured hotel data rather than from an unsupported assumption.

---

## 7. Availability Flow

Example:

> "Do you have a room from 2026-09-25 to 2026-09-27 for 3 guests?"

The backend extracts:

- check-in: `2026-09-25`
- check-out: `2026-09-27`
- guests: `3`

It then calls the deterministic availability function.

For the current mock dataset, the Family Suite is the room type with sufficient capacity for three guests.

```text
Guest message
      ↓
Availability intent detected
      ↓
Dates + guest count extracted
      ↓
Input validation
      ↓
check_availability(...)
      ↓
Room capacity filtering
      ↓
Structured availability result
      ↓
Frontend room cards
```

If required information is missing, the assistant asks for it instead of inventing values.

---

## 8. Conversation Context

The frontend keeps the conversation messages and sends recent conversation context to the backend.

This allows follow-up interactions such as:

```text
Guest:
What rooms do you have?

Assistant:
Our room types include Deluxe King, Deluxe Twin,
Premium King and Family Suite.

Guest:
Is breakfast included?
```

The backend receives the previous messages along with the new question, allowing the conversation to remain coherent.

The frontend limits the submitted context to recent messages rather than sending an unlimited conversation history.

---

## 9. Grounding and Hallucination Prevention

The assistant is intentionally constrained by the hotel knowledge base.

For supported hotel information, responses are based on:

```text
backend/data/hotel.json
```

For unsupported requests, the assistant returns a safe fallback rather than inventing hotel capabilities.

For example, if a guest asks about a service that is not represented in the knowledge base, the assistant explains that the information is not available in the current hotel knowledge base.

This is preferable to confidently inventing hotel facilities, policies, prices, or services.

---

## 10. Deterministic Business Logic vs. AI

A key design decision is to keep business-critical logic outside the conversational layer.

### Conversational layer

Suitable for:

- understanding the guest's natural-language request;
- identifying likely intent;
- extracting simple supported information;
- deciding when information is missing;
- producing a conversational response.

### Deterministic layer

Used for:

- date validation;
- guest-count validation;
- room capacity rules;
- reading configured hotel data;
- availability calculation.

This separation makes important business rules testable and predictable.

For a production implementation with an external LLM, the model could be used as an intent/extraction layer while deterministic services would still remain responsible for actual business decisions.

---

## 11. Error Handling

The application handles errors at multiple levels.

### Frontend

The UI provides:

- loading indicators;
- disabled send state while a request is in progress;
- visible request-error messages;
- a retry path through the chat input;
- empty conversation handling.

### Backend

The API uses request validation and structured JSON responses.

Invalid availability requests are rejected through validation rather than silently accepting incorrect values.

Unsupported questions receive a safe fallback instead of fabricated information.

---

## 12. CORS

During local development, the backend allows requests from the Next.js development server:

```text
http://localhost:3000
http://127.0.0.1:3000
```

This allows the browser frontend to communicate with the FastAPI backend running on port `8000`.

For production, the allowed origins should be restricted to the actual deployed frontend domain.

---

## 13. Current Availability Limitation

The current mock knowledge base contains room capacities and room details, but not real date-specific inventory.

Therefore:

```text
Requested dates
      ↓
Date range is validated
      ↓
Room capacity is checked
      ↓
Eligible room types are returned
```

The system should not be described as checking real hotel inventory.

A production version could replace the current service with a database or hotel PMS/channel-manager integration:

```text
Frontend
   ↓
FastAPI
   ↓
Availability service
   ↓
Hotel database / PMS / inventory provider
   ↓
Real date-specific availability
```

The API contract could remain similar, reducing the impact of that future change on the frontend.

---

## 14. Production Evolution

A production architecture could evolve to:

```text
Guest
  ↓
Web / Mobile UI
  ↓
API Gateway
  ↓
Conversation Orchestrator
  ├── LLM / intent extraction
  ├── Hotel knowledge retrieval
  ├── Availability tool
  ├── Booking tool
  └── Policy tools
          ↓
  Hotel PMS / database
```

Additional production concerns would include:

- authentication and authorization;
- rate limiting;
- structured logging;
- monitoring and tracing;
- secret management;
- persistent conversation storage;
- real hotel inventory;
- booking and cancellation workflows;
- stronger input validation;
- observability for model/tool failures;
- automated evaluation of conversational quality.

---

## 15. Design Principle

The central architecture principle is:

> **Use conversational intelligence for understanding the guest, but keep business-critical decisions deterministic and grounded in hotel data.**

This reduces the risk of hallucinated hotel information while keeping the user experience conversational and simple.
