const TONES = {
  mastered: "bg-emerald-100 text-emerald-700",
  new: "bg-brand-50 text-brand-700",
  available: "bg-slate-100 text-slate-600",
  amber: "bg-orange-100 text-orange-700",
};

export default function StatePill({ tone = "available", children }) {
  return (
    <span className={`rounded-full px-2.5 py-0.5 text-[11px] font-semibold tracking-wide ${TONES[tone] || TONES.available}`}>
      {children}
    </span>
  );
}
