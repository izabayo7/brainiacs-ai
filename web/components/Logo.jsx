// Brainiacs AI mark — a simple stylised brain/cloud, matching the Figma logo.
export default function Logo({ className = "h-7 w-7" }) {
  return (
    <svg className={className} viewBox="0 0 32 32" fill="none" aria-hidden="true">
      <path
        d="M11 6.5a4.2 4.2 0 0 0-4.1 3.2A4 4 0 0 0 6 17.3 4.2 4.2 0 0 0 9.7 24c.5 1.4 1.9 2.4 3.5 2.4 1.2 0 2.3-.6 3-1.5V8.1A3.7 3.7 0 0 0 11 6.5Z"
        fill="#6366f1"
      />
      <path
        d="M21 6.5a4.2 4.2 0 0 1 4.1 3.2A4 4 0 0 1 26 17.3 4.2 4.2 0 0 1 22.3 24c-.5 1.4-1.9 2.4-3.5 2.4-1.2 0-2.3-.6-3-1.5V8.1A3.7 3.7 0 0 1 21 6.5Z"
        fill="#4f46e5"
      />
    </svg>
  );
}
