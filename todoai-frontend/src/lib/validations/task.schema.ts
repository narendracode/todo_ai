import { z } from "zod";

export const taskSchema = z.object({
  title: z.string().min(1, "Title is required").max(500),
  description: z.string().optional(),
  priority: z.enum(["low", "medium", "high", "urgent"]).default("medium"),
  status: z.enum(["todo", "in_progress", "done", "cancelled"]).default("todo"),
  visibility: z.enum(["private", "shared", "public"]).default("private"),
  time_from: z.string().optional(),
  time_to: z.string().optional(),
  expiry_date: z.string().optional(),
  is_recurring: z.boolean().default(false),
  recurrence_rule: z.string().optional(),
  assigned_to_id: z.string().uuid().optional(),
});

export type TaskFormValues = z.infer<typeof taskSchema>;
