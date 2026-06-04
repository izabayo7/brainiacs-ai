"use client";

import { useEffect, useState } from "react";
import { useParams, useRouter } from "next/navigation";
import ReactMarkdown from "react-markdown";
import { api } from "@/lib/api";
import { getStudentId } from "@/lib/student";

export default function ConceptPage() {
  const { id } = useParams();
  const router = useRouter();
  const [concept, setConcept] = useState(null);
  const [error, setError] = useState(null);

  useEffect(() => {
    const sid = getStudentId();
    if (!sid) {
      router.replace("/");
      return;
    }
    api
      .getConcept(id, sid)
      .then(setConcept)
      .catch((e) => setError(e));
  }, [id, router]);

  if (error) {
    const locked = error.status === 403;
    return (
      <div className="rounded-xl border border-gray-200 bg-white p-8 text-center">
        <p className="text-4xl mb-3">{locked ? "🔒" : "⚠️"}</p>
        <h1 className="text-xl font-semibold mb-2">
          {locked ? "This concept is locked" : "Something went wrong"}
        </h1>
        <p className="text-gray-600 mb-5">
          {locked ? "Master its prerequisites first to unlock it." : error.message}
        </p>
        <a href="/" className="text-calm font-medium">
          ← Back to your path
        </a>
      </div>
    );
  }

  if (!concept) return <p className="text-gray-500">Loading…</p>;

  return (
    <article>
      <a href="/" className="text-sm text-gray-500 hover:text-calm">
        ← Your path
      </a>
      <h1 className="text-3xl font-semibold mt-2 mb-6">{concept.name}</h1>

      <div className="prose-chapter rounded-2xl border border-gray-200 bg-white p-8">
        {concept.chapters.map((ch) => (
          <div key={ch.id}>
            <ReactMarkdown>{ch.body_md}</ReactMarkdown>
            {ch.video_url && (
              <div className="my-4 aspect-video">
                <iframe
                  src={ch.video_url}
                  title={ch.title}
                  className="w-full h-full rounded-lg"
                  allowFullScreen
                />
              </div>
            )}
          </div>
        ))}
      </div>

      <div className="mt-6 flex items-center gap-4">
        <button
          onClick={() => router.push(`/quiz/${concept.id}`)}
          className="rounded-xl bg-calm px-6 py-3 text-white font-medium hover:bg-calm/90"
        >
          Start quiz →
        </button>
        {concept.state === "mastered" && (
          <span className="text-sm text-green-700">You've already mastered this — review or move on.</span>
        )}
      </div>
    </article>
  );
}
