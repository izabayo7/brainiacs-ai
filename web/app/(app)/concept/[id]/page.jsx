"use client";

import { useEffect, useState } from "react";
import { useParams, useRouter } from "next/navigation";
import ReactMarkdown from "react-markdown";
import { api } from "@/lib/api";

export default function ConceptPage() {
  const { id } = useParams();
  const router = useRouter();
  const [concept, setConcept] = useState(null);
  const [meta, setMeta] = useState(null); // {index, total, pct}
  const [error, setError] = useState(null);

  useEffect(() => {
    Promise.all([api.getConcept(id), api.listConcepts()])
      .then(([c, list]) => {
        setConcept(c);
        const idx = list.findIndex((x) => x.id === c.id);
        const row = list[idx];
        setMeta({ index: idx + 1, total: list.length, pct: Math.round((row?.p_mastered || 0) * 100) });
      })
      .catch((e) => setError(e));
  }, [id, router]);

  if (error) {
    const locked = error.status === 403;
    return (
      <div className="card mx-auto max-w-lg p-10 text-center">
        <p className="mb-3 text-4xl">{locked ? "🔒" : "⚠️"}</p>
        <h1 className="mb-2 text-xl font-semibold">
          {locked ? "This concept is locked" : "Something went wrong"}
        </h1>
        <p className="mb-5 text-body">
          {locked ? "Master its prerequisites first to unlock it." : error.message}
        </p>
        <a href="/" className="font-medium text-brand-600">← Back to your path</a>
      </div>
    );
  }
  if (!concept) return <p className="text-slate-400">Loading…</p>;

  const chapter = concept.chapters?.[0];

  return (
    <div>
      {/* Breadcrumb + mastery */}
      <div className="mb-6 flex items-center justify-between">
        <a href="/" className="text-sm text-slate-500 hover:text-brand-600">‹ Concepts</a>
        {meta && (
          <span className="rounded-full bg-brand-50 px-3 py-1 font-mono text-xs text-brand-700">
            mastery {meta.pct}%
          </span>
        )}
      </div>

      {meta && (
        <p className="text-xs font-semibold uppercase tracking-widest text-brand-600">
          Concept {meta.index} of {meta.total} · Learn
        </p>
      )}
      <h1 className="mt-1 text-3xl font-semibold tracking-tight">{concept.name}</h1>
      <div className="prose-chapter mt-2 max-w-2xl">
        <ReactMarkdown>{concept.explanation_md}</ReactMarkdown>
      </div>

      {/* Tutor note */}
      <div className="mt-6 flex gap-3 rounded-2xl border border-brand-100 bg-brand-50/60 p-4">
        <span className="step-badge mt-0.5 bg-brand-600 text-white">+</span>
        <div>
          <p className="text-sm text-ink">
            <span className="font-semibold">Tutor note for you:</span> read the idea, then
            trace the worked example yourself before the quiz — that's where mastery moves.
          </p>
          <p className="mt-0.5 font-mono text-xs text-slate-400">
            from your learner model · updates as you practice
          </p>
        </div>
      </div>

      <div className="mt-6 grid gap-6 lg:grid-cols-[1fr_18rem]">
        {/* Main column */}
        <div className="space-y-6">
          {/* Watch card */}
          <div className="card overflow-hidden">
            <div className="flex items-center gap-3 border-b border-line px-5 py-3">
              <span className="step-badge">1</span>
              <span className="font-semibold">Watch or read</span>
            </div>
            <div className="relative grid h-56 place-items-center bg-gradient-to-br from-slate-900 to-brand-700 text-white">
              <div className="grid h-14 w-14 place-items-center rounded-full bg-white/15 backdrop-blur">
                <svg className="h-6 w-6 translate-x-0.5" viewBox="0 0 24 24" fill="white"><path d="M8 5v14l11-7z" /></svg>
              </div>
              <p className="absolute bottom-5 font-mono text-xs text-white/70">
                {concept.name}, explained · curated by your instructor
              </p>
            </div>
            {chapter?.video_url ? null : (
              <p className="px-5 py-3 text-xs text-slate-400">
                Read the notes below — no data needed to start.
              </p>
            )}
          </div>

          {/* Lesson body */}
          <div className="card p-6">
            <div className="mb-3 flex items-center gap-3">
              <span className="step-badge">2</span>
              <span className="font-semibold">The idea, with a worked example</span>
            </div>
            <div className="prose-chapter">
              {chapter ? (
                <ReactMarkdown>{chapter.body_md}</ReactMarkdown>
              ) : (
                <ReactMarkdown>{concept.worked_example_md}</ReactMarkdown>
              )}
            </div>
          </div>

          {/* Ask the tutor */}
          <div className="card p-6">
            <div className="mb-3 flex items-center justify-between">
              <div className="flex items-center gap-3">
                <span className="step-badge bg-brand-600 text-white">+</span>
                <span className="font-semibold">Ask the tutor</span>
              </div>
              <span className="font-mono text-xs text-slate-400">Qwen3.5-4B · self-hosted</span>
            </div>
            <p className="text-sm text-body">
              Scoped to this lesson — concept questions only. The tutor won't solve
              exercises here; that happens in the quiz, where it can see your attempt.
            </p>
            <div className="mt-3 flex flex-wrap gap-2">
              {["Give me a smaller example", "Where do people usually slip?"].map((q) => (
                <span key={q} className="rounded-full bg-brand-50 px-3 py-1 text-xs text-brand-700">
                  {q}
                </span>
              ))}
            </div>
            <div className="mt-3 flex gap-2">
              <input
                disabled
                placeholder={`Ask anything about ${concept.name.toLowerCase()}…`}
                className="flex-1 rounded-xl border border-line px-3.5 py-2.5 text-sm"
              />
              <button className="rounded-xl bg-brand-600 px-5 font-medium text-white">Ask</button>
            </div>
          </div>
        </div>

        {/* Sidebar */}
        <aside className="lg:sticky lg:top-24 lg:self-start">
          <div className="card p-5">
            <h3 className="font-semibold">This lesson</h3>
            <ul className="mt-3 space-y-2 text-sm text-body">
              <li className="flex items-center gap-2"><Dot /> Read the idea</li>
              <li className="flex items-center gap-2"><Dot /> Trace the example</li>
              <li className="flex items-center gap-2"><Dot /> Take the quiz</li>
            </ul>
            <button
              onClick={() => router.push(`/quiz/${concept.id}`)}
              className="mt-5 w-full rounded-xl bg-brand-600 py-3 font-medium text-white transition hover:bg-brand-700"
            >
              Start quiz →
            </button>
            <p className="mt-3 text-xs leading-relaxed text-slate-400">
              The lesson doesn't move your mastery bar — only the quiz does. Each quiz is
              AI-generated, so it can't be memorised.
            </p>
          </div>
        </aside>
      </div>
    </div>
  );
}

function Dot() {
  return <span className="h-3.5 w-3.5 rounded-full border-2 border-slate-300" />;
}
