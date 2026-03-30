import { createSlice, PayloadAction } from "@reduxjs/toolkit";
import { format, endOfMonth, startOfMonth } from "date-fns";

interface CalendarState {
  activeView: string;
  visibleStart: string;
  visibleEnd: string;
  status: "idle" | "loading" | "succeeded" | "failed";
}

const now = new Date();

const calendarSlice = createSlice({
  name: "calendar",
  initialState: {
    activeView: "dayGridMonth",
    visibleStart: format(startOfMonth(now), "yyyy-MM-dd"),
    visibleEnd: format(endOfMonth(now), "yyyy-MM-dd"),
    status: "idle",
  } as CalendarState,
  reducers: {
    setActiveView: (state, action: PayloadAction<string>) => {
      state.activeView = action.payload;
    },
    setVisibleRange: (
      state,
      action: PayloadAction<{ start: string; end: string }>
    ) => {
      state.visibleStart = action.payload.start;
      state.visibleEnd = action.payload.end;
    },
    setCalendarStatus: (
      state,
      action: PayloadAction<CalendarState["status"]>
    ) => {
      state.status = action.payload;
    },
  },
});

export const { setActiveView, setVisibleRange, setCalendarStatus } =
  calendarSlice.actions;
export default calendarSlice.reducer;
