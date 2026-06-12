import "./globals.css";

export const metadata = {
  title: "Brainiacs AI",
  description: "A curriculum-aware AI tutor for the fundamentals of programming.",
};

export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
