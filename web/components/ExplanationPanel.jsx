// Shows the scaffolded explanation + named misconception for a graded answer.

const PRETTY = {
  none: "No misconception — well done",
};

function prettyLabel(label) {
  if (PRETTY[label]) return PRETTY[label];
  return label.replace(/_/g, " ");
}

export default function ExplanationPanel({ graded }) {
  if (!graded || graded.is_correct) return null;
  return (
    <div className="mt-3 rounded-lg border border-amber-200 bg-amber-50 p-4">
      <div className="text-xs font-semibold uppercase tracking-wide text-amber-700 mb-1">
        Misconception: {prettyLabel(graded.misconception_label)}
      </div>
      <p className="text-sm text-ink leading-relaxed">{graded.explanation}</p>
    </div>
  );
}
