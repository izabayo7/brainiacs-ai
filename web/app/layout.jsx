import "./globals.css";
import Logo from "@/components/Logo";

export const metadata = {
  title: "Brainiacs AI",
  description: "A curriculum-aware AI tutor for the fundamentals of programming.",
};

export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <body>
        <header className="sticky top-0 z-20 border-b border-line bg-white/90 backdrop-blur">
          <div className="mx-auto flex max-w-6xl items-center justify-between px-6 py-3">
            <a href="/" className="flex items-center gap-2">
              <Logo />
              <span className="text-lg font-semibold tracking-tight">
                Brainiacs <span className="text-brand-600">AI</span>
              </span>
            </a>
            <nav className="hidden items-center gap-1 text-sm font-medium text-body md:flex">
              <a href="/" className="rounded-lg px-3 py-1.5 hover:bg-mist hover:text-ink">Dashboard</a>
              <a href="/" className="rounded-lg px-3 py-1.5 hover:bg-mist hover:text-ink">Concepts</a>
              <a href="/" className="rounded-lg px-3 py-1.5 hover:bg-mist hover:text-ink">Progress</a>
            </nav>
            <span className="rounded-full bg-brand-50 px-3 py-1 font-mono text-xs text-brand-700">
              pseudocode-only
            </span>
          </div>
        </header>
        <main className="mx-auto max-w-6xl px-6 py-8">{children}</main>
      </body>
    </html>
  );
}
