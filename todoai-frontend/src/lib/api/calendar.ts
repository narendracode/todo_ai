import { CalendarEvent } from "@/types/task";
import apiClient from "./client";

export const calendarApi = {
  getEvents: (start: string, end: string) =>
    apiClient.get<CalendarEvent[]>("/calendar/events", {
      params: { start, end },
    }),
};
