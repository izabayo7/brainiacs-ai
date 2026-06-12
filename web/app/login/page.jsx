"use client";

import { useRouter } from "next/navigation";
import Logo from "@/components/Logo";

export default function LoginPage() {
  const router = useRouter();

  function submit(e) {
    e.preventDefault();
    router.push("/welcome");
  }

  return (
    <div className="grid min-h-screen lg:grid-cols-2">
      {/* Hero panel */}
      <div className="relative hidden overflow-hidden bg-gradient-to-br from-teal-400 via-emerald-500 to-emerald-700 lg:block">
        <div className="absolute inset-0 bg-[radial-gradient(120%_120%_at_0%_0%,rgba(255,255,255,.18),transparent_60%)]" />
        <div className="absolute left-8 top-8 flex items-center gap-2 text-white">
          <Logo className="h-7 w-7 [&_path]:fill-white" />
          <span className="text-lg font-semibold">Brainiacs AI</span>
        </div>
        <p className="absolute bottom-12 left-8 right-12 text-2xl font-semibold leading-snug text-white">
          A curriculum-aware AI tutoring platform for teaching programming fundamentals
          to beginners.
        </p>
      </div>

      {/* Form panel */}
      <div className="flex items-center justify-center bg-white px-6 py-10">
        <form onSubmit={submit} className="w-full max-w-sm">
          <div className="mb-8 flex items-center gap-2 lg:hidden">
            <Logo /> <span className="text-lg font-semibold">Brainiacs AI</span>
          </div>
          <h1 className="text-2xl font-semibold">Login to continue</h1>
          <p className="mt-1 text-sm text-body">
            Welcome back, enter your credentials to continue
          </p>

          <label className="mt-6 block text-sm font-medium text-ink">Username</label>
          <input
            type="text"
            defaultValue="c.izabayo@alustudent.com"
            placeholder="Enter your username"
            className="mt-1 w-full rounded-xl border border-line px-3.5 py-2.5 text-sm focus:border-brand-500 focus:outline-none"
          />

          <label className="mt-4 block text-sm font-medium text-ink">Password</label>
          <input
            type="password"
            defaultValue="demo-password"
            placeholder="Enter your Password"
            className="mt-1 w-full rounded-xl border border-line px-3.5 py-2.5 text-sm focus:border-brand-500 focus:outline-none"
          />

          <div className="mt-3 flex items-center justify-between text-sm">
            <label className="flex items-center gap-2 text-body">
              <input type="checkbox" defaultChecked className="accent-brand-600" /> Remember me
            </label>
            <a href="#" className="text-brand-600 hover:underline">Forgot Password ?</a>
          </div>

          <button
            type="submit"
            className="mt-6 w-full rounded-xl bg-brand-600 py-3 font-medium text-white transition hover:bg-brand-700"
          >
            Log in
          </button>

          <div className="my-6 flex items-center gap-3 text-xs text-slate-400">
            <span className="h-px flex-1 bg-line" /> OR <span className="h-px flex-1 bg-line" />
          </div>
          <p className="text-center text-sm text-body">
            Having problems with login?{" "}
            <a href="#" className="text-brand-600 hover:underline">Contact your school admin</a>
          </p>
        </form>
      </div>
    </div>
  );
}
