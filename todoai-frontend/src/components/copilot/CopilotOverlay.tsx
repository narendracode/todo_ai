"use client";
import { useSession } from "next-auth/react";
import { CopilotKit } from "@copilotkit/react-core";
import { CopilotPopup } from "@copilotkit/react-ui";
import "@copilotkit/react-ui/styles.css";

export default function CopilotOverlay() {
  const { data: session } = useSession();

  // Don't render until the session (and backend token) is ready.
  if (!session?.backendAccessToken) return null;

  return (
    <CopilotKit
      runtimeUrl="/api/copilotkit"
    >
      <CopilotPopup
        instructions="You are an AI assistant for a task scheduling application called TodoAI. Help users manage their tasks, priorities, deadlines, and schedules. You can answer questions about their tasks, suggest priorities, and provide scheduling advice."
        labels={{
          title: "TodoAI Assistant",
          initial: "Hi! I'm your AI task assistant. How can I help you manage your tasks today?",
          placeholder: "Ask me anything about your tasks...",
        }}
      />
    </CopilotKit>
  );
}
