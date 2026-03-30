import { configureStore } from "@reduxjs/toolkit";
import calendarReducer from "./slices/calendarSlice";
import tasksReducer from "./slices/tasksSlice";
import uiReducer from "./slices/uiSlice";

export const store = configureStore({
  reducer: {
    tasks: tasksReducer,
    calendar: calendarReducer,
    ui: uiReducer,
  },
});

export type RootState = ReturnType<typeof store.getState>;
export type AppDispatch = typeof store.dispatch;
