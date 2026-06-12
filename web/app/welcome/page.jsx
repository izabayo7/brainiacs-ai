"use client";

import { useRouter } from "next/navigation";

const STEPS = [
  {
    title: "Take a short baseline",
    body: "16 quick questions, about 15 minutes. It's not graded — it just shows us where to start you.",
  },
  {
    title: "See your starting map",
    body: "Your answers build a picture of your strengths across 8 programming concepts.",
  },
  {
    title: "Start learning",
    body: "The tutor picks your first exercise and adapts as you go — every session picks up where you left off.",
  },
];

export default function WelcomePage() {
  const router = useRouter();
  return (
    <div className="grid min-h-screen lg:grid-cols-[1fr_1.2fr]">
      {/* Dark hero */}
      <div className="relative flex flex-col justify-center overflow-hidden bg-slate-900 px-10 py-12 text-white">
        <div className="absolute inset-0 bg-[radial-gradient(110%_110%_at_100%_0%,rgba(99,102,241,.35),transparent_55%)]" />
        <div className="relative">
          <img
            src="/logo.svg"
            alt="Brainiacs AI"
            className="mb-10 h-9 w-auto [filter:brightness(0)_invert(1)]"
          />
          <h1 className="text-4xl font-semibold">You're in! 🎉</h1>
          <p className="mt-4 max-w-md text-white/70">
            You have now joined African Leadership University on Brainiacs AI — a tutor
            that learns how you think about code, and coaches you concept by concept.
          </p>
          <p className="mt-4 max-w-md text-white/70">
            One thing to know: it guides your reasoning with hints — it won't hand you
            solutions.
          </p>
        </div>
      </div>

      {/* Next steps */}
      <div className="flex items-center bg-white px-10 py-12">
        <div className="w-full max-w-lg">
          <h2 className="text-sm font-semibold uppercase tracking-widest text-brand-600">
            Next steps
          </h2>
          <ol className="mt-6 space-y-6">
            {STEPS.map((s, i) => (
              <li key={i} className="flex gap-4">
                <span className="grid h-9 w-9 shrink-0 place-items-center rounded-full bg-brand-600 font-semibold text-white">
                  {i + 1}
                </span>
                <div>
                  <p className="font-semibold text-ink">{s.title}</p>
                  <p className="mt-1 text-sm text-body">{s.body}</p>
                </div>
              </li>
            ))}
          </ol>

          <div className="mt-8 flex gap-2 rounded-xl border border-line bg-mist p-3 text-xs text-body">
            <span>ⓘ</span>
            <p>
              Before you start: answers are final (no going back), "I'm not sure" is always
              a valid answer, and no scores show until the end. Your progress saves
              automatically — even if your connection drops.
            </p>
          </div>

          <button
            onClick={() => router.push("/")}
            className="mt-8 rounded-xl bg-brand-600 px-6 py-3 font-medium text-white transition hover:bg-brand-700"
          >
            Start my baseline assessment →
          </button>
        </div>
      </div>
    </div>
  );
}
