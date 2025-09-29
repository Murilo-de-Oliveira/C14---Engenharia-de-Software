from fastapi import FastAPI, HTTPException, status
from typing import List
from .models import Task, TaskCreate
from .database import create_task_db, get_all_tasks_db, get_task_db, update_task_db, delete_task_db

app = FastAPI(
    title="API de gerenciamento de tarefas",
    description="Uma API simples para gerenciar uma lista de tarefas (To-Do List).",
    version="1.0.0"
)

@app.post("/tasks/", response_model=Task, status_code=status.HTTP_201_CREATED)
def create_task(task: TaskCreate):
    """
    Cria uma nova tarefa.
    - **title**: Título da tarefa (obrigatório).
    - **description**: Descrição opcional.
    - **completed**: Status da tarefa (padrão: `False`).
    """
    new_task = Task(id=0, **task.model_dump())
    return create_task_db(new_task)

@app.get("/tasks/", response_model=List[Task], status_code=status.HTTP_200_OK)
def read_all_tasks():
    """
    Retorna todas as tarefas cadastradas.
    """
    return get_all_tasks_db()

@app.get("/tasks/{task_id}", response_model=Task, status_code=status.HTTP_200_OK)
def read_task(task_id: int):
    """
    Retorna os dados de uma tarefa específica pelo seu ID.
    """
    db_task = get_task_db(task_id)
    if db_task is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tarefa não encontrada")
    return db_task

@app.put("/tasks/{task_id}", response_model=Task, status_code=status.HTTP_200_OK)
def update_task(task_id: int, task: TaskCreate):
    """
    Atualiza os dados de uma tarefa existente.
    """
    if get_task_db(task_id) is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tarefa não encontrada")
    
    update_task_data = Task(id=task_id, **task.model_dump())
    return update_task_db(task_id, update_task_data)

@app.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id: int):
    """
    Deleta uma tarefa pelo seu ID.
    """
    if not delete_task_db(task_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tarefa não encontrada")
    return

@app.get("/")
def root():
    return {'status': 'ok'}