"use client";

import { useState } from "react";
import { api } from "@/lib/api";

// Functional, lesson-scoped tutor chat for the concept sidebar. Honest about the model.
const SUGGESTIONS = ["Give me a smaller example", "Where do people usually slip?"];

export default function AskTutor({ conceptId, conceptName }) {
  const [question, setQuestion] = useState("");
  const [answer, setAnswer] = useState(null);
  const [model, setModel] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  async function ask(q) {
    const text = (q ?? question).trim();
    if (!text || loading) return;
    setQuestion(text);
    setLoading(true);
    setError(null);
    try {
      const res = await api.askTutor(conceptId, text);
      setAnswer(res.answer);
      setModel(res.model);
    } catch (e) {
      setError(e.message);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="card p-5">
      <div className="mb-2 flex items-center gap-2">
        <span className="step-badge bg-brand-600 text-white">+</span>
        <span className="font-semibold">Ask the tutor</span>
      </div>
      <p className="text-xs leading-relaxed text-body">
        Concept questions about this lesson. The tutor gives hints — it won't solve the
        quiz for you.
      </p>

      <div className="mt-3 flex flex-wrap gap-1.5">
        {SUGGESTIONS.map((q) => (
          <button
            key={q}
            type="button"
            onClick={() => ask(q)}
            className="rounded-full bg-brand-50 px-2.5 py-1 text-xs text-brand-700 hover:bg-brand-100"
          >
            {q}
          </button>
        ))}
      </div>

      <form
        onSubmit={(e) => {
          e.preventDefault();
          ask();
        }}
        className="mt-3"
      >
        <textarea
          rows={2}
          value={question}
          onChange={(e) => setQuestion(e.target.value)}
          placeholder={`Ask anything about ${conceptName?.toLowerCase() || "this lesson"}…`}
          className="w-full rounded-xl border border-line p-2.5 text-sm focus:border-brand-400 focus:outline-none"
        />
        <button
          type="submit"
          disabled={loading || !question.trim()}
          className="mt-2 w-full rounded-xl bg-brand-600 py-2 text-sm font-medium text-white transition hover:bg-brand-700 disabled:opacity-50"
        >
          {loading ? "Thinking…" : "Ask"}
        </button>
      </form>

      {error && <p className="mt-2 text-xs text-red-600">{error}</p>}

      {answer && (
        <div className="mt-3 rounded-xl border-l-4 border-brand-600 bg-mist p-3">
          <p className="whitespace-pre-wrap text-sm leading-relaxed text-ink">{answer}</p>
          {model && (
            <p className="mt-2 font-mono text-[10px] uppercase tracking-wide text-slate-400">
              answered by {model}
            </p>
          )}
        </div>
      )}
    </div>
  );
}
