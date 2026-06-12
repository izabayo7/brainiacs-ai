"use client";

// One question of any of the three pseudocode-safe types, styled like the Figma
// baseline-test workspace. `graded` switches it into read-only result mode.

function move(arr, from, to) {
  const next = arr.slice();
  const [item] = next.splice(from, 1);
  next.splice(to, 0, item);
  return next;
}

export default function QuizQuestion({ index, question, value, onChange, graded }) {
  const disabled = Boolean(graded);

  return (
    <div className="card p-6">
      <div className="mb-3 flex items-start justify-between gap-4">
        <div className="flex items-center gap-3">
          <span className="step-badge">{index + 1}</span>
          <span className="font-mono text-xs uppercase tracking-wide text-slate-400">
            {question.type.replace("_", " ")} · {question.difficulty}
          </span>
        </div>
        {graded && (
          <span
            className={`shrink-0 rounded-full px-2.5 py-0.5 text-xs font-semibold ${
              graded.is_correct ? "bg-emerald-100 text-emerald-700" : "bg-orange-100 text-orange-700"
            }`}
          >
            {graded.is_correct ? "Correct" : "Review"}
          </span>
        )}
      </div>

      {/* Prompt — pseudocode shown in a code panel */}
      <pre className="mb-4 whitespace-pre-wrap rounded-xl bg-slate-50 p-4 font-mono text-sm text-ink">
        {question.prompt}
      </pre>

      {/* MCQ */}
      {question.type === "mcq" && (
        <div className="space-y-2">
          {(question.options || []).map((opt) => {
            const active = value === opt;
            return (
              <button
                key={opt}
                type="button"
                disabled={disabled}
                onClick={() => onChange(opt)}
                className={`flex w-full items-center gap-3 rounded-xl border p-3 text-left text-sm transition ${
                  active ? "border-brand-600 bg-brand-50" : "border-line hover:border-brand-300"
                } ${disabled ? "cursor-default" : ""}`}
              >
                <span className={`grid h-4 w-4 place-items-center rounded-full border ${active ? "border-brand-600" : "border-slate-300"}`}>
                  {active && <span className="h-2 w-2 rounded-full bg-brand-600" />}
                </span>
                {opt}
              </button>
            );
          })}
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
          className="w-full rounded-xl border border-line p-3 font-mono text-sm focus:border-brand-400 focus:outline-none"
        />
      )}

      {/* Pseudocode ordering */}
      {question.type === "pseudocode_order" && (
        <ol className="space-y-2">
          {(value || question.options || []).map((line, i, arr) => (
            <li key={`${line}-${i}`} className="flex items-center gap-2 rounded-xl border border-line p-2">
              <span className="w-5 text-center font-mono text-xs text-slate-400">{i + 1}</span>
              <code className="flex-1 whitespace-pre font-mono text-sm">{line}</code>
              {!disabled && (
                <span className="flex gap-1">
                  <button type="button" aria-label="Move up" disabled={i === 0}
                    onClick={() => onChange(move(arr, i, i - 1))}
                    className="rounded-lg bg-slate-100 px-2 py-1 disabled:opacity-30">↑</button>
                  <button type="button" aria-label="Move down" disabled={i === arr.length - 1}
                    onClick={() => onChange(move(arr, i, i + 1))}
                    className="rounded-lg bg-slate-100 px-2 py-1 disabled:opacity-30">↓</button>
                </span>
              )}
            </li>
          ))}
        </ol>
      )}
    </div>
  );
}
