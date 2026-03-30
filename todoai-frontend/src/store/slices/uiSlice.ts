import { createSlice, PayloadAction } from "@reduxjs/toolkit";

interface UiState {
  taskDialogOpen: boolean;
  editingTaskId: string | null;
  sidebarCollapsed: boolean;
}

const uiSlice = createSlice({
  name: "ui",
  initialState: {
    taskDialogOpen: false,
    editingTaskId: null,
    sidebarCollapsed: false,
  } as UiState,
  reducers: {
    openTaskDialog: (state, action: PayloadAction<string | null>) => {
      state.taskDialogOpen = true;
      state.editingTaskId = action.payload;
    },
    closeTaskDialog: (state) => {
      state.taskDialogOpen = false;
      state.editingTaskId = null;
    },
    toggleSidebar: (state) => {
      state.sidebarCollapsed = !state.sidebarCollapsed;
    },
  },
});

export const { openTaskDialog, closeTaskDialog, toggleSidebar } =
  uiSlice.actions;
export default uiSlice.reducer;
