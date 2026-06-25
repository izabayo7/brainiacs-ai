"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { useSession } from "next-auth/react";
import { api } from "@/lib/api";
import ConceptCard from "@/components/ConceptCard";

export default function Dashboard() {
  const router = useRouter();
  const { data: session } = useSession();
  const [concepts, setConcepts] = useState([]);
  const [progress, setProgress] = useState(null);
  const [error, setError] = useState(null);

  useEffect(() => {
    Promise.all([api.listConcepts(), api.getProgress()])
      .then(([cs, prog]) => {
        setConcepts(cs);
        setProgress(prog);
      })
      .catch((e) => setError(e.message));
  }, []);

  const nameById = Object.fromEntries(concepts.map((c) => [c.id, c.name]));
  const nextConcept = concepts.find((c) => c.slug === progress?.next_concept_slug);
  const masteredCount = concepts.filter((c) => c.state === "mastered").length;
  const avgMastery = concepts.length
    ? Math.round((concepts.reduce((s, c) => s + (c.p_mastered || 0), 0) / concepts.length) * 100)
    : 0;
  const firstName = (session?.user?.name || "").split(" ")[0];

  const openConcept = (concept) => router.push(`/concept/${concept.id}`);

  return (
    <div className="space-y-8">
      <div>
        <h1 className="text-3xl font-semibold tracking-tight">
          Welcome back{firstName ? `, ${firstName}` : ""} 👋
        </h1>
        <p className="mt-1 text-body">
          {masteredCount > 0
            ? `You've mastered ${masteredCount} concept${masteredCount > 1 ? "s" : ""} so far · keep the streak going`
            : "Let's find where to start you — work through the concepts in order."}
        </p>
      </div>

      {error && (
        <div className="card border-red-200 bg-red-50 p-4 text-sm text-red-700">
          Could not reach the API ({error}). Is the backend running on :8000?
        </div>
      )}

      {nextConcept ? (
        <div className="relative overflow-hidden rounded-2xl border border-line bg-white p-7 shadow-card">
          <span className="absolute inset-y-0 left-0 w-1.5 bg-brand-600" />
          <span className="inline-block rounded-full bg-brand-50 px-3 py-1 text-xs font-semibold text-brand-700">
            Pick up where you left off
          </span>
          <h2 className="mt-3 text-2xl font-semibold">{nextConcept.name}</h2>
          <p className="mt-2 max-w-xl text-body">
            This is your next concept. Read the short lesson, then a quick quiz — the
            tutor tracks your mastery and adapts what comes next.
          </p>
          <div className="mt-5 flex items-center gap-4">
            <button onClick={() => openConcept(nextConcept)}
              className="rounded-xl bg-brand-600 px-6 py-3 font-medium text-white transition hover:bg-brand-700">
              Continue →
            </button>
            <span className="font-mono text-sm text-slate-400">~10 min lesson · adaptive quiz</span>
          </div>
        </div>
      ) : concepts.length > 0 ? (
        <div className="rounded-2xl border border-emerald-200 bg-emerald-50 p-7">
          <h2 className="text-xl font-semibold">🎉 All available concepts mastered</h2>
          <p className="mt-2 text-body">Nothing left to unlock right now — great work!</p>
        </div>
      ) : null}

      {progress && (
        <div className="rounded-2xl border border-line bg-white p-6 shadow-card">
          <div className="flex items-center justify-between">
            <h2 className="text-sm font-semibold uppercase tracking-wide text-brand-600">
              Your learner model
            </h2>
            <span className="font-mono text-xs text-slate-400">
              Bayesian Knowledge Tracing · updates as you practice
            </span>
          </div>
          <div className="mt-4 grid gap-3 sm:grid-cols-3">
            <Stat label="avg mastery" value={`${avgMastery}%`} />
            <Stat label="concepts mastered" value={`${masteredCount} / ${concepts.length}`} />
            <Stat label="attempts tracked" value={progress.total_attempts ?? 0} />
          </div>
          <div className="mt-5">
            <p className="text-sm font-medium text-ink">What the system has noticed</p>
            {progress.recurring_difficulties?.length ? (
              <div className="mt-2 flex flex-wrap gap-2">
                {progress.recurring_difficulties.map((d) => (
                  <span key={d.label}
                    className="rounded-full bg-amber-50 px-3 py-1 text-xs font-medium text-amber-800">
                    {d.human} · {d.count}×
                  </span>
                ))}
              </div>
            ) : (
              <p className="mt-1 text-sm text-body">
                Not enough data yet — take a few quizzes and your model fills in.
              </p>
            )}
          </div>
        </div>
      )}

      <div>
        <div className="mb-4 flex items-center justify-between">
          <h2 className="text-sm font-semibold uppercase tracking-wide text-slate-500">
            Your concept map
          </h2>
          <span className="font-mono text-xs text-slate-400">
            {masteredCount}/{concepts.length} mastered · unlock at 85%
          </span>
        </div>
        <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
          {concepts.map((c) => (
            <ConceptCard
              key={c.id}
              concept={c}
              prereqName={c.prerequisite_ids?.map((id) => nameById[id]).filter(Boolean).join(", ")}
              onOpen={openConcept}
            />
          ))}
        </div>
      </div>
    </div>
  );
}

function Stat({ label, value }) {
  return (
    <div className="rounded-xl border border-line bg-mist/50 px-4 py-3">
      <p className="text-2xl font-semibold text-ink">{value}</p>
      <p className="mt-0.5 text-xs uppercase tracking-wide text-slate-500">{label}</p>
    </div>
  );
}
