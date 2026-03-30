"use client";
import { useEffect } from "react";
import { useAppDispatch, useAppSelector } from "@/store/hooks";
import { fetchTasks, selectAllTasks } from "@/store/slices/tasksSlice";
import { openTaskDialog } from "@/store/slices/uiSlice";
import { TaskCard } from "@/components/tasks/TaskCard";
import { Button } from "@/components/ui/button";
import { Plus } from "lucide-react";

export default function DashboardPage() {
  const dispatch = useAppDispatch();
  const tasks = useAppSelector(selectAllTasks);
  const { total, status } = useAppSelector((s) => s.tasks);

  useEffect(() => {
    dispatch(fetchTasks({ size: 5 }));
  }, [dispatch]);

  const todo = tasks.filter((t) => t.status === "todo").length;
  const inProgress = tasks.filter((t) => t.status === "in_progress").length;
  const done = tasks.filter((t) => t.status === "done").length;

  return (
    <div className="p-6 space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-bold">Dashboard</h1>
        <Button onClick={() => dispatch(openTaskDialog(null))}>
          <Plus className="h-4 w-4 mr-2" />
          New Task
        </Button>
      </div>

      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        {[
          { label: "Total", value: total, color: "text-foreground" },
          { label: "Todo", value: todo, color: "text-blue-600" },
          { label: "In Progress", value: inProgress, color: "text-yellow-600" },
          { label: "Done", value: done, color: "text-green-600" },
        ].map(({ label, value, color }) => (
          <div key={label} className="rounded-lg border bg-card p-4">
            <p className="text-sm text-muted-foreground">{label}</p>
            <p className={`text-3xl font-bold mt-1 ${color}`}>{value}</p>
          </div>
        ))}
      </div>

      <div className="space-y-3">
        <h2 className="text-lg font-semibold">Recent Tasks</h2>
        {status === "loading" && (
          <p className="text-muted-foreground text-sm">Loading...</p>
        )}
        {tasks.length === 0 && status === "succeeded" && (
          <p className="text-muted-foreground text-sm">
            No tasks yet. Create your first task!
          </p>
        )}
        {tasks.map((task) => (
          <TaskCard key={task.id} task={task} />
        ))}
      </div>
    </div>
  );
}
