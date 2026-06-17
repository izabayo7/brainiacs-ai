"use client";

import { useEffect, useState } from "react";
import { useParams, useRouter } from "next/navigation";
import ReactMarkdown from "react-markdown";
import { api } from "@/lib/api";
import AskTutor from "@/components/AskTutor";

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
      {concept.summary && (
        <p className="mt-2 max-w-2xl text-body">{concept.summary}</p>
      )}

      {/* Study tip */}
      <div className="mt-6 flex gap-3 rounded-2xl border border-brand-100 bg-brand-50/60 p-4">
        <span className="step-badge mt-0.5 bg-brand-600 text-white">+</span>
        <div>
          <p className="text-sm text-ink">
            <span className="font-semibold">Tip:</span> read the idea, then trace the worked
            example yourself before the quiz — that's where mastery moves.
          </p>
          <p className="mt-0.5 font-mono text-xs text-slate-400">
            a study tip for this lesson
          </p>
        </div>
      </div>

      <div className="mt-6 grid gap-6 lg:grid-cols-[1fr_21rem]">
        {/* Main column — the lesson */}
        <div className="space-y-6">
          <div className="card p-6">
            <div className="prose-chapter">
              {chapter ? (
                <ReactMarkdown>{chapter.body_md}</ReactMarkdown>
              ) : (
                <ReactMarkdown>{concept.worked_example_md}</ReactMarkdown>
              )}
            </div>
          </div>
        </div>

        {/* Sidebar */}
        <aside className="space-y-6 lg:sticky lg:top-24 lg:self-start">
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

          <AskTutor conceptId={concept.id} conceptName={concept.name} />
        </aside>
      </div>
    </div>
  );
}

function Dot() {
  return <span className="h-3.5 w-3.5 rounded-full border-2 border-slate-300" />;
}
