"use client";

import { KeyboardEvent, useState } from "react";

type MessageRole = "user" | "assistant";

type AvailabilityRoom = {
  id: string;
  name: string;
  capacity: number;
  bed_configuration: string;
  price_per_night: number;
  features: string[];
  breakfast_included: boolean;
};

type AvailabilityData = {
  check_in: string;
  check_out: string;
  guests: number;
  rooms: AvailabilityRoom[];
};

type ChatMessage = {
  role: MessageRole;
  content: string;
  availability?: AvailabilityData | null;
};

type ChatResponse = {
  message: string;
  response_type: string;
  conversation: {
    role: MessageRole;
    content: string;
  }[];
  availability: AvailabilityData | null;
};

const API_URL = "http://127.0.0.1:8000";

const suggestedQuestions = [
  "What time is check-in?",
  "Is breakfast included?",
  "Is the pool open?",
  "Do you allow pets?",
];

export default function Home() {
  const [messages, setMessages] = useState<ChatMessage[]>([
    {
      role: "assistant",
      content:
        "Welcome to StayMate Grand Hotel. I'm your virtual hotel concierge. I can help with rooms, breakfast, amenities, policies, and stay availability.",
    },
  ]);

  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [showAvailabilityForm, setShowAvailabilityForm] = useState(false);

  const [checkIn, setCheckIn] = useState("");
  const [checkOut, setCheckOut] = useState("");
  const [guests, setGuests] = useState("2");

  async function sendMessage(message: string) {
    const trimmedMessage = message.trim();

    if (!trimmedMessage || loading) {
      return;
    }

    setError("");
    setInput("");
    setLoading(true);

    const conversationForApi = messages.slice(-10).map((item) => ({
      role: item.role,
      content: item.content,
    }));

    const userMessage: ChatMessage = {
      role: "user",
      content: trimmedMessage,
    };

    setMessages((current) => [...current, userMessage]);

    try {
      const response = await fetch(`${API_URL}/api/chat`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          message: trimmedMessage,
          conversation: conversationForApi,
        }),
      });

      if (!response.ok) {
        throw new Error(`Request failed with status ${response.status}`);
      }

      const data: ChatResponse = await response.json();

      const assistantMessage: ChatMessage = {
        role: "assistant",
        content: data.message,
        availability: data.availability,
      };

      setMessages((current) => [...current, assistantMessage]);
    } catch (requestError) {
      console.error("Chat request failed:", requestError);

      setError(
        "I couldn't connect to the hotel assistant. Please make sure the backend is running and try again.",
      );
    } finally {
      setLoading(false);
    }
  }

  async function handleSubmit(event: React.FormEvent<HTMLFormElement>) {
    event.preventDefault();
    await sendMessage(input);
  }

  async function handleSuggestedQuestion(question: string) {
    await sendMessage(question);
  }

  function handleInputKeyDown(event: KeyboardEvent<HTMLTextAreaElement>) {
    if (event.key === "Enter" && !event.shiftKey) {
      event.preventDefault();

      if (!loading && input.trim()) {
        void sendMessage(input);
      }
    }
  }

  async function handleAvailabilitySubmit(
    event: React.FormEvent<HTMLFormElement>,
  ) {
    event.preventDefault();

    if (!checkIn || !checkOut || !guests) {
      return;
    }

    const guestCount = Number(guests);

    const message = `Do you have a room from ${checkIn} to ${checkOut} for ${guestCount} guests?`;

    setShowAvailabilityForm(false);

    await sendMessage(message);
  }

  function clearConversation() {
    setMessages([
      {
        role: "assistant",
        content:
          "Welcome back. How can I help with your stay at StayMate Grand Hotel?",
      },
    ]);

    setError("");
    setInput("");
  }

  return (
    <main className="min-h-screen bg-[#f5f7f9] text-slate-900">
      <div className="mx-auto flex min-h-screen max-w-7xl flex-col px-4 py-4 sm:px-6 lg:px-8">
        <section className="flex min-h-[calc(100vh-2rem)] flex-1 flex-col overflow-hidden rounded-[28px] border border-slate-200 bg-white shadow-[0_24px_80px_rgba(15,23,42,0.10)]">
          {/* Header */}
          <header className="flex items-center justify-between border-b border-slate-200 px-5 py-4 sm:px-7">
            <div className="flex items-center gap-3">
              <div className="flex h-11 w-11 items-center justify-center rounded-2xl bg-slate-900 text-lg text-white shadow-sm">
                S
              </div>

              <div>
                <div className="flex items-center gap-2">
                  <h1 className="text-base font-semibold tracking-tight text-slate-950">
                    StayMate
                  </h1>

                  <span className="rounded-full bg-emerald-50 px-2 py-0.5 text-[10px] font-semibold uppercase tracking-wider text-emerald-700">
                    Concierge
                  </span>
                </div>

                <p className="text-xs text-slate-500">
                  StayMate Grand Hotel · Bengaluru
                </p>
              </div>
            </div>

            <div className="flex items-center gap-2">
              <span className="hidden text-xs font-medium text-slate-500 sm:inline">
                Assistant online
              </span>

              <span className="h-2.5 w-2.5 rounded-full bg-emerald-500 shadow-[0_0_0_4px_rgba(16,185,129,0.10)]" />

              <button
                type="button"
                onClick={clearConversation}
                className="ml-2 rounded-xl border border-slate-200 px-3 py-2 text-xs font-medium text-slate-600 transition hover:border-slate-300 hover:bg-slate-50"
              >
                New chat
              </button>
            </div>
          </header>

          {/* Chat area */}
          <div className="flex min-h-0 flex-1 flex-col">
            <div className="flex-1 overflow-y-auto px-4 py-6 sm:px-8 sm:py-8">
              <div className="mx-auto max-w-3xl">
                {/* Intro */}
                <div className="mb-8 text-center">
                  <div className="mx-auto mb-4 flex h-16 w-16 items-center justify-center rounded-3xl bg-slate-900 text-2xl text-white shadow-lg">
                    ✦
                  </div>

                  <p className="mb-2 text-xs font-semibold uppercase tracking-[0.18em] text-slate-400">
                    Your hotel concierge
                  </p>

                  <h2 className="text-2xl font-semibold tracking-tight text-slate-950 sm:text-3xl">
                    How can I help with your stay?
                  </h2>

                  <p className="mx-auto mt-2 max-w-lg text-sm leading-6 text-slate-500">
                    Ask about rooms, amenities, breakfast, hotel policies, or
                    check which room types can accommodate your stay.
                  </p>
                </div>

                {/* Messages */}
                <div className="space-y-5">
                  {messages.map((message, index) => (
                    <div
                      key={`${message.role}-${index}`}
                      className={`flex ${
                        message.role === "user"
                          ? "justify-end"
                          : "justify-start"
                      }`}
                    >
                      <div
                        className={`flex max-w-[88%] items-end gap-2.5 sm:max-w-[75%] ${
                          message.role === "user"
                            ? "flex-row-reverse"
                            : "flex-row"
                        }`}
                      >
                        {/* Avatar */}
                        <div
                          className={`flex h-8 w-8 shrink-0 items-center justify-center rounded-xl text-[10px] font-semibold ${
                            message.role === "user"
                              ? "bg-slate-200 text-slate-700"
                              : "bg-slate-900 text-white"
                          }`}
                        >
                          {message.role === "user" ? "You" : "S"}
                        </div>

                        {/* Message + availability */}
                        <div className="space-y-3">
                          <div
                            className={`rounded-2xl px-4 py-3 text-sm leading-6 shadow-sm ${
                              message.role === "user"
                                ? "rounded-br-md bg-slate-900 text-white"
                                : "rounded-bl-md border border-slate-200 bg-slate-50 text-slate-700"
                            }`}
                          >
                            {message.content}
                          </div>

                          {/* Availability cards */}
                          {message.role === "assistant" &&
                            message.availability &&
                            message.availability.rooms.length > 0 && (
                              <div className="space-y-3">
                                {message.availability.rooms.map((room) => (
                                  <div
                                    key={room.id}
                                    className="overflow-hidden rounded-2xl border border-slate-200 bg-white shadow-sm"
                                  >
                                    <div className="border-b border-slate-100 bg-slate-50 px-4 py-3">
                                      <div className="flex items-start justify-between gap-4">
                                        <div>
                                          <p className="text-sm font-semibold text-slate-950">
                                            {room.name}
                                          </p>

                                          <p className="mt-1 text-xs text-slate-500">
                                            {room.bed_configuration}
                                          </p>
                                        </div>

                                        <div className="shrink-0 text-right">
                                          <p className="text-sm font-semibold text-slate-950">
                                            INR{" "}
                                            {room.price_per_night.toLocaleString(
                                              "en-IN",
                                            )}
                                          </p>

                                          <p className="text-[11px] text-slate-400">
                                            per night
                                          </p>
                                        </div>
                                      </div>
                                    </div>

                                    <div className="px-4 py-3">
                                      <div className="mb-3 flex flex-wrap gap-2">
                                        <span className="rounded-full bg-slate-100 px-2.5 py-1 text-[11px] font-medium text-slate-600">
                                          Up to {room.capacity} guests
                                        </span>

                                        {room.breakfast_included && (
                                          <span className="rounded-full bg-emerald-50 px-2.5 py-1 text-[11px] font-medium text-emerald-700">
                                            Breakfast included
                                          </span>
                                        )}
                                      </div>

                                      <div className="flex flex-wrap gap-x-3 gap-y-1">
                                        {room.features
                                          .slice(0, 4)
                                          .map((feature) => (
                                            <span
                                              key={feature}
                                              className="text-xs text-slate-500"
                                            >
                                              • {feature}
                                            </span>
                                          ))}
                                      </div>
                                    </div>
                                  </div>
                                ))}

                                <p className="text-[11px] leading-5 text-slate-400">
                                  Demo availability is based on room capacity.
                                  Live date-specific inventory is not connected
                                  in this version.
                                </p>
                              </div>
                            )}
                        </div>
                      </div>
                    </div>
                  ))}

                  {/* Loading indicator */}
                  {loading && (
                    <div className="flex justify-start">
                      <div className="flex items-end gap-2.5">
                        <div className="flex h-8 w-8 items-center justify-center rounded-xl bg-slate-900 text-xs font-semibold text-white">
                          S
                        </div>

                        <div className="rounded-2xl rounded-bl-md border border-slate-200 bg-slate-50 px-4 py-3">
                          <div className="flex items-center gap-1.5">
                            <span className="h-1.5 w-1.5 animate-bounce rounded-full bg-slate-400 [animation-delay:-0.3s]" />
                            <span className="h-1.5 w-1.5 animate-bounce rounded-full bg-slate-400 [animation-delay:-0.15s]" />
                            <span className="h-1.5 w-1.5 animate-bounce rounded-full bg-slate-400" />
                          </div>
                        </div>
                      </div>
                    </div>
                  )}
                </div>

                {/* Error */}
                {error && (
                  <div className="mt-5 rounded-2xl border border-red-200 bg-red-50 px-4 py-3 text-sm text-red-700">
                    <div className="flex items-start gap-3">
                      <span className="font-semibold">Connection issue</span>
                      <span>{error}</span>
                    </div>
                  </div>
                )}

                {/* Suggested questions */}
                {messages.length <= 1 && !loading && (
                  <div className="mt-8">
                    <p className="mb-3 text-xs font-semibold uppercase tracking-wider text-slate-400">
                      Try asking
                    </p>

                    <div className="grid gap-2 sm:grid-cols-2">
                      {suggestedQuestions.map((question) => (
                        <button
                          key={question}
                          type="button"
                          onClick={() => void handleSuggestedQuestion(question)}
                          className="rounded-2xl border border-slate-200 bg-white px-4 py-3 text-left text-sm font-medium text-slate-600 transition hover:-translate-y-0.5 hover:border-slate-300 hover:bg-slate-50 hover:text-slate-950"
                        >
                          {question}
                        </button>
                      ))}
                    </div>
                  </div>
                )}
              </div>
            </div>

            {/* Availability form */}
            {showAvailabilityForm && (
              <div className="border-t border-slate-200 bg-slate-50 px-4 py-4 sm:px-8">
                <form
                  onSubmit={handleAvailabilitySubmit}
                  className="mx-auto grid max-w-3xl gap-3 sm:grid-cols-[1fr_1fr_0.7fr_auto] sm:items-end"
                >
                  <label className="text-xs font-semibold text-slate-600">
                    Check-in

                    <input
                      type="date"
                      value={checkIn}
                      onChange={(event) => setCheckIn(event.target.value)}
                      className="mt-1.5 h-11 w-full rounded-xl border border-slate-200 bg-white px-3 text-sm text-slate-700 outline-none transition focus:border-slate-400 focus:ring-2 focus:ring-slate-100"
                    />
                  </label>

                  <label className="text-xs font-semibold text-slate-600">
                    Check-out

                    <input
                      type="date"
                      value={checkOut}
                      onChange={(event) => setCheckOut(event.target.value)}
                      className="mt-1.5 h-11 w-full rounded-xl border border-slate-200 bg-white px-3 text-sm text-slate-700 outline-none transition focus:border-slate-400 focus:ring-2 focus:ring-slate-100"
                    />
                  </label>

                  <label className="text-xs font-semibold text-slate-600">
                    Guests

                    <input
                      type="number"
                      min="1"
                      max="20"
                      value={guests}
                      onChange={(event) => setGuests(event.target.value)}
                      className="mt-1.5 h-11 w-full rounded-xl border border-slate-200 bg-white px-3 text-sm text-slate-700 outline-none transition focus:border-slate-400 focus:ring-2 focus:ring-slate-100"
                    />
                  </label>

                  <button
                    type="submit"
                    disabled={loading || !checkIn || !checkOut}
                    className="h-11 rounded-xl bg-slate-900 px-5 text-sm font-semibold text-white transition hover:bg-slate-800 disabled:cursor-not-allowed disabled:opacity-50"
                  >
                    Check rooms
                  </button>
                </form>
              </div>
            )}

            {/* Composer */}
            <div className="border-t border-slate-200 bg-white px-4 py-4 sm:px-8 sm:py-5">
              <div className="mx-auto max-w-3xl">
                <form onSubmit={handleSubmit}>
                  <div className="flex items-end gap-2 rounded-2xl border border-slate-200 bg-slate-50 p-2 shadow-sm transition focus-within:border-slate-300 focus-within:bg-white focus-within:shadow-md">
                    <textarea
                      value={input}
                      onChange={(event) => setInput(event.target.value)}
                      onKeyDown={handleInputKeyDown}
                      placeholder="Ask about rooms, breakfast, check-in..."
                      rows={1}
                      disabled={loading}
                      className="min-h-11 flex-1 resize-none bg-transparent px-3 py-2.5 text-sm text-slate-800 outline-none placeholder:text-slate-400 disabled:cursor-not-allowed"
                    />

                    <button
                      type="submit"
                      disabled={!input.trim() || loading}
                      aria-label="Send message"
                      className="flex h-11 w-11 shrink-0 items-center justify-center rounded-xl bg-slate-900 text-lg text-white transition hover:bg-slate-800 disabled:cursor-not-allowed disabled:opacity-40"
                    >
                      ↑
                    </button>
                  </div>
                </form>

                <div className="mt-3 flex flex-col items-center justify-between gap-2 sm:flex-row">
                  <p className="text-[11px] text-slate-400">
                    StayMate answers using the hotels available information.
                  </p>

                  <button
                    type="button"
                    onClick={() =>
                      setShowAvailabilityForm((current) => !current)
                    }
                    className="text-xs font-semibold text-slate-600 transition hover:text-slate-950"
                  >
                    {showAvailabilityForm
                      ? "Hide availability"
                      : "Check room availability →"}
                  </button>
                </div>
              </div>
            </div>
          </div>
        </section>
      </div>
    </main>
  );
}