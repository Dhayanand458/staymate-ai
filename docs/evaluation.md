# StayMate AI — Evaluation & Test Scenarios

## 1. Purpose

This document records the evaluation scenarios used to verify the StayMate AI hotel guest assistant.

The evaluation focuses on:

- normal hotel questions;
- missing information;
- ambiguity;
- availability requests;
- unsupported assumptions;
- conversation follow-ups;
- frontend loading and error behavior;
- backend failure/fallback behavior;
- end-to-end integration.

The hotel data used by the application is mock/demo data created for this assignment.

---

## 2. Automated Backend Tests

The backend test suite was executed with:

```bash
pytest -q
```

Result:

```text
19 passed, 2 warnings
```

The warnings are deprecation-related warnings from the current test-client dependency stack and did not cause test failures.

The automated tests cover:

- hotel data loading;
- room lookup;
- room capacity filtering;
- availability validation;
- API health;
- hotel endpoint;
- rooms endpoint;
- availability endpoint;
- chat responses;
- unsupported-question fallback;
- missing availability information;
- complete availability requests;
- conversation context preservation.

---

## 3. Evaluation Scenarios

### Scenario 1 — Basic hotel information

**Guest input**

> What time is check-in?

**Expected behavior**

The assistant should answer from the hotel knowledge base.

**Observed result**

The chat API returned:

```text
response_type: hotel_information
```

and the response included the configured 3:00 PM check-in time.

**Status**

PASS

---

### Scenario 2 — Another hotel FAQ

**Guest input**

> Is breakfast included?

**Expected behavior**

The assistant should provide the breakfast information configured for the hotel and room types.

**Observed result**

The chat service returned a hotel-information response using the configured hotel data.

**Status**

PASS

---

### Scenario 3 — Missing availability information

**Guest input**

> Do you have a room?

**Expected behavior**

The assistant should not invent dates or guest count.

It should request:

- check-in date;
- check-out date;
- number of guests.

**Observed result**

The API returned:

```text
response_type: needs_information
```

and asked for the missing availability information.

**Status**

PASS

---

### Scenario 4 — Complete availability request

**Guest input**

> Do you have a room from 2026-09-25 to 2026-09-27 for 3 guests?

**Expected behavior**

The backend should:

1. detect an availability request;
2. extract both dates;
3. extract the guest count;
4. validate the date range;
5. call the deterministic availability service;
6. return eligible room types.

**Observed result**

The API returned:

```text
response_type: availability
check_in: 2026-09-25
check_out: 2026-09-27
guests: 3
```

The Family Suite was returned because its configured capacity is 4.

**Status**

PASS

---

### Scenario 5 — Unsupported hotel capability

**Guest input**

> Does the hotel have a private helicopter service?

**Expected behavior**

The assistant should not invent an answer.

**Observed result**

The API returned:

```text
response_type: fallback
```

and referenced the hotel knowledge base rather than claiming that the hotel provides the service.

**Status**

PASS

---

### Scenario 6 — Conversation follow-up

**Conversation**

Guest:

> What rooms do you have?

Assistant:

> Our room types include Deluxe King, Deluxe Twin, Premium King and Family Suite.

Guest:

> Is breakfast included?

**Expected behavior**

The backend should accept previous conversation context and answer the follow-up.

**Observed result**

The conversation context was preserved and the follow-up received a hotel-information response.

**Status**

PASS

---

### Scenario 7 — Invalid availability date range

**Guest input**

A request where the check-out date is before or equal to the check-in date.

**Expected behavior**

The availability service should reject the invalid date range.

**Observed result**

The deterministic availability function raises a validation error:

```text
Check-out date must be after check-in date.
```

The availability API model also validates this condition.

**Status**

PASS

---

### Scenario 8 — Invalid guest count

**Guest input**

An availability request with zero or an invalid number of guests.

**Expected behavior**

The request should be rejected rather than silently producing a room result.

**Observed result**

The availability validation requires at least one guest.

**Status**

PASS

---

### Scenario 9 — Frontend loading state

**Action**

Submit a chat message from the browser.

**Expected behavior**

The UI should indicate that the assistant is processing the request and prevent confusing duplicate submissions while the request is in progress.

**Observed result**

The frontend displays an assistant loading indicator while waiting for the backend response.

**Status**

PASS

---

### Scenario 10 — Frontend API/network failure

**Action**

Make the backend unavailable while submitting a message.

**Expected behavior**

The frontend should display a visible error state rather than silently failing.

**Observed result**

The frontend contains request-error handling and displays an error message when the chat request cannot be completed.

**Status**

PASS

---

### Scenario 11 — Availability result presentation

**Action**

Submit a complete availability request from the browser.

**Expected behavior**

The response should be understandable without requiring the guest to read raw JSON.

**Observed result**

The frontend renders room result cards containing relevant information such as:

- room name;
- bed configuration;
- price;
- capacity;
- breakfast information;
- room features.

The UI also explicitly states that the current demo availability is based on room capacity rather than live date-specific inventory.

**Status**

PASS

---

### Scenario 12 — End-to-end flow

**Flow**

```text
Open frontend
    ↓
Ask hotel question
    ↓
Frontend calls backend
    ↓
Backend processes request
    ↓
Response displayed in chat
    ↓
Ask follow-up
    ↓
Request availability
    ↓
Provide dates + guests
    ↓
Receive room result
```

**Expected behavior**

The complete flow should work through the browser without directly calling an AI provider from the frontend.

**Observed result**

The frontend successfully communicated with the FastAPI backend, displayed assistant responses, maintained conversation state, and displayed the Family Suite result for the tested three-guest availability request.

**Status**

PASS

---

### Scenario 13 — Knowledge-base grounding

**Action**

Ask questions whose answers are represented in the hotel JSON data.

Examples:

- What time is check-in?
- What time is check-out?
- Is Wi-Fi complimentary?
- Is parking available?
- Are pets allowed?
- What are the cancellation rules?

**Expected behavior**

The assistant should use configured hotel information and avoid inventing unsupported hotel details.

**Observed result**

Supported hotel questions are handled by the local hotel knowledge base, while unsupported requests use a fallback.

**Status**

PASS

---

## 4. Frontend Verification

The following frontend checks were completed:

### Lint

Command:

```bash
npm run lint
```

Result:

```text
Passed
```

No lint errors were reported.

### Production build

Command:

```bash
npm run build
```

Result:

```text
Build completed successfully.
```

The Next.js application compiled successfully, TypeScript validation completed, and the application generated the expected route.

A warning about a `package-lock.json` located outside the frontend repository was displayed by Next.js/Turbopack. It did not prevent the build from completing successfully.

---

## 5. Backend Verification

The backend was tested with:

```bash
pytest -q
```

Result:

```text
19 passed, 2 warnings
```

The backend health endpoint was also verified during local development:

```text
GET /api/health
```

Expected response:

```json
{
  "status": "ok",
  "service": "staymate-ai-backend"
}
```

---

## 6. Known Limitation

The most important known limitation is the availability model.

The current mock hotel data contains room capacities but does not contain real date-specific inventory.

Therefore:

```text
"Available"
```

currently means:

> The configured room type has enough capacity for the requested number of guests and the requested date range is valid.

It does **not** mean that a real room is confirmed vacant for those dates.

This limitation is intentionally disclosed in the application UI and documentation.

---

## 7. AI/Model Limitation

The current implementation does not require a paid external LLM API.

The conversational decision layer is implemented locally using deterministic intent detection, hotel knowledge-base lookup, information extraction, and safe fallback behavior.

For a production version, an LLM could be added for more flexible natural-language understanding while keeping:

- hotel data grounding;
- date validation;
- guest validation;
- availability rules;
- booking operations

outside the model.

---

## 8. Future Evaluation

If the application were extended, additional evaluation should include:

- paraphrased guest questions;
- ambiguous dates;
- natural-language dates such as "next Friday";
- larger guest groups;
- invalid date formats;
- conflicting conversation context;
- model extraction errors;
- model/tool timeout;
- hotel data service failure;
- real date-specific inventory;
- booking confirmation;
- cancellation workflows;
- adversarial or unsupported hotel claims;
- mobile browser testing;
- accessibility testing.

The production evaluation should measure both technical reliability and whether guests can successfully complete their intended task.

---

## 9. Evaluation Summary

The current implementation demonstrates the required local integration path:

```text
Guest
  ↓
Next.js conversational UI
  ↓
FastAPI backend
  ↓
Hotel knowledge base
  ↓
Deterministic availability service
  ↓
Structured response
  ↓
Guest-facing result
```

The automated backend suite passed with 19 tests, and the frontend lint/build checks completed successfully.

The application is intentionally presented as a local assignment prototype rather than a real hotel booking system.
