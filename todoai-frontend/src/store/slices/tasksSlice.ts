import { tasksApi } from "@/lib/api/tasks";
import { Task, TaskCreate, TaskUpdate } from "@/types/task";
import {
  createAsyncThunk,
  createEntityAdapter,
  createSlice,
  PayloadAction,
} from "@reduxjs/toolkit";
import type { RootState } from "../index";

const tasksAdapter = createEntityAdapter<Task>();

export const fetchTasks = createAsyncThunk(
  "tasks/fetchAll",
  async (params?: { status?: string; priority?: string; page?: number; size?: number }) => {
    const res = await tasksApi.list(params);
    return res.data;
  }
);

export const createTask = createAsyncThunk(
  "tasks/create",
  async (data: TaskCreate) => {
    const res = await tasksApi.create(data);
    return res.data;
  }
);

export const updateTask = createAsyncThunk(
  "tasks/update",
  async ({ id, data }: { id: string; data: TaskUpdate }) => {
    const res = await tasksApi.update(id, data);
    return res.data;
  }
);

export const deleteTask = createAsyncThunk(
  "tasks/delete",
  async (id: string) => {
    await tasksApi.delete(id);
    return id;
  }
);

interface TasksState {
  status: "idle" | "loading" | "succeeded" | "failed";
  error: string | null;
  total: number;
  page: number;
  size: number;
  pages: number;
}

const tasksSlice = createSlice({
  name: "tasks",
  initialState: tasksAdapter.getInitialState<TasksState>({
    status: "idle",
    error: null,
    total: 0,
    page: 1,
    size: 20,
    pages: 1,
  }),
  reducers: {
    tasksCleared: tasksAdapter.removeAll,
  },
  extraReducers: (builder) => {
    builder
      .addCase(fetchTasks.pending, (state) => {
        state.status = "loading";
      })
      .addCase(fetchTasks.fulfilled, (state, action) => {
        state.status = "succeeded";
        tasksAdapter.setAll(state, action.payload.items);
        state.total = action.payload.total;
        state.page = action.payload.page;
        state.size = action.payload.size;
        state.pages = action.payload.pages;
      })
      .addCase(fetchTasks.rejected, (state, action) => {
        state.status = "failed";
        state.error = action.error.message ?? "Failed to fetch tasks";
      })
      .addCase(createTask.fulfilled, tasksAdapter.addOne)
      .addCase(updateTask.fulfilled, (state, action) => {
        tasksAdapter.upsertOne(state, action.payload);
      })
      .addCase(deleteTask.fulfilled, (state, action: PayloadAction<string>) => {
        tasksAdapter.removeOne(state, action.payload);
      });
  },
});

export const { tasksCleared } = tasksSlice.actions;
export const {
  selectAll: selectAllTasks,
  selectById: selectTaskById,
  selectIds: selectTaskIds,
} = tasksAdapter.getSelectors((state: RootState) => state.tasks);

export default tasksSlice.reducer;
