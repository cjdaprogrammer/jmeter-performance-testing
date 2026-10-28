
from itertools import count

from fastapi import FastAPI, HTTPException, Response, status
from pydantic import BaseModel, Field

app = FastAPI(
    title="TaskFlow API",
    description="A task management API for performance testing practice.",
    version="1.0.0",
)

# In-memory storage for this learning project.
# Data resets whenever the API process restarts.
tasks: dict[int, dict] = {}
task_ids = count(1)


class TaskCreate(BaseModel):
    title: str = Field(min_length=1, max_length=100)
    description: str = Field(default="", max_length=500)
    completed: bool = False


class TaskUpdate(BaseModel):
    title: str = Field(min_length=1, max_length=100)
    description: str = Field(default="", max_length=500)
    completed: bool = False


@app.get("/health")
def health_check():
    return {"status": "healthy"}


@app.get("/tasks")
def list_tasks():
    return list(tasks.values())


@app.post("/tasks", status_code=status.HTTP_201_CREATED)
def create_task(task: TaskCreate):
    task_id = next(task_ids)

    new_task = {
        "id": task_id,
        **task.model_dump(),
    }

    tasks[task_id] = new_task
    return new_task


@app.get("/tasks/{task_id}")
def get_task(task_id: int):
    task = tasks.get(task_id)

    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found",
        )

    return task


@app.put("/tasks/{task_id}")
def update_task(task_id: int, updated_task: TaskUpdate):
    if task_id not in tasks:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found",
        )

    tasks[task_id] = {
        "id": task_id,
        **updated_task.model_dump(),
    }

    return tasks[task_id]


@app.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id: int):
    if task_id not in tasks:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found",
        )

    del tasks[task_id]
    return Response(status_code=status.HTTP_204_NO_CONTENT)
