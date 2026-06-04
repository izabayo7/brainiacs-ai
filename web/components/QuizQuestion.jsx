"use client";

// Renders one question of any of the three pseudocode-safe types and reports the
// student's response upward. `graded` (optional) switches it into read-only result mode.

function move(arr, from, to) {
  const next = arr.slice();
  const [item] = next.splice(from, 1);
  next.splice(to, 0, item);
  return next;
}

export default function QuizQuestion({ index, question, value, onChange, graded }) {
  const disabled = Boolean(graded);

  return (
    <div className="rounded-xl border border-gray-200 bg-white p-5">
      <div className="flex items-start justify-between gap-4">
        <div className="flex-1">
          <span className="text-xs uppercase tracking-wide text-gray-400">
            Question {index + 1} · {question.type.replace("_", " ")} · {question.difficulty}
          </span>
          <pre className="whitespace-pre-wrap font-mono text-sm mt-2 mb-4 text-ink">
            {question.prompt}
          </pre>
        </div>
        {graded && (
          <span
            className={`shrink-0 text-xs px-2 py-1 rounded-full ${
              graded.is_correct ? "bg-green-100 text-green-700" : "bg-amber-100 text-amber-700"
            }`}
          >
            {graded.is_correct ? "Correct" : "Review"}
          </span>
        )}
      </div>

      {/* MCQ */}
      {question.type === "mcq" && (
        <div className="space-y-2">
          {(question.options || []).map((opt) => (
            <label
              key={opt}
              className={`flex items-center gap-3 rounded-lg border p-3 cursor-pointer ${
                value === opt ? "border-calm bg-calm/5" : "border-gray-200"
              } ${disabled ? "cursor-default" : ""}`}
            >
              <input
                type="radio"
                name={`q-${question.id}`}
                checked={value === opt}
                disabled={disabled}
                onChange={() => onChange(opt)}
              />
              <span className="text-sm">{opt}</span>
            </label>
          ))}
        </div>
      )}

      {/* Predict the output */}
      {question.type === "predict_output" && (
        <textarea
          rows={2}
          disabled={disabled}
          value={value || ""}
          onChange={(e) => onChange(e.target.value)}
          placeholder="What does this print?"
          className="w-full rounded-lg border border-gray-300 p-3 font-mono text-sm"
        />
      )}

      {/* Pseudocode ordering */}
      {question.type === "pseudocode_order" && (
        <ol className="space-y-2">
          {(value || question.options || []).map((line, i, arr) => (
            <li
              key={`${line}-${i}`}
              className="flex items-center gap-2 rounded-lg border border-gray-200 p-2"
            >
              <span className="text-gray-400 text-xs w-5">{i + 1}</span>
              <code className="flex-1 font-mono text-sm whitespace-pre">{line}</code>
              {!disabled && (
                <span className="flex gap-1">
                  <button
                    type="button"
                    aria-label="Move up"
                    disabled={i === 0}
                    onClick={() => onChange(move(arr, i, i - 1))}
                    className="px-2 py-1 rounded bg-gray-100 disabled:opacity-30"
                  >
                    ↑
                  </button>
                  <button
                    type="button"
                    aria-label="Move down"
                    disabled={i === arr.length - 1}
                    onClick={() => onChange(move(arr, i, i + 1))}
                    className="px-2 py-1 rounded bg-gray-100 disabled:opacity-30"
                  >
                    ↓
                  </button>
                </span>
              )}
            </li>
          ))}
        </ol>
      )}
    </div>
  );
}
