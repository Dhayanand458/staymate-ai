# StayMate AI — Hotel Guest Assistant

StayMate AI is a full-stack hotel guest assistant designed to help hotel guests quickly get answers about a property's rooms, amenities, policies, dining, and stay eligibility.

## Live Demo

- Frontend: https://dhayanand458.github.io/staymate-ai/
- Backend health: https://staymate-ai-backend-rdr0.onrender.com/api/health
- GitHub: https://github.com/Dhayanand458/staymate-ai

> The frontend is deployed on GitHub Pages and the FastAPI backend is deployed on Render.

This project was built as a practical software-engineering assignment using a Next.js/React frontend and a FastAPI/Python backend.

> **Implementation note:** The current project is a deployed assignment prototype using a deterministic conversational layer. It does not require a paid API or external LLM service. Hotel answers are grounded in the local JSON knowledge base, while availability and validation are handled by deterministic backend logic.

---

## 1. Product Overview

### Customer problem

Hotel guests often need quick answers to repetitive questions before or during a stay:

- What time is check-in?
- What time is check-out?
- Is breakfast included?
- Is Wi-Fi free?
- Is parking available?
- Is the swimming pool open?
- Are pets allowed?
- What rooms can accommodate a particular number of guests?
- What cancellation policy applies?

A hotel assistant should answer these questions quickly while avoiding unsupported claims.

### StayMate solution

StayMate provides a conversational interface where guests can:

1. Ask natural-language hotel questions.
2. Receive answers grounded in the hotel's knowledge base.
3. Ask follow-up questions within the same conversation.
4. Check room eligibility for a requested date range and number of guests.
5. Receive structured room information for availability-related requests.
6. Receive a controlled fallback when information is not available.
7. See clear loading and connection-error states.

---

# 2. Key Features

## Guest-facing features

- Conversational hotel assistant
- Responsive desktop and mobile UI
- Guest and assistant message bubbles
- Suggested questions
- Loading/typing state
- Backend connection error state
- New-chat/reset functionality
- Availability form
- Structured room availability cards
- Room capacity, bed configuration, pricing, features, and breakfast information
- Conversation context during the current session
- Clear explanation of the current demo availability limitation

## Backend features

- FastAPI REST API
- Hotel JSON knowledge base
- Hotel information endpoint
- Room information endpoint
- Availability endpoint
- Conversational `/api/chat` endpoint
- Deterministic intent routing
- Deterministic availability business logic
- Safe fallback for unsupported questions
- Missing-information handling
- Conversation context
- Input validation
- CORS configuration for local and deployed frontend
- Automated tests
- Swagger/OpenAPI documentation

---

# 3. Architecture

```text
┌────────────────────────────────────┐
│          Next.js Frontend          │
│                                    │
│  Chat UI                           │
│  Suggested Questions               │
│  Availability Form                 │
│  Loading / Error States             │
│  Availability Cards                │
└──────────────────┬─────────────────┘
                   │
                   │ HTTP / JSON
                   ▼
┌────────────────────────────────────┐
│           FastAPI Backend          │
│                                    │
│  /api/chat                         │
│  /api/availability                 │
│  /api/hotel                        │
│  /api/rooms                        │
│  /api/health                       │
└──────────────────┬─────────────────┘
                   │
          ┌────────┴─────────┐
          ▼                  ▼
┌─────────────────┐  ┌────────────────────┐
│ AI / Chat Layer │  │ Business Logic     │
│                 │  │                    │
│ Intent routing  │  │ Date validation    │
│ Grounded answer │  │ Guest validation   │
│ Fallback        │  │ Capacity checks    │
│ Context         │  │ Availability       │
└────────┬────────┘  └──────────┬─────────┘
         │                      │
         └──────────┬───────────┘
                    ▼
          ┌────────────────────┐
          │    hotel.json      │
          │                    │
          │ Hotel information  │
          │ Rooms              │
          │ Amenities          │
          │ Dining             │
          │ Policies           │
          │ FAQ                │
          └────────────────────┘
```

### Responsibility split

The frontend is responsible for presentation and user interaction.

The backend is responsible for:

- validation
- intent routing
- hotel knowledge retrieval
- deterministic availability logic
- structured responses
- fallback behavior

Business-critical availability decisions are deliberately kept outside conversational text generation.

---

# 4. Technology Stack

## Frontend

- Next.js 16.3.6
- React 19.2.8
- TypeScript
- Tailwind CSS 4

## Backend

- Python 3.11+
- FastAPI
- Pydantic
- Uvicorn
- pytest

## Data

The current demo uses:

```text
backend/data/hotel.json
```

No external database is required.

No paid API is required for the current implementation.

---

# 5. Project Structure

```text
staymate-ai/
│
├── backend/
│   ├── app/
│   │   ├── api/
│   │   │   └── routes.py
│   │   ├── services/
│   │   │   ├── ai_service.py
│   │   │   ├── availability.py
│   │   │   └── hotel_service.py
│   │   ├── main.py
│   │   └── models.py
│   │
│   ├── data/
│   │   └── hotel.json
│   │
│   ├── tests/
│   │   ├── test_api.py
│   │   ├── test_availability.py
│   │   └── test_hotel_service.py
│   │
│   └── requirements.txt
│
├── docs/
│
├── frontend/
│   ├── src/
│   │   └── app/
│   │       ├── globals.css
│   │       ├── layout.tsx
│   │       └── page.tsx
│   ├── public/
│   ├── package.json
│   └── ...
│
├── .env.example
├── .gitignore
├── README.md
└── ...
```

Generated directories such as `backend/.venv`, `frontend/node_modules`, `.next`, and Python cache directories should not be committed to Git.

---

# 6. Local Setup

## Prerequisites

Install:

- Node.js
- npm
- Python 3.11+
- Git

The current local implementation does not require a paid API key.

---

## 6.1 Clone the repository

```bash
git clone <your-repository-url>
cd staymate-ai
```

---

# 7. Backend Setup

Open a terminal in:

```text
backend/
```

## Create a virtual environment

### Windows PowerShell

```powershell
python -m venv .venv
```

Activate it:

```powershell
.\.venv\Scripts\Activate.ps1
```

## Install dependencies

```powershell
pip install -r requirements.txt
```

## Start the backend

```powershell
python -m uvicorn app.main:app --reload --port 8000
```

The API will be available at:

```text
http://127.0.0.1:8000
```

Swagger/OpenAPI documentation:

```text
http://127.0.0.1:8000/docs
```

Health check:

```text
http://127.0.0.1:8000/api/health
```

Expected response:

```json
{
  "status": "ok",
  "service": "staymate-ai-backend"
}
```

---

# 8. Frontend Setup

Open a second terminal in:

```text
frontend/
```

Install dependencies:

```powershell
npm install
```

Start the development server:

```powershell
npm run dev
```

The frontend will be available at:

```text
http://localhost:3000
```

The frontend communicates with the backend over HTTP.

The frontend does not contain backend secrets or API keys.

---

# 9. API Endpoints

## Health

```http
GET /api/health
```

Example:

```bash
curl http://127.0.0.1:8000/api/health
```

---

## Hotel information

```http
GET /api/hotel
```

Returns basic hotel information such as:

- hotel name
- location
- check-in
- check-out
- front desk
- Wi-Fi
- parking
- currency

---

## Rooms

```http
GET /api/rooms
```

Returns the room types in the hotel knowledge base.

---

## Availability

```http
POST /api/availability
```

Example request:

```json
{
  "check_in": "2026-09-25",
  "check_out": "2026-09-27",
  "guests": 3
}
```

Example response structure:

```json
{
  "check_in": "2026-09-25",
  "check_out": "2026-09-27",
  "guests": 3,
  "rooms": [
    {
      "id": "family-suite",
      "name": "Family Suite",
      "capacity": 4
    }
  ]
}
```

Invalid dates and invalid guest counts are rejected through backend validation.

---

# 10. Chat API

```http
POST /api/chat
```

Example request:

```json
{
  "message": "What time is check-in?",
  "conversation": []
}
```

Example response structure:

```json
{
  "message": "Check-in is from 3:00 PM. Front desk service is available 24/7.",
  "response_type": "hotel_information",
  "conversation": [
    {
      "role": "user",
      "content": "What time is check-in?"
    },
    {
      "role": "assistant",
      "content": "Check-in is from 3:00 PM. Front desk service is available 24/7."
    }
  ],
  "availability": null
}
```

---

# 11. Availability Conversation

A complete availability request can be sent conversationally.

Example:

```json
{
  "message": "Do you have a room from 2026-09-25 to 2026-09-27 for 3 guests?",
  "conversation": []
}
```

The backend:

1. Detects availability intent.
2. Extracts the requested dates and guest count.
3. Validates the request.
4. Calls deterministic availability logic.
5. Returns structured room information.
6. Allows the frontend to render an availability card.

The current demo returns room types that can accommodate the requested number of guests.

---

# 12. Conversation Context

The frontend sends recent conversation history to the backend.

Example:

```json
{
  "message": "Is breakfast included?",
  "conversation": [
    {
      "role": "user",
      "content": "What rooms do you have?"
    },
    {
      "role": "assistant",
      "content": "Our room types include Deluxe King, Deluxe Twin, Premium King and Family Suite."
    }
  ]
}
```

The backend returns the conversation along with the new assistant response.

The frontend limits the history sent to the backend to recent messages rather than sending an unlimited conversation.

---

# 13. AI / Conversational Approach

The project uses an AI-assistant style architecture while keeping business-critical hotel decisions deterministic.

The important distinction is:

### Conversational responsibilities

The chat layer handles:

- recognizing the user's request type
- selecting an appropriate response path
- using hotel knowledge
- handling missing information
- handling unsupported questions
- maintaining basic conversation context

### Deterministic responsibilities

Backend business logic handles:

- date validation
- guest-count validation
- room capacity
- availability eligibility
- structured room data

This separation makes the application predictable and testable.

### Why this approach?

Hotel availability is a business operation. It should not depend on a model inventing an answer.

For example:

```text
Guest:
I need a room for 3 guests.

Assistant:
→ determine missing dates
→ ask for check-in/check-out
```

After complete details are supplied:

```text
Guest:
25 Sep to 27 Sep, 3 guests.

Assistant
→ validate dates
→ call check_availability()
→ return Family Suite
```

The business result comes from deterministic code and the hotel data, not from generated guesswork.

---

# 14. Grounding and Hallucination Prevention

The current hotel knowledge base is:

```text
backend/data/hotel.json
```

It contains:

- hotel information
- room types
- room capacities
- room features
- amenities
- dining information
- policies
- accessibility information
- check-in requirements
- FAQs

The assistant should only make hotel claims supported by this data.

When the requested information is outside the knowledge base, the system uses a controlled fallback.

Example:

```text
Guest:
Does the hotel have a private helicopter service?

Assistant:
I can help with StayMate Grand Hotel information such as
check-in and check-out, rooms, breakfast, Wi-Fi, parking,
pool, fitness centre, cancellation, accessibility, pets,
smoking, and room eligibility. I don't have enough information
in the hotel knowledge base to answer that question reliably.
```

This is preferable to inventing a hotel service.

---

# 15. Missing Information Handling

For an incomplete availability request:

```text
Guest:
Do you have a room?
```

The system does not guess dates or guest count.

It asks for:

- check-in date
- check-out date
- number of guests

Example:

```text
I can check room eligibility for your stay. Please provide
your check-in date, check-out date, and number of guests.
```

This makes the booking workflow explicit and prevents fabricated availability requests.

---

# 16. Current Availability Model and Limitation

The current implementation is intentionally transparent about its availability model.

It uses room capacity eligibility.

Example:

```text
2 guests
→ Deluxe King
→ Deluxe Twin
→ Premium King
→ Family Suite

3 guests
→ Family Suite

4 guests
→ Family Suite
```

The current `hotel.json` does **not** contain date-specific room inventory.

Therefore this implementation does **not** claim live hotel inventory.

The frontend explicitly communicates:

> Demo availability is based on room capacity. Live date-specific inventory is not connected in this version.

This is an intentional limitation rather than a hidden assumption.

### Production version

A production implementation would connect `checkAvailability()` to a real reservation/property-management system or a date-aware inventory database.

---

# 17. Error Handling

The application handles several failure modes.

## Invalid availability request

Examples:

- check-out before check-in
- same-day check-in/check-out
- zero guests
- guest count above the supported limit

These are rejected through Pydantic validation or deterministic business logic.

## Unsupported hotel question

A controlled fallback is returned instead of inventing a hotel fact.

## Backend connection failure

The frontend shows a clear connection error when it cannot reach FastAPI.

## Loading state

The frontend shows a typing indicator and prevents repeated submissions while a request is being processed.

---

# 18. Frontend UX Decisions

## Conversational-first interface

Hotel guests naturally ask questions in plain language, so the primary interaction is a chat interface.

## Suggested questions

The first screen provides example questions to help guests understand what the assistant can do.

## Structured availability cards

Availability results are displayed as cards rather than raw JSON.

A room card can show:

- room name
- bed configuration
- price per night
- maximum capacity
- breakfast inclusion
- selected room features

## Loading feedback

The typing indicator gives immediate feedback while waiting for the backend.

## Error feedback

A visible connection-error message prevents the interface from appearing broken if the backend is unavailable.

## New chat

The New Chat action provides a simple way to reset the current conversation.

## Responsive design

Tailwind responsive utilities are used so the chat works across desktop and smaller screens.

---

# 19. Engineering Decisions

## Why Next.js?

Next.js provides a practical React application structure, TypeScript support, and production build tooling.

## Why FastAPI?

FastAPI provides:

- simple REST API development
- request validation through Pydantic
- automatic OpenAPI/Swagger documentation
- a lightweight Python backend

## Why JSON?

For this assignment-sized hotel knowledge base, JSON is:

- easy to inspect
- easy to version
- easy to modify
- sufficient for local development
- simple to test

A production system could replace it with a database or hotel-system integration.

## Why deterministic availability?

Room eligibility is a business rule rather than a creative text-generation task.

Keeping it deterministic makes it:

- predictable
- testable
- explainable
- easier to validate

---

# 20. Automated Testing

The backend currently contains 19 automated tests covering:

### API

- health endpoint
- hotel endpoint
- rooms endpoint
- availability endpoint
- invalid availability dates
- invalid guest count

### Chat

- normal hotel question
- unsupported-question fallback
- missing availability information
- complete availability request
- conversation context

### Services

- hotel data
- room list
- room capacity behavior
- availability validation

Run:

```powershell
cd backend
.\.venv\Scripts\Activate.ps1
python -m pytest -v
```

Verified result:

```text
19 passed
```

The current test environment also reports two dependency deprecation warnings. They do not cause test failures.

---

# 21. Frontend Quality Checks

Run from:

```text
frontend/
```

### Lint

```powershell
npm run lint
```

### Production build

```powershell
npm run build
```

Verified project status:

```text
ESLint             PASS
TypeScript         PASS
Next.js build      PASS
```

---

# 22. Evaluation Scenarios

The project is evaluated against the following scenarios.

| # | Scenario | Expected behavior |
|---|---|---|
| 1 | Ask check-in time | Return grounded hotel information |
| 2 | Ask check-out time | Return grounded hotel information |
| 3 | Ask about breakfast | Return knowledge-base information |
| 4 | Ask about unsupported service | Return safe fallback |
| 5 | Ask "Do you have a room?" | Request missing dates and guests |
| 6 | Request room for 3 guests with dates | Return Family Suite eligibility |
| 7 | Request room for 2 guests | Return eligible room types |
| 8 | Send invalid date range | Reject the request |
| 9 | Send invalid guest count | Reject the request |
| 10 | Follow-up with conversation history | Preserve basic context |
| 11 | Backend unavailable | Show frontend connection error |
| 12 | Complete browser flow | Guest → frontend → API → business logic → UI |

---

# 23. Example End-to-End Flow

```text
1. Guest opens http://localhost:3000
                 ↓
2. Guest asks:
   "Do you have a room from 2026-09-25
    to 2026-09-27 for 3 guests?"
                 ↓
3. Next.js sends POST /api/chat
                 ↓
4. FastAPI validates the request
                 ↓
5. Chat layer detects availability intent
                 ↓
6. Backend extracts dates + guest count
                 ↓
7. check_availability() runs
                 ↓
8. Room capacity is checked
                 ↓
9. Family Suite is returned
                 ↓
10. Structured response reaches frontend
                 ↓
11. Frontend displays Family Suite card
```

---

# 24. Production Improvements

The current application is scoped as an assignment prototype.

A production version could add:

## Live inventory

Connect availability to:

- property-management systems
- reservation systems
- date-aware inventory APIs

## Real LLM integration

A production conversational layer could use a hosted or self-hosted LLM for more flexible natural-language understanding and response generation.

The model should still be constrained to hotel knowledge and structured tools.

## Tool calling

Possible tools:

```text
checkAvailability()
getRoomDetails()
getHotelPolicy()
```

Each tool should have a strict schema.

## Authentication

Associate conversations with authenticated guests where appropriate.

## Persistent conversation storage

Store conversations securely when there is a product requirement for persistence.

## Observability

Add:

- structured logging
- request tracing
- latency metrics
- error monitoring
- tool/model failure monitoring

## Security

Add:

- authentication and authorization
- rate limiting
- request size limits
- production secret management
- strict production CORS configuration

## Accessibility

Add formal accessibility testing for:

- keyboard navigation
- focus management
- screen readers
- color contrast
- form labeling

---

# 25. Security Notes

The current local implementation does not require API keys.

The frontend does not contain backend secrets.

The backend CORS configuration supports local development and the deployed
GitHub Pages frontend.

Local origins:
- http://localhost:3000
- http://127.0.0.1:3000

Deployed frontend:
- https://dhayanand458.github.io

Generated files and environment-specific secrets should not be committed.

---

# 26. AI Tools Used

AI assistance was used during development for:

- project scaffolding guidance
- code-generation assistance
- debugging
- test-case design
- architecture discussion
- frontend UX iteration
- documentation drafting

The implementation was manually reviewed and tested against the actual application behavior.

The project intentionally keeps business-critical hotel logic deterministic and testable.

---

# 27. Known Limitations

This is an assignment prototype rather than a production hotel reservation system.

Known limitations:

1. Availability is based on room capacity rather than live room inventory.
2. No real reservation is created.
3. No payment processing exists.
4. No authentication is implemented.
5. The hotel knowledge base is a local JSON file.
6. Conversation history is maintained by the current frontend session.
7. Production monitoring and analytics are not implemented.
8. No real hotel PMS/reservation integration exists.
9. No external paid LLM dependency is required by the current implementation.

These limitations are documented intentionally so that the system does not claim capabilities it does not actually have.

---

# 28. Running the Complete Application

Use two terminals.

## Terminal 1 — Backend

```powershell
cd staymate-ai\backend
.\.venv\Scripts\Activate.ps1
python -m uvicorn app.main:app --reload --port 8000
```

## Terminal 2 — Frontend

```powershell
cd staymate-ai\frontend
npm run dev
```

Open:

```text
http://localhost:3000
```

### Try normal hotel questions

```text
What time is check-in?
```

```text
Is breakfast included?
```

```text
Is the pool open?
```

### Try an incomplete availability request

```text
Do you have a room?
```

### Try a complete availability request

```text
Do you have a room from 2026-09-25 to 2026-09-27 for 3 guests?
```

Expected eligible room:

```text
Family Suite
```

---

# 29. Final Verification

Before submission:

```powershell
# Frontend
cd frontend
npm run lint
npm run build

# Backend
cd ..\backend
.\.venv\Scripts\Activate.ps1
python -m pytest -v
```

Current verified status:

```text
Frontend lint       PASS
Frontend build      PASS
Backend tests       19 passed
```

---

# 30. Submission Checklist

Before submitting the repository:

- [ ] Frontend runs locally
- [ ] Backend runs locally
- [ ] `/api/health` works
- [ ] Swagger `/docs` works
- [ ] Normal hotel question works
- [ ] Unsupported question fallback works
- [ ] Missing availability information is requested
- [ ] Complete availability request works
- [ ] Availability card renders correctly
- [ ] Conversation context works
- [ ] Frontend loading state works
- [ ] Frontend backend-error state works
- [ ] `npm run lint` passes
- [ ] `npm run build` passes
- [ ] `python -m pytest -v` passes
- [ ] No API keys are committed
- [ ] `.venv`, `node_modules`, `.next`, caches are ignored
- [ ] README is complete
- [ ] Evaluation scenarios are documented
- [ ] Known limitations are documented
- [ ] Git status has been reviewed before pushing

---

# 31. Summary

StayMate demonstrates a full-stack hotel guest-assistant workflow:

```text
Guest
  ↓
Next.js conversational UI
  ↓
FastAPI /api/chat
  ↓
Intent + conversation handling
  ↓
Hotel knowledge base
  ↓
Deterministic business logic
  ↓
Structured response
  ↓
Chat UI / availability card
```

The design prioritizes:

- grounded hotel information
- deterministic business logic
- explicit missing-information handling
- safe unsupported-question fallback
- structured availability responses
- testability
- responsive UX
- transparent limitations
- clear separation between frontend, API, and business logic
