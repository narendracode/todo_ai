"use client";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { taskSchema, TaskFormValues } from "@/lib/validations/task.schema";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Textarea } from "@/components/ui/textarea";
import { Label } from "@/components/ui/label";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import type { Task } from "@/types/task";

interface TaskFormProps {
  defaultValues?: Partial<Task>;
  onSubmit: (values: TaskFormValues) => void;
  isLoading?: boolean;
}

export function TaskForm({ defaultValues, onSubmit, isLoading }: TaskFormProps) {
  const {
    register,
    handleSubmit,
    setValue,
    watch,
    formState: { errors },
  } = useForm<TaskFormValues>({
    resolver: zodResolver(taskSchema),
    defaultValues: {
      title: defaultValues?.title ?? "",
      description: defaultValues?.description ?? "",
      priority: defaultValues?.priority ?? "medium",
      status: defaultValues?.status ?? "todo",
      visibility: defaultValues?.visibility ?? "private",
      time_from: defaultValues?.time_from ?? "",
      time_to: defaultValues?.time_to ?? "",
      expiry_date: defaultValues?.expiry_date ?? "",
      is_recurring: defaultValues?.is_recurring ?? false,
      recurrence_rule: defaultValues?.recurrence_rule ?? "",
      assigned_to_id: defaultValues?.assigned_to_id ?? undefined,
    },
  });

  const isRecurring = watch("is_recurring");

  return (
    <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
      <div className="space-y-1">
        <Label htmlFor="title">Title *</Label>
        <Input id="title" {...register("title")} placeholder="Task title" />
        {errors.title && (
          <p className="text-xs text-destructive">{errors.title.message}</p>
        )}
      </div>

      <div className="space-y-1">
        <Label htmlFor="description">Description</Label>
        <Textarea
          id="description"
          {...register("description")}
          placeholder="Optional description"
          rows={3}
        />
      </div>

      <div className="grid grid-cols-2 gap-4">
        <div className="space-y-1">
          <Label>Priority</Label>
          <Select
            defaultValue={defaultValues?.priority ?? "medium"}
            onValueChange={(v) => setValue("priority", v as TaskFormValues["priority"])}
          >
            <SelectTrigger>
              <SelectValue />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="low">Low</SelectItem>
              <SelectItem value="medium">Medium</SelectItem>
              <SelectItem value="high">High</SelectItem>
              <SelectItem value="urgent">Urgent</SelectItem>
            </SelectContent>
          </Select>
        </div>

        <div className="space-y-1">
          <Label>Status</Label>
          <Select
            defaultValue={defaultValues?.status ?? "todo"}
            onValueChange={(v) => setValue("status", v as TaskFormValues["status"])}
          >
            <SelectTrigger>
              <SelectValue />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="todo">Todo</SelectItem>
              <SelectItem value="in_progress">In Progress</SelectItem>
              <SelectItem value="done">Done</SelectItem>
              <SelectItem value="cancelled">Cancelled</SelectItem>
            </SelectContent>
          </Select>
        </div>
      </div>

      <div className="grid grid-cols-2 gap-4">
        <div className="space-y-1">
          <Label htmlFor="time_from">Start Time</Label>
          <Input
            id="time_from"
            type="datetime-local"
            {...register("time_from")}
          />
        </div>
        <div className="space-y-1">
          <Label htmlFor="time_to">End Time</Label>
          <Input
            id="time_to"
            type="datetime-local"
            {...register("time_to")}
          />
        </div>
      </div>

      <div className="space-y-1">
        <Label htmlFor="expiry_date">Expiry Date</Label>
        <Input id="expiry_date" type="date" {...register("expiry_date")} />
      </div>

      <div className="space-y-1">
        <Label>Visibility</Label>
        <Select
          defaultValue={defaultValues?.visibility ?? "private"}
          onValueChange={(v) => setValue("visibility", v as TaskFormValues["visibility"])}
        >
          <SelectTrigger>
            <SelectValue />
          </SelectTrigger>
          <SelectContent>
            <SelectItem value="private">Private</SelectItem>
            <SelectItem value="shared">Shared</SelectItem>
            <SelectItem value="public">Public</SelectItem>
          </SelectContent>
        </Select>
      </div>

      <div className="flex items-center gap-2">
        <input
          id="is_recurring"
          type="checkbox"
          {...register("is_recurring")}
          className="rounded border-input"
        />
        <Label htmlFor="is_recurring">Recurring task</Label>
      </div>

      {isRecurring && (
        <div className="space-y-1">
          <Label htmlFor="recurrence_rule">Recurrence Rule (RRULE)</Label>
          <Input
            id="recurrence_rule"
            {...register("recurrence_rule")}
            placeholder="e.g. FREQ=WEEKLY;BYDAY=MO,WE,FR"
          />
          <p className="text-xs text-muted-foreground">RFC 5545 RRULE format</p>
        </div>
      )}

      <div className="flex justify-end gap-2 pt-2">
        <Button type="submit" disabled={isLoading}>
          {isLoading ? "Saving..." : "Save Task"}
        </Button>
      </div>
    </form>
  );
}
