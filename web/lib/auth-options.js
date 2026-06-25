import CredentialsProvider from "next-auth/providers/credentials";

const API = process.env.NEXT_PUBLIC_API_BASE_URL || "http://localhost:8000";

// Email/password only — no external identity provider, so no learner identity leaves
// the system (self-hosted, data-sovereign).
export const authOptions = {
  session: { strategy: "jwt" },
  providers: [
    CredentialsProvider({
      name: "Email",
      credentials: { email: {}, password: {} },
      async authorize(credentials) {
        const res = await fetch(`${API}/auth/login`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ email: credentials?.email, password: credentials?.password }),
        });
        if (!res.ok) return null;
        const data = await res.json();
        return {
          id: String(data.user.id),
          name: data.user.name,
          email: data.user.email,
          backendToken: data.access_token,
        };
      },
    }),
  ],
  pages: { signIn: "/login" },
  secret: process.env.NEXTAUTH_SECRET || "dev-only-nextauth-secret-change-me",
  callbacks: {
    async jwt({ token, user }) {
      if (user?.backendToken) {
        token.backendToken = user.backendToken;
        token.uid = user.id;
      }
      return token;
    },
    async session({ session, token }) {
      session.backendToken = token.backendToken || null;
      if (session.user) session.user.id = token.uid || null;
      return session;
    },
  },
};
