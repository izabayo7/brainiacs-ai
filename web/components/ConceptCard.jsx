import MasteryMeter from "./MasteryMeter";

const STATE_STYLES = {
  mastered: { ring: "border-green-300 bg-green-50", chip: "bg-green-100 text-green-700", icon: "✓" },
  available: { ring: "border-calm/40 bg-white", chip: "bg-calm/10 text-calm", icon: "→" },
  locked: { ring: "border-gray-200 bg-gray-50 opacity-70", chip: "bg-gray-100 text-gray-500", icon: "🔒" },
};

export default function ConceptCard({ concept, onOpen }) {
  const s = STATE_STYLES[concept.state] || STATE_STYLES.locked;
  const clickable = concept.state !== "locked";
  return (
    <button
      type="button"
      disabled={!clickable}
      onClick={() => clickable && onOpen(concept)}
      className={`text-left w-full rounded-xl border p-4 transition ${s.ring} ${
        clickable ? "hover:shadow-md cursor-pointer" : "cursor-not-allowed"
      }`}
    >
      <div className="flex items-center justify-between mb-2">
        <span className="font-medium">{concept.name}</span>
        <span className={`text-xs px-2 py-0.5 rounded-full ${s.chip}`}>
          {s.icon} {concept.state}
        </span>
      </div>
      <MasteryMeter pMastered={concept.p_mastered} mastered={concept.state === "mastered"} />
    </button>
  );
}
