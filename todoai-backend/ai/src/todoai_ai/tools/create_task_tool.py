from typing import Type

import httpx
from langchain_core.tools import BaseTool
from pydantic import BaseModel, Field


class CreateTaskInput(BaseModel):
    title: str = Field(..., description="Task title (required)")
    description: str | None = Field(None, description="Optional detailed description")
    priority: str = Field(
        "medium",
        description="Priority level: low, medium, high, urgent (default: medium)",
    )
    status: str = Field(
        "todo",
        description="Initial status: todo, in_progress, done, cancelled (default: todo)",
    )
    time_from: str | None = Field(
        None, description="Scheduled start datetime in ISO 8601, e.g. 2026-04-15T09:00:00 (required)"
    )
    time_to: str | None = Field(
        None, description="Scheduled end datetime in ISO 8601, e.g. 2026-04-15T10:00:00 (required)"
    )
    expiry_date: str | None = Field(
        None, description="Due date in YYYY-MM-DD format, e.g. 2026-04-20 (required)"
    )


class CreateTaskTool(BaseTool):
    name: str = "create_task"
    description: str = (
        "Create a new task for the current user. "
        "Returns the created task details including its ID."
    )
    args_schema: Type[BaseModel] = CreateTaskInput

    api_base_url: str
    access_token: str

    def _build_payload(
        self,
        title: str,
        description: str | None,
        priority: str,
        status: str,
        time_from: str | None,
        time_to: str | None,
        expiry_date: str | None,
    ) -> dict:
        payload: dict = {"title": title, "priority": priority, "status": status}
        if description:
            payload["description"] = description
        if time_from:
            payload["time_from"] = time_from
        if time_to:
            payload["time_to"] = time_to
        if expiry_date:
            payload["expiry_date"] = expiry_date
        return payload

    def _run(
        self,
        title: str,
        description: str | None = None,
        priority: str = "medium",
        status: str = "todo",
        time_from: str | None = None,
        time_to: str | None = None,
        expiry_date: str | None = None,
    ) -> str:
        payload = self._build_payload(title, description, priority, status, time_from, time_to, expiry_date)
        with httpx.Client() as client:
            r = client.post(
                f"{self.api_base_url}/tasks",
                json=payload,
                headers={"Authorization": f"Bearer {self.access_token}"},
                timeout=10,
            )
        if not r.is_success:
            return f"Failed to create task: HTTP {r.status_code} — {r.text}"
        t = r.json()
        return f"Task created: [{t['id']}] \"{t['title']}\" | {t['priority']} priority | {t['status']}"

    async def _arun(
        self,
        title: str,
        description: str | None = None,
        priority: str = "medium",
        status: str = "todo",
        time_from: str | None = None,
        time_to: str | None = None,
        expiry_date: str | None = None,
    ) -> str:
        payload = self._build_payload(title, description, priority, status, time_from, time_to, expiry_date)
        async with httpx.AsyncClient() as client:
            r = await client.post(
                f"{self.api_base_url}/tasks",
                json=payload,
                headers={"Authorization": f"Bearer {self.access_token}"},
                timeout=10,
            )
        if not r.is_success:
            return f"Failed to create task: HTTP {r.status_code} — {r.text}"
        t = r.json()
        return f"Task created: [{t['id']}] \"{t['title']}\" | {t['priority']} priority | {t['status']}"
