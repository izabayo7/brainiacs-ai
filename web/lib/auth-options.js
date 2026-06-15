import CredentialsProvider from "next-auth/providers/credentials";
import GoogleProvider from "next-auth/providers/google";

const API = process.env.NEXT_PUBLIC_API_BASE_URL || "http://localhost:8000";
const SYNC_SECRET = process.env.AUTH_SYNC_SECRET || "dev-only-sync-secret";

// Email/password is always available. Google is added only when its OAuth creds
// are configured, so the app runs without them.
const providers = [
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
        image: data.user.avatar_url || null,
        backendToken: data.access_token,
      };
    },
  }),
];

if (process.env.GOOGLE_CLIENT_ID && process.env.GOOGLE_CLIENT_SECRET) {
  providers.unshift(
    GoogleProvider({
      clientId: process.env.GOOGLE_CLIENT_ID,
      clientSecret: process.env.GOOGLE_CLIENT_SECRET,
    })
  );
}

export const authOptions = {
  session: { strategy: "jwt" },
  providers,
  pages: { signIn: "/login" },
  secret: process.env.NEXTAUTH_SECRET || "dev-only-nextauth-secret-change-me",
  callbacks: {
    async jwt({ token, user, account, profile }) {
      // Email/password sign-in: the authorize() result carries the backend token.
      if (user?.backendToken) {
        token.backendToken = user.backendToken;
        token.uid = user.id;
        if (user.image) token.picture = user.image;
      }
      // Google sign-in: sync the verified profile to our backend for a backend token.
      if (account?.provider === "google" && profile) {
        try {
          const res = await fetch(`${API}/auth/google`, {
            method: "POST",
            headers: { "Content-Type": "application/json", "X-Auth-Sync-Secret": SYNC_SECRET },
            body: JSON.stringify({
              email: profile.email,
              name: profile.name,
              avatar_url: profile.picture,
            }),
          });
          if (res.ok) {
            const data = await res.json();
            token.backendToken = data.access_token;
            token.uid = String(data.user.id);
            token.picture = data.user.avatar_url || profile.picture;
          }
        } catch {
          // leave token without backendToken; API calls will 401 and prompt re-login
        }
      }
      return token;
    },
    async session({ session, token }) {
      session.backendToken = token.backendToken || null;
      if (session.user) {
        session.user.id = token.uid || null;
        if (token.picture) session.user.image = token.picture;
      }
      return session;
    },
  },
};
