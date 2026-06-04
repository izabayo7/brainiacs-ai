// A calm, encouraging mastery indicator — words first, not a harsh percentage.

function label(p, mastered) {
  if (mastered) return "Mastered";
  if (p >= 0.6) return "Almost there";
  if (p >= 0.3) return "Building";
  if (p > 0) return "Getting started";
  return "Not started yet";
}

export default function MasteryMeter({ pMastered = 0, mastered = false }) {
  const pct = Math.round(Math.min(1, Math.max(0, pMastered)) * 100);
  const tone = mastered ? "bg-green-500" : "bg-calm";
  return (
    <div>
      <div className="flex items-center justify-between mb-1">
        <span className="text-sm font-medium text-gray-600">{label(pMastered, mastered)}</span>
      </div>
      <div className="h-3 w-full rounded-full bg-gray-200 overflow-hidden" role="progressbar"
           aria-valuenow={pct} aria-valuemin={0} aria-valuemax={100}>
        <div className={`h-full ${tone} transition-all duration-500`} style={{ width: `${pct}%` }} />
      </div>
    </div>
  );
}
