import "./globals.css";

export const metadata = {
  title: "Brainiacs AI",
  description: "Adaptive tutoring for the fundamentals of programming.",
};

export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <body>
        <header className="border-b border-gray-200 bg-white">
          <div className="mx-auto max-w-6xl px-6 py-4 flex items-center justify-between">
            <a href="/" className="text-xl font-semibold tracking-tight">
              Brainiacs <span className="text-calm">AI</span>
            </a>
            <span className="text-sm text-gray-500">Programming fundamentals · pseudocode only</span>
          </div>
        </header>
        <main className="mx-auto max-w-6xl px-6 py-8">{children}</main>
      </body>
    </html>
  );
}
