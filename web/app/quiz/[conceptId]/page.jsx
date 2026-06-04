"use client";

import { useEffect, useState } from "react";
import { useParams, useRouter } from "next/navigation";
import { api } from "@/lib/api";
import { getStudentId } from "@/lib/student";
import QuizQuestion from "@/components/QuizQuestion";
import ExplanationPanel from "@/components/ExplanationPanel";
import MasteryMeter from "@/components/MasteryMeter";

export default function QuizPage() {
  const { conceptId } = useParams();
  const router = useRouter();

  const [studentId, setStudentId] = useState(null);
  const [quiz, setQuiz] = useState(null);
  const [responses, setResponses] = useState({});
  const [result, setResult] = useState(null);
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState(null);

  useEffect(() => {
    const sid = getStudentId();
    if (!sid) {
      router.replace("/");
      return;
    }
    setStudentId(sid);
    api
      .generateQuiz(conceptId, sid)
      .then((q) => {
        setQuiz(q);
        // Seed ordering questions with their initial (shuffled) line order.
        const init = {};
        q.questions.forEach((question) => {
          if (question.type === "pseudocode_order") init[question.id] = question.options || [];
        });
        setResponses(init);
      })
      .catch((e) => setError(e));
  }, [conceptId, router]);

  function setResponse(qid, value) {
    setResponses((prev) => ({ ...prev, [qid]: value }));
  }

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
        student_id: studentId,
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
      <div className="rounded-xl border border-gray-200 bg-white p-8 text-center">
        <p className="text-4xl mb-3">{locked ? "🔒" : "⚠️"}</p>
        <h1 className="text-xl font-semibold mb-2">
          {locked ? "This quiz is locked" : "Could not start the quiz"}
        </h1>
        <p className="text-gray-600 mb-5">{error.message}</p>
        <a href="/" className="text-calm font-medium">← Back to your path</a>
      </div>
    );
  }

  if (!quiz) return <p className="text-gray-500">Generating your quiz…</p>;

  const gradedById = {};
  (result?.graded || []).forEach((g) => (gradedById[g.question_id] = g));

  return (
    <div>
      <a href="/" className="text-sm text-gray-500 hover:text-calm">← Your path</a>
      <div className="flex items-center justify-between mt-2 mb-6">
        <h1 className="text-2xl font-semibold">Quiz</h1>
        <span className="text-xs px-2 py-1 rounded-full bg-gray-100 text-gray-500">
          {quiz.source === "llm" ? "AI-generated for you" : "practice set"}
        </span>
      </div>

      {/* Result summary */}
      {result && (
        <div className="mb-6 rounded-2xl border border-gray-200 bg-white p-6">
          <p className="text-lg font-medium mb-3">{result.encouragement}</p>
          <MasteryMeter pMastered={result.p_mastered} mastered={result.mastered} />
          {result.newly_unlocked.length > 0 && (
            <p className="mt-4 text-green-700">
              🔓 You just unlocked: {result.newly_unlocked.join(", ")}
            </p>
          )}
          <div className="mt-5 flex gap-3">
            {result.mastered ? (
              <button
                onClick={() => router.push("/")}
                className="rounded-xl bg-green-600 px-5 py-2.5 text-white font-medium"
              >
                Back to path →
              </button>
            ) : (
              <button
                onClick={() => window.location.reload()}
                className="rounded-xl bg-calm px-5 py-2.5 text-white font-medium"
              >
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
          {error && <p className="text-red-600 mb-3">{error.message}</p>}
          <button
            onClick={handleSubmit}
            disabled={submitting}
            className="rounded-xl bg-calm px-6 py-3 text-white font-medium hover:bg-calm/90 disabled:opacity-50"
          >
            {submitting ? "Grading…" : "Submit answers"}
          </button>
        </div>
      )}
    </div>
  );
}
