import { CopilotRuntime, EmptyAdapter, copilotRuntimeNextJSAppRouterEndpoint } from "@copilotkit/runtime";
import { AbstractAgent, EventType, type RunAgentInput, type BaseEvent } from "@ag-ui/client";
import { Observable } from "rxjs";

const BACKEND_URL =
  process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000/api/v1";

/**
 * Custom agent that streams responses from the FastAPI backend.
 *
 * CopilotKit v1.54 uses AbstractAgent (@ag-ui/client) as its primary
 * execution model. Providing a custom agent bypasses the built-in LLM
 * provider resolution (which would fail with no API key configured in the
 * frontend) and routes requests directly to our FastAPI streaming endpoint.
 */
class FastAPIAgent extends AbstractAgent {
  run(input: RunAgentInput): Observable<BaseEvent> {
    return new Observable((subscriber) => {
      const execute = async () => {
        // Find the most recent user message to use as the query
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

        const url = `${BACKEND_URL}/ai/stream-answer?query=${encodeURIComponent(query)}`;
        const response = await fetch(url);

        if (!response.ok || !response.body) {
          throw new Error(`Backend returned ${response.status} for ${url}`);
        }

        const reader = response.body.getReader();
        const decoder = new TextDecoder();

        while (true) {
          const { done, value } = await reader.read();
          if (done) break;
          const chunk = decoder.decode(value, { stream: true });
          if (chunk) {
            subscriber.next({
              type: EventType.TEXT_MESSAGE_CONTENT,
              messageId,
              delta: chunk,
            } as BaseEvent);
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

const runtime = new CopilotRuntime({
  // Providing a default agent prevents the runtime from creating a BuiltInAgent
  // (which would fail resolving a provider/model/API key from EmptyAdapter).
  agents: { default: new FastAPIAgent() },
});

export const POST = async (req: Request) => {
  const { handleRequest } = copilotRuntimeNextJSAppRouterEndpoint({
    runtime,
    // EmptyAdapter satisfies the type requirement; actual work is done
    // by FastAPIAgent so the adapter's process() is never invoked.
    serviceAdapter: new EmptyAdapter(),
    endpoint: "/api/copilotkit",
  });

  return handleRequest(req);
};
