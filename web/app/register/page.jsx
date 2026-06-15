"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { signIn } from "next-auth/react";
import { api } from "@/lib/api";

export default function RegisterPage() {
  const router = useRouter();
  const [form, setForm] = useState({ name: "", email: "", password: "" });
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(false);

  const set = (k) => (e) => setForm((f) => ({ ...f, [k]: e.target.value }));

  async function submit(e) {
    e.preventDefault();
    setError(null);
    setLoading(true);
    try {
      await api.register(form);
      const res = await signIn("credentials", {
        email: form.email,
        password: form.password,
        redirect: false,
      });
      if (res?.ok) router.push("/welcome");
      else router.push("/login");
    } catch (err) {
      setError(err.message || "Could not create your account.");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="grid min-h-screen lg:grid-cols-2">
      <div className="relative hidden overflow-hidden lg:block">
        <img src="/login-hero.jpg" alt="" className="absolute inset-0 h-full w-full object-cover" />
        <div className="absolute inset-0 bg-gradient-to-b from-teal-500/70 via-emerald-600/55 to-emerald-900/80" />
        <img src="/logo.svg" alt="Brainiacs AI"
          className="absolute left-8 top-8 h-9 w-auto [filter:brightness(0)_invert(1)]" />
        <p className="absolute bottom-12 left-8 right-12 text-2xl font-semibold leading-snug text-white drop-shadow">
          Learn the fundamentals of programming, one mastered concept at a time.
        </p>
      </div>

      <div className="flex items-center justify-center bg-white px-6 py-10">
        <form onSubmit={submit} className="w-full max-w-sm">
          <img src="/logo.svg" alt="Brainiacs AI" className="mb-8 h-9 w-auto lg:hidden" />
          <h1 className="text-2xl font-semibold">Create your account</h1>
          <p className="mt-1 text-sm text-body">Start learning in a couple of minutes.</p>

          <button type="button" onClick={() => signIn("google", { callbackUrl: "/welcome" })}
            className="mt-6 flex w-full items-center justify-center gap-2 rounded-xl border border-line bg-white py-2.5 font-medium text-ink transition hover:bg-mist">
            Continue with Google
          </button>

          <div className="my-5 flex items-center gap-3 text-xs text-slate-400">
            <span className="h-px flex-1 bg-line" /> OR <span className="h-px flex-1 bg-line" />
          </div>

          <label className="block text-sm font-medium text-ink">Name</label>
          <input required value={form.name} onChange={set("name")} placeholder="Your name"
            className="mt-1 w-full rounded-xl border border-line px-3.5 py-2.5 text-sm focus:border-brand-500 focus:outline-none" />

          <label className="mt-4 block text-sm font-medium text-ink">Email</label>
          <input type="email" required value={form.email} onChange={set("email")} placeholder="you@example.com"
            className="mt-1 w-full rounded-xl border border-line px-3.5 py-2.5 text-sm focus:border-brand-500 focus:outline-none" />

          <label className="mt-4 block text-sm font-medium text-ink">Password</label>
          <input type="password" required minLength={6} value={form.password} onChange={set("password")}
            placeholder="At least 6 characters"
            className="mt-1 w-full rounded-xl border border-line px-3.5 py-2.5 text-sm focus:border-brand-500 focus:outline-none" />

          {error && <p className="mt-3 text-sm text-red-600">{error}</p>}

          <button type="submit" disabled={loading}
            className="mt-6 w-full rounded-xl bg-brand-600 py-3 font-medium text-white transition hover:bg-brand-700 disabled:opacity-50">
            {loading ? "Creating…" : "Create account"}
          </button>

          <p className="mt-6 text-center text-sm text-body">
            Already have an account?{" "}
            <a href="/login" className="font-medium text-brand-600 hover:underline">Log in</a>
          </p>
        </form>
      </div>
    </div>
  );
}
