"use client";
import { Task } from "@/types/task";
import { PriorityBadge } from "./PriorityBadge";
import { StatusBadge } from "./StatusBadge";
import { Button } from "@/components/ui/button";
import { useAppDispatch } from "@/store/hooks";
import { openTaskDialog } from "@/store/slices/uiSlice";
import { deleteTask } from "@/store/slices/tasksSlice";
import { format } from "date-fns";
import { Pencil, Trash2, RefreshCw } from "lucide-react";

export function TaskCard({ task }: { task: Task }) {
  const dispatch = useAppDispatch();

  return (
    <div className="rounded-lg border bg-card p-4 shadow-sm hover:shadow-md transition-shadow">
      <div className="flex items-start justify-between gap-2">
        <div className="flex-1 min-w-0">
          <div className="flex items-center gap-2 flex-wrap">
            <h3 className="font-medium truncate">{task.title}</h3>
            {task.is_recurring && (
              <RefreshCw className="h-3 w-3 text-muted-foreground shrink-0" />
            )}
          </div>
          {task.description && (
            <p className="text-sm text-muted-foreground mt-1 line-clamp-2">
              {task.description}
            </p>
          )}
          <div className="flex items-center gap-2 mt-2 flex-wrap">
            <PriorityBadge priority={task.priority} />
            <StatusBadge status={task.status} />
            {task.time_from && (
              <span className="text-xs text-muted-foreground">
                {format(new Date(task.time_from), "MMM d, HH:mm")}
              </span>
            )}
          </div>
        </div>
        <div className="flex gap-1 shrink-0">
          <Button
            size="icon"
            variant="ghost"
            className="h-8 w-8"
            onClick={() => dispatch(openTaskDialog(task.id))}
          >
            <Pencil className="h-4 w-4" />
          </Button>
          <Button
            size="icon"
            variant="ghost"
            className="h-8 w-8 text-destructive hover:text-destructive"
            onClick={() => dispatch(deleteTask(task.id))}
          >
            <Trash2 className="h-4 w-4" />
          </Button>
        </div>
      </div>
    </div>
  );
}
