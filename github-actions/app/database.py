from typing import Dict, List
from .models import Task

db: Dict[int, Task] = {} #dicionário que servirá como banco de dados provisório
next_task_id = 1 #variável global para ids de tasks

def get_all_tasks_db() -> List[Task]:
    """Retorna todas as tarefas do banco de dados"""
    return list(db.values())

def get_task_db(task_id: int) -> Task | None:
    """Busca uma tarefa pelo seu ID"""
    return db.get(task_id)

def create_task_db(task_data: Task) -> Task:
    """Cria e salva uma tarefa no banco de dados"""
    global next_task_id
    task_data.id = next_task_id
    db[next_task_id] = task_data
    next_task_id += 1
    return task_data

def update_task_db(task_id: int, task_data: Task) -> Task | None:
    """Atualiza uma tarefa existente"""
    if task_id in db:
        db[task_id] = task_data
        return task_data
    return None

def delete_task_db(task_id: int) -> bool:
    """Remove uma tarefa existente"""
    if task_id in db:
        del db[task_id]
        return True
    return False

#Será usada para limpar o banco para realizar os testes
def clear_db():
    """Limpa o banco de dados"""
    global next_task_id
    db.clear()
    next_task_id = 1