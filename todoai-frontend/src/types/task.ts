export type Priority = "low" | "medium" | "high" | "urgent";
export type TaskStatus = "todo" | "in_progress" | "done" | "cancelled";
export type Visibility = "private" | "shared" | "public";

export interface Task {
  id: string;
  owner_id: string;
  assigned_to_id: string | null;
  title: string;
  description: string | null;
  priority: Priority;
  status: TaskStatus;
  visibility: Visibility;
  time_from: string | null;
  time_to: string | null;
  expiry_date: string | null;
  is_recurring: boolean;
  recurrence_rule: string | null;
  created_at: string;
  updated_at: string;
}

export interface PaginatedTasks {
  items: Task[];
  total: number;
  page: number;
  size: number;
  pages: number;
}

export interface TaskCreate {
  title: string;
  description?: string;
  priority?: Priority;
  status?: TaskStatus;
  visibility?: Visibility;
  time_from?: string;
  time_to?: string;
  expiry_date?: string;
  is_recurring?: boolean;
  recurrence_rule?: string;
  assigned_to_id?: string;
}

export interface TaskUpdate extends Partial<TaskCreate> {}

export interface CalendarEvent {
  id: string;
  title: string;
  start: string;
  end: string;
  allDay: boolean;
  backgroundColor: string;
  extendedProps: {
    task_id: string;
    priority: Priority;
    status: TaskStatus;
    is_recurring: boolean;
  };
}
