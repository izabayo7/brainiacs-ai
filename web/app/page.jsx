"use client";

import { useEffect, useState, useCallback } from "react";
import { useRouter } from "next/navigation";
import { api } from "@/lib/api";
import StudentPicker from "@/components/StudentPicker";
import ConceptMap from "@/components/ConceptMap";

export default function Dashboard() {
  const router = useRouter();
  const [studentId, setStudentId] = useState(null);
  const [concepts, setConcepts] = useState([]);
  const [nextSlug, setNextSlug] = useState(null);
  const [error, setError] = useState(null);

  const load = useCallback((sid) => {
    if (!sid) return;
    setError(null);
    Promise.all([api.listConcepts(sid), api.getProgress(sid)])
      .then(([cs, progress]) => {
        setConcepts(cs);
        setNextSlug(progress.next_concept_slug);
      })
      .catch((e) => setError(e.message));
  }, []);

  useEffect(() => {
    if (studentId) load(studentId);
  }, [studentId, load]);

  const nextConcept = concepts.find((c) => c.slug === nextSlug);

  function openConcept(concept) {
    router.push(`/concept/${concept.id}`);
  }

  return (
    <div>
      <div className="flex items-center justify-between mb-8">
        <div>
          <h1 className="text-2xl font-semibold">Your learning path</h1>
          <p className="text-gray-500 text-sm mt-1">
            Work through the concepts in order. Each unlocks the next.
          </p>
        </div>
        <StudentPicker onChange={setStudentId} />
      </div>

      {error && <p className="text-red-600 mb-4">Could not reach the API: {error}</p>}

      <div className="grid gap-8 md:grid-cols-[20rem_1fr]">
        {/* Left pane: the map */}
        <aside>
          <ConceptMap concepts={concepts} onOpen={openConcept} />
        </aside>

        {/* Main pane: what's next */}
        <section>
          <h2 className="text-sm font-semibold uppercase tracking-wide text-gray-500 mb-3">
            What's next
          </h2>
          {nextConcept ? (
            <div className="rounded-2xl border border-calm/30 bg-white p-8">
              <p className="text-gray-500 text-sm">Continue with</p>
              <h3 className="text-2xl font-semibold mt-1 mb-4">{nextConcept.name}</h3>
              <button
                onClick={() => openConcept(nextConcept)}
                className="rounded-xl bg-calm px-6 py-3 text-white font-medium hover:bg-calm/90"
              >
                Continue →
              </button>
            </div>
          ) : (
            <div className="rounded-2xl border border-green-200 bg-green-50 p-8">
              <h3 className="text-xl font-semibold">🎉 All available concepts mastered</h3>
              <p className="text-gray-600 mt-2">
                Nothing left to unlock right now. Great work!
              </p>
            </div>
          )}
        </section>
      </div>
    </div>
  );
}
