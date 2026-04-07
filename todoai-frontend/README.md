# todoai-frontend

Next.js frontend for the TodoAI task scheduling app — with an AI chat overlay powered by CopilotKit.

## Stack

- **Next.js 15** (App Router, React 19)
- **TypeScript** + Tailwind CSS
- **Radix UI** component primitives
- **NextAuth v5** — Google OAuth
- **Redux Toolkit** — client state management
- **CopilotKit** — floating AI chat overlay (backed by Anthropic Claude)
- **@event-calendar/core** — calendar view
- **React Hook Form + Zod** — form validation

## Setup

### 1. Install dependencies

```bash
npm install
```

### 2. Configure environment

```bash
cp .env.local.example .env.local
# Edit .env.local with your values
```

### 3. Start the dev server

```bash
# From repo root (recommended)
make frontend

# Or directly
npm run dev
```

Open http://localhost:3000

---

## Environment Variables — `.env.local`

| Variable | Required | Description |
|---|---|---|
| `NEXTAUTH_URL` | Yes | App URL — `http://localhost:3000` in development |
| `NEXTAUTH_SECRET` | Yes | Random secret — `openssl rand -hex 32` |
| `AUTH_GOOGLE_ID` | Yes | Google OAuth client ID |
| `AUTH_GOOGLE_SECRET` | Yes | Google OAuth client secret |
| `NEXT_PUBLIC_API_URL` | Yes | Backend base URL — `http://localhost:8000/api/v1` |
| `ANTHROPIC_API_KEY` | Yes | Anthropic API key — used by the CopilotKit chat endpoint at `/api/copilotkit` |

---

## Google OAuth Setup

1. Go to [Google Cloud Console](https://console.cloud.google.com) → APIs & Services → Credentials
2. Create an OAuth 2.0 Client ID (type: **Web application**)
3. Add to **Authorized redirect URIs**:
   ```
   http://localhost:3000/api/auth/callback/google
   ```
4. Copy the Client ID → `AUTH_GOOGLE_ID` and Secret → `AUTH_GOOGLE_SECRET`

---

## AI Chat (CopilotKit)

A floating chat button appears in the bottom-right corner of every authenticated page. Clicking it opens a chat window backed by Anthropic Claude via CopilotKit.

**How it works:**
- The frontend `CopilotKit` provider points to the Next.js API route `/api/copilotkit`
- That route runs `CopilotRuntime` with `AnthropicAdapter` (server-side, uses `ANTHROPIC_API_KEY`)
- The UI component is `CopilotPopup` from `@copilotkit/react-ui`

**Extending the chat:**

Register actions the AI can invoke (e.g. create a task, show a graph) using `useCopilotAction`:

```tsx
import { useCopilotAction } from "@copilotkit/react-core";

useCopilotAction({
  name: "createTask",
  description: "Create a new task for the user",
  parameters: [
    { name: "title", type: "string", description: "Task title" },
    { name: "priority", type: "string", enum: ["low", "medium", "high", "urgent"] },
  ],
  handler: async ({ title, priority }) => {
    // call your API here
  },
});
```

For **human-in-the-loop** (approve / reject) flows, use `renderAndWait`:

```tsx
useCopilotAction({
  name: "deleteTask",
  description: "Delete a task after user confirms",
  parameters: [{ name: "taskId", type: "string" }],
  renderAndWait: ({ taskId, handler }) => (
    <ConfirmDialog
      message={`Delete task ${taskId}?`}
      onConfirm={() => handler("confirmed")}
      onCancel={() => handler("cancelled")}
    />
  ),
});
```

Make the current task list readable by the AI using `useCopilotReadable`:

```tsx
import { useCopilotReadable } from "@copilotkit/react-core";

useCopilotReadable({
  description: "The user's current task list",
  value: tasks,
});
```
