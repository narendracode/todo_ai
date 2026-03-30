"use client";
import { useAppDispatch, useAppSelector } from "@/store/hooks";
import { closeTaskDialog } from "@/store/slices/uiSlice";
import { createTask, updateTask, selectTaskById } from "@/store/slices/tasksSlice";
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog";
import { TaskForm } from "./TaskForm";
import type { TaskFormValues } from "@/lib/validations/task.schema";

export function TaskDialog() {
  const dispatch = useAppDispatch();
  const { taskDialogOpen, editingTaskId } = useAppSelector((s) => s.ui);
  const editingTask = useAppSelector((s) =>
    editingTaskId ? selectTaskById(s, editingTaskId) : undefined
  );

  const handleSubmit = async (values: TaskFormValues) => {
    const payload = {
      ...values,
      time_from: values.time_from || undefined,
      time_to: values.time_to || undefined,
      expiry_date: values.expiry_date || undefined,
      recurrence_rule: values.recurrence_rule || undefined,
    };
    if (editingTaskId) {
      await dispatch(updateTask({ id: editingTaskId, data: payload }));
    } else {
      await dispatch(createTask(payload));
    }
    dispatch(closeTaskDialog());
  };

  return (
    <Dialog open={taskDialogOpen} onOpenChange={() => dispatch(closeTaskDialog())}>
      <DialogContent className="max-w-xl max-h-[90vh] overflow-y-auto">
        <DialogHeader>
          <DialogTitle>{editingTaskId ? "Edit Task" : "New Task"}</DialogTitle>
        </DialogHeader>
        <TaskForm
          defaultValues={editingTask}
          onSubmit={handleSubmit}
        />
      </DialogContent>
    </Dialog>
  );
}
