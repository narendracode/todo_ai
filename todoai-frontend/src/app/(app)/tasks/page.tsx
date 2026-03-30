"use client";
import { useEffect } from "react";
import { useAppDispatch, useAppSelector } from "@/store/hooks";
import { fetchTasks, selectAllTasks } from "@/store/slices/tasksSlice";
import { openTaskDialog } from "@/store/slices/uiSlice";
import { TaskCard } from "@/components/tasks/TaskCard";
import { Button } from "@/components/ui/button";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import { Plus } from "lucide-react";
import { useState } from "react";

export default function TasksPage() {
  const dispatch = useAppDispatch();
  const tasks = useAppSelector(selectAllTasks);
  const { status, total, page, pages } = useAppSelector((s) => s.tasks);
  const [statusFilter, setStatusFilter] = useState<string>("all");
  const [priorityFilter, setPriorityFilter] = useState<string>("all");

  useEffect(() => {
    dispatch(
      fetchTasks({
        status: statusFilter === "all" ? undefined : statusFilter,
        priority: priorityFilter === "all" ? undefined : priorityFilter,
      })
    );
  }, [dispatch, statusFilter, priorityFilter]);

  return (
    <div className="p-6 space-y-4">
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-bold">Tasks</h1>
        <Button onClick={() => dispatch(openTaskDialog(null))}>
          <Plus className="h-4 w-4 mr-2" />
          New Task
        </Button>
      </div>

      <div className="flex gap-3 flex-wrap">
        <Select value={statusFilter} onValueChange={setStatusFilter}>
          <SelectTrigger className="w-36">
            <SelectValue placeholder="All statuses" />
          </SelectTrigger>
          <SelectContent>
            <SelectItem value="all">All statuses</SelectItem>
            <SelectItem value="todo">Todo</SelectItem>
            <SelectItem value="in_progress">In Progress</SelectItem>
            <SelectItem value="done">Done</SelectItem>
            <SelectItem value="cancelled">Cancelled</SelectItem>
          </SelectContent>
        </Select>

        <Select value={priorityFilter} onValueChange={setPriorityFilter}>
          <SelectTrigger className="w-36">
            <SelectValue placeholder="All priorities" />
          </SelectTrigger>
          <SelectContent>
            <SelectItem value="all">All priorities</SelectItem>
            <SelectItem value="low">Low</SelectItem>
            <SelectItem value="medium">Medium</SelectItem>
            <SelectItem value="high">High</SelectItem>
            <SelectItem value="urgent">Urgent</SelectItem>
          </SelectContent>
        </Select>

        <span className="text-sm text-muted-foreground self-center">
          {total} task{total !== 1 ? "s" : ""}
        </span>
      </div>

      <div className="space-y-3">
        {status === "loading" && (
          <p className="text-muted-foreground text-sm">Loading tasks...</p>
        )}
        {tasks.length === 0 && status === "succeeded" && (
          <div className="text-center py-12 text-muted-foreground">
            <p>No tasks found.</p>
            <Button
              variant="link"
              onClick={() => dispatch(openTaskDialog(null))}
              className="mt-2"
            >
              Create your first task
            </Button>
          </div>
        )}
        {tasks.map((task) => (
          <TaskCard key={task.id} task={task} />
        ))}
      </div>

      {pages > 1 && (
        <div className="flex justify-center gap-2 pt-4">
          <span className="text-sm text-muted-foreground">
            Page {page} of {pages}
          </span>
        </div>
      )}
    </div>
  );
}
