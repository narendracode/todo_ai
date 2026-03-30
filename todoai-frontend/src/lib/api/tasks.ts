import { PaginatedTasks, Task, TaskCreate, TaskUpdate } from "@/types/task";
import apiClient from "./client";

export const tasksApi = {
  list: (params?: {
    status?: string;
    priority?: string;
    assigned_to?: string;
    page?: number;
    size?: number;
  }) => apiClient.get<PaginatedTasks>("/tasks", { params }),

  get: (id: string) => apiClient.get<Task>(`/tasks/${id}`),

  create: (data: TaskCreate) => apiClient.post<Task>("/tasks", data),

  update: (id: string, data: TaskUpdate) =>
    apiClient.patch<Task>(`/tasks/${id}`, data),

  delete: (id: string) => apiClient.delete(`/tasks/${id}`),

  addShare: (taskId: string, userId: string, canEdit = false) =>
    apiClient.post(`/tasks/${taskId}/shares`, { user_id: userId, can_edit: canEdit }),

  removeShare: (taskId: string, userId: string) =>
    apiClient.delete(`/tasks/${taskId}/shares/${userId}`),
};
