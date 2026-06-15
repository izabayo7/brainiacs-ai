"use client";

import { useEffect, useState } from "react";
import { useParams, useRouter } from "next/navigation";
import { api } from "@/lib/api";
import QuizQuestion from "@/components/QuizQuestion";
import ExplanationPanel from "@/components/ExplanationPanel";
import MasteryBar from "@/components/MasteryBar";

export default function QuizPage() {
  const { conceptId } = useParams();
  const router = useRouter();

  const [quiz, setQuiz] = useState(null);
  const [responses, setResponses] = useState({});
  const [result, setResult] = useState(null);
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState(null);

  useEffect(() => {
    api
      .generateQuiz(conceptId)
      .then((q) => {
        setQuiz(q);
        const init = {};
        q.questions.forEach((question) => {
          if (question.type === "pseudocode_order") init[question.id] = question.options || [];
        });
        setResponses(init);
      })
      .catch((e) => setError(e));
  }, [conceptId, router]);

  const setResponse = (qid, v) => setResponses((p) => ({ ...p, [qid]: v }));

  async function handleSubmit() {
    setSubmitting(true);
    setError(null);
    try {
      const answers = quiz.questions.map((q) => ({
        question_id: q.id,
        type: q.type,
        prompt: q.prompt,
        reference_answer: null,
        response: responses[q.id] ?? "",
      }));
      const res = await api.submitQuiz(conceptId, {
        concept_id: Number(conceptId),
        answers,
      });
      setResult(res);
      window.scrollTo({ top: 0, behavior: "smooth" });
    } catch (e) {
      setError(e);
    } finally {
      setSubmitting(false);
    }
  }

  if (error && !quiz) {
    const locked = error.status === 403;
    return (
      <div className="card mx-auto max-w-lg p-10 text-center">
        <p className="mb-3 text-4xl">{locked ? "🔒" : "⚠️"}</p>
        <h1 className="mb-2 text-xl font-semibold">
          {locked ? "This quiz is locked" : "Could not start the quiz"}
        </h1>
        <p className="mb-5 text-body">{error.message}</p>
        <a href="/" className="font-medium text-brand-600">← Back to your path</a>
      </div>
    );
  }
  if (!quiz) return <p className="text-slate-400">Generating your quiz…</p>;

  const gradedById = {};
  (result?.graded || []).forEach((g) => (gradedById[g.question_id] = g));

  return (
    <div>
      <div className="mb-6 flex items-center justify-between">
        <a href="/" className="text-sm text-slate-500 hover:text-brand-600">‹ Your path</a>
        <span className="rounded-full bg-brand-50 px-3 py-1 font-mono text-xs text-brand-700">
          {quiz.source === "llm" ? "AI-generated for you" : "practice set"}
        </span>
      </div>
      <h1 className="mb-6 text-2xl font-semibold tracking-tight">Quick check</h1>

      {/* Result summary */}
      {result && (
        <div className="card mb-6 p-6">
          <p className="text-lg font-medium">{result.encouragement}</p>
          <div className="mt-4">
            <MasteryBar value={result.p_mastered} />
            <p className="mt-2 font-mono text-xs text-slate-400">
              mastery {Math.round(result.p_mastered * 100)}% · {result.mastered ? "concept mastered" : "unlock at 85%"}
            </p>
          </div>
          {result.newly_unlocked.length > 0 && (
            <p className="mt-4 font-medium text-emerald-700">
              🔓 You just unlocked: {result.newly_unlocked.join(", ")}
            </p>
          )}
          <div className="mt-5 flex gap-3">
            {result.mastered ? (
              <button onClick={() => router.push("/")}
                className="rounded-xl bg-emerald-600 px-5 py-2.5 font-medium text-white">
                Back to path →
              </button>
            ) : (
              <button onClick={() => window.location.reload()}
                className="rounded-xl bg-brand-600 px-5 py-2.5 font-medium text-white hover:bg-brand-700">
                Practise again
              </button>
            )}
          </div>
        </div>
      )}

      {/* Questions */}
      <div className="space-y-4">
        {quiz.questions.map((q, i) => (
          <div key={q.id}>
            <QuizQuestion
              index={i}
              question={q}
              value={responses[q.id]}
              onChange={(v) => setResponse(q.id, v)}
              graded={gradedById[q.id]}
            />
            <ExplanationPanel graded={gradedById[q.id]} />
          </div>
        ))}
      </div>

      {!result && (
        <div className="mt-6">
          {error && <p className="mb-3 text-red-600">{error.message}</p>}
          <button
            onClick={handleSubmit}
            disabled={submitting}
            className="rounded-xl bg-brand-600 px-6 py-3 font-medium text-white transition hover:bg-brand-700 disabled:opacity-50"
          >
            {submitting ? "Grading…" : "Submit answers"}
          </button>
        </div>
      )}
    </div>
  );
}
