from typing import Type

import httpx
from langchain_core.tools import BaseTool
from pydantic import BaseModel, Field


class DeleteTaskInput(BaseModel):
    task_id: str = Field(..., description="UUID of the task to delete")


class DeleteTaskTool(BaseTool):
    name: str = "delete_task"
    description: str = (
        "Permanently delete a task. "
        "Use list_tasks first to get the task_id if you don't have it. "
        "Always confirm with the user before deleting."
    )
    args_schema: Type[BaseModel] = DeleteTaskInput

    api_base_url: str
    access_token: str

    def _run(self, task_id: str) -> str:
        with httpx.Client() as client:
            r = client.delete(
                f"{self.api_base_url}/tasks/{task_id}",
                headers={"Authorization": f"Bearer {self.access_token}"},
                timeout=10,
            )
        if r.status_code == 404:
            return f"Task {task_id} not found."
        if r.status_code == 403:
            return f"Permission denied: you are not the owner of task {task_id}."
        if not r.is_success:
            return f"Failed to delete task: HTTP {r.status_code} — {r.text}"
        return f"Task {task_id} has been deleted."

    async def _arun(self, task_id: str) -> str:
        async with httpx.AsyncClient() as client:
            r = await client.delete(
                f"{self.api_base_url}/tasks/{task_id}",
                headers={"Authorization": f"Bearer {self.access_token}"},
                timeout=10,
            )
        if r.status_code == 404:
            return f"Task {task_id} not found."
        if r.status_code == 403:
            return f"Permission denied: you are not the owner of task {task_id}."
        if not r.is_success:
            return f"Failed to delete task: HTTP {r.status_code} — {r.text}"
        return f"Task {task_id} has been deleted."
