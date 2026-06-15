"use client";

import { useSession, signOut } from "next-auth/react";

export default function UserMenu() {
  const { data: session } = useSession();
  const user = session?.user;
  if (!user) return null;

  return (
    <div className="flex items-center gap-3">
      <div className="flex items-center gap-2 rounded-xl border border-line bg-white px-2.5 py-1.5 shadow-card">
        {user.image ? (
          // eslint-disable-next-line @next/next/no-img-element
          <img src={user.image} alt="" className="h-7 w-7 rounded-full object-cover" />
        ) : (
          <span className="grid h-7 w-7 place-items-center rounded-full bg-brand-600 text-xs font-semibold text-white">
            {(user.name || user.email || "?").slice(0, 1).toUpperCase()}
          </span>
        )}
        <span className="hidden text-sm font-medium text-ink sm:block">{user.name}</span>
      </div>
      <button
        onClick={() => signOut({ callbackUrl: "/login" })}
        className="rounded-lg px-3 py-1.5 text-sm font-medium text-body hover:bg-mist hover:text-ink"
      >
        Sign out
      </button>
    </div>
  );
}
