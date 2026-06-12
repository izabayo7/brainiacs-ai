// Segmented mastery bar — emerald fill on a light track, with subtle tick marks
// (echoing the Figma's "ticks: unlock / mastered" treatment).
export default function MasteryBar({ value = 0, locked = false }) {
  const pct = Math.round(Math.min(1, Math.max(0, value)) * 100);
  return (
    <div className="relative h-2.5 w-full overflow-hidden rounded-full bg-slate-100">
      {!locked && (
        <div
          className="h-full rounded-full bg-emerald-500 transition-all duration-500"
          style={{ width: `${pct}%` }}
        />
      )}
      {/* tick marks at the unlock/mastery thresholds */}
      {[60, 85].map((t) => (
        <span
          key={t}
          className="absolute top-0 h-full w-px bg-white/70"
          style={{ left: `${t}%` }}
        />
      ))}
    </div>
  );
}
