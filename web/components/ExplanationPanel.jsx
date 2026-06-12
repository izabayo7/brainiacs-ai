// Scaffolded feedback for a wrong answer — indigo left-border block, matching the
// "Ask the tutor" answer styling in the Figma.

function prettyLabel(label) {
  return label === "none" ? "no misconception" : label.replace(/_/g, " ");
}

export default function ExplanationPanel({ graded }) {
  if (!graded || graded.is_correct) return null;
  return (
    <div className="mt-3 rounded-r-xl border-l-4 border-brand-600 bg-slate-50 p-4">
      <div className="mb-1 font-mono text-xs uppercase tracking-wide text-brand-700">
        misconception · {prettyLabel(graded.misconception_label)}
      </div>
      <p className="text-sm leading-relaxed text-ink">{graded.explanation}</p>
    </div>
  );
}
