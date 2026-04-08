import {
  CopilotRuntime,
  EmptyAdapter,
  copilotRuntimeNextJSAppRouterEndpoint,
} from "@copilotkit/runtime";
import { AbstractAgent, EventType, type RunAgentInput, type BaseEvent } from "@ag-ui/client";
import { Observable } from "rxjs";
import { auth } from "@/auth";

const BACKEND_URL =
  process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000/api/v1";

/**
 * Custom agent that proxies chat to the FastAPI streaming endpoint.
 * Constructed per-request so it carries the caller's JWT token.
 */
class FastAPIAgent extends AbstractAgent {
  private accessToken: string;

  constructor(accessToken: string) {
    super();
    this.accessToken = accessToken;
  }

  async refreshToken(): Promise<string | null> {
    const session = await auth();
    return session?.backendAccessToken ?? null;
  }

  run(input: RunAgentInput): Observable<BaseEvent> {
    return new Observable((subscriber) => {
      const execute = async () => {
        const messages = input.messages ?? [];
        const lastUserMsg = [...messages]
          .reverse()
          .find((m) => m.role === "user");

        const query =
          typeof lastUserMsg?.content === "string" ? lastUserMsg.content : "";

        const messageId = crypto.randomUUID();
        const { threadId, runId } = input;

        subscriber.next({ type: EventType.RUN_STARTED, threadId, runId } as BaseEvent);
        subscriber.next({
          type: EventType.TEXT_MESSAGE_START,
          messageId,
          role: "assistant",
        } as BaseEvent);

        const url = `${BACKEND_URL}/ai/stream-chat`;
        const body = JSON.stringify({ query, chat_history: [], user_id: "" });
        const fetchOptions = (token: string) => ({
          method: "POST",
          headers: {
            Authorization: `Bearer ${token}`,
            "Content-Type": "application/json",
          },
          body,
        });

        let response = await fetch(url, fetchOptions(this.accessToken));

        // If the token was stale/expired, refresh and retry once
        if (response.status === 401) {
          const freshToken = await this.refreshToken();
          if (freshToken) {
            this.accessToken = freshToken;
            response = await fetch(url, fetchOptions(freshToken));
          }
        }

        if (!response.ok || !response.body) {
          throw new Error(`Backend returned ${response.status} for ${url}`);
        }

        const reader = response.body.getReader();
        const decoder = new TextDecoder();
        let buffer = "";

        while (true) {
          const { done, value } = await reader.read();
          if (done) break;
          buffer += decoder.decode(value, { stream: true });

          // Process complete NDJSON lines
          const lines = buffer.split("\n");
          buffer = lines.pop() ?? ""; // keep incomplete trailing line in buffer

          for (const line of lines) {
            if (!line.trim()) continue;
            try {
              const parsed = JSON.parse(line);
              if (parsed.type === "answer" && parsed.content) {
                subscriber.next({
                  type: EventType.TEXT_MESSAGE_CONTENT,
                  messageId,
                  delta: parsed.content,
                } as BaseEvent);
              }
            } catch {
              // skip malformed lines
            }
          }
        }

        subscriber.next({ type: EventType.TEXT_MESSAGE_END, messageId } as BaseEvent);
        subscriber.next({ type: EventType.RUN_FINISHED, threadId, runId } as BaseEvent);
        subscriber.complete();
      };

      execute().catch((err) => subscriber.error(err));
    });
  }
}

export const POST = async (req: Request) => {
  // Read the token from the server-side session so it's always fresh
  // (NextAuth runs the JWT callback — including token refresh — on every auth() call).
  const session = await auth();
  const accessToken = session?.backendAccessToken ?? null;

  if (!accessToken) {
    return new Response("Unauthorized", { status: 401 });
  }

  const runtime = new CopilotRuntime({
    agents: { default: new FastAPIAgent(accessToken) },
  });

  const { handleRequest } = copilotRuntimeNextJSAppRouterEndpoint({
    runtime,
    serviceAdapter: new EmptyAdapter(),
    endpoint: "/api/copilotkit",
  });

  return handleRequest(req);
};
