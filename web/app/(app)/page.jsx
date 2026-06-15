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
  const [nextSlug, setNextSlug] = useState(null);
  const [error, setError] = useState(null);

  useEffect(() => {
    Promise.all([api.listConcepts(), api.getProgress()])
      .then(([cs, progress]) => {
        setConcepts(cs);
        setNextSlug(progress.next_concept_slug);
      })
      .catch((e) => setError(e.message));
  }, []);

  const nameById = Object.fromEntries(concepts.map((c) => [c.id, c.name]));
  const nextConcept = concepts.find((c) => c.slug === nextSlug);
  const masteredCount = concepts.filter((c) => c.state === "mastered").length;
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
            This is your next concept. Read the short lesson, then a quick AI-generated
            quiz adapts to how you answer.
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
