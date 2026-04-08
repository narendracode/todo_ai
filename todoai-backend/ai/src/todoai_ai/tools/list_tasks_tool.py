from typing import Type

import httpx
from langchain_core.tools import BaseTool
from pydantic import BaseModel, Field


class ListTasksInput(BaseModel):
    status: str | None = Field(
        None,
        description="Filter by status. One of: todo, in_progress, done, cancelled",
    )
    priority: str | None = Field(
        None,
        description="Filter by priority. One of: low, medium, high, urgent",
    )
    page: int = Field(1, description="Page number (1-based, default 1)")
    size: int = Field(20, description="Tasks per page (default 20)")


class ListTasksTool(BaseTool):
    name: str = "list_tasks"
    description: str = (
        "List the current user's tasks. "
        "Optionally filter by status (todo/in_progress/done/cancelled) "
        "or priority (low/medium/high/urgent)."
    )
    args_schema: Type[BaseModel] = ListTasksInput

    api_base_url: str
    access_token: str

    def _run(self, status: str | None = None, priority: str | None = None, page: int = 1, size: int = 20) -> str:
        params: dict = {"page": page, "size": size}
        if status:
            params["status"] = status
        if priority:
            params["priority"] = priority
        with httpx.Client() as client:
            r = client.get(
                f"{self.api_base_url}/tasks",
                params=params,
                headers={"Authorization": f"Bearer {self.access_token}"},
                timeout=10,
            )
        if not r.is_success:
            return f"Failed to list tasks: HTTP {r.status_code} — {r.text}"
        data = r.json()
        items = data.get("items", [])
        if not items:
            return "No tasks found matching the criteria."
        lines = [f"Found {data['total']} task(s) (page {data['page']}/{data['pages']}):"]
        for t in items:
            due = f", due {t['expiry_date']}" if t.get("expiry_date") else ""
            lines.append(
                f"- [{t['id']}] {t['title']} | {t['priority']} priority | {t['status']}{due}"
            )
        return "\n".join(lines)

    async def _arun(self, status: str | None = None, priority: str | None = None, page: int = 1, size: int = 20) -> str:
        params: dict = {"page": page, "size": size}
        if status:
            params["status"] = status
        if priority:
            params["priority"] = priority
        async with httpx.AsyncClient() as client:
            r = await client.get(
                f"{self.api_base_url}/tasks",
                params=params,
                headers={"Authorization": f"Bearer {self.access_token}"},
                timeout=10,
            )
        if not r.is_success:
            return f"Failed to list tasks: HTTP {r.status_code} — {r.text}"
        data = r.json()
        items = data.get("items", [])
        if not items:
            return "No tasks found matching the criteria."
        lines = [f"Found {data['total']} task(s) (page {data['page']}/{data['pages']}):"]
        for t in items:
            due = f", due {t['expiry_date']}" if t.get("expiry_date") else ""
            lines.append(
                f"- [{t['id']}] {t['title']} | {t['priority']} priority | {t['status']}{due}"
            )
        return "\n".join(lines)
