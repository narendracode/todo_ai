import NextAuth from "next-auth";
import Google from "next-auth/providers/google";

const API_URL = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000/api/v1";

// Refresh the backend access token using the refresh token
async function refreshBackendToken(refreshToken: string) {
  const res = await fetch(`${API_URL}/auth/refresh`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ refresh_token: refreshToken }),
  });
  if (!res.ok) return null;
  return res.json();
}

export const { handlers, auth, signIn, signOut } = NextAuth({
  providers: [
    Google({
      clientId: process.env.AUTH_GOOGLE_ID,
      clientSecret: process.env.AUTH_GOOGLE_SECRET,
    }),
  ],
  callbacks: {
    async jwt({ token, account }) {
      // Initial sign-in: exchange Google id_token for backend tokens
      if (account?.id_token) {
        try {
          const res = await fetch(`${API_URL}/auth/google`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ id_token: account.id_token }),
          });
          if (res.ok) {
            const data = await res.json();
            token.backendAccessToken = data.access_token;
            token.backendRefreshToken = data.refresh_token;
            // Expire 1 minute before the real 15-min expiry to avoid edge cases
            token.backendTokenExpiresAt = Date.now() + 14 * 60 * 1000;
          } else {
            console.error("Backend auth/google failed:", res.status, await res.text());
          }
        } catch (err) {
          console.error("Backend unreachable during token exchange:", err);
        }
        return token;
      }

      // Subsequent requests: refresh if the access token has expired or expiry is unknown
      const expired =
        typeof token.backendTokenExpiresAt !== "number" ||
        Date.now() >= token.backendTokenExpiresAt;

      if (token.backendRefreshToken && expired) {
        try {
          const data = await refreshBackendToken(token.backendRefreshToken as string);
          if (data?.access_token) {
            token.backendAccessToken = data.access_token;
            token.backendTokenExpiresAt = Date.now() + 14 * 60 * 1000;
          } else {
            // Refresh token is also invalid — clear everything
            token.backendAccessToken = undefined;
            token.backendRefreshToken = undefined;
            token.backendTokenExpiresAt = undefined;
          }
        } catch (err) {
          console.error("Backend token refresh failed:", err);
          token.backendAccessToken = undefined;
          token.backendRefreshToken = undefined;
          token.backendTokenExpiresAt = undefined;
        }
      }

      return token;
    },
    async session({ session, token }) {
      session.backendAccessToken = token.backendAccessToken as string | undefined;
      return session;
    },
  },
  pages: {
    signIn: "/login",
  },
});
