import MasteryBar from "./MasteryBar";
import StatePill from "./StatePill";

// One concept tile in the "Your concept map" grid.
export default function ConceptCard({ concept, prereqName, onOpen }) {
  const { state, p_mastered } = concept;
  const pct = Math.round((p_mastered || 0) * 100);
  const locked = state === "locked";

  if (locked) {
    return (
      <div className="rounded-2xl border border-dashed border-line bg-white/40 p-4">
        <div className="mb-3 flex items-center gap-1.5 font-medium text-slate-400">
          <LockIcon /> {concept.name}
        </div>
        <MasteryBar value={0} locked />
        <p className="mt-3 text-xs text-slate-400">
          {prereqName ? `Unlocks when ${prereqName} is mastered` : "Locked"}
        </p>
      </div>
    );
  }

  return (
    <button
      type="button"
      onClick={() => onOpen(concept)}
      className="card group p-4 text-left transition hover:shadow-lift"
    >
      <div className="mb-3 flex items-start justify-between gap-2">
        <span className="font-semibold text-ink">{concept.name}</span>
        {state === "mastered" ? (
          <StatePill tone="mastered">MASTERED</StatePill>
        ) : pct === 0 ? (
          <StatePill tone="new">NEW</StatePill>
        ) : null}
      </div>
      <MasteryBar value={p_mastered} />
      <div className="mt-2 flex items-center justify-between text-sm">
        <span className="font-medium text-slate-500">{pct}%</span>
        <span className="font-mono text-xs text-slate-400 group-hover:text-brand-600">
          {state === "mastered" ? "review →" : "continue →"}
        </span>
      </div>
    </button>
  );
}

function LockIcon() {
  return (
    <svg className="h-4 w-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
      <rect x="5" y="11" width="14" height="9" rx="2" />
      <path d="M8 11V8a4 4 0 0 1 8 0v3" />
    </svg>
  );
}
