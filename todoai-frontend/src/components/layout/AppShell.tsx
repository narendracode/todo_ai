"use client";
import dynamic from "next/dynamic";
import { Sidebar } from "./Sidebar";
import { TaskDialog } from "@/components/tasks/TaskDialog";

// CopilotKit pulls in @a2ui/lit which references HTMLElement at module load time.
// Dynamic import with ssr:false keeps it entirely out of the SSR bundle.
const CopilotOverlay = dynamic(
  () => import("@/components/copilot/CopilotOverlay"),
  { ssr: false }
);

export function AppShell({ children }: { children: React.ReactNode }) {
  return (
    <div className="flex min-h-screen">
      <Sidebar />
      <main className="flex-1 overflow-auto">
        {children}
      </main>
      <TaskDialog />
      <CopilotOverlay />
    </div>
  );
}
