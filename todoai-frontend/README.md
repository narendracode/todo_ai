# todoai-frontend

Next.js frontend for the todoai task scheduling app.

## Stack

- Next.js 15 (App Router)
- TypeScript
- Tailwind CSS + Shadcn/ui + Radix UI
- NextAuth v5 (Google OAuth)
- Redux Toolkit
- @event-calendar/core (vkurko/calendar)
- React Hook Form + Zod

## Setup

```bash
# Install dependencies
npm install   # or pnpm install

# Copy env and fill in values
cp .env.local.example .env.local

# Start dev server
npm run dev
```

Open [http://localhost:3000](http://localhost:3000).

## Required Environment Variables

| Variable | Description |
|---|---|
| `NEXTAUTH_URL` | App URL (e.g. http://localhost:3000) |
| `NEXTAUTH_SECRET` | Random secret (openssl rand -hex 32) |
| `AUTH_GOOGLE_ID` | Google OAuth Client ID |
| `AUTH_GOOGLE_SECRET` | Google OAuth Client Secret |
| `NEXT_PUBLIC_API_URL` | Backend API base URL |

## Google OAuth Setup

1. Go to [Google Cloud Console](https://console.cloud.google.com)
2. Create OAuth 2.0 credentials
3. Add `http://localhost:3000/api/auth/callback/google` to Authorized redirect URIs
