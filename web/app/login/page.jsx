"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { signIn } from "next-auth/react";

export default function LoginPage() {
  const router = useRouter();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(false);

  async function submit(e) {
    e.preventDefault();
    setError(null);
    setLoading(true);
    const res = await signIn("credentials", { email, password, redirect: false });
    setLoading(false);
    if (res?.ok) router.push("/");
    else setError("Incorrect email or password.");
  }

  return (
    <div className="grid min-h-screen lg:grid-cols-2">
      {/* Hero panel — real photo with a teal/emerald wash */}
      <div className="relative hidden overflow-hidden lg:block">
        <img src="/login-hero.jpg" alt="A learner studying programming"
          className="absolute inset-0 h-full w-full object-cover" />
        <div className="absolute inset-0 bg-gradient-to-b from-teal-500/70 via-emerald-600/55 to-emerald-900/80" />
        <img src="/logo.svg" alt="Brainiacs AI"
          className="absolute left-8 top-8 h-9 w-auto [filter:brightness(0)_invert(1)]" />
        <p className="absolute bottom-12 left-8 right-12 text-2xl font-semibold leading-snug text-white drop-shadow">
          A curriculum-aware AI tutoring platform for teaching programming fundamentals
          to beginners.
        </p>
      </div>

      {/* Form panel */}
      <div className="flex items-center justify-center bg-white px-6 py-10">
        <form onSubmit={submit} className="w-full max-w-sm">
          <img src="/logo.svg" alt="Brainiacs AI" className="mb-8 h-9 w-auto lg:hidden" />
          <h1 className="text-2xl font-semibold">Login to continue</h1>
          <p className="mt-1 text-sm text-body">
            Welcome back, enter your credentials to continue
          </p>

          <button
            type="button"
            onClick={() => signIn("google", { callbackUrl: "/" })}
            className="mt-6 flex w-full items-center justify-center gap-2 rounded-xl border border-line bg-white py-2.5 font-medium text-ink transition hover:bg-mist"
          >
            <GoogleIcon /> Continue with Google
          </button>

          <div className="my-5 flex items-center gap-3 text-xs text-slate-400">
            <span className="h-px flex-1 bg-line" /> OR <span className="h-px flex-1 bg-line" />
          </div>

          <label className="block text-sm font-medium text-ink">Email</label>
          <input type="email" required value={email} onChange={(e) => setEmail(e.target.value)}
            placeholder="you@example.com"
            className="mt-1 w-full rounded-xl border border-line px-3.5 py-2.5 text-sm focus:border-brand-500 focus:outline-none" />

          <label className="mt-4 block text-sm font-medium text-ink">Password</label>
          <input type="password" required value={password} onChange={(e) => setPassword(e.target.value)}
            placeholder="Enter your password"
            className="mt-1 w-full rounded-xl border border-line px-3.5 py-2.5 text-sm focus:border-brand-500 focus:outline-none" />

          {error && <p className="mt-3 text-sm text-red-600">{error}</p>}

          <button type="submit" disabled={loading}
            className="mt-6 w-full rounded-xl bg-brand-600 py-3 font-medium text-white transition hover:bg-brand-700 disabled:opacity-50">
            {loading ? "Signing in…" : "Log in"}
          </button>

          <p className="mt-6 text-center text-sm text-body">
            New here?{" "}
            <a href="/register" className="font-medium text-brand-600 hover:underline">Create an account</a>
          </p>
        </form>
      </div>
    </div>
  );
}

function GoogleIcon() {
  return (
    <svg className="h-5 w-5" viewBox="0 0 24 24">
      <path fill="#4285F4" d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92a5.06 5.06 0 0 1-2.2 3.32v2.77h3.57c2.08-1.92 3.27-4.74 3.27-8.1z"/>
      <path fill="#34A853" d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84A11 11 0 0 0 12 23z"/>
      <path fill="#FBBC05" d="M5.84 14.1a6.6 6.6 0 0 1 0-4.2V7.06H2.18a11 11 0 0 0 0 9.88l3.66-2.84z"/>
      <path fill="#EA4335" d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.06l3.66 2.84C6.71 7.31 9.14 5.38 12 5.38z"/>
    </svg>
  );
}
