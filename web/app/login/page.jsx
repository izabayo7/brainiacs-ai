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
      {/* Hero panel — real photo with an indigo brand wash */}
      <div className="relative hidden overflow-hidden lg:block">
        <img src="/login-hero.jpg" alt="A learner studying programming"
          className="absolute inset-0 h-full w-full object-cover" />
        <div className="absolute inset-0 bg-gradient-to-b from-brand-600/70 via-brand-700/70 to-ink/90" />
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

          <label className="mt-6 block text-sm font-medium text-ink">Email</label>
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
