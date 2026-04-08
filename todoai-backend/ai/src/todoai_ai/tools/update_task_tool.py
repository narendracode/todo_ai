from typing import Type

import httpx
from langchain_core.tools import BaseTool
from pydantic import BaseModel, Field


class UpdateTaskInput(BaseModel):
    task_id: str = Field(..., description="UUID of the task to update")
    title: str | None = Field(None, description="New title")
    description: str | None = Field(None, description="New description")
    priority: str | None = Field(
        None, description="New priority: low, medium, high, urgent"
    )
    status: str | None = Field(
        None, description="New status: todo, in_progress, done, cancelled"
    )
    time_from: str | None = Field(
        None, description="New start datetime in ISO 8601, e.g. 2026-04-15T09:00:00"
    )
    time_to: str | None = Field(
        None, description="New end datetime in ISO 8601, e.g. 2026-04-15T10:00:00"
    )
    expiry_date: str | None = Field(
        None, description="New due date in YYYY-MM-DD format, e.g. 2026-04-20"
    )


class UpdateTaskTool(BaseTool):
    name: str = "update_task"
    description: str = (
        "Update an existing task. Only the fields you provide will be changed. "
        "Use list_tasks first to get the task_id if you don't have it."
    )
    args_schema: Type[BaseModel] = UpdateTaskInput

    api_base_url: str
    access_token: str

    def _build_payload(self, **kwargs) -> dict:
        return {k: v for k, v in kwargs.items() if v is not None}

    def _run(
        self,
        task_id: str,
        title: str | None = None,
        description: str | None = None,
        priority: str | None = None,
        status: str | None = None,
        time_from: str | None = None,
        time_to: str | None = None,
        expiry_date: str | None = None,
    ) -> str:
        payload = self._build_payload(
            title=title, description=description, priority=priority,
            status=status, time_from=time_from, time_to=time_to, expiry_date=expiry_date,
        )
        if not payload:
            return "No fields provided to update."
        with httpx.Client() as client:
            r = client.patch(
                f"{self.api_base_url}/tasks/{task_id}",
                json=payload,
                headers={"Authorization": f"Bearer {self.access_token}"},
                timeout=10,
            )
        if r.status_code == 404:
            return f"Task {task_id} not found."
        if not r.is_success:
            return f"Failed to update task: HTTP {r.status_code} — {r.text}"
        t = r.json()
        return f"Task updated: [{t['id']}] \"{t['title']}\" | {t['priority']} priority | {t['status']}"

    async def _arun(
        self,
        task_id: str,
        title: str | None = None,
        description: str | None = None,
        priority: str | None = None,
        status: str | None = None,
        time_from: str | None = None,
        time_to: str | None = None,
        expiry_date: str | None = None,
    ) -> str:
        payload = self._build_payload(
            title=title, description=description, priority=priority,
            status=status, time_from=time_from, time_to=time_to, expiry_date=expiry_date,
        )
        if not payload:
            return "No fields provided to update."
        async with httpx.AsyncClient() as client:
            r = await client.patch(
                f"{self.api_base_url}/tasks/{task_id}",
                json=payload,
                headers={"Authorization": f"Bearer {self.access_token}"},
                timeout=10,
            )
        if r.status_code == 404:
            return f"Task {task_id} not found."
        if not r.is_success:
            return f"Failed to update task: HTTP {r.status_code} — {r.text}"
        t = r.json()
        return f"Task updated: [{t['id']}] \"{t['title']}\" | {t['priority']} priority | {t['status']}"
