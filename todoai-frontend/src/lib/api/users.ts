import { User } from "@/types/user";
import apiClient from "./client";

export const usersApi = {
  getMe: () => apiClient.get<User>("/users/me"),
  updateMe: (data: { name?: string; avatar_url?: string }) =>
    apiClient.patch<User>("/users/me", data),
  list: () => apiClient.get<User[]>("/users"),
};
