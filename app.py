from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from todoist_api_python.api import TodoistAPI
from typing import List

app = FastAPI()

# Request models for input validation
class APIKey(BaseModel):
    api_key: str

class TaskDetails(BaseModel):
    api_key: str
    content: str
    due_string: str
    due_lang: str = "en"
    priority: int = 4
    description: str

class TaskUpdateDetails(BaseModel):
    api_key: str
    task_id: str
    content: str
    description: str
    priority: int = 4

class ProjectDetails(BaseModel):
    api_key: str
    name: str

class ProjectID(BaseModel):
    api_key: str
    project_id: str

# 1. Get all tasks
@app.post("/get_tasks/")
def get_tasks(api_key: APIKey):
    try:
        api = TodoistAPI(api_key.api_key)
        tasks = api.get_tasks()
        return tasks
    except Exception as error:
        raise HTTPException(status_code=500, detail=str(error))

# 2. Add a task
@app.post("/add_task/")
def add_task(task_details: TaskDetails):
    try:
        api = TodoistAPI(task_details.api_key)
        task = api.add_task(
            content=task_details.content,
            due_string=task_details.due_string,
            due_lang=task_details.due_lang,
            priority=task_details.priority,
            description=task_details.description
        )
        return task
    except Exception as error:
        raise HTTPException(status_code=500, detail=str(error))

# 3. Update a task
@app.post("/update_task/")
def update_task(task_update: TaskUpdateDetails):
    try:
        api = TodoistAPI(task_update.api_key)
        is_success = api.update_task(task_id=task_update.task_id,
                                     content=task_update.content,
                                     description=task_update.description,
                                     priority=task_update.priority)
        return {"success": is_success}
    except Exception as error:
        raise HTTPException(status_code=500, detail=str(error))

# 4. Close a task
@app.post("/close_task/")
def close_task(task_id: TaskUpdateDetails):
    try:
        api = TodoistAPI(task_id.api_key)
        is_success = api.close_task(task_id=task_id.task_id)
        return {"success": is_success}
    except Exception as error:
        raise HTTPException(status_code=500, detail=str(error))

# 5. Reopen a task
@app.post("/reopen_task/")
def reopen_task(task_id: TaskUpdateDetails):
    try:
        api = TodoistAPI(task_id.api_key)
        is_success = api.reopen_task(task_id=task_id.task_id)
        return {"success": is_success}
    except Exception as error:
        raise HTTPException(status_code=500, detail=str(error))

# 6. Get all projects
@app.post("/get_projects/")
def get_projects(api_key: APIKey):
    try:
        api = TodoistAPI(api_key.api_key)
        projects = api.get_projects()
        return projects
    except Exception as error:
        raise HTTPException(status_code=500, detail=str(error))

# 7. Add a project
@app.post("/add_project/")
def add_project(project_details: ProjectDetails):
    try:
        api = TodoistAPI(project_details.api_key)
        project = api.add_project(name=project_details.name)
        return project
    except Exception as error:
        raise HTTPException(status_code=500, detail=str(error))

# 8. Get project by ID
@app.post("/get_project/")
def get_project(project_id: ProjectID):
    try:
        api = TodoistAPI(project_id.api_key)
        project = api.get_project(project_id=project_id.project_id)
        return project
    except Exception as error:
        raise HTTPException(status_code=500, detail=str(error))

# 9. Get sections in a project
@app.post("/get_sections/")
def get_sections(project_id: ProjectID):
    try:
        api = TodoistAPI(project_id.api_key)
        sections = api.get_sections(project_id=project_id.project_id)
        return sections
    except Exception as error:
        raise HTTPException(status_code=500, detail=str(error))
