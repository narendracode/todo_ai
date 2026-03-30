"use client";
import { Sidebar } from "./Sidebar";
import { TaskDialog } from "@/components/tasks/TaskDialog";

export function AppShell({ children }: { children: React.ReactNode }) {
  return (
    <div className="flex min-h-screen">
      <Sidebar />
      <main className="flex-1 overflow-auto">
        {children}
      </main>
      <TaskDialog />
    </div>
  );
}
